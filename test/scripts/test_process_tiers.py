#!/usr/bin/env python3
"""Behavioral regression tests for durable process tiers and PRD provenance."""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src" / "scripts"))
from workflow_registry import (  # noqa: E402
    artifact_content_hash,
    canonical_applicability_evidence,
    l1_exclusion_evidence,
    resolve_work_item,
    work_items_for_tier,
)
from l0_prd_projection import build_projection, write_projection  # noqa: E402


def b3_rows(text: str) -> list[tuple[str, str]]:
    """Extract B3 ledger rows without accepting tables from other sections."""
    in_ledger = False
    rows: list[tuple[str, str]] = []
    for line in text.splitlines():
        if re.match(r"^##\s+13\.\s*阶段收口表", line):
            in_ledger = True
            continue
        if in_ledger and line.startswith("## " ):
            break
        if not in_ledger or not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if (len(cells) >= 2 and cells[0] not in {"阶段", "---"}
                and cells[1] != "Work Item"):
            rows.append((cells[0], cells[1]))
    return rows

PRD_VALIDATOR = ROOT / "src/stages/003-prd-output/skills/prd-assembly/scripts/validate_artifact.py"
spec = importlib.util.spec_from_file_location("prd_validator", PRD_VALIDATOR)
prd_validator = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(prd_validator)


class ProcessTierTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="pm-tier-contract-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def init(self, tier: str, name: str) -> Path:
        cmd = [sys.executable, str(ROOT / "src/scripts/pipeline.py"), "init", name,
               "--process-tier", tier, "--root", str(self.tmp)]
        proc = subprocess.run(cmd, text=True, capture_output=True, encoding="utf-8", check=False)
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        return self.tmp / "requirements" / name

    def test_init_requires_explicit_tier(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "src/scripts/pipeline.py"), "init", "REQ-990-no-tier", "--root", str(self.tmp)],
            text=True, capture_output=True, encoding="utf-8", check=False,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("--process-tier", proc.stderr)

    def test_difficulty_entry_is_advisory_and_only_medium_high_trigger(self) -> None:
        cases = (("low", False, None), ("medium", True, "L1"), ("high", True, "L2"))
        for difficulty, triggered, recommendation in cases:
            req = self.init("L0", f"REQ-989-{difficulty}")
            proc = subprocess.run(
                [sys.executable, str(ROOT / "src/scripts/pipeline.py"), str(req), "entry",
                 "--difficulty", difficulty], text=True, capture_output=True,
                encoding="utf-8", check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            payload = json.loads(proc.stdout)["difficulty_entry"]
            self.assertEqual(payload["triggered"], triggered)
            self.assertEqual(payload["recommendation"], recommendation)
            if triggered:
                self.assertTrue(payload["selection_required"])
                self.assertIn("人工", payload["reason"])
            else:
                self.assertFalse(payload["selection_required"])

    def test_init_persists_difficulty_recommendation_without_overriding_tier(self) -> None:
        req = self.tmp / "requirements" / "REQ-988-human-tier"
        proc = subprocess.run(
            [sys.executable, str(ROOT / "src/scripts/pipeline.py"), "init", req.name,
             "--process-tier", "L1", "--difficulty", "high", "--root", str(self.tmp)],
            text=True, capture_output=True, encoding="utf-8", check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        text = (req / "00-input/intake-decision.md").read_text(encoding="utf-8")
        self.assertIn("process_tier: L1", text)
        self.assertIn('difficulty_level: "high"', text)
        self.assertIn('tier_recommendation: "L2"', text)
        self.assertIn("人工确认（建议不可自动生效）", text)
        entry = subprocess.run(
            [sys.executable, str(ROOT / "src/scripts/pipeline.py"), str(req), "entry"],
            text=True, capture_output=True, encoding="utf-8", check=False,
        )
        self.assertEqual(entry.returncode, 0, entry.stderr + entry.stdout)
        payload = json.loads(entry.stdout)["difficulty_entry"]
        self.assertTrue(payload["triggered"])
        self.assertEqual(payload["recommendation"], "L2")

    def test_init_projects_only_current_tier(self) -> None:
        expected = {
            "L0": {"mini-prd"},
            "L1": {item["id"] for item in work_items_for_tier("L1")},
            "L2": {item["id"] for item in work_items_for_tier("L2")},
        }
        for tier, ids in expected.items():
            req = self.init(tier, f"REQ-99{len(tier)}-{tier.lower()}")
            decision = (req / "00-input/intake-decision.md").read_text(encoding="utf-8")
            self.assertIn(f"process_tier: {tier}", decision)
            actual = {item["id"] for item in work_items_for_tier(tier)
                      if (req / item["artifact_dir"]).is_dir()}
            self.assertEqual(actual, ids)
            readme = (req / "README.md").read_text(encoding="utf-8")
            self.assertIn(f"`{tier}`", readme)
            issue_record = req / "99-review/support/issue-record.md"
            if tier == "L0":
                self.assertFalse(issue_record.exists())
                continue
            self.assertTrue(issue_record.is_file())
            actual_rows = b3_rows(issue_record.read_text(encoding="utf-8"))
            expected_rows = [(item["stage"], item["id"]) for item in work_items_for_tier(tier)]
            self.assertEqual(actual_rows, expected_rows)

    def test_entry_routes_sparse_l0_material_to_mini_prd(self) -> None:
        req = self.init("L0", "REQ-993-l0-entry")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "src/scripts/pipeline.py"), str(req), "entry"],
            text=True, capture_output=True, encoding="utf-8", check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        payload = json.loads(proc.stdout)
        self.assertIn("材料成熟度 L0", payload["maturity"])
        self.assertIn("mini-prd", payload["recommended_entry"])
        self.assertIn("mini-prd", payload["entry_blocked"])
        self.assertNotIn("project-background-goal", payload["recommended_entry"])
        self.assertNotIn("Stage 1", payload["recommended_entry"])

    def test_entry_keeps_material_maturity_separate_from_l1_l2_tier(self) -> None:
        for tier in ("L1", "L2"):
            req = self.init(tier, f"REQ-993-{tier.lower()}-entry")
            proc = subprocess.run(
                [sys.executable, str(ROOT / "src/scripts/pipeline.py"), str(req), "entry"],
                text=True, capture_output=True, encoding="utf-8", check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            payload = json.loads(proc.stdout)
            self.assertIn("材料成熟度 L0", payload["maturity"])
            self.assertIn("project-background-goal", payload["recommended_entry"])
            self.assertNotIn("交付档位", payload["maturity"])

    def test_issue_record_b3_rejects_missing_cross_tier_and_duplicate_rows(self) -> None:
        req = self.init("L1", "REQ-996-l1-b3")
        issue_record = req / "99-review/support/issue-record.md"
        original = issue_record.read_text(encoding="utf-8")

        def validate(text: str) -> dict:
            issue_record.write_text(text, encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(ROOT / "src/scripts/pipeline.py"), str(req), "gate",
                 "--work-item", "project-background-goal", "--json"],
                text=True, capture_output=True, encoding="utf-8", check=False,
            )
            self.assertNotEqual(proc.returncode, 0, proc.stdout)
            return json.loads(proc.stdout)["issue_record"]

        missing = validate(original.replace(
            "| 003-prd-output | prd-assembly | 0 | 待填写 | open |\n", "", 1,
        ))
        self.assertIn("missing tier work items", " | ".join(missing["errors"]))

        cross_tier = validate(original.replace(
            "| 003-prd-output | prd-assembly | 0 | 待填写 | open |",
            "| 002-product-requirements | page-design | 0 | 待填写 | open |", 1,
        ))
        self.assertIn("cross-tier or wrong-stage", " | ".join(cross_tier["errors"]))

        duplicate = validate(original.replace(
            "| 003-prd-output | prd-assembly | 0 | 待填写 | open |",
            "| 003-prd-output | prd-assembly | 0 | 待填写 | open |\n"
            "| 003-prd-output | prd-assembly | 0 | 待填写 | open |", 1,
        ))
        self.assertIn("duplicate work items", " | ".join(duplicate["errors"]))

    def test_cross_tier_gate_fails_without_side_effects(self) -> None:
        req = self.init("L0", "REQ-991-l0")
        before_review = {p.relative_to(req).as_posix(): p.read_bytes() for p in (req / "99-review").rglob("*") if p.is_file()}
        before_audit = {p.relative_to(req).as_posix(): p.read_bytes() for p in (req / ".audit").rglob("*") if p.is_file()}
        proc = subprocess.run(
            [sys.executable, str(ROOT / "src/scripts/pipeline.py"), str(req), "gate",
             "--work-item", "project-background-goal"],
            text=True, capture_output=True, encoding="utf-8", check=False,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("not enabled for persisted tier L0", proc.stderr)
        after_review = {p.relative_to(req).as_posix(): p.read_bytes() for p in (req / "99-review").rglob("*") if p.is_file()}
        after_audit = {p.relative_to(req).as_posix(): p.read_bytes() for p in (req / ".audit").rglob("*") if p.is_file()}
        self.assertEqual(before_review, after_review)
        self.assertEqual(before_audit, after_audit)

    def test_l1_requires_factual_exclusions_before_prd_assembly(self) -> None:
        req = self.init("L1", "REQ-994-l1-exclusions")
        first = l1_exclusion_evidence(req)
        self.assertFalse(first["ok"])
        self.assertEqual(len(first["issues"]), 6)
        decision = req / "00-input/intake-decision.md"
        text = decision.read_text(encoding="utf-8")
        for field in ("pd", "ix", "fields", "vl", "state", "ex"):
            text = text.replace(
                f'l2_only_{field}: "pending"',
                f'l2_only_{field}: "not_applicable: 沿用既有单一配置，无新增 {field} 设计"',
            )
        decision.write_text(text, encoding="utf-8")
        self.assertTrue(l1_exclusion_evidence(req)["ok"])

    def test_new_req_requires_canonical_applicability_matrix_before_assembly(self) -> None:
        req = self.init("L1", "REQ-994-l1-canonical-matrix")
        result = canonical_applicability_evidence(req)
        self.assertFalse(result["ok"])
        self.assertTrue(any("项目背景" in issue for issue in result["issues"]))

    def test_l1_rejects_generic_exclusion_reason(self) -> None:
        req = self.init("L1", "REQ-994-l1-generic-exclusions")
        decision = req / "00-input/intake-decision.md"
        text = decision.read_text(encoding="utf-8")
        for field in ("pd", "ix", "fields", "vl", "state", "ex"):
            text = text.replace(
                f'l2_only_{field}: "pending"',
                f'l2_only_{field}: "not_applicable: 本期不适用"',
            )
        decision.write_text(text, encoding="utf-8")
        result = l1_exclusion_evidence(req)
        self.assertFalse(result["ok"])
        self.assertEqual(len(result["issues"]), 6)

    def test_l1_quality_contract_blocks_review_gate_until_record_is_complete(self) -> None:
        """A new L1 artifact cannot bypass the quality record at review-ready state."""
        req = self.init("L1", "REQ-994-l1-quality-contract")
        (req / "00-input/SRC-001.md").write_text("# 来源\n\n招聘流程优化的已确认背景。\n", encoding="utf-8")
        artifact = req / resolve_work_item("project-background-goal")["artifact_dir"] / resolve_work_item("project-background-goal")["artifact_file"]
        fixture = (ROOT / "test/skills/project-background-goal/fixtures/hire-website-sufficient.md").read_text(encoding="utf-8")
        fixture = fixture.replace(
            "status: ready_for_human_review",
            "status: ready_for_human_review\nquality_contract_version: \"1\"",
            1,
        )
        without_quality = re.sub(r"\n## 产品质量增强记录\n.*\Z", "\n", fixture, flags=re.DOTALL)
        artifact.write_text(without_quality, encoding="utf-8")

        bg_validator_path = ROOT / "src/stages/001-business-requirements/skills/project-background-goal/scripts/validate_artifact.py"
        bg_spec = importlib.util.spec_from_file_location("background_validator_quality", bg_validator_path)
        bg_validator = importlib.util.module_from_spec(bg_spec)
        assert bg_spec.loader
        bg_spec.loader.exec_module(bg_validator)
        invalid = bg_validator.validate(artifact)
        self.assertFalse(invalid["ok"])
        self.assertTrue(any("产品质量增强记录" in error for error in invalid["errors"]))

        blocked = subprocess.run(
            [sys.executable, str(ROOT / "src/scripts/pipeline.py"), str(req), "gate",
             "--work-item", "project-background-goal", "--json"],
            text=True, capture_output=True, encoding="utf-8", check=False,
        )
        self.assertNotEqual(blocked.returncode, 0, blocked.stdout)

        artifact.write_text(fixture, encoding="utf-8")
        valid = bg_validator.validate(artifact)
        self.assertTrue(valid["ok"], valid["errors"])
        passed = subprocess.run(
            [sys.executable, str(ROOT / "src/scripts/pipeline.py"), str(req), "gate",
             "--work-item", "project-background-goal", "--json"],
            text=True, capture_output=True, encoding="utf-8", check=False,
        )
        # The fixture deliberately retains unrelated open questions, so the
        # full L1 gate still fails its independent stage-closeup check.  What
        # this regression proves is that completing the quality record removes
        # the quality-contract failure without weakening any other gate.
        gate_payload = json.loads(passed.stdout)
        validator_check = next(
            check for check in gate_payload["work_item"]["checks"]
            if check["name"] == "artifact_validator"
        )
        self.assertTrue(validator_check["pass"], gate_payload)

    def test_backfill_rejects_cross_tier_record_without_writing_events(self) -> None:
        req = self.init("L0", "REQ-995-l0-backfill")
        record = req / "99-review" / "review-legacy.md"
        record.write_text("# Legacy review\n- work_item: project-background-goal\n- decision: approve\n", encoding="utf-8")
        events = req / ".audit" / "events.jsonl"
        before = events.read_bytes()
        proc = subprocess.run(
            [sys.executable, str(ROOT / "src/scripts/pipeline.py"), str(req), "backfill"],
            text=True, capture_output=True, encoding="utf-8", check=False,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("not enabled for persisted tier L0", proc.stderr)
        self.assertEqual(before, events.read_bytes())

    def _write_l1_prd_tree(self) -> tuple[Path, list[Path]]:
        req = self.tmp / "REQ-992-manifest"
        (req / "99-review").mkdir(parents=True)
        prd_path = req / "003-prd-output" / "prd.md"
        prd_path.parent.mkdir(parents=True)
        fixture = (ROOT / "test/skills/prd-assembly/fixtures/prd-l1-ok.md").read_text(encoding="utf-8")
        fixture = fixture.replace('applicability_contract_version: "1"', 'applicability_contract_version: "1"\nreader_contract_version: "2"')
        fixture = fixture.replace("## 3. 用户旅程", "## 3. 用户与用户旅程")
        fixture = fixture.replace("## 4. 用户故事", "## 4. 用户故事与优先级")
        fixture = fixture.replace("## 10. 验收依据", "## 10. 验收标准")
        # Reader-facing v8 keeps governance chapters out of the PRD body; the
        # legacy fixture ends with 按需章节 / RTM / 自审 that move to the
        # manifest and 99-review.  Trim them so the derived tree matches the
        # reader contract instead of leaking process material.
        fixture = re.sub(r"\n## 11\. 按需章节\n.*\Z", "\n", fixture, flags=re.DOTALL)
        # Schema-7 registry: L1 = 9 upstreams.  The legacy fixture declares 7;
        # align the frontmatter so D5.2 sees the full tier set.
        statuses = " ".join(prd_validator.UPSTREAM_WORK_ITEMS_L1)
        fixture = re.sub(r'(?m)^upstream_work_item_statuses:.*$',
                         f'upstream_work_item_statuses: "{statuses}"', fixture)
        sources, blocks = [], []
        for index, item in enumerate(work_items_for_tier("L1")):
            if item["id"] == "prd-assembly":
                continue
            artifact = req / item["artifact_dir"] / item["artifact_file"]
            artifact.parent.mkdir(parents=True, exist_ok=True)
            artifact_id = f"SRC-{index + 1:03d}"
            source_text = (
                "---\nartifact_id: " + artifact_id + "\nversion: v1\nstatus: confirmed\n"
                "owner: owner\n---\n# " + item["name"] + "\n\n确认内容 " + item["id"] + "。\n"
            )
            artifact.write_text(source_text, encoding="utf-8")
            digest = artifact_content_hash(source_text)
            rel = artifact.relative_to(req).as_posix()
            sources.append({"work_item": item["id"], "artifact_id": artifact_id, "path": rel,
                            "status": "confirmed", "content_sha256": digest,
                            "target_sections": ["§1-§10"],
                            "selectors": [item["id"]]})
            body = prd_validator._artifact_body(source_text)
            blocks.append(f"<!-- source: work_item={item['id']} artifact_id={artifact_id} sha256={digest} -->\n{body}\n<!-- /source -->")
        prd_path.write_text(fixture + "\n", encoding="utf-8")
        (prd_path.parent / "prd-assembly-manifest.json").write_text(
            json.dumps({"schema_version": 2, "process_tier": "L1", "sources": sources}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return prd_path, [req / source["path"] for source in sources]

    def test_l1_manifest_detects_source_tampering_without_source_blocks(self) -> None:
        prd_path, source_paths = self._write_l1_prd_tree()
        self.assertTrue(prd_validator.validate(prd_path)["ok"], prd_validator.validate(prd_path)["errors"])
        source_paths[0].write_text(source_paths[0].read_text(encoding="utf-8") + "已篡改\n", encoding="utf-8")
        changed = prd_validator.validate(prd_path)
        self.assertFalse(changed["ok"])
        self.assertTrue(any("content_sha256 does not match source file" in error for error in changed["errors"]))

    def _write_l0_projection_tree(self) -> tuple[Path, Path]:
        """Create a real L0 REQ tree with a completed durable applicability matrix."""
        req = self.init("L0", "REQ-997-l0-projection")
        intake = req / "00-input/intake-decision.md"
        completed_rows: list[str] = []
        for line in intake.read_text(encoding="utf-8").splitlines():
            if line.startswith("| §"):
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                cells[2] = "具体事实来自 SRC-001 活动配置"
                cells[3] = "SRC-001"
                cells[4] = "nova"
                cells[5] = "2026-08-20"
                if cells[1] == "conditional":
                    cells[6] = cells[6].replace("待判断", "当前判断为不适用")
                line = "| " + " | ".join(cells) + " |"
            completed_rows.append(line)
        intake.write_text("\n".join(completed_rows) + "\n", encoding="utf-8")
        mini = req / "000-minimal/01-mini-prd/mini-prd.md"
        source = (ROOT / "test/skills/mini-prd/fixtures/mini-prd-ok.md").read_text(encoding="utf-8")
        source = source.replace('status: "draft"', 'status: "confirmed"')
        source = source.replace('confirmed_at: ""', 'confirmed_at: "2026-08-20T00:00:00+00:00"')
        mini.write_text(source, encoding="utf-8")
        prd, manifest = build_projection(mini, reviewer="nova", confirmed_at="2026-08-20T00:00:00+00:00")
        output = req / "003-prd-output/prd.md"
        write_projection(mini, output, output.parent / "prd-assembly-manifest.json",
                         reviewer="nova", projection=(prd, manifest))
        return output, mini

    def test_l0_projection_uses_reader_contract_and_manifest(self) -> None:
        prd_path, _ = self._write_l0_projection_tree()
        result = prd_validator.validate(prd_path)
        self.assertTrue(result["ok"], result["errors"])
        text = prd_path.read_text(encoding="utf-8")
        self.assertIn('reader_contract_version: "2"', text)
        self.assertIn("## 11. 依赖与待决业务问题", text)
        self.assertNotIn("## 需求追溯矩阵", text)
        self.assertNotIn("## 自审记录", text)
        self.assertNotIn("<!-- source: work_item=mini-prd", text)
        # Reader contract requires an applicability block on every generated
        # section (core 8 + §7/§8 不适用占位 + §9.1-§9.4 + §11 = 15).
        self.assertEqual(text.count("<!-- applicability:"), 15)

    def test_l0_projection_detects_source_tampering(self) -> None:
        prd_path, mini = self._write_l0_projection_tree()
        mini.write_text(mini.read_text(encoding="utf-8") + "\n篡改来源。\n", encoding="utf-8")
        changed_source = prd_validator.validate(prd_path)
        self.assertFalse(changed_source["ok"])
        self.assertTrue(any("content_sha256 does not match source file" in error for error in changed_source["errors"]))

    def test_l0_human_approval_publishes_canonical_prd(self) -> None:
        req = self.init("L0", "REQ-998-l0-approval")
        intake = req / "00-input/intake-decision.md"
        rows: list[str] = []
        for line in intake.read_text(encoding="utf-8").splitlines():
            if line.startswith("| §"):
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                cells[2] = "具体事实来自 SRC-001 活动配置"
                cells[3] = "SRC-001"
                cells[4] = "Real Reviewer"
                cells[5] = "2026-08-20"
                if cells[1] == "conditional":
                    cells[6] = cells[6].replace("待判断", "当前判断为不适用")
                line = "| " + " | ".join(cells) + " |"
            rows.append(line)
        intake.write_text("\n".join(rows) + "\n", encoding="utf-8")
        mini = req / "000-minimal/01-mini-prd/mini-prd.md"
        source = (ROOT / "test/skills/mini-prd/fixtures/mini-prd-ok.md").read_text(encoding="utf-8")
        source = source.replace('status: "draft"', 'status: "ready_for_human_review"')
        mini.write_text(source, encoding="utf-8")
        (req / "00-input/authorized-reviewers.json").write_text(
            json.dumps({"reviewers": [{"id": "USR-998", "name": "Real Reviewer", "roles": ["business_owner"]}]}),
            encoding="utf-8",
        )
        proc = subprocess.run(
            [sys.executable, str(ROOT / "src/scripts/pipeline.py"), str(req), "review",
             "--work-item", "mini-prd", "--decision", "approve", "--reviewer", "Real Reviewer",
             "--reviewer-id", "USR-998", "--reviewer-role", "business_owner"],
            text=True, capture_output=True, encoding="utf-8", check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertIn("status: confirmed", mini.read_text(encoding="utf-8"))
        output = req / "003-prd-output/prd.md"
        self.assertTrue(output.is_file())
        self.assertTrue(prd_validator.validate(output)["ok"], prd_validator.validate(output)["errors"])


if __name__ == "__main__":
    unittest.main()
