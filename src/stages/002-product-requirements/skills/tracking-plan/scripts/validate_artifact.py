#!/usr/bin/env python3
"""Sub-skill validator · tracking-plan

tracking-plan is a Branch skill whose output is an independent artifact
(`99-review/support/tracking-plan.md` under each requirement dir), not a
independent tracking-plan artifact. This validator checks that the
§埋点需求分析 section is present and that expected ID prefixes exist.

Copy template from `src/shared/audit/subskill-validator-template.py`.

Run: python3 validate_artifact.py [tracking-plan.md] [--json]
"""

from __future__ import annotations

import argparse
import json
import os
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


# ── Per-sub-skill configuration (edit these) ──────────────
SECTION_NAME = "埋点需求分析"        # sub-skill output section in parent artifact
ID_PATTERN = r"EV-\d+"              # event ID prefix
REQUIRED_REFS = (r"FUN-\d+", r"G\d+")  # every event must link to a FUN and a G
#
# tracking-plan is a Branch skill (see src/framework/workflow-registry.json
# support_capabilities.tracking-plan): its output is an INDEPENDENT artifact
# written to `99-review/support/tracking-plan.md` under each requirement dir —
# NOT a section of another work item. The default target must
# therefore point at that branch artifact location, not at the
# core product templates (which have no §埋点需求分析 section and would
# FAIL by misjudgment). Callers may still override via the CLI positional arg
# or the PM_PARENT_ARTIFACT env var.
# ─────────────────────────────────────────────────────────

# ── Frontmatter contract (per src/templates/_frontmatter-schema.md) ──
# Every field the branch template `templates/tracking-plan-output.md` declares
# must be referenced by this validator (registry_contract_check E3_drift closure).
# Branch artifacts may legitimately carry empty metadata while in draft, so a
# missing/empty field is a WARNING, not a hard ERROR — the only hard error is a
# `status: confirmed` written by an AI (constitution red line; confirmed is set
# solely by `pipeline.py review --decision approve`).
FRONTMATTER_FIELDS = {
    "artifact_id": "全局唯一产物 ID",
    "version": "语义化版本",
    "status": "产物状态（见 _frontmatter-schema.md §2 枚举）",
    "owner": "产物负责人",
    "business_fact_owner": "业务事实负责人",
    "goal_decision_owner": "目标/决策负责人",
    "reviewer": "授权人工 review 人",
    "created_at": "首次创建日期",
    "updated_at": "最后更新日期",
    "confirmed_at": "人工确认日期（仅 confirmed 填写）",
    "upstream_artifact_id": "上游产物 ID",
}
VALID_STATUSES = {
    "draft", "needs_user_input", "conditional_review",
    "ready_for_human_review", "superseded", "legacy_unverified", "simulated",
}


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse the YAML frontmatter header into a {field: value} dict.

    Allows an optional leading HTML comment block before the header (the
    template and generated artifacts both open with a `<!-- ... -->` note).
    Returns {} when no frontmatter is present.
    """
    body = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.DOTALL)
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", body, re.DOTALL)
    if not m:
        return {}
    meta: dict[str, str] = {}
    for line in m.group(1).splitlines():
        line = line.split("#", 1)[0].rstrip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        if key:
            meta[key] = value.strip().strip('"').strip("'")
    return meta


def _check_frontmatter(text: str, errors: list[str], warnings: list[str]) -> None:
    """Validate frontmatter metadata per `_frontmatter-schema.md`.

    Missing/empty core fields are advisory (branch artifacts stay draftable);
    an AI-written `status: confirmed` is the one blocking violation.
    """
    meta = parse_frontmatter(text)
    if not meta:
        warnings.append("No frontmatter found; artifact status and metadata cannot be verified")
        return
    status = meta.get("status")
    if status == "confirmed":
        errors.append(
            "status 'confirmed' is not allowed for this work_item output; "
            "only pipeline.py review --decision approve may set confirmed"
        )
    elif status and status not in VALID_STATUSES:
        warnings.append(
            f"Unrecognized status '{status}' (not in standard whitelist); "
            "check the frontmatter 'status' field"
        )
    for field, purpose in FRONTMATTER_FIELDS.items():
        if field == "status":
            continue  # status handled above with stricter semantics
        if not meta.get(field):
            warnings.append(
                f"Frontmatter field '{field}' ({purpose}) is empty or missing; "
                "fill it in before sending the artifact for confirmed review"
            )


def _default_artifact() -> Path | None:
    """Resolve the default branch artifact location.

    The validator is typically invoked from the repo root, so we look for
    `requirements/*/99-review/support/tracking-plan.md` under the current
    working directory. When several requirements carry a tracking-plan, the
    most recently modified one is used (the active requirement). Returns None
    when none is found so main() can report a clear error instead of silently
    validating the wrong (template) file.
    """
    candidates = sorted(
        Path.cwd().glob("requirements/*/99-review/support/tracking-plan.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def _resolve_artifact(explicit: Path | None) -> Path | None:
    """Resolve the artifact to validate: CLI arg > PM_PARENT_ARTIFACT > default."""
    if explicit is not None:
        return explicit
    env = os.environ.get("PM_PARENT_ARTIFACT")
    if env:
        return Path(env)
    return _default_artifact()


def _norm(h: str) -> str:
    """Strip leading numbering (handles both `## 5.` and `### 5.2` variants)."""
    return re.sub(r"^\d+(\.\d+)*\.?\s*", "", h).strip()


def _extract_section(text: str, section_name: str) -> str:
    """Extract the body under `## <section_name>` (or its H3 variant).

    Accepts both H2 (`## 埋点需求`) and H3 (`### 5.2 埋点需求`) headings
    so the same validator works on either the standalone tracking-plan
    artifact or the embedded PRD §5.2 section.

    The body runs until the next H2 section (sibling break) — sub-
    headings under the section (H3 / H4 / H5) are included so they
    can be validated for nested content like `### 2. 事件清单（EV-XXX）`.
    The starting heading itself is matched at H2 OR H3; if it was H3,
    the stop is at the next H2 only (so the validator behaves correctly
    when running on either standalone tracking-plan (H2 root) or PRD
    §5.2 (H3 root)).
    """
    # Find the section start (H2 or H3).
    start_pattern = (
        r"^(#{2,3})\s+(?:\d+(?:\.\d+)*\.?\s*)?" + re.escape(section_name) + r".*?$"
    )
    start_match = re.search(start_pattern, text, re.MULTILINE)
    if not start_match:
        return ""
    start_hash = start_match.group(1)  # "##" or "###"
    start_level = len(start_hash)
    start_pos = start_match.end()
    # Find the next heading at the same level or shallower (smaller heading count).
    end_pattern = re.compile(r"^(#{2," + str(start_level) + r"})\s+", re.MULTILINE)
    end_match = end_pattern.search(text, pos=start_pos)
    end_pos = end_match.start() if end_match else len(text)
    return text[start_pos:end_pos]


def _make_result(path: Path, errors: list[str], warnings: list[str]) -> dict:
    issues = [
        make_issue(
            severity="CRITICAL",
            check_id=_tp_error_check_id(e),
            family="tracking_plan",
            location=str(path),
            message=e,
        )
        for e in errors
    ]
    issues.extend(
        make_issue(
            severity="MEDIUM",
            check_id=_tp_warning_check_id(w),
            family="tracking_plan",
            location=str(path),
            message=w,
            blocking=False,
        )
        for w in warnings
    )
    return {"ok": not errors, "errors": errors, "warnings": warnings, "issues": issues}


_TP_ERROR_RULES = [
    ("File not found:", "tp.file_not_found"),
    ("Missing required section:", "tp.missing_section"),
    ("Empty section:", "tp.empty_section"),
    ("No EV-", "tp.no_event_ids"),
    ("missing reference to", "tp.event_missing_ref"),
]

_TP_WARNING_RULES = [
    ("no pii_flag values detected", "tp.no_pii_flags"),
    ("coverage matrix not found", "tp.no_coverage_matrix"),
]


def _tp_error_check_id(msg: str) -> str:
    for needle, check_id in _TP_ERROR_RULES:
        if needle in msg:
            return check_id
    return "tp.structural"


def _tp_warning_check_id(msg: str) -> str:
    for needle, check_id in _TP_WARNING_RULES:
        if needle in msg:
            return check_id
    return "tp.semantic"


def validate(path: Path) -> dict:
    errors, warnings = [], []
    if not path.is_file():
        return _make_result(path, [f"File not found: {path}"], [])

    text = path.read_text(encoding="utf-8")

    # Frontmatter metadata contract (per src/templates/_frontmatter-schema.md)
    _check_frontmatter(text, errors, warnings)

    # Section must exist (accept H2 or H3)
    headings = [
        _norm(m.group(1))
        for m in re.finditer(r"^#{2,3}\s+(.+?)\s*$", text, re.MULTILINE)
    ]
    if _norm(SECTION_NAME) not in headings:
        errors.append(f"Missing required section: {SECTION_NAME}")
        return _make_result(path, errors, warnings)

    section_body = _extract_section(text, SECTION_NAME)
    if not section_body:
        errors.append(f"Empty section: {SECTION_NAME}")
        return _make_result(path, errors, warnings)

    # ID prefix must be present
    ids = re.findall(ID_PATTERN, section_body)
    if not ids:
        errors.append(f"No {ID_PATTERN} identifiers found in section {SECTION_NAME}")

    # Every event must reference FUN- and G-
    event_rows = []
    for line in section_body.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        if "EV-" not in line:
            continue
        if set(line.strip()) <= set("|-: "):
            continue
        event_rows.append([c.strip() for c in line.strip().strip("|").split("|")])

    for cells in event_rows:
        if not cells:
            continue
        row_text = " ".join(cells)
        for ref in REQUIRED_REFS:
            if not re.search(ref, row_text):
                errors.append(
                    f"{cells[0]}: missing reference to {ref} (every event must link "
                    f"to a FUN and a G goal)"
                )
                break

    # PII flag values must be valid
    pii_pattern = r"\b(false|quasi|true|sensitive)\b"
    pii_values = re.findall(pii_pattern, section_body)
    if not pii_values:
        warnings.append(
            "Advisory: no pii_flag values detected; confirm PII section is filled"
        )

    # Coverage matrix sanity: every P0 FUN-XXX has must_track count
    fun_lines = re.findall(r"FUN-\d+", section_body)
    if fun_lines and "must_track" not in section_body:
        warnings.append(
            "Advisory: coverage matrix not found; every P0 FUN-XXX should have "
            "a must_track count"
        )

    return _make_result(path, errors, warnings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "artifact", type=Path, nargs="?", default=None,
        help="Branch artifact path (tracking-plan.md). Defaults to the "
             "resolved branch artifact location under requirements/.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    artifact = _resolve_artifact(args.artifact)
    if artifact is None:
        print(
            "ERROR: no artifact path given and no "
            "requirements/*/99-review/support/tracking-plan.md found "
            "(run from the repo root or pass the artifact path explicitly)",
            file=sys.stderr,
        )
        return 1
    result = validate(artifact)
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
