---
name: state-machine
description: Define entity state transitions STATE-XXX — valid states, trigger events, target states, guard conditions, side effects. Third rule sub-skill of function-description orchestration.
---

# State Machine · 状态变化

## Purpose And Boundary

Enumerate every valid state of each in-scope entity and define, for every state × event combination, the target state with its guard conditions and side effects. The transition table is the authoritative source for lifecycle behavior — not a flowchart.

**Do not** design the UI for displaying states (→ interaction-rules `IX-XXX`), define database schemas or field storage (→ validation-rules / implementation), write implementation code, or duplicate exception/recovery text (→ exception-handling).

## Inputs And Outputs

**Input**: confirmed §业务规则 (`BR-XXX`) that gate transitions, confirmed `product-ux` state definitions and flows, and the confirmed scope baseline. **Output**: the §状态变化 section of the parent `function-description.md` (registry `output_section`: 状态变化), using the template resolved by `src/templates/resolver.py function-description.md`.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses + §2 check lenses) before analysis. Load `references/output-contract.md` before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <artifact> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "Which entities in scope carry more than one state? Are the governing BR-XXX confirmed?"
- Enumerate the stateful entities and the confirmed BR rules that gate their transitions. Flag any stateful P0 entity without a governing BR before modeling.
- **If no stateful entity or governing rule exists**, return a routing receipt and STOP — do not proceed to Intake.

### 2. Intake
- "What does the confirmed story/UX actually say about lifecycle — not what I imagine the flow is?"
- List every state the source names, every event it implies, and every constraint it states. Tag each as `FACT` / `DECISION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT` per `src/framework/contracts.md`. Keep the BR-XXX / FEA-XXX source on every candidate.

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "What states genuinely exist as distinct business conditions? Which 'states' are just UI views?"
- **Systems Thinking**: "Which other entities, fields, or processes react to this transition? What must not be broken?"
- **Role Perspective**: "Who triggers each event? Who may not? Who gets notified by side effects?"
- **Constraint Analysis**: "Which BR rules gate each transition? What hard constraints (compliance, timing) apply?"
- **Adversarial**: "What happens on a duplicate event, a rollback attempt, a timeout, or a concurrent trigger? Is any forbidden transition silently skipped?"
- **Reverse Validation**: "From each terminal state backwards, what must have happened for the entity to get there?"

### 4. Clarify
- Research discoverable facts first (existing system state machines, process docs, audit logs).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when an undefined transition or guard condition changes lifecycle behavior, cost, or risk.
- Limit: ≤5 questions per session. Order by impact.

### 5. Generate
- Fill the §状态变化 table: state definitions (进入/退出条件) + transition table (当前状态 | 触发事件 | 目标状态 | 条件 | 副作用 | 来源) + Mermaid state diagram.
- Forbidden transitions are stated explicitly (「不允许」), never left blank. Side effects are named or written 「无」.
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Completeness**: every state × every legal event → target state; no orphan states, no dangling transitions.
- **Guard precision**: every condition is decidable; no 「视情况」「适当时候」.
- **Side effects**: every side effect named (notification, related-entity update, audit, rollback) or 「无」.
- **Consistency**: transitions agree with the BR-XXX rules and IX references they cite.
- **Terminal semantics**: terminal/cancel states cannot transition back; no semantic contradiction.
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.

### 7. Human Gate
Present candidate §状态变化, evidence summary (which story/BR supports each transition), unknowns and impact, required decisions, audit result, change summary.
**Only the product owner / business owner may approve.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → update affected transitions → re-run Audit → return to Human Gate.
- BR or story changes upstream → re-enter this Skill from the beginning (not patched downstream).

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| List states without transition events | Every row: 当前状态 → 触发事件 → 目标状态 → 条件 → 副作用 |
| Leave a forbidden transition blank | State it explicitly: 终态回退 → 不允许 |
| Write "当订单异常时" as a condition | Decidable guard, e.g. "超时 30 分钟未支付" |
| Say "通知相关人员" as a side effect | Name who / which channel / when — or write 「无」 |
| Model only the happy path | Cover success, failure, cancel, timeout, retry, rollback, concurrency |
| Write "按钮变灰" into a state row | That's UI display → interaction-rules; state row = state + transition |

## Example: Sufficient Input → Sufficient Output

**Input**: confirmed FEA-005 (订单) + BR-009 (支付超时自动取消) + UX covering 待支付/已支付/已取消/已发货/已完成.
**Output**: §状态变化 with STATE-001..STATE-008 — state definitions with entry/exit conditions, a full transition table covering timeout auto-cancel, retry, refund rollback, and terminal states, plus a Mermaid diagram.

## Example: Sparse Input → Degraded Output

**Input**: one confirmed line "订单有状态，支付成功才算下单成功" with no state names, no events, no transitions.
**Output**: Preflight returns L1 → Intake registers a single `UNKNOWN` state set → Think identifies missing: full state list? events per state? timeout/cancel/rollback? terminal states? → Clarify generates 3 questions → stops at `needs_user_input`. No transition is fabricated.

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

Every stateful entity in every P0 FUN-XXX has a complete transition table; every state has defined entry/exit events and no orphan states; every transition has a trigger, a decidable guard condition, and named side effects; forbidden transitions are explicit; terminal states are identified and cannot regress; transitions agree with governing BR-XXX; blocking unknowns prevent confirmation; and an authorized human approves the §状态变化 baseline.
