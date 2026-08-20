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
    l1_exclusion_evidence,
    resolve_work_item,
    work_items_for_tier,
)


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
        self.assertEqual(len(first["issues"]), 5)
        decision = req / "00-input/intake-decision.md"
        text = decision.read_text(encoding="utf-8")
        for field in ("pd", "ix", "vl", "state", "ex"):
            text = text.replace(
                f'l2_only_{field}: "pending"',
                f'l2_only_{field}: "not_applicable: 沿用既有单一配置，无新增 {field} 设计"',
            )
        decision.write_text(text, encoding="utf-8")
        self.assertTrue(l1_exclusion_evidence(req)["ok"])

    def test_l1_rejects_generic_exclusion_reason(self) -> None:
        req = self.init("L1", "REQ-994-l1-generic-exclusions")
        decision = req / "00-input/intake-decision.md"
        text = decision.read_text(encoding="utf-8")
        for field in ("pd", "ix", "vl", "state", "ex"):
            text = text.replace(
                f'l2_only_{field}: "pending"',
                f'l2_only_{field}: "not_applicable: 本期不适用"',
            )
        decision.write_text(text, encoding="utf-8")
        result = l1_exclusion_evidence(req)
        self.assertFalse(result["ok"])
        self.assertEqual(len(result["issues"]), 5)

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
                            "target_section": "source-block"})
            body = prd_validator._artifact_body(source_text)
            blocks.append(f"<!-- source: work_item={item['id']} artifact_id={artifact_id} sha256={digest} -->\n{body}\n<!-- /source -->")
        prd_path.write_text(fixture + "\n\n" + "\n\n".join(blocks) + "\n", encoding="utf-8")
        (prd_path.parent / "prd-assembly-manifest.json").write_text(
            json.dumps({"schema_version": 1, "process_tier": "L1", "sources": sources}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return prd_path, [req / source["path"] for source in sources]

    def test_l1_manifest_detects_source_and_block_tampering(self) -> None:
        prd_path, source_paths = self._write_l1_prd_tree()
        self.assertTrue(prd_validator.validate(prd_path)["ok"], prd_validator.validate(prd_path)["errors"])
        source_paths[0].write_text(source_paths[0].read_text(encoding="utf-8") + "已篡改\n", encoding="utf-8")
        changed = prd_validator.validate(prd_path)
        self.assertFalse(changed["ok"])
        self.assertTrue(any("content_sha256 does not match source file" in error for error in changed["errors"]))
        # Rebuild a clean tree, then edit only the embedded PRD block.
        shutil.rmtree(prd_path.parents[2])
        prd_path, _ = self._write_l1_prd_tree()
        prd_path.write_text(prd_path.read_text(encoding="utf-8").replace("确认内容 project-background-goal。", "人工摘要被改写。", 1), encoding="utf-8")
        changed_block = prd_validator.validate(prd_path)
        self.assertFalse(changed_block["ok"])
        self.assertTrue(any("source block content was changed" in error for error in changed_block["errors"]))


if __name__ == "__main__":
    unittest.main()
