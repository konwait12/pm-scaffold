# Output Contract · Solution Assessment

## Artifact States

| Status | Meaning | Downstream use |
|---|---|---|
| `draft` | Initial candidate; Audit not complete | No |
| `needs_user_input` | A material fact or decision blocks confirmation | No |
| `conditional_review` | Structurally reviewable with explicit non-blocking unknowns | No |
| `ready_for_human_review` | Self-audit passed; waiting for authorized review | No |
| `confirmed` | Authorized human explicitly approved this version | Yes |
| `superseded` | A newer confirmed assessment replaces this version | No |

## Version Rules

- Start candidates at `v0.1`.
- Increment the minor candidate version for each human-requested revision: `v0.2`, `v0.3`.
- Use `v1.0` for the first confirmed assessment unless the host project defines another policy.
- Increment the patch/minor version for confirmed changes according to impact.
- Keep a concise change summary between human-facing versions. Do not retain every internal self-audit iteration.

## Knowledge-State Labels

| Label | Definition |
|---|---|
| `FACT` | Explicit source statement within the source's authority scope (e.g., quoted vendor quote, published price) |
| `DECISION` | Explicit decision by an authorized human |
| `ASSUMPTION` | Provisional condition accepted for analysis but not confirmed (e.g., estimated headcount) |
| `AI_INFERENCE` | AI-derived estimate or interpretation supported by evidence but not a confirmed business fact |
| `UNKNOWN` | Missing information |
| `CONFLICT` | Incompatible source statements require resolution |

**Cost/risk figures are rarely FACT.** Estimates must be labeled `AI_INFERENCE` or `ASSUMPTION` and given an owner until the decision owner confirms them.

## Required Sections

### Feasibility mode

Use all headings from `src/support-skills/solution-assessment/feasibility-templates/feasibility-report.md`:

- `## 市场空间` — target users, penetration, theoretical space
- `## 技术可行性` — each challenge → Verified / Needs Verification / Not Feasible
- `## 投入产出` — R&D cost, ops cost, expected revenue, payback period
- `## 风险评估` — each risk → impact + probability + mitigation
- `## 结论` — 做 / 不做 / 有条件做, with specific measurable conditions and AI recommendation

### Comparison mode

Use all headings from `src/support-skills/solution-assessment/solution-comparison-templates/solution-comparison.md`:

- `## 候选方案` — every solution at equal depth (description, cost, scope, timeline, risk, pros/cons)
- `## 方案对比矩阵` — weighted criteria (defined BEFORE scoring) × scores = ranked results
- `## AI 推荐` — recommended option with confidence (HIGH/MEDIUM/LOW), accepted trade-offs, and conditions that would change the recommendation
- `## 人工决策` — the human's choice recorded as DEC-XXX with rationale, decision-maker, and date

If a section has no confirmed content, write `待确认` and link it to a question or unknown ID; do not delete the heading.

## Human Responsibilities

- Decision owner: makes the final choice (or Go/No-Go) and confirms material figures.
- PM: defines criteria, checks equal-depth description, owns the recommendation's clarity.
- Final reviewer: authorizes the assessment for downstream use. One person may hold multiple roles, but the decision rights must be explicit.

## Downstream Handoff

Emit a compact handoff containing:

```text
confirmed_version
mode (feasibility | comparison)
recommendation (with confidence)
human_decision (DEC-XXX)
key_assumptions_that_flip_it
scope_impact (which Work Items to reflow if any)
source_ids
```

Do not create new requirements or designs in this handoff.

## Clarifications Session Contract

Each Clarify Session is logged as a structured row inside the artifact's `## Clarifications` section (placed after the last content section and before the version-change summary). One row per Session, ordered by session id:

| Field | Meaning | Example |
|---|---|---|
| `session_id` | Monotonic `CL-NNN`, zero-padded | `CL-001` |
| `category` | One of 6 Impact × Uncertainty categories (scope / data-model / UX / non-functional / integration / compliance) | `scope` |
| `question` | The single question asked this turn, paraphrased | "通知模块自研 vs 外采的预算上限是多少?" |
| `ai_preliminary_judgment` | The AI's preliminary answer with evidence | "Inferred from SRC-002: 自研 2 人×4 周 ≈ ¥X; need confirmation" |
| `options` | 2–5 mutually exclusive options (or "free-form short answer") | A) ≤¥10万 B) ≤¥30万 C) other |
| `decision_owner` | The decision owner who answers | VP of Engineering |
| `blocking` | yes / no | `yes` |
| `deferral_risk` | What breaks if we defer | "成本维度无法打分，矩阵无法收敛" |
| `accepted_answer` | The chosen option after human reply | `A (≤¥10万)` |
| `reflow_target` | The artifact section that gets updated | `## 方案对比矩阵` |
| `integrated_at` | ISO timestamp when answer was written back | `2026-08-11T10:30:00Z` |
| `integrated_by` | AI or human actor | `AI` |
| `audit_recheck` | Result of the re-Audit after integration (`pass` / `fail` / `n/a`) | `pass` |

Rules:

- One row per Session. Never merge multiple Q+A rounds into a single row.
- `accepted_answer` MUST be filled in before the artifact reaches `ready_for_human_review`.
- `reflow_target` MUST reference an existing section heading.
- `audit_recheck` MUST be the last field filled; if `fail`, switch status back to `needs_user_input` and run another Session.
