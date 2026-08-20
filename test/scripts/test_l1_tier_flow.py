#!/usr/bin/env python3
"""L1 Process Tier end-to-end tests: predecessor tier-exemption.

Regression guard for BUG-1 (L1 档 predecessors 检查未做 tier 豁免)——
orchestrator.build_status 与 dor_check.check_item 必须只检查「当前 tier 集内」的前置，
否则 L1 REQ 走到 acceptance-criteria 时被 exception-handling/interaction-rules(not_created) 卡死。
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src" / "scripts"))
sys.path.insert(0, str(ROOT))

from orchestrator import build_status  # noqa: E402
from workflow_registry import resolve_work_item, tier_for_req, work_items_for_tier  # noqa: E402


class L1TierFlowTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = Path(tempfile.mkdtemp(prefix="req-l1-test-"))
        self.req_dir = self._tmp / "REQ-997-l1-flow"
        self.req_dir.mkdir(parents=True)
        (self.req_dir / "00-input").mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _stub(self, wi_id: str, status: str = "confirmed") -> None:
        wi = resolve_work_item(wi_id)
        d = self.req_dir / wi["artifact_dir"]
        d.mkdir(parents=True, exist_ok=True)
        (d / wi["artifact_file"]).write_text(
            f"---\nartifact_id: X\nstatus: {status}\n---\n# stub\n",
            encoding="utf-8",
        )

    def _write_readme(self, tier: str) -> None:
        (self.req_dir / "README.md").write_text(
            f"# REQ\n\n## 流程档位\n\n- **process_tier**：`{tier}`（L0 / L1 / L2）\n",
            encoding="utf-8",
        )

    def test_tier_for_req_parses_readme_bold_field(self) -> None:
        """BUG-2 回归：README 模板的 `- **process_tier**：L1` 必须能被 tier_for_req 解析。"""
        self._write_readme("L1")
        self.assertEqual(tier_for_req(self.req_dir), "L1")

    def test_l1_status_exempts_out_of_tier_predecessors(self) -> None:
        """L1 集内 7 个上游全部 confirmed 后，acceptance-criteria 不应被 EX/IX 前置卡住。"""
        self._write_readme("L1")
        for wi in work_items_for_tier("L1"):
            if wi["id"] == "acceptance-criteria":
                continue
            self._stub(wi["id"])
        result = build_status(self.req_dir)
        self.assertEqual(result["next_work_item"], "acceptance-criteria")
        self.assertFalse(result["blocked"], f"blockers={result['blockers']}")
        self.assertTrue(result["workflow_valid"])
        self.assertNotIn("exception-handling", [b for b in result["blockers"]])
        self.assertNotIn("interaction-rules", [b for b in result["blockers"]])

    def test_l1_check_item_dor_passes_with_exemption(self) -> None:
        """dor_check.check_item 对 acceptance-criteria 的 DoR：EX/IX 前置 tier 豁免后 dor_pass=True。"""
        self._write_readme("L1")
        for wi in work_items_for_tier("L1"):
            if wi["id"] == "acceptance-criteria":
                continue
            self._stub(wi["id"])
        import dor_check
        item = resolve_work_item("acceptance-criteria")
        result = dor_check.check_item(self.req_dir, item)
        self.assertTrue(result["dor_pass"], f"predecessors={result['predecessors']}")

    def test_l1_pipeline_status_cli(self) -> None:
        """pipeline status --process-tier L1 端到端。"""
        self._write_readme("L1")
        for wi in work_items_for_tier("L1"):
            if wi["id"] == "acceptance-criteria":
                continue
            self._stub(wi["id"])
        proc = subprocess.run(
            [sys.executable, str(ROOT / "src/scripts/pipeline.py"), str(self.req_dir),
             "status", "--process-tier", "L1"],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        import json
        out = json.loads(proc.stdout)
        self.assertEqual(out["next_work_item"], "acceptance-criteria")
        self.assertFalse(out["blocked"])


if __name__ == "__main__":
    unittest.main()
