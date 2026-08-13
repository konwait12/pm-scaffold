---
name: exception-handling
description: Enumerate failure modes, retry/rollback/recovery policy, and user-visible prompts (EX-XXX) for each P0 function so the parent artifact's §异常与失败处理 is complete, decidable, and traceable. Part of function-description orchestration (4/5, after state-machine).
bind: function-description (called after state-machine)
---

# Exception Handling 异常与失败处理

## Purpose And Boundary

Define, for every in-scope function, what can go wrong and how the system responds: a decidable trigger condition, the system behavior (拦截 / 降级 / 回滚 / 阻断), a recovery path (重试 / 手动 / 自动 / 终止) with its boundary, and a user-visible Chinese prompt. Every `EX-XXX` row must be consumable by `acceptance-criteria` (AC-XXX) downstream as a verifiable failure case.

**Do not** redefine validation rules (→ `validation-rules`), domain business rules (→ `business-rules`), state transitions (→ `state-machine`), UI presentation or interaction feedback (→ `interaction-rules`), measurable acceptance cases (→ `acceptance-criteria`), or implementation-level error handling (try-catch, exception types, timeout milliseconds, message queues, idempotency keys).

## Inputs And Outputs

Inputs: per-function blocks `FUN-XXX` with confirmed states (`state-machine`), business rejection branches (`business-rules`), validation rejections (`validation-rules`), external dependency list, and confirmed failure sources. Output: `EX-XXX` rows written into parent `function-description.md` §2 分功能详述, each FUN's `#### 异常与失败处理` subsection, following `src/templates/stage-2-product/function-description.md`.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses) before analysis. Load `references/output-contract.md` before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <artifact> --json` before review. Load `references/question-patterns.md` when failure sources are sparse (主动向业务方采集失败场景).

## Thinking Prompts (per stage)

### 1. Preflight
- "Which FUN-XXX are in scope? What is each function's risk density (money, inventory, data, external dependency)?"
- Confirm upstream failure sources (state-machine, business-rules, validation-rules) exist and identify failure-source owners.
- **If no function block or no confirmed failure source exists**, return a routing receipt and STOP — do not proceed to Intake.
- Assess maturity: L0 (no failure info) → L1 (single sparse failure mention) → L2 (some failure branches) → L3 (well-specified) → L4 (confirmed upstream).

### 2. Intake
- "For this FUN, what does the upstream actually say can fail — not what I think might fail?"
- Extract failure statements verbatim before interpreting. Classify each as `FACT`, `DECISION`, `ASSUMPTION`, `AI_INFERENCE`, `UNKNOWN`, or `CONFLICT`.
- Register sources with SRC-IDs. Never invent failure scenarios from silence; a missing failure branch is `UNKNOWN`, not absent.

### 3. Think (apply thinking-core.md §1 mandatory lenses + domain lenses)
- **First Principles**: "What observable failure must the system absorb? Which failures are masked as a blanket 'system error'?"
- **Systems Thinking**: "Which upstream/downstream systems, data, or roles are affected when this fails?"
- **Failure Source Enumeration**: "Walk the six failure-source classes (校验 / 权限 / 资源 / 业务 / 冲突 / 网络) — which are genuinely possible for this function?"
- **Adversarial**: "If we did nothing here, what breaks silently? Can I construct a counterexample?"
- **Reverse Validation**: "From the recovery we promise the user, what must be true about the system's behavior?"

### 4. Clarify
- Resolve discoverable facts from upstream first (most failure points are already confirmed by business-rules / state-machine / validation-rules).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when an answer can change recovery strategy, prompt copy, or compensation behavior.
- Limit: ≤5 questions per session. Order by impact.

### 5. Generate
- Fill `EX-XXX` rows. One row per failure — trigger condition and system behavior are separate cells.
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Coverage**: every P0 FUN has ≥1 EX; every high-risk path (money, inventory, external dependency) has a defined failure branch.
- **Decidability**: every trigger condition can be reproduced by test/development without ambiguity.
- **No Silent Failure**: every EX has a user-visible prompt; no blanket "系统异常，请稍后重试" rows.
- **Boundary**: no validation rules, state transitions, interaction copy, or implementation details leaked in.
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.

### 7. Human Gate
Present: candidate EX rows, evidence summary (what sources support each failure scenario), unknowns and their impact, required decisions (recovery strategy, prompt copy, compensation), audit result, change summary.
**Only the business/function owner may approve.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → update affected EX rows → re-run Audit → return to Human Gate.
- Later contradictions → re-enter this Skill from the beginning (not patched downstream).

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Give every function one blanket "系统异常，请稍后重试" row | Enumerate which of the six failure-source classes are genuinely possible for this function |
| Write triggers like "当系统繁忙时" / "视网络情况" | Write decidable triggers: "当提交时余额不足导致扣款失败" |
| Mix trigger condition and system behavior into one sentence | One fact per row: condition (什么失败) → behavior (系统做什么) |
| Say "提示用户稍后重试" without a retry boundary | Specify retry count / interval / idempotency, or switch to manual/terminate |
| Use one prompt for recoverable and unrecoverable failures | Separate recoverable (retry/auto) from unrecoverable (terminate → human handling) |
| Handle money/inventory failures without compensation | Define rollback/compensation for money, inventory, and data-affecting failures |
| Let AI-inferred failure scenarios masquerade as FACT | Tag every EX row FACT/DECISION/AI_INFERENCE/UNKNOWN and register unknowns |
| Slip implementation detail (try-catch, timeout ms, MQ, idempotency keys) into the table | Keep product-level behavior only; implementation detail stays with engineering |

## Example: Sufficient Input → Sufficient Output

**Input**: `state-machine` + `business-rules` confirmed for FUN-001 (活动预约提交) — BR-005 (活动已结束驳回), external payment dependency with known timeout, P0 risk density high.
**Output**: 4 `EX-XXX` rows, each with decidable trigger, system behavior (拦截/降级/回滚), recovery boundary (retry 3× / 30s interval / idempotent), Chinese user prompt, and SRC trace — e.g. EX-001 网络超时 → 弹窗"提交失败，请重试" → 重试 3 次幂等提交 (B19).

## Example: Sparse Input → Degraded Output

**Input**: "给下单功能加点异常处理"
**Output**: Intake registers the source → Preflight returns L1 → six failure-source scan finds no confirmed failure info → Clarify generates 3 batched questions (哪些失败已在别处确认？金钱/库存失败是否需要补偿？重试上限是多少？) → stops at `needs_user_input`.

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

Every P0 function has at least one `EX-XXX` with a decidable trigger; every EX has a recovery path with boundary and a user-visible prompt; recoverable and unrecoverable failures are distinct; no silent failure remains; the boundary against validation/state/interaction/implementation is preserved; EX rows trace to FUN-XXX and source IDs; blocking unknowns prevent confirmation; and an authorized human approves the baseline.
