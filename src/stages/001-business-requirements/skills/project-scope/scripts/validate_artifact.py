"""
Validate the stable structure of a project-scope Markdown artifact.

The artifact is always Chinese because the deliverable is consumed by business
stakeholders. Section headings match exactly the strings in REQUIRED_HEADINGS.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FRONTMATTER = {
    "artifact_id",
    "version",
    "status",
    "owner",
    "goal_decision_owner",
    "business_sponsor",
    "reviewer",
    "created_at",
    "updated_at",
    "confirmed_at",
}

REQUIRED_HEADINGS = [
    "项目元数据",
    "范围总览",
    "In-Scope（已确认纳入本期）",
    "Out-of-Scope（已确认不做）",
    "Deferred（暂缓做）",
    "Conditional（条件成立则纳入）",
    "来源追溯",
    "待确认问题",
    "Constitution Compliance",
    "版本变更摘要",
]

PENDING_PLACEHOLDERS = ("待确认",)

VALID_STATUSES = {
    "draft",
    "needs_user_input",
    "conditional_review",
    "ready_for_human_review",
    "confirmed",
    "superseded",
}


def _normalize_heading(heading: str) -> str:
    return re.sub(r"\s*（[^）]*）\s*$", "", re.sub(r"^\d+\.\s*", "", heading).strip()).strip()


def parse_frontmatter(text: str) -> dict[str, str]:
    text = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.DOTALL)
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"\'')
    return result


def validate(path: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}

    text = path.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)

    missing_metadata = sorted(REQUIRED_FRONTMATTER - metadata.keys())
    if missing_metadata:
        errors.append(f"Missing frontmatter fields: {', '.join(missing_metadata)}")

    status = metadata.get("status")
    if status and status not in VALID_STATUSES:
        errors.append(
            f"Invalid status '{status}'. Valid: {', '.join(sorted(VALID_STATUSES))}"
        )

    artifact_headings = [
        _normalize_heading(match.group(1))
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    ]

    missing_headings = [
        h for h in REQUIRED_HEADINGS
        if _normalize_heading(h) not in artifact_headings
    ]
    if missing_headings:
        errors.append(f"Missing required headings: {', '.join(missing_headings)}")

    # Out-of-Scope must have at least 1 item with a reason.
    out_match = re.search(
        r"^##\s+\d+\.\s*Out-of-Scope.*?$(.*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if out_match:
        out_body = out_match.group(1)
        # Check that the body has at least one data row (a table row with S-1xx).
        out_rows = [line for line in out_body.splitlines()
                    if line.lstrip().startswith("|") and "S-1" in line]
        if not out_rows:
            warnings.append(
                "Soft: Out-of-Scope has no S-1xx items; confirm that nothing is explicitly excluded. "
                "A scope with no exclusions is a red flag."
            )

    # ready_for_human_review requires all four lists to be non-empty.
    if status == "ready_for_human_review":
        for section_pattern, label in [
            (r"^##\s+\d+\.\s*In-Scope.*?$(.*?)(?=^##\s+|\Z)", "In-Scope"),
            (r"^##\s+\d+\.\s*Out-of-Scope.*?$(.*?)(?=^##\s+|\Z)", "Out-of-Scope"),
        ]:
            m = re.search(section_pattern, text, re.MULTILINE | re.DOTALL)
            if m:
                cleaned = re.sub(r"待确认|UNKNOWN|TBD", "", m.group(1)).strip()
                if len(cleaned) < 30:
                    warnings.append(
                        f"Semantic: {label} section is essentially empty at ready_for_human_review"
                    )

    if "SRC-" not in text:
        errors.append("No SRC-* source traceability identifier found")

    if status == "confirmed":
        unresolved = [
            k for k in ("goal_decision_owner", "business_sponsor", "reviewer", "confirmed_at")
            if metadata.get(k, "") in {"", *PENDING_PLACEHOLDERS}
        ]
        if unresolved:
            errors.append(
                "Confirmed artifact has unresolved confirmation fields: "
                + ", ".join(unresolved)
            )

    if any(p in text for p in PENDING_PLACEHOLDERS) and status == "confirmed":
        body_without_headings = re.sub(
            r"^##\s+\d+\.\s*[^\n]*$", "", text, flags=re.MULTILINE
        )
        if any(p in body_without_headings for p in PENDING_PLACEHOLDERS):
            warnings.append(
                "Confirmed artifact still contains 待确认 markers in body content; "
                "verify these are accepted non-blocking items"
            )

    issues = []
    for e in errors:
        issues.append({"code": "SC-STRUCT", "severity": "blocking", "message": e, "waivable": False})
    for w in warnings:
        issues.append({"code": "SC-SEMANTIC", "severity": "advisory", "message": w, "waivable": False})
    return {"ok": not errors, "errors": errors, "warnings": warnings, "issues": issues}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = validate(args.artifact)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS" if result["ok"] else "FAIL")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
