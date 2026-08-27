#!/usr/bin/env python3
"""Validate the field-rules.md artifact (PRD §9.2 字段清单唯一上游).

The artifact carries the structured field definition table (F-XXX).  This
validator checks the stable structure and the F-XXX / VL-XXX cross-binding
only — field semantics are business facts owned by the human reviewer.

Run: python3 validate_artifact.py [<field-rules.md>] [--json]
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


SKILL_ID = "field_rules"
CHECK_PREFIX = "field"

REQUIRED_FRONTMATTER = {
    "artifact_id", "version", "status", "owner",
    "business_fact_owner", "goal_decision_owner", "reviewer",
    "created_at", "updated_at", "confirmed_at",
}

REQUIRED_HEADINGS = [
    "字段清单总览",
    "字段定义表",
    "字段来源说明",
    "字段与校验",
]

VALID_STATUSES = {
    "draft", "needs_user_input", "conditional_review",
    "ready_for_human_review", "confirmed",
    "superseded", "legacy_unverified", "simulated",
}

FIELD_ID_RE = re.compile(r"\bF-\d+\b")
VL_ID_RE = re.compile(r"\bVL-\d+\b")


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

    # 字段定义表必须产出至少一个 F-XXX。
    if any(hh.startswith("字段定义表") for hh in headings) and not FIELD_ID_RE.search(text):
        errors.append("Field definition table must carry at least one F-XXX ID")

    # §4 反向绑定：有 VL-XXX 时每个字段应可被校验引用；无 VL 时允许 TBD-VL。
    if any(hh.startswith("字段与校验") for hh in headings) and not VL_ID_RE.search(text) and "TBD-VL" not in text:
        warnings.append(
            "字段与校验反向绑定未发现 VL-XXX 引用，也未声明 TBD-VL；确认 VL 尚未产出即可"
        )

    issues = [make_issue(severity="CRITICAL", check_id=_check_id(e), family=SKILL_ID,
                         location=str(path), message=e) for e in errors]
    issues.extend(make_issue(severity="MEDIUM", check_id=_check_id(w, warning=True),
                             family=SKILL_ID, location=str(path), message=w, blocking=False)
                  for w in warnings)
    return {"ok": not errors, "errors": errors, "warnings": warnings, "issues": issues}


_ERROR_RULES = [
    ("Missing frontmatter fields:", "field.missing_frontmatter"),
    ("Invalid status", "field.invalid_status"),
    ("Missing required heading:", "field.missing_heading"),
    ("Field definition table must carry", "field.missing_field_id"),
]

_WARNING_RULES = [
    ("字段与校验反向绑定未发现", "field.missing_vl_binding"),
]


def _check_id(msg: str, *, warning: bool = False) -> str:
    rules = _WARNING_RULES if warning else _ERROR_RULES
    for needle, check_id in rules:
        if needle in msg:
            return check_id
    return "field.semantic" if warning else "field.structural"


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
