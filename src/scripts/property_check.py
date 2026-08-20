#!/usr/bin/env python3
"""Property-based completeness checker for stage-2 product-requirements artifacts.

Goes beyond structural validation to check logical completeness:
1. State machine exhaustiveness: every state × known event → target state defined
2. Exception path coverage: every BR with an exception branch has a recovery path
3. VL↔AC pairing: every validation rule has a corresponding acceptance criterion
4. Evidence coverage: applicable BR/VL/AC anchors form a verifiable loop

Accepts any of the 9 stage-2 artifact types:
  feature-list, functional-flow, page-design, interaction-rules,
  business-rules, validation-rules, state-machine, exception-handling, acceptance-criteria

Usage: python3 property_check.py <stage2-artifact.md> [--json]
Exit 0 = complete, 1 = gaps found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
from validation_errors import make_issue

FAMILY = "property_check"


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
    frontmatter field.  Templates produced by ``resolver.py`` open with an
    optional ``<!-- ... -->`` comment block before the YAML header, so strip
    it first — otherwise ``re.match`` anchored at the string start fails and
    every stage-2 artifact is mis-reported as missing artifact_id/status.
    """
    text = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.DOTALL)
    match = re.match(r"---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("'\"")
    return result


def check_minimum_threshold(text: str, artifact_path: str = "<artifact>") -> list[dict]:
    """B11: minimum threshold — an artifact must not silent-pass the gate."""
    issues = []
    if not re.search(r"(?m)^#{1,2}\s+\S+", text):
        issues.append(make_issue(
            severity="CRITICAL",
            check_id="minimum_threshold.no_headings",
            family=FAMILY,
            location=artifact_path,
            field_path="sections.headings",
            message="产物缺少章节标题",
            expected="至少有一个 `## ` 或 `# ` 章节（空文件/无章节产物不得通过闸门）",
            actual="全文 0 个 # 或 ## 标题",
            repair_hint="在产物开头添加章节标题，例如 ## 1. 业务背景 / ## 功能清单 FEA-001；若使用模板请按模板的章节结构填写内容",
            source_ref="constitution §4 知识状态必须标注 + B11 silent-pass gate",
        ))
    fm = _parse_frontmatter(text)
    for field in ("artifact_id", "status"):
        if not fm.get(field):
            issues.append(make_issue(
                severity="CRITICAL",
                check_id=f"minimum_threshold.missing_frontmatter_{field}",
                family=FAMILY,
                location=artifact_path,
                field_path=f"frontmatter.{field}",
                message=f"frontmatter 缺少必备字段 {field}",
                expected=f"产物 YAML frontmatter 必须含 `{field}: <value>`（与 templates/_frontmatter-schema.md 一致）",
                actual=f"frontmatter 中未找到字段 {field}（或值为空）",
                repair_hint=f"在文件最上方 YAML frontmatter（---...--- 区块）中添加一行: `{field}: {'<如-FD-001>' if field=='artifact_id' else 'draft'}`",
                source_ref="contracts.md §Artifact States + _frontmatter-schema.md",
            ))
    if not issues:
        issues.append(make_issue(
            severity="INFO",
            check_id="minimum_threshold.pass",
            family=FAMILY,
            location=artifact_path,
            message="Minimum threshold OK: ≥1 heading section + required frontmatter (artifact_id/status)",
            blocking=False,
        ))
    return issues


def _rule_id_re(prefix: str) -> str:
    """Regex fragment matching a rule/feature ID, with an optional letter suffix.

    Accepts `PREFIX-123` and `PREFIX-123A` (single uppercase letter). OBS-005:
    older checks only matched pure digits (`BR-\\d+`), so suffixed IDs such as
    BR-006A were silently skipped by the rule-density / pairing / exception
    checks and under-counted the rules per FUN.
    """
    return rf"\b{prefix}-\d+[A-Z]?\b"


TRACE_ANCHOR_RE = re.compile(r"\b(?:FUN|FEA|ST|BR|VL|EX|IX|STATE|SRC|BG|G)-\d+[A-Z]?\b")


def _row_id_anchors(section: str, prefix: str) -> list[tuple[str, set[str]]]:
    """Return each row ID and external FUN/FEA trace anchors."""
    rows: list[tuple[str, set[str]]] = []
    row_re = re.compile(r"^\s*\|\s*(" + _rule_id_re(prefix) + r")\s*\|", re.MULTILINE)
    for match in row_re.finditer(section):
        end = section.find("\n", match.start())
        line = section[match.start(): end if end >= 0 else len(section)]
        rid = match.group(1)
        anchors = {m.group(0) for m in TRACE_ANCHOR_RE.finditer(line) if m.group(0) != rid}
        rows.append((rid, anchors))
    return rows


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


def check_state_machine(text: str, artifact_path: str = "<artifact>") -> list[dict]:
    """Check state transition completeness (parses the 状态变化 section only)."""
    issues = []
    # E2E-021：非状态机工作项（feature-list/page-design/validation-rules/exception-handling/
    # acceptance-criteria 等）合法地不定义状态机。若产物根本没有「状态变化」章节，
    # 直接跳过该检查，否则会对每个非状态机产物误报 state_machine.missing_table。
    if _norm("状态变化") not in _norm(text) and "状态迁移" not in _norm(text):
        return issues
    section = section_by_keyword(text, "状态变化")
    state_rows = re.findall(
        r'\|\s*[^|]+\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
        section,
    )
    if not state_rows:
        issues.append(make_issue(
            severity="MEDIUM",
            check_id="state_machine.missing_table",
            family=FAMILY,
            location=artifact_path,
            field_path="sections.状态变化.table",
            message="No state transition table found in 状态变化 section",
            expected="若产物定义状态机（状态变化章节非空），必须包含 STATE × 触发事件 → 目标状态 的6列表格",
            actual="状态变化章节未匹配到任何4列以上的状态行（可能标题命名不一致或使用了纯列表）",
            repair_hint="按子模板 state-machine-output.md 的 6 列格式填写：| STATE | 状态名称 | 触发事件 | 目标状态 | 条件 | 所属 FUN |",
            source_ref="state-machine skill output-contract §状态迁移矩阵",
            blocking=False,
        ))
        return issues

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

    terminal_keywords = ['完成', '结束', '关闭', '归档', 'done', 'complete', 'closed']
    for state in states:
        if any(kw in state for kw in terminal_keywords):
            continue
        outgoing = [(s, e) for (s, e) in transitions if s == state]
        if not outgoing:
            issues.append(make_issue(
                severity="HIGH",
                check_id="state_machine.no_outgoing",
                family=FAMILY,
                location=artifact_path,
                field_path=f"sections.状态变化.states.{state}",
                message=f"State '{state}' has no outgoing transitions (non-terminal state)",
                expected=f"非终态 '{state}' 必须至少定义 1 条 触发事件→目标状态 的迁移行",
                actual=f"'{state}' 当前状态变化表格中 outgoing 迁移数 = 0",
                repair_hint=f"在 状态变化 表格为 '{state}' 增加至少一个触发事件（如「用户提交」「审批通过」「系统处理完成」「超时 N 分钟」等），并指定目标状态",
                source_ref="thinking-core.md §透镜7 穷尽性 / state-machine subskill output-contract",
            ))

    for event in events:
        incoming = [(s, e) for (s, e) in transitions if e == event]
        if not incoming:
            issues.append(make_issue(
                severity="MEDIUM",
                check_id="state_machine.event_no_incoming",
                family=FAMILY,
                location=artifact_path,
                field_path=f"sections.状态变化.events.{event}",
                message=f"Event '{event}' triggers no transitions",
                expected=f"每个在表中出现过的触发事件 '{event}' 必须至少从 1 个源状态触发迁移",
                actual=f"事件 '{event}' 在全表匹配到 0 条 incoming 迁移（可能只是目标状态的注释？）",
                repair_hint=f"若 '{event}' 是真实触发条件，请为它在表格中补充至少一行源状态；若是拼写错误或注释，请删除或修正事件名称",
                source_ref="state-machine 子技能 SKILL.md §完整性检查",
                blocking=False,
            ))

    if not issues:
        issues.append(make_issue(
            severity="INFO",
            check_id="state_machine.pass",
            family=FAMILY,
            location=artifact_path,
            message=f"State machine: {len(states)} states, {len(events)} events, {len(transitions)} transitions — appears complete",
            blocking=False,
        ))

    return issues


def check_exception_coverage(text: str, artifact_path: str = "<artifact>") -> list[dict]:
    """Check every BR exception branch has a recovery path."""
    issues = []
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

    recovery_keywords = ['恢复', '重试', '重授权', '重新', '联系']
    ex_with_recovery: list[tuple[str, str]] = []
    for line in section_by_keyword(text, "异常").split("\n"):
        m = re.match(r'^\|\s*(EX-\d+[A-Z]?|BR-\d+[A-Z]?)\s*\|(.+)$', line.strip())
        if m and any(kw in m.group(2) for kw in recovery_keywords):
            ex_with_recovery.append((m.group(1), m.group(2)))

    for br in exception_brs:
        br_id = br["id"]
        has_recovery = (
            any(br_id in row_text for _, row_text in ex_with_recovery)
            or any(ex_id in br["row"] for ex_id, _ in ex_with_recovery)
            or any(kw in br["row"] for kw in recovery_keywords)
        )
        if not has_recovery:
            issues.append(make_issue(
                severity="HIGH",
                check_id="exception_coverage.missing_recovery",
                family=FAMILY,
                location=artifact_path,
                field_path=f"tables.业务规则.rows.{br_id}",
                message=f"BR {br_id} 规则内容含异常语义，但异常处理章节未找到 recovery path",
                expected=f"每条包含异常/失败/拒绝/超时语义的业务规则（{br_id}）必须在 异常与失败处理 章节定义对应的恢复路径（重试/回滚/联系支持/转人工 等）",
                actual=f"{br_id} 的规则内容：'{br['content'][:60]}'；未在 异常章节匹配到含 恢复/重试/重新/联系 等关键字的恢复方案；规则类型列='{br['row'].split(' | ')[1][:20]}'",
                repair_hint=f"（1）在 异常与失败处理 表格中为 {br_id} 新增 EX-xxx 行，写明恢复方式（重试 N 次？转人工？提示用户并返回草稿？）；（2）或在业务规则表格本 {br_id} 行的「预期行为」列直接声明恢复动作",
                source_ref="exception-handling subskill output-contract / thinking-core.md §透镜8 异常路径",
            ))

    if not issues:
        issues.append(make_issue(
            severity="INFO",
            check_id="exception_coverage.pass",
            family=FAMILY,
            location=artifact_path,
            message=f"Exception coverage: {len(exception_brs)} exception BRs, all have recovery paths",
            blocking=False,
        ))

    return issues


def check_vl_ac_pairing(text: str, artifact_path: str = "<artifact>") -> list[dict]:
    """Advisory check that applicable VL anchors have measurable AC evidence."""
    issues = []
    vl_section = section_by_keyword(text, "校验规则")
    ac_section = section_by_keyword(text, "验收依据")
    vl_ids = set(re.findall(_rule_id_re("VL"), vl_section))
    ac_ids = set(re.findall(_rule_id_re("AC"), ac_section))

    vl_anchors = {a for _, anchors in _row_id_anchors(vl_section, "VL") for a in anchors if a.startswith(("FUN-", "FEA-"))}
    ac_anchors = {a for _, anchors in _row_id_anchors(ac_section, "AC") for a in anchors if a.startswith(("FUN-", "FEA-"))}
    uncovered = sorted(vl_anchors - ac_anchors)
    for fun in uncovered:
        issues.append(make_issue(
            severity="MEDIUM",
            check_id="vl_ac_pairing.uncovered_fun",
            family=FAMILY,
            location=artifact_path,
            field_path=f"tables.校验规则.anchors.{fun}",
            message=f"{fun} has validation rules (VL) but no acceptance criteria (AC)",
            expected=f"对需要用户/业务验收的 {fun}，应有至少一条可验证 AC；纯平台或全局约束可标注不适用",
            actual=f"校验规则引用 {fun}，但验收依据未发现同一 FUN/FEA 锚点（VL={len(vl_ids)}, AC={len(ac_ids)}）",
            repair_hint=f"补充引用 {fun} 的 Given/When/Then AC，或明确 scope=GLOBAL / 不适用及理由",
            source_ref="acceptance-criteria subskill SKILL.md §EAR 语法",
            blocking=False,
        ))

    if not issues:
        issues.append(make_issue(
            severity="INFO",
            check_id="vl_ac_pairing.pass",
            family=FAMILY,
            location=artifact_path,
            message=f"VL↔AC pairing: {len(vl_ids)} VLs, {len(ac_ids)} ACs — all VL FUNs covered by ACs",
            blocking=False,
        ))

    return issues


def _id_fun_pairs(section: str, id_prefix: str, gap: int) -> list[tuple[str, str]]:
    """Extract (ID, preferred FUN/FEA anchor) pairs from table rows.

    `gap` is the number of cells between the ID cell and the 所属 FUN cell:
      BR: | BR-X | 规则描述 | 类型 | 触发条件 | 约束/逻辑 | FUN-X | 来源 |  → gap=4
      VL: | VL-X | 校验内容 | 校验规则 | 错误提示 | FUN-X | 来源 |        → gap=3
      AC: | AC-X | 验收标准 | 量化阈值 | 来源目标 G | FUN-X | 优先级 |    → gap=3
    `[^|\n]` keeps each match on a single table row (same fix as B1), so a
    non-ID cell can never anchor across newlines.
    """
    pairs: list[tuple[str, str]] = []
    for rid, anchors in _row_id_anchors(section, id_prefix):
        preferred = sorted(a for a in anchors if a.startswith(("FUN-", "FEA-")))
        if preferred:
            pairs.append((rid, preferred[0]))
    return pairs


def _table_rule_density(text: str, artifact_path: str) -> list[dict]:
    """Risk-adapted evidence coverage for table layouts."""
    issues = []
    br_pairs = _id_fun_pairs(section_by_keyword(text, "业务规则"), "BR", 4)
    vl_pairs = _id_fun_pairs(section_by_keyword(text, "校验规则"), "VL", 3)
    ac_pairs = _id_fun_pairs(section_by_keyword(text, "验收依据"), "AC", 3)

    funs = sorted({fun for _, fun in br_pairs + vl_pairs + ac_pairs})
    if not funs:
        issues.append(make_issue(
            severity="INFO",
            check_id="rule_density.not_applicable",
            family=FAMILY,
            location=artifact_path,
            field_path="tables.功能清单",
            message="未发现 FUN/FEA 规则锚点；覆盖度检查不适用于当前产物",
            blocking=False,
        ))
        return issues

    for fun in funs:
        br_count = sum(1 for _, f in br_pairs if f == fun)
        vl_count = sum(1 for _, f in vl_pairs if f == fun)
        ac_count = sum(1 for _, f in ac_pairs if f == fun)
        total = br_count + vl_count + ac_count

        if br_count and not ac_count:
            issues.append(make_issue(
                severity="MEDIUM", check_id="rule_density.missing_acceptance",
                family=FAMILY, location=artifact_path,
                field_path=f"tables.rules.anchors.{fun}",
                message=f"{fun} has business rules but no acceptance evidence (BR={br_count}, VL={vl_count}, AC={ac_count})",
                expected="有业务约束或状态变化的功能应有至少一条可验证 AC；只读/平台能力可说明不适用",
                actual=f"{fun} 当前 BR={br_count}, VL={vl_count}, AC={ac_count}",
                repair_hint=f"为 {fun} 补充可测量 AC，或记录该能力不需要用户验收的适用性判断",
                source_ref="acceptance-criteria SKILL.md §Traceability", blocking=False,
            ))
        else:
            issues.append(make_issue(
                severity="INFO", check_id="rule_density.coverage_summary",
                family=FAMILY, location=artifact_path,
                field_path=f"tables.rules.anchors.{fun}",
                message=f"{fun} evidence coverage: BR={br_count}, VL={vl_count}, AC={ac_count}",
                blocking=False,
            ))

    return issues


def check_rule_density(text: str, artifact_path: str = "<artifact>") -> list[dict]:
    """Check each FUN has sufficient rule coverage."""
    issues = []
    fun_blocks = re.split(r'###\s+(FUN-\d+[A-Z]?)', text)
    if len(fun_blocks) < 3:
        return _table_rule_density(text, artifact_path)

    for i in range(1, len(fun_blocks), 2):
        fun_id = fun_blocks[i]
        block = fun_blocks[i + 1] if i + 1 < len(fun_blocks) else ""
        br_count = len(re.findall(_rule_id_re("BR"), block))
        vl_count = len(re.findall(_rule_id_re("VL"), block))
        ac_count = len(re.findall(_rule_id_re("AC"), block))
        total = br_count + vl_count + ac_count

        if br_count and not ac_count:
            issues.append(make_issue(
                severity="MEDIUM", check_id="rule_density.missing_acceptance",
                family=FAMILY, location=artifact_path,
                field_path=f"sections.heading_blocks.{fun_id}",
                message=f"{fun_id} has business rules but no acceptance evidence (BR={br_count}, VL={vl_count}, AC={ac_count})",
                expected="有业务约束或状态变化的功能应有至少一条可验证 AC；只读/平台能力可说明不适用",
                actual=f"{fun_id} 当前 BR={br_count}, VL={vl_count}, AC={ac_count}",
                repair_hint=f"为 {fun_id} 补充可测量 AC，或记录该能力不需要用户验收的适用性判断",
                source_ref="acceptance-criteria SKILL.md §Traceability", blocking=False,
            ))
        else:
            issues.append(make_issue(
                severity="INFO", check_id="rule_density.coverage_summary",
                family=FAMILY, location=artifact_path,
                field_path=f"sections.heading_blocks.{fun_id}",
                message=f"{fun_id} evidence coverage: BR={br_count}, VL={vl_count}, AC={ac_count}",
                blocking=False,
            ))

    return issues


def main():
    parser = argparse.ArgumentParser(description="Property-based completeness checker for stage-2 product-requirements artifacts")
    parser.add_argument("artifact", type=Path, help="Path to a stage-2 artifact (feature-list/functional-flow/.../acceptance-criteria.md)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.artifact.exists():
        print(f"File not found: {args.artifact}", file=sys.stderr)
        sys.exit(2)

    text = args.artifact.read_text(encoding="utf-8")
    art_path = str(args.artifact)

    all_issues = []
    all_issues.extend(check_minimum_threshold(text, art_path))
    all_issues.extend(check_state_machine(text, art_path))
    all_issues.extend(check_exception_coverage(text, art_path))
    all_issues.extend(check_vl_ac_pairing(text, art_path))
    all_issues.extend(check_rule_density(text, art_path))

    errors = [i for i in all_issues if i.get("severity") in ("HIGH", "CRITICAL") and i.get("blocking", True)]
    warnings = [i for i in all_issues if i.get("severity") == "MEDIUM" or (i.get("severity") in ("HIGH","CRITICAL") and not i.get("blocking", True))]
    info = [i for i in all_issues if i.get("severity") == "INFO"]

    if args.json:
        from validation_errors import aggregate_by_check_id
        print(json.dumps({
            "ok": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "info": [i["message"] for i in info],
            "aggregate_by_check_id": aggregate_by_check_id([errors + warnings]),
            "total_issues_scanned": len(all_issues),
        }, ensure_ascii=False, indent=2))
    else:
        from validation_errors import format_issue
        for e in errors:
            print(f"ERROR {format_issue(e)}")
        for w in warnings:
            print(f"WARN  {format_issue(w)}")
        for i in info:
            print(f"INFO  [{i.get('check_id')}] {i['message']}")
        if not errors:
            print("✅ Property checks passed (standardized format: [check_id] location.field_path: expect vs actual (修复))")

    sys.exit(0 if len(errors) == 0 else 1)


if __name__ == "__main__":
    main()
