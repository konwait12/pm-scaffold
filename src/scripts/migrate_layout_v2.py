#!/usr/bin/env python3
"""Migrate REQ-DIR folders from the flat Wave layout to the v2 stage layout."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

MAPPINGS = {
    "00_input": "00-input",
    "01_background-goal": "001-business-requirements/01-background-goal",
    "02_journey-stories": "001-business-requirements/02-user-journey-stories",
    "03_ux": "002-product-requirements/01-product-ux",
    "04_function": "002-product-requirements/02-function-description",
    "05_prd": "003-prd-output",
    "99_review": "99-review",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_manifest(req_dir: Path) -> dict[str, str]:
    return {
        str(path.relative_to(req_dir)): digest(path)
        for path in sorted(req_dir.rglob("*")) if path.is_file()
    }


def plan_migration(req_dir: Path) -> dict:
    moves = []
    conflicts = []
    for old, new in MAPPINGS.items():
        source, target = req_dir / old, req_dir / new
        if not source.exists():
            continue
        if target.exists():
            conflicts.append({"source": old, "target": new, "reason": "target exists"})
        else:
            moves.append({"source": old, "target": new})
    return {"requirement": req_dir.name, "moves": moves, "conflicts": conflicts}


def rewrite_paths(req_dir: Path) -> int:
    changed = 0
    replacements = sorted(MAPPINGS.items(), key=lambda pair: len(pair[0]), reverse=True)
    for path in req_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in replacements:
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def mark_simulated(req_dir: Path) -> int:
    if not req_dir.name.startswith("REQ-002-"):
        return 0
    changed = 0
    for path in req_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        updated = text.replace("status: confirmed", "status: simulated")
        updated = updated.replace("status = confirmed", "status = simulated")
        if "artifact_id:" in updated and "simulation: true" not in updated:
            updated = updated.replace("artifact_id:", "simulation: true\nartifact_id:", 1)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def apply_migration(req_dir: Path, plan: dict) -> dict:
    if plan["conflicts"]:
        raise RuntimeError(f"migration conflicts: {plan['conflicts']}")
    before = file_manifest(req_dir)
    for move in plan["moves"]:
        source, target = req_dir / move["source"], req_dir / move["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(target))
    rewritten = rewrite_paths(req_dir)
    simulated = mark_simulated(req_dir)
    after = file_manifest(req_dir)
    review_dir = req_dir / "99-review"
    review_dir.mkdir(parents=True, exist_ok=True)
    result = {
        **plan,
        "applied_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "rewritten_markdown_files": rewritten,
        "simulated_files": simulated,
        "before_hashes": before,
        "after_hashes": after,
    }
    (review_dir / "layout-migration-v2.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="One-shot migration tool: flat Wave layout -> v2 stage layout. "
                    "Only needed for requirements created before the v2 layout.",
    )
    parser.add_argument("req_dirs", nargs="+", type=Path)
    parser.add_argument("--apply", action="store_true", help="Actually move/rewrite requirement files")
    parser.add_argument("--confirm", action="store_true",
                        help="Required with --apply: acknowledge that files will be moved and rewritten")
    args = parser.parse_args()
    if args.apply and not args.confirm:
        print("ERROR: --apply moves directories and rewrites .md content in place.", file=sys.stderr)
        print("       This is a one-shot migration tool; run without --apply for a dry-run,", file=sys.stderr)
        print("       or re-run with --apply --confirm to proceed.", file=sys.stderr)
        return 2
    results = []
    for req_dir in args.req_dirs:
        if not req_dir.is_dir():
            print(f"ERROR: {req_dir} is not a directory", file=sys.stderr)
            return 1
        plan = plan_migration(req_dir)
        if args.apply:
            plan = apply_migration(req_dir, plan)
        results.append(plan)
    print(json.dumps({"mode": "apply" if args.apply else "dry-run", "results": results}, ensure_ascii=False, indent=2))
    return 1 if any(result["conflicts"] for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())
