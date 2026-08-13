#!/usr/bin/env python3
"""PRD workflow status, machine gates, and explicit human review."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from dor_check import check_item
from orchestrator import build_status
from workflow_registry import branch_capabilities, find_artifact, resolve_work_item, work_items


def run_json(script: str, req_dir: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / script), str(req_dir), "--json"],
        capture_output=True, text=True, check=False,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": result.stderr.strip() or result.stdout.strip()}


def run_property_check(artifact: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "property_check.py"), str(artifact), "--json"],
        capture_output=True, text=True, check=False,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": result.stderr.strip() or result.stdout.strip()}


ACTIVE = {"needs_user_input", "conditional_review", "ready_for_human_review"}

# Entry-assessment content signals (src/shared/intake-routing 的 6 信号落地)
ENTRY_SIGNAL_KEYWORDS = {
    "problem": ("问题", "痛点", "现状", "目标", "为什么"),
    "roles": ("角色", "用户", "部门", "干系人", "业务方", "客户"),
    "constraints": ("约束", "时间", "预算", "合规", "法律", "期限"),
    "solution": ("方案", "系统", "平台", "页面", "流程设计", "原型"),
    "features": ("功能", "模块", "能力"),
    "rules": ("规则", "条件", "触发", "计算", "权限"),
}


def entry_content_signals(req_dir: Path) -> dict[str, bool]:
    """Read 00-input material content and detect the 6 entry-assessment signals."""
    text = ""
    input_dir = req_dir / "00-input"
    if input_dir.is_dir():
        for p in sorted(input_dir.glob("*.md")):
            text += p.read_text(encoding="utf-8", errors="ignore") + "\n"
    return {name: any(k in text for k in keywords) for name, keywords in ENTRY_SIGNAL_KEYWORDS.items()}


def entry_branch_signals(req_dir: Path) -> list[dict]:
    """Entry-stage branch-skill signals derived from 00-input material."""
    input_dir = req_dir / "00-input"
    src_files = sorted(input_dir.glob("SRC-*.md")) if input_dir.is_dir() else []
    text = ""
    for p in src_files:
        text += p.read_text(encoding="utf-8", errors="ignore") + "\n"
    out: list[dict] = []
    if not src_files:
        out.append({"id": "brainstorming", "signal": "L0 无源材料，建议发散收敛", "auto_detect": False})
    if len(src_files) >= 2:
        out.append({"id": "requirement-restate", "signal": "多源材料（≥2 SRC），建议需求复述确认", "auto_detect": False})
    elif any(k in text for k in ("歧义", "不一致", "待确认", "待定", "可能", "也许")):
        out.append({"id": "requirement-restate", "signal": "材料含歧义/待确认标记，建议需求复述确认", "auto_detect": False})
    return out


def branch_skill_signals(req_dir: Path, statuses: dict) -> list[dict]:
    """Detect machine-checkable triggers for conditional/branch skills.

    Deterministic triggers: prd-publish (prd-assembly confirmed), and
    entry-stage signals from 00-input content (brainstorming / restate).
    Semantic triggers (competitive-research, solution-assessment) remain
    AI-judged and are surfaced as hints, never auto-invoked.
    """
    signals: list[dict] = []
    if statuses.get("prd-assembly") == "confirmed":
        signals.append({"id": "prd-publish", "signal": "prd-assembly confirmed", "auto_detect": True})
    if "needs_user_input" in statuses.values():
        signals.append({"id": "issue-record", "signal": "存在 needs_user_input 产物", "auto_detect": False})
    signals.extend(entry_branch_signals(req_dir))
    return signals


def init_requirement(name: str | None) -> int:
    """Create a requirement skeleton from the registry (REQ-NNN-topic-name)."""
    if not name:
        print("ERROR: init requires a requirement name like REQ-001-my-feature", file=sys.stderr)
        return 1
    if not re.fullmatch(r"REQ-\d{3}[A-Za-z0-9_-]*", name):
        print(f"ERROR: invalid requirement name '{name}' (expect REQ-NNN-topic)", file=sys.stderr)
        return 1
    req_dir = Path("requirements") / name
    if req_dir.exists():
        print(f"ERROR: {req_dir} already exists", file=sys.stderr)
        return 1
    req_dir.mkdir(parents=True, exist_ok=True)
    (req_dir / "00-input").mkdir()
    (req_dir / "99-review").mkdir()
    # stage artifact dirs derived from the registry (single source of truth)
    for item in work_items():
        (req_dir / item["artifact_dir"]).mkdir(parents=True, exist_ok=True)
    # authorized-reviewers skeleton: AI must never fill a real reviewer here
    (req_dir / "00-input" / "authorized-reviewers.json").write_text(
        json.dumps({"reviewers": []}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (req_dir / "00-input" / "source-register.md").write_text(
        "# 来源登记 (Source Register)\n\n"
        "> 登记所有原始需求材料。格式: SRC-NNN → 材料位置 / URL / 飞书链接\n\n"
        "| 来源 ID | 类型 | 位置 | 摘要 | 登记日期 | 权威范围 |\n"
        "|---|---|---|---|---|---|\n"
        "| SRC-001 | `待填写` | `待填写` | `待填写` | `待填写` | `待填写` |\n",
        encoding="utf-8",
    )
    # README index skeleton
    rows = "\n".join(
        f"| `{item['artifact_dir']}/` | `{item['id']}`: {item['name']} | ⏸ |"
        for item in work_items()
    )
    (req_dir / "README.md").write_text(
        f"# {name}\n\n"
        "> 需求产物索引\n\n"
        "## 业务一句话\n\n`待填写`\n\n"
        "## 目录索引\n\n"
        "| 目录 | 内容 | 状态 |\n|---|---|---|\n"
        "| `00-input/` | 原始需求材料 + authorized-reviewers.json | `待填写` |\n"
        f"{rows}\n"
        "| `99-review/` | 评审记录 | ⏸ |\n",
        encoding="utf-8",
    )
    print(f"Created {req_dir}")
    print(f"  Next: put source materials in {req_dir}/00-input/, then run")
    print(f"        python3 src/scripts/pipeline.py {req_dir} status")
    return 0


def artifact_content_hash(text: str) -> str:
    canonical = re.sub(
        r"(?m)^(status|reviewer|reviewed_at|confirmed_at):.*$",
        r"\1: <review-metadata>",
        text,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def machine_gate(req_dir: Path, item: dict) -> dict:
    result = check_item(req_dir, item)
    records = run_json("branch_validator.py", req_dir)
    cross = {"ok": True, "skipped": item["id"] != "prd-assembly"}
    if item["id"] == "prd-assembly":
        cross = run_json("traceability_check.py", req_dir)
    # logical-completeness property check only applies to function-description
    prop = {"ok": True, "skipped": item["id"] != "function-description"}
    if item["id"] == "function-description":
        art = find_artifact(req_dir, item)
        prop = run_property_check(art) if art else {"ok": False, "skipped": False, "error": "artifact not found"}
    ok = (result["dor_pass"] and result["dod_pass"] and bool(cross.get("ok"))
          and bool(records.get("ok")) and bool(prop.get("ok")))
    return {"ok": ok, "work_item": result, "cross_trace": cross, "records": records, "property": prop}


def load_authorized_reviewer(req_dir: Path, reviewer_id: str, reviewer: str, reviewer_role: str) -> dict | None:
    registry = req_dir / "00-input" / "authorized-reviewers.json"
    if not registry.is_file():
        return None
    try:
        entries = json.loads(registry.read_text(encoding="utf-8")).get("reviewers", [])
    except (json.JSONDecodeError, OSError):
        return None
    for entry in entries:
        if (entry.get("id") == reviewer_id and entry.get("name") == reviewer
                and reviewer_role in entry.get("roles", [])):
            return entry
    return None


def review(req_dir: Path, item: dict, decision: str, reviewer: str, reviewer_id: str,
           reviewer_role: str, comments: str, waivers: list[str] | None = None) -> int:
    normalized_reviewer = reviewer.strip().lower()
    if (not normalized_reviewer or normalized_reviewer in {"ai", "待确认", "待评审"}
            or "simulat" in normalized_reviewer or "模拟" in reviewer):
        print("ERROR: a real named human reviewer is required", file=sys.stderr)
        return 1
    if not load_authorized_reviewer(req_dir, reviewer_id, reviewer, reviewer_role):
        print("ERROR: reviewer id, name, and role must match 00-input/authorized-reviewers.json", file=sys.stderr)
        return 1
    if reviewer_role not in item.get("reviewer_roles", []):
        print(f"ERROR: role {reviewer_role} cannot approve {item['id']}", file=sys.stderr)
        return 1
    artifact = find_artifact(req_dir, item)
    if not artifact:
        print("ERROR: artifact not found", file=sys.stderr)
        return 1
    current_status = re.search(r"(?m)^status:\s*(\S+)", artifact.read_text(encoding="utf-8"))
    current_status = current_status.group(1) if current_status else "unknown"
    if decision == "approve" and current_status != "ready_for_human_review":
        print(f"ERROR: approval requires ready_for_human_review, got {current_status}", file=sys.stderr)
        return 1
    gate = machine_gate(req_dir, item)
    if decision == "approve":
        result = gate.get("work_item", {}).get("result", {})
        issues = result.get("issues", [])
        waiver_map = {}
        for w in (waivers or []):
            if "=" in w:
                code, reason = w.split("=", 1)
                waiver_map[code.strip()] = reason.strip()
        for issue in issues:
            if issue.get("severity") == "waiver_required" and issue.get("waivable"):
                code = issue.get("code", "")
                if code not in waiver_map:
                    print(f"ERROR: waiver_required issue '{issue.get('message','')}' needs --waive {code}=<reason>", file=sys.stderr)
                    return 1
    if decision == "approve" and not gate["ok"]:
        print(json.dumps(gate, ensure_ascii=False, indent=2))
        print("ERROR: machine gates must pass before approval", file=sys.stderr)
        return 1
    review_dir = req_dir / "99-review"
    review_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    artifact_text = artifact.read_text(encoding="utf-8")
    artifact_hash = artifact_content_hash(artifact_text)
    artifact_meta = re.search(r"(?m)^version:\s*[\"']?([^\s\"']+)", artifact_text)
    artifact_version = artifact_meta.group(1) if artifact_meta else "unknown"
    record = review_dir / f"review-{item['id']}-{now[:10]}.md"
    suffix = 1
    while record.exists():
        record = review_dir / f"review-{item['id']}-{now[:10]}-{suffix}.md"
        suffix += 1
    record.write_text(
        "\n".join([
            f"# Review: {item['name']}", "",
            f"- work_item: {item['id']}", f"- artifact: {artifact.relative_to(req_dir)}",
            f"- artifact_version: {artifact_version}", f"- artifact_content_sha256: {artifact_hash}",
            f"- decision: {decision}", f"- reviewer: {reviewer}", f"- reviewer_id: {reviewer_id}",
            f"- reviewer_role: {reviewer_role}", f"- reviewed_at: {now}",
            f"- comments: {comments or '无'}", ""
        ]), encoding="utf-8",
    )
    text = artifact_text
    target_status = "confirmed" if decision == "approve" else "draft"
    text = re.sub(r"(?m)^status:\s*\S+", f"status: {target_status}", text, count=1)
    if re.search(r"(?m)^reviewer:", text):
        text = re.sub(r"(?m)^reviewer:.*$", f"reviewer: {reviewer}", text, count=1)
    if re.search(r"(?m)^reviewed_at:", text):
        text = re.sub(r"(?m)^reviewed_at:.*$", f"reviewed_at: {now}", text, count=1)
    if decision == "approve" and re.search(r"(?m)^confirmed_at:", text):
        text = re.sub(r"(?m)^confirmed_at:.*$", f"confirmed_at: {now}", text, count=1)
    artifact.write_text(text, encoding="utf-8")
    print(f"Recorded {decision}: {record.relative_to(req_dir)}")
    return 0 if decision == "approve" else 2


def main() -> int:
    # `pipeline.py init <name>` — init is the action, <name> is the target.
    if len(sys.argv) >= 2 and sys.argv[1] == "init":
        return init_requirement(sys.argv[2] if len(sys.argv) > 2 else None)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("req_dir", type=Path)
    parser.add_argument("action", nargs="?", choices=["status", "entry", "gate", "review", "reflow"], default="status")
    parser.add_argument("--stage")
    parser.add_argument("--work-item", choices=[item["id"] for item in work_items()])
    parser.add_argument("--wave", type=int, choices=range(1, 6), help="Deprecated compatibility alias")
    parser.add_argument("--yes", action="store_true", help="Non-interactive machine checks only; never human approval")
    parser.add_argument("--decision", choices=["approve", "changes"])
    parser.add_argument("--reviewer")
    parser.add_argument("--reviewer-id")
    parser.add_argument("--reviewer-role")
    parser.add_argument("--waive", action="append", default=[], help="Waive a waiver_required issue: CODE=reason")
    parser.add_argument("--apply", action="store_true", help="reflow: actually flip downstream to superseded (default is dry-run)")
    parser.add_argument("--comments", default="")
    parser.add_argument("--preset", help="Template preset to use (resolved via src/templates/resolver.py)")
    parser.add_argument("--variant", choices=["standard", "executive", "technical"], default="standard", help="PRD output variant (prd-assembly only)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.req_dir.is_dir():
        print(f"ERROR: {args.req_dir} is not a directory", file=sys.stderr)
        return 1
    if args.wave:
        print("DEPRECATED: --wave will be removed after the v3 compatibility baseline.", file=sys.stderr)
    if args.yes:
        print("NOTICE: --yes runs machine checks only and does not bypass human review.", file=sys.stderr)
    if args.action == "status":
        result = build_status(args.req_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if args.action == "entry":
        result = build_status(args.req_dir)
        input_dir = args.req_dir / "00-input"
        src_count = len(list(input_dir.glob("SRC-*.md"))) if input_dir.is_dir() else 0
        artifact_count = sum(1 for s in result["work_items"].values() if s not in ("not_created", ""))
        confirmed_count = sum(1 for s in result["work_items"].values() if s == "confirmed")

        # If workflow invalid (over-active items), surface the fix first.
        if result["invalid_active_items"]:
            maturity = "⚠️ 越级待审"
            entry = f"先修正: 将 {', '.join(result['invalid_active_items'])} 降为 draft，确认 {result['active_work_item']}"
        elif confirmed_count == 5:
            maturity, entry = "L4 已全部确认", "Stage 3 (prd-publish 或重跑)"
        elif result["work_items"].get("product-ux") in ACTIVE:
            maturity, entry = "L3 产品方案已成型", "Stage 2 (product-ux 续跑)"
        elif result["work_items"].get("user-journey-and-stories") in ACTIVE:
            maturity, entry = "L1/L2 业务需求已成型", "Stage 1 (user-journey-and-stories 续跑)"
        elif result["work_items"].get("project-background-goal") in ACTIVE:
            maturity, entry = "L1 背景已成型", "Stage 1 (project-background-goal 续跑)"
        elif artifact_count > 0:
            maturity, entry = f"L1 已有 {artifact_count} 份产物", "Stage 1 (user-journey-and-stories)"
        elif src_count > 0:
            sig = entry_content_signals(args.req_dir)
            if sig["features"] and sig["rules"]:
                maturity, entry = "L3 材料含功能清单与业务规则", "Stage 1 (project-background-goal 快速起草)"
            elif sig["solution"]:
                maturity, entry = "L2 材料含产品级方案", "Stage 1 (project-background-goal)"
            else:
                maturity, entry = f"L1 有 {src_count} 份原始材料（内容信号 {sum(sig.values())}/6）", "Stage 1 (project-background-goal)"
        else:
            maturity, entry = "L0 仅想法", "brainstorming（发散收敛）→ Stage 1"

        entry_blocked = None
        if not result["invalid_active_items"] and confirmed_count == 0 and not result["work_items"].get("project-background-goal") in ACTIVE:
            if src_count == 0:
                entry_blocked = "L0 材料不足：先发散候选（brainstorming）或补充材料，再进入 Stage 1"
            elif sum(entry_content_signals(args.req_dir).values()) < 2:
                entry_blocked = "L1 材料稀疏：建议补料或 requirement-restate（需求复述）确认理解"

        print(json.dumps({
            "requirement": result["requirement"],
            "source_count": src_count,
            "artifact_count": artifact_count,
            "confirmed_count": confirmed_count,
            "maturity": maturity,
            "recommended_entry": entry,
            "entry_blocked": entry_blocked,
            "content_signals": entry_content_signals(args.req_dir),
            "workflow_valid": result["workflow_valid"],
            "active_work_item": result["active_work_item"],
            "invalid_active_items": result["invalid_active_items"],
            "next_work_item": result["next_work_item"],
            "blockers": result["blockers"],
            "branch_skill_signals": branch_skill_signals(args.req_dir, result["work_items"]),
        }, ensure_ascii=False, indent=2))
        return 0
    if not (args.work_item or args.wave):
        print("ERROR: --work-item is required", file=sys.stderr)
        return 1
    item = resolve_work_item(args.work_item, args.wave)
    if args.stage and args.stage != item["stage"]:
        print(f"ERROR: {item['id']} belongs to {item['stage']}", file=sys.stderr)
        return 1
    if args.action == "gate":
        result = machine_gate(args.req_dir, item)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1
    if args.action == "reflow":
        results = {"work_item": item["id"], "impact": [], "applied": bool(args.apply), "superseded": []}
        for downstream in work_items():
            if downstream["order"] > item["order"]:
                dart = find_artifact(args.req_dir, downstream)
                if dart:
                    text = dart.read_text(encoding="utf-8")
                    fm = re.search(r"(?m)^status:\s*(\S+)", text)
                    status = fm.group(1) if fm else "unknown"
                    if status in ("confirmed", "ready_for_human_review"):
                        action = "superseded" if args.apply else "will become superseded on apply"
                        results["impact"].append({"id": downstream["id"], "status": status, "action": action})
                        if args.apply:
                            new_text = re.sub(r"(?m)^status:\s*\S+", "status: superseded", text, count=1)
                            dart.write_text(new_text, encoding="utf-8")
                            results["superseded"].append(downstream["id"])
        if args.apply and results["superseded"]:
            now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            review_dir = args.req_dir / "99-review"
            review_dir.mkdir(parents=True, exist_ok=True)
            record = review_dir / f"change-record-reflow-{now[:10]}.md"
            suffix = 1
            while record.exists():
                record = review_dir / f"change-record-reflow-{now[:10]}-{suffix}.md"
                suffix += 1
            record.write_text(
                "\n".join([
                    f"# Change Record: reflow {item['id']}", "",
                    f"- trigger: {item['id']} changed", f"- applied_at: {now}",
                    f"- superseded: {', '.join(results['superseded'])}", "",
                    "- decision_id: 待填写（DEC-NNN，对齐 src/templates/others/decision-record.md）",
                    "- decider: 待填写", "- rationale: 待填写", "",
                    "Downstream artifacts were flipped to `superseded`; they must be re-validated",
                    "after the earliest affected work item is re-confirmed.", "",
                ]), encoding="utf-8",
            )
            results["change_record"] = str(record.relative_to(args.req_dir))
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0
    if not args.decision or not args.reviewer or not args.reviewer_id or not args.reviewer_role:
        print("ERROR: review requires --decision, --reviewer, --reviewer-id, and --reviewer-role", file=sys.stderr)
        return 1
    return review(args.req_dir, item, args.decision, args.reviewer, args.reviewer_id, args.reviewer_role, args.comments, args.waive)


if __name__ == "__main__":
    sys.exit(main())
