#!/usr/bin/env python3

from __future__ import annotations

import importlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "src/scripts"
sys.path.insert(0, str(SCRIPTS))

import migrate_layout_v2
import traceability_check
import workflow_registry


class WorkflowRuntimeTest(unittest.TestCase):
    def write_reviewer_registry(self, req: Path) -> None:
        path = req / "00-input/authorized-reviewers.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"reviewers": [{
            "id": "USR-001", "name": "Real Reviewer", "roles": ["business_owner"]
        }]}), encoding="utf-8")

    def test_registry_paths_and_order(self) -> None:
        items = workflow_registry.work_items()
        self.assertEqual([item["order"] for item in items if item["order"] <= 5], [1, 2, 3, 4, 5])  # main 5 work items
        self.assertGreaterEqual(len({item["id"] for item in items}), 5)  # 5 main + N sub-skills
        for item in items:
            self.assertTrue((ROOT / item["skill_path"] / "SKILL.md").is_file())
            self.assertTrue((ROOT / item["skill_path"] / "scripts/validate_artifact.py").is_file())
            self.assertTrue(item["reviewer_roles"])

    def test_registry_artifact_index_is_complete_and_consistent(self) -> None:
        registry = workflow_registry.load_registry()
        items = {item["id"]: item for item in registry["work_items"]}
        artifacts = {artifact["id"]: artifact for artifact in registry["artifact_types"]}

        self.assertGreaterEqual(len(artifacts), 8)  # 8 base + sub-skill artifacts
        self.assertEqual(
            {output for item in items.values() for output in item["required_outputs"]},
            set(artifacts),
        )
        for artifact in artifacts.values():
            self.assertIn(artifact["producer"], items)
            self.assertIn(artifact["id"], items[artifact["producer"]]["required_outputs"])
            self.assertTrue(set(artifact["depends_on"]).issubset(artifacts))
            self.assertTrue(artifact["prd_destination"])

        final_prd = artifacts["final-prd"]
        self.assertEqual(set(final_prd["depends_on"]), set(artifacts) - {"final-prd"})

    def test_internal_capabilities_are_indexed_under_parent_work_items(self) -> None:
        registry = workflow_registry.load_registry()
        parents = {item["id"] for item in registry["work_items"]}
        capabilities = registry["internal_capabilities"]
        self.assertEqual(len(capabilities), 8)
        self.assertEqual(len({capability["id"] for capability in capabilities}), 8)
        for capability in capabilities:
            self.assertIn(capability["parent_work_item"], parents)
            self.assertTrue((ROOT / capability["skill_path"] / "SKILL.md").is_file())
            self.assertTrue(capability["output_section"])

    def test_support_skills_have_single_authoritative_location(self) -> None:
        expected = {"competitive-research", "solution-assessment", "prd-publish", "brainstorming"}
        support_root = ROOT / "src/support-skills"
        self.assertEqual({path.name for path in support_root.iterdir() if path.is_dir()}, expected)
        for name in expected:
            self.assertTrue((support_root / name / "SKILL.md").is_file())
        self.assertFalse((ROOT / "src/branches").exists())

    def test_agent_metadata_contract(self) -> None:
        for item in workflow_registry.work_items():
            path = ROOT / item["skill_path"] / "agents/openai.yaml"
            text = path.read_text(encoding="utf-8")
            self.assertIn("interface:\n", text, path)
            self.assertRegex(text, r"(?m)^  display_name: .+$")
            self.assertRegex(text, r"(?m)^  short_description: .+$")
            self.assertIn("  default_prompt: |\n", text, path)
            self.assertIn("trigger_examples:\n", text, path)
            self.assertIn("should_not_trigger_examples:\n", text, path)
            for line in text.splitlines():
                if re.match(r"^  - ", line):
                    self.assertRegex(line, r'^  - (".*"|\|)$', path)

    def test_layout_migration_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            req = Path(temp) / "REQ-999-test"
            old = req / "01_background-goal"
            old.mkdir(parents=True)
            (old / "background-goal.md").write_text("artifact_id: BG-TEST-001\n", encoding="utf-8")
            plan = migrate_layout_v2.plan_migration(req)
            self.assertEqual(len(plan["moves"]), 1)
            migrate_layout_v2.apply_migration(req, plan)
            second = migrate_layout_v2.plan_migration(req)
            self.assertEqual(second["moves"], [])
            self.assertEqual(second["conflicts"], [])
            self.assertTrue((req / "001-business-requirements/01-background-goal/background-goal.md").is_file())

    def test_traceability_requires_explicit_edges(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            req = Path(temp)
            rows = {
                "001-business-requirements/01-background-goal/background-goal.md": "| G1 | Goal |\n",
                "001-business-requirements/02-user-journey-stories/journey-and-stories.md": "| ST-001 | G1 | Story |\n",
                "002-product-requirements/01-product-ux/ux.md": "| FEA-001 | ST-001 | Feature |\n",
                "002-product-requirements/02-function-description/function.md": "| FUN-001 | FEA-001 | Function |\n| AC-001 | FUN-001 | G1 | Then success |\n| BR-001 | FUN-001 | Rule |\n",
            }
            for rel, text in rows.items():
                path = req / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            self.assertTrue(traceability_check.validate(req)["ok"])
            (req / "002-product-requirements/01-product-ux/ux.md").write_text("| FEA-001 | Feature without story |\n", encoding="utf-8")
            self.assertFalse(traceability_check.validate(req)["ok"])

    def test_traceability_high_issue_blocks_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            req = Path(temp)
            rows = {
                "001-business-requirements/01-background-goal/background-goal.md": "| G1 | Goal |\n",
                "001-business-requirements/02-user-journey-stories/journey-and-stories.md": "| ST-001 | G1 | Story |\n",
                "002-product-requirements/01-product-ux/ux.md": "| FEA-001 | ST-001 | Feature |\n",
                "002-product-requirements/02-function-description/function.md": "| FUN-001 | FEA-001 | Function |\n| AC-001 | FUN-001 | Then success |\n| BR-001 | FUN-001 | Rule |\n",
            }
            for rel, text in rows.items():
                path = req / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            result = traceability_check.validate(req)
            self.assertFalse(result["ok"])
            self.assertTrue(any(issue["severity"] == "HIGH" for issue in result["issues"]))

    def test_yes_and_simulated_reviewer_cannot_confirm(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            req = Path(temp)
            target = req / "001-business-requirements/01-background-goal/background-goal.md"
            target.parent.mkdir(parents=True)
            self.write_reviewer_registry(req)
            target.write_text("---\nartifact_id: BG-T-001\nstatus: draft\n---\n", encoding="utf-8")
            command = [
                sys.executable, str(SCRIPTS / "pipeline.py"), str(req), "review",
                "--work-item", "project-background-goal", "--decision", "approve",
                "--reviewer", "simulated", "--yes",
                "--reviewer-id", "USR-001", "--reviewer-role", "business_owner",
            ]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("status: draft", target.read_text(encoding="utf-8"))
            command[command.index("simulated")] = "Real Reviewer"
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ready_for_human_review", result.stderr)
            self.assertIn("status: draft", target.read_text(encoding="utf-8"))

    def test_human_changes_returns_failure_and_keeps_unconfirmed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            req = Path(temp)
            target = req / "001-business-requirements/01-background-goal/background-goal.md"
            target.parent.mkdir(parents=True)
            self.write_reviewer_registry(req)
            target.write_text("---\nartifact_id: BG-T-002\nstatus: ready_for_human_review\n---\n", encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(SCRIPTS / "pipeline.py"), str(req), "review",
                "--work-item", "project-background-goal", "--decision", "changes",
                "--reviewer", "Real Reviewer", "--comments", "目标仍不清楚",
                "--reviewer-id", "USR-001", "--reviewer-role", "business_owner",
            ], capture_output=True, text=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("status: draft", target.read_text(encoding="utf-8"))
            self.assertEqual(len(list((req / "99-review").glob("review-*.md"))), 1)

    def test_authorized_approval_records_identity_and_artifact_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            req = Path(temp)
            target = req / "001-business-requirements/01-background-goal/background-goal.md"
            target.parent.mkdir(parents=True)
            self.write_reviewer_registry(req)
            # entry_material DoR: bg approval requires >= 1 registered source
            (req / "00-input").mkdir(parents=True, exist_ok=True)
            (req / "00-input/SRC-001.md").write_text("# 需求来源（测试）\n业务方代表A 提出的邀约转化率优化需求。\n", encoding="utf-8")
            # B3 每阶段强制收口：issue-record 必须存在且含 bg 收口行
            support = req / "99-review" / "support"
            support.mkdir(parents=True, exist_ok=True)
            (support / "issue-record.md").write_text(
                "# Issue Record（测试）\n\n## 13. 阶段收口表\n\n"
                "| 阶段 | Work Item | 问题数 | 收口日期 | 状态 |\n|---|---|---|---|---|\n"
                "| 001-business-requirements | project-background-goal | 0 | 2026-08-13 | closed |\n",
                encoding="utf-8",
            )
            fixture = ROOT / "test/skills/project-background-goal/fixtures/hire-website-confirmed.md"
            text = fixture.read_text(encoding="utf-8")
            text = re.sub(r"(?m)^status:\s*\S+", "status: ready_for_human_review", text, count=1)
            target.write_text(text, encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(SCRIPTS / "pipeline.py"), str(req), "review",
                "--work-item", "project-background-goal", "--decision", "approve",
                "--reviewer", "Real Reviewer", "--reviewer-id", "USR-001",
                "--reviewer-role", "business_owner",
            ], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            record = next((req / "99-review").glob("review-*.md")).read_text(encoding="utf-8")
            self.assertIn("artifact_version:", record)
            self.assertRegex(record, r"artifact_content_sha256: [0-9a-f]{64}")
            self.assertIn("reviewer_id: USR-001", record)
            self.assertIn("reviewer_role: business_owner", record)
            self.assertIn("status: confirmed", target.read_text(encoding="utf-8"))
            validated = subprocess.run([
                sys.executable, str(SCRIPTS / "branch_validator.py"), str(req), "--json",
            ], capture_output=True, text=True, check=False)
            self.assertEqual(validated.returncode, 0, validated.stdout)
            target.write_text(target.read_text(encoding="utf-8") + "\nsubstantive change\n", encoding="utf-8")
            validated = subprocess.run([
                sys.executable, str(SCRIPTS / "branch_validator.py"), str(req), "--json",
            ], capture_output=True, text=True, check=False)
            self.assertNotEqual(validated.returncode, 0)
            self.assertIn("differs from its ReviewRecord hash", validated.stdout)


if __name__ == "__main__":
    unittest.main()
