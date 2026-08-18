#!/usr/bin/env python3
"""Validate the business-rules.md artifact.

This work_item is an independent work_item producing a standalone business-rules.md
artifact. The validator checks the full file content for:
  1. BR-XXX rule identifiers present
  2. Rule statements (not just placeholder text)
  3. Source traceability to upstream FEA/ST
  4. Reference to ears-syntax.md
  5. Frontmatter and status consistency

Run: python3 validate_artifact.py [<business-rules.md>] [--json]
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
ARTIFACT_NAME = "business-rules.md"
ARTIFACT_GLOBS = [
    "requirements/*/002-product-requirements/05-business-rules/business-rules.md",
]
BR_ID_RE = re.compile(r"BR-\d+")
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

SKILL_ID = "business_rules"
CHECK_PREFIX = "br"


def _project_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "src" / "framework" / "workflow-registry.json").is_file():
            return parent
    return p.parents[8]


# ── C3 收紧：逐行挂接 / 内容 / 来源（借鉴点三：先逐行、后全文）────
FUN_ID_RE = re.compile(r"\bFUN-\d+\b")
SECTION_FUN_RE = re.compile(r"^#{1,6}\s*FUN-\d+\b")
REF_SOURCE_RE = re.compile(
    r"\b(?:BR|ST|FEA|VL|EX|AC|IX|FD|FUN|SRC|STATE|US|BG|PD|PRD)-\d+\b"
)


def _c3_line_checks(text: str, pid_re: object, kind: str) -> tuple[list[str], list[str]]:
    """逐行收紧：以目标 ID 为首列的规则行必须 (1) 带真实内容 (2) 挂接 FUN-XXX
    (3) 引用来源。返回 (errors, warnings)。"""
    errors: list[str] = []
    warnings: list[str] = []
    section_fun: str | None = None
    for line in text.splitlines():
        ls = line.strip()
        mh = SECTION_FUN_RE.match(ls)
        if mh:
            section_fun = FUN_ID_RE.search(ls).group(0)
            continue
        if not ls.startswith("|"):
            continue
        cells = [c.strip() for c in ls.strip("|").split("|")]
        if not cells or not cells[0]:
            continue
        first = re.sub(r"[*_`]", "", cells[0])
        idm = pid_re.search(first)
        if not idm or first != idm.group(0):
            continue  # 首列不是目标 ID，跳过（如 来源追溯 / 冲突对 等引用表）
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
        # (2) FUN 挂接：行内有 FUN-XXX 或正处于 FUN-XXX 区块
        if not FUN_ID_RE.search(ls) and section_fun is None:
            errors.append(
                f"{rid} is orphan: not attached to any FUN-XXX "
                "(no '所属 FUN' cell and not under a '#### FUN-XXX' section)."
            )
            continue
        # (3) 来源追溯（warning，来源可为自由文本）
        if not REF_SOURCE_RE.search(ls):
            warnings.append(
                f"{rid} lacks a source trace on its row; each rule should "
                "reference an upstream ST-XXX / FEA-XXX / source."
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
        elif "BR-" in e and ("missing" in e.lower() or "not found" in e.lower()):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_br_ids", "CRITICAL",
                f"'{ARTIFACT_NAME}' 必须包含至少一个 BR-XXX 业务规则标识符",
                "未找到任何 BR-XXX 标识符",
                "为每条业务规则补充形如 BR-001 的稳定标识符",
            )
        elif "rule statement" in e.lower() or "规则语句" in e:
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_rule_statement", "CRITICAL",
                "每条 BR-XXX 规则必须包含完整规则语句",
                "存在无规则语句的 BR-XXX 占位符",
                "为占位符 BR-XXX 补充完整规则语句",
            )
        elif "source" in e.lower() or "来源" in e:
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_source_trace", "HIGH",
                "每条 BR-XXX 必须追溯到上游 FEA/ST-XXX",
                "业务规则缺少上游来源追溯",
                "在规则中引用对应的 FEA-XXX 或 ST-XXX 上游",
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
        elif "ears" in w.lower():
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_ears_ref",
                "业务规则应遵循 ears-syntax.md 指南",
                "未发现 ears-syntax.md 引用",
                "在规则撰写时引用 ears-syntax.md 指南",
            )
        elif "FEA-" in w or "ST-" in w:
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_upstream_trace",
                "业务规则应追溯到上游 FEA-XXX 或 ST-XXX",
                "未发现上游追溯引用",
                "在规则中引用对应的 FEA-XXX 或 ST-XXX",
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

    # BR identifiers must exist
    br_ids = sorted(set(BR_ID_RE.findall(text)))
    if not br_ids:
        errors.append(f"No BR-XXX identifiers found in {ARTIFACT_NAME}")

    # Rule statements: 逐行内容 / FUN 挂接 / 来源（C3 收紧，替代全文弱检查）
    line_errors, line_warnings = _c3_line_checks(text, BR_ID_RE, "rule")
    errors.extend(line_errors)
    warnings.extend(line_warnings)

    # Source traceability: FEA or ST references
    fea_ids = sorted(set(FEA_ID_RE.findall(text)))
    st_ids = sorted(set(ST_ID_RE.findall(text)))
    if br_ids and not fea_ids and not st_ids:
        warnings.append(
            f"No FEA-XXX or ST-XXX upstream traceability found in {ARTIFACT_NAME}. "
            "Each BR-XXX should trace to a FEA-XXX or ST-XXX."
        )

    # EARS syntax reference - warning
    if "ears-syntax" not in text.lower() and "ears" not in text.lower():
        warnings.append(
            f"No ears-syntax.md reference found in {ARTIFACT_NAME}. "
            "Business rules should follow ears-syntax.md guidelines."
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
