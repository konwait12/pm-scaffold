# Output Contract · state-machine

Produces the §状态变化 section of the parent `function-description.md` artifact (registry `output_section`: 状态变化).
Output format must match the corresponding table in `src/templates/stage-2-product/function-description.md`.

## ID Contract

- Every state definition row and every transition row carries a stable ID `STATE-XXX` (STATE-001, STATE-002, …), global-unique, zero-padded, no gaps, no duplicates, never confused with `BR-XXX` (business rule) or `ST-XXX` (user story).
- Every STATE-XXX is attached to exactly one `FUN-XXX` block in the parent artifact — no orphan transitions.
- Every transition row's `来源` references a confirmed `BR-XXX` / `IX-XXX` / story statement.
- IDs are never reused after a state or transition is removed (gap-filling breaks audit history).

## Artifact States

| Status | Meaning | Downstream use |
|---|---|---|
| `draft` | Initial candidate; Audit not complete | No |
| `needs_user_input` | An undefined transition or guard decision blocks confirmation | No |
| `conditional_review` | Structurally reviewable with explicit non-blocking unknowns | No |
| `ready_for_human_review` | Self-audit passed; waiting for authorized review | No |
| `confirmed` | Authorized human explicitly approved this version | Yes |
| `superseded` | A newer confirmed baseline replaces this version | No |

## Version Rules

- Start candidates at `v0.1`.
- Increment the minor candidate version for each human-requested revision: `v0.2`, `v0.3`.
- Use `v1.0` for the first confirmed baseline unless the host project defines another policy.
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

Use all headings from `src/templates/stage-2-product/function-description.md` for the §状态变化 block (状态定义, 状态转移表, 状态机图 Mermaid, 状态完备性检查, 事实与决定, 待确认问题). If a state or transition has no confirmed content, write `待确认` and link it to a question or unknown ID; do not delete the heading.

> The placeholder `待确认` is preserved in the Chinese PRD convention. Translators may use `[NEEDS CLARIFICATION]` in English-only artifacts as long as the validator recognizes both forms.

## State Definition Row Shape

| 状态 ID | 状态名称 | 所属功能 (FUN) | 描述 | 进入条件 | 退出条件 |
|---|---|---|---|---|---|
| STATE-XXX | unique, consistent name | FUN-XXX | one-line meaning | decidable condition | decidable condition |

## Transition Row Shape

| 当前状态 | 触发事件 | 目标状态 | 条件 | 副作用 | 来源 (BR/IX) |
|---|---|---|---|---|---|
| State-A | event | State-B | decidable guard | named effects or 「无」 | BR-XXX / IX-XXX |

Forbidden transitions are listed with target = 「不允许」 and a stated reason; they are never left blank.

## Human Responsibilities

- Product owner: confirms lifecycle behavior and transition policy.
- Business owner: confirms the guard conditions and side-effect triggers rooted in business rules.
- Product manager: checks completeness, guard precision, source coverage, downstream usability.
- Final reviewer: authorizes the §状态变化 baseline. One person may hold multiple roles, but decision rights must be explicit.

## Downstream Handoff

Emit a compact handoff for downstream sub-skills:

```text
confirmed_states            # STATE-XXX list per entity
transition_matrix           # state × event → target + guard + side effect
terminal_states             # states with no legal outbound transitions
illegal_transitions         # explicit forbidden matrix
state_triggers_for_events   # which events map to exception/recovery paths
accepted_assumptions
open_nonblocking_unknowns
source_ids
```

Do not create exception/recovery narratives (→ exception-handling) or acceptance criteria (→ acceptance-criteria) in this handoff; reference them as triggers only.

## Clarifications Session Contract

Each Clarify Session is logged as a structured row in the parent artifact's `## Clarifications` section. One row per Session, ordered by session id:

| Field | Meaning | Example |
|---|---|---|
| `session_id` | Monotonic `CL-NNN`, zero-padded | `CL-010` |
| `category` | One of 6 Impact × Uncertainty categories (scope / data-model / UX / non-functional / integration / compliance) | `data-model` |
| `question` | The single question asked this turn | "Timeout auto-cancel interval" |
| `ai_preliminary_judgment` | The AI's preliminary answer with evidence | "Inferred from BR-009: 30 min unpaid → auto-cancel; needs confirmation" |
| `options` | 2–5 mutually exclusive options (or "free-form short answer") | A) 15min B) 30min C) 24h |
| `decision_owner` | Business owner who answers | Ops lead |
| `blocking` | yes / no | `yes` |
| `deferral_risk` | What breaks if we defer | "Timeout transition undecidable" |
| `accepted_answer` | The chosen option after human reply | `B (30min)` |
| `reflow_target` | The artifact section that gets updated | `§状态变化 STATE-004` |
| `integrated_at` | ISO timestamp when answer was written back | `2026-08-13T12:00:00Z` |
| `integrated_by` | AI or human actor | `AI` |
| `audit_recheck` | Result of the re-Audit after integration (`pass` / `fail` / `n/a`) | `pass` |

Rules:

- One row per Session. Never merge multiple Q+A rounds into a single row.
- `accepted_answer` MUST be filled in before the artifact reaches `ready_for_human_review`.
- `reflow_target` MUST reference an existing section heading.
- `audit_recheck` MUST be the last field filled; if `fail`, switch status back to `needs_user_input` and run another Session.
- See `SKILL.md` § Clarify for the runtime order.
