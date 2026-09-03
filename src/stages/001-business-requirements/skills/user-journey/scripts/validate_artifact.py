#!/usr/bin/env python3
"""Validate a standalone user-journey document and its governance companion."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def _bootstrap_scripts() -> None:
    p = Path(__file__).resolve()
    while p.parent != p:
        candidate = p / "src" / "scripts"
        if (candidate / "validation_errors.py").is_file():
            if str(candidate) not in sys.path:
                sys.path.insert(0, str(candidate))
            return
        p = p.parent


_bootstrap_scripts()
from validation_errors import make_issue


REQUIRED_FIELDS = {
    "artifact_id", "version", "status", "owner", "business_fact_owner",
    "goal_decision_owner", "reviewer", "created_at", "updated_at",
    "confirmed_at", "upstream_artifact_id",
}
REQUIRED_HEADINGS = [
    "预检与摘要", "一句话旅程叙事", "业务生命周期分解", "角色旅程矩阵",
    "路径与情绪", "触点、痛点与机会", "旅程覆盖与边界", "待确认与风险", "参考资料",
]
GOVERNANCE_HEADINGS = ["类型判断与输入充分度", "主张来源与知识状态", "澄清记录", "HTML 审阅板记录", "AI Audit", "PM 确认与变更"]
# ``confirmed`` is recognized only to emit a precise rejection; this skill
# never creates that state. ``simulated`` belongs to other artifact families.
VALID_STATUSES = {"draft", "needs_user_input", "conditional_review", "ready_for_human_review", "confirmed", "superseded"}
FORBIDDEN_MAIN_HEADINGS = {"事实与决定", "假设、AI 推断、未知与冲突", "来源追溯", "Constitution Compliance", "Clarifications", "产品质量增强记录"}
# 项目级会议基线（可选）：不再硬编码特定会议 ID；若治理伴随文件登记了基线段，则校验段内 token 与原文链接。
GOVERNANCE_BASELINE_SECTIONS = ("项目级会议基线（可选）", "001 会议基线读取记录")
BASELINE_REQUIRED_TOKENS = ("读取命令", "四类拆分", "使用位置")


def parse_frontmatter(text: str) -> dict[str, str]:
    text = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.DOTALL)
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip("\"'")
    return values


def headings(text: str) -> list[str]:
    return [re.sub(r"^\d+\.\s*", "", item.strip()) for item in re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]


def section(text: str, title: str) -> str:
    match = re.search(rf"^##\s+{re.escape(title)}\s*$(.*?)(?=^##\s+|\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def issue(severity: str, check_id: str, path: Path, message: str, blocking: bool = True) -> dict[str, object]:
    return make_issue(
        severity=severity,
        check_id=check_id,
        family="user_journey",
        location=str(path),
        message=message,
        expected="符合 user-journey 输出契约",
        actual=message,
        repair_hint="按 user-journey SKILL.md、模板和治理伴随文件修复",
        blocking=blocking,
    )


def validate(path: Path) -> dict[str, object]:
    errors: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []
    if not path.is_file():
        errors.append(issue("CRITICAL", "uj.file_not_found", path, f"File not found: {path}"))
        return {"ok": False, "errors": [x["message"] for x in errors], "warnings": [], "issues": errors}

    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    missing = sorted(REQUIRED_FIELDS - meta.keys())
    if missing:
        errors.append(issue("CRITICAL", "uj.missing_frontmatter", path, f"Missing frontmatter fields: {', '.join(missing)}"))
    status = meta.get("status", "")
    if status == "confirmed":
        errors.append(issue("CRITICAL", "uj.status_confirmed", path, "status 'confirmed' is not allowed; only an authorized human review may confirm it"))
    elif status and status not in VALID_STATUSES:
        errors.append(issue("CRITICAL", "uj.invalid_status", path, f"Invalid status: {status}"))

    document_headings = headings(text)
    missing_headings = [title for title in REQUIRED_HEADINGS if title not in document_headings]
    if missing_headings:
        errors.append(issue("CRITICAL", "uj.missing_headings", path, f"Missing headings: {', '.join(missing_headings)}"))
    forbidden = [title for title in document_headings if title in FORBIDDEN_MAIN_HEADINGS]
    if forbidden or any(marker in text for marker in ("ReviewRecord", "SHA-256", "SRC-001 |")):
        errors.append(issue("CRITICAL", "uj.governance_in_main", path, "Machine governance records must stay in user-journey.governance.md"))

    if not re.search(r"角色|role|persona", text, re.IGNORECASE):
        errors.append(issue("CRITICAL", "uj.role_missing", path, "No role definition found"))
    if not re.search(r"阶段|phase|lifecycle", text, re.IGNORECASE):
        errors.append(issue("CRITICAL", "uj.lifecycle_missing", path, "No lifecycle phase definition found"))
    if not re.search(r"情绪|emotion|痛点|机会|opportunity", text, re.IGNORECASE):
        errors.append(issue("CRITICAL", "uj.emotion_missing", path, "No emotion, pain-point, or opportunity mapping found"))
    path_tokens = re.findall(r"normal|alternative|exception|failure|handoff|recovery|正常|备选|异常|失败|交接|恢复", text, re.IGNORECASE)
    if len(set(token.lower() for token in path_tokens)) < 2:
        errors.append(issue("CRITICAL", "uj.path_diversity_missing", path, "Journey must distinguish a main path and at least one variant or explicitly record its absence"))
    if not re.search(r"(?:SRC|BG)-\d+", text):
        warnings.append(issue("MEDIUM", "uj.source_missing", path, "No upstream/source identifier found", False))
    if not re.search(r"FACT|DECISION|ASSUMPTION|AI_INFERENCE|UNKNOWN|CONFLICT", text):
        warnings.append(issue("MEDIUM", "uj.knowledge_state_missing", path, "No knowledge-state label found", False))

    # 伴随文件定位：默认按 artifact 命名（`<stem>.governance.md`），找不到则回退到规范名（兼容旧用法）
    companion = path.with_name(f"{path.stem}.governance.md")
    if not companion.is_file():
        legacy = path.with_name("user-journey.governance.md")
        if legacy.is_file():
            companion = legacy
    if not companion.is_file():
        severity = "CRITICAL" if status in {"ready_for_human_review", "confirmed"} else "MEDIUM"
        target = errors if severity == "CRITICAL" else warnings
        target.append(issue(severity, "uj.governance_missing", path, f"Companion file not found: {companion.name}", severity == "CRITICAL"))
    else:
        governance_text = companion.read_text(encoding="utf-8")
        gov_meta = parse_frontmatter(governance_text)
        required_gov = {"artifact_id", "main_artifact", "main_version", "main_sha256", "status", "board_artifact"}
        missing_gov = sorted(required_gov - gov_meta.keys())
        if missing_gov:
            errors.append(issue("CRITICAL", "uj.governance_frontmatter_missing", companion, f"Governance companion missing: {', '.join(missing_gov)}"))
        missing_gov_headings = [title for title in GOVERNANCE_HEADINGS if title not in headings(governance_text)]
        if missing_gov_headings:
            errors.append(issue("CRITICAL", "uj.governance_headings_missing", companion, f"Governance companion missing headings: {', '.join(missing_gov_headings)}"))
        if gov_meta.get("artifact_id") and gov_meta["artifact_id"] != meta.get("artifact_id"):
            errors.append(issue("CRITICAL", "uj.artifact_id_mismatch", companion, "Main document and governance companion have different artifact_id values"))
        if gov_meta.get("main_version") and gov_meta["main_version"] != meta.get("version"):
            errors.append(issue("CRITICAL", "uj.version_mismatch", companion, "Main document and governance companion have different versions"))
        actual_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        recorded_hash = gov_meta.get("main_sha256", "")
        if recorded_hash not in {"", "待确认", "待补充"} and recorded_hash != actual_hash:
            errors.append(issue("CRITICAL", "uj.hash_mismatch", companion, "main_sha256 does not match user-journey.md"))
        if status == "confirmed":
            errors.append(issue("CRITICAL", "uj.status_confirmed", path, "user-journey output cannot be confirmed by the skill"))
        if meta.get("artifact_id", "").endswith("-001"):
            # 项目级会议基线（可选）：仅当治理伴随文件登记了基线段才校验；未登记不报错
            meeting_section = ""
            for title in GOVERNANCE_BASELINE_SECTIONS:
                meeting_section = section(governance_text, title)
                if meeting_section:
                    break
            if meeting_section:
                missing_tokens = [t for t in BASELINE_REQUIRED_TOKENS if t not in meeting_section]
                if missing_tokens:
                    errors.append(issue("CRITICAL", "uj.meeting_baseline_incomplete", companion,
                        f"治理伴随文件登记了项目级会议基线，但缺少必要 token：{', '.join(missing_tokens)}"))
                if not re.search(r"https?://|feishu\.cn|lark\.cn|notion\.|confluence\.", meeting_section):
                    warnings.append(issue("MEDIUM", "uj.meeting_baseline_no_link", companion,
                        "项目级会议基线段未发现原文链接，请确认是否需要补充", False))

    return {
        "ok": not errors,
        "errors": [x["message"] for x in errors],
        "warnings": [x["message"] for x in warnings],
        "issues": errors + warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = validate(args.artifact)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else ("PASS" if result["ok"] else "FAIL"))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
