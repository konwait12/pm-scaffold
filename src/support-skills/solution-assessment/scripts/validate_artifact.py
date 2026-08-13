#!/usr/bin/env python3
"""Validate a solution-assessment output (feasibility report or solution comparison)."""

from __future__ import annotations

import argparse, json, re, sys
from pathlib import Path

FEASIBILITY_HEADINGS = ["市场空间", "技术可行性", "投入产出", "风险评估", "结论"]
COMPARISON_HEADINGS = ["候选方案", "方案对比矩阵", "AI 推荐", "人工决策"]
PENDING = ("待确认",)


def _norm(h: str) -> str:
    h = re.sub(r"^\d+\.\s*", "", h).strip()
    h = re.sub(r"^[一二三四五六七八九十]+、\s*", "", h).strip()
    return h


def validate(path: Path) -> dict:
    errors, warnings = [], []
    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}
    text = path.read_text(encoding="utf-8")
    headings = [_norm(m.group(1)) for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]
    targets = FEASIBILITY_HEADINGS if "可行性" in text else COMPARISON_HEADINGS
    for h in targets:
        if _norm(h) not in headings:
            errors.append(f"Missing required heading: {h}")
    if not re.search(r"做|不做|有条件做|推荐方案", text):
        warnings.append("No clear recommendation found; assessment should conclude with 做/不做/有条件做")
    if any(p in text for p in PENDING):
        warnings.append("Assessment still has 待确认 placeholders")
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
