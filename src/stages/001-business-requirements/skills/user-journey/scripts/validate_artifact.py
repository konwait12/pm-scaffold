#!/usr/bin/env python3
"""Validate the user-journey.md artifact.

This work_item is an independent work_item producing a standalone user-journey.md
artifact. The validator checks the full file content for:
  1. Lifecycle phase markers
  2. Role matrix (at least one role identified)
  3. Emotion mapping entries
  4. Path diversity (main path + at least one variant)
  5. Frontmatter and status consistency

Run: python3 validate_artifact.py <user-journey.md> [--json]
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


ARTIFACT_NAME = "user-journey.md"
ARTIFACT_GLOBS = [
    "requirements/*/001-business-requirements/01-user-journey/user-journey.md",
    "requirements/*/001-business-requirements/02-user-journey-stories/user-journey.md",
]
SKILL_ID = "user_journey"
CHECK_PREFIX = "uj"

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
        elif "lifecycle" in e.lower():
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_lifecycle", "CRITICAL",
                "用户旅程必须包含生命周期阶段定义",
                "未发现生命周期阶段标记",
                "在旅程中定义并标注 lifecycle phases（阶段）",
            )
        elif "role matrix" in e.lower() or "role" in e.lower():
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_role_matrix", "CRITICAL",
                "用户旅程必须包含角色矩阵（至少一个角色）",
                "未发现角色矩阵或角色定义",
                "在旅程中添加角色矩阵或角色定义部分",
            )
        elif "emotion" in e.lower():
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_emotion", "CRITICAL",
                "用户旅程必须包含情绪映射",
                "未发现情绪映射标记",
                "在旅程中添加情绪映射（emotion mapping）",
            )
        elif "path" in e.lower() and "diversity" in e.lower():
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.missing_path_diversity", "CRITICAL",
                "用户旅程必须包含路径多样性（主路径 + 至少一个变体）",
                "未发现路径变体或多样性",
                "添加主路径和至少一条变体路径（路径分叉）",
            )
        elif "ST-" in e or "ST-XXX" in e:
            cid, sev, exp, act, fix = (
                f"{CHECK_PREFIX}.story_traceability", "HIGH",
                "用户旅程应追溯到对应的用户故事 ST-XXX",
                "未发现 ST-XXX 故事追溯",
                "在旅程节点或路径上标注对应的 ST-XXX 引用",
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
                "旅程内容应引用来源材料 SRC-XXX",
                "未发现 SRC-XXX 来源引用",
                "在旅程节点中引用对应的 SRC-XXX 来源材料",
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

    # Check 1: Lifecycle phases present
    lifecycle_markers = [
        "阶段", "phase", "lifecycle", "用户旅程阶段",
        "阶段 1", "阶段 2", "阶段一", "阶段二",
    ]
    if not any(marker in text for marker in lifecycle_markers):
        errors.append("No lifecycle phase markers found in user journey")

    # Check 2: Role matrix (at least one role)
    role_markers = [
        "角色", "role", "用户角色", "actor",
        "用户画像", "persona",
    ]
    if not any(marker in text for marker in role_markers):
        errors.append("No role matrix or role definition found in user journey")

    # Check 3: Emotion mapping
    emotion_markers = [
        "情绪", "emotion", "情绪映射", "emotion map",
        "pain point", "pain-point", "痛点",
        "机会", "opportunity",
    ]
    if not any(marker in text for marker in emotion_markers):
        errors.append("No emotion mapping markers found in user journey")

    # Check 4: Path diversity (main path + variant)
    # Look for path/branch/fork markers
    path_markers = [
        "路径", "path", "流程", "flow",
        "分支", "branch", "变体", "variant",
        "分叉", "fork",
    ]
    path_marker_count = sum(1 for marker in path_markers if marker in text)
    if path_marker_count < 2:
        errors.append(
            "Insufficient path diversity: main path and at least one variant required. "
            "Add branch/fork/variant path markers."
        )

    # Check 5: Story traceability (ST-XXX) - warning only
    st_ids = re.findall(r"\bST-\d+\b", text)
    if not st_ids:
        warnings.append("No ST-XXX story traceability identifiers found in user journey")

    # Check 6: Source traceability (SRC-XXX) - warning only
    if "SRC-" not in text:
        warnings.append("No SRC-XXX source traceability identifiers found in user journey")

    # Check 7: Knowledge-state tags - warning only
    if not any(tag in text for tag in ("FACT", "DECISION", "AI_INFERENCE", "UNKNOWN")):
        warnings.append(
            "No knowledge-state tags (FACT/DECISION/AI_INFERENCE/UNKNOWN) found in user journey"
        )

    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "issues": _make_issues(errors, warnings, path)}


def resolve_artifact(path_arg: str | None) -> Path | None:
    """Explicit path wins; otherwise auto-resolve the user-journey.md."""
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
                   help="Artifact path. Default: auto-resolve user-journey.md.")
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
