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

REQUIRED_HEADINGS_V8_L2 = [
    "项目背景",
    "项目范围",
    "用户旅程",
    "用户故事",
    "功能清单",
    "功能流程",
    "原型/UX",
    "交互规则",
    "业务规则",
    "验收依据",
    "需求追溯矩阵",
    "自审记录",
]

REQUIRED_HEADINGS_V8_L1 = [
    "项目背景",
    "项目范围",
    "用户旅程",
    "用户故事",
    "功能清单",
    "功能流程",
    "业务规则",
    "验收依据",
    "需求追溯矩阵",
    "自审记录",
]

# These sub-sections correspond to upstream artifacts that do not exist in L1.
# L1 applicability is decided in intake-decision.md, not represented by invented
# "not applicable" prose in the final PRD.
L1_FORBIDDEN_L2_ONLY_SUBSECTIONS = {
    "校验规则",
    "状态变化",
    "异常处理",
}


def _required_headings(meta: dict) -> list[str]:
    """按 prd_structure_version / process_tier 分叉必含章节列表。"""
    version = meta.get("prd_structure_version", "7")
    if version != "8":
        return REQUIRED_HEADINGS_V7  # 缺省/非 8 = 存量 v7 契约（REQ-001 等冻结）
    tier = meta.get("process_tier", "L2").upper()
    if tier == "L1":
        return REQUIRED_HEADINGS_V8_L1
    return REQUIRED_HEADINGS_V8_L2


# 12 upstream work_item IDs that must be confirmed (L2 完整档全量)
UPSTREAM_WORK_ITEMS = [
    "project-background-goal",  # G
    "user-journey",             # UJ
    "user-stories",             # US
    "feature-list",             # ST → FEA
    "functional-flow",           # FUN
    "page-design",              # PD
    "interaction-rules",         # IX
    "business-rules",           # BR
    "validation-rules",         # VL
    "state-machine",            # SM
    "exception-handling",       # EX
    "acceptance-criteria",       # AC
]

# L1 标准档：仅 7 个上游 work_item（page-design/interaction-rules/validation-rules/
# state-machine/exception-handling 不参与）；L2 完整档 = 全 12。
UPSTREAM_WORK_ITEMS_L1 = [
    "project-background-goal",  # G
    "user-journey",             # UJ
    "user-stories",             # US
    "feature-list",             # ST → FEA
    "functional-flow",          # FUN
    "business-rules",           # BR
    "acceptance-criteria",      # AC
]


def _upstream_work_items(meta: dict) -> list[str]:
    tier = meta.get("process_tier", "L2").upper()
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


def _l1_state_machine_signals(business_rules: str) -> list[str]:
    """Return structured state-machine signals that L1 must route to L2.

    Ordinary business conditions such as a time threshold are valid in L1. This
    deliberately looks for an explicit state model or a state-transition table,
    rather than treating every occurrence of the word "状态" as a violation.
    """
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


def _validate_assembly_manifest(path: Path, text: str, meta: dict[str, str], errors: list[str]) -> None:
    """Verify v8 PRD source provenance when the artifact lives in a REQ tree.

    Legacy standalone fixtures remain structural tests. A v8 PRD placed in a real
    REQ directory, however, must carry an assembly manifest and exact source
    blocks so a manually summarised or post-assembly-modified PRD cannot pass.
    """
    req_dir = _req_dir_for(path)
    if not req_dir or meta.get("prd_structure_version") != "8":
        return
    if meta.get("status") not in {"ready_for_human_review", "confirmed"}:
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
    if manifest.get("schema_version") != 1 or manifest.get("process_tier", "").upper() != tier:
        errors.append("Assembly manifest failed: schema_version=1 and matching process_tier are required")
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
        required = ("artifact_id", "path", "status", "content_sha256", "target_section")
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

    if meta.get("prd_structure_version") == "8" and meta.get("process_tier", "L2").upper() == "L1":
        forbidden = [
            match.group(1).strip()
            for match in re.finditer(r"^###\s+(?:9\.[2-4]\s+)?(.+?)\s*$", text, re.MULTILINE)
            if _norm(match.group(1)) in L1_FORBIDDEN_L2_ONLY_SUBSECTIONS
        ]
        if forbidden:
            errors.append(
                "L1 PRD must omit L2-only business-rule sub-sections rather than mark them not applicable: "
                + ", ".join(forbidden)
            )

    sections = _sections(text)
    if meta.get("prd_structure_version") == "8" and meta.get("process_tier", "L2").upper() == "L1":
        state_machine_signals = _l1_state_machine_signals(sections.get("业务规则", ""))
        if state_machine_signals:
            errors.append(
                "L1 PRD must not model L2-only state-machine behavior in §9.1: "
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
    upstream_ids = re.findall(r"\b(?:G|BG|UJ|US|FEA|FUN|FL|FF|PD|IX|BR|VL|STATE|SM|EX|AC|PRD|SRC)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b", upstream_value)
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

    if "RTM" not in text and "需求追溯矩阵" not in text:
        errors.append("No RTM (Requirements Traceability Matrix) found")

    _validate_assembly_manifest(path, text, meta, errors)

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
        # L1 标准档无 page-design/interaction-rules 上游 → PD/IX 槽位豁免（不告警）
        if meta.get("process_tier", "L2").upper() == "L1":
            for exempt in ("PD", "IX"):
                missing_trace_ids = [k for k in missing_trace_ids if k != exempt]
        if missing_trace_ids:
            warnings.append(
                f"Forward traceability incomplete: missing IDs for: {', '.join(missing_trace_ids)}. "
                "Expected chain: G→UJ→US→ST→FEA→FUN→PD→IX→BR→VL→SM→EX→AC"
            )

        # RTM section checks
        rtm_section = re.search(
            r"^##\s+\d+\.\s*需求追溯矩阵\s*$(.*?)(?=^##\s+|\Z)",
            text, re.MULTILINE | re.DOTALL
        )
        if rtm_section:
            rtm_rows = [
                l for l in rtm_section.group(1).splitlines()
                if l.lstrip().startswith("|") and "---" not in l and "目标" not in l
            ]
            rtm_data = [r for r in rtm_rows if "待确认" not in r]
            if len(rtm_data) == 0:
                warnings.append("Semantic: RTM has no data rows; traceability matrix should be populated")
            # RTM column count: should have ≥6 columns for full chain
            header_match = re.search(r"^\|\s*([^|]+\|){5,}\s*[^|]+\|\s*$", rtm_section.group(1), re.MULTILINE)
            if header_match:
                col_count = header_match.group(0).count("|") - 1
                if col_count < 6:
                    warnings.append(
                        f"Semantic (G_CROSS): RTM header has {col_count} columns, expected ≥6 "
                        "for full traceability chain"
                    )

        # Check for new content not in upstream
        new_content_markers = ["新增需求", "补充功能", "额外建议"]
        if any(m in text for m in new_content_markers):
            warnings.append(
                "Semantic: PRD contains '新增需求/补充功能/额外建议' markers; "
                "PRD assembly should only aggregate, not introduce new requirements"
            )

        # Content-density gate: PRD must EMBED upstream content, not point to it.
        # Aggregation contract requires §1-§4/§6/§7 + BR/VL/SM/EX/AC tables to be
        # fully verbose-embedded. A single-line pointer like "详见 FD-001" delegates
        # content upstream, leaving the PRD thin and non-self-contained → FAIL.
        # However, "详见" inside an embedded source block IS legitimate
        # upstream-internal cross-reference, not a PRD-level pointer. Exclude
        # source-block bodies from this check.
        pointer_scan_text = _strip_source_blocks(text)
        pointer_refs = re.findall(
            r"(?:详见|内容见)\s*[`\[]?\s*[A-Za-z][A-Za-z0-9_\-]{0,40}", pointer_scan_text
        )
        if pointer_refs:
            uniq = list(dict.fromkeys(pointer_refs))
            errors.append(
                "Content-density gate failed: PRD delegates content via upstream "
                f"pointers ({', '.join(uniq[:6])}) instead of embedding it verbatim. "
                "Embed the full BR/VL/SM/EX/AC tables and story cards; do not write "
                "'详见 XX-XXX' pointers."
            )

        # R&D-review-v1 hard standards (蒸馏自 B1 prd-reviewer + G3 pm-master,
        # 完整定义见 references/prd-scoring-rubric.md §4.1). This is advisory
        # only — failures append warnings, never errors — so legacy fixtures and
        # in-progress drafts remain valid.
        if status in {"ready_for_human_review", "confirmed"}:
            rnp_warnings = _rd_review_hard_stds(text)
            warnings.extend(rnp_warnings)

    # If an external append-only anchor exists, verify its chain and this PRD's
    # latest row. Legacy fixtures without an anchor remain valid.
    req_dir = _req_dir_for(path)
    if req_dir and hash_anchor and (req_dir / "99-review" / hash_anchor.ANCHOR_FILENAME).is_file():
        chain = hash_anchor.verify_anchor_chain(req_dir)
        if not chain["ok"]:
            errors.extend(f"Hash anchor chain failed: {item}" for item in chain["issues"])
        elif status in {"ready_for_human_review", "confirmed"} and meta.get("reviewer"):
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
    ("L1 PRD must not model L2-only state-machine behavior in §9.1:", "prd.l1_state_machine_bypass"),
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
    ("RTM has no data rows", "prd.rtm_no_data"),
    ("RTM header has", "prd.rtm_column_count"),
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
