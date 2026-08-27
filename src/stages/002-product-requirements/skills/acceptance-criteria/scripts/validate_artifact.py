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
from product_quality import validate_quality_record
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

# ── 模糊词 / 无阈值扫描（C 档移植：work buddy requirements-gathering 的 validateRequirements 思路）───
# 扫描 AC 表行（形如 "| AC-001 | ..."）中的空泛词，以及写了 Given/When/Then 却无量化阈值的行。
# 仅产生 MEDIUM advisory（blocking=False），不阻断现有 gate。
VAGUE_AC_WORDS = (
    "快速", "迅速", "流畅", "顺畅", "合理", "正常", "正常工作",
    "提升体验", "提升用户体验", "优化体验", "改善体验",
    "友好", "用户友好", "易用", "高效", "效率高",
    "容易", "简单易用", "便捷", "稳定", "美观", "及时",
)
AC_ROW_RE = re.compile(r"^\s*\|?\s*AC-\d+\s*\|")
# 行级"量化信号"：数字 / 百分号 / 时间或金额单位。故意排除 "个/人/次" 等会随中文出现的宽泛字，
# 避免把含"用户/个"的正常 AC 行误判为无阈值。
ROW_THRESHOLD_RE = re.compile(
    r"[0-9０-９]|%|％|秒|分钟|小时|天|日|周|月|季|年|ms|元|万|倍|pp"
)
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


def _iter_ac_rows(text: str):
    """Yield (line_no, row) for each AC table row like '| AC-001 | ...'."""
    for line_no, line in enumerate(text.splitlines(), start=1):
        if AC_ROW_RE.match(line.strip()):
            yield line_no, line


def _has_gwt_in_row(row: str) -> bool:
    return bool(re.search(r"\b(given|when|then)\b", row, re.IGNORECASE))


def _has_quantified_token(row: str) -> bool:
    # 先剔除 ID 类引用（AC-/G-/FUN-/FEA-/ST-/BR-/EX-/VL- 等含数字的编号）与优先级值（P0/P1/P2），
    # 避免把"编号/优先级里的数字"误当作量化阈值（例如仅剩 G-001 / P0 的行不算有阈值）。
    cleaned = re.sub(
        r"\b(?:AC|G|FUN|FEA|ST|BR|EX|VL|STATE)-\d+(?:-\d+)?\b|\bP[0-9]\b", " ", row
    )
    return bool(ROW_THRESHOLD_RE.search(cleaned))


def _row_preview(row: str, limit: int = 80) -> str:
    return row.strip().strip("|").strip()[:limit]


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
        elif w.startswith("Vague language"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.vague_language",
                "AC 验收标准应使用可量化、可测量的表述，避免空泛形容词（快速/流畅/合理/正常/友好/高效 等）",
                "AC 行出现空泛词",
                "将空泛词替换为可量化指标（如 P99 ≤ 3s / 覆盖率 ≥ 99% / 30 天内）",
            )
        elif w.startswith("AC row without quantified threshold"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.no_quantified_threshold",
                "每条 AC 应有可核验的量化阈值（数字/百分比/时间单位等）",
                "该 AC 行未发现任何量化阈值",
                "为该 AC 补充量化阈值（如 ≤ 500ms / ≥ 95% / 30 天内）",
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

    # 模糊词 / 无量化阈值扫描（C 档移植 · advisory 非阻断）
    # 只扫 AC 表行；命中输出 MEDIUM warning，不影响 ok / gate 结果。
    for line_no, row in _iter_ac_rows(text):
        for word in VAGUE_AC_WORDS:
            if word in row:
                warnings.append(
                    f"Vague language in AC row (line {line_no}): '{word}' in: "
                    f"{_row_preview(row)}"
                )
        if _has_gwt_in_row(row) and not _has_quantified_token(row):
            warnings.append(
                f"AC row without quantified threshold (line {line_no}): "
                f"{_row_preview(row)}"
            )

    quality_errors, quality_warnings = validate_quality_record(
        text, required=(meta.get("quality_contract_version") == "1" and status in {"ready_for_human_review", "confirmed"})
    )
    errors.extend(quality_errors)
    warnings.extend(quality_warnings)
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
