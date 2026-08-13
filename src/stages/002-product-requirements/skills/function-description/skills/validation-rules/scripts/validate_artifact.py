#!/usr/bin/env python3
"""Sub-skill validator template.

Each sub-skill produces a section of the parent artifact. This validator checks
that the section exists in the parent artifact and that the expected ID prefix
is present. Copy to <sub-skill>/scripts/validate_artifact.py and set:
  SECTION_NAME, ID_PATTERN, and the parent artifact glob.

Run: python3 validate_artifact.py <parent-artifact.md> [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ── Per-sub-skill configuration (edit these) ──────────────
SECTION_NAME = "分功能详述"        # e.g. "交互规则"（子 Skill 输出父产物章节）
ID_PATTERN = r"VL-\d+"            # e.g. r"\bIX-\d+\b"
# ─────────────────────────────────────────────────────────


def _norm(h: str) -> str:
    return re.sub(r"^\d+\.\s*", "", h).strip()


# 字段定义表 (field definition table) — merged from the legacy 字段规则说明.
# Optional, warning-level only: triggers only when a 字段定义表 section exists.
FIELD_TABLE_HEADING_RE = re.compile(r"^#{1,4}\s*字段定义表\s*$", re.MULTILINE)
FIELD_ID_RE = re.compile(r"\bF-\d+\b")
FIELD_SOURCE_RE = re.compile(r"\b(?:IX|FUN)-\d+\b")


def _field_definition_table_warnings(text: str) -> list:
    """Optional check for the 字段定义表 section (legacy 字段规则说明).

    Warning-level only — never produces errors. If the section is absent,
    no check runs, so existing fixtures are unaffected.
    """
    warnings = []
    m = FIELD_TABLE_HEADING_RE.search(text)
    if not m:
        return warnings

    # Collect contiguous markdown table lines following the heading.
    table_lines = []
    for line in text[m.end():].splitlines():
        line = line.strip()
        if line.startswith("|"):
            table_lines.append(line)
        elif table_lines:
            break

    if not table_lines:
        warnings.append("字段定义表: 章节存在但未找到表格")
        return warnings

    header = table_lines[0]
    if "字段名" not in header or "类型" not in header:
        warnings.append("字段定义表: 表头缺少「字段名」或「类型」列")

    # Skip the separator row (`|---|`) if present; otherwise all lines are rows.
    rows_start = 2 if len(table_lines) > 1 and "---" in table_lines[1] else 1
    for row in table_lines[rows_start:]:
        fid = FIELD_ID_RE.search(row)
        if fid and not FIELD_SOURCE_RE.search(row):
            warnings.append(
                f"字段定义表: 字段 {fid.group(0)} 缺少来源引用（上游 IX-XXX / FUN-XXX）"
            )
    return warnings


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

    # ID prefix must be present
    ids = re.findall(ID_PATTERN, text)
    if not ids:
        errors.append(f"No {ID_PATTERN} identifiers found in section {SECTION_NAME}")

    # Knowledge state tags present for traceable content
    if not any(tag in text for tag in ("FACT", "DECISION", "AI_INFERENCE", "UNKNOWN")):
        warnings.append("No knowledge-state tags (FACT/DECISION/AI_INFERENCE/UNKNOWN) found")

    # Optional: 字段定义表 (legacy 字段规则说明) — warning-level, non-blocking.
    warnings.extend(_field_definition_table_warnings(text))

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path, nargs="?", default=None,
                   help="Parent artifact path.")
    p.add_argument("--json", action="store_true", dest="j")
    args = p.parse_args()
    if args.artifact is None:
        print("Usage: python3 validate_artifact.py <artifact.md> [--json]", file=sys.stderr)
        sys.exit(2)
    r = validate(args.artifact)
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
