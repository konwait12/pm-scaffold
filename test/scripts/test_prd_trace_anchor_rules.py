#!/usr/bin/env python3
"""Regression tests for semantically valid PRD trace anchors."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "scripts"))
import property_check


def _validator(skill: str):
    path = ROOT / "src" / "stages" / "002-product-requirements" / "skills" / skill / "scripts" / "validate_artifact.py"
    spec = importlib.util.spec_from_file_location(f"validate_{skill.replace('-', '_')}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class TraceAnchorValidatorTest(unittest.TestCase):
    def _validate(self, skill: str, row: str) -> list[str]:
        body = """---
artifact_id: TEST-001
status: draft
---

# Test

| ID | 内容 | 锚点 |
|---|---|---|
""" + row + "\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / f"{skill}.md"
            path.write_text(body, encoding="utf-8")
            return _validator(skill).validate(path)["errors"]

    def test_feature_anchor_is_valid_without_fun(self) -> None:
        for skill, row in (
            ("business-rules", "| BR-001 | 登录前必须同意隐私声明 | FEA-001 |"),
            ("validation-rules", "| VL-001 | 邮箱格式 | FEA-001 |"),
            ("exception-handling", "| EX-001 | 认证服务超时后保留草稿 | FEA-001 |"),
            ("state-machine", "| STATE-001 | 订单待确认 | FEA-001 |"),
        ):
            self.assertFalse(any("is orphan" in error for error in self._validate(skill, row)), skill)

    def test_global_scope_is_valid_without_feature_anchor(self) -> None:
        for skill, row in (
            ("business-rules", "| BR-001 | 所有用户数据变更必须留存审计记录 | scope: GLOBAL |"),
            ("validation-rules", "| VL-001 | 所有导入文件必须限制大小 | 适用范围: 全局 |"),
            ("exception-handling", "| EX-001 | 审计服务不可用时进入降级队列 | scope: GLOBAL |"),
            ("state-machine", "| STATE-001 | 全局数据保留生命周期 | 适用范围: 全局 |"),
        ):
            self.assertFalse(any("is orphan" in error for error in self._validate(skill, row)), skill)

    def test_missing_anchor_is_rejected(self) -> None:
        errors = self._validate("validation-rules", "| VL-001 | 邮箱格式 | 必须符合格式 |")
        self.assertTrue(any("is orphan" in error for error in errors))


class RiskAdaptedCoverageTest(unittest.TestCase):
    def test_single_valid_rule_and_ac_is_not_a_numeric_defect(self) -> None:
        text = """# Test
## 业务规则
| BR ID | 内容 | 锚点 |
|---|---|---|
| BR-001 | 用户必须确认删除 | FUN-001 |
## 验收依据
| AC ID | 内容 | 锚点 |
|---|---|---|
| AC-001 | Given 用户确认删除, when 提交, then 删除成功 | FUN-001 |
"""
        issues = property_check.check_rule_density(text)
        self.assertFalse(any(issue["severity"] in {"HIGH", "CRITICAL", "MEDIUM"} for issue in issues))

    def test_feature_anchor_pairs_validation_and_acceptance(self) -> None:
        text = """# Test
## 校验规则
| VL ID | 内容 | 锚点 |
|---|---|---|
| VL-001 | 金额非负 | FEA-001 |
## 验收依据
| AC ID | 内容 | 锚点 |
|---|---|---|
| AC-001 | Given 负数金额, when 提交, then 拒绝 | FEA-001 |
"""
        issues = property_check.check_vl_ac_pairing(text)
        self.assertFalse(any(issue["severity"] == "MEDIUM" for issue in issues))


if __name__ == "__main__":
    unittest.main()
