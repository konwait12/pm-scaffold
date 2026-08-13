---
name: business-rules
description: Extract domain-level business rules BR-XXX (constraints, calculations, policies, permissions, timing) from confirmed UX and stories. First rule sub-skill of function-description orchestration.
---

# Business Rules · 业务规则

## Purpose And Boundary

Establish what the system must compute, enforce, and decide at the domain level — independent of how any UI presents it. Every BR must be traceable to a confirmed `ST-XXX` or `FEA-XXX` and must be executable: a developer can turn it into code without asking a follow-up question.

**Do not** describe UI behavior (→ interaction-rules `IX-XXX`), write field format/length/required checks (→ validation-rules `VL-XXX`), model state transitions (→ state-machine), define failure/recovery paths (→ exception-handling), or write acceptance tests (→ acceptance-criteria `AC-XXX`).

## Inputs And Outputs

**Input**: confirmed `product-ux` (FEA-XXX + UX steps) and confirmed upstream stories (`ST-XXX`), plus the confirmed scope baseline. **Output**: the §业务规则 section of the parent `function-description.md` (registry `output_section`: 业务规则), using the template resolved by `src/templates/resolver.py function-description.md`.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses + §2 check lenses) before analysis. Load `references/output-contract.md` before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <artifact> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "Are all upstream FEA / ST confirmed for the functions I am about to rule?"
- Enumerate P0 functions and their upstream story links. Flag missing ownership or contradictory UX as `CONFLICT` before writing any rule.
- **If no confirmed upstream function exists**, return a routing receipt and STOP — do not proceed to Intake.

### 2. Intake
- "What does the confirmed story/UX actually require the system to compute or enforce — not what I assume it means?"
- Extract candidate rules verbatim before interpreting. Tag each candidate's knowledge state: `FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT` per `src/framework/contracts.md`.
- Keep the `ST-XXX` / `FEA-XXX` source on every candidate. Do not merge claims from different sources into one rule.

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "What observable business result must the system guarantee? Which constraints are disguised as assumptions?"
- **Systems Thinking**: "Which other rules, states, fields, or features does this rule interact with? What already works and must not be broken?"
- **Role Perspective**: "For each role governed by this rule — who may, who may not, who depends on the outcome?"
- **Constraint Analysis**: "What are the hard constraints (compliance, pricing policy, legal) this rule must never violate?"
- **Adversarial**: "Could the opposite of this rule be true in some scenario? What evidence would disprove it?"
- **Reverse Validation**: "From the intended outcome backwards, what must the system compute or enforce to get there?"

### 4. Clarify
- Research discoverable facts first (existing pricing sheets, published policies, system logs).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when a missing constraint or policy decision changes a rule's outcome, scope, cost, or risk.
- Limit: ≤5 questions per session. Order by impact.
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）；送审前 dor_check 会硬检查收口与引用。

### 5. Generate
- Fill the §业务规则 table. One rule per row; force a class: 计算 / 约束 / 条件 / 权限 / 时序.
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Rule separation**: BR (domain) vs VL (field format) vs IX (interaction) vs state vs exception vs AC — no leakage.
- **Determinism**: every rule has a pass/fail judgment; no 「合理」「适当」「尽快」.
- **Traceability**: every BR-XXX links to a ST-XXX / FEA-XXX; every P0 FUN has ≥1 BR.
- **Conflict scan**: no two BRs contradict; conflicts stay visible until an authorized human resolves them.
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Present candidate §业务规则, evidence summary (which story/UX supports each rule), unknowns and their impact, required decisions, audit result, change summary.
**Only the product owner / business policy owner may approve.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → update affected rules → re-run Audit → return to Human Gate.
- Story/UX contradictions discovered later → re-enter this Skill from the beginning (not patched downstream).

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Write "系统应校验输入" without specifying the rule | Write "BR-003: 客单价 ≥ ¥500 按 VIP 档计算折扣, 公式 price×0.9, 边界 ¥499.99 不触发" |
| Define a BR that is really a UI interaction | Reference IX from product-ux; BR = domain constraint |
| Write "金额不能太大" without a bound | State exact bound and boundary behavior (e.g. 单笔 > ¥100k 需审批) |
| Copy the confirmed UX flow verbatim as "rules" | Ask "what must the system compute/enforce?" for each function |
| Skip permission rules because only the main role is mentioned | Cover every confirmed role; tag inferred ones as AI_INFERENCE |
| Write 10 pages of rules for a 1-line story | Scale rule density to input density; degrade when sparse |

## Example: Sufficient Input → Sufficient Output

**Input**: confirmed product-ux FEA-002 (活动报名) + ST-002 story specifying VVIP threshold, quota limit, and signup deadline.
**Output**: §业务规则 with BR-001..BR-004 — quota-exceeded rejection, VVIP threshold discount, deadline cutoff, quota allocation order — each classified (约束/计算/时序), traceable to ST-002 / FEA-002, with reject behavior stated.

## Example: Sparse Input → Degraded Output

**Input**: one confirmed line "活动报名要限制人数" with no threshold, no quota, no deadline.
**Output**: Preflight returns L1 → Intake registers a single candidate as `UNKNOWN` → Think identifies missing: quota number? per-user or global? first-come or lottery? deadline? → Clarify generates 3 questions → stops at `needs_user_input`. No BR is fabricated to fill the table.

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |

## Completion

Every P0 FUN-XXX has ≥1 classified, deterministic BR-XXX; every BR is traceable to a confirmed ST-XXX / FEA-XXX; no UI vocabulary leaks in; no rule contradicts another; rule density matches input density; blocking unknowns prevent confirmation; and an authorized product/policy owner approves the §业务规则 baseline.
