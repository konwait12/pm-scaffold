#!/usr/bin/env python3
"""Property-based completeness checker for function-description artifacts.

Goes beyond structural validation to check logical completeness:
1. State machine exhaustiveness: every state × known event → target state defined
2. Exception path coverage: every BR with an exception branch has a recovery path
3. VL↔AC pairing: every validation rule has a corresponding acceptance criterion
4. Rule density: each FUN has sufficient BR+VL+AC coverage

Usage: python3 property_check.py <function-description.md> [--json]
Exit 0 = complete, 1 = gaps found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


def _norm(text: str) -> str:
    """Normalize text for comparison: lowercase, strip brackets/parens content."""
    t = text.lower().strip()
    t = re.sub(r'[（(][^)）]*[)）]', '', t)
    t = re.sub(r'[〔【][^】〕]*[】〕]', '', t)
    return re.sub(r'\s+', '', t)


def _parse_frontmatter(text: str) -> dict[str, str]:
    """Parse YAML frontmatter (``---\\n...\\n---``) into a flat dict.

    Mirrors ``workflow_registry.read_frontmatter`` so the minimum-threshold
    check agrees with the rest of the scaffold on what counts as a required
    frontmatter field.
    """
    match = re.match(r"---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("'\"")
    return result


def check_minimum_threshold(text: str) -> list[dict]:
    """B11: minimum threshold — an artifact must not silent-pass the gate.

    An empty file or a section-less artifact must NOT be reported as complete
    just because the four content checks find nothing to flag. Require:
      1. at least one ``## `` or ``# `` heading section, and
      2. the required frontmatter fields ``artifact_id`` / ``status``.
    Any missing requirement is reported as an ERROR (CRITICAL), not a warning,
    so ``machine_gate`` rejects the artifact with a non-zero exit.
    """
    issues = []
    if not re.search(r"(?m)^#{1,2}\s+\S+", text):
        issues.append({
            "severity": "CRITICAL",
            "check": "minimum_threshold",
            "message": "产物缺少章节标题：必须至少有一个 `## ` 或 `# ` 章节（空文件/无章节产物不得通过）",
        })
    fm = _parse_frontmatter(text)
    for field in ("artifact_id", "status"):
        if not fm.get(field):
            issues.append({
                "severity": "CRITICAL",
                "check": "minimum_threshold",
                "message": f"frontmatter 缺少必备字段 {field}",
            })
    if not issues:
        issues.append({
            "severity": "INFO",
            "check": "minimum_threshold",
            "message": "Minimum threshold: artifact has ≥1 heading section and required frontmatter (artifact_id/status)",
        })
    return issues


def _rule_id_re(prefix: str) -> str:
    """Regex fragment matching a rule/feature ID, with an optional letter suffix.

    Accepts `PREFIX-123` and `PREFIX-123A` (single uppercase letter). OBS-005:
    older checks only matched pure digits (`BR-\\d+`), so suffixed IDs such as
    BR-006A were silently skipped by the rule-density / pairing / exception
    checks and under-counted the rules per FUN.
    """
    return rf"\b{prefix}-\d+[A-Z]?\b"


def parse_sections(text: str) -> dict[str, str]:
    """Extract sections by ## heading."""
    sections = {}
    current = "preamble"
    current_content = []
    for line in text.split("\n"):
        m = re.match(r'^##\s+(.+)', line)
        if m:
            sections[current] = "\n".join(current_content)
            current = _norm(m.group(1))
            current_content = []
        else:
            current_content.append(line)
    sections[current] = "\n".join(current_content)
    return sections


def section_by_keyword(text: str, *keywords: str) -> str:
    """Return the concatenated content of sections whose heading contains any keyword.

    `parse_sections` keys keep their leading numbering (e.g. "5.状态变化"), so we
    match by keyword rather than exact name.
    """
    return "\n".join(
        val for key, val in parse_sections(text).items()
        if any(kw in key for kw in keywords)
    )


def check_state_machine(text: str) -> list[dict]:
    """Check state transition completeness (parses the 状态变化 section only)."""
    issues = []
    # Only parse the 状态变化 section, and read the 6-column table correctly:
    # | STATE | 状态名称 | 触发事件 | 目标状态 | 条件 | 所属 FUN |
    section = section_by_keyword(text, "状态变化")
    state_rows = re.findall(
        r'\|\s*[^|]+\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
        section,
    )
    if not state_rows:
        return [{"severity": "MEDIUM", "check": "state_machine", "message": "No state transition table found in 状态变化 section"}]

    states = set()
    events = set()
    transitions = set()

    for row in state_rows:
        current = _norm(row[0])   # 状态名称
        event = _norm(row[1])     # 触发事件
        target = _norm(row[2])    # 目标状态
        if current and event and target:
            # Skip header rows
            if any(h in current for h in ['状态名称', '当前状态', 'state']):
                continue
            states.add(current)
            events.add(event)
            transitions.add((current, event))

    # Check: every state has at least one outgoing transition (except terminal)
    terminal_keywords = ['完成', '结束', '关闭', '归档', 'done', 'complete', 'closed']
    for state in states:
        if any(kw in state for kw in terminal_keywords):
            continue
        outgoing = [(s, e) for (s, e) in transitions if s == state]
        if not outgoing:
            issues.append({
                "severity": "HIGH",
                "check": "state_machine",
                "message": f"State '{state}' has no outgoing transitions (non-terminal state)",
            })

    # Check: each event transitions from at least one state
    for event in events:
        incoming = [(s, e) for (s, e) in transitions if e == event]
        if not incoming:
            issues.append({
                "severity": "MEDIUM",
                "check": "state_machine",
                "message": f"Event '{event}' triggers no transitions",
            })

    if not issues:
        issues.append({
            "severity": "INFO",
            "check": "state_machine",
            "message": f"State machine: {len(states)} states, {len(events)} events, {len(transitions)} transitions — appears complete",
        })

    return issues


def check_exception_coverage(text: str) -> list[dict]:
    """Check every BR exception branch has a recovery path."""
    issues = []
    # BR table columns: | BR-ID | 规则内容 | 类型 | 触发条件 | 预期行为 | 所属功能 | 来源 |
    # OBS-004: exception semantics are judged from the 规则内容 column (col 2),
    # NOT the 类型 column (col 3). A BR whose 类型 cell says 异常 but whose content
    # carries no exception keyword must NOT be flagged, while a BR whose content
    # contains 失败/异常/拒绝/… must be (the recovery check then applies).
    # Single-character keywords (不/满) are intentionally excluded: against full
    # sentence content they match benign substrings (不同/不改/无效/满足 …) and
    # would re-introduce the exact false positives OBS-004 removes.
    exception_keywords = ['失败', '异常', '超时', '过期', '无法', '拒绝', '禁止', '冲突']
    br_rows = re.findall(
        r'\|\s*(' + _rule_id_re("BR") + r')\s*\|([^|\n]+)\|([^|\n]+)\|([^|\n]+)\|([^|\n]+)\|',
        section_by_keyword(text, "业务规则"),
    )
    exception_brs = []
    for br_id, content, rule_type, trigger, behavior in br_rows:
        content = content.strip()
        if any(kw in content for kw in exception_keywords):
            exception_brs.append({
                "id": br_id,
                "content": content,
                "row": " | ".join(c.strip() for c in (content, rule_type, trigger, behavior)),
            })

    # Exception-handling entries that demonstrably carry a recovery path: an
    # EX/BR row whose text contains a recovery keyword (same table row).
    recovery_keywords = ['恢复', '重试', '重授权', '重新', '联系']
    ex_with_recovery: list[tuple[str, str]] = []
    for line in section_by_keyword(text, "异常").split("\n"):
        m = re.match(r'^\|\s*(EX-\d+[A-Z]?|BR-\d+[A-Z]?)\s*\|(.+)$', line.strip())
        if m and any(kw in m.group(2) for kw in recovery_keywords):
            ex_with_recovery.append((m.group(1), m.group(2)))

    for br in exception_brs:
        br_id = br["id"]
        # A recovery counts when (a) an exception entry with a recovery path cites
        # this BR (e.g. EX 触发条件: 提交时当日已有预约（BR-009）), (b) the BR row
        # cites an EX id that has a recovery (e.g. 预期行为: 异常详情见 EX-001), or
        # (c) the BR row itself spells out the recovery (重试/重新/恢复/联系 …).
        has_recovery = (
            any(br_id in row_text for _, row_text in ex_with_recovery)
            or any(ex_id in br["row"] for ex_id, _ in ex_with_recovery)
            or any(kw in br["row"] for kw in recovery_keywords)
        )
        if not has_recovery:
            issues.append({
                "severity": "HIGH",
                "check": "exception_coverage",
                "message": f"BR {br_id} ('{br['content'][:60]}') 规则内容含异常语义"
                           f"（失败/异常/拒绝 等），但异常处理章节未找到 recovery path"
                           f"（类型列：'{br['row'].split(' | ')[1][:20]}'）",
            })

    if not issues:
        issues.append({
            "severity": "INFO",
            "check": "exception_coverage",
            "message": f"Exception coverage: {len(exception_brs)} exception BRs, all have recovery paths",
        })

    return issues


def check_vl_ac_pairing(text: str) -> list[dict]:
    """Check every VL's owning FUN has a corresponding AC (VL↔AC via 所属 FUN)."""
    issues = []
    vl_section = section_by_keyword(text, "校验规则")
    ac_section = section_by_keyword(text, "验收依据")
    vl_ids = set(re.findall(_rule_id_re("VL"), vl_section))
    ac_ids = set(re.findall(_rule_id_re("AC"), ac_section))

    # FUN is the 5th column in both tables:
    #   VL: | VL-001 | 校验内容 | 校验规则 | 错误提示 | FUN-XXX | 来源 |
    #   AC: | AC-001 | 验收标准 | 量化阈值 | 来源目标 G | FUN-XXX | 优先级 |
    # `[^|\n]` (not `[^|]`) keeps each match on a single table row so a trailing
    # `VL-00X` cell in a field table cannot anchor across newlines and capture
    # a neighbouring 类型 column (布尔/数字/文本) as if it were a FUN id.
    vl_funs = set(re.findall(r'\|\s*VL-\d+[A-Z]?\s*\|(?:[^|\n]*\|){3}\s*([^|\n]+?)\s*\|', vl_section))
    ac_funs = set(re.findall(r'\|\s*AC-\d+[A-Z]?\s*\|(?:[^|\n]*\|){3}\s*([^|\n]+?)\s*\|', ac_section))
    uncovered = {f for f in vl_funs - ac_funs if f and f != "—"}
    for fun in sorted(uncovered):
        issues.append({
            "severity": "MEDIUM",
            "check": "vl_ac_pairing",
            "message": f"FUN {fun} has validation rules (VL) but no acceptance criteria (AC)",
        })

    if not issues:
        issues.append({
            "severity": "INFO",
            "check": "vl_ac_pairing",
            "message": f"VL↔AC pairing: {len(vl_ids)} VLs, {len(ac_ids)} ACs — all VL FUNs covered by ACs",
        })

    return issues


def _id_fun_pairs(section: str, id_prefix: str, gap: int) -> list[tuple[str, str]]:
    """Extract (ID, FUN) pairs from a table section's 所属 FUN column.

    `gap` is the number of cells between the ID cell and the 所属 FUN cell:
      BR: | BR-X | 规则描述 | 类型 | 触发条件 | 约束/逻辑 | FUN-X | 来源 |  → gap=4
      VL: | VL-X | 校验内容 | 校验规则 | 错误提示 | FUN-X | 来源 |        → gap=3
      AC: | AC-X | 验收标准 | 量化阈值 | 来源目标 G | FUN-X | 优先级 |    → gap=3
    `[^|\n]` keeps each match on a single table row (same fix as B1), so a
    non-ID cell can never anchor across newlines.
    """
    pairs: list[tuple[str, str]] = []
    pattern = re.compile(
        r"\|\s*(" + _rule_id_re(id_prefix) + r")\s*\|(?:[^|\n]*\|){"
        + str(gap) + r"}\s*([^|\n]+?)\s*\|"
    )
    for m in pattern.finditer(section):
        fun = re.search(r"\bFUN-\d+[A-Z]?\b", m.group(2))
        if fun:
            pairs.append((m.group(1), fun.group(0)))
    return pairs


def _table_rule_density(text: str) -> list[dict]:
    """Table-based rule density for 功能清单表格 layouts (no `### FUN-XXX`).

    The 功能清单 table defines features (FEA-XXX); FUN IDs are referenced in
    the 功能流程 / 业务规则 / 校验规则 / 验收依据 tables. BR/VL/AC counts are
    aggregated per FUN from the 所属 FUN column of the rule tables, then the
    same density thresholds as the heading-based path are applied. When no FUN
    can be located, keep the B5 "skipped" warning as a fallback.
    """
    issues = []
    br_pairs = _id_fun_pairs(section_by_keyword(text, "业务规则"), "BR", 4)
    vl_pairs = _id_fun_pairs(section_by_keyword(text, "校验规则"), "VL", 3)
    ac_pairs = _id_fun_pairs(section_by_keyword(text, "验收依据"), "AC", 3)

    funs = sorted({fun for _, fun in br_pairs + vl_pairs + ac_pairs})
    if not funs:
        issues.append({
            "severity": "MEDIUM",
            "check": "rule_density",
            "message": "未检测到功能子标题（### FUN-XXX）或表格中的 FUN 引用，规则密度校验跳过",
        })
        return issues

    for fun in funs:
        br_count = sum(1 for _, f in br_pairs if f == fun)
        vl_count = sum(1 for _, f in vl_pairs if f == fun)
        ac_count = sum(1 for _, f in ac_pairs if f == fun)
        total = br_count + vl_count + ac_count

        if total < 3:
            issues.append({
                "severity": "HIGH",
                "check": "rule_density",
                "message": f"{fun} has only {total} rules (BR={br_count}, VL={vl_count}, AC={ac_count}) — under-specified (minimum 3)",
            })
        elif total < 6:
            issues.append({
                "severity": "MEDIUM",
                "check": "rule_density",
                "message": f"{fun} has {total} rules (BR={br_count}, VL={vl_count}, AC={ac_count}) — consider adding more coverage",
            })

    if not issues:
        issues.append({
            "severity": "INFO",
            "check": "rule_density",
            "message": f"All {len(funs)} FUNs have sufficient rule density",
        })

    return issues


def check_rule_density(text: str) -> list[dict]:
    """Check each FUN has sufficient rule coverage.

    Supports two artifact layouts:
    1. `### FUN-XXX` sub-heading blocks (each FUN's rules live under its
       heading) — original heading-based path, unchanged.
    2. Table-based feature lists (功能清单表格): FUN IDs are referenced in the
       所属 FUN column of the 业务规则 / 校验规则 / 验收依据 tables, and
       BR/VL/AC counts are aggregated per FUN from those tables.
    Falls back to a MEDIUM "skipped" warning when no FUN can be located.
    """
    issues = []
    fun_blocks = re.split(r'###\s+(FUN-\d+[A-Z]?)', text)
    # `re.split` with a capturing group returns [prefix, id, block, id, block, ...].
    # When no `### FUN-XXX` heading matches, the list has length 1 (just the whole
    # text) and the loop below never runs — so we must detect that case explicitly
    # instead of silently reporting "all blocks pass".
    if len(fun_blocks) < 3:
        # No `### FUN-XXX` headings → try the table-based layout.
        return _table_rule_density(text)

    for i in range(1, len(fun_blocks), 2):
        fun_id = fun_blocks[i]
        block = fun_blocks[i + 1] if i + 1 < len(fun_blocks) else ""
        br_count = len(re.findall(_rule_id_re("BR"), block))
        vl_count = len(re.findall(_rule_id_re("VL"), block))
        ac_count = len(re.findall(_rule_id_re("AC"), block))
        total = br_count + vl_count + ac_count

        if total < 3:
            issues.append({
                "severity": "HIGH",
                "check": "rule_density",
                "message": f"{fun_id} has only {total} rules (BR={br_count}, VL={vl_count}, AC={ac_count}) — under-specified (minimum 3)",
            })
        elif total < 6:
            issues.append({
                "severity": "MEDIUM",
                "check": "rule_density",
                "message": f"{fun_id} has {total} rules (BR={br_count}, VL={vl_count}, AC={ac_count}) — consider adding more coverage",
            })

    if not issues:
        issues.append({
            "severity": "INFO",
            "check": "rule_density",
            "message": "All FUN blocks have sufficient rule density",
        })

    return issues


def main():
    parser = argparse.ArgumentParser(description="Property-based completeness checker for function-description artifacts")
    parser.add_argument("artifact", type=Path, help="Path to function-description.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.artifact.exists():
        print(f"File not found: {args.artifact}", file=sys.stderr)
        sys.exit(2)

    text = args.artifact.read_text(encoding="utf-8")

    all_issues = []
    all_issues.extend(check_minimum_threshold(text))
    all_issues.extend(check_state_machine(text))
    all_issues.extend(check_exception_coverage(text))
    all_issues.extend(check_vl_ac_pairing(text))
    all_issues.extend(check_rule_density(text))

    errors = [i for i in all_issues if i["severity"] in ("HIGH", "CRITICAL")]
    warnings = [i for i in all_issues if i["severity"] == "MEDIUM"]
    info = [i for i in all_issues if i["severity"] == "INFO"]

    if args.json:
        print(json.dumps({
            "ok": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "info": [i["message"] for i in info],
        }, ensure_ascii=False, indent=2))
    else:
        for e in errors:
            print(f"ERROR [{e['check']}]: {e['message']}")
        for w in warnings:
            print(f"WARN  [{w['check']}]: {w['message']}")
        for i in info:
            print(f"INFO  [{i['check']}]: {i['message']}")
        if not errors:
            print("✅ Property checks passed")

    sys.exit(0 if len(errors) == 0 else 1)


if __name__ == "__main__":
    main()
