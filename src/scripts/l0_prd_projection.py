#!/usr/bin/env python3
"""Deterministically project a confirmed L0 mini-prd into a reader-facing PRD.

L0 keeps one human-reviewed work item. This module creates no business fact:
every generated PRD section is selected from the mini-prd or is a fact-based
applicability decision read from the durable intake matrix. Provenance lives in
the manifest; the final PRD never embeds a second copy of the mini-prd.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from workflow_registry import artifact_content_hash, read_frontmatter


CANONICAL_TEMPLATE_VERSION = "1"
APPLICABILITY_KEYS = (
    "项目背景", "项目范围", "用户旅程", "用户故事", "功能清单", "功能流程",
    "原型/UX", "交互规则", "业务规则", "计算与流程规则", "校验规则",
    "状态变化", "异常处理", "验收依据", "按需章节",
)


def _req_dir_for(path: Path) -> Path | None:
    for parent in (path.parent, *path.parents):
        if (parent / "00-input" / "intake-decision.md").is_file():
            return parent
    return None


def _real(value: str) -> bool:
    return value.strip() not in {"", "待填写", "待判断", "待确认", "YYYY-MM-DD", "N/A", "NA", "暂无", "本期不做", "本期不适用"}


def _parse_conditional(value: str) -> tuple[str, str]:
    trigger = re.search(r"触发条件[：:]\s*([^；;|]+)", value)
    current = re.search(r"当前判断[：:]\s*([^；;|]+)", value)
    return (trigger.group(1).strip() if trigger else "", current.group(1).strip() if current else "")


def _intake_applicability(mini_path: Path) -> dict[str, dict[str, str]]:
    """Read the durable chapter decisions rather than inventing them at projection time."""
    req_dir = _req_dir_for(mini_path)
    if req_dir is None:
        raise ValueError("L0 projection requires 00-input/intake-decision.md")
    intake = req_dir / "00-input" / "intake-decision.md"
    rows: dict[str, dict[str, str]] = {}
    for line in intake.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8 or cells[0] == "章节" or not cells[0].startswith("§"):
            continue
        key = re.sub(r"^§\d+(?:\.\d+)?\s*", "", cells[0]).strip()
        if key not in APPLICABILITY_KEYS:
            continue
        rows[key] = {
            "status": cells[1], "basis": cells[2], "source": cells[3],
            "decided_by": cells[4], "decided_at": cells[5],
            "decision": cells[6], "review_trigger": cells[7],
        }
    missing = [key for key in APPLICABILITY_KEYS if key not in rows]
    if missing:
        raise ValueError("L0 projection intake applicability matrix is missing: " + ", ".join(missing))
    for key, row in rows.items():
        if row["status"] not in {"required", "conditional", "not_applicable"}:
            raise ValueError(f"L0 projection intake applicability has invalid status for {key}")
        if row["status"] == "not_applicable" and row["basis"].strip() in {"N/A", "NA", "暂无", "本期不做", "本期不适用", "无"}:
            raise ValueError(f"L0 projection not_applicable applicability for {key} needs a factual basis")
        required = ("basis", "source", "decided_by", "decided_at", "review_trigger")
        absent = [field for field in required if not _real(row[field])]
        if absent:
            raise ValueError(f"L0 projection intake applicability for {key} is incomplete: {', '.join(absent)}")
        if row["status"] == "conditional":
            trigger, current = _parse_conditional(row["decision"])
            if not _real(trigger) or not _real(current):
                raise ValueError(f"L0 projection conditional applicability for {key} needs trigger and current judgment")
    return rows


def _body_after_frontmatter(text: str) -> str:
    return re.sub(r"\A(?:<!--.*?-->\s*)?---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL).strip()


def _sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^##\s+(?:\d+\.\s*)?(.+?)\s*$", text, re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        title = re.sub(r"^\d+\.\s*", "", match.group(1)).strip()
        sections[title] = text[match.end():end].strip()
    return sections


def _applicability(status: str, basis: str, source: str, decided_by: str, decided_at: str,
                   trigger: str = "", current_judgment: str = "", review_trigger: str = "") -> str:
    fields = {
        "status": status,
        "basis": basis,
        "source": source,
        "decided_by": decided_by,
        "decided_at": decided_at,
        "trigger": trigger,
        "current_judgment": current_judgment or ("必须提供" if status == "required" else "当前无新增深度需求"),
        "review_trigger": review_trigger or "范围、行为或风险变化时复审",
    }
    return "<!-- applicability: " + "; ".join(f"{key}={value}" for key, value in fields.items()) + " -->"


def build_projection(mini_path: Path, mini_text: str | None = None, *, reviewer: str,
                     confirmed_at: str | None = None) -> tuple[str, dict]:
    """Return canonical PRD text and its manifest for one L0 mini-prd.

    The caller owns transactional writing. The returned manifest binds the
    selected mini-prd sections and source hash; no source body is copied.
    """
    source_text = mini_text if mini_text is not None else mini_path.read_text(encoding="utf-8")
    meta = read_frontmatter(mini_path) if mini_text is None else _frontmatter(source_text)
    if meta.get("process_tier", "").upper() != "L0":
        raise ValueError("L0 projection requires mini-prd process_tier: L0")
    artifact_id = meta.get("artifact_id", "")
    if not artifact_id:
        raise ValueError("L0 projection requires mini-prd artifact_id")
    parts = _sections(source_text)
    required = ("改什么", "为什么", "影响范围", "行为需求与验收", "异常与边界", "依赖与开口问题")
    missing = [title for title in required if not parts.get(title)]
    if missing:
        raise ValueError("L0 projection requires mini-prd sections: " + ", ".join(missing))
    decisions = _intake_applicability(mini_path)

    decided_at = (confirmed_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat())
    source_ref = artifact_id
    source_hash = artifact_content_hash(source_text)
    owner = meta.get("owner", "")
    fact_owner = meta.get("business_fact_owner", "")
    goal_owner = meta.get("goal_decision_owner", "")
    version = meta.get("version", "v0.1")
    scope = parts["影响范围"]
    change = parts["改什么"]
    reason = parts["为什么"]
    behavior = parts["行为需求与验收"]
    boundary = parts["异常与边界"]
    open_items = parts["依赖与开口问题"]
    no_deep_basis = f"{scope} 本次未声明新的页面结构、交互规则、字段校验或持久状态模型。"

    def decision(title: str) -> tuple[str, str, str, str, str, str, str, str]:
        item = decisions[title]
        trigger, judgment = _parse_conditional(item["decision"])
        return (item["status"], item["basis"], item["source"], item["decided_by"],
                item["decided_at"], trigger, judgment or item["decision"], item["review_trigger"])

    section_decisions = {
        "项目背景": "项目背景",
        "项目范围": "项目范围",
        "用户与用户旅程": "用户旅程",
        "用户故事与优先级": "用户故事",
        "功能清单": "功能清单",
        "功能流程": "功能流程",
        "页面与体验": "原型/UX",
        "交互规则": "交互规则",
        "验收标准": "验收依据",
        "依赖与待决业务问题": "按需章节",
    }

    def applicability_for(title: str) -> str:
        decision_title = section_decisions.get(title, title)
        status, basis, source, decided_by, decided_at_value, trigger, judgment, review = decision(decision_title)
        return _applicability(status, basis, source, decided_by, decided_at_value, trigger, judgment, review)

    def section(number: str, title: str, content: str) -> str:
        return (f"## {number}. {title}\n\n"
                + applicability_for(title)
                + f"\n\n{content}\n")

    def decision_content(title: str) -> str:
        status, _basis, _source, _decided_by, _decided_at_value, _trigger, judgment, _review = decision(title)
        return judgment if status == "required" else ""

    prd = [
        "---",
        f"artifact_id: PRD-{artifact_id.removeprefix('MP-')}",
        f"version: {version}",
        "status: draft",
        f"owner: {owner}",
        f"business_fact_owner: {fact_owner}",
        f"goal_decision_owner: {goal_owner}",
        f"reviewer: {reviewer}",
        f"created_at: {meta.get('created_at', decided_at)}",
        f"updated_at: {decided_at}",
        "confirmed_at: \"\"",
        "prd_structure_version: \"8\"",
        "reader_contract_version: \"2\"",
        "process_tier: \"L0\"",
        "issue_in_prd: false",
        "applicability_contract_version: \"1\"",
        f"upstream_artifact_ids: [\"{artifact_id}\"]",
        "upstream_work_item_statuses: \"mini-prd:confirmed\"",
        "---",
        "",
        "# PRD（产品需求文档）",
        "",
        "<!-- canonical_prd_projection: source=mini-prd; mapping_version=1; no_new_business_facts=true -->",
        "",
        section("1", "项目背景", reason),
        section("2", "项目范围", scope),
        section("3", "用户与用户旅程",
                "> L0 投影简化：mini-prd 单节『影响范围』未拆分为独立旅程图；详细路径见 §2 项目范围。"),
        section("4", "用户故事与优先级", change + "\n\n> L0 投影简化：mini-prd 未采集 Gherkin 用户故事与 MoSCoW 优先级；本节以『改什么』作为最小故事叙述。"),
        section("5", "功能清单", change),
        section("6", "功能流程", behavior),
        "## 7. 页面与体验\n\n" + applicability_for("原型/UX") + "\n\n> 本期不适用：详见上方 applicability 块的 `basis` 与 `source` 字段。\n",
        "## 8. 交互规则\n\n" + applicability_for("交互规则") + "\n\n> 本期不适用：详见上方 applicability 块的 `basis` 与 `source` 字段。\n",
        "## 9. 业务规则\n\n" + applicability_for("业务规则") + "\n",
        "### 9.1 计算与流程规则\n\n" + applicability_for("计算与流程规则") + f"\n\n{behavior}\n",
        *( ["### 9.2 校验规则\n\n" + applicability_for("校验规则") + f"\n\n{decision_content('校验规则')}\n"] if decisions["校验规则"]["status"] == "required" else ["### 9.2 校验规则\n\n" + applicability_for("校验规则") + "\n\n> 本期不适用：详见上方 applicability 块的 `basis` 与 `source` 字段。\n"] ),
        *( ["### 9.3 状态变化\n\n" + applicability_for("状态变化") + f"\n\n{decision_content('状态变化')}\n"] if decisions["状态变化"]["status"] == "required" else ["### 9.3 状态变化\n\n" + applicability_for("状态变化") + "\n\n> 本期不适用：详见上方 applicability 块的 `basis` 与 `source` 字段。\n"] ),
        *( ["### 9.4 异常处理与恢复\n\n" + applicability_for("异常处理") + f"\n\n{boundary}\n"] if decisions["异常处理"]["status"] == "required" else ["### 9.4 异常处理与恢复\n\n" + applicability_for("异常处理") + "\n\n> 本期不适用：详见上方 applicability 块的 `basis` 与 `source` 字段。\n"] ),
        section("10", "验收标准", behavior),
        *( [section("11", "依赖与待决业务问题", open_items)] if _real(open_items) else [] ),
        "",
    ]
    manifest = {
        "schema_version": 2,
        "process_tier": "L0",
        "projection_version": CANONICAL_TEMPLATE_VERSION,
        "sources": [{
            "work_item": "mini-prd",
            "artifact_id": artifact_id,
            "path": mini_path.relative_to(_req_dir_for(mini_path)).as_posix(),
            "status": "confirmed",
            "content_sha256": source_hash,
            "target_sections": ["§1", "§2", "§3", "§4", "§5", "§6", "§9", "§10", "§11"],
            "selectors": ["改什么", "为什么", "影响范围", "行为需求与验收", "异常与边界", "依赖与开口问题"],
        }],
    }
    return "\n".join(prd), manifest


def _frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("'\"")
    return result


def write_projection(mini_path: Path, output_path: Path, manifest_path: Path, *, reviewer: str,
                     confirmed_at: str | None = None, projection: tuple[str, dict] | None = None) -> None:
    """Atomically publish a preflighted L0 projection and its manifest."""
    prd, manifest = projection or build_projection(mini_path, reviewer=reviewer, confirmed_at=confirmed_at)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, dir=output_path.parent) as prd_tmp, \
         tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, dir=manifest_path.parent) as manifest_tmp:
        prd_tmp.write(prd)
        manifest_tmp.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        prd_tmp_path, manifest_tmp_path = Path(prd_tmp.name), Path(manifest_tmp.name)
    try:
        os.replace(prd_tmp_path, output_path)
        os.replace(manifest_tmp_path, manifest_path)
    except OSError:
        prd_tmp_path.unlink(missing_ok=True)
        manifest_tmp_path.unlink(missing_ok=True)
        raise
