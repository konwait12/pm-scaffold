#!/usr/bin/env python3
"""Validate the §功能清单 (feature list) section of a function-description artifact.

The feature-list sub-skill produces the §功能清单 section of the parent
function-description.md artifact (registry `output_section`: 功能清单). This
validator checks that:

  1. the 功能清单 section exists in the parent artifact;
  2. at least one FEA-XXX identifier is present (the FEA-XXX placeholder does not count);
  3. every FEA table row in the section traces to ≥1 ST-XXX (no orphan feature);
  4. the artifact status is in the whitelist, which deliberately EXCLUDES
     `confirmed` — a sub-skill can never write confirmed; only
     `pipeline.py review --decision approve` may.

Two run modes:

  * explicit:  python3 validate_artifact.py <parent-or-fixture-artifact.md> [--json]
  * default:   (no path) auto-resolve the parent function-description.md under
               requirements/*/002-product-requirements/02-function-description/
               and validate it.

run_tests.sh always passes a fixture path (mode 1); the pipeline/orchestrator
can rely on the default mode (mode 2).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ── Per-sub-skill configuration (edit these) ──────────────
SECTION_NAME = "功能清单"
FEA_ID_RE = re.compile(r"FEA-\d+")
ST_ID_RE = re.compile(r"ST-\d+")
# Status whitelist deliberately EXCLUDES `confirmed`: only the pipeline may set it.
VALID_STATUSES = {
    "draft",
    "needs_user_input",
    "conditional_review",
    "ready_for_human_review",
    "superseded",
    "legacy_unverified",
    "simulated",
}
PARENT_ARTIFACT_GLOBS = [
    "requirements/*/002-product-requirements/02-function-description/function-description.md",
    "requirements/*/002-product-requirements/function-description.md",
]
# ─────────────────────────────────────────────────────────


def _norm(h: str) -> str:
    # Strip leading numbering ("1. ") and trailing （…） suffixes so headings
    # like "## 1. 功能清单（Feature List）" match SECTION_NAME.
    return re.sub(r"\s*（[^）]*）\s*$", "", re.sub(r"^\d+\.\s*", "", h).strip()).strip()


def _project_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "src" / "framework" / "workflow-registry.json").is_file():
            return parent
    return p.parents[8]


def parse_frontmatter(text: str) -> dict[str, str]:
    # Allow optional leading HTML comment block(s) before the YAML frontmatter.
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


def _section_text(text: str) -> str | None:
    """Return the §功能清单 block: from its (possibly numbered) heading to the next
    ##/### heading. Supports both "## N. 功能清单" and "### N.N 功能清单" forms."""
    headings = list(re.finditer(r"^#{2,3}\s+(.+?)\s*$", text, re.MULTILINE))
    for i, m in enumerate(headings):
        if _norm(m.group(1)) == _norm(SECTION_NAME):
            end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
            return text[m.start():end]
    return None


def _orphan_fea_rows(section: str) -> list[str]:
    """FEA table rows inside the section that carry no ST-XXX traceability."""
    orphans: list[str] = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|") or "---" in line:
            continue
        if FEA_ID_RE.search(line) and not ST_ID_RE.search(line):
            ids = sorted(set(FEA_ID_RE.findall(line)))
            orphans.append(f"{'/'.join(ids)} (row: {line[:80]}…)")
    return orphans


def validate(path: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}

    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    status = meta.get("status")

    if not meta:
        warnings.append("No frontmatter found; artifact status cannot be verified")
    elif status == "confirmed":
        errors.append(
            "status 'confirmed' is not allowed for this sub-skill output; "
            "only pipeline.py review --decision approve may set confirmed"
        )
    elif status and status not in VALID_STATUSES:
        errors.append(
            f"Invalid status '{status}'. Valid (excluding confirmed): "
            f"{', '.join(sorted(VALID_STATUSES))}"
        )

    section = _section_text(text)
    if section is None:
        errors.append(f"Missing required section: {SECTION_NAME}")
        return {"ok": not errors, "errors": errors, "warnings": warnings}

    # FEA identifiers must exist in the section (FEA-XXX placeholder does not count).
    fea_ids = sorted(set(FEA_ID_RE.findall(section)))
    if not fea_ids:
        errors.append(f"No FEA-XXX feature identifiers found in section {SECTION_NAME}")

    # Every FEA table row must trace to ≥1 ST-XXX.
    orphans = _orphan_fea_rows(section)
    if orphans:
        errors.append("FEA row(s) without ST-XXX story traceability: " + "; ".join(orphans))

    # Reverse sanity: if FEA rows exist, the section must reference some ST-XXX.
    st_ids = sorted(set(ST_ID_RE.findall(section)))
    if fea_ids and not st_ids:
        errors.append(f"No ST-XXX identifiers found in section {SECTION_NAME}")

    # Priority markers present (P0/P1/P2)?
    if not re.search(r"\bP[012]\b", section):
        warnings.append(f"No P0/P1/P2 priority markers found in section {SECTION_NAME}")

    # Knowledge-state tags present for traceable content.
    if not any(tag in section for tag in ("FACT", "DECISION", "AI_INFERENCE", "UNKNOWN")):
        warnings.append(
            f"No knowledge-state tags (FACT/DECISION/AI_INFERENCE/UNKNOWN) found in section {SECTION_NAME}"
        )

    if status == "ready_for_human_review" and not fea_ids:
        warnings.append("status is ready_for_human_review but no FEA identifiers found")

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def resolve_artifact(path_arg: str | None) -> Path | None:
    """Explicit path wins; otherwise auto-resolve the parent function-description.md."""
    if path_arg:
        return Path(path_arg)
    root = _project_root()
    for glob in PARENT_ARTIFACT_GLOBS:
        for hit in sorted(root.glob(glob)):
            return hit
    return None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path, nargs="?", default=None,
                   help="Parent artifact (or fixture) path. Default: auto-resolve the "
                        "parent function-description.md.")
    p.add_argument("--json", action="store_true", dest="j")
    args = p.parse_args()

    path = resolve_artifact(args.artifact)
    if path is None:
        msg = (
            "No artifact provided and no parent function-description.md found "
            "under requirements/*/. "
            "Run: python3 validate_artifact.py <parent-or-fixture-artifact.md> [--json]"
        )
        if args.j:
            print(json.dumps({"ok": False, "errors": [msg], "warnings": []},
                             ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: {msg}")
        return 2

    r = validate(path)
    if args.j:
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
