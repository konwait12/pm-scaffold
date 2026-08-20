#!/usr/bin/env python3
"""Validate the structure of a mini-prd (L0 lightweight PRD) artifact.

Checks:
  1. Frontmatter present with required fields (incl. process_tier: L0)
  2. All 6 required sections present
  3. No upstream pointers (详见/内容见) — content must be embedded
  4. Confirmed artifacts have resolved confirmation fields
  5. No residual 待确认 markers in body when confirmed

Run: python3 validate_artifact.py [<mini-prd.md>] [--json]
"""

from __future__ import annotations

import argparse
import hashlib
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

try:
    from workflow_registry import artifact_content_hash
except ImportError:  # pragma: no cover - standalone invocation fallback
    def artifact_content_hash(text: str) -> str:
        canonical = re.sub(r"(?m)^(status|reviewer|reviewed_at|confirmed_at):.*$", r"\1: <review-metadata>", text)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

try:
    import hash_anchor
except ImportError:  # pragma: no cover
    hash_anchor = None

SKILL_ID = "mini_prd"
CHECK_PREFIX = "miniprd"

REQUIRED_FRONTMATTER = {
    "artifact_id", "version", "status", "owner",
    "business_fact_owner", "goal_decision_owner", "reviewer",
    "created_at", "updated_at", "confirmed_at", "process_tier",
    "upstream_artifact_ids",
}

REQUIRED_HEADINGS = [
    "改什么",
    "为什么",
    "影响范围",
    "行为需求与验收",
    "异常与边界",
    "依赖与开口问题",
]

PENDING = ("待确认",)
VALID_STATUSES = {
    "draft", "needs_user_input", "conditional_review",
    "ready_for_human_review", "confirmed",
    "superseded", "legacy_unverified", "simulated",
}


def _norm(h: str) -> str:
    return re.sub(r"\s*（[^）]*）\s*$", "", re.sub(r"^\d+\.\s*", "", h).strip()).strip()


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


def _sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE))
    result: dict[str, str] = {}
    for i, match in enumerate(matches):
        title = _norm(match.group(1))
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        result[title] = text[match.end():end].strip()
    return result


def _meaningful(body: str) -> bool:
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    body = re.sub(r"[`*_>#|~-]", "", body)
    body = re.sub(r"\s+", "", body)
    return bool(body) and not re.fullmatch(r"(待确认|暂无|无|N/?A|TBD|见上游|详见上游)+", body, re.I)


def _declared_hash(meta: dict[str, str]) -> tuple[str | None, str | None]:
    for key in ("content_sha256", "artifact_content_sha256", "manifest_sha256"):
        if key in meta:
            return key, meta[key].strip()
    return None, None


def _hash_without_declaration(text: str, key: str) -> str:
    cleaned = re.sub(rf"(?m)^{re.escape(key)}\s*:.*$\n?", "", text)
    return artifact_content_hash(cleaned)


def _req_dir_for(path: Path) -> Path | None:
    for parent in (path.parent, *path.parents):
        if (parent / "99-review").is_dir():
            return parent
    return None


def validate(path: Path) -> dict[str, object]:
    errors, warnings = [], []
    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"], "warnings": []}

    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    status = meta.get("status")

    missing = sorted(REQUIRED_FRONTMATTER - meta.keys())
    if missing:
        errors.append(f"Missing frontmatter fields: {', '.join(missing)}")

    if status and status not in VALID_STATUSES:
        errors.append(f"Invalid status '{status}'")

    # L0 档位强制：process_tier 必须是 L0（L1/L2 走完整产物链）
    tier = meta.get("process_tier", "").upper()
    if tier and tier != "L0":
        errors.append(
            f"mini-prd 只服务 L0 档位，frontmatter process_tier={meta.get('process_tier')} "
            "与档位不符——请回 intake-routing 走 L1/L2 完整产物链"
        )

    headings = [_norm(m.group(1)) for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]
    missing_h = [h for h in REQUIRED_HEADINGS if _norm(h) not in headings]
    if missing_h:
        errors.append(f"Missing required headings: {', '.join(missing_h)}")

    # A mini-PRD is useful only when each required section carries an actual
    # decision or acceptance detail; headings alone must not satisfy the gate.
    sections = _sections(text)
    empty_sections = [h for h in REQUIRED_HEADINGS if h in sections and not _meaningful(sections[h])]
    if empty_sections:
        errors.append(
            "Meaningful-content gate failed: empty or placeholder sections: "
            + ", ".join(empty_sections)
        )

    source_value = meta.get("upstream_artifact_ids", "")
    source_tokens = re.findall(r"\b(?:SRC|BG|UJ|US|FEA|FUN|FL|PD|IX|BR|VL|STATE|SM|EX|AC|REQ)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b", source_value)
    if status in {"ready_for_human_review", "confirmed"} and not source_tokens:
        errors.append("Source-trace gate failed: at least one valid upstream_artifact_ids/source ID is required")
    elif not source_tokens:
        warnings.append("Source-trace incomplete: upstream_artifact_ids has no valid source ID")

    declared_key, declared = _declared_hash(meta)
    if declared_key and not re.fullmatch(r"[0-9a-fA-F]{64}", declared or ""):
        errors.append(f"Hash declaration invalid: {declared_key} must be 64 hexadecimal characters")
    elif declared_key and declared:
        computed = _hash_without_declaration(text, declared_key)
        if declared.lower() != computed.lower():
            errors.append(
                f"Hash integrity failed: {declared_key} does not match canonical artifact content (expected {computed[:12]}…)"
            )

    req_dir = _req_dir_for(path)
    if req_dir and hash_anchor and (req_dir / "99-review" / hash_anchor.ANCHOR_FILENAME).is_file():
        chain = hash_anchor.verify_anchor_chain(req_dir)
        if not chain["ok"]:
            errors.extend(f"Hash anchor chain failed: {item}" for item in chain["issues"])
        elif status in {"ready_for_human_review", "confirmed"} and meta.get("reviewer"):
            current_hash = artifact_content_hash(text)
            rel = path.relative_to(req_dir).as_posix()
            check = hash_anchor.verify_artifact_anchored(req_dir, rel, current_hash, meta["reviewer"])
            if not check.get("anchored"):
                errors.append("Hash anchor integrity failed: latest external anchor does not match artifact hash/reviewer")

    if status == "confirmed":
        unresolved = [k for k in ("business_fact_owner", "goal_decision_owner", "reviewer", "confirmed_at")
                      if meta.get(k, "") in {"", *PENDING}]
        if unresolved:
            errors.append("Confirmed artifact has unresolved confirmation fields: " + ", ".join(unresolved))

    if any(p in text for p in PENDING) and status == "confirmed":
        body = re.sub(r"^##\s+\d+\.\s*[^\n]*$", "", text, flags=re.MULTILINE)
        if any(p in body for p in PENDING):
            warnings.append("Confirmed mini-prd still contains 待确认 markers in body")

    # 内容密度：禁止指针引用（详见 XX-XXX）
    pointer_refs = re.findall(r"(?:详见|内容见)\s*[`\[]?\s*[A-Za-z][A-Za-z0-9_\-]{0,40}", text)
    if pointer_refs:
        uniq = list(dict.fromkeys(pointer_refs))
        errors.append(
            f"Content-density gate failed: mini-prd delegates content via upstream "
            f"pointers ({', '.join(uniq[:6])}) instead of embedding it. "
            "Embed the rule/acceptance content inline; do not write '详见 XX-XXX'."
        )

    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "issues": _make_issues(errors, warnings, path)}


_MINI_ERROR_RULES = [
    ("Missing frontmatter fields:", "miniprd.missing_frontmatter"),
    ("Invalid status", "miniprd.invalid_status"),
    ("只服务 L0 档位", "miniprd.wrong_tier"),
    ("Missing required headings:", "miniprd.missing_headings"),
    ("Confirmed artifact has unresolved confirmation fields:", "miniprd.unresolved_confirmation"),
    ("Content-density gate failed:", "miniprd.pointer_only_content"),
    ("Meaningful-content gate failed:", "miniprd.empty_content"),
    ("Source-trace gate failed:", "miniprd.source_trace"),
    ("Hash declaration invalid:", "miniprd.hash_format"),
    ("Hash integrity failed:", "miniprd.hash_mismatch"),
    ("Hash anchor", "miniprd.hash_anchor"),
]

_MINI_WARNING_RULES = [
    ("Confirmed mini-prd still contains 待确认 markers", "miniprd.pending_markers_in_confirmed"),
]


def _check_id(msg: str, rules: list[tuple[str, str]], fallback: str) -> str:
    for needle, check_id in rules:
        if needle in msg:
            return check_id
    return fallback


def _make_issues(errors: list[str], warnings: list[str], path: Path) -> list[dict]:
    issues: list[dict] = []
    for e in errors:
        issues.append(make_issue(
            severity="CRITICAL",
            check_id=_check_id(e, _MINI_ERROR_RULES, "miniprd.structural"),
            family=SKILL_ID,
            location=str(path),
            message=e,
        ))
    for w in warnings:
        issues.append(make_issue(
            severity="MEDIUM",
            check_id=_check_id(w, _MINI_WARNING_RULES, "miniprd.semantic"),
            family=SKILL_ID,
            location=str(path),
            message=w,
            blocking=False,
        ))
    return issues


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path)
    p.add_argument("--json", action="store_true", dest="j")
    a = p.parse_args()
    r = validate(a.artifact)
    if a.j:
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
