"""
Validate the stable structure of a brainstorming Markdown artifact.

The artifact is the divergence/convergence process record (brainstorming-output.md),
NOT a PRD deliverable. It never produces `confirmed`.

Section headings follow the template at src/templates/others/brainstorming-output.md.
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


REQUIRED_FRONTMATTER = {
    "artifact_id",
    "version",
    "status",
    "owner",
    "created_at",
    "updated_at",
    "confirmed_at",
}

REQUIRED_HEADINGS = [
    "原始输入",
    "发散结果",
    "候选清单",
    "人工处置表",
    "Include 项写回",
    "收敛后输入包",
    "Constitution Compliance",
    "版本变更摘要",
]

PENDING_PLACEHOLDERS = ("待确认", "待填写", "待补充", "TBD")

VALID_STATUSES = {
    "draft",
    "needs_user_input",
    "conditional_review",
    "ready_for_human_review",
    "confirmed",   # kept in the set only so it can be explicitly rejected below
    "superseded",
}


def parse_frontmatter(text: str) -> dict[str, str]:
    text = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.DOTALL)
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n", text, re.MULTILINE | re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"\'')
    return result


def _collect_rows(body: str, id_prefix: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in body.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        if id_prefix not in line:
            continue
        if set(line.strip()) <= set("|-: "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def validate(path: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}

    text = path.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)
    status = metadata.get("status")

    missing_metadata = sorted(REQUIRED_FRONTMATTER - metadata.keys())
    if missing_metadata:
        errors.append(f"Missing frontmatter fields: {', '.join(missing_metadata)}")

    if status and status not in VALID_STATUSES:
        errors.append(f"Invalid status '{status}'. Valid: {', '.join(sorted(VALID_STATUSES))}")

    if status == "confirmed":
        errors.append("Brainstorming process record must never reach 'confirmed'")

    artifact_headings = [
        re.sub(r"^\d+\.\s*", "", m.group(1)).strip()
        for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    ]
    missing_headings = [h for h in REQUIRED_HEADINGS if h not in artifact_headings]
    if missing_headings:
        errors.append(f"Missing required headings: {', '.join(missing_headings)}")

    # SCN-XXX candidate rows must have non-placeholder Evidence and Impact.
    rows = _collect_rows(text, "SCN-")
    if status in ("ready_for_human_review", "conditional_review") and not rows:
        warnings.append(
            "Advisory: 候选清单 is empty at review. Confirm the ask is genuinely empty."
        )
    for cells in rows:
        # candidate table has exactly 6 columns: ID | 发散维度 | Candidate | Evidence | Impact | 知识状态
        # (disposition table has 8; include write-back table has 3) — scope strictly to candidate rows.
        if len(cells) == 6:
            if any(p in cells[3] for p in PENDING_PLACEHOLDERS) or any(
                p in cells[4] for p in PENDING_PLACEHOLDERS
            ):
                warnings.append(
                    f"Advisory: {cells[0]} candidate has placeholder Evidence or Impact"
                )
            if cells[5].strip() != "AI_INFERENCE":
                warnings.append(
                    f"Advisory: {cells[0]} knowledge state should be AI_INFERENCE before disposition"
                )

    # Disposition table must have non-placeholder disposition for include rows.
    disp_rows = _collect_rows(text, "SCN-")
    for cells in disp_rows:
        # disposition table: ID | Role-Lifecycle | Candidate | Evidence | Impact | Human Disposition | Reason | Write-back Target
        if len(cells) >= 8:
            disp = cells[5].strip()
            reason = cells[6].strip()
            target = cells[7].strip()
            if disp not in ("include", "exclude", "defer", "research"):
                if any(p in disp for p in PENDING_PLACEHOLDERS):
                    warnings.append(
                        f"Advisory: {cells[0]} Human Disposition still placeholder"
                    )
            elif disp == "include":
                if any(p in reason for p in PENDING_PLACEHOLDERS):
                    warnings.append(
                        f"Advisory: {cells[0]} include reason still placeholder"
                    )
                if any(p in target for p in PENDING_PLACEHOLDERS):
                    warnings.append(
                        f"Advisory: {cells[0]} include Write-back Target still placeholder"
                    )

    issues = [
        make_issue(
            severity="CRITICAL",
            check_id=_bs_error_check_id(e),
            family="brainstorming",
            location=str(path),
            message=e,
        )
        for e in errors
    ]
    issues.extend(
        make_issue(
            severity="MEDIUM",
            check_id=_bs_warning_check_id(w),
            family="brainstorming",
            location=str(path),
            message=w,
            blocking=False,
        )
        for w in warnings
    )
    return {"ok": not errors, "errors": errors, "warnings": warnings, "issues": issues}


_BS_ERROR_RULES = [
    ("Missing frontmatter fields:", "bs.missing_frontmatter"),
    ("Invalid status", "bs.invalid_status"),
    ("must never reach 'confirmed'", "bs.confirmed_forbidden"),
    ("Missing required headings:", "bs.missing_headings"),
]

_BS_WARNING_RULES = [
    ("候选清单 is empty at review", "bs.empty_candidate_list_at_review"),
    ("candidate has placeholder Evidence or Impact", "bs.placeholder_candidate"),
    ("knowledge state should be AI_INFERENCE", "bs.non_inference_candidate"),
    ("Human Disposition still placeholder", "bs.placeholder_disposition"),
    ("include Write-back Target still placeholder", "bs.placeholder_writeback"),
    ("include reason still placeholder", "bs.placeholder_include_reason"),
]


def _bs_error_check_id(msg: str) -> str:
    for needle, check_id in _BS_ERROR_RULES:
        if needle in msg:
            return check_id
    return "bs.structural"


def _bs_warning_check_id(msg: str) -> str:
    for needle, check_id in _BS_WARNING_RULES:
        if needle in msg:
            return check_id
    return "bs.semantic"


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