#!/usr/bin/env python3
"""Validate a prd-publish output record.

Includes an optional SHA-256 tamper check: when the publish record sits inside a
requirement directory (ancestor containing 003-prd-output/prd.md and 99-review/),
the current prd.md content is re-hashed and compared against the confirmed
SHA-256 stored in the latest review-prd-assembly-*.md ReviewRecord.
"""

from __future__ import annotations

import argparse, hashlib, json, re, sys
from pathlib import Path

REQUIRED_HEADINGS = ["发布前检查", "发布渠道", "通知"]
PENDING = ("待确认",)
REVIEW_RECORD_GLOB = "review-prd-assembly-*.md"


def _norm(h: str) -> str:
    return re.sub(r"^\d+\.\s*", "", h).strip()


def _artifact_content_hash(text: str) -> str:
    """与 src/scripts/pipeline.py 的 artifact_content_hash 保持同步（拷贝而非 import：
    校验器由 run_tests.sh 以任意 cwd 调用，src.scripts 不在 sys.path 上）。
    归一化规则：frontmatter 中 status/reviewer/reviewed_at/confirmed_at 行替换为占位符后 sha256。"""
    canonical = re.sub(
        r"(?m)^(status|reviewer|reviewed_at|confirmed_at):.*$",
        r"\1: <review-metadata>",
        text,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _find_req_dir(path: Path) -> Path | None:
    """从被校验文件向上找需求目录（同时包含 003-prd-output/prd.md 与 99-review/ 的祖先）。"""
    for parent in path.parents:
        if (parent / "003-prd-output" / "prd.md").is_file() and (parent / "99-review").is_dir():
            return parent
    return None


def _tamper_check(path: Path, errors: list[str], warnings: list[str]) -> None:
    """SHA-256 复核：当前 prd.md 哈希 vs 确认时 ReviewRecord 中的 artifact_content_sha256。

    找不到需求上下文（如独立 fixture）时静默跳过，不产生 error/warning。
    """
    req_dir = _find_req_dir(path)
    if req_dir is None:
        return
    current_hash = _artifact_content_hash(
        (req_dir / "003-prd-output" / "prd.md").read_text(encoding="utf-8")
    )
    records = sorted(
        (req_dir / "99-review").glob(REVIEW_RECORD_GLOB),
        key=lambda p: (p.stat().st_mtime, p.name),
    )
    if not records:
        warnings.append("无 ReviewRecord，跳过 SHA-256 复核")
        return
    m = re.search(r"(?m)^[-*]\s*artifact_content_sha256:\s*([0-9a-fA-F]{64})", records[-1].read_text(encoding="utf-8"))
    if not m:
        warnings.append("ReviewRecord 缺少 artifact_content_sha256，跳过 SHA-256 复核")
        return
    if m.group(1).lower() == current_hash:
        warnings.append("SHA-256 复核通过：prd.md 与确认时一致（Tamper Check）")
    else:
        errors.append("SHA-256 mismatch：产物在确认后被修改")


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
    _tamper_check(path, errors, warnings)
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
