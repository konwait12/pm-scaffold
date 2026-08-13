# Output Contract · business-rules

Produces the §业务规则 section of the parent `function-description.md` artifact (registry `output_section`: 业务规则).
Output format must match the corresponding table in `src/templates/stage-2-product/function-description.md`.

## ID Contract

- Every rule row carries a stable ID `BR-XXX` (BR-001, BR-002, …), global-unique, zero-padded, no gaps, no duplicates.
- Every BR-XXX is attached to exactly one `FUN-XXX` block in the parent artifact — no orphan rules outside a function block.
- Every BR-XXX `来源` references a confirmed `ST-XXX` or `FEA-XXX`.
- IDs are never reused after a rule is removed (gap-filling breaks audit history).

## Artifact States

| Status | Meaning | Downstream use |
|---|---|---|
| `draft` | Initial candidate; Audit not complete | No |
| `needs_user_input` | A material constraint or policy decision blocks confirmation | No |
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

Use all headings from `src/templates/stage-2-product/function-description.md` for the §业务规则 block (规则索引, 分功能详述, 规则冲突检查, 事实与决定, 待确认问题, 来源追溯). If a rule has no confirmed content, write `待确认` and link it to a question or unknown ID; do not delete the heading.

> The placeholder `待确认` is preserved in the Chinese PRD convention. Translators may use `[NEEDS CLARIFICATION]` in English-only artifacts as long as the validator recognizes both forms.

## Rule Row Shape

| ID | 规则描述 | 类型 | 触发条件 | 约束/逻辑 | 来源 |
|---|---|---|---|---|---|
| BR-XXX | EARS-style statement | 计算 / 约束 / 条件 / 权限 / 时序 | exact trigger | closed logic + reject behavior | ST-XXX / FEA-XXX |

## Human Responsibilities

- Product owner: confirms rule behavior and policy.
- Business policy owner: confirms constraints and calculations (thresholds, quotas, deadlines, formulas).
- Product manager: checks completeness, determinism, source coverage, downstream usability.
- Final reviewer: authorizes the §业务规则 baseline. One person may hold multiple roles, but the decision rights must be explicit.

## Downstream Handoff

Emit a compact handoff for downstream sub-skills:

```text
confirmed_rules            # BR-XXX list
rule_class_per_row         # 计算/约束/条件/权限/时序
input_fields_affected      # which F-XXX fields feed which rule
state_triggers_from_rules  # conditions that gate state-machine transitions
accepted_assumptions
open_nonblocking_unknowns
source_ids
```

Do not create field validations (→ validation-rules), state tables (→ state-machine), exception paths (→ exception-handling), or acceptance criteria (→ acceptance-criteria) in this handoff.

## Clarifications Session Contract

Each Clarify Session is logged as a structured row in the parent artifact's `## Clarifications` section. One row per Session, ordered by session id:

| Field | Meaning | Example |
|---|---|---|
| `session_id` | Monotonic `CL-NNN`, zero-padded | `CL-004` |
| `category` | One of 6 Impact × Uncertainty categories (scope / data-model / UX / non-functional / integration / compliance) | `data-model` |
| `question` | The single question asked this turn | "VIP discount threshold" |
| `ai_preliminary_judgment` | The AI's preliminary answer with evidence | "Inferred from ST-002: spend ≥ ¥500k/yr; needs confirmation" |
| `options` | 2–5 mutually exclusive options (or "free-form short answer") | A) ¥300k B) ¥500k C) ¥1M |
| `decision_owner` | Policy owner who answers | VP of Sales |
| `blocking` | yes / no | `yes` |
| `deferral_risk` | What breaks if we defer | "Discount tiers remain undecidable" |
| `accepted_answer` | The chosen option after human reply | `B (¥500k)` |
| `reflow_target` | The artifact section that gets updated | `§业务规则 BR-003` |
| `integrated_at` | ISO timestamp when answer was written back | `2026-08-13T10:00:00Z` |
| `integrated_by` | AI or human actor | `AI` |
| `audit_recheck` | Result of the re-Audit after integration (`pass` / `fail` / `n/a`) | `pass` |

Rules:

- One row per Session. Never merge multiple Q+A rounds into a single row.
- `accepted_answer` MUST be filled in before the artifact reaches `ready_for_human_review`.
- `reflow_target` MUST reference an existing section heading.
- `audit_recheck` MUST be the last field filled; if `fail`, switch status back to `needs_user_input` and run another Session.
- See `SKILL.md` § Clarify for the runtime order.
