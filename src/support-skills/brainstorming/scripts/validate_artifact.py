#!/usr/bin/env python3
"""Validate the stable structure of a brainstorming Markdown artifact.

The artifact (99-review/support/brainstorming-output.md) is a support record
produced when the entry router reports L0 (idea only) or materials are thin.
It contains an SCN-XXX candidate table (all AI_INFERENCE) and an 8-column
human disposition table; only `include` candidates carry a write-back target.
The record itself never reaches status `confirmed`.
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
    "reviewer",
    "created_at",
    "updated_at",
    "confirmed_at",
}

# Chinese section headings (the artifact is a Chinese support record).
REQUIRED_HEADINGS = [
    "原始输入",
    "发散结果",
    "候选清单",
    "人工处置表",
    "收敛后输入包",
    "版本变更摘要",
]

# The brainstorming record is a candidate set for human disposition: it may
# never itself reach `confirmed` (only pipeline.py review may confirm the
# downstream work item after the input package is written back).
VALID_STATUSES = {
    "draft",
    "needs_user_input",
    "conditional_review",
    "ready_for_human_review",
}

DISPOSITIONS = {"include", "exclude", "defer", "research"}

PENDING_PLACEHOLDERS = ("待填写", "待确认", "待补充", "TBD", "tbd")


def _normalize_heading(heading: str) -> str:
    """Strip a leading '## ', numbering like '1. ' and trailing （…） suffixes."""
    heading = re.sub(r"^##\s+", "", heading)
    return re.sub(r"\s*（[^）]*）\s*$", "", re.sub(r"^\d+\.\s*", "", heading).strip()).strip()


def parse_frontmatter(text: str) -> dict[str, str]:
    # Allow an optional leading HTML comment block (the template and example
    # artifacts ship with a desensitization header).
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


def _split_sections(text: str) -> list[tuple[str, str]]:
    """Split the artifact into (heading_line, body) sections on ^## lines."""
    sections: list[tuple[str, str]] = []
    current = "HEAD"
    body: list[str] = []
    for line in text.splitlines():
        if re.match(r"^##\s+", line):
            if body:
                sections.append((current, "\n".join(body)))
            current = line
            body = []
        else:
            body.append(line)
    if body:
        sections.append((current, "\n".join(body)))
    return sections


def _is_placeholder(cell: str) -> bool:
    cell = cell.strip().strip("`").strip()
    if not cell:
        return True
    return any(p in cell for p in PENDING_PLACEHOLDERS)


def _col_map(header: list[str]) -> dict[str, int]:
    """Map normalized header labels to column indexes."""
    mapping: dict[str, int] = {}
    for i, cell in enumerate(header):
        norm = re.sub(r"\W+", "", cell).lower()
        if "candidateid" in norm or ("candidate" in norm and "id" in norm):
            mapping["id"] = i
        if "disposition" in norm:
            mapping["disposition"] = i
        if "writeback" in norm and "target" in norm:
            mapping["writeback"] = i
        if "evidence" in norm:
            mapping["evidence"] = i
        if "impact" in norm:
            mapping["impact"] = i
    return mapping


def _parse_tables(sections: list[tuple[str, str]]) -> list[tuple[str, list[str], list[list[str]]]]:
    """Extract (heading, header_cells, data_rows) for every table with an
    identifiable header. Data rows are rows containing an SCN-XXX cell."""
    tables: list[tuple[str, list[str], list[list[str]]]] = []
    for heading, body in sections:
        rows: list[list[str]] = []
        for line in body.splitlines():
            s = line.strip()
            if s.startswith("|") and s.endswith("|"):
                rows.append([c.strip() for c in s.strip("|").split("|")])
        if not rows:
            continue
        header_idx = None
        for i, cells in enumerate(rows):
            joined = " ".join(cells)
            if re.search(r"candidate\s*id|disposition|evidence|impact", joined, re.IGNORECASE):
                header_idx = i
                break
        if header_idx is None:
            continue
        header = rows[header_idx]
        data = [r for r in rows[header_idx + 1:]
                if any(re.search(r"SCN-\d+", c) for c in r)]
        tables.append((heading, header, data))
    return tables


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
    if status:
        if status == "confirmed":
            errors.append(
                "Invalid status 'confirmed': the brainstorming record is a candidate set for "
                "human disposition and never reaches confirmed; only the downstream work item "
                "may be confirmed via pipeline.py review"
            )
        elif status not in VALID_STATUSES:
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

    sections = _split_sections(text)
    tables = _parse_tables(sections)

    has_candidate_table = False
    has_disposition_table = False
    for heading, header, data_rows in tables:
        cols = _col_map(header)
        if not data_rows:
            continue
        if "evidence" in cols and "impact" in cols:
            has_candidate_table = True
            for row in data_rows:
                for col, label in (("evidence", "Evidence"), ("impact", "Impact")):
                    if col in cols and (cols[col] >= len(row) or _is_placeholder(row[cols[col]])):
                        errors.append(
                            f"{_normalize_heading(heading)}: candidate {row[0] if row else '?'} "
                            f"has placeholder/empty {label}; every candidate needs non-placeholder "
                            f"{label}"
                        )
        if "disposition" in cols:
            has_disposition_table = True
            for row in data_rows:
                if cols["disposition"] >= len(row):
                    errors.append(f"Disposition table row {row[0] if row else '?'} has no disposition value")
                    continue
                disposition = row[cols["disposition"]].strip().lower()
                if disposition not in DISPOSITIONS:
                    errors.append(
                        f"Invalid disposition '{row[cols['disposition']].strip()}' for {row[0] if row else '?'}: "
                        f"must be one of {', '.join(sorted(DISPOSITIONS))}"
                    )
                if disposition == "include":
                    if "writeback" not in cols or cols["writeback"] >= len(row) \
                            or _is_placeholder(row[cols["writeback"]]):
                        errors.append(
                            f"Include candidate {row[0] if row else '?'} has no non-placeholder "
                            f"Write-back Target; every include item must name its write-back "
                            f"destination in the project-background-goal input package"
                        )
                if disposition == "research":
                    warnings.append(
                        f"{row[0] if row else '?'}: disposition is 'research'; ensure it is "
                        f"registered in issue-record / a QuestionRecord with an owner"
                    )

    if not has_candidate_table:
        errors.append("No SCN-XXX candidate table found (a table with Candidate ID + Evidence + Impact columns)")
    if not has_disposition_table:
        errors.append("No disposition table found (a table with a Human Disposition column)")

    # Soft: a ready_for_human_review record should contain a converged input
    # package of sufficient length when include items exist.
    if status == "ready_for_human_review":
        bundle = ""
        for heading, body in sections:
            if _normalize_heading(heading) == "收敛后输入包":
                bundle = re.sub(r"待填写|待确认|TBD", "", body)
                break
        if len(bundle.strip()) < 50:
            warnings.append(
                "收敛后输入包 section is shorter than 50 chars; the input package handed to "
                "project-background-goal should be a sufficient bundle (≥ 50 字)"
            )

    issues = []
    for e in errors:
        issues.append({"code": "BS-STRUCT", "severity": "blocking", "message": e, "waivable": False})
    for w in warnings:
        issues.append({"code": "BS-SEMANTIC", "severity": "advisory", "message": w, "waivable": False})
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
