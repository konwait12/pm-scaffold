#!/usr/bin/env python3
"""Manifest provenance boundary tests for reader-facing v8 PRD assembly.

The reader-facing final PRD no longer embeds upstream source bodies.  Provenance
is proven by the ``prd-assembly-manifest.json`` sidecar: artifact IDs, paths,
confirmed status, content SHA-256, target_sections, and selectors.  The source
block remains a *legacy v8* compatibility carrier until controlled reflow.

Boundary rules pinned here:
  1. Legacy v8 source blocks still isolate their ``##`` headings and ``详见``
     pointers from PRD-level chapter extraction (backward compatibility).
  2. Reader v8 passes WITHOUT any source block when the manifest is complete.
  3. Reader v8 fails when a source file hash changes, the manifest misses
     selectors/target_sections, schema_version is wrong, or the tier mismatches.
  4. Reader v8 fails on top-level ``详见`` pointer delegation.
"""

import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
SKILL_SCRIPT = ROOT / "src/stages/003-prd-output/skills/prd-assembly/scripts/validate_artifact.py"
sys.path.insert(0, str(SKILL_SCRIPT.parent))
sys.path.insert(0, str(ROOT / "src" / "scripts"))

from workflow_registry import artifact_content_hash, work_items_for_tier  # noqa: E402

spec = importlib.util.spec_from_file_location("validate_artifact", SKILL_SCRIPT)
validate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_module)

LEGACY_UPSTREAM_BODY = (
    "# 项目背景与目标 · BG-202\n"
    "## 1. 目标\n"
    "- G-001：OAB 推送\n"
    "## 2. 现状与问题\n"
    "详见上游 OBS-001 报告\n"
)


def _write(content: str) -> Path:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        return Path(f.name)


def _legacy_l1_fm(*, status: str = "ready_for_human_review") -> str:
    return (
        "---\n"
        "artifact_id: PRD-T\n"
        "version: v0.1\n"
        f"status: {status}\n"
        "owner: x\nbusiness_fact_owner: x\ngoal_decision_owner: x\nreviewer: x\n"
        "created_at: 2026-08-20\nupdated_at: 2026-08-20\nconfirmed_at: \"\"\n"
        "prd_structure_version: \"8\"\n"
        "process_tier: \"L1\"\n"
        "issue_in_prd: false\n"
        'upstream_artifact_ids: ["BG-202"]\n'
        "upstream_work_item_statuses: \"feasibility-analysis project-background-goal project-scope user-journey user-stories feature-list functional-flow business-rules acceptance-criteria\"\n"
        "---\n"
    )


def _legacy_l1_body() -> str:
    digest = "0" * 64
    return (
        "## 1. 项目背景\n\n"
        f"<!-- source: work_item=project-background-goal artifact_id=BG-202 sha256={digest} -->\n"
        f"{LEGACY_UPSTREAM_BODY}\n"
        "<!-- /source -->\n\n"
        "## 2. 项目范围\n\nscope.\n\n"
        "## 3. 用户旅程\n\njourney.\n\n"
        "## 4. 用户故事\n\nstories.\n\n"
        "## 5. 功能清单\n\nfeatures.\n\n"
        "## 6. 功能流程\n\nflow.\n\n"
        "## 9. 业务规则\n\n### 9.1 计算与流程规则\n\nrules.\n\n"
        "## 10. 验收依据\n\nacceptance.\n\n"
        "## 需求追溯矩阵\n\n| G | S | F | F | A |\n|---|---|---|---|---|\n| G-1 | S-1 | F-1 | FF-1 | A-1 |\n\n"
        "## 自审记录（Constitution Compliance）\n\n| 原则 | 状态 | 备注 |\n|---|---|---|\n| ① | PASS | ok |\n"
    )


# --------------------------------------------------------------------------
# Legacy v8 compatibility: source blocks keep isolating upstream structure.
# --------------------------------------------------------------------------

def test_legacy_v8_embedded_headings_ignored():
    """Legacy v8: upstream ``##`` headings inside a source block must NOT count
    as PRD top-level sections."""
    result = validate_module.validate(_write(_legacy_l1_fm() + _legacy_l1_body()))
    assert result["ok"], f"Legacy v8 with embedded ## headings must PASS; got: {result.get('errors')}"


def test_legacy_v8_pointer_inside_source_block_allowed():
    """Legacy v8: ``详见`` inside a source block must not trip the pointer gate."""
    result = validate_module.validate(_write(_legacy_l1_fm() + _legacy_l1_body()))
    for err in result["errors"]:
        assert "Content-density gate failed" not in err, \
            f"Pointer inside source block wrongly flagged: {err}"


def test_legacy_v8_pointer_outside_source_block_ignored_for_legacy():
    """Legacy v8 keeps the old contract: a top-level ``详见`` pointer combined
    with a full source block is the legacy shape and stays valid until reflow."""
    body = _legacy_l1_body().replace(
        "## 10. 验收依据\n\nacceptance.",
        "## 10. 验收依据\n\n详细规则详见 BR-001\n\nacceptance.",
    )
    result = validate_module.validate(_write(_legacy_l1_fm() + body))
    assert result["ok"], f"Legacy v8 pointer pairing must remain compatible; got: {result.get('errors')}"


# --------------------------------------------------------------------------
# Reader v8 provenance: manifest is the single source of truth.
# --------------------------------------------------------------------------

def _build_reader_tree(*, omit_selectors: bool = False, omit_targets: bool = False,
                       schema_version: int = 2, tier_override: str | None = None,
                       tamper_index: int | None = None, pointer_leak: bool = False) -> Path:
    """Create a REQ tree: 99-review + 7 confirmed upstreams + reader PRD + manifest.

    Returns the PRD path.  No source block is embedded — the reader contract
    proves provenance exclusively through the manifest sidecar.
    """
    root = Path(tempfile.mkdtemp(prefix="prd-prov-"))
    (root / "99-review").mkdir(parents=True)
    prd_path = root / "003-prd-output/prd.md"
    prd_path.parent.mkdir(parents=True)

    fixture = (ROOT / "test/skills/prd-assembly/fixtures/prd-l1-ok.md").read_text(encoding="utf-8")
    fixture = fixture.replace('applicability_contract_version: "1"',
                              'applicability_contract_version: "1"\nreader_contract_version: "2"')
    fixture = fixture.replace("## 3. 用户旅程", "## 3. 用户与用户旅程")
    fixture = fixture.replace("## 4. 用户故事", "## 4. 用户故事与优先级")
    fixture = fixture.replace("## 10. 验收依据", "## 10. 验收标准")
    fixture = re.sub(r"\n## 11\. 按需章节\n.*\Z", "\n", fixture, flags=re.DOTALL)
    if pointer_leak:
        fixture = fixture.replace("G-001 目标：提升活动提醒触达率。", "规则详见 BR-001。")

    items = [item for item in work_items_for_tier("L1")
             if item["id"] != "prd-assembly"]
    sources = []
    for index, item in enumerate(items):
        artifact = root / item["artifact_dir"] / item["artifact_file"]
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact_id = f"SRC-{index + 1:03d}"
        source_text = (
            "---\nartifact_id: " + artifact_id + "\nversion: v1\nstatus: confirmed\n"
            "---\n# " + item["name"] + "\n\n确认内容 " + item["id"] + "。\n"
        )
        artifact.write_text(source_text, encoding="utf-8")
        digest = artifact_content_hash(source_text)
        rel = artifact.relative_to(root).as_posix()
        source = {"work_item": item["id"], "artifact_id": artifact_id, "path": rel,
                  "status": "confirmed", "content_sha256": digest,
                  "target_sections": ["§1-§10"], "selectors": [item["id"]]}
        if omit_selectors:
            source["selectors"] = []
        if omit_targets:
            source["target_sections"] = []
        sources.append(source)
    if tamper_index is not None:
        path = root / sources[tamper_index]["path"]
        path.write_text(path.read_text(encoding="utf-8") + "\n已篡改。\n", encoding="utf-8")
    manifest = {"schema_version": schema_version,
                "process_tier": tier_override or "L1",
                "sources": sources}
    prd_path.write_text(fixture, encoding="utf-8")
    (prd_path.parent / "prd-assembly-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return prd_path


def test_reader_v8_without_source_blocks_passes():
    """Reader v8 has no source block and no RTM/self-review; complete manifest
    is sufficient provenance."""
    prd_path = _build_reader_tree()
    result = validate_module.validate(prd_path)
    assert result["ok"], result["errors"]
    text = prd_path.read_text(encoding="utf-8")
    assert "<!-- source: work_item=" not in text
    assert "## 需求追溯矩阵" not in text
    assert "## 自审记录" not in text


def test_reader_v8_source_hash_change_fails():
    """Tampering with a confirmed upstream source file must be detected."""
    prd_path = _build_reader_tree(tamper_index=0)
    result = validate_module.validate(prd_path)
    assert not result["ok"]
    assert any("content_sha256 does not match source file" in e for e in result["errors"])


def test_reader_v8_missing_selectors_fails():
    prd_path = _build_reader_tree(omit_selectors=True)
    result = validate_module.validate(prd_path)
    assert not result["ok"]
    assert any("missing fields: " in e and "selectors" in e for e in result["errors"])


def test_reader_v8_missing_target_sections_fails():
    prd_path = _build_reader_tree(omit_targets=True)
    result = validate_module.validate(prd_path)
    assert not result["ok"]
    assert any("missing fields: " in e and "target_sections" in e for e in result["errors"])


def test_reader_v8_manifest_wrong_schema_fails():
    prd_path = _build_reader_tree(schema_version=1)
    result = validate_module.validate(prd_path)
    assert not result["ok"]
    assert any("schema_version=2" in e for e in result["errors"])


def test_reader_v8_manifest_wrong_tier_fails():
    prd_path = _build_reader_tree(tier_override="L2")
    result = validate_module.validate(prd_path)
    assert not result["ok"]
    assert any("matching process_tier" in e for e in result["errors"])


def test_reader_v8_pointer_delegation_fails():
    """Reader v8 must fail when a chapter delegates content via upstream pointers."""
    prd_path = _build_reader_tree(pointer_leak=True)
    result = validate_module.validate(prd_path)
    assert not result["ok"]
    assert any("Content-density gate failed" in e for e in result["errors"])


if __name__ == "__main__":
    import sys as _sys
    failed = []
    for fn_name in sorted(globals()):
        if fn_name.startswith("test_") and callable(globals()[fn_name]):
            try:
                globals()[fn_name]()
            except Exception as exc:
                failed.append((fn_name, str(exc)[:200]))
                print(f"FAIL {fn_name}: {type(exc).__name__}: {str(exc)[:120]}")
    if failed:
        _sys.exit(1)
    print("✅ all manifest provenance boundary tests pass")
