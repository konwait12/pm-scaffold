from __future__ import annotations
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = PROJECT_ROOT / "src" / "stages" / "001-business-requirements" / "skills" / "project-background-goal" / "scripts" / "validate_artifact.py"
SPEC = importlib.util.spec_from_file_location("validate_artifact", SCRIPT_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
def main_doc(project_type: str) -> str:
    current = {
        "重构": "之前通过 H5 和人工核销完成预约，流程长且转化率只有 47%。之后希望把流程整合为更短的统一业务流程。",
        "从 0 到 1": "目前线下人工完成活动邀约和登记：\n1. 运营通过微信发送活动信息。\n2. 客人电话回复是否参加。\n3. 运营用表格登记并在现场人工核对。",
        "迭代": "现有项目已经支持活动详情，本次只补充与活动地点相关的业务信息。",
    }[project_type]
    background = "现有预约方式影响客人完成业务，业务方希望改善结果。" if project_type != "迭代" else "客服经常需要向客人重复说明活动地点，导致沟通成本增加。"
    goal = "预约完成率从 47% 提升到 60%，并把平均完成时间从 6 分钟降到 2 分钟。" if project_type == "重构" else ("建立可复用的活动邀约、登记和核对业务过程，并能通过完成率和人工耗时判断是否成功。" if project_type == "从 0 到 1" else "增加活动地点后，客人能在详情中直接获得准确地点，减少重复咨询。")
    return f"""---
artifact_id: BG-TEST
version: v0.1
status: draft
project_type: {project_type}
owner: PM
created_at: 2026-08-28
updated_at: 2026-08-28
---
# 项目背景与目标
## 一句话摘要
为相关角色解决业务问题并获得可判断的结果。
## 项目背景
{background}
## 当前现状与已有做法
{current}
## 核心问题与证据
现状造成效率或体验问题，会议记录和业务数据提供了依据。
## 目标与成功判断
{goal}
## 角色与干系人
业务负责人、运营人员和受影响的客人。
## 约束与依赖
需要业务负责人确认时间窗口和数据口径。
## 边界与非目标
不在本次背景目标中定义页面、字段或技术实现。
## 待确认与风险
数据口径和最终目标值仍需 PM 确认。
## 参考资料
2026-08-27 项目阶段性成果讨论会议纪要；业务现状说明。
"""
GOVERNANCE = """---
artifact_id: BG-TEST
main_artifact: background-goal.md
main_version: v0.1
main_sha256: {hash_value}
status: draft
---
# 项目背景与目标治理伴随文件
## 类型判断与 PM 选择
- AI 判断：重构，依据现状已有系统
- PM 选择：重构
## 主张来源与知识状态
| 主张 | 知识状态 | 来源或依据 | 主文档落点 |
|---|---|---|---|
| 现状 | FACT | 会议纪要 | 当前现状与已有做法 |
## 澄清记录
暂无阻断问题。
## AI Audit
- Audit 结论：通过
## PM 确认与变更
- 待 PM 确认。
"""
class ValidateArtifactTest(unittest.TestCase):
    def write_pair(self, directory: Path, project_type: str = "重构") -> Path:
        main = directory / "background-goal.md"
        text = main_doc(project_type)
        main.write_text(text, encoding="utf-8")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        (directory / "background-goal.governance.md").write_text(GOVERNANCE.format(hash_value=digest), encoding="utf-8")
        return main
    def test_three_project_types_pass(self) -> None:
        for project_type in ("重构", "从 0 到 1", "迭代"):
            with self.subTest(project_type=project_type), tempfile.TemporaryDirectory() as temp_dir:
                result = VALIDATOR.validate(self.write_pair(Path(temp_dir), project_type))
                self.assertTrue(result["ok"], result)
    def test_main_document_rejects_machine_governance(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            main = self.write_pair(directory)
            main.write_text(main.read_text(encoding="utf-8") + "\n## Constitution Compliance\n", encoding="utf-8")
            result = VALIDATOR.validate(main)
            self.assertFalse(result["ok"])
            self.assertTrue(any("machine governance" in error for error in result["errors"]))
    def test_missing_companion_is_warning_for_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            main = Path(temp_dir) / "background-goal.md"
            main.write_text(main_doc("迭代"), encoding="utf-8")
            result = VALIDATOR.validate(main)
            self.assertTrue(result["ok"], result)
            self.assertTrue(any("Companion file" in warning for warning in result["warnings"]))
    def test_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            main = self.write_pair(Path(temp_dir))
            main.write_text(main.read_text(encoding="utf-8").replace("47%", "48%"), encoding="utf-8")
            result = VALIDATOR.validate(main)
            self.assertFalse(result["ok"])
            self.assertTrue(any("main_sha256" in error for error in result["errors"]))
    def test_zero_to_one_requires_business_flow(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            main = self.write_pair(Path(temp_dir), "从 0 到 1")
            text = main.read_text(encoding="utf-8").replace("1. 运营通过微信发送活动信息。\n2. 客人电话回复是否参加。\n3. 运营用表格登记并在现场人工核对。", "目前没有系统。")
            main.write_text(text, encoding="utf-8")
            result = VALIDATOR.validate(main)
            self.assertFalse(result["ok"])
            self.assertTrue(any("业务流程" in error for error in result["errors"]))

    def test_001_requires_meeting_baseline_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            main = self.write_pair(directory)
            main.write_text(main.read_text(encoding="utf-8").replace("artifact_id: BG-TEST", "artifact_id: BG-001"), encoding="utf-8")
            governance = directory / "background-goal.governance.md"
            governance.write_text(governance.read_text(encoding="utf-8").replace("artifact_id: BG-TEST", "artifact_id: BG-001"), encoding="utf-8")
            result = VALIDATOR.validate(main)
            self.assertFalse(result["ok"])
            self.assertTrue(any("飞书会议原文" in error for error in result["errors"]))
if __name__ == "__main__":
    unittest.main()
