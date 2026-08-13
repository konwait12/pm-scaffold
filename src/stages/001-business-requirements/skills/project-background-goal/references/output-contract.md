# Output Contract

## Artifact States

| Status | Meaning | Downstream use |
|---|---|---|
| `draft` | Initial candidate; Audit not complete | No |
| `needs_user_input` | A material fact or decision blocks confirmation | No |
| `conditional_review` | Structurally reviewable with explicit non-blocking unknowns and unknown | No |
| `ready_for_human_review` | Self-audit passed; waiting for authorized review | No |
| `confirmed` | Authorized human explicitly approved this version | Yes |
| `superseded` | A newer confirmed baseline replaces this version | No |

## Version Rules

- Start candidates at `v0.1`.
- Increment the minor candidate version for each human-requested revision: `v0.2`, `v0.3`.
- Use `v1.0` for the first confirmed baseline unless the host project defines another policy.
- Increment the patch/minor version for confirmed baseline changes according to impact.
- Keep a concise change summary between human-facing versions. Do not retain every internal self-audit iteration.

## Knowledge-State Labels

| Label | Definition |
|---|---|
| `FACT` | Explicit source statement within the source's authority scope |
| `DECISION` | Explicit decision by an authorized human |
| `ASSUMPTION` | Provisional condition accepted for analysis but not confirmed |
| `AI_INFERENCE` | AI-derived interpretation supported by evidence but not a business fact |
| `UNKNOWN` | Missing information |
| `CONFLICT` | Incompatible source statements require resolution |

## Required Sections

Use all headings from `src/templates/stage-1-business/background-goal.md`. If a section has no confirmed content, write `待确认` (to be confirmed) and link it to a question or unknown ID; do not delete the heading.

> The placeholder `待确认` is preserved in the Chinese PRD convention. Translators may use `[NEEDS CLARIFICATION]` in English-only artifacts as long as the validator recognizes both forms.

## Human Responsibilities

- Business fact owner: confirms current-state facts and business context.
- Goal decision owner: confirms intended outcomes, success judgment, timing, and acceptable risk.
- Product manager: checks completeness, clarity, source coverage, and downstream usability.
- Final reviewer: authorizes the baseline for downstream use. One person may hold multiple roles, but the decision rights must be explicit.

## Downstream Handoff

Emit a compact handoff containing:

```text
confirmed_version
background_summary
goal_summary
confirmed_roles
known_lifecycle_clues
constraints_and_dependencies
accepted_assumptions
open_nonblocking_unknowns
source_ids
```

Do not create the user journey or user stories in this handoff.

## Clarifications Session Contract

Each Clarify Session is logged as a structured row inside the artifact's `## Clarifications` section (placed after §11 待确认问题 and before §14 Constitution Compliance). One row per Session, ordered by session id:

| Field | Meaning | Example |
|---|---|---|
| `session_id` | Monotonic `CL-NNN`, zero-padded | `CL-001` |
| `category` | One of 6 Impact × Uncertainty categories (scope / data-model / UX / non-functional / integration / compliance) | `scope` |
| `question` | The single question asked this turn, paraphrased | "VVIP threshold for invitation scope" |
| `ai_preliminary_judgment` | The AI's preliminary answer with evidence | "Inferred from SRC-002 §3: VVIP = spend ≥ ¥500k/year; need confirmation" |
| `options` | 2–5 mutually exclusive options (or "free-form short answer") | A) ¥500k B) ¥300k C) ¥1M D) other |
| `decision_owner` | Fact owner or decision owner who answers | VP of CRM |
| `blocking` | yes / no | `yes` |
| `deferral_risk` | What breaks if we defer | "Scope of invitations remains undecidable" |
| `accepted_answer` | The chosen option after human reply | `A (¥500k)` |
| `reflow_target` | The artifact section that gets updated | `§8 初步边界与非目标` |
| `integrated_at` | ISO timestamp when answer was written back | `2026-08-11T10:30:00Z` |
| `integrated_by` | AI or human actor | `AI` |
| `audit_recheck` | Result of the re-Audit after integration (`pass` / `fail` / `n/a`) | `pass` |

Rules:

- One row per Session. Never merge multiple Q+A rounds into a single row.
- `accepted_answer` MUST be filled in before the artifact reaches `ready_for_human_review`.
- `reflow_target` MUST reference an existing section heading.
- `audit_recheck` MUST be the last field filled; if `fail`, switch status back to `needs_user_input` and run another Session.
- See `SKILL.md` § Clarify Is Its Own Loop for the runtime order.