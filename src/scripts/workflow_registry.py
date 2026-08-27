#!/usr/bin/env python3
"""Load and resolve the stage, work-item, and artifact registry."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
REGISTRY_PATH = PROJECT / "src/framework/workflow-registry.json"


def artifact_content_hash(text: str) -> str:
    """Single canonical SHA-256 of an artifact's content.

    Review-metadata fields (status / reviewer / reviewed_at / confirmed_at)
    are stripped before hashing so post-confirmation edits to those fields do
    not break `branch_validator` cross-checks against a recorded ReviewRecord.
    Both `pipeline.py` and `branch_validator.py` import this function — keep
    the algorithm here as the single source of truth.
    """
    canonical = re.sub(
        r"(?m)^(status|reviewer|reviewed_at|confirmed_at):.*$",
        r"\1: <review-metadata>",
        text,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_registry() -> dict:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    if registry.get("schema_version") not in (3, 4, 5, 6, 7):
        raise ValueError("Unsupported workflow registry schema")
    return registry


def work_items() -> list[dict]:
    return sorted(load_registry()["work_items"], key=lambda item: item["order"])


def work_items_for_tier(tier: str = "L2") -> list[dict]:
    """按 Process Tier 过滤 work_items；缺省 L2 = 现状 13 项（不含 mini-prd）。

    tier 语义：
      L0 → 仅 mini-prd
      L1 → 7 核心产物 + prd-assembly
      L2 → 现有全 13 项
    work_item 未声明 tiers 时视为 L2（向后兼容存量 registry 读取方）。
    """
    tier = (tier or "L2").upper()
    items = []
    for item in work_items():
        tiers = item.get("tiers") or ["L2"]
        if tier in tiers:
            items.append(item)
    return items


VALID_TIERS = {"L0", "L1", "L2"}
L1_L2_ONLY_FIELDS = {
    "l2_only_pd": "PD 页面/原型",
    "l2_only_ix": "IX 交互规则",
    "l2_only_fields": "FIELDS 字段规则",
    "l2_only_vl": "VL 校验规则",
    "l2_only_state": "STATE 状态机",
    "l2_only_ex": "EX 异常处理",
}

CANONICAL_PRD_APPLICABILITY = (
    "项目背景", "项目范围", "用户旅程", "用户故事", "功能清单", "功能流程",
    "原型/UX", "交互规则", "业务规则", "计算与流程规则", "字段清单", "校验规则",
    "状态变化", "异常处理", "验收依据", "按需章节",
)


def persisted_tier(req_dir: Path) -> tuple[str, str]:
    """Return (tier, source) from durable intake data."""
    decision = req_dir / "00-input" / "intake-decision.md"
    if decision.is_file():
        fm = read_frontmatter(decision)
        tier = fm.get("process_tier", "").upper()
        if tier in VALID_TIERS:
            return tier, "intake-decision"
        raise ValueError(f"invalid or missing process_tier in {decision}")
    readme = req_dir / "README.md"
    try:
        text = readme.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return "L2", "legacy-default"
    match = re.search(r"(?m)^\s*[-*]?\s*\*{0,2}process_tier\*{0,2}\s*[:：]\s*[\"']?`?([Ll][0-2])", text)
    if match:
        return match.group(1).upper(), "README-compat"
    return "L2", "legacy-default"


def require_persisted_tier(req_dir: Path) -> str:
    return persisted_tier(req_dir)[0]


def l1_exclusion_evidence(req_dir: Path) -> dict[str, object]:
    """Validate machine-readable factual exclusions for L1-only omissions."""
    if require_persisted_tier(req_dir) != "L1":
        return {"ok": True, "skipped": True, "issues": []}
    decision = req_dir / "00-input" / "intake-decision.md"
    meta = read_frontmatter(decision)
    issues: list[str] = []
    for field, label in L1_L2_ONLY_FIELDS.items():
        value = meta.get(field, "").strip()
        match = re.fullmatch(r"not_applicable\s*:\s*(.+)", value, re.IGNORECASE)
        reason = match.group(1).strip() if match else ""
        generic = re.search(
            r"(?:本期不适用|无此需求|没有这些能力|无需(?:页面|交互|校验|状态|异常)|不涉及(?:页面|交互|校验|状态|异常))",
            reason,
            re.IGNORECASE,
        )
        factual_anchor = re.search(
            r"(?:页面|入口|字段|角色|状态|模块|功能|来源|SRC-|BG-|FUN-|REQ-|既有|沿用|失败恢复|服务|配置)",
            reason,
            re.IGNORECASE,
        )
        if (
            not match
            or re.fullmatch(r"(?:N/?A|none|无|待填写|待确认|TBD|TODO|pending|-)\.?", reason, re.IGNORECASE)
            or generic
            or not factual_anchor
        ):
            issues.append(f"{label} requires not_applicable plus a specific fact in intake-decision.md")
    return {"ok": not issues, "skipped": False, "issues": issues}


def canonical_applicability_evidence(req_dir: Path) -> dict[str, object]:
    """Validate the durable canonical-PRD applicability matrix for new REQs.

    This is intentionally a final-delivery gate, not a replacement for a work
    item's own validator.  Legacy REQs without the v1 marker remain readable;
    newly initialized REQs must turn every template row into an auditable
    decision before they can deliver a PRD.
    """
    decision = req_dir / "00-input" / "intake-decision.md"
    if not decision.is_file():
        return {"ok": True, "skipped": True, "issues": []}
    meta = read_frontmatter(decision)
    if meta.get("applicability_contract_version") != "1":
        return {"ok": True, "skipped": True, "issues": []}
    rows: dict[str, list[str]] = {}
    for line in decision.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8 or cells[0] == "章节" or not cells[0].startswith("§"):
            continue
        key = re.sub(r"^§\d+(?:\.\d+)?\s*", "", cells[0]).strip()
        if key in CANONICAL_PRD_APPLICABILITY:
            rows[key] = cells
    pending = {"", "待填写", "待判断", "待确认", "YYYY-MM-DD", "N/A", "NA", "暂无", "本期不做", "本期不适用"}
    issues: list[str] = []
    for title in CANONICAL_PRD_APPLICABILITY:
        cells = rows.get(title)
        if not cells:
            issues.append(f"canonical PRD applicability matrix is missing {title}")
            continue
        status, basis, source, decided_by, decided_at, decision_text, review_trigger = cells[1:]
        if status not in {"required", "conditional", "not_applicable"}:
            issues.append(f"canonical PRD applicability {title} has invalid status")
            continue
        absent = [label for label, value in (
            ("basis", basis), ("source", source), ("decided_by", decided_by),
            ("decided_at", decided_at), ("review_trigger", review_trigger),
        ) if value.strip() in pending]
        if absent:
            issues.append(f"canonical PRD applicability {title} is incomplete: {', '.join(absent)}")
        if status == "not_applicable" and basis.strip() in {"N/A", "NA", "暂无", "本期不做", "本期不适用", "无"}:
            issues.append(f"canonical PRD not_applicable {title} requires a factual basis")
        if status == "conditional" and ("触发条件" not in decision_text or "当前判断" not in decision_text
                                          or "待判断" in decision_text):
            issues.append(f"canonical PRD conditional applicability {title} needs trigger and current judgment")
    return {"ok": not issues, "skipped": False, "issues": issues}


def assert_work_item_in_tier(req_dir: Path, item: dict) -> str:
    tier = require_persisted_tier(req_dir)
    enabled = {candidate["id"] for candidate in work_items_for_tier(tier)}
    if item["id"] not in enabled:
        raise ValueError(f"work item {item['id']} is not enabled for persisted tier {tier}")
    return tier


def tier_for_req(req_dir: Path) -> str:
    """读取持久 process_tier；缺失时以 L2 兼容历史 REQ。

    新 REQ 的唯一事实源是 ``00-input/intake-decision.md``。README 只在
    历史迁移场景中兼容读取；不存在两者时按 L2 运行，避免意外降档。
    """
    return require_persisted_tier(req_dir)


def branch_capabilities() -> list[dict]:
    """Return conditional/branch skills (support + newly-registered branch skills)."""
    return list(load_registry().get("support_capabilities", []))


def resolve_branch_capability(branch_id: str) -> dict:
    for cap in branch_capabilities():
        if cap["id"] == branch_id:
            return cap
    raise KeyError(f"Unknown branch capability: {branch_id}")


def resume_work_item_for_tier(capability: dict, tier: str) -> str | None:
    """按持久交付档位解析分支能力的回流工作项。

    材料成熟度与 process tier 正交；分支能力不得把稀疏材料自动解释为 L0。
    """
    normalized = (tier or "L2").upper()
    mapping = capability.get("resume_work_item_by_tier") or {}
    return mapping.get(normalized, capability.get("resume_work_item"))


def resolve_work_item(work_item: str | None = None, wave: int | None = None) -> dict:
    items = work_items()
    if wave is not None:
        for item in items:
            if item["legacy_wave"] == wave:
                return item
        raise KeyError(f"Unknown legacy wave: {wave}")
    if work_item:
        for item in items:
            if item["id"] == work_item:
                return item
        raise KeyError(f"Unknown work item: {work_item}")
    raise ValueError("work_item or wave is required")


def artifact_dirs(req_dir: Path, item: dict) -> list[Path]:
    """Canonical + legacy artifact directories for a work_item.

    ``legacy_artifact_dir`` may be a single string (pre-v7 merged layout, e.g.
    ``02_journey-stories``) or a list (directory renumberings such as v7→v8
    that moved ``02-user-journey`` → ``03-user-journey`` and kept confirmed
    REQs at the old path). ``find_artifact`` searches them in order so existing
    confirmed artifacts stay locatable after registry renumbering.
    """
    dirs = [req_dir / item["artifact_dir"]]
    legacy = item.get("legacy_artifact_dir")
    if isinstance(legacy, str):
        legacy = [legacy]
    for path in legacy or []:
        dirs.append(req_dir / path)
    return dirs


def find_artifact(req_dir: Path, item: dict) -> Path | None:
    for directory in artifact_dirs(req_dir, item):
        if not directory.exists():
            continue
        preferred = directory / item["artifact_file"]
        if preferred.exists():
            return preferred
        for path in sorted(directory.glob("*.md")):
            if path.name != "README.md" and not re.search(r"v0\.\d+", path.name):
                return path
    return None


def read_frontmatter(path: Path) -> dict[str, str]:
    text = re.sub(r"^<!--.*?-->\s*", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    match = re.match(r"---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("'\"")
    return result


def artifact_status(req_dir: Path, item: dict) -> str:
    artifact = find_artifact(req_dir, item)
    return read_frontmatter(artifact).get("status", "unknown") if artifact else "not_created"


def skill_path(item: dict) -> Path:
    return PROJECT / item["skill_path"]
