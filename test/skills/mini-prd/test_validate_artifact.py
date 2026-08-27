#!/usr/bin/env python3
"""Unit tests for mini-prd validate_artifact.py"""

import sys
import tempfile
from pathlib import Path

SKILL_SCRIPT = Path(__file__).resolve().parent.parent.parent.parent / "src/stages/000-minimal/skills/mini-prd/scripts/validate_artifact.py"
sys.path.insert(0, str(SKILL_SCRIPT.parent))

import importlib.util
spec = importlib.util.spec_from_file_location("validate_artifact", SKILL_SCRIPT)
validate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_module)


def _write(content: str) -> Path:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        return Path(f.name)


def test_positive_fixture_passes():
    fixture = Path(__file__).resolve().parent / "fixtures/mini-prd-ok.md"
    result = validate_module.validate(fixture)
    assert result["ok"], result.get("errors")


def test_missing_frontmatter_fails():
    tmp = _write("# Just a title\n\nNo frontmatter.\n")
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Missing frontmatter" in e for e in result["errors"])
    finally:
        tmp.unlink()


def test_missing_section_fails():
    tmp = _write(
        "---\nartifact_id: MP-001\nversion: v0.1\nstatus: draft\nowner: nova\n"
        "business_fact_owner: nova\ngoal_decision_owner: nova\nreviewer: nova\n"
        "created_at: 2026-08-20\nupdated_at: 2026-08-20\nconfirmed_at: ''\n"
        "process_tier: L0\nupstream_artifact_ids: []\n---\n"
        "## 1. 改什么\n内容\n## 2. 为什么\n内容\n"  # 缺 §3-§6
    )
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Missing required headings" in e for e in result["errors"])
    finally:
        tmp.unlink()


def test_wrong_tier_fails():
    tmp = _write(
        "---\nartifact_id: MP-001\nversion: v0.1\nstatus: draft\nowner: nova\n"
        "business_fact_owner: nova\ngoal_decision_owner: nova\nreviewer: nova\n"
        "created_at: 2026-08-20\nupdated_at: 2026-08-20\nconfirmed_at: ''\n"
        "process_tier: L2\nupstream_artifact_ids: []\n---\n"  # 错档位：L2
        "## 1. 改什么\n内容\n## 2. 为什么\n内容\n## 3. 影响范围\n内容\n"
        "## 4. 行为需求与验收\n内容\n## 5. 异常与边界\n内容\n## 6. 依赖与开口问题\n内容\n"
    )
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("只服务 L0 档位" in e for e in result["errors"])
    finally:
        tmp.unlink()


def test_pointer_reference_fails():
    tmp = _write(
        "---\nartifact_id: MP-001\nversion: v0.1\nstatus: draft\nowner: nova\n"
        "business_fact_owner: nova\ngoal_decision_owner: nova\nreviewer: nova\n"
        "created_at: 2026-08-20\nupdated_at: 2026-08-20\nconfirmed_at: ''\n"
        "process_tier: L0\nupstream_artifact_ids: []\n---\n"
        "## 1. 改什么\n内容\n## 2. 为什么\n内容\n## 3. 影响范围\n内容\n"
        "## 4. 行为需求与验收\n详见 BR-001\n## 5. 异常与边界\n内容\n## 6. 依赖与开口问题\n内容\n"
    )
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Content-density gate failed" in e for e in result["errors"])
    finally:
        tmp.unlink()


def _valid_mini_prd(*, status: str = "draft", source: str = "[\"SRC-001\"]", extra: str = "") -> str:
    return (
        "---\nartifact_id: MP-001\nversion: v0.1\nstatus: " + status + "\nowner: nova\n"
        "business_fact_owner: nova\ngoal_decision_owner: nova\nreviewer: nova\n"
        "created_at: 2026-08-20\nupdated_at: 2026-08-20\nconfirmed_at: ''\n"
        "process_tier: L0\nupstream_artifact_ids: " + source + "\n" + extra + "---\n"
        "## 1. 改什么\n将活动详情页的截止日期改为服务端配置。\n"
        "## 2. 为什么\n避免用户按错误日期报名。\n"
        "## 3. 影响范围\n仅影响活动详情页展示，无数据迁移。\n"
        "## 4. 行为需求与验收\nGiven 有截止日期，When 打开页面，Then 显示服务端日期。\n"
        "## 5. 异常与边界\n服务端无日期时显示待定文案。\n"
        "## 6. 依赖与开口问题\n依赖 RSVP 服务；时区格式待业务确认。\n"
    )


def test_placeholder_section_fails():
    content = _valid_mini_prd().replace("## 4. 行为需求与验收\nGiven 有截止日期，When 打开页面，Then 显示服务端日期。", "## 4. 行为需求与验收\n待确认")
    tmp = _write(content)
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Meaningful-content gate failed" in item for item in result["errors"])
    finally:
        tmp.unlink()


def test_review_ready_without_source_fails():
    tmp = _write(_valid_mini_prd(status="ready_for_human_review", source="[]"))
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Source-trace gate failed" in item for item in result["errors"])
    finally:
        tmp.unlink()


def test_declared_hash_tamper_fails():
    content = _valid_mini_prd(extra="content_sha256: " + "0" * 64 + "\n")
    tmp = _write(content)
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Hash integrity failed" in item for item in result["errors"])
    finally:
        tmp.unlink()


def test_declared_hash_format_fails():
    tmp = _write(_valid_mini_prd(extra="content_sha256: invalid\n"))
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("Hash declaration invalid" in item for item in result["errors"])
    finally:
        tmp.unlink()


def test_quality_contract_rejects_review_without_evidence():
    content = _valid_mini_prd(status="ready_for_human_review", extra='quality_contract_version: "1"\n')
    tmp = _write(content)
    try:
        result = validate_module.validate(tmp)
        assert not result["ok"]
        assert any("产品质量增强记录" in item for item in result["errors"])
    finally:
        tmp.unlink()


def test_legacy_mini_prd_remains_read_only_compatible():
    content = _valid_mini_prd(status="ready_for_human_review")
    tmp = _write(content)
    try:
        result = validate_module.validate(tmp)
        assert result["ok"], result.get("errors")
        assert any("产品质量增强记录" in item for item in result["warnings"])
    finally:
        tmp.unlink()
