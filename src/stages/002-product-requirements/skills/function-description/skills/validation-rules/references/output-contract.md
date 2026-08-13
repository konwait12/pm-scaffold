# Output Contract · validation-rules

Produces the §系统校验 section of the parent `function-description.md` artifact (registry `output_section`: 系统校验).
Output format must match the corresponding table in `src/templates/stage-2-product/function-description.md`.

## ID Contract

- Every validation row carries a stable ID `VL-XXX` (VL-001, VL-002, …), global-unique, zero-padded, no gaps, no duplicates, never confused with `BR-XXX`.
- Every VL-XXX is attached to exactly one `FUN-XXX` block in the parent artifact — no global pile-up outside a function block.
- Every VL-XXX `来源` references a confirmed `BR-XXX` / `FEA-XXX` / field definition (F-XXX).
- IDs are never reused after a check is removed (gap-filling breaks audit history).

## Artifact States

| Status | Meaning | Downstream use |
|---|---|---|
| `draft` | Initial candidate; Audit not complete | No |
| `needs_user_input` | A validation boundary or error-message decision blocks confirmation | No |
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

Use all headings from `src/templates/stage-2-product/function-description.md` for the §系统校验 block (校验索引, 分功能详述, 校验覆盖检查, 事实与决定, 待确认问题). If a check has no confirmed content, write `待确认` and link it to a question or unknown ID; do not delete the heading.

> The placeholder `待确认` is preserved in the Chinese PRD convention. Translators may use `[NEEDS CLARIFICATION]` in English-only artifacts as long as the validator recognizes both forms.

## Rule Row Shape

| ID | 校验内容 | 校验规则 | 触发时机 | 错误提示 | 关联字段 (F) | 关联业务规则 (BR) | 来源 |
|---|---|---|---|---|---|---|---|
| VL-XXX | what is checked | executable value domain | when it fails | Chinese message (≤30 chars) | F-XXX | BR-XXX | FACT/DECISION/... |

## 字段定义表 (Field Definition Table)

按需产出（P1 按需），并入老版「字段规则说明」（字段名称、类型、长度、校验规则、来源）；同域合并到本 Skill。当上游 product-ux 的字段定义需要补充实现级字段契约时，在 §系统校验 内产出 `字段定义表` 小节。字段级校验逻辑由 VL-XXX 承担，本表只登记字段契约，不重复撰写校验表达式。

| 字段 ID | 字段名 | 类型 | 长度/范围 | 必填 | 来源（上游 IX/FUN） | 关联校验 VL-XXX |
|---|---|---|---|---|---|---|
| F-XXX | field name | string/int/... | length or value domain | 是/否 | IX-XXX / FUN-XXX | VL-XXX |

- 每个 `F-XXX` 全局唯一、零填充，不得与 `BR-XXX` / `VL-XXX` 混淆。
- `来源（上游 IX/FUN）` 必须引用上游已确认的 interaction-rules（IX-XXX）或 function-description（FUN-XXX）。
- 每个 F-XXX 至少关联一个 VL-XXX；未定义校验的字段在 `校验覆盖检查` 中标 ⚠️。
- 表头缺「字段名/类型」或字段无来源引用时，`validate_artifact.py` 仅记 warning（不阻塞），由人工评审把关。

## Human Responsibilities

- Product owner: confirms check boundaries and error-message copy.
- Business owner: confirms value domains (phone charset, amount caps, codebooks) traceable to business facts.
- Product manager: checks coverage, decidability, user-facing quality of messages, downstream usability.
- Final reviewer: authorizes the §系统校验 baseline. One person may hold multiple roles, but decision rights must be explicit.

## Downstream Handoff

Emit a compact handoff for downstream sub-skills:

```text
confirmed_checks           # VL-XXX list
field_coverage_map         # every user-input field → its VLs; gaps flagged
cross_field_dependencies   # A-required-when-B relations (for AC and tests)
error_message_copy         # final Chinese copy per VL
accepted_assumptions
open_nonblocking_unknowns
source_ids
```

Do not create business rules (→ business-rules), state tables (→ state-machine), exception paths (→ exception-handling), or acceptance criteria (→ acceptance-criteria) in this handoff.

## Clarifications Session Contract

Each Clarify Session is logged as a structured row in the parent artifact's `## Clarifications` section. One row per Session, ordered by session id:

| Field | Meaning | Example |
|---|---|---|
| `session_id` | Monotonic `CL-NNN`, zero-padded | `CL-007` |
| `category` | One of 6 Impact × Uncertainty categories (scope / data-model / UX / non-functional / integration / compliance) | `data-model` |
| `question` | The single question asked this turn | "Mobile number charset" |
| `ai_preliminary_judgment` | The AI's preliminary answer with evidence | "Inferred from BR-005: mainland CN, ^1[3-9]; needs confirmation" |
| `options` | 2–5 mutually exclusive options (or "free-form short answer") | A) mainland CN B) CN+HK C) global E.164 |
| `decision_owner` | Field/format owner who answers | Product owner |
| `blocking` | yes / no | `yes` |
| `deferral_risk` | What breaks if we defer | "Format regex undecidable" |
| `accepted_answer` | The chosen option after human reply | `A (mainland CN)` |
| `reflow_target` | The artifact section that gets updated | `§系统校验 VL-003` |
| `integrated_at` | ISO timestamp when answer was written back | `2026-08-13T11:00:00Z` |
| `integrated_by` | AI or human actor | `AI` |
| `audit_recheck` | Result of the re-Audit after integration (`pass` / `fail` / `n/a`) | `pass` |

Rules:

- One row per Session. Never merge multiple Q+A rounds into a single row.
- `accepted_answer` MUST be filled in before the artifact reaches `ready_for_human_review`.
- `reflow_target` MUST reference an existing section heading.
- `audit_recheck` MUST be the last field filled; if `fail`, switch status back to `needs_user_input` and run another Session.
- See `SKILL.md` § Clarify for the runtime order.
