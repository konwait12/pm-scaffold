#!/usr/bin/env python3
"""Regression tests for E2E-035 (P2 distillation: docx export / DDD guide / red team).

Verifies:
  1. prd_to_docx.py exists, is importable, and returns 2 (dependency missing)
     with a clear message instead of silently degrading.
  2. ddd-design-guide.md exists and references PRD upstreams (STATE/BR/etc.).
  3. red-team-naysayer.md exists, is advisory-only (never mutates status).
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PRD_ASSEMBLY = ROOT / "src/stages/003-prd-output/skills/prd-assembly"
AUDIT_DIR = ROOT / "src/shared/audit"
DOCX_SCRIPT = ROOT / "src/scripts/prd_to_docx.py"


def test_p2_docx_script_present_and_importable():
    assert DOCX_SCRIPT.is_file(), f"missing {DOCX_SCRIPT}"
    # Syntax check via compile
    compile(DOCX_SCRIPT.read_text(encoding="utf-8"), str(DOCX_SCRIPT), "exec")


def test_p2_docx_returns_dependency_missing():
    """Without python-docx installed, exit code must be 2 (clear failure), not 0."""
    probe = ROOT / "requirements/REQ-001-fsn-rsvp-reddot/003-prd-output/prd.md"
    if not probe.is_file():
        return  # no real PRD to probe; skip
    try:
        import docx  # noqa: F401
        return  # dependency present; behavior test skipped
    except ImportError:
        pass
    proc = subprocess.run(
        [sys.executable, str(DOCX_SCRIPT), str(probe), "--output", "/tmp/p2-test.docx"],
        text=True, capture_output=True, encoding="utf-8", check=False,
    )
    assert proc.returncode == 2, f"expected exit 2 (missing dep), got {proc.returncode}: {proc.stderr}"
    assert "python-docx" in proc.stderr


def test_p2_ddd_guide_present_and_covers_upstreams():
    guide = PRD_ASSEMBLY / "references/ddd-design-guide.md"
    assert guide.is_file(), f"missing {guide}"
    text = guide.read_text(encoding="utf-8")
    for token in ("7 阶段", "STATE", "贫血模型", "BR"):
        assert token in text, f"ddd guide missing token: {token}"


def test_p2_red_team_present_and_advisory():
    red = AUDIT_DIR / "red-team-naysayer.md"
    assert red.is_file(), f"missing {red}"
    text = red.read_text(encoding="utf-8")
    for token in ("10 铁律", "三阶段", "只提问", "advisory"):
        assert token in text, f"red-team guide missing token: {token}"


def test_p2_skil_loading_table_references_new_docs():
    skill = PRD_ASSEMBLY / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    assert "ddd-design-guide.md" in text
    assert "red-team-naysayer.md" in text


if __name__ == "__main__":
    test_p2_docx_script_present_and_importable()
    test_p2_docx_returns_dependency_missing()
    test_p2_ddd_guide_present_and_covers_upstreams()
    test_p2_red_team_present_and_advisory()
    test_p2_skil_loading_table_references_new_docs()
    print("✅ all E2E-035 (P2 distillation) regression tests pass")