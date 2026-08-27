#!/usr/bin/env python3
"""Deterministically project confirmed tier upstreams into a reader-facing PRD.

This is the L1/L2 counterpart of ``l0_prd_projection.py``: registry-driven,
deterministic, and strictly read-only with respect to business facts.  The
final ``prd.md`` contains only selected, deduplicated product facts; provenance
(artifact IDs, paths, confirmed status, SHA-256, target_sections, selectors)
lives in ``prd-assembly-manifest.json``; process/audit material stays in
``99-review/`` and ``.audit/``.

Guarantees:
  * Work-item set comes from ``workflow_registry.work_items_for_tier()`` —
    nothing is hardcoded to a specific REQ.
  * Content is selected by ``WORK_ITEM_SECTION_MAP`` (upstream H2 selectors);
    governance/process chapters are never copied into the PRD.
  * Applicability metadata is read from the durable intake-decision.md
    canonical matrix — never invented at projection time.
  * Output is always a ``draft``.  The module refuses to overwrite a
    confirmed/ready_for_human_review PRD; confirmation is exclusively an
    authorized human ``pipeline.py review --decision approve``.

Run:
  python3 prd_assembly_projection.py <req_dir> [--tier L1|L2] [--apply] [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from workflow_registry import (
    artifact_content_hash,
    find_artifact,
    read_frontmatter,
    require_persisted_tier,
    work_items_for_tier,
)

PROJECTION_VERSION = "1"
READER_CONTRACT_VERSION = "2"

# PRD section key -> (heading number, reader-facing title).
PRD_SECTIONS = {
    "§1": ("1", "项目背景"),
    "§2": ("2", "项目范围"),
    "§3": ("3", "用户与用户旅程"),
    "§4": ("4", "用户故事与优先级"),
    "§5": ("5", "功能清单"),
    "§6": ("6", "功能流程"),
    "§7": ("7", "页面与体验"),
    "§8": ("8", "交互规则"),
    "§9": ("9", "业务规则"),
    "§9.1": ("9.1", "计算与流程规则"),
    "§9.2": ("9.2", "字段清单"),
    "§9.3": ("9.3", "校验规则"),
    "§9.4": ("9.4", "状态变化"),
    "§9.5": ("9.5", "异常处理与恢复"),
    "§10": ("10", "验收标准"),
    "§11": ("11", "依赖与待决业务问题"),
}

# intake-decision.md canonical matrix chapter label -> PRD section key.
INTAKE_TO_PRD = {
    "§1 项目背景": "§1",
    "§2 项目范围": "§2",
    "§3 用户旅程": "§3",
    "§4 用户故事": "§4",
    "§5 功能清单": "§5",
    "§6 功能流程": "§6",
    "§7 原型/UX": "§7",
    "§8 交互规则": "§8",
    "§9 业务规则": "§9",
    "§9.1 计算与流程规则": "§9.1",
    "§9.2 字段清单": "§9.2",
    "§9.3 校验规则": "§9.3",
    "§9.4 状态变化": "§9.4",
    "§9.5 异常处理": "§9.5",
    "§10 验收依据": "§10",
    "§11 按需章节": "§11",
    # Legacy intake rows created before the schema-7 chapter split (§9.2 字段清单
    # / §9.3 校验 / §9.4 状态 / §9.5 异常).  Old REQs still carry these labels.
    "§9.2 校验规则": "§9.3",
    "§9.3 状态变化": "§9.4",
    "§9.4 异常处理": "§9.5",
}

# Legacy rows that split into two PRD sections.  The old "校验规则" row covered
# both field definitions and validation rules; under schema-7 it feeds both
# §9.2 字段清单 and §9.3 校验规则.
LEGACY_SPLIT_INTAKE = {
    "§9.2 校验规则": "§9.2",
}

# Upstream work_item -> { PRD section key: [upstream H2 title selectors] }.
# Selectors match number-stripped H2 titles by prefix.  Only business-bearing
# chapters are listed; governance/process chapters are never selected.
# Kept in sync with workflow-registry.json schema_version 7 tier membership:
# L1 = 9 upstreams, L2 = 15 upstreams.
WORK_ITEM_SECTION_MAP = {
    "feasibility-analysis": {
        "§1": ["结论摘要", "市场空间", "技术可行性", "投入产出", "风险评估"],
    },
    "project-background-goal": {
        "§1": [
            "需求来源与触发", "项目与需求背景", "当前现状与已有做法",
            "核心问题与证据", "目标、未来期望与成功判断",
            "用户角色与利益相关者", "时间、约束与依赖",
        ],
    },
    "project-scope": {
        "§2": ["结论摘要", "In Scope", "Out of Scope", "Deferred", "Conditional"],
    },
    "user-journey": {
        "§3": ["业务生命周期分解", "用户旅程图"],
    },
    "user-stories": {
        "§4": ["用户故事卡片", "旅程→故事覆盖矩阵"],
    },
    "feature-list": {
        "§5": ["功能清单", "功能→故事追溯矩阵"],
        "§2": ["范围基线"],
    },
    "functional-flow": {
        "§6": ["主流程", "分支流程", "异常流程", "P1 功能流程简述"],
    },
    "page-design": {
        "§7": ["页面与步骤描述", "页面结构"],
    },
    "interaction-rules": {
        "§8": ["交互规则"],
    },
    "business-rules": {
        "§9.1": ["业务规则"],
    },
    "field-rules": {
        "§9.2": ["字段清单总览", "字段定义表", "字段来源说明", "字段与校验"],
    },
    "validation-rules": {
        "§9.3": ["系统校验", "跨字段约束", "校验时机分层"],
    },
    "state-machine": {
        "§9.4": ["状态定义", "状态转换表", "禁止转换显式声明"],
    },
    "exception-handling": {
        "§9.5": ["异常与失败处理"],
    },
    "acceptance-criteria": {
        "§10": ["验收标准", "AC 表", "验收依据"],
    },
}

# Section keys that the reader contract requires per tier.
REQUIRED_READER_CORE = {"§1", "§2", "§3", "§4", "§5", "§6", "§9", "§9.1", "§10"}
REQUIRED_READER_L2 = REQUIRED_READER_CORE | {"§7", "§8", "§9.2", "§9.3", "§9.4", "§9.5"}

# Sections that exist only when the tier has a confirmed upstream providing them.
TIER_ONLY_SECTIONS = {
    "§7": "page-design",
    "§8": "interaction-rules",
    "§9.2": "field-rules",
    "§9.3": "validation-rules",
    "§9.4": "state-machine",
    "§9.5": "exception-handling",
}

# Authoritative upstream for a section that must fall back on older REQs.
# Schema-7 split §2 范围 (project-scope) and §9.2 字段清单 (field-rules) out of
# artifacts that older REQs still carry.  When the authoritative upstream is
# missing (legacy REQ), fall back to the older carrier's business chapters.
FALLBACK_SECTION_SOURCES = {
    "§2": [  # authoritative: project-scope
        ("project-background-goal", ["初步边界与非目标"]),
        ("feature-list", ["范围基线"]),
    ],
    "§9.2": [  # authoritative: field-rules
        ("validation-rules", ["字段定义表", "字段清单", "字段"]),
    ],
}

OPEN_ITEM_RE = re.compile(r"\b(?:Q|UNK|ISS|DEC)-\d+\b")
_HEADING_RE = re.compile(r"^#{2,4}\s+(.+?)\s*$", re.MULTILINE)
_PLACEHOLDER_RE = re.compile(r"待填写|待判断|待确认|TBD|TODO|YYYY-MM-DD|本期不做|N/?A")


def _strip_frontmatter(text: str) -> str:
    return re.sub(r"\A(?:<!--.*?-->\s*)?---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL).strip()


def _strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def _norm_heading(raw: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)?\.\s*", "", raw.strip()).strip()


def _h2_blocks(body: str) -> list[tuple[str, str]]:
    """Return [(normalized_title, content)] of top-level (##) chapters."""
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", body, re.MULTILINE))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = _norm_heading(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        content = _strip_comments(body[match.end():end]).strip()
        blocks.append((title, content))
    return blocks


def _req_dir_for(path: Path) -> Path | None:
    for parent in (path.parent, *path.parents):
        if (parent / "00-input" / "intake-decision.md").is_file():
            return parent
    return None


def _intake_applicability(req_dir: Path) -> dict[str, dict[str, str]]:
    """Read the durable canonical applicability matrix from intake-decision.md."""
    intake = req_dir / "00-input" / "intake-decision.md"
    meta = read_frontmatter(intake)
    if meta.get("applicability_contract_version") != "1":
        raise ValueError(
            "prd_assembly_projection requires applicability_contract_version: \"1\" "
            "in 00-input/intake-decision.md"
        )
    rows: dict[str, dict[str, str]] = {}
    for line in intake.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("| §"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            continue
        prd_key = INTAKE_TO_PRD.get(cells[0])
        if prd_key is None:
            continue
        rows[prd_key] = {
            "status": cells[1], "basis": cells[2], "source": cells[3],
            "decided_by": cells[4], "decided_at": cells[5],
            "decision": cells[6], "review_trigger": cells[7],
        }
        split_key = LEGACY_SPLIT_INTAKE.get(cells[0])
        if split_key is not None and split_key not in rows:
            # Legacy "校验规则" row feeds both the new §9.2 字段清单 and §9.3 校验规则.
            rows[split_key] = {
                "status": cells[1], "basis": cells[2] + "（派生自 legacy §9.2 校验规则行）",
                "source": cells[3], "decided_by": cells[4], "decided_at": cells[5],
                "decision": cells[6], "review_trigger": cells[7],
            }
    if not rows:
        raise ValueError(
            "prd_assembly_projection requires the canonical applicability matrix "
            "(| §… rows) in 00-input/intake-decision.md"
        )
    return rows


def _parse_conditional(value: str) -> tuple[str, str]:
    trigger = re.search(r"触发条件[：:]\s*([^；;|]+)", value)
    current = re.search(r"当前判断[：:]\s*([^；;|]+)", value)
    return (trigger.group(1).strip() if trigger else "",
            current.group(1).strip() if current else "")


def _applicability_block(decision: dict[str, str]) -> str:
    status = decision.get("status", "")
    trigger, current = _parse_conditional(decision.get("decision", ""))
    fields = {
        "status": status,
        "basis": decision.get("basis", ""),
        "source": decision.get("source", ""),
        "decided_by": decision.get("decided_by", ""),
        "decided_at": decision.get("decided_at", ""),
        "trigger": trigger,
        "current_judgment": current or ("必须提供" if status == "required" else ""),
        "review_trigger": decision.get("review_trigger", ""),
    }
    return "<!-- applicability: " + "; ".join(f"{k}={v}" for k, v in fields.items()) + " -->"


_INSTRUCTION_LEAD_RE = re.compile(
    r"^(说明|解释|明确|记录|列出|描述|定义|分析|评估|识别|总结|确认|核对|补充|保持|确保|遵循|先)"
)


def _strip_instruction_lead(content: str) -> str:
    """Drop an upstream template instruction that leads a chapter block.

    Conservative: only a standalone short line that starts with a known
    imperative verb and carries no structural markers (:, |, **, digits,
    SRC, §) is treated as guidance, never as a business fact.
    """
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        stripped = line.strip()
        if (
            len(stripped) <= 80
            and not re.search(r"[:|\*\d§]|SRC", stripped)
            and _INSTRUCTION_LEAD_RE.match(stripped)
        ):
            lines[index] = ""
        break
    return "\n".join(lines).strip()


def _select_content(blocks: list[tuple[str, str]], selectors: list[str]) -> list[str]:
    """Pick upstream chapters whose number-stripped title matches a selector."""
    picked: list[str] = []
    for title, content in blocks:
        content = _strip_instruction_lead(content)
        if not content:
            continue
        for selector in selectors:
            if title == selector or title.startswith(selector) or selector in title:
                picked.append(f"**{title}**\n\n{content}")
                break
    return picked


def _renumber_subheadings(content: str, section_number: str) -> str:
    """Rewrite upstream ``### X.Y`` sub-headings so they follow the PRD chapter
    number instead of the upstream artifact's own numbering.

    Example: functional-flow's internal ``### 2.1`` becomes ``### 6.1`` once
    assembled under PRD §6.  Applies only when the target chapter number is a
    plain integer (§6/§7/§8/§10/§11); §9.x chapters keep their own generated
    sub-numbers and are left untouched.  Idempotent on content that already
    carries the correct prefix.
    """
    if not re.fullmatch(r"\d+", section_number):
        return content
    return re.sub(
        r"^###\s+(\d+)\.(\d+)\b",
        lambda m: f"### {section_number}.{m.group(2)}",
        content,
        flags=re.MULTILINE,
    )


def _collect_upstreams(req_dir: Path, tier: str) -> tuple[list[tuple[dict, Path, str, dict[str, str]]], list[str]]:
    """Return (collected, missing_ids) for tier upstreams.

    ``collected`` entries are (work_item, artifact_path, source_text, meta).
    Missing artifacts are tolerated and reported (controlled legacy fallback,
    option B): an older REQ may predate the schema-7 upstream split.  An
    artifact that exists but is NOT confirmed still blocks assembly — assembly
    must never consume unconfirmed business content.
    """
    collected: list[tuple[dict, Path, str, dict[str, str]]] = []
    missing: list[str] = []
    for item in work_items_for_tier(tier):
        if item["id"] == "prd-assembly":
            continue
        artifact = find_artifact(req_dir, item)
        if artifact is None:
            missing.append(item["id"])
            continue
        text = artifact.read_text(encoding="utf-8")
        meta = read_frontmatter(artifact)
        if meta.get("status") != "confirmed":
            raise ValueError(
                f"prd_assembly_projection blocked: {item['id']} must be confirmed "
                f"before PRD assembly (got {meta.get('status', 'unknown')})"
            )
        collected.append((item, artifact, text, meta))
    return collected, missing


def _open_items(collected: list[tuple[dict, Path, str, dict[str, str]]]) -> list[str]:
    """Extract real open decision items (Q- rows) from upstream 待确认问题 chapters.

    Returns rendered table rows (| ID | item | status |).  Only real pending
    business questions survive; 事实与决定 DEC/FCT ledger rows and template
    placeholders are governance, not PRD content, and stay out of the PRD.
    """
    seen: dict[str, str] = {}
    for _item, _path, text, _meta in collected:
        body = _strip_frontmatter(text)
        for title, content in _h2_blocks(body):
            if title != "待确认问题" and not title.startswith("待确认问题"):
                continue
            for match in re.finditer(r"^\|\s*((?:Q|UNK|ISS|DEC)-\d+(?:-\d+)*)\s*\|(.*)$", content, re.MULTILINE):
                item_id, rest = match.group(1), match.group(2).strip()
                if item_id in seen:
                    continue
                cells = [cell.strip() for cell in rest.split("|")]
                description = cells[0] if cells else ""
                if not description or _PLACEHOLDER_RE.search(description):
                    continue
                seen[item_id] = description
    return [f"| {item_id} | {description} | open |" for item_id, description in sorted(seen.items())]


def build_projection(req_dir: Path, tier: str | None = None) -> tuple[str, dict]:
    """Return (prd_text, manifest) for the tier's confirmed upstreams.

    The caller owns writing.  Output is a draft: no auto-confirmation ever.
    """
    tier = (tier or require_persisted_tier(req_dir)).upper()
    if tier not in {"L1", "L2"}:
        raise ValueError("prd_assembly_projection supports L1/L2; L0 uses l0_prd_projection.py")

    collected, missing = _collect_upstreams(req_dir, tier)
    legacy_fallback = bool(missing)
    decisions = _intake_applicability(req_dir)
    collected_by_id = {item["id"]: (item, artifact, text, meta) for item, artifact, text, meta in collected}

    # Per-section content assembled from authoritative upstreams.
    section_blocks: dict[str, list[str]] = {}
    manifest_sources: list[dict] = []
    upstream_ids: list[str] = []
    upstream_statuses: list[str] = []
    for item, artifact, text, meta in collected:
        body = _strip_frontmatter(text)
        blocks = _h2_blocks(body)
        selectors_map = WORK_ITEM_SECTION_MAP.get(item["id"], {})
        for section_key, selectors in selectors_map.items():
            picked = _select_content(blocks, selectors)
            if picked:
                section_blocks.setdefault(section_key, []).extend(picked)
        artifact_id = meta.get("artifact_id", "")
        if artifact_id:
            upstream_ids.append(artifact_id)
        upstream_statuses.append(f"{item['id']}: confirmed")
        manifest_sources.append({
            "work_item": item["id"],
            "artifact_id": artifact_id,
            "path": artifact.relative_to(req_dir).as_posix(),
            "status": "confirmed",
            "content_sha256": artifact_content_hash(text),
            "target_sections": sorted(selectors_map.keys()),
            "selectors": [s for sels in selectors_map.values() for s in sels],
        })

    # Controlled legacy fallback (option B): when the authoritative upstream of a
    # section is missing (schema-7 split on old REQs), pull business content from
    # the older carrier artifact so the draft has real content, not pointers.
    if legacy_fallback:
        for section_key, fallbacks in FALLBACK_SECTION_SOURCES.items():
            if section_blocks.get(section_key):
                continue
            for carrier_id, selectors in fallbacks:
                entry = collected_by_id.get(carrier_id)
                if entry is None:
                    continue
                _item, _artifact, text, _meta = entry
                picked = _select_content(_h2_blocks(_strip_frontmatter(text)), selectors)
                if picked:
                    section_blocks.setdefault(section_key, []).extend(picked)
                    break

    # Required core sections must have content; block when a selector maps to
    # nothing (route back upstream instead of inventing a summary).  §9 is a
    # container whose content lives in the §9.x sub-sections.
    required = REQUIRED_READER_L2 if tier == "L2" else REQUIRED_READER_CORE
    empty_required = [key for key in required
                      if key not in TIER_ONLY_SECTIONS
                      and key != "§9"
                      and not section_blocks.get(key)]
    if empty_required:
        raise ValueError(
            "prd_assembly_projection blocked: no business content selected for "
            + ", ".join(empty_required)
            + " — route back to the upstream artifact before assembling."
        )

    # Tier-only sections appear only when the tier upstream actually contributed
    # content (directly or via controlled legacy fallback).  For L1, page/
    # interaction/validation/state/exception sections stay absent.  §9.1-§9.5
    # are sub-sections of the §9 container; §7/§8 are standalone.
    SUB_SECTIONS = {"§9.1", "§9.2", "§9.3", "§9.4", "§9.5"}
    STANDALONE_TIER_SECTIONS = {"§7", "§8"}
    body_parts: list[str] = []
    for section_key, (number, title) in PRD_SECTIONS.items():
        decision = decisions.get(section_key)
        if decision is None:
            continue
        content = "\n\n".join(section_blocks.get(section_key, []))
        content = _renumber_subheadings(content, number)
        if section_key in SUB_SECTIONS:
            if not content:
                continue
            body_parts.append(
                f"### {number} {title}\n\n{_applicability_block(decision)}\n\n{content}\n"
            )
        elif section_key in STANDALONE_TIER_SECTIONS:
            if not content:
                continue
            body_parts.append(
                f"## {number}. {title}\n\n{_applicability_block(decision)}\n\n{content}\n"
            )
        elif section_key == "§9":
            # Container chapter; children were emitted above as ### 9.x.
            body_parts.append(
                f"## {number}. {title}\n\n{_applicability_block(decision)}\n"
            )
        elif section_key == "§11":
            open_rows = _open_items(collected)
            if not open_rows:
                continue
            body_parts.append(
                f"## {number}. {title}\n\n{_applicability_block(decision)}\n\n"
                "| ID | 待决问题 | 状态 |\n|---|---|---|\n" + "\n".join(open_rows) + "\n"
            )
        else:
            body_parts.append(
                f"## {number}. {title}\n\n{_applicability_block(decision)}\n\n{content}\n"
            )

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    owner = collected[0][3].get("owner", "")
    frontmatter = [
        "---",
        f"artifact_id: PRD-{req_dir.name}",
        "version: \"v0.1\"",
        "status: draft",
        f"owner: {owner}",
        "business_fact_owner: 待填写（由授权 reviewer 在审批时确认）",
        "goal_decision_owner: 待填写（由授权 reviewer 在审批时确认）",
        "reviewer: \"\"",
        f"created_at: {now}",
        f"updated_at: {now}",
        "confirmed_at: \"\"",
        "prd_structure_version: \"8\"",
        f"reader_contract_version: \"{READER_CONTRACT_VERSION}\"",
        f"process_tier: \"{tier}\"",
        "applicability_contract_version: \"1\"",
        "legacy_fallback: " + ("true" if legacy_fallback else "false"),
        "upstream_artifact_ids: [" + ", ".join(f'"{i}"' for i in upstream_ids) + "]",
        "upstream_work_item_statuses: \"" + " | ".join(upstream_statuses) + "\"",
        "---",
        "",
        "# PRD（产品需求文档）",
        "",
        f"<!-- deterministic_prd_projection: tier={tier}; projection_version={PROJECTION_VERSION}; no_new_business_facts=true"
        + ("; legacy_fallback=" + ",".join(missing) if legacy_fallback else "")
        + " -->",
        "",
    ]
    prd_text = "\n".join(frontmatter + body_parts) + "\n"
    manifest = {
        "schema_version": 2,
        "process_tier": tier,
        "projection_version": PROJECTION_VERSION,
        "sources": manifest_sources,
    }
    if legacy_fallback:
        manifest["legacy_fallback"] = True
        manifest["missing_work_items"] = missing
    return prd_text, manifest


def write_draft(req_dir: Path, *, apply: bool = False, tier: str | None = None) -> dict:
    """Preview (default) or atomically write (--apply) the draft projection.

    Refuses to overwrite a confirmed/ready_for_human_review PRD: controlled
    rebuild requires `pipeline.py reflow --work-item prd-assembly --apply`
    first, then this generator, then an authorized human approval.
    """
    prd_text, manifest = build_projection(req_dir, tier=tier)
    tier = manifest["process_tier"]
    output = req_dir / "003-prd-output" / "prd.md"
    manifest_path = req_dir / "003-prd-output" / "prd-assembly-manifest.json"

    if apply:
        if output.is_file():
            existing = read_frontmatter(output)
            if existing.get("status") in {"confirmed", "ready_for_human_review"}:
                raise ValueError(
                    f"refusing to overwrite {output.relative_to(req_dir)} (status="
                    f"{existing.get('status')}); run pipeline.py reflow --work-item "
                    "prd-assembly --apply first, then rebuild, then an authorized "
                    "human review --decision approve."
                )
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False,
                                         dir=output.parent) as prd_tmp, \
             tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False,
                                         dir=manifest_path.parent) as mf_tmp:
            prd_tmp.write(prd_text)
            mf_tmp.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
            prd_tmp_path, mf_tmp_path = Path(prd_tmp.name), Path(mf_tmp.name)
        try:
            os.replace(prd_tmp_path, output)
            os.replace(mf_tmp_path, manifest_path)
        except OSError:
            prd_tmp_path.unlink(missing_ok=True)
            mf_tmp_path.unlink(missing_ok=True)
            raise

    return {
        "tier": tier,
        "apply": apply,
        "prd_path": str(output.relative_to(req_dir)),
        "manifest_path": str(manifest_path.relative_to(req_dir)),
        "status": "draft",
        "legacy_fallback": manifest.get("legacy_fallback", False),
        "missing_work_items": manifest.get("missing_work_items", []),
        "upstreams": [s["work_item"] for s in manifest["sources"]],
        "sections": sorted({s for s in manifest["sources"] for s in s["target_sections"]}),
        "sources": len(manifest["sources"]),
        "prd_lines": prd_text.count("\n") + 1,
        "wrote": apply,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("req_dir", type=Path)
    parser.add_argument("--tier", choices=["L0", "L1", "L2"], default=None,
                        help="Override preview tier (persisted intake tier is the default)")
    parser.add_argument("--apply", action="store_true",
                        help="Atomically write the draft + manifest (default is dry-run)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.req_dir.is_dir():
        print(f"ERROR: {args.req_dir} is not a directory", file=sys.stderr)
        return 1
    try:
        result = write_draft(args.req_dir, apply=args.apply, tier=args.tier)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")
        print(f"{'APPLIED (draft written)' if result['wrote'] else 'DRY-RUN (no files written)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
