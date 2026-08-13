#!/usr/bin/env python3
"""Unit tests for brainstorming validate_artifact.py — SCN candidate table, disposition four-value, write-back target."""

import sys
import tempfile
from pathlib import Path

SKILL_SCRIPT = Path(__file__).resolve().parent.parent.parent.parent / "src/support-skills/brainstorming/scripts/validate_artifact.py"
sys.path.insert(0, str(SKILL_SCRIPT.parent))

import importlib.util
spec = importlib.util.spec_from_file_location("validate_artifact", SKILL_SCRIPT)
validate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_module)

FRONTMATTER = (
    "---\n"
    "artifact_id: BS-TEST-001\n"
    "version: v0.1\n"
    "status: ready_for_human_review\n"
    "owner: 产品经理A（占位）\n"
    "reviewer: 业务方负责人B（占位）\n"
    "created_at: 2026-08-13\n"
    "updated_at: 2026-08-13\n"
    "confirmed_at: （授权人工 review 后填写）\n"
    "---\n\n"
)

BUNDLE = (
    "业务方代表A 提出客户邀约活动，名单约 500 人，邀约方式与内容未定义。"
    "人工处置确认：生命周期五阶段与三类角色纳入输入包；异常场景暂缓；渠道依赖待调研。"
)


def _mkdoc(disposition: str, writeback: str = "输入包 §生命周期线索", status: str = "ready_for_human_review") -> str:
    """A structurally complete brainstorming artifact; one SCN-001 candidate."""
    return (
        FRONTMATTER.replace("ready_for_human_review", status)
        + "# 头脑风暴输出\n\n"
        + "## 原始输入\n\n一句话想法：做客户邀约活动，名单约 500 人。\n\n"
        + "## 发散结果\n\n- 生命周期候选一条\n\n"
        + "## 候选清单（全部 AI_INFERENCE）\n\n"
        + "| Candidate ID | 发散维度 | Candidate | Evidence | Impact | 知识状态 |\n"
        + "|---|---|---|---|---|---|\n"
        + "| SCN-001 | lifecycle | 生命周期五阶段 | 原始想法原文仅提到邀约活动，为 AI 推断 | 为旅程与功能划分提供骨架 | AI_INFERENCE |\n\n"
        + "## 人工处置表\n\n"
        + "| Candidate ID | Role-Lifecycle | Candidate | Evidence | Impact | Human Disposition | Reason | Write-back Target |\n"
        + "|---|---|---|---|---|---|---|---|\n"
        + f"| SCN-001 | lifecycle | 生命周期五阶段 | 同候选表 SCN-001 | 旅程骨架 | {disposition} | 业务方代表A 确认 | {writeback} |\n\n"
        + "## 收敛后输入包\n\n"
        + BUNDLE + "\n\n"
        + "## 版本变更摘要\n\n- v0.1: 初稿\n"
    )


def test_confirmed_fixture_passes():
    """The positive fixture must pass the validator."""
    fixture = Path(__file__).resolve().parent / "fixtures/brainstorming-confirmed.md"
    result = validate_module.validate(fixture)
    assert result["ok"], f"Fixture should pass: {result.get('errors')}"
    print("✅ test_confirmed_fixture_passes")


def test_valid_dispositions_pass():
    """All four disposition values are accepted for a well-formed row."""
    for disposition in ("include", "exclude", "defer", "research"):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(_mkdoc(disposition))
            tmp = f.name
        try:
            result = validate_module.validate(Path(tmp))
            assert result["ok"], f"Disposition '{disposition}' should pass: {result.get('errors')}"
        finally:
            Path(tmp).unlink()
    print("✅ test_valid_dispositions_pass")


def test_invalid_disposition_rejected():
    """A disposition outside the four values must be rejected."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(_mkdoc("maybe"))
        tmp = f.name
    try:
        result = validate_module.validate(Path(tmp))
        assert not result["ok"], "Invalid disposition 'maybe' must be rejected"
        assert any("Invalid disposition" in e for e in result["errors"]), (
            f"Expected Invalid disposition error; got: {result['errors']}"
        )
    finally:
        Path(tmp).unlink()
    print("✅ test_invalid_disposition_rejected")


def test_include_without_writeback_rejected():
    """An include candidate without a non-placeholder Write-back Target must be rejected."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(_mkdoc("include", writeback="待填写"))
        tmp = f.name
    try:
        result = validate_module.validate(Path(tmp))
        assert not result["ok"], "Include candidate with placeholder write-back target must be rejected"
        assert any("Write-back Target" in e for e in result["errors"]), (
            f"Expected Write-back Target error; got: {result['errors']}"
        )
    finally:
        Path(tmp).unlink()
    print("✅ test_include_without_writeback_rejected")


def test_confirmed_status_rejected():
    """The brainstorming record must never reach status confirmed."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(_mkdoc("include", status="confirmed"))
        tmp = f.name
    try:
        result = validate_module.validate(Path(tmp))
        assert not result["ok"], "Status 'confirmed' must be rejected for the brainstorming record"
        assert any("confirmed" in e for e in result["errors"]), (
            f"Expected confirmed rejection error; got: {result['errors']}"
        )
    finally:
        Path(tmp).unlink()
    print("✅ test_confirmed_status_rejected")


if __name__ == "__main__":
    test_confirmed_fixture_passes()
    test_valid_dispositions_pass()
    test_invalid_disposition_rejected()
    test_include_without_writeback_rejected()
    test_confirmed_status_rejected()
    print("\n5 tests passed.")
