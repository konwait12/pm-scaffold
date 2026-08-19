#!/usr/bin/env python3
"""Unit tests for prd-assembly validate_artifact.py"""

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
    """Content-density gate: a PRD that delegates content via '详见 FD-001' pointers must FAIL."""
    all_upstream = ";".join(
        f"{wi}:confirmed" for wi in validate_module.UPSTREAM_WORK_ITEMS
    )
    headings = [
        "## 1. 项目背景与目标", "## 2. 业务角色、用户旅程与用户故事",
        "## 2. 用户旅程", "## 3. 用户故事与范围基线", "## 4. 功能清单",
        "## 5. 功能流程", "## 6. 页面设计", "## 7. 交互规则", "## 8. 业务规则",
        "## 9. 校验规则", "## 10. 状态变化", "## 11. 异常处理", "## 12. 验收依据",
        "## 需求追溯矩阵", "## 自审记录",
    ]
    fm = (
        "---\nartifact_id: PRD-T\nversion: v0.1\nstatus: ready_for_human_review\n"
        "owner: x\nbusiness_fact_owner: x\ngoal_decision_owner: x\nreviewer: x\n"
        "created_at: 2026-08-17\nupdated_at: 2026-08-17\nconfirmed_at: \"\"\n"
        f"upstream_work_item_statuses: \"{all_upstream}\"\n---\n"
    )
    body = "\n\n".join(headings) + "\n\n（规则列表：BR-001~BR-025，详见 FD-001\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(fm + body)
        tmp = f.name
    try:
        result = validate_module.validate(Path(tmp))
        assert not result["ok"], "Pointer-delegated PRD should FAIL content-density gate"
        assert any("Content-density gate failed" in e for e in result["errors"]), \
            f"Expected pointer gate error; got: {result['errors']}"
        print("✅ test_pointer_gate_fails")
    finally:
        Path(tmp).unlink()



if __name__ == "__main__":
    import sys
    failed = []
    for fn_name in [
        "test_positive_fixture_passes",
        "test_missing_contract_fails",
        "test_violation_fixture_emits_d52_error",
        "test_pointer_gate_fails",
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
