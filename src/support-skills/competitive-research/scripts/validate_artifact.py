#!/usr/bin/env python3
"""Validate a competitive-research output artifact."""

from __future__ import annotations

import argparse, json, re, sys
from pathlib import Path

REQUIRED_HEADINGS = ["竞品列表", "逐品分析", "横向对比", "结论"]
PENDING = ("待确认",)
ANALYSIS_SECTIONS = ["逐品分析", "横向对比"]
SRC_ID_RE = re.compile(r"SRC-\d+")


def _norm(h: str) -> str:
    return re.sub(r"^\d+\.\s*", "", h).strip()


def _section(text: str, heading: str) -> str:
    """Return the section body between this heading and the next '##' heading."""
    m = re.search(rf"^##\s+{heading}\s*$", text, re.MULTILINE)
    if not m:
        return ""
    nxt = re.search(r"^##\s+", text[m.end():], re.MULTILINE)
    end = m.end() + nxt.start() if nxt else len(text)
    return text[m.end():end]


def validate(path: Path) -> dict:
    errors, warnings = [], []
    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}
    text = path.read_text(encoding="utf-8")
    headings = [_norm(m.group(1)) for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]
    for h in REQUIRED_HEADINGS:
        if _norm(h) not in headings:
            errors.append(f"Missing required heading: {h}")
    if "AI_INFERENCE" not in text and "竞品" not in text:
        warnings.append("Competitive findings should be marked AI_INFERENCE until confirmed")
    if any(p in text for p in PENDING):
        warnings.append("Artifact contains 待确认 placeholders")
    # Source Fidelity (SKILL.md Audit): 逐品分析/横向对比 with concrete content
    # (table rows or list entries) must trace every claim to an SRC-ID.
    if not SRC_ID_RE.search(text):
        has_analysis = any(
            re.search(r"^\s*\|", _section(text, h), re.MULTILINE)
            or re.search(r"^\s*[-*+]\s+\S", _section(text, h), re.MULTILINE)
            for h in ANALYSIS_SECTIONS
        )
        if has_analysis:
            warnings.append(
                "No SRC-ID found: 逐品分析/横向对比 claims must cite SRC-xxx "
                "(Source Fidelity)"
            )
    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path)
    p.add_argument("--json", action="store_true", dest="j")
    a = p.parse_args()
    r = validate(a.artifact)
    if a.j:
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
