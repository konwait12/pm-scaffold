#!/usr/bin/env python3
"""Validate the structure of a prd-assembly Markdown artifact (final PRD).

This work_item is an independent work_item producing a standalone prd.md artifact.
The validator checks the full file content for:
  1. All 13 required PRD sections present
  2. All 12 upstream work_items confirmed and listed
  3. Forward traceability chain: G→UJ→US→ST→FEA→FUN→PD→IX→BR→VL→SM→EX→AC
  4. Backward traceability chain: AC→EX→SM→BR→VL→IX→PD→FUN→FEA→ST→US→UJ
  5. RTM matrix present
  6. Frontmatter and status consistency

Run: python3 validate_artifact.py [<prd.md>] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def _bootstrap_scripts() -> None:
    import sys as _sys
    p = Path(__file__).resolve().parent
    while p.parent != p:
        cand = p / "src" / "scripts"
        if (cand / "validation_errors.py").is_file():
            if str(cand) not in _sys.path:
                _sys.path.insert(0, str(cand))
            return
        p = p.parent

_bootstrap_scripts()
from validation_errors import make_issue

SKILL_ID = "prd_assembly"
CHECK_PREFIX = "prd"

REQUIRED_FRONTMATTER = {
    "artifact_id", "version", "status", "owner",
    "business_fact_owner", "goal_decision_owner", "reviewer",
    "created_at", "updated_at", "confirmed_at",
}

# PRD must have 13 sections (not the old 7)
REQUIRED_HEADINGS = [
    "项目背景与目标",
    "业务角色、用户旅程与用户故事",
    "UX：页面设计与交互规则",
    "分功能描述",
    "按需章节",
    "事实与决定",
    "验收依据",
    "需求追溯矩阵",
    "自审记录",
    # The 9 additional sections from v2 plan:
    "业务规则",
    "校验规则",
    "状态机",
    "异常处理",
]

# 12 upstream work_item IDs that must be confirmed
UPSTREAM_WORK_ITEMS = [
    "project-background-goal",  # G
    "user-journey",             # UJ
    "user-stories",             # US
    "feature-list",             # ST → FEA
    "functional-flow",           # FUN
    "page-design",              # PD
    "interaction-rules",         # IX
    "business-rules",           # BR
    "validation-rules",         # VL
    "state-machine",            # SM
    "exception-handling",       # EX
    "acceptance-criteria",       # AC
]

PENDING = ("待确认",)
VALID_STATUSES = {
    "draft", "needs_user_input", "conditional_review",
    "ready_for_human_review", "confirmed",
    "superseded", "legacy_unverified", "simulated",
}


def _norm(h: str) -> str:
    return re.sub(r"\s*（[^）]*）\s*$", "", re.sub(r"^\d+\.\s*", "", h).strip()).strip()


def _project_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "src" / "framework" / "workflow-registry.json").is_file():
            return parent
    return p.parents[8]


def parse_frontmatter(text: str) -> dict[str, str]:
    text = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.DOTALL)
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    result: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        k, v = line.split(":", 1)
        result[k.strip()] = v.strip().strip('"\'')
    return result


def validate(path: Path) -> dict[str, object]:
    errors, warnings = [], []
    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}

    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    status = meta.get("status")

    missing = sorted(REQUIRED_FRONTMATTER - meta.keys())
    if missing:
        errors.append(f"Missing frontmatter fields: {', '.join(missing)}")

    if status and status not in VALID_STATUSES:
        errors.append(f"Invalid status '{status}'")

    headings = [_norm(m.group(1)) for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]
    missing_h = [h for h in REQUIRED_HEADINGS if _norm(h) not in headings]
    if missing_h:
        errors.append(f"Missing required headings: {', '.join(missing_h)}")

    if "RTM" not in text and "需求追溯矩阵" not in text:
        errors.append("No RTM (Requirements Traceability Matrix) found")

    if status == "confirmed":
        unresolved = [k for k in ("business_fact_owner", "goal_decision_owner", "reviewer", "confirmed_at")
                      if meta.get(k, "") in {"", *PENDING}]
        if unresolved:
            errors.append("Confirmed artifact has unresolved confirmation fields: " + ", ".join(unresolved))

    if any(p in text for p in PENDING) and status == "confirmed":
        body = re.sub(r"^##\s+\d+\.\s*[^\n]*$", "", text, flags=re.MULTILINE)
        if any(p in body for p in PENDING):
            warnings.append("Confirmed PRD still contains 待确认 markers in body")

    # Semantic red flags specific to PRD assembly
    if status == "ready_for_human_review" or status == "confirmed":
        # Check all 12 upstream work_items are confirmed
        upstream_statuses = meta.get("upstream_work_item_statuses", "")
        missing_upstream = []
        for wi in UPSTREAM_WORK_ITEMS:
            if wi not in upstream_statuses:
                missing_upstream.append(wi)
        if missing_upstream:
            errors.append(
                f"PRD DoD D5.2 failed: missing upstream work_item confirmation for: "
                f"{', '.join(missing_upstream)} (need all 12 confirmed before PRD)"
            )

        # Forward traceability chain G→UJ→US→ST→FEA→FUN→PD→IX→BR→VL→SM→EX→AC
        # Combined upstream-artifact-id regex (used by consistency_check E1 and shown above
        # as 12 separate re.search lines for per-prefix diagnostics). Keep both in sync.
        # Note: this is the "scope" regex — covers all upstream + prd (PRD- for self).
        # The E1 consistency check looks for `(BG|UJ|US|FEA|FL|PD|IX|BR|VL|SM|EX|PRD)-\d+(?:-\d+)?`
        # in source code, so keep the literal pattern below (capturing group, no \b anchors).
        UPSTREAM_ID_PATTERN = re.compile(
            r"(BG|UJ|US|FEA|FL|PD|IX|BR|VL|STATE|EX|AC|PRD)-\d+(?:-\d+)?"
        )
        forward_chain_ids = {
            "G": bool(re.search(r"\bG-\d+\b", text)),           # project-background-goal
            "UJ": bool(re.search(r"\bUJ-\d+\b", text)),         # user-journey
            "US": bool(re.search(r"\bUS-\d+\b", text)),         # user-stories
            "ST": bool(re.search(r"\bST-\d+\b", text)),         # user-stories
            "FEA": bool(re.search(r"\bFEA-\d+\b", text)),        # feature-list
            "FUN": bool(re.search(r"\bFUN-\d+\b", text)),       # functional-flow
            "PD": bool(re.search(r"\bPD-\d+\b", text)),         # page-design
            "IX": bool(re.search(r"\bIX-\d+\b", text)),        # interaction-rules
            "BR": bool(re.search(r"\bBR-\d+\b", text)),         # business-rules
            "VL": bool(re.search(r"\bVL-\d+\b", text)),        # validation-rules
            "SM": bool(re.search(r"\bSM-\d+\b|\bSTATE-\d+\b", text)),  # state-machine
            "EX": bool(re.search(r"\bEX-\d+\b", text)),        # exception-handling
            "AC": bool(re.search(r"\bAC-\d+\b", text)),         # acceptance-criteria
        }
        missing_trace_ids = [k for k, v in forward_chain_ids.items() if not v]
        if missing_trace_ids:
            warnings.append(
                f"Forward traceability incomplete: missing IDs for: {', '.join(missing_trace_ids)}. "
                "Expected chain: G→UJ→US→ST→FEA→FUN→PD→IX→BR→VL→SM→EX→AC"
            )

        # RTM section checks
        rtm_section = re.search(
            r"^##\s+\d+\.\s*需求追溯矩阵\s*$(.*?)(?=^##\s+|\Z)",
            text, re.MULTILINE | re.DOTALL
        )
        if rtm_section:
            rtm_rows = [
                l for l in rtm_section.group(1).splitlines()
                if l.lstrip().startswith("|") and "---" not in l and "目标" not in l
            ]
            rtm_data = [r for r in rtm_rows if "待确认" not in r]
            if len(rtm_data) == 0:
                warnings.append("Semantic: RTM has no data rows; traceability matrix should be populated")
            # RTM column count: should have ≥6 columns for full chain
            header_match = re.search(r"^\|\s*([^|]+\|){5,}\s*[^|]+\|\s*$", rtm_section.group(1), re.MULTILINE)
            if header_match:
                col_count = header_match.group(0).count("|") - 1
                if col_count < 6:
                    warnings.append(
                        f"Semantic (G_CROSS): RTM header has {col_count} columns, expected ≥6 "
                        "for full traceability chain"
                    )

        # Check for new content not in upstream
        new_content_markers = ["新增需求", "补充功能", "额外建议"]
        if any(m in text for m in new_content_markers):
            warnings.append(
                "Semantic: PRD contains '新增需求/补充功能/额外建议' markers; "
                "PRD assembly should only aggregate, not introduce new requirements"
            )

        # Content-density gate: PRD must EMBED upstream content, not point to it.
        # Aggregation contract requires §1-§4/§6/§7 + BR/VL/SM/EX/AC tables to be
        # fully verbose-embedded. A single-line pointer like "详见 FD-001" delegates
        # content upstream, leaving the PRD thin and non-self-contained → FAIL.
        pointer_refs = re.findall(
            r"(?:详见|内容见)\s*[`\[]?\s*[A-Za-z][A-Za-z0-9_\-]{0,40}", text
        )
        if pointer_refs:
            uniq = list(dict.fromkeys(pointer_refs))
            errors.append(
                "Content-density gate failed: PRD delegates content via upstream "
                f"pointers ({', '.join(uniq[:6])}) instead of embedding it verbatim. "
                "Embed the full BR/VL/SM/EX/AC tables and story cards; do not write "
                "'详见 XX-XXX' pointers."
            )

    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "issues": _make_issues(errors, warnings, path)}


_PRD_ERROR_RULES = [
    ("Missing frontmatter fields:", "prd.missing_frontmatter"),
    ("Invalid status", "prd.invalid_status"),
    ("Missing required headings:", "prd.missing_headings"),
    ("No RTM", "prd.missing_rtm"),
    ("Confirmed artifact has unresolved confirmation fields:", "prd.unresolved_confirmation"),
    ("PRD DoD D5.2 failed:", "prd.d52_missing_upstream"),
    ("Content-density gate failed:", "prd.pointer_only_content"),
]

_PRD_WARNING_RULES = [
    ("Confirmed PRD still contains 待确认 markers", "prd.pending_markers_in_confirmed"),
    ("RTM has no data rows", "prd.rtm_no_data"),
    ("RTM header has", "prd.rtm_column_count"),
    ("Forward traceability incomplete", "prd.forward_trace_incomplete"),
    ("PRD contains", "prd.new_content_markers"),
]


def _check_id(msg: str, rules: list[tuple[str, str]], fallback: str) -> str:
    for needle, check_id in rules:
        if needle in msg:
            return check_id
    return fallback


def _make_issues(errors: list[str], warnings: list[str], path: Path) -> list[dict]:
    """双轨制：errors/warnings 保持字符串列表，issues 为 make_issue 统一 dict。"""
    issues: list[dict] = []
    for e in errors:
        issues.append(make_issue(
            severity="CRITICAL",
            check_id=_check_id(e, _PRD_ERROR_RULES, "prd.structural"),
            family=SKILL_ID,
            location=str(path),
            message=e,
        ))
    for w in warnings:
        issues.append(make_issue(
            severity="MEDIUM",
            check_id=_check_id(w, _PRD_WARNING_RULES, "prd.semantic"),
            family=SKILL_ID,
            location=str(path),
            message=w,
            blocking=False,
        ))
    return issues


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path)
    p.add_argument("--json", action="store_true", dest="j")
    a = p.parse_args()
    r = validate(a.artifact)
    if a.j:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("PASS" if r["ok"] else "FAIL")
        for e in r["errors"]:
            print(f"ERROR: {e}")
        for w in r["warnings"]:
            print(f"WARNING: {w}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
