#!/usr/bin/env python3
"""Compatibility entry point for shared review, change, and reflow records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from workflow_registry import (
    artifact_content_hash,
    find_artifact,
    read_frontmatter,
    work_items,
)


def validate_records(req_dir: Path) -> dict:
    issues = []
    artifacts = {}
    review_records = list(req_dir.glob("99-review/review-*.md"))
    for item in work_items():
        artifact = find_artifact(req_dir, item)
        if artifact:
            fm = read_frontmatter(artifact)
            artifact_id = fm.get("artifact_id")
            if artifact_id:
                artifacts[artifact_id] = artifact
            if fm.get("status") == "confirmed":
                reviewer = fm.get("reviewer", "")
                normalized = reviewer.lower()
                if (not reviewer or reviewer in {"待确认", "待评审", "AI"}
                        or "simulat" in normalized or "模拟" in reviewer):
                    issues.append({"severity": "CRITICAL", "file": str(artifact.relative_to(req_dir)), "message": "confirmed artifact has no valid human reviewer"})
                expected = str(artifact.relative_to(req_dir))
                matching_records = [record for record in review_records if expected in record.read_text(encoding="utf-8")]
                if not matching_records:
                    issues.append({"severity": "CRITICAL", "file": expected, "message": "confirmed artifact has no matching ReviewRecord"})
                else:
                    current_hash = artifact_content_hash(artifact.read_text(encoding="utf-8"))
                    newest = matching_records[-1].read_text(encoding="utf-8")
                    recorded_hash = re.search(r"artifact_content_sha256:\s*([0-9a-f]{64})", newest)
                    if recorded_hash and recorded_hash.group(1) != current_hash:
                        issues.append({"severity": "CRITICAL", "file": expected, "message": "confirmed artifact content differs from its ReviewRecord hash"})

    for record in review_records:
        text = record.read_text(encoding="utf-8")
        for required in ["work_item:", "decision:", "reviewer:", "reviewed_at:"]:
            if required not in text:
                issues.append({"severity": "HIGH", "file": str(record.relative_to(req_dir)), "message": f"review record missing {required}"})

    for record in list(req_dir.glob("**/*change*.md")) + list(req_dir.glob("**/*reflow*.md")):
        text = record.read_text(encoding="utf-8")
        if not re.search(r"downstream|下游|影响", text, re.IGNORECASE):
            issues.append({"severity": "HIGH", "file": str(record.relative_to(req_dir)), "message": "change/reflow record missing downstream impact"})

    blocking = [issue for issue in issues if issue["severity"] in {"CRITICAL", "HIGH"}]
    return {"ok": not blocking, "issues": issues}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("req_dir", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--branch", help="Deprecated and ignored")
    args = parser.parse_args()
    if not args.req_dir.is_dir():
        print(f"ERROR: {args.req_dir} is not a directory", file=sys.stderr)
        return 1
    result = validate_records(args.req_dir)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Shared record validation: {'PASS' if result['ok'] else 'FAIL'}")
        for issue in result["issues"]:
            print(f"  [{issue['severity']}] {issue['file']}: {issue['message']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
