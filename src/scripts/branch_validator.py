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

import hash_anchor


def _reviewed_at(record: Path) -> str:
    """Return the reviewed_at timestamp of a review record ('' if missing)."""
    m = re.search(r"(?m)^\s*-\s*reviewed_at:\s*(.+)$", record.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else ""


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
                    # B7 fix: glob order is not guaranteed to be time-sorted; the
                    # newest record must be selected by reviewed_at, not [-1].
                    matching_records.sort(key=lambda r: _reviewed_at(r))
                    current_hash = artifact_content_hash(artifact.read_text(encoding="utf-8"))
                    newest = matching_records[-1].read_text(encoding="utf-8")
                    recorded_hash = re.search(r"artifact_content_sha256:\s*([0-9a-f]{64})", newest)
                    if recorded_hash and recorded_hash.group(1) != current_hash:
                        issues.append({"severity": "CRITICAL", "file": expected, "message": "confirmed artifact content differs from its ReviewRecord hash"})
                    # B13 fix: external anchor check. The chain hash on its own
                    # is closed-loop (artifact + ReviewRecord can be swapped in
                    # lockstep). The .hash-anchor.jsonl file under 99-review
                    # provides an external append-only anchor; if BOTH the
                    # artifact and the ReviewRecord were rewritten together
                    # AND the anchor was rewritten too, the anchor's internal
                    # hash chain breaks (or the row goes missing entirely).
                    anchor_chain = hash_anchor.verify_anchor_chain(req_dir)
                    if not anchor_chain["ok"]:
                        for chain_issue in anchor_chain["issues"]:
                            issues.append({"severity": "CRITICAL", "file": expected, "message": chain_issue})
                        continue
                    if anchor_chain["missing"]:
                        # Backward-compat: legacy requirements never recorded
                        # anchors — skip the per-artifact check rather than
                        # regress all 8 existing cases.
                        continue
                    anchor_check = hash_anchor.verify_artifact_anchored(
                        req_dir, expected, current_hash, reviewer,
                    )
                    if anchor_check["missing_anchor"]:
                        issues.append({"severity": "CRITICAL", "file": expected,
                                       "message": "confirmed artifact not anchored to .hash-anchor.jsonl"})
                    else:
                        # report every mismatched row's individual problems
                        for mismatch in anchor_check["mismatches"]:
                            if not mismatch["sha256_match"]:
                                issues.append({"severity": "CRITICAL", "file": expected,
                                               "message": "anchor sha256 mismatch"})
                            if not mismatch["reviewer_match"]:
                                issues.append({"severity": "CRITICAL", "file": expected,
                                               "message": "anchor reviewer mismatch with ReviewRecord"})

    for record in review_records:
        text = record.read_text(encoding="utf-8")
        for required in ["work_item:", "decision:", "reviewer:", "reviewed_at:"]:
            if required not in text:
                issues.append({"severity": "HIGH", "file": str(record.relative_to(req_dir)), "message": f"review record missing {required}"})
        # B13 fix: immutable self-fingerprint of the ReviewRecord. record_sha256
        # covers the whole record body except the record_sha256 line itself, so
        # editing any field (e.g. artifact_content_sha256 to match a rewritten
        # artifact) breaks the fingerprint even when the artifact + record hash
        # pair is kept internally consistent.
        has_created = bool(re.search(r"(?m)^\s*-\s*record_created_at:", text))
        has_sha = bool(re.search(r"(?m)^\s*-\s*record_sha256:", text))
        if not has_created or not has_sha:
            # Backward-compat: legacy ReviewRecords predate the immutable-anchor
            # fields. Missing fields are a non-blocking HIGH notice (blocking=False),
            # so already-confirmed cases never FAIL merely for lacking the new
            # fields; only a present-but-mismatched record_sha256 is CRITICAL.
            missing = [name for name, present in (("record_created_at", has_created), ("record_sha256", has_sha)) if not present]
            issues.append({"severity": "HIGH", "blocking": False,
                           "file": str(record.relative_to(req_dir)),
                           "message": f"review record missing immutable anchor ({' / '.join(missing)})"})
        if has_sha:
            declared = re.search(r"(?m)^\s*-\s*record_sha256:\s*(\S+)\s*$", text)
            computed = hash_anchor.record_body_sha256(text)
            if not declared or declared.group(1) != computed:
                issues.append({"severity": "CRITICAL", "file": str(record.relative_to(req_dir)),
                               "message": "review record content differs from its record_sha256"})

    for record in list(req_dir.glob("**/*change*.md")) + list(req_dir.glob("**/*reflow*.md")):
        text = record.read_text(encoding="utf-8")
        if not re.search(r"downstream|下游|影响", text, re.IGNORECASE):
            issues.append({"severity": "HIGH", "file": str(record.relative_to(req_dir)), "message": "change/reflow record missing downstream impact"})

    blocking = [issue for issue in issues
                if issue["severity"] in {"CRITICAL", "HIGH"} and issue.get("blocking", True)]
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
