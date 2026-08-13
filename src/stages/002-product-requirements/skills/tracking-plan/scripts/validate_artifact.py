#!/usr/bin/env python3
"""Sub-skill validator · tracking-plan

Each sub-skill produces a section of the parent artifact. This validator
checks that the tracking-plan section is present in the parent
function-description artifact and that expected ID prefixes exist.

Copy template from `src/shared/audit/subskill-validator-template.py`.

Run: python3 validate_artifact.py <parent-artifact.md> [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ── Per-sub-skill configuration (edit these) ──────────────
SECTION_NAME = "埋点需求分析"        # sub-skill output section in parent artifact
ID_PATTERN = r"EV-\d+"              # event ID prefix
REQUIRED_REFS = (r"FUN-\d+", r"G-\d+")  # every event must link to a FUN and a G
# Path to parent artifact, relative to the sub-skill scripts/ dir.
# Tracking-plan writes into the §埋点需求分析 section of the parent
# `function-description.md`. The default points at the template that
# ships with the repository; callers may override via CLI positional arg
# or by setting the PM_PARENT_ARTIFACT env var.
#
# __file__ = src/stages/002-product-requirements/skills/tracking-plan/scripts/validate_artifact.py
# parents[0]=scripts, [1]=tracking-plan, [2]=skills, [3]=002-product-requirements,
# [4]=stages, [5]=src, [6]=<repo root>
_PROJECT_ROOT = Path(__file__).resolve().parents[6]
PARENT_ARTIFACT = Path(os.environ.get(
    "PM_PARENT_ARTIFACT",
    str(
        _PROJECT_ROOT
        / "src"
        / "templates"
        / "stage-2-product"
        / "function-description.md"
    ),
))
# ─────────────────────────────────────────────────────────


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


def validate(path: Path) -> dict:
    errors, warnings = [], []
    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}

    text = path.read_text(encoding="utf-8")

    # Section must exist (accept H2 or H3)
    headings = [
        _norm(m.group(1))
        for m in re.finditer(r"^#{2,3}\s+(.+?)\s*$", text, re.MULTILINE)
    ]
    if _norm(SECTION_NAME) not in headings:
        errors.append(f"Missing required section: {SECTION_NAME}")
        return {"ok": False, "errors": errors, "warnings": warnings}

    section_body = _extract_section(text, SECTION_NAME)
    if not section_body:
        errors.append(f"Empty section: {SECTION_NAME}")
        return {"ok": False, "errors": errors, "warnings": warnings}

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

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "artifact", type=Path, nargs="?", default=None,
        help="Parent artifact path. Defaults to configured path.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    artifact = args.artifact or PARENT_ARTIFACT
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
