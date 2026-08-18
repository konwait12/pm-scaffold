#!/usr/bin/env python3
"""Validate the validation-rules.md artifact.

This work_item is an independent work_item producing a standalone validation-rules.md
artifact. The validator checks the full file content for:
  1. VL-XXX rule identifiers present
  2. Field definitions (field name, type, description)
  3. Error messages present
  4. Reference to nfr-catalog.md
  5. Frontmatter and status consistency

Run: python3 validate_artifact.py [<validation-rules.md>] [--json]
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
ARTIFACT_NAME = "validation-rules.md"
ARTIFACT_GLOBS = [
    "requirements/*/002-product-requirements/06-validation-rules/validation-rules.md",
]
VL_ID_RE = re.compile(r"VL-\d+")
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

SKILL_ID = "validation_rules"
CHECK_PREFIX = "vl"


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
                f"{rid} lacks a source trace on its row; each check should "
                "reference an upstream BR-XXX / FEA-XXX / field."
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


def _field_definition_table_warnings(text: str) -> list:
    """Optional check for the 字段定义表 section (legacy 字段规则说明).

    Warning-level only — never produces errors. If the section is absent,
    no check runs, so existing fixtures are unaffected.
    """
    warnings = []
    field_table_heading_re = re.compile(r"^#{1,4}\s*字段定义表\s*$", re.MULTILINE)
    field_id_re = re.compile(r"\bF-\d+\b")
    field_source_re = re.compile(r"\b(?:IX|FUN|FEA)-\d+\b")

    m = field_table_heading_re.search(text)
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
        fid = field_id_re.search(row)
        if fid and not field_source_re.search(row):
            warnings.append(
                f"字段定义表: 字段 {fid.group(0)} 缺少来源引用（上游 IX-XXX / FUN-XXX / FEA-XXX）"
            )
    return warnings


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
        elif "VL-" in e and ("missing" in e.lower() or "not found" in e.lower()):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_vl_ids", "CRITICAL",
                f"'{ARTIFACT_NAME}' 必须包含至少一个 VL-XXX 校验规则标识符",
                "未找到任何 VL-XXX 标识符",
                "为每条校验规则补充形如 VL-001 的稳定标识符",
            )
        elif "field" in e.lower() and ("missing" in e.lower() or "not found" in e.lower()):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_field_def", "HIGH",
                "每条 VL-XXX 规则必须包含字段定义",
                "校验规则缺少字段定义",
                "在规则中明确定义字段名、类型、格式",
            )
        elif "error message" in e.lower() or "错误消息" in e:
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_error_message", "HIGH",
                "每条 VL-XXX 规则必须包含用户可见错误提示",
                "校验规则缺少错误消息",
                "为每条规则补充用户可见的错误提示文字",
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
        elif w.startswith("字段定义表:"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.field_table_issue",
                "字段定义表应包含完整字段定义和来源追溯",
                "字段定义表存在问题",
                "检查并修复字段定义表",
            )
        elif "nfr-catalog" in w.lower():
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_nfr_ref",
                "校验规则应遵循 nfr-catalog.md 指南",
                "未发现 nfr-catalog.md 引用",
                "在规则撰写时引用 nfr-catalog.md 指南",
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

    # VL identifiers must exist
    vl_ids = sorted(set(VL_ID_RE.findall(text)))
    if not vl_ids:
        errors.append(f"No VL-XXX identifiers found in {ARTIFACT_NAME}")

    # Field definitions must be present (field name/type markers)
    field_markers = ["字段", "field", "类型", "type", "格式", "format", "范围", "range"]
    has_fields = any(marker in text for marker in field_markers)
    if not has_fields and vl_ids:
        warnings.append(
            f"No explicit field definitions found in {ARTIFACT_NAME}. "
            "Each VL-XXX rule should define the field, type, and valid range."
        )

    # Error messages must be present
    error_markers = ["错误", "error", "message", "提示", "提示信息", "invalid"]
    has_error_msg = any(marker in text for marker in error_markers)
    if not has_error_msg and vl_ids:
        warnings.append(
            f"No error messages found in {ARTIFACT_NAME}. "
            "Each VL-XXX rule should include a user-visible error message."
        )

    # 逐行内容 / FUN 挂接 / 来源（C3 收紧）
    line_errors, line_warnings = _c3_line_checks(text, VL_ID_RE, "validation check")
    errors.extend(line_errors)
    warnings.extend(line_warnings)

    # nfr-catalog reference - warning
    if "nfr-catalog" not in text.lower():
        warnings.append(
            f"No nfr-catalog.md reference found in {ARTIFACT_NAME}. "
            "Validation rules should follow nfr-catalog.md guidelines."
        )

    # Knowledge-state tags
    if not any(tag in text for tag in ("FACT", "DECISION", "AI_INFERENCE", "UNKNOWN")):
        warnings.append(
            f"No knowledge-state tags (FACT/DECISION/AI_INFERENCE/UNKNOWN) found in {ARTIFACT_NAME}"
        )

    # Optional: 字段定义表 (legacy) — warning-level, non-blocking.
    warnings.extend(_field_definition_table_warnings(text))

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
