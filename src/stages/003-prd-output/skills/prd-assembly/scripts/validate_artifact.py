#!/usr/bin/env python3
"""Validate the structure of a prd-assembly Markdown artifact (final PRD).

This work_item is an independent work_item producing a standalone prd.md artifact.
The validator checks the full file content for:
  1. All 13 required PRD sections present
  2. All 12 upstream work_items confirmed and listed
  3. Forward traceability chain: G→UJ→US→ST→FEA→FUN→PD→IX→BR→VL→SM→EX→AC
  4. Backward traceability chain: AC→EX→SM→BR→VL→IX→PD→FUN→FEA→ST→US→UJ
  5. RTM matrix present
  6. Frontmatter and status consistency

Run: python3 validate_artifact.py [<prd.md>] [--json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


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

try:
    from workflow_registry import artifact_content_hash
except ImportError:  # pragma: no cover
    def artifact_content_hash(text: str) -> str:
        canonical = re.sub(r"(?m)^(status|reviewer|reviewed_at|confirmed_at):.*$", r"\1: <review-metadata>", text)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

try:
    import hash_anchor
except ImportError:  # pragma: no cover
    hash_anchor = None

SKILL_ID = "prd_assembly"
CHECK_PREFIX = "prd"

REQUIRED_FRONTMATTER = {
    "artifact_id", "version", "status", "owner",
    "business_fact_owner", "goal_decision_owner", "reviewer",
    "created_at", "updated_at", "confirmed_at",
}

# PRD must expose the current registry v7 work-item sections.
# v8（prd_structure_version=8）起章节重排为 10 主干 + 按需 + 附录：
#   - L2 完整档：10 主干全含（§1-§10）
#   - L1 标准档：无 page-design/interaction-rules 上游 → 仅 8 主干
# v7（缺省）存量 REQ（如 REQ-001）冻结旧 14 headings 契约，不可变。
REQUIRED_HEADINGS_V7 = [
    "项目背景与目标",
    "用户旅程",
    "用户故事与范围基线",
    "功能清单",
    "功能流程",
    "页面设计",
    "交互规则",
    "业务规则",
    "校验规则",
    "状态变化",
    "异常处理",
    "验收依据",
    "需求追溯矩阵",
    "自审记录",
]

# New reader-facing v8 headings. Historical v8 artifacts use the prior names;
# preserve their validation compatibility until they are reflowed and rebuilt.
REQUIRED_HEADINGS_V8_READER_CORE = [
    "项目背景",
    "项目范围",
    "用户与用户旅程",
    "用户故事与优先级",
    "功能清单",
    "功能流程",
    "业务规则",
    "验收标准",
]
REQUIRED_HEADINGS_V8_READER_L2 = [
    *REQUIRED_HEADINGS_V8_READER_CORE[:6],
    "页面与体验",
    "交互规则",
    *REQUIRED_HEADINGS_V8_READER_CORE[6:],
]
REQUIRED_HEADINGS_V8_LEGACY_L2 = [
    "项目背景", "项目范围", "用户旅程", "用户故事", "功能清单",
    "功能流程", "原型/UX", "交互规则", "业务规则", "验收依据",
    "需求追溯矩阵", "自审记录",
]
REQUIRED_HEADINGS_V8_LEGACY_L1 = [
    "项目背景", "项目范围", "用户旅程", "用户故事", "功能清单",
    "功能流程", "业务规则", "验收依据", "需求追溯矩阵", "自审记录",
]
# Current reader-facing titles are used by rebuilt v8 artifacts. Existing v8
# fixtures without reader_contract_version remain compatible during migration.
REQUIRED_HEADINGS_V8_L2 = REQUIRED_HEADINGS_V8_READER_L2
REQUIRED_HEADINGS_V8_L1 = list(REQUIRED_HEADINGS_V8_READER_CORE)
REQUIRED_HEADINGS_V8_L1_LEGACY = REQUIRED_HEADINGS_V8_LEGACY_L1

# L1 has no page, interaction, validation, state, or exception upstream. Their
# trace slots are therefore intentionally absent from reader-facing L1 output.
L1_EXEMPT_TRACE_PREFIXES = ("PD", "IX", "VL", "SM", "STATE", "EX")

APPLICABILITY_TOP_HEADINGS = tuple(dict.fromkeys(REQUIRED_HEADINGS_V8_L2 + REQUIRED_HEADINGS_V8_L1 + ["依赖与待决业务问题"]))
APPLICABILITY_SUBSECTIONS = ("计算与流程规则", "字段清单", "校验规则", "状态变化", "异常处理", "异常处理与恢复")
_APPLICABILITY_RE = re.compile(r"<!--\s*applicability:\s*(.*?)\s*-->", re.DOTALL)
_APPLICABILITY_FIELDS = ("status", "basis", "source", "decided_by", "decided_at")
_APPLICABILITY_STATUSES = {"required", "conditional", "not_applicable"}

# Reader-facing v8 governance chapters.  These carry process/audit material that
# belongs in prd-assembly-manifest.json, 99-review/, or .audit/ — never as top-level
# chapters of the final PRD.  Legacy v8/v7 artifacts may keep them until reflow.
GOVERNANCE_LEAK_KEYWORDS = (
    "自审",                 # 自审记录 / 自审记录（Constitution Compliance）
    "需求追溯矩阵",          # legacy RTM chapter
    "追溯矩阵",
    "clarifications",
    "来源追溯",
    "版本变更摘要",
    "下游输入摘要",
    "产品质量增强记录",
    "constitution compliance",
    "上游 verbatim",
    "下游交接",
    "阶段收口",
    "预检输入充分度",
    "按需章节",
    "需求来源与触发",        # BG 上游 chapter leaked into PRD top level
)


def _applicability_attrs(block: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for item in block.split(";"):
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        attrs[key.strip()] = value.strip()
    return attrs


def _has_real_value(value: str | None) -> bool:
    if not value:
        return False
    normalized = value.strip()
    return normalized not in {"", "待填写", "待判断", "待确认", "YYYY-MM-DD", "TBD", "N/A", "NA", "暂无", "本期不做"}


def _validate_applicability_contract(text: str, meta: dict[str, str], errors: list[str], warnings: list[str]) -> None:
    """Validate applicability for generated v8 sections only.

    The reader-facing contract deliberately omits optional empty chapters.  Each
    generated product section remains auditable, but L0/L1 are not forced to
    manufacture L2-shaped placeholder sections merely to satisfy a count.
    """
    reader_v8 = meta.get("prd_structure_version") == "8" and meta.get("reader_contract_version") == "2"
    if not reader_v8:
        return
    reviewable = meta.get("status") in {"ready_for_human_review", "confirmed"}
    stripped = _strip_source_blocks(text)
    targets: list[tuple[str, str]] = []
    for match in re.finditer(r"^##\s+(?:\d+\.\s*)?(.+?)\s*$", stripped, re.MULTILINE):
        title = _norm(match.group(1))
        if title in APPLICABILITY_TOP_HEADINGS:
            targets.append((title, stripped[match.end():]))
    for match in re.finditer(r"^###\s+(?:9\.[1-5]\s+)?(.+?)\s*$", stripped, re.MULTILINE):
        title = _norm(match.group(1))
        if title in APPLICABILITY_SUBSECTIONS:
            targets.append((title, stripped[match.end():]))
    required = _required_headings(meta)
    present_top = {title for title, _tail in targets}
    missing = [title for title in required if title not in present_top]
    if missing:
        errors.append("Applicability contract failed: missing generated required sections: " + ", ".join(missing))
    for title, tail in targets:
        block_match = _APPLICABILITY_RE.search(tail)
        if not block_match:
            errors.append(f"Applicability contract failed: missing status block for {title}")
            continue
        attrs = _applicability_attrs(block_match.group(1))
        status = attrs.get("status", "")
        if status not in _APPLICABILITY_STATUSES:
            errors.append(f"Applicability contract failed: {title} status must be required, conditional, or not_applicable")
            continue
        missing_fields = [field for field in _APPLICABILITY_FIELDS if not _has_real_value(attrs.get(field))]
        if missing_fields:
            errors.append(f"Applicability contract failed: {title} missing {', '.join(missing_fields)}")
        if status == "conditional":
            conditional_missing = [field for field in ("trigger", "current_judgment", "review_trigger") if not _has_real_value(attrs.get(field))]
            if conditional_missing:
                errors.append(f"Applicability contract failed: {title} conditional status missing {', '.join(conditional_missing)}")
        if status == "not_applicable":
            basis = attrs.get("basis", "")
            source = attrs.get("source", "")
            if re.search(r"^(?:N/?A|暂无|本期不做|本期不适用)$", basis, re.I) or not _has_real_value(basis):
                errors.append(f"Applicability contract failed: {title} not_applicable requires factual basis")
            if not _has_real_value(source) or source.lower() in {"n/a", "na", "暂无"}:
                errors.append(f"Applicability contract failed: {title} not_applicable requires a source citation")
        if not reviewable:
            warnings.append(f"Applicability contract pending review for {title}")


def _validate_governance_leak(meta: dict[str, str], text: str, errors: list[str]) -> None:
    """Reader-facing v8 must not expose process/audit chapters as PRD top levels.

    Governance material (self-review, RTM, Clarifications, provenance, quality
    records, version summaries, upstream verbatim mirrors) lives in the manifest
    and project-side review/audit carriers.  A top-level chapter with one of the
    GOVERNANCE_LEAK_KEYWORDS signals that process content leaked into the
    reader-facing product spec.
    """
    if meta.get("reader_contract_version") != "2":
        return
    stripped = _strip_source_blocks(text)
    leaky: list[str] = []
    for match in re.finditer(r"^##\s+(?:\d+\.\s*)?(.+?)\s*$", stripped, re.MULTILINE):
        title = _norm(match.group(1)).lower()
        for keyword in GOVERNANCE_LEAK_KEYWORDS:
            if keyword in title:
                leaky.append(match.group(1).strip())
                break
    if leaky:
        errors.append(
            "Governance leak: reader-facing v8 PRD must not carry process/audit "
            "chapters: " + ", ".join(leaky[:6])
            + ". Keep them in prd-assembly-manifest.json, 99-review/, and .audit/."
        )


def _required_headings(meta: dict) -> list[str]:
    """按 prd_structure_version / process_tier 分叉必含章节列表。"""
    version = meta.get("prd_structure_version", "7")
    if version != "8":
        return REQUIRED_HEADINGS_V7  # 缺省/非 8 = 存量 v7 契约（REQ-001 等冻结）
    tier = meta.get("process_tier", "L2").upper()
    if meta.get("reader_contract_version") != "2":
        if tier == "L1":
            return REQUIRED_HEADINGS_V8_LEGACY_L1
        return REQUIRED_HEADINGS_V8_LEGACY_L2
    if tier in {"L0", "L1"}:
        return REQUIRED_HEADINGS_V8_L1
    return REQUIRED_HEADINGS_V8_L2


# Upstream work_item IDs that must be confirmed per tier.  Kept in sync with
# workflow-registry.json schema_version 7 membership (L2 = 15, L1 = 9).
# A REQ whose tier upstreams were created before the schema-7 upgrade fails
# D5.2 until the new upstream artifacts are produced and confirmed — this is a
# real governance state, not a validation bug, and must not be hidden.
UPSTREAM_WORK_ITEMS = [
    "feasibility-analysis",     # FA
    "project-background-goal",  # G
    "project-scope",            # PS
    "user-journey",             # UJ
    "user-stories",             # US
    "feature-list",             # ST → FEA
    "functional-flow",           # FUN
    "page-design",              # PD
    "interaction-rules",         # IX
    "business-rules",           # BR
    "field-rules",              # FR
    "validation-rules",         # VL
    "state-machine",            # SM
    "exception-handling",       # EX
    "acceptance-criteria",       # AC
]

# L1 标准档：9 个上游 work_item（page-design/interaction-rules/field-rules/
# validation-rules/state-machine/exception-handling 不参与）；L2 完整档 = 全 15。
UPSTREAM_WORK_ITEMS_L1 = [
    "feasibility-analysis",     # FA
    "project-background-goal",  # G
    "project-scope",            # PS
    "user-journey",             # UJ
    "user-stories",             # US
    "feature-list",             # ST → FEA
    "functional-flow",          # FUN
    "business-rules",           # BR
    "acceptance-criteria",      # AC
]

# L0 has a compact evidence chain, not a reduced final-PRD contract.  Its
# single confirmed mini-prd is deterministically projected into that contract.
UPSTREAM_WORK_ITEMS_L0 = ["mini-prd"]


def _upstream_work_items(meta: dict) -> list[str]:
    tier = meta.get("process_tier", "L2").upper()
    if tier == "L0":
        return UPSTREAM_WORK_ITEMS_L0
    if tier == "L1":
        return UPSTREAM_WORK_ITEMS_L1
    return UPSTREAM_WORK_ITEMS

PENDING = ("待确认",)
VALID_STATUSES = {
    "draft", "needs_user_input", "conditional_review",
    "ready_for_human_review", "confirmed",
    "superseded", "legacy_unverified", "simulated",
}


def _norm(h: str) -> str:
    return re.sub(r"\s*（[^）]*）\s*$", "", re.sub(r"^\d+\.\s*", "", h).strip()).strip()


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


def _source_block_ranges(text: str) -> list[tuple[int, int]]:
    """Return [(start, end), ...] of all source-block bodies (between the HTML
    comments). Used to exclude embedded upstream content from PRD-level heading
    extraction, since their `##` headings belong to upstream artifacts, not to
    this PRD's own chapter structure.
    """
    pat = re.compile(
        r"<!--\s*source:\s*work_item=[^\s>]+"
        r"\s+artifact_id=[^\s>]+"
        r"\s+sha256=[0-9a-fA-F]{64}\s*-->"
        r"(.*?)"
        r"<!--\s*/source\s*-->",
        re.DOTALL,
    )
    return [(m.start(1), m.end(1)) for m in pat.finditer(text)]


# R&D-review-v1 hard-standard checklist (advisory). Distilled from
# `prd-reviewer` (B1) and `pm-master` (G3). Defined in
# references/prd-scoring-rubric.md §4.1. Each item maps to one advisory
# warning; never escalates to an error.
_RD_HARD_STDS = (
    ("component",  "组件级需求",        "页面/接口/数据模型分层清晰"),
    ("state",      "状态机",           "涉及状态变更的字段须文档化"),
    ("tracking",   "埋点方案",         "事件名 + 触发时机 + 上报参数 + 分析维度"),
    ("contract",   "接口契约",         "调用方 / 返回结构 / 错误码"),
    ("acceptance", "验收标准",         "Given/When/Then + 量化阈值"),
    ("fallback",   "异常降级",         "至少 1 条失败路径 + 兜底"),
    ("rollout",    "灰度与回滚",       "适用范围 + 比例 + 监控 + 回滚触发条件"),
)


def _rd_review_hard_stds(text: str) -> list[str]:
    """Probe the PRD body for the 7 R&D-review-v1 hard-standard signals.

    Returns a list of advisory warnings (one per missing signal). Signals are
    matched by section heading keywords inside the source-block-stripped body.
    Detection uses _strip_source_blocks so headings embedded inside upstream
    bodies don't pollute the probe.
    """
    stripped = _strip_source_blocks(text)
    headings = [
        _norm(m.group(1))
        for m in re.finditer(r"^#{1,4}\s+(.+?)\s*$", stripped, re.MULTILINE)
    ]
    blob = stripped
    warnings: list[str] = []
    for key, title, hint in _RD_HARD_STDS:
        keyword_hits = [
            h for h in headings
            if key in h or title in h or hint.split()[0] in h
        ]
        keyword_in_body = (
            title in blob or hint.split()[0] in blob or key in blob
        )
        if not keyword_hits and not keyword_in_body:
            warnings.append(
                f"R&D-review-v1 hard standard advisory: missing signal "
                f"`{title}` ({hint}). See references/prd-scoring-rubric.md §4.1. "
                f"This is advisory only — does not block current gate."
            )
    return warnings


def _strip_source_blocks(text: str) -> str:
    """Replace source-block bodies with blank lines so heading regex skips them
    while preserving line numbers for error messages."""
    out = list(text)
    for start, end in _source_block_ranges(text):
        for i in range(start, end):
            if out[i] == "\n":
                continue
            out[i] = " "
    return "".join(out)


def _sections(text: str) -> dict[str, str]:
    """Top-level PRD sections (## headings), excluding headings inside source blocks."""
    stripped = _strip_source_blocks(text)
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", stripped, re.MULTILINE))
    result: dict[str, str] = {}
    for i, match in enumerate(matches):
        title = _norm(match.group(1))
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        result[title] = text[match.end():end].strip()
    return result


def _l1_embedded_l2only_rule_ids(business_rules: str) -> list[str]:
    """Return real L2-only rule IDs (VL/STATE/EX) that L1 must route to L2.

    Only the rule-ID column or the rule-description column counts as *defining*
    an L2-only rule.  Trace-anchor references in later table columns (追溯锚点 /
    来源) point at existing upstream behavior and are not new L2-only rules —
    treating them as violations would break every confirmed L1 PRD whose BR
    table cites EX-xx anchors from the functional-flow artifact.
    """
    ids: set[str] = set()
    for line in business_rules.splitlines():
        if line.lstrip().startswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 2:
                if re.fullmatch(r"(?:VL|STATE|EX)-\d+", cells[0]):
                    ids.add(cells[0])
                ids.update(re.findall(r"\b(?:VL|STATE|EX)-\d+\b", cells[1]))
                continue
        ids.update(re.findall(r"\b(?:VL|STATE|EX)-\d+\b", line))
    return sorted(ids)


def _l1_state_machine_signals(business_rules: str) -> list[str]:
    """Return structured state-machine signals that L1 must route to L2.

    Ordinary business conditions such as a time threshold are valid in L1. This
    deliberately looks for an explicit state model or a state-transition table,
    rather than treating every occurrence of the word "状态" as a violation.
    """
    # Applicability metadata is governance, not a business state model. Exclude
    # comments before scanning so words such as "状态" and "守卫" in the
    # review-trigger field cannot cause a false upgrade.
    business_rules = re.sub(r"<!--.*?-->", "", business_rules, flags=re.DOTALL)
    signals: list[str] = []
    if re.search(r"状态机|状态枚举|状态转移", business_rules):
        signals.append("explicit state-model terminology")

    for line in business_rules.splitlines():
        normalized = line.lower()
        has_state = "状态" in line or "state" in normalized
        has_event = "触发事件" in line or "事件" in line or "event" in normalized
        has_transition = any(
            marker in line or marker in normalized
            for marker in ("守卫", "转移", "终止状态", "目标状态", "下一状态", "起始状态", "guard")
        )
        if has_state and has_event and has_transition:
            signals.append("state-transition table")
            break
    return signals


def _meaningful(body: str) -> bool:
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    body = re.sub(r"[`*_>#|~-]", "", body)
    body = re.sub(r"\s+", "", body)
    return bool(body) and not re.fullmatch(r"(待确认|暂无|无|N/?A|TBD|见上游|详见上游)+", body, re.I)


def _declared_hash(meta: dict[str, str]) -> tuple[str | None, str | None]:
    for key in ("content_sha256", "artifact_content_sha256", "manifest_sha256"):
        if key in meta:
            return key, meta[key].strip()
    return None, None


def _hash_without_declaration(text: str, key: str) -> str:
    cleaned = re.sub(rf"(?m)^{re.escape(key)}\s*:.*$\n?", "", text)
    return artifact_content_hash(cleaned)


def _req_dir_for(path: Path) -> Path | None:
    for parent in (path.parent, *path.parents):
        if (parent / "99-review").is_dir():
            return parent
    return None


def _artifact_body(text: str) -> str:
    """Return the Markdown payload after optional YAML frontmatter."""
    return re.sub(r"\A(?:<!--.*?-->\s*)?---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL).strip()


def _safe_source_path(req_dir: Path, raw_path: str) -> Path | None:
    """Resolve a manifest path without allowing it to escape the REQ root."""
    candidate = (req_dir / raw_path).resolve()
    try:
        candidate.relative_to(req_dir.resolve())
    except ValueError:
        return None
    return candidate


def _source_block(text: str, work_item: str, artifact_id: str) -> tuple[str, str] | None:
    pattern = re.compile(
        r"<!--\s*source:\s*work_item=" + re.escape(work_item)
        + r"\s+artifact_id=" + re.escape(artifact_id)
        + r"\s+sha256=([0-9a-fA-F]{64})\s*-->\s*(.*?)\s*<!--\s*/source\s*-->",
        re.DOTALL,
    )
    match = pattern.search(text)
    return (match.group(1).lower(), match.group(2).strip()) if match else None


def _validate_assembly_manifest(path: Path, text: str, meta: dict[str, str],
                                errors: list[str], warnings: list[str]) -> None:
    """Validate v8 provenance sidecar without requiring copied source bodies."""
    reader_v8 = meta.get("prd_structure_version") == "8" and meta.get("reader_contract_version") == "2"
    req_dir = _req_dir_for(path)
    if not req_dir or meta.get("prd_structure_version") != "8":
        return
    if reader_v8:
        manifest_path = path.parent / "prd-assembly-manifest.json"
        if not manifest_path.is_file():
            errors.append("Assembly manifest failed: reader-facing v8 requires 003-prd-output/prd-assembly-manifest.json")
            return
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Assembly manifest failed: cannot parse manifest: {exc}")
            return
        tier = meta.get("process_tier", "L2").upper()
        expected = _upstream_work_items(meta)
        if manifest.get("schema_version") != 2 or manifest.get("process_tier", "").upper() != tier:
            errors.append("Assembly manifest failed: reader-facing v8 requires schema_version=2 and matching process_tier")
        sources = manifest.get("sources")
        if not isinstance(sources, list):
            errors.append("Assembly manifest failed: sources must be a list")
            return
        by_item = {source.get("work_item"): source for source in sources if isinstance(source, dict)}
        missing = [item for item in expected if item not in by_item]
        unexpected = [item for item in by_item if item not in expected]
        if missing:
            # Controlled legacy fallback (option B): a REQ created before the
            # schema-7 upstream split legitimately lacks the new upstreams; the
            # projection records this in the manifest and PRD frontmatter.  This
            # is tolerated for drafts only — the D5.2 gate still requires the
            # full tier set before any ready_for_human_review/confirmed state.
            if meta.get("legacy_fallback") == "true" and manifest.get("legacy_fallback") is True:
                warnings.append(
                    "Assembly manifest legacy_fallback: missing tier sources: "
                    + ", ".join(missing)
                    + " — produce the missing upstreams and reflow before human approval."
                )
            else:
                errors.append("Assembly manifest failed: missing tier sources: " + ", ".join(missing))
        if unexpected:
            errors.append("Assembly manifest failed: out-of-tier sources: " + ", ".join(str(item) for item in unexpected))
        for work_item in expected:
            source = by_item.get(work_item)
            if not isinstance(source, dict):
                continue
            required = ("artifact_id", "path", "status", "content_sha256", "target_sections", "selectors")
            absent = [field for field in required if not source.get(field)]
            if absent:
                errors.append(f"Assembly manifest failed: {work_item} missing fields: {', '.join(absent)}")
                continue
            source_path = _safe_source_path(req_dir, source["path"])
            if source_path is None or not source_path.is_file():
                errors.append(f"Assembly manifest failed: {work_item} source path is missing or escapes REQ: {source['path']}")
                continue
            source_text = source_path.read_text(encoding="utf-8")
            source_meta = parse_frontmatter(source_text)
            if source["status"] != "confirmed" or source_meta.get("status") != "confirmed":
                errors.append(f"Assembly manifest failed: {work_item} must be confirmed")
            if source_meta.get("artifact_id") != source["artifact_id"]:
                errors.append(f"Assembly manifest failed: {work_item} artifact_id does not match source frontmatter")
            if source["content_sha256"].lower() != artifact_content_hash(source_text).lower():
                errors.append(f"Assembly manifest failed: {work_item} content_sha256 does not match source file")
            if not isinstance(source["target_sections"], list) or not source["target_sections"]:
                errors.append(f"Assembly manifest failed: {work_item} needs non-empty target_sections")
            if not isinstance(source["selectors"], list) or not source["selectors"]:
                errors.append(f"Assembly manifest failed: {work_item} needs non-empty selectors")
        return
    manifest_path = path.parent / "prd-assembly-manifest.json"
    if not manifest_path.is_file():
        errors.append("Assembly manifest failed: v8 PRD in a REQ directory requires 003-prd-output/prd-assembly-manifest.json")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Assembly manifest failed: cannot parse manifest: {exc}")
        return
    tier = meta.get("process_tier", "L2").upper()
    expected = _upstream_work_items(meta)
    if manifest.get("schema_version") not in {1, 2} or manifest.get("process_tier", "").upper() != tier:
        errors.append("Assembly manifest failed: schema_version 1/2 and matching process_tier are required")
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        errors.append("Assembly manifest failed: sources must be a list")
        return
    by_item: dict[str, dict] = {}
    for source in sources:
        if not isinstance(source, dict) or not isinstance(source.get("work_item"), str):
            errors.append("Assembly manifest failed: every source needs a work_item object field")
            continue
        work_item = source["work_item"]
        if work_item in by_item:
            errors.append(f"Assembly manifest failed: duplicate source work_item {work_item}")
        by_item[work_item] = source
    missing = [item for item in expected if item not in by_item]
    unexpected = [item for item in by_item if item not in expected]
    if missing:
        errors.append("Assembly manifest failed: missing tier sources: " + ", ".join(missing))
    if unexpected:
        errors.append("Assembly manifest failed: out-of-tier sources: " + ", ".join(unexpected))
    for work_item in expected:
        source = by_item.get(work_item)
        if not source:
            continue
        required = ("artifact_id", "path", "status", "content_sha256")
        absent = [field for field in required if not source.get(field)]
        if absent:
            errors.append(f"Assembly manifest failed: {work_item} missing fields: {', '.join(absent)}")
            continue
        if source["status"] != "confirmed":
            errors.append(f"Assembly manifest failed: {work_item} must be confirmed")
            continue
        if not isinstance(source["path"], str) or not isinstance(source["artifact_id"], str):
            errors.append(f"Assembly manifest failed: {work_item} path and artifact_id must be strings")
            continue
        source_path = _safe_source_path(req_dir, source["path"])
        if source_path is None or not source_path.is_file():
            errors.append(f"Assembly manifest failed: {work_item} source path is missing or escapes REQ: {source['path']}")
            continue
        source_text = source_path.read_text(encoding="utf-8")
        source_meta = parse_frontmatter(source_text)
        actual_hash = artifact_content_hash(source_text)
        if source_meta.get("status") != "confirmed":
            errors.append(f"Assembly manifest failed: {work_item} source frontmatter is not confirmed")
        if source_meta.get("artifact_id") != source["artifact_id"]:
            errors.append(f"Assembly manifest failed: {work_item} artifact_id does not match source frontmatter")
        if source.get("content_sha256", "").lower() != actual_hash.lower():
            errors.append(f"Assembly manifest failed: {work_item} content_sha256 does not match source file")
        block = _source_block(text, work_item, source["artifact_id"])
        if block is None:
            errors.append(f"Assembly manifest failed: {work_item} has no matching source block in PRD")
            continue
        block_hash, block_body = block
        if block_hash != actual_hash.lower():
            errors.append(f"Assembly manifest failed: {work_item} source block hash does not match source file")
        if block_body != _artifact_body(source_text):
            errors.append(f"Assembly manifest failed: {work_item} source block content was changed after assembly")


def validate(path: Path) -> dict[str, object]:
    errors, warnings = [], []
    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}

    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    status = meta.get("status")

    missing = sorted(REQUIRED_FRONTMATTER - meta.keys())
    if missing:
        errors.append(f"Missing frontmatter fields: {', '.join(missing)}")

    if status and status not in VALID_STATUSES:
        errors.append(f"Invalid status '{status}'")

    # Source blocks (embedded upstream content) must not contribute to
    # PRD-level heading extraction: their `##` headings belong to upstream
    # artifacts, not to this PRD's own chapter structure.
    stripped_for_headings = _strip_source_blocks(text)
    headings = [_norm(m.group(1)) for m in re.finditer(r"^##\s+(.+?)\s*$", stripped_for_headings, re.MULTILINE)]
    required_headings = _required_headings(meta)
    missing_h = [h for h in required_headings if _norm(h) not in headings]
    if missing_h:
        errors.append(f"Missing required headings: {', '.join(missing_h)}")

    sections = _sections(text)
    _validate_applicability_contract(text, meta, errors, warnings)
    _validate_governance_leak(meta, text, errors)

    is_reader_v8 = (
        meta.get("prd_structure_version") == "8"
        and meta.get("reader_contract_version") == "2"
    )
    is_l1 = is_reader_v8 and meta.get("process_tier", "L2").upper() == "L1"
    if is_l1:
        # L1 has no L2-only upstreams. Real L2-only IDs or state-machine
        # structure must trigger an upgrade instead of being hidden in §9.1.
        business_rules = sections.get("业务规则", "")
        l2only_rules = _l1_embedded_l2only_rule_ids(business_rules)
        if l2only_rules:
            errors.append(
                "L1 PRD must not embed real L2-only rules (VL/STATE/EX): "
                + ", ".join(sorted(set(l2only_rules)))
                + ". Record applicability in intake-decision.md and upgrade the REQ to L2."
            )
        state_machine_signals = _l1_state_machine_signals(business_rules)
        if state_machine_signals:
            errors.append(
                "L1 PRD must not model L2-only state-machine behavior: "
                + ", ".join(state_machine_signals)
                + ". Record the applicability evidence in intake-decision.md and upgrade the REQ to L2."
            )
    required_nonempty = [h for h in required_headings if h in sections and not _meaningful(sections[h])]
    if required_nonempty:
        errors.append(
            "Meaningful-content gate failed: empty or placeholder sections: "
            + ", ".join(required_nonempty)
        )

    # Every declared upstream ID must be a real trace token; placeholder or
    # malformed IDs make the PRD impossible to audit back to source artifacts.
    upstream_value = meta.get("upstream_artifact_ids", "")
    upstream_ids = re.findall(r"\b(?:G|BG|UJ|US|FEA|FUN|FL|FF|PD|IX|BR|VL|STATE|SM|EX|AC|PRD|MP|SRC)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b", upstream_value)
    if status in {"ready_for_human_review", "confirmed"} and not upstream_ids:
        errors.append("Source-trace gate failed: upstream_artifact_ids must contain at least one valid artifact ID")
    if upstream_value and re.search(r"(?:待确认|TBD|TODO|XXX|\[\])", upstream_value, re.I):
        errors.append("Source-trace gate failed: upstream_artifact_ids contains unresolved placeholder")

    declared_key, declared = _declared_hash(meta)
    if declared_key and not re.fullmatch(r"[0-9a-fA-F]{64}", declared or ""):
        errors.append(f"Hash declaration invalid: {declared_key} must be 64 hexadecimal characters")
    elif declared_key and declared:
        computed = _hash_without_declaration(text, declared_key)
        if declared.lower() != computed.lower():
            errors.append(f"Hash integrity failed: {declared_key} does not match canonical artifact content (expected {computed[:12]}…)")

    # RTM is a project-side audit artifact in v8. Legacy/v7 remains strict.
    if meta.get("prd_structure_version") != "8" and "RTM" not in text and "需求追溯矩阵" not in text:
        errors.append("No RTM (Requirements Traceability Matrix) found")

    _validate_assembly_manifest(path, text, meta, errors, warnings)

    if status == "confirmed":
        unresolved = [k for k in ("business_fact_owner", "goal_decision_owner", "reviewer", "confirmed_at")
                      if meta.get(k, "") in {"", *PENDING}]
        if unresolved:
            errors.append("Confirmed artifact has unresolved confirmation fields: " + ", ".join(unresolved))

    if any(p in text for p in PENDING) and status == "confirmed":
        body = re.sub(r"^##\s+\d+\.\s*[^\n]*$", "", text, flags=re.MULTILINE)
        if any(p in body for p in PENDING):
            warnings.append("Confirmed PRD still contains 待确认 markers in body")

    # Semantic red flags specific to PRD assembly
    if status == "ready_for_human_review" or status == "confirmed":
        # Check all upstream work_items are confirmed（L1 只查 7 个，L2 查全 12）
        tier = meta.get("process_tier", "L2").upper()
        upstream_items = _upstream_work_items(meta)
        upstream_statuses = meta.get("upstream_work_item_statuses", "")
        missing_upstream = []
        for wi in upstream_items:
            if wi not in upstream_statuses:
                missing_upstream.append(wi)
        if missing_upstream:
            errors.append(
                f"PRD DoD D5.2 failed: missing upstream work_item confirmation for: "
                f"{', '.join(missing_upstream)} (need all {len(upstream_items)} tier-confirmed before PRD)"
            )
        # Q6：L1 档不得混入 L2-only 上游（page-design/interaction-rules/validation-rules/
        # state-machine/exception-handling）——错配说明装配走错档位。
        if tier == "L1":
            unexpected = [
                wi for wi in UPSTREAM_WORK_ITEMS
                if wi not in UPSTREAM_WORK_ITEMS_L1 and wi in upstream_statuses
            ]
            if unexpected:
                errors.append(
                    f"PRD DoD D5.2 failed: L1 PRD must not declare L2-only upstream work_items: "
                    f"{', '.join(unexpected)}"
                )

        # Forward traceability chain G→UJ→US→ST→FEA→FUN→PD→IX→BR→VL→SM→EX→AC
        # Combined upstream-artifact-id regex (used by consistency_check E1 and shown above
        # as 12 separate re.search lines for per-prefix diagnostics). Keep both in sync.
        # Note: this is the "scope" regex — covers all upstream + prd (PRD- for self).
        # The E1 consistency check looks for `(BG|UJ|US|FEA|FL|PD|IX|BR|VL|SM|EX|PRD)-\d+(?:-\d+)?`
        # in source code, so keep the literal pattern below (capturing group, no \b anchors).
        UPSTREAM_ID_PATTERN = re.compile(
            r"(BG|UJ|US|FEA|FL|PD|IX|BR|VL|STATE|EX|AC|PRD)-\d+(?:-\d+)?"
        )
        forward_chain_ids = {
            "G": bool(re.search(r"\bG-\d+\b", text)),           # project-background-goal
            "UJ": bool(re.search(r"\bUJ-\d+\b", text)),         # user-journey
            "US": bool(re.search(r"\bUS-\d+\b", text)),         # user-stories
            "ST": bool(re.search(r"\bST-\d+\b", text)),         # user-stories
            "FEA": bool(re.search(r"\bFEA-\d+\b", text)),        # feature-list
            "FUN": bool(re.search(r"\b(FUN|FL|FEA)-\d+(?:-\d+)?\b", text)),  # functional-flow 节点实为 FEA 作用域（E2E-017 后无 FUN- 前缀）
            "PD": bool(re.search(r"\bPD-\d+\b", text)),         # page-design
            "IX": bool(re.search(r"\bIX-\d+\b", text)),        # interaction-rules
            "BR": bool(re.search(r"\bBR-\d+\b", text)),         # business-rules
            "VL": bool(re.search(r"\bVL-\d+\b", text)),        # validation-rules
            "SM": bool(re.search(r"\bSM-\d+\b|\bSTATE-\d+\b", text)),  # state-machine
            "EX": bool(re.search(r"\bEX-\d+\b", text)),        # exception-handling
            "AC": bool(re.search(r"\bAC-\d+\b", text)),         # acceptance-criteria
        }
        missing_trace_ids = [k for k, v in forward_chain_ids.items() if not v]
        # L0 is intentionally a one-source evidence chain.  Its canonical PRD
        # has the same chapter contract, but it cannot invent upstream IDs that
        # do not exist; the mini-prd source block and manifest are its trace.
        if meta.get("process_tier", "L2").upper() == "L0":
            missing_trace_ids = []
        # L1 标准档无 L2-only 上游（PD/IX/VL/SM/EX）→ 相应 ID 槽位豁免（不告警）。
        # PRD 汇总章节仍完整，只是这些能力以「本期不适用」承载、无真实 ID。
        if meta.get("process_tier", "L2").upper() == "L1":
            for exempt in L1_EXEMPT_TRACE_PREFIXES:
                missing_trace_ids = [k for k in missing_trace_ids if k != exempt]
        if missing_trace_ids:
            warnings.append(
                f"Forward traceability incomplete: missing IDs for: {', '.join(missing_trace_ids)}. "
                "Expected chain: G→UJ→US→ST→FEA→FUN→PD→IX→BR→VL→SM→EX→AC"
            )

    # Reader-facing v8 does not carry a duplicate RTM. The trace report is
    # generated from upstream artifacts plus the manifest in 99-review/.

        # Check for new content not in upstream
        new_content_markers = ["新增需求", "补充功能", "额外建议"]
        if any(m in text for m in new_content_markers):
            warnings.append(
                "Semantic: PRD contains '新增需求/补充功能/额外建议' markers; "
                "PRD assembly should only aggregate, not introduce new requirements"
            )

        # Content-density gate: a reader-facing PRD must contain substantive
        # behavior/rules/acceptance content, but no longer needs verbatim source
        # blocks. A pointer-only section remains invalid.  This gate applies to
        # reader-facing v8 only: legacy v8/v7 artifacts legitimately pair
        # "详见上游" pointers with embedded source blocks until reflow.
        if is_reader_v8:
            pointer_refs = re.findall(
                r"(?:详见|内容见)\s*[`\[]?\s*[A-Za-z][A-Za-z0-9_\-]{0,40}", text
            )
            if pointer_refs:
                uniq = list(dict.fromkeys(pointer_refs))
                errors.append(
                    "Content-density gate failed: PRD delegates content via upstream "
                    f"pointers ({', '.join(uniq[:6])}) instead of stating the behavior, "
                    "rule, or acceptance condition in the final PRD."
                )
        reader_body = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        if not any(_meaningful(sections.get(name, "")) for name in required_headings):
            errors.append("Meaningful-content gate failed: reader-facing PRD has no substantive product content")

        # R&D-review-v1 hard standards (蒸馏自 B1 prd-reviewer + G3 pm-master,
        # 完整定义见 references/prd-scoring-rubric.md §4.1). This is advisory
        # only — failures append warnings, never errors — so legacy fixtures and
        # in-progress drafts remain valid.
        if status in {"ready_for_human_review", "confirmed"}:
            rnp_warnings = _rd_review_hard_stds(text)
            warnings.extend(rnp_warnings)

    # If an external append-only anchor exists, verify its chain and this PRD's
    # latest row. Legacy fixtures without an anchor remain valid.
    # B2 fix: the per-artifact anchor check is enforced only once the PRD is
    # `confirmed` — the anchor row is written by pipeline.py review (approve),
    # so requiring it at `ready_for_human_review` created a deadlock (gate
    # blocked approval before the anchor could ever be recorded).  The chain
    # integrity check still runs for every status.
    req_dir = _req_dir_for(path)
    if req_dir and hash_anchor and (req_dir / "99-review" / hash_anchor.ANCHOR_FILENAME).is_file():
        chain = hash_anchor.verify_anchor_chain(req_dir)
        if not chain["ok"]:
            errors.extend(f"Hash anchor chain failed: {item}" for item in chain["issues"])
        elif status == "confirmed" and meta.get("reviewer"):
            current_hash = artifact_content_hash(text)
            rel = path.relative_to(req_dir).as_posix()
            check = hash_anchor.verify_artifact_anchored(req_dir, rel, current_hash, meta["reviewer"])
            if not check.get("anchored"):
                errors.append("Hash anchor integrity failed: latest external anchor does not match artifact hash/reviewer")

    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "issues": _make_issues(errors, warnings, path)}


_PRD_ERROR_RULES = [
    ("Missing frontmatter fields:", "prd.missing_frontmatter"),
    ("Invalid status", "prd.invalid_status"),
    ("Missing required headings:", "prd.missing_headings"),
    ("Governance leak:", "prd.governance_leak"),
    ("L1 PRD must not embed real L2-only", "prd.l1_embedded_l2only_rules"),
    ("L1 PRD must not model L2-only state-machine behavior:", "prd.l1_state_machine_bypass"),
    ("No RTM", "prd.missing_rtm"),
    ("Confirmed artifact has unresolved confirmation fields:", "prd.unresolved_confirmation"),
    ("PRD DoD D5.2 failed:", "prd.d52_missing_upstream"),
    ("Content-density gate failed:", "prd.pointer_only_content"),
    ("Meaningful-content gate failed:", "prd.empty_content"),
    ("Source-trace gate failed:", "prd.source_trace"),
    ("Hash declaration invalid:", "prd.hash_format"),
    ("Hash integrity failed:", "prd.hash_mismatch"),
    ("Hash anchor", "prd.hash_anchor"),
    ("Assembly manifest failed:", "prd.assembly_manifest"),
]

_PRD_WARNING_RULES = [
    ("Confirmed PRD still contains 待确认 markers", "prd.pending_markers_in_confirmed"),
    ("Forward traceability incomplete", "prd.forward_trace_incomplete"),
    ("PRD contains", "prd.new_content_markers"),
]


def _check_id(msg: str, rules: list[tuple[str, str]], fallback: str) -> str:
    for needle, check_id in rules:
        if needle in msg:
            return check_id
    return fallback


def _make_issues(errors: list[str], warnings: list[str], path: Path) -> list[dict]:
    """双轨制：errors/warnings 保持字符串列表，issues 为 make_issue 统一 dict。"""
    issues: list[dict] = []
    for e in errors:
        issues.append(make_issue(
            severity="CRITICAL",
            check_id=_check_id(e, _PRD_ERROR_RULES, "prd.structural"),
            family=SKILL_ID,
            location=str(path),
            message=e,
        ))
    for w in warnings:
        issues.append(make_issue(
            severity="MEDIUM",
            check_id=_check_id(w, _PRD_WARNING_RULES, "prd.semantic"),
            family=SKILL_ID,
            location=str(path),
            message=w,
            blocking=False,
        ))
    return issues


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path)
    p.add_argument("--json", action="store_true", dest="j")
    a = p.parse_args()
    r = validate(a.artifact)
    if a.j:
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
