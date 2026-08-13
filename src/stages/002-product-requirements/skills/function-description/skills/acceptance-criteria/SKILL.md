---
name: acceptance-criteria
description: Write atomic, measurable acceptance criteria AC-XXX in Given/When/Then for each P0 function, with quantified thresholds traced to Stage 1 goals (G-XXX). Part of function-description orchestration (5/5, called last to validate all previous sub-skills).
bind: function-description (called last, validates all previous sub-skills)
---

# Acceptance Criteria 验收依据

## Purpose And Boundary

Define what "done" means for each function in a form dev, QA, and business can agree on: atomic, independently testable `AC-XXX` in Given/When/Then, with quantified thresholds or observable outcomes. Every AC is a contract between product and verification — not a test case, not a description of the interface.

**Do not** write executable test cases / assertion scripts (→ QA), domain business rules (→ `business-rules`), field validation rules (→ `validation-rules`), UI presentation or interaction (→ `interaction-rules`), state transitions (→ `state-machine`), failure recovery flows (→ `exception-handling`), or implementation detail (API, schema, framework).

## Inputs And Outputs

Inputs: confirmed `FUN-XXX` blocks with BR/VL/ST/EX from the four prior sub-skills, plus Stage 1 goals `G-XXX` from `project-background-goal` for quantified thresholds. Output: `AC-XXX` rows in parent `function-description.md` §2 分功能详述, each FUN's `#### 验收依据` subsection, following `src/templates/stage-2-product/function-description.md`.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses) before analysis. Load `references/output-contract.md` before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <artifact> --json` before review. Load `references/question-patterns.md` when success definitions or thresholds are sparse (主动向业务方确认成功标准).

## Thinking Prompts (per stage)

### 1. Preflight
- "Which FUN-XXX are in scope? Are all four rule sub-skills (BR/VL/ST/EX) confirmed? Which G-XXX goals carry quantifiable thresholds?"
- **If a P0 function has no confirmed BR/VL/ST/EX**, warn and do not fabricate AC on top of missing upstream.
- Assess maturity: L0 (no success definition) → L1 (single sparse mention) → L2 (some thresholds) → L3 (well-specified) → L4 (confirmed upstream).

### 2. Intake
- "What is the confirmed success definition for this function — from BR/VL/ST/EX, not from my assumption?"
- Preserve `FUN-XXX` → `G-XXX` / `ST-XXX` links. Flag contradictions between AC-implied behavior and upstream rules as `CONFLICT`.

### 3. Think (apply thinking-core.md §1 mandatory lenses + domain lenses)
- **First Principles**: "What observable result would prove this function works? What would the user/operator see?"
- **Testability**: "Given a set of inputs, can anyone uniquely decide pass or fail without reading the implementation?"
- **Reverse Validation**: "From the target outcome (G-XXX), what must be true and measurable?"
- **Adversarial**: "Can I construct a counterexample that passes my AC but is still broken? A case that should pass but my AC rejects?"
- **Atomicity**: "Is each AC one behavior, independently runnable, independently failing?"

### 4. Clarify
- Attempt to resolve thresholds from confirmed goals/BR/VL/EX first; do not ask what AI can derive from sources.
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when an answer changes the success definition, a key threshold, or exception-path scope.
- Limit: ≤5 questions per session. Order by impact.

### 5. Generate
- Fill `AC-XXX` rows. Each P0 FUN: ≥1 main-flow AC + ≥1 exception/boundary AC.
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Measurability**: every quantifiable result has a threshold; no "快速"/"流畅"/"合理".
- **Atomicity**: no bundled "并且" checks.
- **Traceability**: every threshold traces to a confirmed G-XXX; AI-inferred thresholds tagged `AI_INFERENCE`.
- **No Overlap**: AC is a measure of BR/VL/ST/EX, not a rewrite of them; no test-case or implementation detail leaked.
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.

### 7. Human Gate
Product owner confirms the completion definition; business owner confirms thresholds align with G-XXX goals; testing reviews verifiability (can each AC be passed/failed by constructed inputs).
**Only an authorized human may approve.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → update affected AC rows → re-run Audit → return to Human Gate.
- A threshold or success-definition change from upstream → return to the earliest affected work item.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Write "系统应正常工作" / "提升体验" as an AC | Given X, when Y, then observable Z with a quantified threshold |
| Use "快速" / "流畅" / "合理" without a baseline | ≤ 2 秒, ≥ 99.9%, 0 元 — traced to G-XXX |
| Bundle multiple checks with "并且" into one AC | One AC = one behavior, independently testable |
| Write `then 调用 checkBalance() 接口` | `then` describes the observable outcome, not internal calls |
| Describe the UI instead of the outcome ("弹窗显示…") | Describe the observable system state/result |
| Write AC only for the happy path | Main-flow AC + ≥1 exception/boundary AC per P0 FUN |
| Fabricate a threshold unrelated to business goals | Trace every threshold to a confirmed G-XXX; tag AI_INFERENCE/UNKNOWN |
| Draft test scripts or assertion code | AC is the contract; test cases are QA's job |

## Example: Sufficient Input → Sufficient Output

**Input**: FUN-001 (活动预约提交) with BR-005 (活动已结束驳回), VL-001 (姓必填), EX-001 (网络超时重试), G2 (预约成功率 ≥ 99%).
**Output**: 3 `AC-XXX` rows — main flow (Given 已登录客人填写完整信息, when 点即刻预约, then ≤3s 内进入二次确认页, 关联 G2), exception path (Given 活动已结束, when 提交, then 展示"活动已结束"页且不创建预约), boundary (Given 姓为空, when 提交, then 姓输入框显示"请输入您的姓氏").

## Example: Sparse Input → Degraded Output

**Input**: "验收标准你看着写"
**Output**: Preflight → no confirmed success definition → Clarify generates 3 batched questions (成功定义是什么？关键量化阈值 G-XXX 是多少？异常路径接受哪些失败？) → writes only the directly-supported AC rows, marks the rest `UNKNOWN`, stops at `needs_user_input`.

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

Every P0 function has at least one main-flow `AC-XXX` and one exception/boundary `AC-XXX`; every AC is atomic and Given/When/Then; every quantifiable result has a threshold traced to a confirmed G-XXX; no test-case or implementation detail leaks in; AC trigger conditions and expected outcomes are consistent with BR/VL/EX; blocking unknowns prevent confirmation; and an authorized human approves the baseline.
