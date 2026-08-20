#!/usr/bin/env python3
"""Validate the exception-handling.md artifact.

This work_item is an independent work_item producing a standalone exception-handling.md
artifact. The validator checks the full file content for:
  1. EX-XXX exception identifiers present
  2. Failure modes documented
  3. Recovery paths with retry/rollback policy
  4. Frontmatter and status consistency

Run: python3 validate_artifact.py [<exception-handling.md>] [--json]
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
ARTIFACT_NAME = "exception-handling.md"
ARTIFACT_GLOBS = [
    "requirements/*/002-product-requirements/08-exception-handling/exception-handling.md",
]
EX_ID_RE = re.compile(r"EX-\d+")
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

SKILL_ID = "exception_handling"
CHECK_PREFIX = "ex"


def _project_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "src" / "framework" / "workflow-registry.json").is_file():
            return parent
    return p.parents[8]


# ── C3 收紧：逐行挂接 / 内容 / 来源（借鉴点三：先逐行、后全文）────
TRACE_ANCHOR_RE = re.compile(r"\b(?:FUN|FEA|ST|BR|VL|EX|IX|STATE|SRC|BG|G)-\d+[A-Z]?\b")
SECTION_TRACE_RE = re.compile(r"^#{1,6}\s*((?:FUN|FEA|ST|BR|VL|EX|IX|STATE|SRC|BG|G)-\d+[A-Z]?)\b")
GLOBAL_SCOPE_RE = re.compile(r"(?:适用范围|scope)\s*[:：]?\s*(?:GLOBAL|全局)\b", re.IGNORECASE)
REF_SOURCE_RE = re.compile(
    r"\b(?:BR|ST|FEA|VL|EX|AC|IX|FD|FUN|SRC|STATE|US|BG|PD|PRD)-\d+\b"
)


def _c3_line_checks(text: str, pid_re: object, kind: str) -> tuple[list[str], list[str]]:
    """逐行检查目标行：必须有真实内容和可解释追溯锚点。
    (3) 存在来源/依据引用。返回 (errors, warnings)。"""
    errors: list[str] = []
    warnings: list[str] = []
    section_anchor: str | None = None
    for line in text.splitlines():
        ls = line.strip()
        mh = SECTION_TRACE_RE.match(ls)
        if mh:
            section_anchor = mh.group(1)
            continue
        if not ls.startswith("|"):
            continue
        cells = [c.strip() for c in ls.strip("|").split("|")]
        if not cells or not cells[0]:
            continue
        first = re.sub(r"[*_`]", "", cells[0])
        idm = pid_re.search(first)
        if not idm or first != idm.group(0):
            continue  # 首列不是目标 ID，跳过（如 恢复/回滚 等引用表）
        rid = idm.group(0)
        # (1) 内容完整性：去除引用标记后仍应留有实质语句
        body = "".join(REF_SOURCE_RE.sub("", c) for c in cells[1:])
        body_clean = body.replace(" ", "").replace("-", "")
        if len(body_clean) < 4:
            errors.append(
                f"{rid} carries no {kind} content: the row only holds the identifier "
                "and reference cells; fill in a real statement."
            )
            continue
        # (2) 追溯锚点：功能级、跨功能或全局条目均可；禁止凭空伪造 FUN
        anchors = [m.group(0) for m in TRACE_ANCHOR_RE.finditer(ls)]
        has_external_anchor = any(anchor != rid for anchor in anchors)
        if not has_external_anchor and section_anchor != rid and not GLOBAL_SCOPE_RE.search(ls):
            errors.append(
                f"{rid} is orphan: no trace anchor or explicit GLOBAL scope "
                "(use FUN/FEA/ST/BR/VL/EX/IX/STATE/SRC/BG/G or scope=GLOBAL)."
            )
            continue
        # (3) 来源追溯（warning）
        if not REF_SOURCE_RE.search(ls):
            warnings.append(
                f"{rid} lacks a source trace on its row; each exception "
                "should reference an upstream BR / ST / function."
            )
    return errors, warnings


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
        elif "EX-" in e and ("missing" in e.lower() or "not found" in e.lower()):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_ex_ids", "CRITICAL",
                f"'{ARTIFACT_NAME}' 必须包含至少一个 EX-XXX 异常标识符",
                "未找到任何 EX-XXX 标识符",
                "为每个异常补充形如 EX-001 的稳定标识符",
            )
        elif "failure mode" in e.lower() or "失败模式" in e:
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_failure_modes", "CRITICAL",
                "每个 EX-XXX 必须包含失败模式描述",
                "异常缺少失败模式描述",
                "为每个异常补充失败模式（failure mode）描述",
            )
        elif "recovery" in e.lower() or "恢复" in e:
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_recovery_path", "HIGH",
                "每个 EX-XXX 必须包含用户可见恢复路径",
                "异常缺少恢复路径",
                "为每个异常补充用户可见的恢复/回滚路径",
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
        elif "retry" in w.lower() or "rollback" in w.lower():
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_retry_rollback",
                "异常应包含 retry/rollback 策略",
                "未发现 retry 或 rollback 策略",
                "补充异常重试/回滚策略",
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

    # EX identifiers must exist
    ex_ids = sorted(set(EX_ID_RE.findall(text)))
    if not ex_ids:
        errors.append(f"No EX-XXX identifiers found in {ARTIFACT_NAME}")

    # Failure modes must be present
    failure_markers = [
        "failure", "fail", "失败", "异常", "error",
        "rejection", "拒绝", "超时", "timeout",
        "dependency", "依赖",
    ]
    has_failure_modes = any(marker.lower() in text.lower() for marker in failure_markers)
    if ex_ids and not has_failure_modes:
        warnings.append(
            f"No explicit failure mode descriptions found in {ARTIFACT_NAME}. "
            "Each EX-XXX should document the failure mode."
        )

    # Recovery path must be present
    recovery_markers = [
        "recovery", "恢复", "回滚", "rollback",
        "retry", "重试", "补偿", "compensate",
        "fallback", "降级",
    ]
    has_recovery = any(marker.lower() in text.lower() for marker in recovery_markers)
    if ex_ids and not has_recovery:
        warnings.append(
            f"No explicit recovery path found in {ARTIFACT_NAME}. "
            "Each EX-XXX should include a user-visible recovery path and retry/rollback policy."
        )

    # 逐行内容 / FUN 挂接 / 来源（C3 收紧）
    line_errors, line_warnings = _c3_line_checks(text, EX_ID_RE, "exception")
    errors.extend(line_errors)
    warnings.extend(line_warnings)

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
