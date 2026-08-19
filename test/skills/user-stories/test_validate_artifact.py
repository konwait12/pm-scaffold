#!/usr/bin/env python3
"""Unit tests for the independent user-stories validator."""

import json
import sys
import tempfile
from pathlib import Path

# Add the skill scripts dir to path
SKILL_SCRIPT = Path(__file__).resolve().parent.parent.parent.parent / "src/stages/001-business-requirements/skills/user-stories/scripts/validate_artifact.py"
sys.path.insert(0, str(SKILL_SCRIPT.parent))

import importlib.util
spec = importlib.util.spec_from_file_location("validate_artifact", SKILL_SCRIPT)
validate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_module)


def test_positive_fixture_passes():
    fixture = Path(__file__).resolve().parent / "fixtures/hire-website-journey-confirmed.md"
    result = validate_module.validate(fixture)
    assert result["ok"], result.get("errors")


def test_missing_contract_fails():
    """File with missing frontmatter and headings must fail."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write("# Just a title\n\nNo frontmatter, no proper structure.\n")
        tmp = f.name
    try:
        result = validate_module.validate(Path(tmp))
        assert not result["ok"], "Should fail: missing frontmatter and headings"
        assert not result["ok"]
    finally:
        Path(tmp).unlink()


if __name__ == "__main__":
    import sys
    failed = []
    for fn_name in [
        "test_positive_fixture_passes",
        "test_missing_contract_fails",
    ]:
        fn = locals().get(fn_name) or globals().get(fn_name)
        if fn is None:
            continue
        try:
            fn()
        except Exception as exc:
            failed.append((fn_name, str(exc)[:200]))
            print(f"FAIL {fn_name}: {type(exc).__name__}: {str(exc)[:120]}")
    if failed:
        sys.exit(1)
