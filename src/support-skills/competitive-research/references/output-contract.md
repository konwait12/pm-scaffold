# Output Contract · Competitive Research

## Artifact States

| Status | Meaning | Downstream use |
|---|---|---|
| `draft` | Initial candidate; Audit not complete | No |
| `needs_user_input` | A material fact or decision blocks confirmation | No |
| `conditional_review` | Structurally reviewable with explicit non-blocking unknowns | No |
| `ready_for_human_review` | Self-audit passed; waiting for authorized review | No |
| `confirmed` | Authorized human explicitly approved applicability of this version | Yes |
| `superseded` | A newer confirmed analysis replaces this version | No |

## Version Rules

- Start candidates at `v0.1`.
- Increment the minor candidate version for each human-requested revision: `v0.2`, `v0.3`.
- Use `v1.0` for the first confirmed analysis unless the host project defines another policy.
- Increment the patch/minor version for confirmed changes according to impact.
- Keep a concise change summary between human-facing versions. Do not retain every internal self-audit iteration.

## Knowledge-State Labels

| Label | Definition |
|---|---|
| `FACT` | Explicit official source statement within its authority scope (official site, published spec, verified doc) |
| `DECISION` | Explicit decision by an authorized human |
| `ASSUMPTION` | Provisional condition accepted for analysis but not confirmed |
| `AI_INFERENCE` | AI-derived interpretation supported by evidence (screenshots, reviews, comparisons) but not a confirmed business fact |
| `UNKNOWN` | Missing or unavailable public information |
| `CONFLICT` | Incompatible source statements (e.g., vendor claim vs user review) require resolution |

**Default label for this skill is `AI_INFERENCE`.** A competitor finding only becomes usable for product decisions after the business owner confirms its applicability to our context.

## Required Sections

Use all headings from the template at `src/support-skills/competitive-research/templates/competitive-analysis.md`:

- `## 竞品列表` — every selected competitor with selection rationale (direct/indirect/aspirational)
- `## 逐品分析` — per-competitor deep dive using the selected framework, with SRC-IDs
- `## 横向对比` — cross-competitor patterns, divergences, and market-standard signals
- `## 结论` — the mandatory "So What": what we should do, do differently, ignore, and not know yet

If a section has no confirmed content, write `待确认` (to be confirmed) and link it to a question or unknown ID; do not delete the heading.

## Human Responsibilities

- Research owner (PM): defines the research goal and comparison dimensions.
- Business owner: confirms competitor selection, insight applicability, and recommended actions.
- Final reviewer: authorizes the analysis for downstream use. One person may hold multiple roles, but the decision rights must be explicit.

## Downstream Handoff

Emit a compact handoff containing:

```text
confirmed_version
research_goal (business-level / functional-level)
competitor_scope (SRC-IDs, direct/indirect/aspirational)
market_standard_patterns
differentiation_gaps
so_what_recommendations (mapped to goal IDs)
open_unknowns
```

Do not create the user journey, UX rules, or feature descriptions in this handoff.

## Clarifications Session Contract

Each Clarify Session is logged as a structured row inside the artifact's `## Clarifications` section (placed after `## 结论` and before the version-change summary). One row per Session, ordered by session id:

| Field | Meaning | Example |
|---|---|---|
| `session_id` | Monotonic `CL-NNN`, zero-padded | `CL-001` |
| `category` | One of 6 Impact × Uncertainty categories (scope / data-model / UX / non-functional / integration / compliance) | `scope` |
| `question` | The single question asked this turn, paraphrased | "会员等级分几档：直接抄 A 的 3 档还是自研 5 档?" |
| `ai_preliminary_judgment` | The AI's preliminary answer with evidence | "Inferred from SRC-002 §3: 3 档覆盖主流竞品; need confirmation" |
| `options` | 2–5 mutually exclusive options (or "free-form short answer") | A) 3 档 B) 5 档 C) other |
| `decision_owner` | Business owner who answers | VP of CRM |
| `blocking` | yes / no | `yes` |
| `deferral_risk` | What breaks if we defer | "横向对比维度无法定档" |
| `accepted_answer` | The chosen option after human reply | `A (3 档)` |
| `reflow_target` | The artifact section that gets updated | `## 横向对比` |
| `integrated_at` | ISO timestamp when answer was written back | `2026-08-11T10:30:00Z` |
| `integrated_by` | AI or human actor | `AI` |
| `audit_recheck` | Result of the re-Audit after integration (`pass` / `fail` / `n/a`) | `pass` |

Rules:

- One row per Session. Never merge multiple Q+A rounds into a single row.
- `accepted_answer` MUST be filled in before the artifact reaches `ready_for_human_review`.
- `reflow_target` MUST reference an existing section heading.
- `audit_recheck` MUST be the last field filled; if `fail`, switch status back to `needs_user_input` and run another Session.
