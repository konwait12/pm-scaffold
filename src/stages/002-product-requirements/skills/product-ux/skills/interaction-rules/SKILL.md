---
name: interaction-rules
description: Define page-level interaction rules IX-XXX — user operation → system response, covering normal/error/empty/loading/edge behavior. MUST stay at the page layer; business rules belong to function-description. Sub-skill of product-ux, fills §3.3.
---

# Interaction Rules

## Purpose And Boundary

Define, for each interactive element on a confirmed page, the exact pair "user operation → system response": what the user does and what the system visibly does back, including state changes, feedback timing, modal/dialog behavior, and navigation triggers. Every rule is written so a developer can implement it and a tester can reproduce it from that single rule.

**Do not** write data validation logic (→ function-description `VL-XXX`), business calculations (→ function-description `BR-XXX`), permission rules (→ function-description), or acceptance criteria (`AC-XXX`). Interaction rules describe what the *user sees and does* at the page layer; the system's domain judgment belongs downstream.

## Inputs And Outputs

Inputs: the confirmed page skeleton (§4) from `page-design`, the confirmed UX flow (§3.1/§3.2) from `ux-flow`, and the parent product-ux §2 feature list. Output: §3.3 交互规则 IX-XXX of the parent `product-ux.md` — a rule table (ID, 规则描述, 触发条件, 系统响应, 适用页面/功能, 来源) written per `references/rule-writing-format.md`. Not a standalone artifact.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses) before analysis. Load `references/output-contract.md` before drafting. Load `references/rule-writing-format.md` before writing any rule. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <product-ux.md> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "Which pages and interactive elements are confirmed? Which FEA and flow step does each rule trace to?"
- Enumerate pages from §4; on each, list clickable/tappable elements from the actions column.
- **If the page skeleton is missing or unconfirmed**, return a routing receipt and STOP — rules cannot be attached to invented pages.

### 2. Intake
- "What does each confirmed action actually trigger — not what a generic pattern says it should?"
- Collect verbatim from §4 actions and §3.1 flow branches: the operation, its precondition, and the intended outcome.
- Classify each rule claim as `FACT`, `DECISION`, `ASSUMPTION`, `AI_INFERENCE`, `UNKNOWN`, or `CONFLICT` per `src/framework/contracts.md`.
- A response I invent for completeness must be tagged `AI_INFERENCE`.

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "What is the observable feedback the user must get after this operation? What feedback is implied but unstated?"
- **Systems Thinking**: "Does this response depend on a downstream system result (async, payment, notification) that must be represented as a state?"
- **Adversarial**: "What happens on double-click, timeout, network loss, or a stale page? Is the error response defined?"
- **Reverse Validation**: "From the desired user experience backwards, what responses must exist for each operation?"
- **Confirmation Bias Defense**: "Am I writing the rule the requester assumed ('submit shows a success toast') or the rule the flow actually needs?"
- **Knowledge Boundary**: "Which responses are confirmed and which are my page-layer inference?"

### 4. Clarify
- Resolve discoverable gaps first (re-check page actions, flow branches, platform conventions).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when the answer changes a P0 page's interaction or feedback behavior.
- Limit: ≤5 questions per session. Do not ask about business rules (→ function-description) or visual styling.

### 5. Generate
- One rule per interactive element or behavior, in §3.3 table form or paragraph form per `rule-writing-format.md`.
- Assign `IX-XXX` IDs sequentially and uniquely; every rule references its applicable page and its `FEA-XXX`.
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Completeness**: every P0 page's interactive elements have a rule; no orphan rules without a page.
- **State Coverage**: loading/empty/error/disabled/timeout covered per rule where applicable.
- **Boundary**: scan for validation/calculation/permission keywords → route to function-description.
- **Implementability**: no "合理提示"/"适当反馈" vagueness; each response is a concrete action or state.
- Run `scripts/validate_artifact.py <product-ux.md> --json`. Fix all errors. Warnings → document.

### 7. Human Gate
Present: the IX rule list grouped by layer (entry/identity, core operation, feedback/exception), per-rule trigger→response, and any rule marked `AI_INFERENCE`.
**Product owner confirms interaction behavior; business owner confirms feedback/error handling.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → update affected rules → re-run Audit → return to Human Gate.
- A changed page action (from page-design) invalidates the rules hanging on it → return to the affected rules, not a downstream patch.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Write a functional sentence without the system response ("点击进入下一步") | Pair every trigger with an observable system response |
| Write the system action without the trigger context ("系统打开弹窗") | State what the user did to cause it |
| Describe only the success path | Cover loading, empty, error, disabled, timeout for each element |
| Say "给出合理提示" / "适当反馈" | Give a concrete response: specific message, page, or state |
| Write "密码必须 8 位" / "仅 VIP 可操作" / "库存不足禁止下单" | Route validation/calculation/permission to function-description |
| Create orphan rules not tied to a page | Every IX references an applicable page + FEA-XXX |
| Copy interaction rules between pages blindly | Reuse via a shared, referenceable rule; vary only what genuinely differs |

## Example: Sufficient Input → Sufficient Output

**Input**: confirmed pages for "场地预约" FEA-001 (场地列表页, 详情页, 填写页, 结果页) with actions and next states from page-design.
**Output**: §3.3 IX rules — e.g., IX-001 场地卡片点击→进入详情页; IX-002 提交按钮 loading→成功跳结果页/失败驻留表单+错误提示; IX-003 未登录点击预约→跳登录页、登录后回跳; IX-004 名额满的场地置灰不可点; each with trigger→response, applicable page, source, and no BR/VL leakage.

## Example: Sparse Input → Degraded Output

**Input**: "给预约流程加些交互规则吧" with no confirmed pages or actions.
**Output**: Preflight returns L1 (no page skeleton) → Intake notes no rule material → Think lists missing (哪些可交互元素? 触发与响应? 异常反馈?) → Clarify generates ≤5 batched questions → stops at `needs_user_input`. No IX rules are invented for nonexistent pages.

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（写规则时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | §3.3 产出结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/rule-writing-format.md` | 交互规则书写格式（段落式，必读） | 写任何规则前 |
| `references/source-handling.md` | 上游追溯规则（FEA-/PG-/SRC- 引用） | Intake/追溯时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 交互规则领域 lens，必读） | 每次任务开始（必读） |

## Completion

Every P0 page's interactive elements have an `IX-XXX` rule with trigger → system response; state coverage (loading/empty/error/disabled/timeout) is addressed where applicable; every rule references its applicable page and FEA; no data-validation, calculation, or permission logic leaks into IX; rules are written so a developer can implement and a tester can reproduce them; the rule table matches the page/flow inventory; and an authorized human approves the interaction rules before function-description runs.
