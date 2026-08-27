#!/usr/bin/env python3
"""Validate the user-stories.md artifact.

This work_item is an independent work_item producing a standalone user-stories.md
artifact. The validator checks the full file content for:
  1. Story format compliance (ST-XXX identifiers)
  2. MoSCoW priority labels (Must/Should/Could/Won't)
  3. Coverage matrix (stories traceable to journey)
  4. Scope baseline (In/Out/Deferred/Conditional)
  5. Frontmatter and status consistency

Run: python3 validate_artifact.py <user-stories.md> [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def _bootstrap_scripts() -> None:
    import sys as _sys
    p = Path(__file__).resolve().parent
    while p.parent != p:
        cand = p / "src" / "scripts"
        if (cand / "validation_errors.py").is_file():
            if str(cand) not in _sys.path:
                _sys.path.insert(0, str(cand))
            return
        p = p.parent

_bootstrap_scripts()
from validation_errors import make_issue
from product_quality import validate_quality_record


ARTIFACT_NAME = "user-stories.md"
ARTIFACT_GLOBS = [
    "requirements/*/001-business-requirements/01-user-journey/user-stories.md",
    "requirements/*/001-business-requirements/02-user-journey-stories/user-stories.md",
]
SKILL_ID = "user_stories"
CHECK_PREFIX = "us"

VALID_STATUSES = {
    "draft",
    "needs_user_input",
    "conditional_review",
    "ready_for_human_review",
    "superseded",
    "legacy_unverified",
    "simulated",
}


def _project_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "src" / "framework" / "workflow-registry.json").is_file():
            return parent
    return p.parents[8]


def parse_frontmatter(text: str) -> dict[str, str]:
    text = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.DOTALL)
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    result: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        k, v = line.split(":", 1)
        result[k.strip()] = v.strip().strip('"\'')
    return result


def _moscow_labels(text: str) -> dict[str, int]:
    """Count MoSCoW labels found in text."""
    labels = {
        "Must": 0, "Should": 0, "Could": 0, "Won't": 0,
        "Must have": 0, "Should have": 0, "Could have": 0, "Won't have": 0,
        "M": 0, "S": 0, "C": 0, "W": 0,
    }
    for label, count in labels.items():
        labels[label] = len(re.findall(r"\b" + re.escape(label) + r"\b", text, re.IGNORECASE))
    return labels


def _scope_baseline_markers(text: str) -> dict[str, bool]:
    """Check for scope baseline markers."""
    return {
        "In": bool(re.search(r"\bIn\b.*\bscope\b", text, re.IGNORECASE)),
        "Out": bool(re.search(r"\bOut\b.*\bscope\b", text, re.IGNORECASE)),
        "Deferred": bool(re.search(r"\bDeferred\b", text, re.IGNORECASE)),
        "Conditional": bool(re.search(r"\bConditional\b", text, re.IGNORECASE)),
    }


def _make_issues(errors: list[str], warnings: list[str], path: Path) -> list[dict]:
    issues: list[dict] = []
    for e in errors:
        if e.startswith("File not found"):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.file_not_found", "CRITICAL",
                "产物文件必须存在且可读", f"文件不存在: {e}",
                "确认产物路径正确, 或先创建对应的 artifact 文件",
            )
        elif e.startswith("status 'confirmed' is not allowed"):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.status_confirmed", "CRITICAL",
                "子 skill 输出永远不允许 status=confirmed",
                f"实际状态: {e}",
                "将状态改为 draft / ready_for_human_review 等, 由 pipeline.py review --decision approve 负责置为 confirmed",
            )
        elif e.startswith("Invalid status"):
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.status_invalid", "CRITICAL",
                "frontmatter status 必须在白名单内（且不含 confirmed）",
                f"非法状态: {e}",
                "修正 frontmatter 的 status 字段为合法取值",
            )
        elif "ST-" in e or "story identifier" in e.lower():
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_story_ids", "CRITICAL",
                "用户故事必须包含 ST-XXX 标识符（占位符不算）",
                "未发现 ST-XXX 故事标识符",
                "为每个故事卡片补充形如 ST-001 的稳定标识符",
            )
        elif "MoSCoW" in e or "moscow" in e.lower():
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_moscow", "CRITICAL",
                "用户故事必须标注 MoSCoW 优先级（M/S/C/W）",
                "未发现 MoSCoW 优先级标记",
                "为每个故事标注 Must/Should/Could/Won't (M/S/C/W) 优先级",
            )
        elif "scope baseline" in e.lower() or "in/out" in e.lower():
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_scope_baseline", "CRITICAL",
                "用户故事必须包含范围基线（In/Out/Deferred/Conditional）",
                "未发现范围基线标记",
                "在故事集中添加 In/Out/Deferred/Conditional 范围基线定义",
            )
        elif "UJ-" in e or "journey" in e.lower():
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.journey_traceability", "HIGH",
                "每个故事应追溯到对应的用户旅程 UJ-XXX",
                "未发现 UJ-XXX 旅程追溯",
                "在故事卡片上标注对应的 UJ-XXX 旅程节点",
            )
        else:
            cid, sev, exp, act, fix = f"{CHECK_PREFIX}.error", "CRITICAL", None, None, None
        issues.append(make_issue(
            severity=sev, check_id=cid, family=SKILL_ID,
            location=str(path), message=e,
            expected=exp, actual=act, repair_hint=fix,
        ))
    for w in warnings:
        if w.startswith("No frontmatter"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_frontmatter",
                "产物应带 YAML frontmatter 以便校验状态",
                "未发现 frontmatter",
                "在产物头部补充 YAML frontmatter（含 status 字段）",
            )
        elif w.startswith("No knowledge-state tags"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_ks_tags",
                "可追溯内容应带有知识状态标签 (FACT/DECISION/AI_INFERENCE/UNKNOWN)",
                "全文未发现任何知识状态标签",
                "在事实/决定/推断内容旁标注 FACT / DECISION / AI_INFERENCE / UNKNOWN",
            )
        elif w.startswith("No SRC-"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_src",
                "故事内容应引用来源材料 SRC-XXX",
                "未发现 SRC-XXX 来源引用",
                "在故事中引用对应的 SRC-XXX 来源材料",
            )
        elif w.startswith("No Must"):
            cid, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_must_stories",
                "MoSCoW 中应至少有一个 Must story",
                "未发现任何 Must story",
                "确保核心用户需求至少有一个 Must story",
            )
        else:
            cid, exp, act, fix = f"{CHECK_PREFIX}.warning", None, None, None
        issues.append(make_issue(
            severity="MEDIUM", check_id=cid, family=SKILL_ID,
            location=str(path), message=w,
            expected=exp, actual=act, repair_hint=fix, blocking=False,
        ))
    return issues


def validate(path: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": [],
                "issues": _make_issues([f"File not found: {path}"], [], path)}

    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    status = meta.get("status")

    if not meta:
        warnings.append("No frontmatter found; artifact status cannot be verified")
    elif status == "confirmed":
        errors.append(
            "status 'confirmed' is not allowed for this work_item output; "
            "only pipeline.py review --decision approve may set confirmed"
        )
    elif status and status not in VALID_STATUSES:
        errors.append(
            f"Invalid status '{status}'. Valid (excluding confirmed): "
            f"{', '.join(sorted(VALID_STATUSES))}"
        )

    # Check 1: Story identifiers (ST-XXX)
    st_ids = re.findall(r"\bST-\d+\b", text)
    if not st_ids:
        errors.append("No ST-XXX story identifiers found in user stories")

    # Check 2: MoSCoW labels
    moscow = _moscow_labels(text)
    has_moscow = any(v > 0 for v in moscow.values())
    if not has_moscow:
        errors.append(
            "No MoSCoW priority markers (Must/Should/Could/Won't or M/S/C/W) found. "
            "Each story must be labeled with a MoSCoW priority."
        )
    # Warning if no Must stories
    must_count = moscow["Must"] + moscow["Must have"] + moscow["M"]
    if must_count == 0 and st_ids:
        warnings.append(
            "No Must stories found. Verify that core user needs are covered by at least one Must story."
        )

    # Check 3: Journey traceability (UJ-XXX) - warning only
    uj_ids = re.findall(r"\bUJ-\d+\b", text)
    if not uj_ids and st_ids:
        warnings.append("No UJ-XXX journey traceability identifiers found in user stories")

    # Check 3.5: ST↔G same-row link (B5 pre-check)
    # traceability_check.REQUIRED_EDGES enforces story→goal at PRD gate; catching
    # it here at submission time avoids a post-confirmation reflow cascade.
    st_without_goal = []
    for line in text.splitlines():
        if re.match(r"^\s*\|.*\bST-\d+\b", line):
            if not re.search(r"\bG-?\d+\b", line):
                st_without_goal.append(
                    re.search(r"\bST-\d+\b", line).group(0)
                )
    if st_without_goal:
        errors.append(
            "ST rows missing same-row goal link (G-XXX): "
            + ", ".join(sorted(set(st_without_goal)))
            + ". Each story row must carry its upstream goal ID on the same "
            + "line (traceability required_edges story→goal)."
        )

    # Check 4: Scope baseline
    scope = _scope_baseline_markers(text)
    has_scope = any(scope.values())
    if not has_scope and st_ids:
        warnings.append(
            "No scope baseline markers (In/Out/Deferred/Conditional) found. "
            "Add scope baseline to establish what is in scope, out of scope, deferred, and conditional."
        )

    # Check 5: Source traceability (SRC-XXX) - warning only
    if "SRC-" not in text:
        warnings.append("No SRC-XXX source traceability identifiers found in user stories")

    # Check 6: Knowledge-state tags - warning only
    if not any(tag in text for tag in ("FACT", "DECISION", "AI_INFERENCE", "UNKNOWN")):
        warnings.append(
            "No knowledge-state tags (FACT/DECISION/AI_INFERENCE/UNKNOWN) found in user stories"
        )

    quality_errors, quality_warnings = validate_quality_record(
        text, required=(meta.get("quality_contract_version") == "1" and status in {"ready_for_human_review", "confirmed"})
    )
    errors.extend(quality_errors)
    warnings.extend(quality_warnings)
    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "issues": _make_issues(errors, warnings, path)}


def resolve_artifact(path_arg: str | None) -> Path | None:
    """Explicit path wins; otherwise auto-resolve the user-stories.md."""
    if path_arg:
        return Path(path_arg)
    root = _project_root()
    for glob in ARTIFACT_GLOBS:
        for hit in sorted(root.glob(glob)):
            return hit
    return None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path, nargs="?", default=None,
                   help="Artifact path. Default: auto-resolve user-stories.md.")
    p.add_argument("--json", action="store_true", dest="j")
    args = p.parse_args()

    path = resolve_artifact(args.artifact)
    if path is None:
        msg = (
            f"No artifact provided and no {ARTIFACT_NAME} found under requirements/*/. "
            f"Run: python3 validate_artifact.py <{ARTIFACT_NAME}> [--json]"
        )
        if args.j:
            print(json.dumps({"ok": False, "errors": [msg], "warnings": []},
                             ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: {msg}")
        return 2

    r = validate(path)
    if args.j:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("PASS" if r["ok"] else "FAIL")
        for e in r["errors"]:
            print(f"ERROR: {e}")
        for w in r["warnings"]:
            print(f"WARNING: {w}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
