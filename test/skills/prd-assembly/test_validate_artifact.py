#!/usr/bin/env python3
"""Unit tests for prd-assembly validate_artifact.py"""

import importlib.util
import re
import sys
import tempfile
from pathlib import Path

SKILL_SCRIPT = Path(__file__).resolve().parent.parent.parent.parent / "src/stages/003-prd-output/skills/prd-assembly/scripts/validate_artifact.py"
sys.path.insert(0, str(SKILL_SCRIPT.parent))

import importlib.util
spec = importlib.util.spec_from_file_location("validate_artifact", SKILL_SCRIPT)
validate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_module)


def test_positive_fixture_passes():
    fixture = Path(__file__).resolve().parent / "fixtures/hire-website-prd-confirmed.md"
    result = validate_module.validate(fixture)
    assert result["ok"], result.get("errors")


def test_missing_contract_fails():
    """File with missing frontmatter must fail."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write("# Just a title\n\nNo frontmatter.\n")
        tmp = f.name
    try:
        result = validate_module.validate(Path(tmp))
        assert not result["ok"], "Should fail: missing frontmatter"
        assert any("Missing frontmatter" in e for e in result["errors"])
        print("✅ test_missing_contract_fails")
    finally:
        Path(tmp).unlink()


def test_violation_fixture_emits_d52_error():
    """Violation fixture should fail D5.2 (missing upstream current IDs)."""
    fixture = Path(__file__).resolve().parent / "fixtures/prd-violation-missing-upstream.md"
    if not fixture.exists():
        print("⚠️  test_violation_fixture_emits_d52_error: fixture missing, skipped")
        return
    result = validate_module.validate(fixture)
    assert not result["ok"], "Violation fixture should fail D5.2"
    has_d52 = any("D5.2" in e for e in result["errors"])
    assert has_d52, f"Should emit D5.2 error; got: {result['errors']}"
    print("✅ test_violation_fixture_emits_d52_error")


def test_pointer_gate_fails():
    """Content-density gate (reader-facing v8): a PRD that delegates content via
    '详见 BR-001' pointers must FAIL.  Legacy v8/v7 keep the old behavior."""
    content = _reader_l1_content().replace(
        "G-001 目标：提升活动提醒触达率。",
        "规则详见 BR-001，流程详见 FF-001。",
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp = Path(f.name)
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"], "Pointer-delegated reader v8 PRD should FAIL content-density gate"
        assert any("Content-density gate failed" in e for e in result["errors"]), \
            f"Expected pointer gate error; got: {result['errors']}"
        print("✅ test_pointer_gate_fails")
    finally:
        tmp.unlink()


def test_l1_positive_fixture_passes():
    """L1 标准档 PRD：§7/§8/§9.2-§9.4 以「本期不适用 + 承接依据」从简承载、章节结构完整，应 PASS（V8_L1 分叉）。"""
    fixture = Path(__file__).resolve().parent / "fixtures/prd-l1-ok.md"
    result = validate_module.validate(fixture)
    assert result["ok"], f"L1 fixture should PASS; got: {result.get('errors')}"
    print("✅ test_l1_positive_fixture_passes")


def test_l1_violation_l2_only_upstream_fails():
    """L1 档声明 L2-only 上游（Q6 双查）必须 FAIL。"""
    fixture = Path(__file__).resolve().parent / "fixtures/prd-l1-violation-l2-only-upstream.md"
    result = validate_module.validate(fixture)
    assert not result["ok"], "L1 PRD 声明 L2-only 上游应 FAIL"
    has_q6 = any("L2-only upstream" in e for e in result["errors"])
    assert has_q6, f"Expected L2-only upstream error; got: {result['errors']}"
    print("✅ test_l1_violation_l2_only_upstream_fails")


def test_l1_optional_l2only_subsection_is_allowed():
    """Reader-facing L1 PRD omits unsupported L2-only depth instead of emitting an empty shell."""
    content = _reader_l1_content()
    content = content.replace("### 9.2 校验规则", "### 9.2 已省略的历史章节")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp = Path(f.name)
    try:
        result = validate_module.validate(tmp)
        assert result["ok"], result.get("errors")
    finally:
        tmp.unlink()


def test_l1_state_machine_in_business_rules_fails():
    """Reader-facing L1 must not hide an L2 state-machine design in §9.1."""
    content = _reader_l1_content().replace(
        "BR-001 活动开始前 24h 触发提醒（FEA-001）。",
        """BR-001 活动开始前 24h 触发提醒。

| 起始状态 | 触发事件 | 守卫条件 | 终止状态 |
| --- | --- | --- | --- |
| 草稿 | 提交 | 信息完整 | 已发布 |""",
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp = Path(f.name)
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("L1 PRD must not model L2-only state-machine behavior" in item for item in result["errors"])
    finally:
        tmp.unlink()


def test_reader_v8_l1_embedding_l2only_rule_fails():
    """Reader L1 must fail when a real L2-only rule ID (VL/STATE/EX) leaks in."""
    content = _reader_l1_content().replace(
        "BR-001 活动开始前 24h 触发提醒（FEA-001）。",
        "BR-001 活动开始前 24h 触发提醒；VL-001 字段长度校验见上游。",
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp = Path(f.name)
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("L1 PRD must not embed real L2-only" in item for item in result["errors"])
    finally:
        tmp.unlink()


def test_reader_v8_governance_leak_fails():
    """Reader-facing v8 must reject governance chapters in the PRD body."""
    content = _reader_l1_content() + (
        "\n## 12. 自审记录\n\n| 原则 | 状态 |\n|---|---|\n| ① | PASS |\n"
        "\n## 13. 需求追溯矩阵\n\n| G | AC |\n|---|---|\n| G-001 | AC-001 |\n"
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp = Path(f.name)
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Governance leak" in item for item in result["errors"]), \
            f"Expected governance leak error; got: {result['errors']}"
    finally:
        tmp.unlink()


def test_reader_v8_l1_without_l2_sections_passes():
    """Reader L1 with only the core sections (no page/interaction/state) passes."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(_reader_l1_content())
        tmp = Path(f.name)
    try:
        result = validate_module.validate(tmp)
        assert result["ok"], result.get("errors")
    finally:
        tmp.unlink()


def _reader_l1_content(*, source: str = "[\"BG-001\", \"UJ-001\", \"US-001\", \"FL-001\", \"FF-001\", \"BR-001\", \"AC-001\"]", extra: str = "") -> str:
    """Reader-facing v8 L1 content derived from the legacy v8 L1 fixture.

    The legacy fixture keeps v8 chapter skeletons (§7 原型/UX, §8 交互规则,
    §9.2-§9.4).  The reader contract omits unsupported L2-only depth, so the
    derived content retitles the reader-core chapters and adds the
    reader_contract_version marker.
    """
    fixture = Path(__file__).resolve().parent / "fixtures/prd-l1-ok.md"
    text = fixture.read_text(encoding="utf-8")
    text = text.replace('upstream_artifact_ids: ["BG-001", "UJ-001", "US-001", "FL-001", "FF-001", "BR-001", "AC-001"]',
                        "upstream_artifact_ids: " + source)
    text = text.replace('prd_structure_version: "8"', 'prd_structure_version: "8"\nreader_contract_version: "2"')
    text = text.replace("## 3. 用户旅程", "## 3. 用户与用户旅程")
    text = text.replace("## 4. 用户故事\n", "## 4. 用户故事与优先级\n")
    text = text.replace("## 10. 验收依据", "## 10. 验收标准")
    # Schema-7 registry: L1 = 9 upstreams.  The legacy fixture declares 7;
    # align the frontmatter so D5.2 sees the full tier set.
    statuses = " ".join(validate_module.UPSTREAM_WORK_ITEMS_L1)
    text = re.sub(r'(?m)^upstream_work_item_statuses:.*$',
                  f'upstream_work_item_statuses: "{statuses}"', text)
    # The legacy fixture ends with governance chapters (按需章节 / RTM / 自审).
    # Reader-facing v8 keeps those in the manifest and 99-review, not in the PRD.
    text = re.sub(r"\n## 11\. 按需章节\n.*\Z", "\n", text, flags=re.DOTALL)
    return text.replace("---\n\n# PRD", extra + "---\n\n# PRD", 1)


def test_l1_placeholder_section_fails():
    content = _reader_l1_content().replace("G-001 目标：提升活动提醒触达率。", "待确认")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp = Path(f.name)
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Meaningful-content gate failed" in item for item in result["errors"])
    finally:
        tmp.unlink()


def test_l1_missing_source_fails():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(_reader_l1_content(source="[]"))
        tmp = Path(f.name)
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Source-trace gate failed" in item for item in result["errors"])
    finally:
        tmp.unlink()


def test_l1_declared_hash_tamper_fails():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(_reader_l1_content(extra="content_sha256: " + "0" * 64 + "\n"))
        tmp = Path(f.name)
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Hash integrity failed" in item for item in result["errors"])
    finally:
        tmp.unlink()


def _as_l2(content: str) -> str:
    """Upgrade reader L1 content to a full L2 declaration (15 upstreams)."""
    content = content.replace('process_tier: "L1"', 'process_tier: "L2"')
    content = content.replace(
        'upstream_artifact_ids: ["BG-001", "UJ-001", "US-001", "FL-001", "FF-001", "BR-001", "AC-001"]',
        'upstream_artifact_ids: ["FA-001", "BG-001", "PS-001", "UJ-001", "US-001", "FL-001", "FF-001", "PD-001", "IX-001", "BR-001", "FR-001", "VL-001", "STATE-001", "EX-001", "AC-001"]',
    )
    statuses = " ".join(validate_module.UPSTREAM_WORK_ITEMS)
    return re.sub(r'(?m)^upstream_work_item_statuses:.*$',
                  f'upstream_work_item_statuses: "{statuses}"', content)


def test_reader_v8_l2_requires_page_and_interaction():
    """Reader L2 must require 页面与体验 + 交互规则; reader L1 must not."""
    l2 = _as_l2(_reader_l1_content())
    l2 = l2.replace("## 10. 验收标准", "## 7. 页面与体验\n\n页面布局与字段说明。\n\n## 8. 交互规则\n\n交互行为与反馈。\n\n## 10. 验收标准")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(l2)
        tmp = Path(f.name)
    try:
        result = validate_module.validate(tmp)
        assert result["ok"], f"Reader L2 with page/interaction should PASS; got: {result['errors']}"
    finally:
        tmp.unlink()
    # L2 without page/interaction sections must FAIL.
    incomplete = _as_l2(_reader_l1_content())
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(incomplete)
        tmp = Path(f.name)
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Missing required headings" in item for item in result["errors"])
    finally:
        tmp.unlink()



if __name__ == "__main__":
    import sys
    failed = []
    for fn_name in [
        "test_positive_fixture_passes",
        "test_missing_contract_fails",
        "test_violation_fixture_emits_d52_error",
        "test_pointer_gate_fails",
        "test_l1_positive_fixture_passes",
        "test_l1_violation_l2_only_upstream_fails",
        "test_l1_optional_l2only_subsection_is_allowed",
        "test_l1_state_machine_in_business_rules_fails",
        "test_reader_v8_l1_embedding_l2only_rule_fails",
        "test_reader_v8_governance_leak_fails",
        "test_reader_v8_l1_without_l2_sections_passes",
        "test_l1_placeholder_section_fails",
        "test_l1_missing_source_fails",
        "test_l1_declared_hash_tamper_fails",
        "test_reader_v8_l2_requires_page_and_interaction",
    ]:
        fn = locals().get(fn_name) or globals().get(fn_name)
        if fn is None:
            continue
        try:
            fn()
        except Exception as exc:
            failed.append((fn_name, str(exc)[:200]))
            print(f"FAIL {fn_name}: {type(exc).__name__}: {str(exc)[:120]}")
    if failed:
        sys.exit(1)
