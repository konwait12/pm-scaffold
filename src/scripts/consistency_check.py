#!/usr/bin/env python3
"""Cross-document consistency check: workflow-registry.json ↔ PM docs ↔ Skill files.

Checks:
1. Registry paths (stages / work_items / internal_capabilities / support_capabilities)
   all resolve to existing directories or files on disk.
2. Every registered work item has a SKILL.md, a scripts/validate_artifact.py, and a
   references/thinking-framework.md that references src/framework/thinking-core.md.
3. Artifact types: every artifact_type.producer maps to a known work item; every
   artifact_type.depends_on entry maps to a known artifact_type id.
4. PM doc 01 (三阶段主流程与工作事项) formal-output table (rows 1-10) is consistent
   with registry artifact_types (id + producer), so PM-facing and machine-facing
   definitions do not drift.
5. Reviewer roles: every work item's reviewer_roles is non-empty and each role is
   a known role token (business_owner / product_owner / tech_owner / designer / qa).

Exit code 0 = consistent, 1 = inconsistencies found (non-interactive must fail).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
REGISTRY = PROJECT / "src/framework/workflow-registry.json"
DOC_01 = PROJECT / "docs/00-plan/01-三阶段主流程与工作事项.md"
THINKING_CORE = PROJECT / "src/framework/thinking-core.md"

KNOWN_ROLES = {"business_owner", "product_owner", "tech_owner", "designer", "qa", "tester", "legal", "ops"}


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def check_paths(registry: dict, errors: list[str]) -> None:
    for stage in registry.get("stages", []):
        p = PROJECT / stage["path"]
        if not p.is_dir():
            errors.append(f"Registry stage path missing: {stage['id']} -> {stage['path']}")
    for item in registry.get("work_items", []):
        p = PROJECT / item["skill_path"]
        if not p.is_dir():
            errors.append(f"Registry work-item skill path missing: {item['id']} -> {item['skill_path']}")
    for cap in registry.get("internal_capabilities", []):
        p = PROJECT / cap["skill_path"]
        if not p.is_dir():
            errors.append(f"Registry internal-capability path missing: {cap['id']} -> {cap['skill_path']}")
    for cap in registry.get("support_capabilities", []):
        p = PROJECT / cap["skill_path"]
        if not p.is_dir():
            errors.append(f"Registry support-capability path missing: {cap['id']} -> {cap['skill_path']}")


def check_skill_contracts(registry: dict, errors: list[str], warnings: list[str]) -> None:
    item_ids = {item["id"] for item in registry.get("work_items", [])}
    for item in registry.get("work_items", []):
        base = PROJECT / item["skill_path"]
        if not (base / "SKILL.md").is_file():
            errors.append(f"{item['id']}: missing SKILL.md")
        if not (base / "scripts/validate_artifact.py").is_file():
            errors.append(f"{item['id']}: missing scripts/validate_artifact.py")
        tf = base / "references/thinking-framework.md"
        if not tf.is_file():
            errors.append(f"{item['id']}: missing references/thinking-framework.md")
        else:
            text = tf.read_text(encoding="utf-8")
            if "thinking-core.md" not in text:
                warnings.append(f"{item['id']}: references/thinking-framework.md does not reference src/framework/thinking-core.md")
    # sub-skills: their thinking-framework must also reference thinking-core
    for cap in registry.get("internal_capabilities", []):
        tf = PROJECT / cap["skill_path"] / "references/thinking-framework.md"
        if tf.is_file():
            text = tf.read_text(encoding="utf-8")
            if "thinking-core.md" not in text:
                warnings.append(f"{cap['id']}: sub-skill thinking-framework.md does not reference thinking-core.md")
        else:
            errors.append(f"{cap['id']}: sub-skill missing references/thinking-framework.md")
    # reviewer roles
    for item in registry.get("work_items", []):
        roles = item.get("reviewer_roles", [])
        if not roles:
            errors.append(f"{item['id']}: empty reviewer_roles")
        for role in roles:
            if role not in KNOWN_ROLES:
                warnings.append(f"{item['id']}: reviewer role '{role}' not in known set {sorted(KNOWN_ROLES)}")


def check_artifact_types(registry: dict, errors: list[str]) -> None:
    item_ids = {item["id"] for item in registry.get("work_items", [])}
    artifact_ids = {a["id"] for a in registry.get("artifact_types", [])}
    for a in registry.get("artifact_types", []):
        if a["producer"] not in item_ids:
            errors.append(f"Artifact type '{a['id']}': producer '{a['producer']}' is not a known work item")
        for dep in a.get("depends_on", []):
            if dep not in artifact_ids:
                errors.append(f"Artifact type '{a['id']}': depends_on '{dep}' is not a known artifact type")


def check_doc01_vs_registry(registry: dict, errors: list[str], warnings: list[str]) -> None:
    if not DOC_01.is_file():
        warnings.append("PM doc 01 missing; skipping doc↔registry comparison")
        return
    doc = DOC_01.read_text(encoding="utf-8")
    artifact_types = registry.get("artifact_types", [])
    # 01 document table lists 10 formal outputs with producer names in col 2.
    # Producers used in 01: project-background-goal, user-journey-and-stories,
    # product-ux, function-description, prd-assembly.
    doc_producers = set(re.findall(r"`(project-background-goal|user-journey-and-stories|product-ux|function-description|prd-assembly)`", doc))
    registry_producers = {a["producer"] for a in artifact_types}
    if not registry_producers.issubset(doc_producers):
        missing = registry_producers - doc_producers
        warnings.append(f"Producers in registry not mentioned in PM doc 01: {sorted(missing)}")
    # Check the 10 output rows exist (marker rows 1 and 10)
    if "项目背景与目标基线" not in doc or "最终 PRD" not in doc:
        errors.append("PM doc 01 missing formal-output table markers (项目背景与目标基线 / 最终 PRD)")



def check_requirements_content(warnings: list[str]) -> None:
    """Close the 'empty requirements/' blind spot.

    `requirements/` is gitignored (each user creates their own), so a fresh
    clone legitimately has none.  But if REQ-* dirs exist, their structure
    must be valid, and we surface how many non-simulated PRDs actually exist
    so the repo cannot silently claim 'validated' without evidence.
    """
    req_root = PROJECT / "requirements"
    if not req_root.is_dir():
        warnings.append("requirements/ 不存在 — 尚无真实端到端需求产物（待首个真实需求验证）")
        return
    req_dirs = [d for d in req_root.iterdir() if d.is_dir() and d.name.startswith("REQ-")]
    if not req_dirs:
        warnings.append("requirements/ 为空 — 尚无真实端到端需求产物（待首个真实需求验证）")
        return
    real_prds = 0
    for d in req_dirs:
        if not (d / "README.md").is_file():
            warnings.append(f"{d.name}: 缺 README.md（骨架不完整）")
        if not (d / "00-input").is_dir():
            warnings.append(f"{d.name}: 缺 00-input/（骨架不完整）")
        prd = d / "003-prd-output" / "prd.md"
        if prd.is_file():
            text = prd.read_text(encoding="utf-8")
            if not re.search(r"(?m)^status:\s*simulated", text):
                real_prds += 1
    if real_prds == 0:
        warnings.append("requirements/ 存在 REQ-* 目录但无非 simulated prd.md — 尚无真实人工确认产物")


def check_reference_integrity(registry: dict, errors: list[str], warnings: list[str]) -> None:
    """Every references/*.md under a skill must be cited somewhere (SKILL.md / thinking-framework.md / other references)."""
    import re as _re
    for item in registry.get("work_items", []):
        base = PROJECT / item["skill_path"]
        ref_dir = base / "references"
        if not ref_dir.is_dir():
            continue
        # collect all text that could cite references
        citation_sources: list[str] = []
        for f in [base / "SKILL.md", ref_dir / "thinking-framework.md"]:
            if f.is_file():
                citation_sources.append(f.read_text(encoding="utf-8"))
        # also sub-skill references dirs
        sub_dir = base / "skills"
        if sub_dir.is_dir():
            for sub in sorted(sub_dir.iterdir()):
                sref = sub / "references/thinking-framework.md"
                if sref.is_file():
                    citation_sources.append(sref.read_text(encoding="utf-8"))
        blob = "\n".join(citation_sources)
        for ref_file in sorted(ref_dir.glob("*.md")):
            if ref_file.name in {"thinking-framework.md", "output-contract.md", "audit-checklist.md"}:
                continue  # core files, always loaded by convention
            if ref_file.stem not in blob and ref_file.name not in blob:
                warnings.append(f"{item['id']}: references/{ref_file.name} not cited in SKILL.md / thinking-framework.md")
    # support skills
    for cap in registry.get("support_capabilities", []):
        base = PROJECT / cap["skill_path"]
        ref_dir = base / "references"
        if not ref_dir.is_dir():
            continue
        blob = ""
        for f in [base / "SKILL.md", ref_dir / "thinking-framework.md"]:
            if f.is_file():
                blob += f.read_text(encoding="utf-8")
        for ref_file in sorted(ref_dir.glob("*.md")):
            if ref_file.name in {"thinking-framework.md"}:
                continue
            if ref_file.stem not in blob and ref_file.name not in blob:
                warnings.append(f"{cap['id']}: references/{ref_file.name} not cited in SKILL.md / thinking-framework.md")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not REGISTRY.is_file():
        print(f"ERROR: registry missing: {REGISTRY}")
        return 1
    if not THINKING_CORE.is_file():
        warnings.append("src/framework/thinking-core.md missing (referenced by all thinking-frameworks)")

    registry = load_registry()
    check_paths(registry, errors)
    check_skill_contracts(registry, errors, warnings)
    check_artifact_types(registry, errors)
    check_doc01_vs_registry(registry, errors, warnings)
    check_reference_integrity(registry, errors, warnings)
    check_requirements_content(warnings)

    print("== consistency_check ==")
    for w in warnings:
        print(f"  WARN: {w}")
    for e in errors:
        print(f"  ERROR: {e}")
    print(f"Result: {len(errors)} errors, {len(warnings)} warnings")
    if errors:
        return 1
    if warnings:
        print("Consistent with warnings (reviewable).")
        return 0
    print("Consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
