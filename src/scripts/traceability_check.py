#!/usr/bin/env python3
"""Validate explicit G→ST→FEA→FUN→AC/BR relationships across artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from workflow_registry import find_artifact, work_items

PATTERNS = {
    "goal": r"\bG\d+\b",
    "story": r"\bST-\d+\b",
    "feature": r"\bFEA-\d+\b",
    "function": r"\bFUN-\d+\b",
    "acceptance": r"\bAC-\d+\b",
    "rule": r"\bBR-\d+\b",
}
REQUIRED_EDGES = [
    ("story", "goal"),
    ("feature", "story"),
    ("function", "feature"),
    ("acceptance", "function"),
    ("rule", "function"),
]
CROSS_LEVEL_EDGES = [
    ("acceptance", "goal"),  # G↔AC: each acceptance criterion should reference the goal it validates
]
# Reverse direction: every upstream ID must be referenced by some downstream ID
# (no orphan goals / stories / features / functions that nothing traces to).
REVERSE_EDGES = [
    ("goal", "story"),
    ("story", "feature"),
    ("feature", "function"),
    ("function", "acceptance"),
    ("function", "rule"),
]


def collect(req_dir: Path) -> tuple[dict[str, set[str]], set[tuple[str, str]], dict[str, str]]:
    ids = {kind: set() for kind in PATTERNS}
    edges: set[tuple[str, str]] = set()
    locations = {}
    for item in work_items():
        artifact = find_artifact(req_dir, item)
        if not artifact:
            continue
        for line_no, line in enumerate(artifact.read_text(encoding="utf-8").splitlines(), 1):
            # Table rows: connect IDs across the entire row (columns represent relationships)
            if line.lstrip().startswith("|") and "---" not in line:
                row_ids = {}
                for kind, pattern in PATTERNS.items():
                    found = set(re.findall(pattern, line))
                    row_ids[kind] = found
                    ids[kind].update(found)
                    for identifier in found:
                        locations.setdefault(identifier, f"{artifact.relative_to(req_dir)}:{line_no}")
                for downstream, upstream in REQUIRED_EDGES + CROSS_LEVEL_EDGES:
                    for child in row_ids[downstream]:
                        for parent in row_ids[upstream]:
                            edges.add((child, parent))
            else:
                # Non-table lines: connect IDs that appear together
                line_ids = {}
                for kind, pattern in PATTERNS.items():
                    found = set(re.findall(pattern, line))
                    line_ids[kind] = found
                    ids[kind].update(found)
                    for identifier in found:
                        locations.setdefault(identifier, f"{artifact.relative_to(req_dir)}:{line_no}")
                for downstream, upstream in REQUIRED_EDGES + CROSS_LEVEL_EDGES:
                    for child in line_ids[downstream]:
                        for parent in line_ids[upstream]:
                            edges.add((child, parent))
    return ids, edges, locations


def validate(req_dir: Path) -> dict:
    ids, edges, locations = collect(req_dir)
    issues = []
    for downstream, upstream in REQUIRED_EDGES:
        upstream_ids = ids[upstream]
        downstream_ids = ids[downstream]
        if not downstream_ids:
            issues.append({"severity": "CRITICAL", "relation": f"{upstream}->{downstream}", "message": f"No {downstream} IDs found"})
            continue
        if not upstream_ids:
            issues.append({"severity": "CRITICAL", "relation": f"{upstream}->{downstream}", "message": f"No {upstream} IDs found"})
            continue
        linked_children = {child for child, parent in edges if child in downstream_ids and parent in upstream_ids}
        for orphan in sorted(downstream_ids - linked_children):
            issues.append({
                "severity": "CRITICAL",
                "relation": f"{upstream}->{downstream}",
                "id": orphan,
                "location": locations.get(orphan),
                "message": f"{orphan} has no explicit {upstream} link on the same traceability row or statement",
            })
    for downstream, upstream in CROSS_LEVEL_EDGES:
        upstream_ids = ids[upstream]
        downstream_ids = ids[downstream]
        if not downstream_ids or not upstream_ids:
            continue
        linked = {child for child, parent in edges if child in downstream_ids and parent in upstream_ids}
        for orphan in sorted(downstream_ids - linked):
            issues.append({
                "severity": "HIGH",
                "relation": f"{upstream}↔{downstream} (cross-level)",
                "id": orphan,
                "location": locations.get(orphan),
                "message": f"{orphan} has no explicit {upstream} link — verify this AC validates the correct business goal",
            })
    # Reverse traceability: every upstream ID must be consumed by some downstream.
    for upstream, downstream in REVERSE_EDGES:
        upstream_ids = ids[upstream]
        downstream_ids = ids[downstream]
        if not upstream_ids:
            continue
        referenced = {parent for child, parent in edges if child in downstream_ids and parent in upstream_ids}
        for orphan in sorted(upstream_ids - referenced):
            issues.append({
                "severity": "MEDIUM",
                "relation": f"{upstream}←{downstream} (reverse)",
                "id": orphan,
                "location": locations.get(orphan),
                "message": f"{orphan} is not referenced by any {downstream} — reverse traceability gap",
            })
    return {
        "ok": not any(issue["severity"] in {"CRITICAL", "HIGH"} for issue in issues),
        "counts": {kind: len(values) for kind, values in ids.items()},
        "edge_count": len(edges),
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("req_dir", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.req_dir.is_dir():
        print(f"ERROR: {args.req_dir} is not a directory", file=sys.stderr)
        return 1
    result = validate(args.req_dir)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Traceability: {'PASS' if result['ok'] else 'FAIL'}")
        print(f"Counts: {result['counts']} edges={result['edge_count']}")
        for issue in result["issues"]:
            print(f"  [{issue['severity']}] {issue['relation']}: {issue['message']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
