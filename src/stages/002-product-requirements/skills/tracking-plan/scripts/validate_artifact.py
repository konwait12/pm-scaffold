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
import re
import sys
from pathlib import Path

# ── Per-sub-skill configuration (edit these) ──────────────
SECTION_NAME = "埋点需求分析"        # sub-skill output section in parent artifact
ID_PATTERN = r"EV-\d+"              # event ID prefix
REQUIRED_REFS = (r"FUN-\d+", r"G-\d+")  # every event must link to a FUN and a G
# Path to parent artifact, relative to the sub-skill scripts/ dir.
PARENT_ARTIFACT = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "function-description.md"
)
# ─────────────────────────────────────────────────────────


def _norm(h: str) -> str:
    return re.sub(r"^\d+\.\s*", "", h).strip()


def _extract_section(text: str, section_name: str) -> str:
    """Extract the body under `## <section_name>` (or its numbered variant)."""
    pattern = (
        r"^##\s+(?:\d+\.\s*)?" + re.escape(section_name) + r".*?$"
        r"(.*?)(?=^##\s+|\Z)"
    )
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def validate(path: Path) -> dict:
    errors, warnings = [], []
    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}

    text = path.read_text(encoding="utf-8")

    # Section must exist
    headings = [_norm(m.group(1)) for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]
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
