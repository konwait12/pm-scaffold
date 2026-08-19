#!/usr/bin/env python3
"""Validate the feature-list.md artifact.

This work_item is an independent work_item producing a standalone feature-list.md
artifact. The validator checks the full file content for:
  1. FEA-XXX identifiers present
  2. Each FEA traces to at least one ST-XXX story
  3. Priority markers (P0/P1/P2) present
  4. Frontmatter and status consistency

Two run modes:
  * explicit:  python3 validate_artifact.py <artifact.md> [--json]
  * default:   (no path) auto-resolve feature-list.md under
               requirements/*/002-product-requirements/01-feature-list/

Run: python3 validate_artifact.py [<feature-list.md>] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ── 统一错误格式引导（借鉴点四: make_issue 契约）───────────
def _bootstrap_scripts() -> None:
    import sys as _sys
    p = Path(__file__).resolve().parent
    while p.parent != p:
        cand = p / "src" / "scripts"
        if (cand / "validation_errors.py").is_file():
            if str(cand) not in _sys.path:
                _sys.path.insert(0, str(cand))
            return
        p = p.parent

_bootstrap_scripts()
from validation_errors import make_issue
# ─────────────────────────────────────────────────────────

# ── Per-work-item configuration ──────────────────────────
ARTIFACT_NAME = "feature-list.md"
ARTIFACT_GLOBS = [
    "requirements/*/002-product-requirements/01-feature-list/feature-list.md",
]
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
# ─────────────────────────────────────────────────────────

SKILL_ID = "feature_list"
CHECK_PREFIX = "fl"


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


def _orphan_fea_rows(text: str) -> list[str]:
    """FEA table rows inside the 功能清单 table that carry no ST-XXX traceability.

    Only rows within the feature-list table (header `| ID | 功能名称 | ... 所属故事 ST ...`)
    are scanned. Cross-references to FEA-XXX elsewhere — unknowns (§4), questions (§5),
    clarification sessions, source tables (§6) — must NOT be flagged as orphan features;
    a full-file scan would raise false positives on any row mentioning FEA-XXX.
    """
    orphans: list[str] = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "| ID | 功能名称" in line and "所属故事 ST" in line:
            for body in lines[i + 1:]:
                b = body.strip()
                if not b.startswith("|"):
                    break  # table ended (next heading / blank line)
                if "---" in b:
                    continue
                if FEA_ID_RE.search(b) and not ST_ID_RE.search(b):
                    ids = sorted(set(FEA_ID_RE.findall(b)))
                    orphans.append(f"{'/'.join(ids)} (row: {b[:80]}…)")
    return orphans


def _make_issues(errors: list[str], warnings: list[str], path: Path) -> list[dict]:
    """双轨制: errors/warnings 保持字符串列表, issues 为 make_issue 标准 dict."""
    issues: list[dict] = []
    for e in errors:
        if e.startswith("File not found"):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.file_not_found", "CRITICAL",
                "产物文件必须存在且可读", f"文件不存在: {e}",
                "确认产物路径正确, 或先创建对应的 artifact 文件",
            )
        elif e.startswith("status 'confirmed' is not allowed"):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.status_confirmed", "CRITICAL",
                "子 skill 输出永远不允许 status=confirmed",
                f"实际状态: {e}",
                "将状态改为 draft / ready_for_human_review 等, 由 pipeline.py review --decision approve 负责置为 confirmed",
            )
        elif e.startswith("Invalid status"):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.status_invalid", "CRITICAL",
                "frontmatter status 必须在白名单内（且不含 confirmed）",
                f"非法状态: {e}",
                "修正 frontmatter 的 status 字段为合法取值",
            )
        elif e.startswith("No FEA-"):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_fea_ids", "CRITICAL",
                f"'{ARTIFACT_NAME}' 内必须包含至少一个 FEA-XXX 功能标识符（占位符不算）",
                f"未找到任何 FEA-XXX 标识符",
                "为功能行补充形如 FEA-001 的稳定标识符",
            )
        elif e.startswith("FEA row(s) without ST-"):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.orphan_fea", "CRITICAL",
                "每个 FEA 表格行必须追溯至少一个 ST-XXX 故事",
                f"存在孤立 FEA 行: {e}",
                "为孤立功能行补充所属故事 ST-XXX 引用",
            )
        elif e.startswith("No ST-"):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_st_ids", "CRITICAL",
                "存在 FEA 行时必须引用至少一个 ST-XXX 故事",
                f"未找到任何 ST-XXX 标识符",
                "在章节中补充故事来源 ST-XXX 引用",
            )
        else:
            cid, sev, exp, act, fix = f"{CHECK_PREFIX}.error", "CRITICAL", None, None, None
        issues.append(make_issue(
            severity=sev, check_id=cid, family=SKILL_ID,
            location=str(path), message=e,
            expected=exp, actual=act, repair_hint=fix,
        ))
    for w in warnings:
        if w.startswith("No frontmatter"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_frontmatter",
                "产物应带 YAML frontmatter 以便校验状态",
                "未发现 frontmatter",
                "在产物头部补充 YAML frontmatter（含 status 字段）",
            )
        elif w.startswith("No P0/P1/P2"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_priority",
                f"'{ARTIFACT_NAME}' 内应包含 P0/P1/P2 优先级标记",
                "未发现任何优先级标记",
                "为功能行补充 P0/P1/P2 优先级标记",
            )
        elif w.startswith("No knowledge-state tags"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_ks_tags",
                "可追溯内容应带有知识状态标签 (FACT/DECISION/AI_INFERENCE/UNKNOWN)",
                f"{ARTIFACT_NAME} 未发现任何知识状态标签",
                "在事实/决定/推断内容旁标注 FACT / DECISION / AI_INFERENCE / UNKNOWN",
            )
        elif w.startswith("status is ready_for_human_review but no FEA"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.review_without_fea",
                "ready_for_human_review 状态要求已有 FEA 标识符",
                "状态就绪但无 FEA 标识符",
                "补充功能清单内容及 FEA-XXX 标识符后再提交评审",
            )
        else:
            cid, exp, act, fix = f"{CHECK_PREFIX}.warning", None, None, None
        issues.append(make_issue(
            severity="MEDIUM", check_id=cid, family=SKILL_ID,
            location=str(path), message=w,
            expected=exp, actual=act, repair_hint=fix, blocking=False,
        ))
    return issues


def validate(path: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": [],
                "issues": _make_issues([f"File not found: {path}"], [], path)}

    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    status = meta.get("status")

    if not meta:
        warnings.append("No frontmatter found; artifact status cannot be verified")
    elif status == "confirmed":
        errors.append(
            "status 'confirmed' is not allowed for this work_item output; "
            "only pipeline.py review --decision approve may set confirmed"
        )
    elif status and status not in VALID_STATUSES:
        errors.append(
            f"Invalid status '{status}'. Valid (excluding confirmed): "
            f"{', '.join(sorted(VALID_STATUSES))}"
        )

    # FEA identifiers must exist in the whole file (FEA-XXX placeholder does not count).
    fea_ids = sorted(set(FEA_ID_RE.findall(text)))
    if not fea_ids:
        errors.append(f"No FEA-XXX feature identifiers found in {ARTIFACT_NAME}")

    # Every FEA table row must trace to ≥1 ST-XXX.
    orphans = _orphan_fea_rows(text)
    if orphans:
        errors.append("FEA row(s) without ST-XXX story traceability: " + "; ".join(orphans))

    # Reverse sanity: if FEA rows exist, must reference some ST-XXX.
    st_ids = sorted(set(ST_ID_RE.findall(text)))
    if fea_ids and not st_ids:
        errors.append(f"No ST-XXX identifiers found in {ARTIFACT_NAME}")

    # Priority markers present (P0/P1/P2)?
    if not re.search(r"\bP[012]\b", text):
        warnings.append(f"No P0/P1/P2 priority markers found in {ARTIFACT_NAME}")

    # Knowledge-state tags present for traceable content.
    if not any(tag in text for tag in ("FACT", "DECISION", "AI_INFERENCE", "UNKNOWN")):
        warnings.append(
            f"No knowledge-state tags (FACT/DECISION/AI_INFERENCE/UNKNOWN) found in {ARTIFACT_NAME}"
        )

    if status == "ready_for_human_review" and not fea_ids:
        warnings.append("status is ready_for_human_review but no FEA identifiers found")

    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "issues": _make_issues(errors, warnings, path)}


def resolve_artifact(path_arg: str | None) -> Path | None:
    """Explicit path wins; otherwise auto-resolve the feature-list.md."""
    if path_arg:
        return Path(path_arg)
    root = _project_root()
    for glob in ARTIFACT_GLOBS:
        for hit in sorted(root.glob(glob)):
            return hit
    return None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path, nargs="?", default=None,
                   help=f"Artifact path. Default: auto-resolve {ARTIFACT_NAME}.")
    p.add_argument("--json", action="store_true", dest="j")
    args = p.parse_args()

    path = resolve_artifact(args.artifact)
    if path is None:
        msg = (
            f"No artifact provided and no {ARTIFACT_NAME} found under requirements/*/. "
            f"Run: python3 validate_artifact.py <{ARTIFACT_NAME}> [--json]"
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
