"""Regression tests for requirement-restate traceability routing."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[3]
    / "src/stages/001-business-requirements/skills/requirement-restate/scripts/validate_artifact.py"
)
FIXTURE = Path(__file__).resolve().parent / "fixtures/requirement-restate-confirmed.md"

spec = importlib.util.spec_from_file_location("requirement_restate_validator", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def _validate_text(text: str) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as handle:
        handle.write(text)
        path = Path(handle.name)
    try:
        return module.validate(path)
    finally:
        path.unlink()


def test_sourced_conflicts_and_unknowns_have_complete_pm_routing() -> None:
    result = module.validate(FIXTURE)
    assert result["ok"], result["errors"]


def test_unknown_without_issue_record_link_fails() -> None:
    text = FIXTURE.read_text(encoding="utf-8").replace(" | ISS-006 |", " | — |", 1)
    result = _validate_text(text)
    assert not result["ok"]
    assert any("UNK-001 unknown is missing an ISS-NNN" in error for error in result["errors"])


if __name__ == "__main__":
    test_sourced_conflicts_and_unknowns_have_complete_pm_routing()
    test_unknown_without_issue_record_link_fails()
