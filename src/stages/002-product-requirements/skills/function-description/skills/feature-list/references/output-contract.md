# Output Contract · feature-list

Produces the §功能清单 section of the parent `function-description.md` artifact (registry `output_section`: 功能清单).
Output format must match the corresponding table in `src/templates/stage-2-product/function-description.md`.

## ID Contract

- Every feature row carries a stable ID `FEA-XXX` (FEA-001, FEA-002, …), global-unique, zero-padded, no gaps, no duplicates.
- Every FEA-XXX traces to ≥1 confirmed `ST-XXX` in the `所属故事 ST` column — no orphan feature.
- Every FEA-XXX boundary is non-overlapping with every other FEA.
- IDs are never reused after a feature is removed (gap-filling breaks audit history).

## FEA Row Shape

| ID | 功能名称 | 所属故事 ST | 优先级 | 一句话描述 | 来源 |
|---|---|---|---|---|---|
| FEA-XXX | name | ST-XXX (comma-separated) | P0 / P1 / P2 | one-line scope + in/out | ST-XXX / decision |

- `所属故事 ST`: the confirmed stories this feature satisfies; must contain ≥1 `ST-XXX`.
- `优先级`: P0 (core, no workaround) / P1 (important, workaround exists) / P2 (nice to have), with rationale recorded.
- `一句话描述`: states the boundary — what the feature does and explicitly does not do.
- `来源`: the ST-XXX / decision that establishes this feature.

## Artifact States

| Status | Meaning | Downstream use |
|---|---|---|
| `draft` | Initial candidate; Audit not complete | No |
| `needs_user_input` | A material scope/boundary decision blocks confirmation | No |
| `conditional_review` | Structurally reviewable with explicit non-blocking unknowns | No |
| `ready_for_human_review` | Self-audit passed; waiting for authorized review | No |
| `confirmed` | Authorized human explicitly approved this version | Yes |
| `superseded` | A newer confirmed baseline replaces this version | No |

> A sub-skill can never write `confirmed` to the parent artifact. Only `pipeline.py review --decision approve` may. The validator's status whitelist therefore excludes `confirmed`.

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

Use all headings from `src/templates/stage-2-product/function-description.md` for the §功能清单 block (功能规格概览, 功能清单, 待确认问题, 来源追溯). If a feature has no confirmed content, write `待确认` and link it to a question or unknown ID; do not delete the heading.

> The placeholder `待确认` is preserved in the Chinese PRD convention. Translators may use `[NEEDS CLARIFICATION]` in English-only artifacts as long as the validator recognizes both forms.

## Human Responsibilities

- Product owner: confirms feature scope and boundaries.
- Business owner: confirms the feature set matches the scope baseline.
- Product manager: checks completeness, non-overlap, priority rationale, downstream usability.
- Final reviewer: authorizes the §功能清单 baseline. One person may hold multiple roles, but the decision rights must be explicit.

## Downstream Handoff

Emit a compact handoff for downstream sub-skills:

```text
confirmed_features          # FEA-XXX list
feature_boundaries          # in/out per FEA
feature_priority            # P0/P1/P2 per FEA
story_traceability          # FEA-XXX → ST-XXX map
open_nonblocking_unknowns
source_ids
```

Do not create UX flows (→ `function-description`/`functional-flow`), interaction rules (→ `interaction-rules`), page skeletons (→ `page-design`), business rules (→ `business-rules`), field validations (→ `validation-rules`), state tables (→ `state-machine`), exception paths (→ `exception-handling`), or acceptance criteria (→ `acceptance-criteria`) in this handoff.

## Clarifications Session Contract

Each Clarify Session is logged as a structured row in the parent artifact's `## Clarifications` section. One row per Session, ordered by session id:

| Field | Meaning | Example |
|---|---|---|
| `session_id` | Monotonic `CL-NNN`, zero-padded | `CL-004` |
| `category` | One of 6 Impact × Uncertainty categories (scope / data-model / UX / non-functional / integration / compliance) | `scope` |
| `question` | The single question asked this turn | "名单来源" |
| `ai_preliminary_judgment` | The AI's preliminary answer with evidence | "Inferred from ST-002: CRM 导出 CSV; needs confirmation" |
| `options` | 2–5 mutually exclusive options (or "free-form short answer") | A) CRM 导出 B) Excel 上传 C) 两者都支持 |
| `decision_owner` | Scope owner who answers | 市场部 王经理 |
| `blocking` | yes / no | `yes` |
| `deferral_risk` | What breaks if we defer | "名单导入功能边界无法确定" |
| `accepted_answer` | The chosen option after human reply | `C` |
| `reflow_target` | The artifact section that gets updated | `§功能清单 FEA-001` |
| `integrated_at` | ISO timestamp when answer was written back | `2026-08-13T10:00:00Z` |
| `integrated_by` | AI or human actor | `AI` |
| `audit_recheck` | Result of the re-Audit after integration (`pass` / `fail` / `n/a`) | `pass` |

Rules:

- One row per Session. Never merge multiple Q+A rounds into a single row.
- `accepted_answer` MUST be filled in before the artifact reaches `ready_for_human_review`.
- `reflow_target` MUST reference an existing section heading.
- `audit_recheck` MUST be the last field filled; if `fail`, switch status back to `needs_user_input` and run another Session.
- See `SKILL.md` § Clarify for the runtime order.
