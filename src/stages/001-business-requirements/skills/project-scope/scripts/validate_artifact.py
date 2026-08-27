#!/usr/bin/env python3
"""Validate the project-scope.md artifact (PRD §2 范围基线唯一上游).

The artifact carries the four-state scope baseline (In / Out / Deferred /
Conditional) plus assumptions, dependencies, and risk posture.  This validator
checks the stable structure only — scope content is a business fact owned by
the human reviewer.

Run: python3 validate_artifact.py [<project-scope.md>] [--json]
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


SKILL_ID = "project_scope"
CHECK_PREFIX = "scope"

REQUIRED_FRONTMATTER = {
    "artifact_id", "version", "status", "owner",
    "business_fact_owner", "goal_decision_owner", "reviewer",
    "created_at", "updated_at", "confirmed_at",
}

# 四态范围基线 + 假设/依赖/风险姿态。章节标题匹配 SKILL.md output-contract。
REQUIRED_HEADINGS = [
    "结论摘要",
    "In Scope",
    "Out of Scope",
    "Deferred",
    "Conditional",
    "假设清单",
    "依赖清单",
    "风险姿态",
]

VALID_STATUSES = {
    "draft", "needs_user_input", "conditional_review",
    "ready_for_human_review", "confirmed",
    "superseded", "legacy_unverified", "simulated",
}

SCOPE_ID_RE = re.compile(r"\bSCOPE-(?:[A-Z]+-)?\d+\b")
KNOWLEDGE_STATE_RE = re.compile(r"\b(?:FACT|DECISION|ASSUMPTION|AI_INFERENCE|UNKNOWN|CONFLICT)\b")


def _norm(h: str) -> str:
    return re.sub(r"\s*（[^）]*）\s*$", "", re.sub(r"^\d+\.\s*", "", h).strip()).strip()


def _headings(text: str) -> list[str]:
    return [_norm(m.group(1)) for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]


def _parse_frontmatter(text: str) -> dict[str, str]:
    text = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.DOTALL)
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    result: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("'\"")
    return result


def validate(path: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}

    text = path.read_text(encoding="utf-8")
    meta = _parse_frontmatter(text)
    missing_fm = sorted(REQUIRED_FRONTMATTER - meta.keys())
    if missing_fm:
        errors.append(f"Missing frontmatter fields: {', '.join(missing_fm)}")

    status = meta.get("status", "")
    if status and status not in VALID_STATUSES:
        errors.append(f"Invalid status '{status}'")

    headings = _headings(text)
    for h in REQUIRED_HEADINGS:
        if not any(hh == h or hh.startswith(h) for hh in headings):
            errors.append(f"Missing required heading: {h}")

    # 四态基线必须有 SCOPE- ID 行（或显式声明无 Conditional 项）。
    if any(hh.startswith("In Scope") for hh in headings) and not SCOPE_ID_RE.search(text):
        errors.append("Scope baseline must carry at least one SCOPE- ID")

    # 假设清单必须带知识状态标签，否则无法证伪。
    if "假设清单" in headings and not KNOWLEDGE_STATE_RE.search(text):
        warnings.append(
            "假设清单未发现知识状态标签（FACT/DECISION/ASSUMPTION/AI_INFERENCE/UNKNOWN/CONFLICT）"
        )

    issues = [make_issue(severity="CRITICAL", check_id=_check_id(e), family=SKILL_ID,
                         location=str(path), message=e) for e in errors]
    issues.extend(make_issue(severity="MEDIUM", check_id=_check_id(w, warning=True),
                             family=SKILL_ID, location=str(path), message=w, blocking=False)
                  for w in warnings)
    return {"ok": not errors, "errors": errors, "warnings": warnings, "issues": issues}


_ERROR_RULES = [
    ("Missing frontmatter fields:", "scope.missing_frontmatter"),
    ("Invalid status", "scope.invalid_status"),
    ("Missing required heading:", "scope.missing_heading"),
    ("Scope baseline must carry", "scope.missing_scope_id"),
]

_WARNING_RULES = [
    ("假设清单未发现知识状态标签", "scope.missing_knowledge_state"),
]


def _check_id(msg: str, *, warning: bool = False) -> str:
    rules = _WARNING_RULES if warning else _ERROR_RULES
    for needle, check_id in rules:
        if needle in msg:
            return check_id
    return "scope.semantic" if warning else "scope.structural"


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
