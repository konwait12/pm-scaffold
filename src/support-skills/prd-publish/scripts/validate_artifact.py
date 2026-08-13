#!/usr/bin/env python3
"""Validate a prd-publish output record."""

from __future__ import annotations

import argparse, json, re, sys
from pathlib import Path

REQUIRED_HEADINGS = ["发布前检查", "发布渠道", "通知"]
PENDING = ("待确认",)


def _norm(h: str) -> str:
    return re.sub(r"^\d+\.\s*", "", h).strip()


def validate(path: Path) -> dict:
    errors, warnings = [], []
    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}
    text = path.read_text(encoding="utf-8")
    headings = [_norm(m.group(1)) for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]
    for h in REQUIRED_HEADINGS:
        if _norm(h) not in headings:
            errors.append(f"Missing required heading: {h}")
    if "已发布" not in text and "已生成" not in text:
        warnings.append("Publish record has no confirmed channel; verify release happened")
    if any(p in text for p in PENDING):
        warnings.append("Publish record still has 待确认 placeholders")
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
