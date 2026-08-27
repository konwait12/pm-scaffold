#!/usr/bin/env python3
"""Validate the functional-flow.md artifact.

This work_item is an independent work_item producing a standalone functional-flow.md
artifact. The validator checks the full file content for:
  1. FEA-XXX and ST-XXX traceability identifiers present
  2. Mermaid flowchart syntax present
  3. Main path, branch paths, and exception paths documented
  4. Frontmatter and status consistency

Two run modes:
  * explicit:  python3 validate_artifact.py <artifact.md> [--json]
  * default:   (no path) auto-resolve functional-flow.md under
               requirements/*/002-product-requirements/02-functional-flow/

Run: python3 validate_artifact.py [<functional-flow.md>] [--json]
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
from product_quality import validate_quality_record
# ─────────────────────────────────────────────────────────

# ── Per-work-item configuration ──────────────────────────
ARTIFACT_NAME = "functional-flow.md"
ARTIFACT_GLOBS = [
    "requirements/*/002-product-requirements/02-functional-flow/functional-flow.md",
]
FEA_ID_RE = re.compile(r"FEA-\d+")
ST_ID_RE = re.compile(r"ST-\d+")
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

SKILL_ID = "functional_flow"
CHECK_PREFIX = "ff"


def _project_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "src" / "framework" / "workflow-registry.json").is_file():
            return parent
    return p.parents[8]


def parse_frontmatter(text: str) -> dict[str, str]:
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


def _make_issues(errors: list[str], warnings: list[str], path: Path) -> list[dict]:
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
        elif "FEA-" in e and ("missing" in e.lower() or "not found" in e.lower()):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_fea_ids", "CRITICAL",
                f"'{ARTIFACT_NAME}' 内必须包含至少一个 FEA-XXX 功能标识符",
                "未找到任何 FEA-XXX 标识符",
                "为每个功能流程补充形如 FEA-001 的稳定标识符",
            )
        elif "ST-" in e and ("missing" in e.lower() or "not found" in e.lower()):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_st_ids", "CRITICAL",
                "存在功能流程时必须引用至少一个 ST-XXX 故事",
                "未找到任何 ST-XXX 标识符",
                "在流程中补充故事来源 ST-XXX 引用",
            )
        elif "Mermaid" in e or "flowchart" in e.lower():
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_mermaid", "CRITICAL",
                "功能流程必须包含 Mermaid 流程图",
                "未发现 Mermaid 语法",
                "为每个功能流程添加 Mermaid flowchart 代码块",
            )
        elif "branch" in e.lower() or "exception" in e.lower():
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_path_types", "CRITICAL",
                "功能流程必须包含主路径、分支路径和异常路径",
                "未发现完整的路径类型",
                "补充主流程、分支流程（decision point）和异常处理路径",
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
        elif w.startswith("No knowledge-state tags"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_ks_tags",
                "可追溯内容应带有知识状态标签 (FACT/DECISION/AI_INFERENCE/UNKNOWN)",
                "全文未发现任何知识状态标签",
                "在事实/决定/推断内容旁标注 FACT / DECISION / AI_INFERENCE / UNKNOWN",
            )
        elif w.startswith("No FEA-"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_fea_in_path",
                "功能流程应追溯到对应的 FEA-XXX 功能",
                "流程节点未发现 FEA-XXX 追溯",
                "在流程节点中引用对应的 FEA-XXX 功能标识符",
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

    # FEA identifiers must exist
    fea_ids = sorted(set(FEA_ID_RE.findall(text)))
    if not fea_ids:
        errors.append(f"No FEA-XXX identifiers found in {ARTIFACT_NAME}")

    # ST identifiers must exist when FEA present
    st_ids = sorted(set(ST_ID_RE.findall(text)))
    if fea_ids and not st_ids:
        errors.append(f"No ST-XXX identifiers found in {ARTIFACT_NAME}")

    # Mermaid flowchart must be present
    has_mermaid = bool(re.search(r"```mermaid", text, re.IGNORECASE))
    if not has_mermaid:
        warnings.append(f"No Mermaid flowchart found in {ARTIFACT_NAME}; add ```mermaid blocks")

    # Path diversity: main path + at least one branch/exception path
    path_type_markers = [
        "主流程", "主路径", "main flow", "main path",
        "分支", "branch", "decision", "条件",
        "异常", "exception", "error", "失败",
    ]
    path_types_found = sum(1 for m in path_type_markers if m.lower() in text.lower())
    if path_types_found < 2:
        warnings.append(
            f"Insufficient path diversity in {ARTIFACT_NAME}: "
            "expected main path + branch/exception paths. "
            "Add branch decision points and exception paths."
        )

    # FEA traceability in paths - warning
    if fea_ids and "FEA-" not in text:
        warnings.append(f"No FEA-XXX traceability found in flow paths")

    # Knowledge-state tags
    if not any(tag in text for tag in ("FACT", "DECISION", "AI_INFERENCE", "UNKNOWN")):
        warnings.append(
            f"No knowledge-state tags (FACT/DECISION/AI_INFERENCE/UNKNOWN) found in {ARTIFACT_NAME}"
        )

    quality_errors, quality_warnings = validate_quality_record(
        text, required=(meta.get("quality_contract_version") == "1" and status in {"ready_for_human_review", "confirmed"})
    )
    errors.extend(quality_errors)
    warnings.extend(quality_warnings)
    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "issues": _make_issues(errors, warnings, path)}


def resolve_artifact(path_arg: str | None) -> Path | None:
    """Explicit path wins; otherwise auto-resolve the functional-flow.md."""
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
