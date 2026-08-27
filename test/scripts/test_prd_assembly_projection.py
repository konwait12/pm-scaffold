#!/usr/bin/env python3
"""Unit tests for the deterministic L1/L2 PRD projection generator."""

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src" / "scripts"))

from workflow_registry import artifact_content_hash, work_items_for_tier  # noqa: E402

PROJ_SCRIPT = ROOT / "src/scripts/prd_assembly_projection.py"
spec = importlib.util.spec_from_file_location("prd_assembly_projection", PROJ_SCRIPT)
proj = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(proj)

TIER_UPSTREAMS = {
    "L1": [item["id"] for item in work_items_for_tier("L1") if item["id"] != "prd-assembly"],
    "L2": [item["id"] for item in work_items_for_tier("L2") if item["id"] != "prd-assembly"],
}

# Minimal upstream bodies with selectable business chapters + governance tails.
_UPSTREAM_BODIES = {
    "feasibility-analysis": (
        "## 1. 结论摘要\n\nFA-001 可行：技术/市场/投入产出通过。\n"
        "## 3. 技术可行性\n\n技术栈可复用，无阻塞。\n"
        "## 5. 风险评估\n\n风险：数据源延迟；缓解：缓存。\n"
    ),
    "project-background-goal": (
        "## 1. 需求来源与触发\n\n需求来自 SRC-001 业务诉求。\n"
        "## 5. 目标、未来期望与成功判断\n\nG-001 目标：提升转化率。\n"
        "## 8. 初步边界与非目标\n\nIn: 核心流程；Out: 跨端同步。\n"
        "## 11. 待确认问题\n\n| ID | 问题 | AI 判断 | 选项 | 决策人 | 阻断 | 延后 | 回写 |\n|---|---|---|---|---|---|---|---|\n"
        "| Q-001 | 基线数据待数据侧确认 | 推断 | A/B | 数据侧 | 否 | 低 | §5 |\n"
        "## 12. 来源追溯\n\nSRC-001。\n"
    ),
    "project-scope": (
        "## 1. 结论摘要\n\n基线 v1：In 2 / Out 1 / Deferred 0 / Conditional 0。\n"
        "## 2. In Scope（本期做）\n\nPS-001 核心流程（P0）。\n"
        "## 3. Out of Scope（本期不做）\n\nPS-002 跨端同步（后续版本）。\n"
    ),
    "user-journey": (
        "## 1. 业务生命周期分解\n\n生命周期：触达 → 预约 → 提醒。\n"
        "## 2. 用户旅程图\n\nUJ-001 旅程图。\n"
    ),
    "user-stories": (
        "## 1. 用户故事卡片\n\nST-001 用户想要提醒。\n"
        "## 2. 旅程→故事覆盖矩阵\n\n| 旅程 | 故事 |\n|---|---|\n| 提醒 | ST-001 |\n"
    ),
    "feature-list": (
        "## 1. 功能清单\n\nFEA-001 活动提醒（ST-001，P0）。\n"
        "## 2. 功能→故事追溯矩阵\n\n| FEA | ST |\n|---|---|\n| FEA-001 | ST-001 |\n"
    ),
    "functional-flow": (
        "## 2. 主流程（P0）\n\nFEA-001 主流程步骤。\n"
        "## 3. 分支流程\n\n分支：超时回退。\n"
    ),
    "page-design": (
        "## 2. 页面与步骤描述\n\nPD-001 页面布局与字段。\n"
    ),
    "interaction-rules": (
        "## 2. 交互规则\n\nIX-001 交互行为与反馈。\n"
    ),
    "business-rules": (
        "## 1. 业务规则\n\n| ID | 规则描述 | 类型 | 触发条件 | 约束/逻辑 | 追溯锚点 | 来源 |\n|---|---|---|---|---|---|---|\n"
        "| BR-001 | 24h 内不可预约 | 约束 | 选日期 | 置灰 | FEA-001 | SRC-001 |\n"
    ),
    "field-rules": (
        "## 1. 字段清单总览\n\n字段 3 个：手机号/日期/备注。\n"
        "## 2. 字段定义表\n\n| 字段 | 类型 | 必填 |\n|---|---|---|\n| 手机号 | string | 是 |\n"
    ),
    "validation-rules": (
        "## 1. 系统校验\n\nVL-001 手机号格式校验。\n"
        "## 2. 字段定义表\n\n| 字段 ID | 字段名 | 类型 | 必填 | 关联校验 |\n|---|---|---|---|---|\n| F-001 | 手机号 | string | 是 | VL-001 |\n"
    ),
    "state-machine": (
        "## 1. 状态定义\n\nSTATE-001 草稿/已确认/已取消。\n"
        "## 2. 状态转换表\n\n| 起始 | 事件 | 终止 |\n|---|---|---|\n| 草稿 | 提交 | 已确认 |\n"
    ),
    "exception-handling": (
        "## 1. 异常与失败处理\n\nEX-001 预约失败兜底。\n"
    ),
    "acceptance-criteria": (
        "## 1. 验收标准\n\nAC-001 Given…When…Then…。\n"
    ),
}


def _intake(tier: str) -> str:
    rows = [
        ("§1 项目背景", "required", "背景基线", "SRC-001", "pm", "2026-08-25", "当前判断：必须提供", "背景变化"),
        ("§2 项目范围", "required", "范围边界", "SRC-001", "pm", "2026-08-25", "当前判断：必须提供", "范围变化"),
        ("§3 用户旅程", "required", "角色路径", "SRC-001", "pm", "2026-08-25", "当前判断：必须说明受影响路径", "角色变化"),
        ("§4 用户故事", "required", "用户价值", "SRC-001", "pm", "2026-08-25", "当前判断：必须追溯用户价值", "目标变化"),
        ("§5 功能清单", "required", "功能范围", "SRC-001", "pm", "2026-08-25", "当前判断：必须提供可实施功能", "功能变化"),
        ("§6 功能流程", "required", "可观察行为", "SRC-001", "pm", "2026-08-25", "当前判断：必须提供可观察行为", "入口变化"),
        ("§7 原型/UX", "conditional", "页面结构变化", "SRC-001", "pm", "2026-08-25", "触发条件：页面结构变化；当前判断：待判断", "页面变化"),
        ("§8 交互规则", "conditional", "新交互", "SRC-001", "pm", "2026-08-25", "触发条件：新增交互；当前判断：待判断", "交互变化"),
        ("§9 业务规则", "required", "流程约束", "SRC-001", "pm", "2026-08-25", "当前判断：必须说明流程约束", "规则变化"),
        ("§9.1 计算与流程规则", "required", "适用业务规则", "SRC-001", "pm", "2026-08-25", "当前判断：必须提供", "规则变化"),
        ("§9.2 字段清单", "conditional", "字段属性", "SRC-001", "pm", "2026-08-25", "触发条件：新增字段或数据模型；当前判断：待判断", "字段变化"),
        ("§9.3 校验规则", "conditional", "字段校验", "SRC-001", "pm", "2026-08-25", "触发条件：新增字段校验；当前判断：待判断", "校验变化"),
        ("§9.4 状态变化", "conditional", "状态模型", "SRC-001", "pm", "2026-08-25", "触发条件：新增状态模型；当前判断：待判断", "状态变化"),
        ("§9.5 异常处理", "conditional", "失败语义", "SRC-001", "pm", "2026-08-25", "触发条件：新增失败语义；当前判断：待判断", "异常变化"),
        ("§10 验收依据", "required", "可判定验收", "SRC-001", "pm", "2026-08-25", "当前判断：必须可判定", "验收变化"),
        ("§11 按需章节", "conditional", "无独立来源", "SRC-001", "pm", "2026-08-25", "触发条件：新增按需来源；当前判断：暂无", "新增来源"),
    ]
    if tier == "L2":
        for row in rows:
            if row[0] in {"§7 原型/UX", "§8 交互规则", "§9.2 字段清单", "§9.3 校验规则", "§9.4 状态变化", "§9.5 异常处理"}:
                rows[rows.index(row)] = (row[0], "required", row[2], row[3], row[4], row[5],
                                         "当前判断：L2 必填", row[7])
    table = "\n".join("| " + " | ".join(row) + " |" for row in rows)
    return (
        "---\nartifact_id: INTAKE-T\nversion: \"v1\"\nstatus: ready_for_human_review\n"
        f"process_tier: {tier}\napplicability_contract_version: \"1\"\n---\n\n"
        "## 3. Canonical PRD 章节适用性矩阵\n\n"
        "| 章节 | 状态 | 依据 | 来源 | 决策人 | 决策时间 | 决策/判断 | 复审触发 |\n"
        "|---|---|---|---|---|---|---|---|\n" + table + "\n"
    )


class ProjectionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="prd-proj-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _tree(self, tier: str, *, confirmed: bool = True,
              missing_artifact: str | None = None,
              missing_artifacts: list[str] | None = None,
              legacy_intake: bool = False) -> Path:
        req = self.tmp / f"REQ-9{len(tier)}1-{tier.lower()}-tree"
        (req / "00-input").mkdir(parents=True)
        (req / "99-review").mkdir()
        if legacy_intake:
            # Pre-schema-7 intake labels: 校验规则/状态变化/异常处理 were the
            # sections that later split into 字段清单/校验/状态/异常.
            text = _intake(tier)
            text = text.replace("| §9.2 字段清单 |", "| §9.2 校验规则 |")
            text = text.replace("| §9.3 校验规则 |", "| §9.3 状态变化 |")
            text = text.replace("| §9.4 状态变化 |", "| §9.4 异常处理 |")
            text = text.replace("| §9.5 异常处理 |", "| §9.5 已删除占位 |")
            (req / "00-input/intake-decision.md").write_text(text, encoding="utf-8")
        else:
            (req / "00-input/intake-decision.md").write_text(_intake(tier), encoding="utf-8")
        skip = {missing_artifact} if missing_artifact else set(missing_artifacts or [])
        for item in work_items_for_tier(tier):
            if item["id"] == "prd-assembly":
                continue
            if item["id"] in skip:
                continue
            artifact = req / item["artifact_dir"] / item["artifact_file"]
            artifact.parent.mkdir(parents=True, exist_ok=True)
            status = "confirmed" if confirmed else "draft"
            body = _UPSTREAM_BODIES[item["id"]]
            artifact.write_text(
                f"---\nartifact_id: {item['id'].upper().replace('-', '')}-001\n"
                f"version: v1\nstatus: {status}\n---\n# {item['name']}\n\n{body}",
                encoding="utf-8",
            )
        return req

    def test_legacy_fallback_uses_old_carriers(self) -> None:
        """Option B: a schema-7-era REQ missing project-scope/field-rules falls
        back to BG boundary chapters (§2) and VL field tables (§9.2) instead of
        emitting pointers, and the manifest records the legacy state."""
        req = self._tree("L2", missing_artifacts=["project-scope", "field-rules"],
                         legacy_intake=True)
        prd, manifest = proj.build_projection(req)
        self.assertIn("## 2. 项目范围", prd)
        self.assertIn("In: 核心流程", prd)          # BG 初步边界与非目标 fallback
        self.assertIn("### 9.2 字段清单", prd)
        self.assertIn("F-001", prd)                  # VL 字段定义表 fallback
        self.assertIn("### 9.3 校验规则", prd)       # legacy 校验行拆分支撑
        self.assertTrue(manifest["legacy_fallback"])
        self.assertEqual(sorted(manifest["missing_work_items"]),
                         ["field-rules", "project-scope"])
        self.assertIn("legacy_fallback: true", prd)

    def test_no_fallback_when_all_upstreams_present(self) -> None:
        req = self._tree("L2")
        prd, manifest = proj.build_projection(req)
        self.assertNotIn("legacy_fallback: true", prd)
        self.assertNotIn("legacy_fallback", manifest)

    def test_l1_projection_reader_contract(self) -> None:
        req = self._tree("L1")
        prd, manifest = proj.build_projection(req)
        text = prd
        self.assertIn('reader_contract_version: "2"', text)
        self.assertIn('status: draft', text)
        self.assertIn("## 1. 项目背景", text)
        self.assertIn("## 9. 业务规则", text)
        self.assertIn("### 9.1 计算与流程规则", text)
        self.assertIn("## 10. 验收标准", text)
        # L1 must omit L2-only depth and governance chapters.
        self.assertNotIn("## 7. 页面与体验", text)
        self.assertNotIn("## 8. 交互规则", text)
        self.assertNotIn("### 9.2 字段清单", text)
        self.assertNotIn("### 9.3 校验规则", text)
        self.assertNotIn("### 9.4 状态变化", text)
        self.assertNotIn("### 9.5 异常处理与恢复", text)
        self.assertNotIn("## 自审记录", text)
        self.assertNotIn("## 需求追溯矩阵", text)
        self.assertNotIn("<!-- source: work_item=", text)
        self.assertNotIn("## 来源追溯", text)
        self.assertNotIn("## 版本变更摘要", text)
        # §11 keeps only real Q- rows, not DEC ledger rows.
        self.assertIn("| Q-001 |", text)
        self.assertNotIn("| DEC-", text)

    def test_l2_projection_includes_tier_only_sections(self) -> None:
        req = self._tree("L2")
        prd, manifest = proj.build_projection(req)
        for expected in ("## 7. 页面与体验", "## 8. 交互规则",
                         "### 9.2 字段清单", "### 9.3 校验规则", "### 9.4 状态变化", "### 9.5 异常处理与恢复"):
            self.assertIn(expected, prd)
        self.assertEqual(manifest["process_tier"], "L2")
        self.assertEqual(manifest["schema_version"], 2)
        self.assertEqual(len(manifest["sources"]), 15)

    def test_manifest_binds_selectors_and_hashes(self) -> None:
        req = self._tree("L1")
        _prd, manifest = proj.build_projection(req)
        self.assertEqual(manifest["schema_version"], 2)
        by_item = {s["work_item"]: s for s in manifest["sources"]}
        self.assertEqual(set(by_item), set(TIER_UPSTREAMS["L1"]))
        for source in manifest["sources"]:
            self.assertTrue(source["target_sections"])
            self.assertTrue(source["selectors"])
            self.assertEqual(source["status"], "confirmed")
            artifact = req / source["path"]
            self.assertTrue(artifact.is_file())
            self.assertEqual(source["content_sha256"],
                             artifact_content_hash(artifact.read_text(encoding="utf-8")))

    def test_unconfirmed_upstream_blocks(self) -> None:
        req = self._tree("L1", confirmed=False)
        with self.assertRaises(ValueError):
            proj.build_projection(req)

    def test_missing_upstream_blocks(self) -> None:
        req = self._tree("L1", missing_artifact="business-rules")
        with self.assertRaises(ValueError):
            proj.build_projection(req)

    def test_refuses_to_overwrite_confirmed_prd(self) -> None:
        req = self._tree("L1")
        output = req / "003-prd-output/prd.md"
        output.parent.mkdir(parents=True)
        output.write_text(
            "---\nartifact_id: PRD-T\nstatus: confirmed\n---\n# old\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            proj.write_draft(req, apply=True)

    def test_apply_writes_draft_when_not_confirmed(self) -> None:
        req = self._tree("L1")
        output = req / "003-prd-output/prd.md"
        output.parent.mkdir(parents=True)
        output.write_text(
            "---\nartifact_id: PRD-T\nstatus: superseded\n---\n# old\n", encoding="utf-8")
        result = proj.write_draft(req, apply=True)
        self.assertTrue(result["wrote"])
        self.assertEqual(proj.read_frontmatter(output).get("status"), "draft")
        manifest = json.loads((req / "003-prd-output/prd-assembly-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 2)

    def test_deterministic_output(self) -> None:
        req = self._tree("L2")
        first, m1 = proj.build_projection(req)
        second, m2 = proj.build_projection(req)
        self.assertEqual(first, second)
        self.assertEqual(m1, m2)


if __name__ == "__main__":
    unittest.main()
