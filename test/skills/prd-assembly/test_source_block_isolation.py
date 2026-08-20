#!/usr/bin/env python3
"""Regression test for E2E-032: PRD source-block heading isolation.

v8 PRD embeds upstream artifact bodies inside `<!-- source: ... -->` HTML
comments. The validator must treat those embedded `##`/`###` headings as
upstream-internal, not as PRD-level chapter structure, and must not flag
`详见 XX-XXX` references that appear inside an embedded source block.
"""

import importlib.util
import sys
import tempfile
from pathlib import Path

SKILL_SCRIPT = Path(__file__).resolve().parent.parent.parent.parent / "src/stages/003-prd-output/skills/prd-assembly/scripts/validate_artifact.py"
sys.path.insert(0, str(SKILL_SCRIPT.parent))

spec = importlib.util.spec_from_file_location("validate_artifact", SKILL_SCRIPT)
validate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_module)

# Build a real upstream artifact body that contains `##` subheadings + a `详见`
# cross-reference. This emulates a source artifact with internal structure.
UPSTREAM_BODY = (
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


def _l1_fm(*, process_tier: str = "L1", status: str = "ready_for_human_review") -> str:
    return (
        "---\n"
        "artifact_id: PRD-T\n"
        "version: v0.1\n"
        f"status: {status}\n"
        "owner: x\nbusiness_fact_owner: x\ngoal_decision_owner: x\nreviewer: x\n"
        "created_at: 2026-08-20\nupdated_at: 2026-08-20\nconfirmed_at: \"\"\n"
        "prd_structure_version: \"8\"\n"
        f"process_tier: \"{process_tier}\"\n"
        "issue_in_prd: false\n"
        'upstream_artifact_ids: ["BG-202"]\n'
        "upstream_work_item_statuses: \"project-background-goal user-journey user-stories feature-list functional-flow business-rules acceptance-criteria\"\n"
        "---\n"
    )


def test_l1_headings_pass_when_source_block_contains_double_hash():
    """L1 PRD: chapters use `## 1. 项目背景` etc.; the embedded upstream body
    (between source comments) contains its own `##` subheadings which must NOT
    be counted as PRD top-level sections."""
    digest = "0" * 64
    body = (
        "## 1. 项目背景\n\n"
        f"<!-- source: work_item=project-background-goal artifact_id=BG-202 sha256={digest} -->\n"
        f"{UPSTREAM_BODY}\n"
        "<!-- /source -->\n\n"
        "## 2. 项目范围\n\n"
        "scope.\n\n"
        "## 3. 用户旅程\n\n"
        "journey.\n\n"
        "## 4. 用户故事\n\n"
        "stories.\n\n"
        "## 5. 功能清单\n\n"
        "features.\n\n"
        "## 6. 功能流程\n\n"
        "flow.\n\n"
        "## 9. 业务规则\n\n"
        "### 9.1 计算与流程规则\n\nrules.\n\n"
        "## 10. 验收依据\n\n"
        "acceptance.\n\n"
        "## 需求追溯矩阵\n\n"
        "| G | S | F | F | A |\n"
        "|---|---|---|---|---|\n"
        "| G-1 | S-1 | F-1 | FF-1 | A-1 |\n\n"
        "## 自审记录（Constitution Compliance）\n\n"
        "| 原则 | 状态 | 备注 |\n"
        "|---|---|---|\n"
        "| ① | PASS | ok |\n"
    )
    txt = _l1_fm() + body
    p = _write(txt)
    try:
        result = validate_module.validate(p)
        assert result["ok"], f"L1 with embedded ## headings must PASS; got: {result.get('errors')}"
    finally:
        p.unlink()


def test_详见_inside_source_block_not_flagged_as_pointer():
    """`详见 上游 OBS-001` appears inside the embedded source block. The
    content-density gate must NOT flag this as a PRD-level pointer."""
    digest = "0" * 64
    body = (
        "## 1. 项目背景\n\n"
        f"<!-- source: work_item=project-background-goal artifact_id=BG-202 sha256={digest} -->\n"
        f"{UPSTREAM_BODY}\n"
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
    txt = _l1_fm() + body
    p = _write(txt)
    try:
        result = validate_module.validate(p)
        for err in result["errors"]:
            assert "Content-density gate failed" not in err, \
                f"Pointer inside source block wrongly flagged: {err}"
    finally:
        p.unlink()


def test_详见_outside_source_block_still_flagged():
    """Sanity: a `详见` outside any source block must still trigger the gate."""
    digest = "0" * 64
    body = (
        "## 1. 项目背景\n\n"
        f"<!-- source: work_item=project-background-goal artifact_id=BG-202 sha256={digest} -->\n"
        f"{UPSTREAM_BODY}\n"
        "<!-- /source -->\n\n"
        "## 2. 项目范围\n\nscope.\n\n"
        "## 3. 用户旅程\n\njourney.\n\n"
        "## 4. 用户故事\n\nstories.\n\n"
        "## 5. 功能清单\n\nfeatures.\n\n"
        "## 6. 功能流程\n\nflow.\n\n"
        "## 9. 业务规则\n\n### 9.1 计算与流程规则\n\nrules.\n\n"
        "## 10. 验收依据\n\n"
        "详细规则详见 BR-001\n\n"   # ← top-level pointer, must FAIL
        "## 需求追溯矩阵\n\n| G | S | F | F | A |\n|---|---|---|---|---|\n| G-1 | S-1 | F-1 | FF-1 | A-1 |\n\n"
        "## 自审记录（Constitution Compliance）\n\n| 原则 | 状态 | 备注 |\n|---|---|---|\n| ① | PASS | ok |\n"
    )
    txt = _l1_fm() + body
    p = _write(txt)
    try:
        result = validate_module.validate(p)
        assert any("Content-density gate failed" in e for e in result["errors"]), \
            "Top-level `详见` must still be flagged"
    finally:
        p.unlink()


if __name__ == "__main__":
    test_l1_headings_pass_when_source_block_contains_double_hash()
    test_详见_inside_source_block_not_flagged_as_pointer()
    test_详见_outside_source_block_still_flagged()
    print("✅ all E2E-032 regression tests pass")