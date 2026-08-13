---
name: page-design
description: Define the page skeleton for each step in the confirmed functional flow — entry trigger, preconditions, main content areas, available actions, and next state — without visual design. Sub-skill of product-ux, fills §2 页面设计 (page skeletons) of product-ux.md.
---

# Page Design

## Purpose And Boundary

Turn every step in the confirmed functional flow into a concrete page/step skeleton: how the user arrives, what must already be true, what content the page carries, what actions the user can take, and where each action leads. The result must be consumable by `interaction-rules` (which adds IX behavior) and by function-description (which adds BR/VL/AC) without re-interpreting.

**Do not** specify visual design (colors, fonts, spacing, component styling), write interaction micro-details (animation, hover, scroll, modal appearance), design database models, or define business/validation/permission rules. Page skeleton is a content-and-navigation contract, not a mockup.

## Inputs And Outputs

Inputs: the confirmed functional flow (§2.1 主流程 / §2.2 分支流程 / §2.3 异常流程) from `functional-flow` (in function-description), the feature list (`FEA-XXX`) from function-description's `feature-list`, and the confirmed stories they trace to. Output: §2 页面设计 of the parent `product-ux.md` (§2.1 页面与步骤描述 table + §2.2 HTML 原型 entry when needed), following `src/templates/stage-2-product/product-ux.md`. Not a standalone artifact.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses) before analysis. Load `references/output-contract.md` before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <product-ux.md> --json` before review. Load `references/prototype-techniques.md` when the flow has ≥3 pages or needs stakeholder review of look-and-feel.

## Thinking Prompts (per stage)

### 1. Preflight
- "Which pages/steps come out of the confirmed functional flow? Which FEA and story does each trace to?"
- Extract the page inventory from the functional flow's §2.1 主流程 / §2.2 分支流程 / §2.3 异常流程. Any page not present in the flow must be flagged, not silently added.
- **If the functional flow is missing or unconfirmed**, return a routing receipt and STOP — page skeletons cannot be invented without steps to hang on.

### 2. Intake
- "What does each flow step actually imply about content, actions, and next states — not what I think a good page looks like?"
- Collect verbatim from the flow: step name, entry edge, branch conditions that reach it, exit edges.
- Classify page facts as `FACT`, `DECISION`, `ASSUMPTION`, `AI_INFERENCE`, `UNKNOWN`, or `CONFLICT` per `src/framework/contracts.md`.
- A content block or action I add for completeness must be tagged `AI_INFERENCE`.

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "What must the user see and do here to advance toward the outcome? Which elements are assumed but not required?"
- **Systems Thinking**: "Does this page's action chain to a data source, another role's task, or an external service?"
- **Adversarial**: "What happens when a precondition fails? Is there an entry path that bypasses the preconditions I assumed?"
- **Reverse Validation**: "From the next-state backwards, what content/action must this page provide so the next step can run?"
- **Confirmation Bias Defense**: "Am I designing the page the requester sketched, or the page the flow actually needs?"
- **Knowledge Boundary**: "Which page facts are confirmed and which are my structural inference?"

### 4. Clarify
- Resolve discoverable gaps first (re-check flow branches, story text, role definitions).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when the answer changes a P0 page's entry, preconditions, content, actions, or next state.
- Limit: ≤5 questions per session. Do not ask about visual styling (out of scope) or rules (downstream).
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）；送审前 dor_check 会硬检查收口与引用。

### 5. Generate
- One row per page/step in the §2.1 table: 页面/步骤, 所属功能, 入口, 前置条件, 主要内容, 操作, 下一状态.
- Keep content at the "what is on the page" level; keep actions one-per-row with an explicit next state (including 停留本页 / 退出流程).
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Completeness**: every page from the functional flow has a row; no orphan pages; every page has ≥1 action.
- **Action-NextState Closure**: every action has an explicit next state; no dangling arrows.
- **Boundary**: no visual styling, no interaction micro-details, no BR/VL/AC.
- **Traceability**: each row traces to FEA-XXX and a flow step.
- Run `scripts/validate_artifact.py <product-ux.md> --json`. Fix all errors. Warnings → document.
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Present: the page inventory, per-page entry/precondition/action/next-state, pages marked `AI_INFERENCE`, and any page that over-reaches into visual design.
**Product owner confirms page inventory and navigation; business owner confirms preconditions and next states.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → update affected rows → re-run Audit → return to Human Gate.
- A changed flow step (from functional-flow) invalidates the pages hanging on it → return to the affected pages, not a downstream patch.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Write content as visual layout ("top big button, blue card below") | Describe what information the page presents |
| List actions without next states | Give every action an explicit next state (success/fail/stay/exit) |
| Merge multiple actions into one vague sentence | One action per row, each with a defined outcome |
| Add pages not present in the functional flow | Every page traces to a flow step + FEA-XXX |
| Only design the happy-path page | Cover normal/alternate/error/timeout/cancel/recovery variants |
| Sneak in interaction micro-details or rules | Keep skeletons at content-and-navigation level |
| Split pages by "screen count" without reason | Split by genuine state/step differences |

## Example: Sufficient Input → Sufficient Output

**Input**: confirmed functional flow with 4 steps for "场地预约" FEA-001 (列表→详情→填写→结果) plus confirmed stories.
**Output**: §2.1 table rows — 场地列表页 (入口: 首页导航; 前置: 已登录; 内容: 场地卡片列表+筛选; 操作: 筛选/查看详情/下拉刷新; 下一状态: 详情页/列表刷新), 场地详情页, 填写页, 结果页 — each with explicit entry/precondition/actions/next states and knowledge tags.

## Example: Sparse Input → Degraded Output

**Input**: "给预约流程做个页面吧" with no flow steps confirmed.
**Output**: Preflight returns L1 (no flow) → Intake notes no page material → Think lists missing (页面清单? 前置条件? 操作与下一状态?) → Clarify generates ≤5 batched questions → stops at `needs_user_input`. No page rows are invented from a blank slate.

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（写页面时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | §2 产出结构与 ID 契约 | Draft 前 |
| `references/prototype-techniques.md` | 可点击原型技法：先出页面清单经人工确认，再生成单文件 HTML；覆盖主流程与全部分支场景（≥3 页或多方评审时用） | 需原型时（可选） |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 上游追溯规则（FEA-/ST-/SRC- 引用） | Intake/追溯时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 页面领域 lens，必读） | 每次任务开始（必读） |

## Completion

All pages/steps from the confirmed functional flow have a §2.1 row with entry, preconditions, content, actions, and next state; every page has at least one action and every action has an explicit next state; page inventory matches the flow with no orphan or invented pages; content stays at information-and-navigation level without visual or interaction/rules leakage; prototype (if any) is a communication aid, not a substitute for the table; and an authorized human approves the page skeleton before interaction-rules runs.
