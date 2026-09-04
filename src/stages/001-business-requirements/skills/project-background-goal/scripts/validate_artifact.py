#!/usr/bin/env python3
"""Validate standalone project-background-goal documents."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

REQUIRED_FIELDS = {"artifact_id", "version", "status", "project_type", "owner", "created_at", "updated_at"}
REQUIRED_HEADINGS = ["一句话摘要", "项目背景", "当前现状与已有做法", "核心问题与证据", "目标与成功判断", "角色与干系人", "约束与依赖", "边界与非目标", "待确认与风险", "参考资料"]
GOVERNANCE_HEADINGS = ["类型判断与 PM 选择", "主张来源与知识状态", "澄清记录", "AI Audit", "PM 确认与变更"]
VALID_TYPES = {"重构", "从 0 到 1", "迭代"}
VALID_STATUSES = {"draft", "needs_user_input", "ready_for_human_review", "confirmed", "superseded"}
MACHINE_HEADINGS = {"事实与决定", "假设、AI 推断、未知与冲突", "待确认问题", "来源追溯", "下游输入摘要", "Constitution Compliance", "Clarifications", "产品质量增强记录"}
# 项目级会议基线（可选）：不再硬编码特定会议 ID；若治理伴随文件登记了基线段，则校验段内 token 与原文链接。

def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("\"\'")
    return result

def headings(text: str) -> list[str]:
    return [re.sub(r"^\d+\.\s*", "", item.strip()) for item in re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]

def get_section(text: str, name: str) -> str:
    match = re.search(rf"^##\s+(?:\d+\.\s*)?{re.escape(name)}\s*$(.*?)(?=^##\s+|\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""

def substantive(value: str) -> bool:
    return len(re.sub(r"待确认|待补充|TBD|UNKNOWN|[-*#>|\s]", "", value)) >= 12


def _strip_structural(text: str) -> str:
    """结构化扫描 helper：去除 markdown 列表标记 / 代码块；表格行保留单元格内容。

    W4 第⑤条：所有 in-text 类字符串检测必须走结构化扫描，避免误伤 markdown 表格分隔符
    （`SRC-001 |`）、列表标记、代码块。
    """
    out: list[str] = []
    in_code = False
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if s.startswith("|"):
            # 表格行：去除首尾 | 与单元格分隔符，保留单元格内容
            if re.fullmatch(r"\|[\s\-:|]+\|", s):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            out.append(" ".join(cells))
            continue
        out.append(re.sub(r"^\s*[-*]\s+", "", ln))
    return "\n".join(out)

def finding(severity: str, check_id: str, message: str, blocking: bool = True) -> dict[str, object]:
    return {"severity": severity, "check_id": check_id, "message": message, "blocking": blocking}

def validate(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": [], "issues": []}
    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)
    errors, warnings = [], []
    missing = sorted(REQUIRED_FIELDS - meta.keys())
    if missing:
        errors.append(finding("CRITICAL", "bg.missing_frontmatter", f"Missing frontmatter fields: {', '.join(missing)}"))
    if meta.get("status") and meta["status"] not in VALID_STATUSES:
        errors.append(finding("CRITICAL", "bg.invalid_status", f"Invalid status: {meta['status']}"))
    project_type = meta.get("project_type", "")
    if project_type not in VALID_TYPES and project_type not in {"", "待确认"}:
        errors.append(finding("CRITICAL", "bg.invalid_project_type", f"Invalid project_type: {project_type}"))
    document_headings = headings(text)
    missing_headings = [name for name in REQUIRED_HEADINGS if name not in document_headings]
    if missing_headings:
        errors.append(finding("CRITICAL", "bg.missing_headings", f"Missing headings: {', '.join(missing_headings)}"))
    forbidden = [name for name in document_headings if name in MACHINE_HEADINGS]
    # W4 第⑤条：机器治理标识检测走结构化扫描（避免 markdown 表格分隔符误伤）
    body_for_gov = _strip_structural(text)
    if forbidden or any(marker in body_for_gov for marker in ("ReviewRecord", "SHA-256")):
        errors.append(finding("CRITICAL", "bg.machine_governance_in_main", "Move machine governance records from the main document to its companion file."))
    if not substantive(get_section(text, "参考资料")):
        warnings.append(finding("MEDIUM", "bg.references_missing", "Reference list is empty or still a placeholder.", False))

    # 空骨架红线（防冗杂约定 §1）：占位符密度 advisory
    import re as _re
    placeholder_pattern = r"待确认|待补充|TBD|TODO|UNKNOWN|\[空\]|^\s*-\s*$|^\s*\*\s*$"
    total_lines = max(len([ln for ln in text.splitlines() if ln.strip()]), 1)
    placeholder_lines = len([ln for ln in text.splitlines() if _re.search(placeholder_pattern, ln)])
    density = placeholder_lines / total_lines
    if density > 0.30:
        warnings.append(finding("MEDIUM", "bg.bloat_warning",
            f"占位符密度 {density:.0%}（{placeholder_lines}/{total_lines} 行）超过 30%；产物形式完整但内容可能为空骨架。详见 references/anti-bloat-conventions.md §1",
            blocking=False))

    # 护栏 B4：第一性原理段（advisory，不阻断）
    # 触发：主文档含「## 第一性原理」段时，期望每条追问有实质回答
    # 类型分支：迭代类型仅检查"根本问题 + 不做的代价"两条；其他类型五问全查
    fp_section_match = _re.search(
        r"^##\s+第一性原理\s*$(.*?)(?=^##\s+|\Z)",
        text, _re.MULTILINE | _re.DOTALL,
    )
    if fp_section_match:
        fp_section = fp_section_match.group(1).strip()
        fp_lines = [ln.strip() for ln in fp_section.splitlines() if ln.strip()]
        non_placeholder_fp = [
            ln for ln in fp_lines
            if not _re.search(placeholder_pattern, ln)
            and not ln.startswith("<!--")
            and not ln.startswith(">")
        ]
        # 5 问标识（rough match）
        questions = {
            "根本问题": ["根本问题", "真正要解决"],
            "不做的代价": ["不解决", "不做的代价"],
            "为什么是现在": ["为什么是现在", "时机"],
            "核心假设": ["核心假设", "假设"],
            "解决标志": ["解决标志", "标志"],
        }
        if project_type in {"重构", "从 0 到 1"} or not project_type:
            required_keys = list(questions.keys())
        else:  # 迭代类型：只查两条
            required_keys = ["根本问题", "不做的代价"]
        missing = []
        for key in required_keys:
            hit = any(
                any(m in ln for m in questions[key])
                and not _re.search(r"^[-*]\s*$|^\s*-\s*$|^\s*\*\s*$", ln)
                for ln in non_placeholder_fp
            )
            if not hit:
                missing.append(key)
        # 关键修复：当 whole section 是模板占位描述时，non_placeholder_fp 也会包含模板
        # 因此改用"原始模板占位描述句"判断：若五问每问都没真正回答，归为空壳
        template_filler = (
            "思想层追问" in fp_section
            or "护栏 B4" in fp_section
            or "类型分支写法" in fp_section
        )
        if missing and not template_filler:
            warnings.append(finding("MEDIUM", "bg.first_principles_hollow",
                f"第一性原理段未实质回答以下追问：{', '.join(missing)}；"
                f"模板填空式思考会回避这些根本问题。建议 PM 在 Generate 阶段勾选" +
                f"「本项目不适用」并登记理由（governance 第一性原理登记段）",
                blocking=False))
    current = get_section(text, "当前现状与已有做法")
    goal = get_section(text, "目标与成功判断")
    background = get_section(text, "项目背景")
    if project_type == "重构":
        if not (re.search(r"之前|原来|当前|现状|改造前|before", current, re.I) and re.search(r"之后|改造后|未来|目标|替换|after", current + goal, re.I)):
            errors.append(finding("CRITICAL", "bg.rebuild_before_after_missing", "重构项目必须说明之前现状以及要改成什么样。"))
        if not re.search(r"\d|%|分钟|小时|天|周|月|年|次|人日|成本|转化", current + get_section(text, "核心问题与证据")):
            warnings.append(finding("MEDIUM", "bg.rebuild_evidence_unquantified", "重构动机没有可量化证据；请补充数据或标为待确认。", False))
    elif project_type == "从 0 到 1":
        steps = len(re.findall(r"^\s*(?:\d+\.|[-*])\s+", current, re.MULTILINE))
        if steps < 2:
            errors.append(finding("CRITICAL", "bg.zero_to_one_process_missing", "从 0 到 1 项目必须说明至少两步已有做法或首个完整业务流程。"))
        if not substantive(goal):
            errors.append(finding("CRITICAL", "bg.goal_missing", "从 0 到 1 项目必须说明要建立什么业务结果。"))
    elif project_type == "迭代":
        if not (substantive(background) and substantive(goal)):
            errors.append(finding("CRITICAL", "bg.iteration_background_goal_missing", "迭代需求必须说明为什么加/改，以及加/改后要获得什么结果。"))
        if len(text) > 5000:
            warnings.append(finding("MEDIUM", "bg.iteration_too_long", "迭代背景目标篇幅过长；确认没有写成完整项目章程。", False))
    else:
        warnings.append(finding("MEDIUM", "bg.project_type_unconfirmed", "Project type is not confirmed; complete AI judgment and PM selection first.", False))
    companion = path.with_name(f"{path.stem}.governance.md")
    if not companion.is_file():
        record = finding("CRITICAL" if meta.get("status") == "confirmed" else "MEDIUM", "bg.governance_missing", f"Companion file not found: {companion.name}", meta.get("status") == "confirmed")
        (errors if record["blocking"] else warnings).append(record)
    else:
        governance = companion.read_text(encoding="utf-8")
        gov_meta = frontmatter(governance)
        missing_gov = {"artifact_id", "main_artifact", "main_version", "main_sha256", "status"} - gov_meta.keys()
        if missing_gov:
            errors.append(finding("CRITICAL", "bg.governance_frontmatter_missing", f"Governance companion is missing: {', '.join(sorted(missing_gov))}"))
        missing_gov_headings = [name for name in GOVERNANCE_HEADINGS if name not in headings(governance)]
        if missing_gov_headings:
            errors.append(finding("CRITICAL", "bg.governance_headings_missing", f"Governance companion missing headings: {', '.join(missing_gov_headings)}"))
        if gov_meta.get("artifact_id") and gov_meta["artifact_id"] != meta.get("artifact_id"):
            errors.append(finding("CRITICAL", "bg.artifact_id_mismatch", "Main document and governance companion have different artifact_id values."))
        if gov_meta.get("main_version") and gov_meta["main_version"] != meta.get("version"):
            errors.append(finding("CRITICAL", "bg.version_mismatch", "Main document and governance companion have different version values."))
        actual_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        recorded_hash = gov_meta.get("main_sha256", "")
        if recorded_hash not in {"", "待确认", "待补充"} and recorded_hash != actual_hash:
            errors.append(finding("CRITICAL", "bg.hash_mismatch", "main_sha256 does not match the human-facing document."))
        if project_type in VALID_TYPES and not re.search(r"AI.*判断|PM.*选择", get_section(governance, "类型判断与 PM 选择")):
            errors.append(finding("CRITICAL", "bg.type_choice_missing", "Governance companion must record both AI judgment and PM selection."))
        if meta.get("artifact_id", "").endswith("-001"):
            meeting_section = get_section(governance, "项目级会议基线（可选）") or get_section(governance, "001 会议基线读取记录")
            if meeting_section:
                missing_tokens = [t for t in ("读取命令", "四类拆分", "使用位置") if t not in meeting_section]
                if missing_tokens:
                    errors.append(finding("CRITICAL", "bg.meeting_baseline_incomplete",
                        f"治理伴随文件登记了项目级会议基线，但缺少必要 token：{', '.join(missing_tokens)}"))
                if not re.search(r"https?://|feishu\.cn|lark\.cn|notion\.|confluence\.", meeting_section):
                    warnings.append(finding("MEDIUM", "bg.meeting_baseline_no_link",
                        "项目级会议基线段未发现原文链接，请确认是否需要补充", False))
        if meta.get("status") == "confirmed" and ("确认" not in get_section(governance, "PM 确认与变更") or "待确认" in get_section(governance, "PM 确认与变更")):
            errors.append(finding("CRITICAL", "bg.confirmation_missing", "Confirmed document requires a completed PM confirmation record."))
    return {"ok": not errors, "errors": [x["message"] for x in errors], "warnings": [x["message"] for x in warnings], "issues": errors + warnings}

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
