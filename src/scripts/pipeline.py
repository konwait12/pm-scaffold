#!/usr/bin/env python3
"""PRD workflow status, machine gates, and explicit human review."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from dor_check import check_item
from orchestrator import build_status
from workflow_registry import (
    artifact_content_hash,
    branch_capabilities,
    find_artifact,
    read_frontmatter,
    resolve_work_item,
    assert_work_item_in_tier,
    canonical_applicability_evidence,
    require_persisted_tier,
    resolve_branch_capability,
    resume_work_item_for_tier,
    tier_for_req,
    work_items,
    work_items_for_tier,
)

import audit_log
import hash_anchor
from l0_prd_projection import build_projection, write_projection


def run_script_json(script: Path, target: Path, *extra_args: str) -> dict:
    """Run an arbitrary validator script against a target path with `--json`.

    Unlike `run_json` (which resolves scripts under src/scripts/), this helper
    accepts a full script path so shared validators (e.g. the issue-record
    validator under src/shared/clarify/...) can be invoked from the gate.
    """
    result = subprocess.run(
        [sys.executable, str(script), str(target), "--json", *extra_args],
        capture_output=True, text=True, check=False,
        encoding="utf-8", errors="replace",
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": result.stderr.strip() or result.stdout.strip()}


def run_json(script: str, req_dir: Path) -> dict:
    return run_script_json(Path(__file__).parent / script, req_dir)


def run_property_check(artifact: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "property_check.py"), str(artifact), "--json"],
        capture_output=True, text=True, check=False,
        encoding="utf-8", errors="replace",
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": result.stderr.strip() or result.stdout.strip()}


ACTIVE = {"needs_user_input", "conditional_review", "ready_for_human_review"}

# issue-record: 跨阶段问题清单是「每个案例必备的稳定产物」（非可选分支）。
# 校验器位于 shared 下（src/shared/clarify/skills/issue-record/），与主干
# work-item 校验器（src/scripts/ 下）路径不同，需用 run_script_json 单独调用。
ISSUE_RECORD_VALIDATOR = (
    Path(__file__).parent.parent
    / "shared/clarify/skills/issue-record/scripts/validate_artifact.py"
)
ISSUE_RECORD_PATH = "99-review/support/issue-record.md"


def check_issue_record(req_dir: Path) -> dict:
    """校验 L1/L2 的、按持久化档位派生的 issue-record。

    1. L0 不应调用本函数；它不创建 issue-record。
    2. L1/L2 的 issue-record 必须存在，且 validator 用 req_dir 的 intake tier
       校验 B3 阶段收口表是否与当前档位 work item 集合精确匹配。
    3. 校验结果并入返回 dict 的 `issue_record` 字段。
    """
    path = req_dir / ISSUE_RECORD_PATH
    if not path.is_file():
        return {
            "ok": False,
            "path": ISSUE_RECORD_PATH,
            "error": f"{ISSUE_RECORD_PATH} 不存在（L1/L2 B3 治理产物，缺失即 gate 失败）",
        }
    result = run_script_json(ISSUE_RECORD_VALIDATOR, path, "--req-dir", str(req_dir))
    result["path"] = str(path.relative_to(req_dir).as_posix())
    result["ok"] = bool(result.get("ok"))
    return result


# Entry-assessment content signals (src/shared/intake-routing 的 6 信号落地)
ENTRY_SIGNAL_KEYWORDS = {
    "problem": ("问题", "痛点", "现状", "目标", "为什么"),
    "roles": ("角色", "用户", "部门", "干系人", "业务方", "客户"),
    "constraints": ("约束", "时间", "预算", "合规", "法律", "期限"),
    "solution": ("方案", "系统", "平台", "页面", "流程设计", "原型"),
    "features": ("功能", "模块", "能力"),
    "rules": ("规则", "条件", "触发", "计算", "权限"),
}

# 需求难度是用户在入口处选择的交互维度，和持久化 process tier 分开。
# 难度只用于决定是否展示档位建议：低难度不打开档位建议入口；中/高难度
# 才展示一个可审计的建议。建议永远不会写入 process_tier，也不会创建目录。
DIFFICULTY_LEVELS = {"low", "medium", "high"}


def normalize_difficulty(value: str | None) -> str | None:
    """Normalize CLI/frontmatter difficulty values without guessing missing input."""
    if not value:
        return None
    aliases = {"低": "low", "中": "medium", "高": "high", "低难度": "low",
               "中难度": "medium", "高难度": "high"}
    normalized = aliases.get(value.strip().lower(), value.strip().lower())
    return normalized if normalized in DIFFICULTY_LEVELS else None


def tier_recommendation(req_dir: Path, difficulty: str | None) -> dict:
    """Return a non-authoritative tier suggestion for the difficulty entry.

    The recommendation is deliberately read-only.  A human must still pass
    ``--process-tier`` to ``init``; no recommendation is allowed to mutate the
    intake decision or switch an existing requirement between tiers.
    """
    level = normalize_difficulty(difficulty)
    if level is None:
        return {
            "triggered": False,
            "difficulty": difficulty or "未选择",
            "recommendation": None,
            "selection_required": False,
            "reason": "未选择需求难度，不展示档位建议入口。",
        }
    if level == "low":
        return {
            "triggered": False,
            "difficulty": level,
            "recommendation": None,
            "selection_required": False,
            "reason": "低难度需求不触发档位建议入口；如需创建 REQ，直接由人工确认 L0。",
        }
    if level == "high":
        return {
            "triggered": True,
            "difficulty": level,
            "recommendation": "L2",
            "selection_required": True,
            "reason": "高难度默认建议完整状态化路径 L2；仍需人工确认。",
        }

    # 中难度默认建议 L1；输入中已出现状态、异常、校验、多角色、敏感或
    # 多系统信号时，建议升级 L2。这里只提供提示，不代替资格矩阵。
    input_dir = req_dir / "00-input"
    text = ""
    if input_dir.is_dir():
        for path in sorted(input_dir.glob("SRC-*.md")):
            text += path.read_text(encoding="utf-8", errors="ignore") + "\n"
    hard_signals = ("状态", "状态机", "异常", "恢复", "校验", "权限", "PII", "敏感",
                    "合规", "多角色", "多系统", "迁移", "资金")
    if any(signal in text for signal in hard_signals):
        return {
            "triggered": True,
            "difficulty": level,
            "recommendation": "L2",
            "selection_required": True,
            "reason": "中难度材料命中状态/风险/多系统等升级信号，建议 L2；需人工确认。",
        }
    return {
        "triggered": True,
        "difficulty": level,
        "recommendation": "L1",
        "selection_required": True,
        "reason": "中难度且暂未命中硬升级信号，建议受限标准路径 L1；需人工确认。",
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
        out.append({"id": "brainstorming", "signal": "无源材料，建议发散收敛（头脑风暴）；材料成熟度不等于交付档位", "auto_detect": False})
    if len(src_files) >= 2:
        out.append({"id": "requirement-restate", "signal": "多源材料（≥2 SRC），建议需求复述确认", "auto_detect": False})
    elif any(k in text for k in ("歧义", "不一致", "待确认", "待定", "可能", "也许")):
        out.append({"id": "requirement-restate", "signal": "材料含歧义/待确认标记，建议需求复述确认", "auto_detect": False})
    return out


def branch_skill_signals(req_dir: Path, statuses: dict) -> list[dict]:
    """Detect machine-checkable triggers for conditional/branch skills.

    Deterministic triggers: entry-stage signals from 00-input content
    (requirement-restate 发散/复述). Semantic triggers (competitive-research,
    feasibility-analysis) remain
    AI-judged and are surfaced as hints, never auto-invoked.
    """
    signals: list[dict] = []
    if "needs_user_input" in statuses.values():
        signals.append({"id": "issue-record", "signal": "存在 needs_user_input 产物", "auto_detect": False})
    signals.extend(entry_branch_signals(req_dir))
    return signals


# Optional plugin root for installations where lark-cli is not on PATH. A
# checkout must not depend on a particular user's home directory.
LARK_PLUGIN_ROOT = Path(os.environ["PM_SCAFFOLD_LARK_PLUGIN_ROOT"]).expanduser() \
    if os.environ.get("PM_SCAFFOLD_LARK_PLUGIN_ROOT") else None


def _detect_feishu_capability() -> dict:
    """扫描本机是否具备飞书能力（lark-cli / lark 插件）。

    返回结构：``{"lark_cli": bool, "lark_plugin": bool, "version": str}``

    扫描规则：
        1. ``which lark-cli``（macOS PATH 已注入时优先命中）；
        2. 可选兜底：检查 ``PM_SCAFFOLD_LARK_PLUGIN_ROOT/<ver>/bin/lark-cli``；
        3. ``lark_cli`` 为真时跑 ``lark-cli --version`` 捕获 stdout。

    刻意不跑 ``lark-cli auth status``：宿主环境托管外部凭证注入下可能报
    "Credential management is not supported" —— 用 ``--version`` 判断可执行性即可。
    """
    lark_plugin = LARK_PLUGIN_ROOT is not None and LARK_PLUGIN_ROOT.is_dir()
    lark_cli = False
    version = ""
    # 1. which lark-cli（macOS）
    try:
        which_result = subprocess.run(
            ["which", "lark-cli"],
            capture_output=True, text=True, check=False,
            encoding="utf-8", errors="replace",
        )
        if which_result.returncode == 0 and which_result.stdout.strip():
            lark_cli = True
    except (OSError, subprocess.SubprocessError):
        pass
    # 2. 兜底：直接扫描 lark 插件 bin 目录
    if not lark_cli and LARK_PLUGIN_ROOT is not None and lark_plugin:
        for version_dir in sorted(LARK_PLUGIN_ROOT.iterdir(), reverse=True):
            if version_dir.is_dir() and (version_dir / "bin" / "lark-cli").is_file():
                lark_cli = True
                break
    # 3. lark-cli --version（捕获输出，不依赖 auth status）
    if lark_cli:
        try:
            ver_result = subprocess.run(
                ["lark-cli", "--version"],
                capture_output=True, text=True, check=False,
                encoding="utf-8", errors="replace",
                timeout=5,
            )
            if ver_result.returncode == 0:
                version = ver_result.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            pass
    return {"lark_cli": lark_cli, "lark_plugin": lark_plugin, "version": version}


def _lark_plugin_version_str() -> str:
    """从可选 LARK_PLUGIN_ROOT 取最大版本目录名（如 ``1.0.3``）。"""
    if LARK_PLUGIN_ROOT is None or not LARK_PLUGIN_ROOT.is_dir():
        return ""
    versions = sorted(
        [p.name for p in LARK_PLUGIN_ROOT.iterdir()
         if p.is_dir() and p.name[:1].isdigit()],
        reverse=True,
    )
    return versions[0] if versions else ""


def _stdin_interactive() -> bool:
    """True only when stdin is a real TTY with readable input available.

    CI runners and sandbox shells often expose a pseudo-TTY with no input
    stream; ``input()`` would block forever there.  ``select()`` with a short
    timeout detects a TTY that actually has pending data (or EOF), and the
    Windows ``msvcrt.kbhit()`` branch keeps the behavior cross-platform.
    """
    if not sys.stdin.isatty():
        return False
    try:
        import msvcrt  # Windows
        return bool(msvcrt.kbhit())
    except ImportError:
        pass
    try:
        import select
        ready, _, _ = select.select([sys.stdin], [], [], 0.2)
        return bool(ready)
    except (OSError, ValueError):
        return False


def _prompt_feishu_integration(req_dir: Path) -> None:
    """init 完成后扫描飞书能力并询问是否启用，落盘 00-input/feishu-enabled.json。

    - 检测到 lark-cli 或 lark 插件：
        - TTY 且 stdin 有输入：主动询问 [y/N]，y 写 ``enabled:true``，N/默认写 ``enabled:false``；
        - 非 TTY / 伪 TTY 无输入：跳过询问，打印能力扫描结果，写默认 ``enabled:false``。
    - 未检测到：不询问，写 ``{"enabled": false, "reason": "..."}``。
    """
    feishu = _detect_feishu_capability()
    today = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
    feishu_file = req_dir / "00-input" / "feishu-enabled.json"
    if feishu.get("lark_cli") or feishu.get("lark_plugin"):
        plugin_ver = _lark_plugin_version_str()
        parts = []
        if feishu.get("lark_cli"):
            parts.append(f"lark-cli 已安装（{feishu.get('version') or 'version unknown'}）")
        if feishu.get("lark_plugin"):
            parts.append(f"飞书插件 v{plugin_ver or 'unknown'} 可用")
        print(f"  飞书能力扫描：检测到 {'; '.join(parts)}")
        if _stdin_interactive():
            answer = input(
                "  检测到飞书能力，是否启用飞书集成？"
                "本项目将以 lark-cli 为来源读取飞书文档/发布 PRD。[y/N] "
            ).strip().lower()
            enabled = answer in ("y", "yes")
            print(f"  飞书集成：{'已启用' if enabled else '未启用（默认）'}")
        else:
            print("  飞书集成：非交互环境，跳过询问，默认未启用")
            enabled = False
        payload = {
            "enabled": enabled,
            "detected_at": today,
            "lark_cli_version": feishu.get("version", ""),
            "lark_plugin_version": plugin_ver,
        }
    else:
        print("  飞书能力扫描：未检测到 lark-cli 与 lark 插件")
        payload = {"enabled": False, "reason": "lark-cli and lark plugin not detected"}
    feishu_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )


def init_requirement(name: str | None, root: Path | None = None, process_tier: str | None = None,
                     difficulty: str | None = None) -> int:
    """Create a requirement skeleton from the registry (REQ-NNN-topic-name)."""
    if not name:
        print("ERROR: init requires a requirement name like REQ-NNN-my-feature", file=sys.stderr)
        return 1
    if process_tier not in {"L0", "L1", "L2"}:
        print("ERROR: init requires explicit --process-tier L0|L1|L2", file=sys.stderr)
        return 1
    normalized_difficulty = normalize_difficulty(difficulty)
    if difficulty is not None and normalized_difficulty is None:
        print("ERROR: --difficulty must be low|medium|high（低|中|高）", file=sys.stderr)
        return 1
    if not re.fullmatch(r"REQ-\d{3}[A-Za-z0-9_-]*", name):
        print(f"ERROR: invalid requirement name '{name}' (expect REQ-NNN-topic)", file=sys.stderr)
        return 1
    requirements_root = (root.resolve() if root is not None else Path.cwd()) / "requirements"
    req_dir = requirements_root / name
    if req_dir.exists():
        print(f"ERROR: {req_dir} already exists", file=sys.stderr)
        return 1
    req_dir.mkdir(parents=True, exist_ok=True)
    (req_dir / "00-input").mkdir()
    (req_dir / "99-review").mkdir()
    # Only create directories enabled by the durable tier.
    for item in work_items_for_tier(process_tier):
        (req_dir / item["artifact_dir"]).mkdir(parents=True, exist_ok=True)
    intake_template = Path(__file__).parent.parent / "shared/intake-routing/templates/intake-decision.md"
    if not intake_template.is_file():
        print(f"ERROR: intake decision template not found: {intake_template}", file=sys.stderr)
        return 1
    recommendation = tier_recommendation(req_dir, normalized_difficulty)
    intake_text = (intake_template.read_text(encoding="utf-8")
                   .replace("{PROCESS_TIER}", process_tier)
                   .replace("{REQ_NAME}", name)
                   .replace("{DIFFICULTY_LEVEL}", normalized_difficulty or "待人工选择")
                   .replace("{TIER_RECOMMENDATION}", recommendation["recommendation"] or "不触发")
                   .replace("{TIER_SELECTION_MODE}", "人工确认（建议不可自动生效）"))
    (req_dir / "00-input/intake-decision.md").write_text(intake_text, encoding="utf-8")
    # authorized-reviewers skeleton: AI must never fill a real reviewer here
    (req_dir / "00-input" / "authorized-reviewers.json").write_text(
        json.dumps({"reviewers": []}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    # L1/L2 的 B3 账本来自共享模板，但行集必须由持久化档位派生；L0 不创建它。
    issue_record_template = (
        Path(__file__).parent.parent
        / "shared/clarify/skills/issue-record/assets/issue-record-template.md"
    )
    if process_tier != "L0" and issue_record_template.is_file():
        support_dir = req_dir / "99-review" / "support"
        support_dir.mkdir(parents=True, exist_ok=True)
        ledger_rows = "\n".join(
            f"| {item['stage']} | {item['id']} | 0 | 待填写 | open |"
            for item in work_items_for_tier(process_tier)
        )
        issue_text = (
            issue_record_template.read_text(encoding="utf-8")
            .replace("{PROCESS_TIER}", process_tier)
            .replace("{B3_LEDGER_ROWS}", ledger_rows)
        )
        (support_dir / "issue-record.md").write_text(
            issue_text,
            encoding="utf-8",
        )
    # 单一真相源：source-register 骨架来自 project-init 共享模板（src/shared/
    # project-init/templates/source-register-skeleton.md），不在 pipeline 内硬编码。
    source_register_template = (
        Path(__file__).parent.parent
        / "shared/project-init/templates/source-register-skeleton.md"
    )
    if not source_register_template.is_file():
        print(f"ERROR: source-register template not found: {source_register_template}", file=sys.stderr)
        return 1
    (req_dir / "00-input" / "source-register.md").write_text(
        source_register_template.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    # 单一真相源：README 骨架来自 project-init 共享模板（src/shared/project-init/
    # templates/readme-skeleton.md），不在 pipeline 内硬编码 README 索引表。
    readme_template = (
        Path(__file__).parent.parent
        / "shared/project-init/templates/readme-skeleton.md"
    )
    if not readme_template.is_file():
        print(f"ERROR: README template not found: {readme_template}", file=sys.stderr)
        return 1
    # 模板含占位符 REQ-{NNN} · {业务主题}，读取后按需求名替换
    m = re.match(r"REQ-(\d{3})(?:-(.+))?$", name)
    req_num = m.group(1) if m else ""
    req_topic = (m.group(2) if m and m.group(2) else "").strip()
    readme_content = (
        readme_template.read_text(encoding="utf-8")
        .replace("{NNN}", req_num)
        .replace("{业务主题}", req_topic)
        .replace("{PROCESS_TIER}", process_tier)
        .replace("`待填写`（L0 / L1 / L2）", f"`{process_tier}`（L0 / L1 / L2）")
    )
    first_item = work_items_for_tier(process_tier)[0]
    readme_content = readme_content.replace(
        "**`project-background-goal`（项目背景与目标）· status = draft**",
        f"**`{first_item['id']}`（{first_item['name']}）· status = draft**",
    )
    enabled_dirs = {item["artifact_dir"] for item in work_items_for_tier(process_tier)}
    lines = readme_content.splitlines()
    filtered = []
    for line in lines:
        match = re.search(r"\| `([^`]+)` \|", line)
        candidate = match.group(1).rstrip("/") if match else ""
        all_dirs = {item["artifact_dir"] for item in work_items()}
        if candidate in all_dirs and candidate not in enabled_dirs:
            continue
        filtered.append(line)
    readme_content = "\n".join(filtered) + "\n"
    (req_dir / "README.md").write_text(readme_content, encoding="utf-8")
    # 事件溯源：初始化完成写入 init 事件（inline payload 无需 record 文件）
    audit_log.append_event(
        req_dir,
        event_type="init",
        payload={"skeleton_created_by": "pipeline.py init", "registry_schema_version": len(list(work_items()))},
        extra={"requirement_name": name},
    )
    print(f"Created {req_dir}")
    print(f"  Next: put source materials in {req_dir}/00-input/, then run")
    print(f"        python3 src/scripts/pipeline.py {req_dir} status")
    # B4 fix: pre-warn about product_owner-only work items so the reviewer
    # registry is configured with both roles up front, avoiding mid-flow
    # approval interruptions (roles: functional-flow/page-design/interaction-
    # rules/field-rules/validation-rules/state-machine/exception-handling).
    if process_tier in {"L1", "L2"}:
        po_only = [
            i["id"] for i in work_items_for_tier(process_tier)
            if i.get("reviewer_roles") == ["product_owner"]
        ]
        if po_only:
            print("  NOTE: 以下 work item 仅接受 product_owner 角色审批："
                  + ", ".join(po_only))
            print("        建议在 00-input/authorized-reviewers.json 为评审人预配")
            print("        business_owner + product_owner 双角色，避免审批中断。")
    # 飞书能力扫描 + 主动询问（仅 init 一次；非 TTY 自动写默认 false）
    _prompt_feishu_integration(req_dir)
    return 0


def machine_gate(req_dir: Path, item: dict) -> dict:
    result = check_item(req_dir, item)
    records = run_json("branch_validator.py", req_dir)
    cross = {"ok": True, "skipped": item["id"] != "prd-assembly"}
    if item["id"] == "prd-assembly":
        cross = run_json("traceability_check.py", req_dir)
    # logical-completeness property check applies to all 9 stage-2 work items
    STAGE2_IDS = {
        "feature-list", "functional-flow", "page-design", "interaction-rules",
        "business-rules", "validation-rules", "state-machine", "exception-handling", "acceptance-criteria"
    }
    prop = {"ok": True, "skipped": item["id"] not in STAGE2_IDS}
    if item["id"] in STAGE2_IDS:
        art = find_artifact(req_dir, item)
        prop = run_property_check(art) if art else {"ok": False, "skipped": False, "error": "artifact not found"}
    # L0 不建 issue-record；L1/L2 一律使用 intake 持久化档位的 B3 账本。
    process_tier = tier_for_req(req_dir)
    issue_record = {"ok": True, "skipped": process_tier == "L0"}
    if process_tier != "L0":
        issue_record = check_issue_record(req_dir)
    applicability = {"ok": True, "skipped": item["id"] != "prd-assembly"}
    if item["id"] == "prd-assembly":
        applicability = canonical_applicability_evidence(req_dir)
    ok = (result["dor_pass"] and result["dod_pass"] and bool(cross.get("ok"))
          and bool(records.get("ok")) and bool(prop.get("ok")) and bool(issue_record.get("ok"))
          and bool(applicability.get("ok")))
    return {"ok": ok, "work_item": result, "cross_trace": cross, "records": records,
            "property": prop, "issue_record": issue_record, "applicability": applicability}


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


def write_change_record(req_dir: Path, item: dict, artifact: Path, from_status: str,
                        to_status: str, reason: str, changed_by: str,
                        reviewer_id: str = "", reviewer_role: str = "",
                        comments: str = "") -> Path:
    """B12: write an audit trail for a reverse status transition.

    Reverse transitions (`* → draft` / `* → superseded`) must not happen
    silently. Every such transition writes a `99-review/change-*.md` record
    carrying `from_status`, `to_status`, `reason`, `changed_at`, `changed_by`.
    The filename matches `*change*.md` so `branch_validator` audits it too
    (it requires a downstream-impact signal, which the footer provides).
    """
    review_dir = req_dir / "99-review"
    review_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    record = review_dir / f"change-{item['id']}-{now[:10]}.md"
    suffix = 1
    while record.exists():
        record = review_dir / f"change-{item['id']}-{now[:10]}-{suffix}.md"
        suffix += 1
    record.write_text(
        "\n".join([
            f"# Change Record: {item['id']} {from_status} → {to_status}", "",
            f"- work_item: {item['id']}",
            f"- artifact: {artifact.relative_to(req_dir).as_posix()}",
            f"- from_status: {from_status}",
            f"- to_status: {to_status}",
            f"- reason: {reason}",
            f"- changed_at: {now}",
            f"- changed_by: {changed_by}",
            f"- reviewer_id: {reviewer_id}",
            f"- reviewer_role: {reviewer_role}",
            f"- comments: {comments or '无'}", "",
            "> 逆向跃迁已留痕；下游产物需重新校验（影响范围由 branch_validator 审计）。", "",
        ]), encoding="utf-8",
    )
    return record


def reviewer_cli(argv: list[str]) -> int:
    """E2E-001: manage 00-input/authorized-reviewers.json from the CLI.

    subcommands:
      pipeline.py reviewer add <req_dir> --id <id> --name <name> --roles r1,r2 [--roles ...]
      pipeline.py reviewer list <req_dir>
    Registration is strictly an alias for the human to grant review rights;
    it never auto-fills a reviewer into a review call.
    """
    if not argv:
        print("usage: pipeline.py reviewer add <req_dir> --id <id> --name <name> --roles r1,r2")
        print("       pipeline.py reviewer list <req_dir>")
        return 2
    sub, *rest = argv
    parser = argparse.ArgumentParser(prog=f"pipeline.py reviewer {sub}")
    parser.add_argument("req_dir", type=Path)
    if sub == "add":
        parser.add_argument("--id", required=True, dest="rid")
        parser.add_argument("--name", required=True)
        parser.add_argument("--roles", required=True, help="comma-separated role list, e.g. product_owner,pm")
    parser.add_argument("--json", action="store_true")
    try:
        args = parser.parse_args(rest)
    except SystemExit as e:
        return int(e.code or 2)
    if not args.req_dir.is_dir():
        print(f"ERROR: {args.req_dir} is not a directory", file=sys.stderr)
        return 1
    registry = args.req_dir / "00-input" / "authorized-reviewers.json"
    data = {"reviewers": []}
    if registry.is_file():
        try:
            data = json.loads(registry.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {"reviewers": []}
        data.setdefault("reviewers", [])

    if sub == "add":
        # 去重：同 id+name 存在则合并 roles，否则新增
        roles = [r.strip() for r in args.roles.split(",") if r.strip()]
        for entry in data["reviewers"]:
            if entry.get("id") == args.rid and entry.get("name") == args.name:
                merged = {**entry, "roles": sorted(set(entry.get("roles", [])) | set(roles))}
                entry.update(merged)
                break
        else:
            data["reviewers"].append({"id": args.rid, "name": args.name, "roles": roles})
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        out = {"added": [args.rid], "roles": roles, "registry": str(registry)}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    # list
    out = {"reviewers": data["reviewers"], "registry": str(registry)}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def review(req_dir: Path, item: dict, decision: str, reviewer: str, reviewer_id: str,
           reviewer_role: str, comments: str, reason: str = "") -> int:
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
    current_status = re.search(r"(?m)^status:\s*[\"']?([\w-]+)", artifact.read_text(encoding="utf-8"))
    current_status = current_status.group(1) if current_status else "unknown"
    if decision == "approve" and current_status != "ready_for_human_review":
        print(f"ERROR: approval requires ready_for_human_review, got {current_status}", file=sys.stderr)
        return 1
    # B12: reverse transitions (`* → draft`) must be audited. A `changes`
    # decision silently reverting a confirmed/superseded artifact to draft is
    # forbidden — it requires a non-empty --reason and writes a change record.
    if decision == "changes" and not (reason or "").strip():
        print("ERROR: --decision changes requires a non-empty --reason "
              "(reverse transition to draft must be audited)", file=sys.stderr)
        return 1
    gate = machine_gate(req_dir, item)
    if decision == "approve" and not gate["ok"]:
        print(json.dumps(gate, ensure_ascii=False, indent=2))
        print("ERROR: machine gates must pass before approval", file=sys.stderr)
        return 1
    review_dir = req_dir / "99-review"
    review_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    artifact_text = artifact.read_text(encoding="utf-8")
    # L0 remains a single human approval.  Before recording that approval, build
    # the canonical PRD in memory from the mini-prd plus durable intake matrix.
    # A missing/placeholder matrix fails before ReviewRecord, audit, anchor, or
    # any status mutation is written.
    l0_projection: tuple[str, dict] | None = None
    if decision == "approve" and item["id"] == "mini-prd" and tier_for_req(req_dir) == "L0":
        try:
            l0_projection = build_projection(artifact, artifact_text, reviewer=reviewer, confirmed_at=now)
        except (OSError, ValueError) as projection_err:
            print(f"ERROR: cannot project L0 mini-prd into canonical PRD: {projection_err}", file=sys.stderr)
            return 1
    artifact_hash = artifact_content_hash(artifact_text)
    artifact_meta = re.search(r"(?m)^version:\s*[\"']?([^\s\"']+)", artifact_text)
    artifact_version = artifact_meta.group(1) if artifact_meta else "unknown"
    record = review_dir / f"review-{item['id']}-{now[:10]}.md"
    suffix = 1
    while record.exists():
        record = review_dir / f"review-{item['id']}-{now[:10]}-{suffix}.md"
        suffix += 1
    # B13 fix: every ReviewRecord carries an immutable self-fingerprint.
    # record_created_at pins when the record was created; record_sha256 covers
    # the whole record body except the record_sha256 line itself. Editing any
    # field of the record (e.g. artifact_content_sha256 to match a rewritten
    # artifact) changes the body, so the declared record_sha256 no longer
    # matches and branch_validator flags it as CRITICAL.
    record_lines = [
        f"# Review: {item['name']}", "",
        f"- work_item: {item['id']}", f"- artifact: {artifact.relative_to(req_dir).as_posix()}",
        f"- artifact_version: {artifact_version}", f"- artifact_content_sha256: {artifact_hash}",
        f"- decision: {decision}", f"- reviewer: {reviewer}", f"- reviewer_id: {reviewer_id}",
        f"- reviewer_role: {reviewer_role}", f"- reviewed_at: {now}",
        f"- record_created_at: {now}",
        f"- record_sha256: {hash_anchor.RECORD_SHA256_PLACEHOLDER}",
        f"- comments: {comments or '无'}", "",
    ]
    record_text = "\n".join(record_lines)
    record_sha256 = hash_anchor.record_body_sha256(record_text)
    final_record_text = record_text.replace(hash_anchor.RECORD_SHA256_PLACEHOLDER, record_sha256)
    record.write_text(final_record_text, encoding="utf-8")
    # 事件溯源：为本次评审写入 review 审计事件（绑定 ReviewRecord hash）
    try:
        audit_log.append_event(
            req_dir,
            event_type="review",
            payload=str(record.relative_to(req_dir).as_posix()),
            payload_sha256=hashlib.sha256(final_record_text.encode("utf-8")).hexdigest(),
            extra={
                "work_item": item["id"],
                "decision": decision,
                "reviewer": reviewer,
                "reviewer_id": reviewer_id,
                "reviewer_role": reviewer_role,
                "artifact_version": artifact_version,
                "artifact_content_sha256": artifact_hash,
            },
        )
    except (ValueError, FileNotFoundError) as audit_err:
        # 审计事件写入失败必须 fail-loud：确认操作整体中止
        record.unlink(missing_ok=True)
        print(f"ERROR: failed to append review audit event: {audit_err}", file=sys.stderr)
        return 1
    # B13 fix: record an external append-only hash anchor on approve.
    # The ReviewRecord is closed-loop (artifact + ReviewRecord can be swapped
    # together); the anchor chain under 99-review/.hash-anchor.jsonl provides
    # a tamper-evident external reference. record_anchor is idempotent on
    # (artifact_id, review_record, sha256) so retries and post-confirm metadata
    # edits (status/reviewer stamps) do not pile up duplicate rows.
    artifact_meta_for_anchor = read_frontmatter(artifact)
    hash_anchor.record_anchor(
        req_dir,
        artifact=str(artifact.relative_to(req_dir).as_posix()),
        artifact_id=artifact_meta_for_anchor.get("artifact_id") or item["id"],
        reviewer=reviewer,
        review_record=str(record.relative_to(req_dir).as_posix()),
        sha256=artifact_hash,
    )
    # B12: reverse transition audit trail — `changes` (→ draft) must leave a
    # change record with from_status / to_status / reason / changed_at /
    # changed_by before the status is actually flipped.
    if decision == "changes":
        change_record = write_change_record(
            req_dir, item, artifact, current_status, "draft",
            reason, reviewer, reviewer_id, reviewer_role, comments,
        )
        # 事件溯源：逆向跃迁 change 记录 → change 审计事件
        try:
            change_record_text = change_record.read_text(encoding="utf-8")
            audit_log.append_event(
                req_dir,
                event_type="change",
                payload=str(change_record.relative_to(req_dir)),
                payload_sha256=hash_anchor._line_sha256(change_record_text) if hasattr(hash_anchor, "_line_sha256")
                    else __import__("hashlib").sha256(change_record_text.encode("utf-8")).hexdigest(),
                extra={
                    "work_item": item["id"],
                    "from_status": current_status,
                    "to_status": "draft",
                    "reason": reason,
                    "changed_by": reviewer,
                },
            )
        except (ValueError, FileNotFoundError) as audit_err:
            print(f"ERROR: failed to append change audit event: {audit_err}", file=sys.stderr)
            return 1
        print(f"Recorded change: {change_record.relative_to(req_dir)}")
    text = artifact_text
    target_status = "confirmed" if decision == "approve" else "draft"
    text = re.sub(r"(?m)^status:\s*\S+", f"status: {target_status}", text, count=1)
    if re.search(r"(?m)^reviewer:", text):
        text = re.sub(r"(?m)^reviewer:.*$", f"reviewer: {reviewer}", text, count=1)
    else:
        # B1 fix: templates without a reviewer field (e.g. feasibility-report /
        # project-scope frontmatter) would otherwise stay reviewer-less after
        # approval, tripping branch_validator's confirmed.no_valid_reviewer and
        # forcing a full reflow cycle.  Always stamp the real reviewer on review.
        text = re.sub(r"(?m)^(status:\s*\S+)$", f"\\1\nreviewer: {reviewer}", text, count=1)
    if re.search(r"(?m)^reviewed_at:", text):
        text = re.sub(r"(?m)^reviewed_at:.*$", f"reviewed_at: {now}", text, count=1)
    if decision == "approve" and re.search(r"(?m)^confirmed_at:", text):
        text = re.sub(r"(?m)^confirmed_at:.*$", f"confirmed_at: {now}", text, count=1)
    artifact.write_text(text, encoding="utf-8")
    if l0_projection is not None:
        projection_path = req_dir / "003-prd-output" / "prd.md"
        try:
            write_projection(
                artifact,
                projection_path,
                req_dir / "003-prd-output" / "prd-assembly-manifest.json",
                reviewer=reviewer,
                confirmed_at=now,
                projection=l0_projection,
            )
            projection_meta = read_frontmatter(projection_path)
            hash_anchor.record_anchor(
                req_dir,
                artifact=str(projection_path.relative_to(req_dir).as_posix()),
                artifact_id=projection_meta.get("artifact_id") or "prd-assembly",
                reviewer=reviewer,
                review_record=str(record.relative_to(req_dir).as_posix()),
                sha256=artifact_content_hash(projection_path.read_text(encoding="utf-8")),
            )
        except OSError as projection_err:
            # The projection was fully preflighted.  A filesystem failure is still
            # surfaced loudly rather than claiming an L0 delivery completed.
            print(f"ERROR: failed to publish L0 canonical PRD projection: {projection_err}", file=sys.stderr)
            return 1
    print(f"Recorded {decision}: {record.relative_to(req_dir)}")
    return 0 if decision == "approve" else 2


def _match_field(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text)
    return m.group(1).strip() if m else None


def audit_backfill(req_dir: Path) -> int:
    """Backfill AuditEvents from legacy review/change records (pre-audit_log).

    REQ-001~008 were created before event sourcing was adopted: they carry
    ``99-review/review-*.md`` / ``change-*.md`` records but no
    ``.audit/events.jsonl``. This command replays those records into
    append-only events (marked ``backfilled: true``) so ``verify_chain`` /
    ``reconstruct_causality`` / ``projection_cache`` work for history
    directories without rewriting any existing content.

    Idempotent: a record already referenced by an existing event's ``payload``
    is skipped. ``recorded_at`` is taken from the record's ``reviewed_at`` /
    ``changed_at`` when it keeps the log monotonic; otherwise the append uses
    "now" and the original timestamp stays preserved in the record body.
    """
    # Resolve the durable tier before inspecting records.  Backfill is a write
    # action, so it must not smuggle an out-of-tier historical record into the
    # event chain.
    try:
        persisted_tier = require_persisted_tier(req_dir)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    events = audit_log.replay_events(req_dir)
    existing_refs = {ev["payload"] for ev in events if isinstance(ev.get("payload"), str)}

    def _iso(ts: str | None):
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else None
        except ValueError:
            return None

    last_dt: datetime | None = None
    for ev in events:
        dt = _iso(ev.get("recorded_at"))
        if dt and (last_dt is None or dt > last_dt):
            last_dt = dt

    review_dir = req_dir / "99-review"
    if not review_dir.is_dir():
        print("No 99-review/ records found; nothing to backfill.", file=sys.stderr)
        return 1

    appended = 0
    skipped = 0
    # Collect (path, text, ts_dt) then sort by timestamp so the event log is
    # CHRONOLOGICAL — projection_cache folds with "latest event wins", which
    # assumes events arrive in time order. Alphabetical order is NOT
    # chronological (e.g. "review-x-2026-08-14-1.md" sorts before
    # "review-x-2026-08-14.md" because '-' < '.'), so sorting by ts matters
    # when a work item has multiple review records (REQ-004 had two).
    pending: list[tuple[Path, str, datetime | None]] = []
    for pattern in ("review-*.md", "change-*.md"):
        for p in sorted(review_dir.glob(pattern)):
            rel = str(p.relative_to(req_dir).as_posix())
            if rel in existing_refs:
                skipped += 1
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except OSError as e:
                print(f"ERROR: cannot read {rel}: {e}", file=sys.stderr)
                return 1
            ts = (_match_field(text, r"(?m)^\s*-\s*reviewed_at:\s*(.+)$")
                  or _match_field(text, r"(?m)^\s*-\s*changed_at:\s*(.+)$"))
            pending.append((p, text, _iso(ts)))

    pending.sort(key=lambda t: (t[2] is not None, t[2] or datetime.min, t[0].name))
    # Validate the whole batch before the first append.  A failure leaves the
    # audit chain untouched rather than producing a partial backfill.
    for p, text, _rec_dt in pending:
        rel = str(p.relative_to(req_dir).as_posix())
        work_item_id = _match_field(text, r"(?m)^\s*-\s*work_item:\s*(\S+)")
        if not work_item_id:
            print(f"ERROR: {rel}: missing work_item; cannot validate persisted tier {persisted_tier}", file=sys.stderr)
            return 1
        try:
            assert_work_item_in_tier(req_dir, resolve_work_item(work_item_id))
        except (KeyError, ValueError) as exc:
            print(f"ERROR: {rel}: {exc}", file=sys.stderr)
            return 1
    for p, text, rec_dt in pending:
        rel = str(p.relative_to(req_dir).as_posix())
        extra = {
            "backfilled": True,
            "work_item": _match_field(text, r"(?m)^\s*-\s*work_item:\s*(\S+)"),
            "decision": _match_field(text, r"(?m)^\s*-\s*decision:\s*(\S+)"),
            "reviewer": _match_field(text, r"(?m)^\s*-\s*reviewer:\s*(.+)$"),
            "from_status": _match_field(text, r"(?m)^\s*-\s*from_status:\s*(\S+)"),
            "to_status": _match_field(text, r"(?m)^\s*-\s*to_status:\s*(\S+)"),
            "reason": _match_field(text, r"(?m)^\s*-\s*reason:\s*(.+)$"),
            "artifact_content_sha256": _match_field(text, r"(?m)^\s*-\s*artifact_content_sha256:\s*([0-9a-f]{64})"),
            "artifact_version": _match_field(text, r"(?m)^\s*-\s*artifact_version:\s*(\S+)"),
        }
        recorded_at = None
        if rec_dt and (last_dt is None or rec_dt >= last_dt):
            recorded_at = _match_field(text, r"(?m)^\s*-\s*reviewed_at:\s*(.+)$") \
                or _match_field(text, r"(?m)^\s*-\s*changed_at:\s*(.+)$")
            last_dt = rec_dt
        payload_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
        try:
            audit_log.append_event(
                req_dir,
                event_type="review" if p.name.startswith("review-") else "change",
                payload=rel,
                payload_sha256=payload_sha256,
                recorded_at=recorded_at,
                extra=extra,
            )
        except (ValueError, FileNotFoundError) as audit_err:
            # Monotonic guard: retry with "now" so backfill never blocks.
            print(f"WARN: {rel}: {audit_err}; retrying with current timestamp", file=sys.stderr)
            audit_log.append_event(
                req_dir,
                event_type="review" if p.name.startswith("review-") else "change",
                payload=rel,
                payload_sha256=payload_sha256,
                extra=extra,
            )
        appended += 1

    print(json.dumps({
        "requirement": req_dir.resolve().name,
        "appended_events": appended,
        "already_referenced": skipped,
        "note": "backfilled events carry backfilled:true; original reviewed_at/changed_at "
                "remain in the record bodies (events store recorded_at=backfill time when monotonic)",
    }, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    # `pipeline.py init <name>` — init is the action, <name> is the target.
    if len(sys.argv) >= 2 and sys.argv[1] == "init":
        init_parser = argparse.ArgumentParser(prog="pipeline.py init")
        init_parser.add_argument("name", nargs="?", help="Requirement name: REQ-NNN-topic")
        init_parser.add_argument(
            "--root", type=Path, default=None,
            help="Directory that receives requirements/<name>; defaults to the current directory",
        )
        init_parser.add_argument("--process-tier", required=True, choices=["L0", "L1", "L2"],
                                 help="Persist the REQ process tier in 00-input/intake-decision.md")
        init_parser.add_argument("--difficulty", choices=["low", "medium", "high"], default=None,
                                 help="Optional entry difficulty; medium/high show a non-authoritative tier recommendation")
        init_args = init_parser.parse_args(sys.argv[2:])
        return init_requirement(init_args.name, init_args.root, init_args.process_tier, init_args.difficulty)
    # E2E-001: `pipeline.py reviewer add <req_dir> --id <id> --name <name> --roles r1,r2`
    #          / `pipeline.py reviewer list <req_dir>` — 提供登记评审人的 CLI 入口，
    #          摆脱"手改 00-input/authorized-reviewers.json"的痛点。
    if len(sys.argv) >= 2 and sys.argv[1] == "reviewer":
        return reviewer_cli(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("req_dir", type=Path)
    parser.add_argument("action", nargs="?", choices=["status", "entry", "gate", "review", "reflow", "backfill"], default="status")
    parser.add_argument("--stage")
    parser.add_argument("--work-item", choices=[item["id"] for item in work_items()])
    parser.add_argument("--wave", type=int, choices=range(1, 6), help="Deprecated compatibility alias")
    parser.add_argument("--yes", action="store_true", help="Non-interactive machine checks only; never human approval")
    parser.add_argument("--decision", choices=["approve", "changes"])
    parser.add_argument("--reviewer")
    parser.add_argument("--reviewer-id")
    parser.add_argument("--reviewer-role")
    parser.add_argument("--apply", action="store_true", help="reflow: actually flip downstream to superseded (default is dry-run)")
    parser.add_argument("--no-cascade", action="store_true",
                        help="reflow (B6): apply the change WITHOUT flipping downstream to superseded — "
                             "for metadata/traceability-only fixes. A change record is still written for audit.")
    parser.add_argument("--comments", default="")
    parser.add_argument("--reason", default="", help="B12: required for reverse transitions (--decision changes); recorded in the change record")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--process-tier", choices=["L0", "L1", "L2"], default=None,
                        help="status/entry preview only; gate/review/reflow always use persisted intake tier")
    parser.add_argument("--difficulty", choices=["low", "medium", "high"], default=None,
                        help="entry only: low hides tier suggestion; medium/high show a human-review suggestion")
    args = parser.parse_args()
    if not args.req_dir.is_dir():
        print(f"ERROR: {args.req_dir} is not a directory", file=sys.stderr)
        return 1
    if args.wave:
        print("DEPRECATED: --wave will be removed after the v3 compatibility baseline.", file=sys.stderr)
    if args.yes:
        print("NOTICE: --yes runs machine checks only and does not bypass human review.", file=sys.stderr)
    if args.action == "status":
        try:
            persisted = tier_for_req(args.req_dir)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        result = build_status(args.req_dir, tier=args.process_tier)
        result["persisted_tier"] = persisted
        result["tier_preview"] = args.process_tier
        result["tier_source"] = "intake-decision" if (args.req_dir / "00-input/intake-decision.md").is_file() else "legacy-compat"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if args.action == "entry":
        try:
            persisted = tier_for_req(args.req_dir)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        result = build_status(args.req_dir, tier=args.process_tier)
        input_dir = args.req_dir / "00-input"
        src_count = len(list(input_dir.glob("SRC-*.md"))) if input_dir.is_dir() else 0
        artifact_count = sum(1 for s in result["work_items"].values() if s not in ("not_created", ""))
        confirmed_count = sum(1 for s in result["work_items"].values() if s == "confirmed")
        tier = args.process_tier or persisted
        brainstorming_resume = resume_work_item_for_tier(
            resolve_branch_capability("brainstorming"), persisted
        )

        # If workflow invalid (over-active items), surface the fix first.
        if result["invalid_active_items"]:
            maturity = "⚠️ 越级待审"
            entry = f"先修正: 将 {', '.join(result['invalid_active_items'])} 降为 draft，确认 {result['active_work_item']}"
        elif confirmed_count == len(work_items_for_tier(tier)):
            maturity, entry = "L4 已全部确认", "PRD 已确认，可发布（复核由 branch_validator 自动执行）"
        elif any(result["work_items"].get(wid) in ACTIVE for wid in (
            "feature-list", "functional-flow", "page-design", "interaction-rules",
            "business-rules", "validation-rules", "state-machine", "exception-handling", "acceptance-criteria"
        )):
            maturity, entry = "L3 产品方案已成型", "Stage 2 (feature-list 等续跑)"
        elif result["work_items"].get("user-stories") in ACTIVE:
            maturity, entry = "L1/L2 业务需求已成型", "Stage 1 (user-stories 续跑)"
        elif result["work_items"].get("user-journey") in ACTIVE:
            maturity, entry = "L1/L2 业务需求已成型", "Stage 1 (user-journey 续跑)"
        elif result["work_items"].get("project-background-goal") in ACTIVE:
            maturity, entry = "L1 背景已成型", "Stage 1 (project-background-goal 续跑)"
        elif artifact_count > 0:
            maturity, entry = f"L1 已有 {artifact_count} 份产物", "Stage 1 (user-journey)"
        elif src_count > 0:
            sig = entry_content_signals(args.req_dir)
            if sig["features"] and sig["rules"]:
                maturity, entry = "L3 材料含功能清单与业务规则", "Stage 1 (project-background-goal 快速起草)"
            elif sig["solution"]:
                maturity, entry = "L2 材料含产品级方案", "Stage 1 (project-background-goal)"
            else:
                maturity, entry = f"L1 有 {src_count} 份原始材料（内容信号 {sum(sig.values())}/6）", "Stage 1 (project-background-goal)"
        else:
            if persisted == "L0":
                maturity, entry = "材料成熟度 L0：仅有想法", f"发散收敛（brainstorming）→ {brainstorming_resume}"
            else:
                maturity, entry = "材料成熟度 L0：仅有想法", (
                    f"发散收敛（brainstorming）或补充材料 → {brainstorming_resume}"
                )

        entry_blocked = None
        if not result["invalid_active_items"] and confirmed_count == 0 and not result["work_items"].get("project-background-goal") in ACTIVE:
            if src_count == 0:
                entry_blocked = (
                    f"材料不足：先发散收敛（brainstorming）或补充材料，再进入 {brainstorming_resume}"
                )
            elif sum(entry_content_signals(args.req_dir).values()) < 2:
                entry_blocked = "材料成熟度 L1：建议补料或 requirement-restate（需求复述）确认理解"

        # 初始化时记录的难度是入口默认值；命令行参数只允许在只读 entry
        # 预览中显式覆盖，不会改写 intake，也不会改变持久化档位。
        persisted_difficulty = None
        decision_path = args.req_dir / "00-input/intake-decision.md"
        if decision_path.is_file():
            persisted_difficulty = read_frontmatter(decision_path).get("difficulty_level")
        difficulty = args.difficulty or persisted_difficulty
        recommendation = tier_recommendation(args.req_dir, difficulty)
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
            "persisted_tier": persisted,
            "tier_preview": args.process_tier,
            "tier_source": "intake-decision" if (args.req_dir / "00-input/intake-decision.md").is_file() else "legacy-compat",
            "difficulty_entry": recommendation,
        }, ensure_ascii=False, indent=2))
        return 0
    if args.action == "backfill":
        return audit_backfill(args.req_dir)
    if not (args.work_item or args.wave):
        print("ERROR: --work-item is required", file=sys.stderr)
        return 1
    item = resolve_work_item(args.work_item, args.wave)
    try:
        assert_work_item_in_tier(args.req_dir, item)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.stage and args.stage != item["stage"]:
        print(f"ERROR: {item['id']} belongs to {item['stage']}", file=sys.stderr)
        return 1
    if args.action == "gate":
        result = machine_gate(args.req_dir, item)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1
    if args.action == "reflow":
        no_cascade = bool(getattr(args, "no_cascade", False))
        results = {"work_item": item["id"], "impact": [], "applied": bool(args.apply),
                   "superseded": [], "no_cascade": no_cascade}
        pending_updates: list[tuple[Path, str]] = []
        for downstream in work_items_for_tier(tier_for_req(args.req_dir)):
            if downstream["order"] > item["order"]:
                dart = find_artifact(args.req_dir, downstream)
                if dart:
                    text = dart.read_text(encoding="utf-8")
                    fm = re.search(r"(?m)^status:\s*[\"']?([\w-]+)", text)
                    status = fm.group(1) if fm else "unknown"
                    if status in ("confirmed", "ready_for_human_review"):
                        # B6: --no-cascade keeps downstream confirmed — the
                        # change is metadata/traceability-only, so the existing
                        # confirmations remain valid; only a change record is
                        # written for audit.
                        if no_cascade:
                            action = "kept (no-cascade)"
                        else:
                            action = "superseded" if args.apply else "will become superseded on apply"
                        results["impact"].append({"id": downstream["id"], "status": status, "action": action})
                        if args.apply and not no_cascade:
                            new_text = re.sub(r"(?m)^status:\s*\S+", "status: superseded", text, count=1)
                            pending_updates.append((dart, new_text))
                            results["superseded"].append(downstream["id"])
        if args.apply and (results["superseded"] or no_cascade):
            now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            review_dir = args.req_dir / "99-review"
            review_dir.mkdir(parents=True, exist_ok=True)
            record = review_dir / f"change-record-reflow-{now[:10]}.md"
            suffix = 1
            while record.exists():
                record = review_dir / f"change-record-reflow-{now[:10]}-{suffix}.md"
                suffix += 1
            record_body = "\n".join([
                f"# Change Record: reflow {item['id']}", "",
                f"- trigger: {item['id']} changed",
                # B12: reverse transitions (`* → superseded`) carry the same
                # audit fields as `--decision changes` (from/to/reason/changed_*).
                f"- from_status: confirmed/ready_for_human_review",
                f"- to_status: superseded" if not no_cascade else "- to_status: unchanged (no-cascade)",
                f"- reason: {args.reason or 'reflow triggered by upstream change'}",
                f"- changed_at: {now}",
                f"- changed_by: reflow (machine-executed, human-initiated)",
                f"- superseded: {', '.join(results['superseded']) or 'none (no-cascade)'}", "",
                "- decision_id: 待填写（DEC-NNN，对齐 src/templates/others/decision-record.md）",
                "- decider: 待填写", "- rationale: 待填写", "",
                ("Downstream artifacts were flipped to `superseded`; they must be re-validated"
                 "after the earliest affected work item is re-confirmed."
                 if not no_cascade else
                 "no-cascade: downstream confirmations kept valid (metadata/traceability-only fix);"
                 "verify gate on the changed work item still passes."),
                "",
            ])
            # Pre-write all outputs, then publish the audit event, then atomically
            # replace each artifact. A failed preflight or event append leaves all
            # live downstream artifacts untouched.
            prepared: list[tuple[Path, Path]] = []
            try:
                for index, (dart, new_text) in enumerate(pending_updates, start=1):
                    tmp = dart.with_name(f".{dart.name}.reflow-{now[:10]}-{index}.tmp")
                    tmp.write_text(new_text, encoding="utf-8")
                    prepared.append((dart, tmp))
                record.write_text(record_body, encoding="utf-8")
            except OSError as write_err:
                for _dart, tmp in prepared:
                    tmp.unlink(missing_ok=True)
                record.unlink(missing_ok=True)
                print(f"ERROR: failed to prepare reflow changes: {write_err}", file=sys.stderr)
                return 1
            results["change_record"] = str(record.relative_to(args.req_dir).as_posix())
            # 事件先于状态可见，满足 audit-log 单一事实来源不变式。
            try:
                audit_log.append_event(
                    args.req_dir,
                    event_type="reflow",
                    payload=str(record.relative_to(args.req_dir).as_posix()),
                    payload_sha256=__import__("hashlib").sha256(record_body.encode("utf-8")).hexdigest(),
                    extra={
                        "work_item": item["id"],
                        "superseded": results["superseded"],
                        "reason": args.reason or "reflow triggered by upstream change",
                    },
                )
            except (ValueError, FileNotFoundError) as audit_err:
                for _dart, tmp in prepared:
                    tmp.unlink(missing_ok=True)
                record.unlink(missing_ok=True)
                print(f"ERROR: failed to append reflow audit event: {audit_err}", file=sys.stderr)
                return 1
            try:
                for dart, tmp in prepared:
                    os.replace(tmp, dart)
            except OSError as commit_err:
                for _dart, tmp in prepared:
                    tmp.unlink(missing_ok=True)
                print(f"CRITICAL: reflow event recorded but artifact commit failed: {commit_err}", file=sys.stderr)
                return 1
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0
    if not args.decision or not args.reviewer or not args.reviewer_id or not args.reviewer_role:
        print("ERROR: review requires --decision, --reviewer, --reviewer-id, and --reviewer-role", file=sys.stderr)
        return 1
    return review(args.req_dir, item, args.decision, args.reviewer, args.reviewer_id,
                  args.reviewer_role, args.comments, args.reason)


if __name__ == "__main__":
    sys.exit(main())
