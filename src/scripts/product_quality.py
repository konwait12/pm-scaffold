"""Shared, evidence-oriented quality checks for L0/L1 product artifacts."""

from __future__ import annotations

import re

QUALITY_HEADING = "产品质量增强记录"
QUALITY_ROWS = (
    "受影响角色与结果",
    "采用方案与被排除替代",
    "价值-成本-风险",
    "失败边界与回退",
    "可证伪条件/停止条件",
)
KNOWLEDGE_STATES = ("FACT", "DECISION", "ASSUMPTION", "UNKNOWN", "AI_INFERENCE", "CONFLICT")
GENERIC_VALUES = ("待确认", "待填写", "待判断", "暂无", "本期不适用", "本期不做", "N/A", "NA")


def _section(text: str) -> str:
    match = re.search(
        r"^##\s+(?:\d+\.\s*)?产品质量增强记录\s*$\n(.*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def validate_quality_record(text: str, *, required: bool) -> tuple[list[str], list[str]]:
    """Return (errors, warnings), requiring substantive rows only at review gate."""
    body = _section(text)
    if not body:
        message = "缺少‘产品质量增强记录’：需记录用户影响、替代方案、价值-成本-风险、失败回退和可证伪条件"
        return ([message] if required else [], [] if required else [message])

    errors: list[str] = []
    warnings: list[str] = []
    for row in QUALITY_ROWS:
        matches = [line for line in body.splitlines() if line.lstrip().startswith("|") and row in line]
        if not matches:
            (errors if required else warnings).append(f"产品质量增强记录缺少项目：{row}")
            continue
        # A row is substantive when it has a conclusion, a knowledge state and a source/owner.
        line = matches[0]
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        conclusion = cells[1] if len(cells) > 1 else ""
        state = cells[2] if len(cells) > 2 else ""
        source = cells[3] if len(cells) > 3 else ""
        owner = cells[4] if len(cells) > 4 else ""
        missing = []
        if not conclusion or conclusion in GENERIC_VALUES:
            missing.append("结论")
        if not any(token in state for token in KNOWLEDGE_STATES):
            missing.append("知识状态")
        if not source or source in GENERIC_VALUES:
            missing.append("来源/位置")
        if not owner or owner in GENERIC_VALUES:
            missing.append("判断人")
        if missing:
            message = f"产品质量增强记录‘{row}’缺少真实字段：{', '.join(missing)}"
            (errors if required else warnings).append(message)
    return errors, warnings

