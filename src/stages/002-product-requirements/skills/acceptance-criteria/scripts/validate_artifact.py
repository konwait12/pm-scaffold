#!/usr/bin/env python3
"""Validate the acceptance-criteria.md artifact.

This work_item is an independent work_item producing a standalone acceptance-criteria.md
artifact. The validator checks the full file content for:
  1. AC-XXX acceptance criteria identifiers present
  2. Given/When/Then format for each AC
  3. Quantified thresholds
  4. G-X goal traceability
  5. Frontmatter and status consistency

Run: python3 validate_artifact.py [<acceptance-criteria.md>] [--json]
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
ARTIFACT_NAME = "acceptance-criteria.md"
ARTIFACT_GLOBS = [
    "requirements/*/002-product-requirements/09-acceptance-criteria/acceptance-criteria.md",
]
AC_ID_RE = re.compile(r"AC-\d+")
G_ID_RE = re.compile(r"\bG-\d+\b")
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

SKILL_ID = "acceptance_criteria"
CHECK_PREFIX = "ac"


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


def _given_when_then_format(text: str) -> dict[str, int]:
    """Count Given/When/Then occurrences to check format compliance."""
    given = len(re.findall(r"\bGiven\b", text, re.IGNORECASE))
    when = len(re.findall(r"\bWhen\b", text, re.IGNORECASE))
    then = len(re.findall(r"\bThen\b", text, re.IGNORECASE))
    return {"Given": given, "When": when, "Then": then}


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
        elif "AC-" in e and ("missing" in e.lower() or "not found" in e.lower()):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_ac_ids", "CRITICAL",
                f"'{ARTIFACT_NAME}' 必须包含至少一个 AC-XXX 验收标准标识符",
                "未找到任何 AC-XXX 标识符",
                "为每条验收标准补充形如 AC-001 的稳定标识符",
            )
        elif "Given" in e or "When" in e or "Then" in e:
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_gwt_format", "CRITICAL",
                "每条 AC-XXX 必须包含 Given/When/Then 格式",
                "验收标准缺少 Given/When/Then 格式",
                "将每条 AC 改写为 Given... When... Then... 格式",
            )
        elif "threshold" in e.lower() or "量化" in e:
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_quantified_threshold", "HIGH",
                "每条 AC-XXX 必须包含量化阈值（可核验的指标）",
                "验收标准缺少量化阈值",
                "为每条 AC 补充量化阈值（数字/百分比/时间等可测量指标）",
            )
        elif "G-" in e or "goal" in e.lower():
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_goal_trace", "HIGH",
                "每条 AC-XXX 应追溯到对应的 G-X 目标",
                "验收标准缺少 G-X 目标追溯",
                "在每条 AC 上引用对应的 G-X 目标引用",
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
        elif "G-" in w or "goal" in w.lower():
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_goal_ref",
                "验收标准应追溯到 G-X 目标",
                "未发现 G-X 目标引用",
                "在 AC 中引用对应的 G-X 目标",
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

    # AC identifiers must exist
    ac_ids = sorted(set(AC_ID_RE.findall(text)))
    if not ac_ids:
        errors.append(f"No AC-XXX identifiers found in {ARTIFACT_NAME}")

    # Given/When/Then format check
    gwt = _given_when_then_format(text)
    if ac_ids:
        if not (gwt["Given"] >= 1 and gwt["When"] >= 1 and gwt["Then"] >= 1):
            errors.append(
                f"AC entries missing Given/When/Then format. "
                f"Found Given={gwt['Given']}, When={gwt['When']}, Then={gwt['Then']}. "
                "Each AC-XXX must be written in Given... When... Then... format."
            )

    # Quantified thresholds (must have numbers or measurable units)
    has_threshold = bool(re.search(
        r"[0-9０-９]|%|％|¥|元|万|天|日|周|月|季|年|pp|m?s|ms|次|个|人",
        text
    ))
    if ac_ids and not has_threshold:
        warnings.append(
            f"No quantified thresholds found in {ARTIFACT_NAME}. "
            "Each AC-XXX should include a measurable threshold (number/percent/time/etc.)."
        )

    # G-X goal traceability - warning
    g_ids = sorted(set(G_ID_RE.findall(text)))
    if ac_ids and not g_ids:
        warnings.append(
            f"No G-X goal traceability found in {ARTIFACT_NAME}. "
            "Each AC-XXX should reference a G-X goal from Stage 1."
        )

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
