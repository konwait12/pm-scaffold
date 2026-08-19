#!/usr/bin/env python3
"""Unit tests for acceptance-criteria validate_artifact.py — 模糊词/无阈值 advisory 回归护栏（E2E-014）。

回归护栏目标：
  - 正向用例（ac-vague-language.md）命中 `ac.vague_language` 与 `ac.no_quantified_threshold`
    （MEDIUM / blocking=False），且 ok=True（advisory 不阻断 gate）。
  - 负向对照（ac-confirmed.md 基准 fixture）不应产生上述 advisory。
  - 防回归：advisory 的 warning 文本内嵌行预览（含 G-XXX 引用）时，不得被
    `missing_goal_ref` 的 "G-" 子串启发式吞并（历史误分类 bug 的护栏）。
"""

import importlib.util
import sys
from pathlib import Path

SKILL_SCRIPT = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "src/stages/002-product-requirements/skills/acceptance-criteria/scripts/validate_artifact.py"
)
sys.path.insert(0, str(SKILL_SCRIPT.parent))

spec = importlib.util.spec_from_file_location("validate_artifact", SKILL_SCRIPT)
validate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_module)

ADVISORY_CHECK_IDS = {"ac.vague_language", "ac.no_quantified_threshold"}

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def test_vague_fixture_emits_both_advisories():
    """空泛词 + 无量化阈值 fixture 必须同时命中两个 advisory，且不阻断 gate。"""
    fixture = FIXTURE_DIR / "ac-vague-language.md"
    assert fixture.is_file(), f"fixture missing: {fixture}"
    result = validate_module.validate(fixture)
    assert result["ok"], f"advisory 不应阻断 gate: {result.get('errors')}"

    check_ids = [i["check_id"] for i in result["issues"]]
    assert "ac.vague_language" in check_ids, (
        f"应命中 ac.vague_language; got check_ids={check_ids}"
    )
    assert "ac.no_quantified_threshold" in check_ids, (
        f"应命中 ac.no_quantified_threshold; got check_ids={check_ids}"
    )
    # 两个 advisory 都是 MEDIUM / blocking=False
    for issue in result["issues"]:
        if issue["check_id"] in ADVISORY_CHECK_IDS:
            assert issue["severity"] == "MEDIUM", issue
            assert issue["blocking"] is False, issue
    print("✅ test_vague_fixture_emits_both_advisories")


def test_no_threshold_count_matches_vague_rows():
    """AC-001~003（无阈值）命中 3 条 no_quantified_threshold；AC-004（已量化 P99≤500ms）为负向对照不应命中。"""
    fixture = FIXTURE_DIR / "ac-vague-language.md"
    result = validate_module.validate(fixture)
    check_ids = [i["check_id"] for i in result["issues"]]
    count = sum(1 for cid in check_ids if cid == "ac.no_quantified_threshold")
    assert count == 3, (
        f"无阈值行应为 3（AC-001/002/003），AC-004 不应命中; got count={count}"
    )
    print("✅ test_no_threshold_count_matches_vague_rows")


def test_vague_advisory_not_swallowed_by_goal_heuristic():
    """防回归：advisory warning 内嵌行预览（含 G-XXX）时不得被误分类为 missing_goal_ref。"""
    fixture = FIXTURE_DIR / "ac-vague-language.md"
    result = validate_module.validate(fixture)
    check_ids = [i["check_id"] for i in result["issues"]]
    assert "ac.missing_goal_ref" not in check_ids, (
        f"G- 子串启发式不得吞并 advisory; got check_ids={check_ids}"
    )
    print("✅ test_vague_advisory_not_swallowed_by_goal_heuristic")


def test_baseline_fixture_has_no_advisories():
    """负向对照：已量化的基准 fixture（ac-confirmed.md）不应产生任何 advisory / 误分类。"""
    fixture = FIXTURE_DIR / "ac-confirmed.md"
    assert fixture.is_file(), f"fixture missing: {fixture}"
    result = validate_module.validate(fixture)
    assert result["ok"], f"基准 fixture 应通过: {result.get('errors')}"
    check_ids = {i["check_id"] for i in result["issues"]}
    assert not check_ids.intersection(
        ADVISORY_CHECK_IDS | {"ac.missing_goal_ref"}
    ), f"基准 fixture 不应命中 advisory/误分类; got check_ids={check_ids}"
    print("✅ test_baseline_fixture_has_no_advisories")


if __name__ == "__main__":
    test_vague_fixture_emits_both_advisories()
    test_no_threshold_count_matches_vague_rows()
    test_vague_advisory_not_swallowed_by_goal_heuristic()
    test_baseline_fixture_has_no_advisories()
    print("\n4 tests passed.")
