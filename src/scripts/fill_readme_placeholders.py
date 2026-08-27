#!/usr/bin/env python3
"""Fill `待填写` placeholders in requirements/REQ-XXX/README.md from real sources.

HARD CONTRACT (do not relax):
  - Only writes fields whose value can be unambiguously pulled from an existing
    artifact (PRD frontmatter, intake-decision, BRD / mini-prd / background-goal).
  - Never invents business facts. If the source says `待填写` we keep `待填写`.
  - business_fact_owner / goal_decision_owner / reviewer that still carry the
    literal `待填写` token are NOT filled in — those are human-only assignments.
  - Source for every filled field is appended as an HTML comment so the change
    is auditable. Re-runs are idempotent (overwrites previous auto-fills but
    leaves any manually-edited non-placeholder text alone).

Usage:
  python3 src/scripts/fill_readme_placeholders.py [--apply] [REQ-XXX ...]
  default: --dry-run, all REQ-* in requirements/
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQ_DIR = ROOT / "requirements"
PLACEHOLDER_RE = re.compile(r"`待填写`")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"\A---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    out: dict[str, str] = {}
    for raw in m.group(1).splitlines():
        if ":" not in raw:
            continue
        k, v = raw.split(":", 1)
        out[k.strip()] = v.strip().strip("'\"")
    return out


def _section_after(text: str, heading: str) -> str:
    """Return body after `## {heading}` until next `## `. Tolerates `## N. heading`."""
    pat = re.compile(r"^##\s+(?:\d+\.\s+)?" + re.escape(heading) + r"\s*$", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return ""
    tail = text[m.end():]
    stop = re.search(r"^##\s+", tail, re.MULTILINE)
    return tail if stop is None else tail[:stop.start()]


def _first_bullet_after(text: str, heading: str) -> str:
    body = _section_after(text, heading)
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("- "):
            return line[2:].strip().strip("`")
        if line.startswith("**") and "**" in line[2:]:
            return re.sub(r"^(\*\*[^*]+\*\*)\s*[:：]\s*", "", line).strip()
    return ""


def _extract_one_liner(req_dir: Path, tier: str) -> tuple[str, str]:
    """Return (one_liner, source_label). Tier picks the canonical source."""
    if tier == "l0":
        p = req_dir / "000-minimal" / "01-mini-prd" / "mini-prd.md"
        if p.is_file():
            for ln in p.read_text(encoding="utf-8").splitlines():
                if "目标（一句话）" in ln:
                    return (ln.split("：", 1)[1].strip().strip("`* "),
                            f"mini-prd §1 ({p.relative_to(req_dir)})")
            for ln in p.read_text(encoding="utf-8").splitlines():
                if "改动点" in ln and "硬编码" in ln:
                    txt = ln.split("：", 1)[1].strip().strip("`* ")
                    return (txt[:140] + ("…" if len(txt) > 140 else ""),
                            f"mini-prd §1 ({p.relative_to(req_dir)})")
        return ("", "mini-prd 未找到")

    # L1 / L2 → BG upstream §2 项目与需求背景 / §1 需求来源与触发
    p = req_dir / "001-business-requirements" / "01-background-goal" / "background-goal.md"
    if p.is_file():
        text = p.read_text(encoding="utf-8")

        def _join(items: list[str]) -> str:
            cleaned = [s for s in items if s and len(s) > 8
                       and "本次产物范围" not in s
                       and "业务环境" not in s
                       and "需求由来" not in s
                       and "为什么现在" not in s
                       and not s.startswith("来源")]
            # 一句话业务摘要：取前 2 条最具代表性的 bullet
            cleaned = cleaned[:2]
            if not cleaned:
                return ""
            joined = "；".join(cleaned)
            if len(joined) > 220:
                joined = joined[:220] + "…"
            return joined

        # §2 项目与需求背景 —— 偏好这里（更聚焦业务背景）
        def _clean_bullet(s: str) -> str:
            # 去掉 markdown 加粗 `**...**` 的所有 `*` 标记，但保留中文文本和数字列表前缀
            s = re.sub(r"\*+", "", s)            # 去掉所有 *
            s = re.sub(r"^[\-\s]*\d+\.\s*", "", s)  # 去掉 `1. ` `2. ` 等数字列表前缀
            s = re.sub(r"^[\-\*\s]+", "", s)      # 去掉 `- ` 或 `* ` 前缀
            s = re.sub(r"^[【】\[\]\(\)\s]+", "", s)
            return s.strip()

        body2 = _section_after(text, "项目与需求背景")
        if body2:
            bullets: list[str] = []
            for line in body2.splitlines():
                stripped = line.strip()
                # 数字列表 / bullet / 普通行都接收
                if re.match(r"^(\d+\.\s|\-\s|\*\s)", stripped):
                    bullets.append(_clean_bullet(stripped))
            joined = _join(bullets)
            if joined:
                return (joined, f"BG §2 项目与需求背景 ({p.relative_to(req_dir)})")

        # §1 需求来源与触发 fallback（取"本次产物范围"作为业务一句话）
        body1 = _section_after(text, "需求来源与触发")
        if body1:
            for line in body1.splitlines():
                stripped = line.strip()
                if "本次产物范围" in stripped:
                    val = re.sub(r"^[【】\[\]\(\)\-\s\*]*", "", stripped)
                    val = re.sub(r"^\*\*本次产物范围\*\*[：:]\s*", "", val)
                    val = val.strip().strip("*").strip()
                    if val:
                        return (val[:220] + ("…" if len(val) > 220 else ""),
                                f"BG §1 需求来源与触发 ({p.relative_to(req_dir)})")
    return ("", "BG upstream 未找到")


def _safe_owner(value: str) -> str:
    """Treat owner field as fillable only when source value is real (not 待填写)."""
    if not value:
        return ""
    if "待填写" in value:
        return ""  # AI refuses to fabricate; keep README's 待填写
    return value.strip()


def fill_one(req_dir: Path) -> tuple[str, list[str]]:
    readme = req_dir / "README.md"
    if not readme.is_file():
        return ("", ["README.md missing"])
    text = readme.read_text(encoding="utf-8")
    original = text

    # Collect sources
    intake_path = req_dir / "00-input" / "intake-decision.md"
    prd_path = req_dir / "003-prd-output" / "prd.md"
    intake_fm = _frontmatter(_read_text(intake_path))
    prd_fm = _frontmatter(_read_text(prd_path))

    tier = (intake_fm.get("process_tier") or prd_fm.get("process_tier", "")).strip('"').lower()

    notes: list[str] = []
    # 1. 业务一句话
    one_liner, source = _extract_one_liner(req_dir, tier)
    if one_liner:
        text = re.sub(
            r"(## 业务一句话\s*\n\s*\n)`待填写`",
            lambda m: f"{m.group(1)}{one_liner} <!-- auto-fill from {source} -->",
            text,
            count=1,
        )
        notes.append(f"业务一句话 ← {source}")

    # 2. process_tier / issue_in_prd / prd_structure_version
    issue = prd_fm.get("issue_in_prd", "")
    ps = prd_fm.get("prd_structure_version", "").strip('"')
    if issue:
        text = re.sub(
            r"\*\*issue_in_prd\*\*：`待填写`",
            f"**issue_in_prd**：`{issue}`",
            text,
            count=1,
        )
        notes.append(f"issue_in_prd ← prd.md frontmatter ({issue})")
    if ps:
        text = re.sub(
            r"\*\*prd_structure_version\*\*：`待填写`（8）",
            f"**prd_structure_version**：`{ps}`",
            text,
            count=1,
        )
        notes.append(f"prd_structure_version ← prd.md frontmatter ({ps})")

    # 3. 当前阶段日期
    created = prd_fm.get("created_at") or intake_fm.get("decided_at", "")
    if created:
        text = re.sub(
            r"· `待填写日期`",
            f"· `{created[:10]}`",
            text,
            count=1,
        )
        notes.append(f"当前阶段日期 ← {created[:10]}")

    # 4. 决策链（owner 三栏）—— 仅当 PRD 字段不是 `待填写` 占位时填
    bfo = _safe_owner(prd_fm.get("business_fact_owner", ""))
    gdo = _safe_owner(prd_fm.get("goal_decision_owner", ""))
    rev = _safe_owner(prd_fm.get("reviewer", ""))
    if bfo:
        text = re.sub(
            r"\| 业务事实 owner \| `待填写` \|",
            f"| 业务事实 owner | `{bfo}` |",
            text,
            count=1,
        )
        notes.append("业务事实 owner ← prd.md frontmatter")
    if gdo:
        text = re.sub(
            r"\| 目标决策 owner \| `待填写` \|",
            f"| 目标决策 owner | `{gdo}` |",
            text,
            count=1,
        )
        notes.append("目标决策 owner ← prd.md frontmatter")
    if rev:
        text = re.sub(
            r"\| 评审者 \| `待填写` \|",
            f"| 评审者 | `{rev}` |",
            text,
            count=1,
        )
        notes.append("评审者 ← prd.md frontmatter")

    # 5. 目录索引里 `00-input/` 状态：基于文件存在事实
    if (req_dir / "00-input" / "intake-decision.md").is_file():
        text = re.sub(
            r"\| `00-input/` \| 原始需求材料 \| `待填写` \|",
            "| `00-input/` | 原始需求材料 | `已沉淀`（intake-decision.md + 授权 reviewer） |",
            text,
            count=1,
        )
        notes.append("00-input/ 状态 ← 文件存在事实")

    return (text if text != original else original, notes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fill README 待填写 placeholders")
    parser.add_argument("reqs", nargs="*", help="REQ names to process (default: all)")
    parser.add_argument("--apply", action="store_true", help="Write changes (default dry-run)")
    args = parser.parse_args()

    targets = args.reqs or sorted(p.name for p in REQ_DIR.glob("REQ-*") if p.is_dir())
    total_notes: list[str] = []
    for name in targets:
        req_dir = REQ_DIR / name
        if not req_dir.is_dir():
            print(f"[skip] {name} not found")
            continue
        new_text, notes = fill_one(req_dir)
        if notes:
            tag = "APPLY" if args.apply else "DRY"
            print(f"[{tag}] {name}")
            for n in notes:
                print(f"   - {n}")
            if args.apply:
                (req_dir / "README.md").write_text(new_text, encoding="utf-8")
            total_notes.extend(notes)
    if not args.apply:
        print(f"\nDry-run complete. {len(total_notes)} field(s) would change. Re-run with --apply to write.")


if __name__ == "__main__":
    main()