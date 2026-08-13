#!/usr/bin/env python3
"""Unit tests for the prd-publish SHA-256 tamper check.

Builds a temporary requirement directory (003-prd-output/prd.md + 99-review/
ReviewRecord + publish-record) and verifies:
- unmodified prd.md passes with an informational SHA-256 warning
- post-confirmation modification fails with "SHA-256 mismatch"
- a standalone publish record (no requirement context) silently skips
- a requirement context without any ReviewRecord warns and skips
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "src/scripts"
sys.path.insert(0, str(SCRIPTS))

from pipeline import artifact_content_hash  # noqa: E402  (authoritative normalization)

VALIDATOR = ROOT / "src/support-skills/prd-publish/scripts/validate_artifact.py"
SPEC = importlib.util.spec_from_file_location("prd_publish_validate_artifact", VALIDATOR)
prd_publish = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(prd_publish)

PRD_CONTENT = """---
artifact_id: PRD-001
version: v1.0
status: confirmed
reviewer: Real Reviewer
reviewed_at: 2026-08-13T10:00:00+00:00
---

# 招聘网站 PRD

## 背景

公司需要招聘网站，支持岗位发布与简历收集。
"""

REVIEW_RECORD = """# Review: PRD Assembly

- work_item: prd-assembly
- artifact: 003-prd-output/prd.md
- artifact_version: v1.0
- artifact_content_sha256: {hash}
- decision: approve
- reviewer: Real Reviewer
- reviewer_id: USR-001
- reviewer_role: business_owner
- reviewed_at: 2026-08-13T10:00:00+00:00
- comments: 无
"""

PUBLISH_RECORD = """## 发布前检查

- [x] 所有上游 confirmed
- [x] 追溯检查通过
- [x] 人工最终确认

## 发布渠道

| 渠道 | 状态 | 链接 |
|---|---|---|
| 飞书文档 | 已发布 | https://example.feishu.cn/docx |

## 通知

已通知产品负责人和研发团队。
"""


class PrdPublishTamperTest(unittest.TestCase):
    def build_req(self, tmp: Path, name: str = "REQ-001-tamper") -> Path:
        """Build a requirement tree and return the publish-record path."""
        req = tmp / name
        (req / "003-prd-output").mkdir(parents=True)
        (req / "99-review" / "support").mkdir(parents=True)
        (req / "003-prd-output" / "prd.md").write_text(PRD_CONTENT, encoding="utf-8")
        (req / "99-review" / "review-prd-assembly-2026-08-13.md").write_text(
            REVIEW_RECORD.format(hash=artifact_content_hash(PRD_CONTENT)), encoding="utf-8"
        )
        publish = req / "99-review" / "support" / "publish-record-2026-08-13.md"
        publish.write_text(PUBLISH_RECORD, encoding="utf-8")
        return publish

    def test_unmodified_prd_passes_tamper_check(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            publish = self.build_req(Path(temp))
            result = prd_publish.validate(publish)
            self.assertTrue(result["ok"], result)
            self.assertEqual(result["errors"], [])
            self.assertTrue(any("SHA-256" in w for w in result["warnings"]), result["warnings"])

    def test_tampered_prd_fails_with_sha256_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            publish = self.build_req(Path(temp))
            prd = publish.parent.parent.parent / "003-prd-output" / "prd.md"
            prd.write_text(PRD_CONTENT + "\n确认后被篡改的内容\n", encoding="utf-8")
            result = prd_publish.validate(publish)
            self.assertFalse(result["ok"])
            self.assertTrue(
                any("SHA-256 mismatch" in e for e in result["errors"]), result["errors"]
            )

    def test_standalone_publish_record_silently_skips(self) -> None:
        # 无需求上下文的独立文件（如 fixtures）必须静默跳过，不产生 error/warning
        with tempfile.TemporaryDirectory() as temp:
            publish = Path(temp) / "publish-record.md"
            publish.write_text(PUBLISH_RECORD, encoding="utf-8")
            result = prd_publish.validate(publish)
            self.assertTrue(result["ok"], result)
            self.assertEqual(result["errors"], [])
            self.assertFalse(any("SHA-256" in w for w in result["warnings"]), result["warnings"])

    def test_missing_review_record_warns_and_skips(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            req = Path(temp) / "REQ-002-no-record"
            (req / "003-prd-output").mkdir(parents=True)
            (req / "99-review" / "support").mkdir(parents=True)
            (req / "003-prd-output" / "prd.md").write_text(PRD_CONTENT, encoding="utf-8")
            publish = req / "99-review" / "support" / "publish-record-2026-08-13.md"
            publish.write_text(PUBLISH_RECORD, encoding="utf-8")
            result = prd_publish.validate(publish)
            self.assertTrue(result["ok"], result)
            self.assertTrue(any("无 ReviewRecord" in w for w in result["warnings"]), result["warnings"])


if __name__ == "__main__":
    unittest.main()
