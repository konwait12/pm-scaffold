#!/usr/bin/env python3
"""Validate the interaction-rules.md artifact.

This work_item is an independent work_item producing a standalone interaction-rules.md
artifact. The validator checks the full file content for:
  1. IX-XXX rule identifiers present
  2. Five interaction states covered (loading/empty/error/disabled/timeout)
  3. Page/FEA traceability
  4. Frontmatter and status consistency

Run: python3 validate_artifact.py [<interaction-rules.md>] [--json]
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
ARTIFACT_NAME = "interaction-rules.md"
ARTIFACT_GLOBS = [
    "requirements/*/002-product-requirements/04-interaction-rules/interaction-rules.md",
]
IX_ID_RE = re.compile(r"IX-\d+")
FEA_ID_RE = re.compile(r"FEA-\d+")
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

SKILL_ID = "interaction_rules"
CHECK_PREFIX = "ix"


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


def _five_states_coverage(text: str) -> dict[str, bool]:
    """Check if five interaction states are covered."""
    state_markers = {
        "loading": bool(re.search(r"loading|加载|加载中|加载状态", text, re.IGNORECASE)),
        "empty": bool(re.search(r"empty|空状态|空|无数据", text, re.IGNORECASE)),
        "error": bool(re.search(r"error|错误|异常|失败", text, re.IGNORECASE)),
        "disabled": bool(re.search(r"disabled|禁用|不可点击|不可操作", text, re.IGNORECASE)),
        "timeout": bool(re.search(r"timeout|超时|连接超时|请求超时", text, re.IGNORECASE)),
    }
    return state_markers


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
        elif "IX-" in e and ("missing" in e.lower() or "not found" in e.lower()):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_ix_ids", "CRITICAL",
                f"'{ARTIFACT_NAME}' 必须包含至少一个 IX-XXX 交互规则标识符",
                "未找到任何 IX-XXX 标识符",
                "为每条交互规则补充形如 IX-001 的稳定标识符",
            )
        elif "5" in e and ("state" in e.lower() or "状态" in e):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_five_states", "CRITICAL",
                "交互规则必须覆盖 5 种状态（loading/empty/error/disabled/timeout）",
                "缺少完整的状态覆盖",
                "补充缺少的交互状态规则（loading/empty/error/disabled/timeout）",
            )
        elif "page" in e.lower() or "FEA" in e:
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_page_fea_trace", "HIGH",
                "每条交互规则应追溯到对应的页面/FEA-XXX",
                "交互规则缺少页面或 FEA 追溯",
                "在规则中引用对应的页面或 FEA-XXX 功能标识符",
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
        elif w.startswith("Missing state:"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.incomplete_state_coverage",
                "交互规则应覆盖 5 种状态（loading/empty/error/disabled/timeout）",
                "状态覆盖不完整",
                "补充缺少的交互状态规则",
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

    # IX identifiers must exist
    ix_ids = sorted(set(IX_ID_RE.findall(text)))
    if not ix_ids:
        errors.append(f"No IX-XXX identifiers found in {ARTIFACT_NAME}")

    # Five interaction states coverage
    states = _five_states_coverage(text)
    missing_states = [s for s, found in states.items() if not found]
    if missing_states:
        warnings.append(
            f"Interaction states not fully covered in {ARTIFACT_NAME}: "
            f"missing {', '.join(missing_states)}. "
            "Each IX-XXX rule should cover loading/empty/error/disabled/timeout states."
        )

    # Page/FEA traceability - warning only
    fea_ids = sorted(set(FEA_ID_RE.findall(text)))
    if not fea_ids and ix_ids:
        warnings.append(f"No FEA-XXX traceability found in {ARTIFACT_NAME}")

    # Knowledge-state tags
    if not any(tag in text for tag in ("FACT", "DECISION", "AI_INFERENCE", "UNKNOWN")):
        warnings.append(
            f"No knowledge-state tags (FACT/DECISION/AI_INFERENCE/UNKNOWN) found in {ARTIFACT_NAME}"
        )

    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "issues": _make_issues(errors, warnings, path)}


def resolve_artifact(path_arg: str | None) -> Path | None:
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
