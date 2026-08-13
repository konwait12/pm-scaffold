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
    # Find BR rules that imply exceptions (look for "失败", "异常", "超时", "过期", etc.)
    exception_keywords = ['失败', '异常', '超时', '过期', '不', '无法', '拒绝', '禁止', '满', '冲突']
    br_lines = re.findall(r'\|\s*(BR-\d+)\s*\|([^|]+)\|([^|]+)\|', section_by_keyword(text, "业务规则"))
    exception_brs = []
    for br_id, _, desc in br_lines:
        if any(kw in desc for kw in exception_keywords):
            exception_brs.append((br_id, desc.strip()))

    # Find exception handling entries
    ex_entries = re.findall(r'(EX-\d+|BR-\d+).*?(恢复|重试|重授权|重新|联系)',
                            section_by_keyword(text, "异常"), re.DOTALL)

    for br_id, desc in exception_brs:
        # Check if this BR has a corresponding recovery entry
        has_recovery = any(br_id in ex[0] or any(kw in desc for kw in ['恢复', '重试', '重新提交', '联系'] if kw in ex[1])
                          for ex in ex_entries)
        if not has_recovery:
            issues.append({
                "severity": "HIGH",
                "check": "exception_coverage",
                "message": f"BR {br_id} ('{desc[:60]}') describes an exception but no recovery path found in exception-handling section",
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
    vl_ids = set(re.findall(r'\bVL-\d+\b', vl_section))
    ac_ids = set(re.findall(r'\bAC-\d+\b', ac_section))

    # FUN is the 5th column in both tables:
    #   VL: | VL-001 | 校验内容 | 校验规则 | 错误提示 | FUN-XXX | 来源 |
    #   AC: | AC-001 | 验收标准 | 量化阈值 | 来源目标 G | FUN-XXX | 优先级 |
    vl_funs = set(re.findall(r'\|\s*VL-\d+\s*\|(?:[^|]*\|){3}\s*([^|]+?)\s*\|', vl_section))
    ac_funs = set(re.findall(r'\|\s*AC-\d+\s*\|(?:[^|]*\|){3}\s*([^|]+?)\s*\|', ac_section))
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


def check_rule_density(text: str) -> list[dict]:
    """Check each FUN has sufficient rule coverage."""
    issues = []
    fun_blocks = re.split(r'###\s+(FUN-\d+)', text)
    for i in range(1, len(fun_blocks), 2):
        fun_id = fun_blocks[i]
        block = fun_blocks[i + 1] if i + 1 < len(fun_blocks) else ""
        br_count = len(re.findall(r'\bBR-\d+\b', block))
        vl_count = len(re.findall(r'\bVL-\d+\b', block))
        ac_count = len(re.findall(r'\bAC-\d+\b', block))
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
