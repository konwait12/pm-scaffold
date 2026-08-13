---
name: feasibility-analysis
description: Assess whether a concrete product-level solution is feasible across the four dimensions 市场空间 / 技术可行性 / 投入产出 / 风险评估, and produce a 做 / 不做 / 有条件做 recommendation with explicit AI confidence. When ≥2 materially different solutions exist for the same goal, handle the tradeoff as the §多方案取舍 chapter inside the feasibility report (weighted decision matrix defined before scoring) — never as a standalone deliverable. AI recommends; the human decision owner decides.
---

# Feasibility Analysis · 可行性分析

## Purpose And Boundary

When technical, compliance, resource, or business constraints call the feasibility of a concrete product-level solution into question, this skill frames the assessment objectively across four dimensions — **市场空间、技术可行性、投入产出、风险评估** — and presents a 做 / 不做 / 有条件做 recommendation with confidence — but **never makes the final decision**. The human decision-maker owns the choice.

When ≥2 materially different solutions exist for the same goal (build vs. buy, different approaches, different scope tradeoffs), the comparison is handled as the **§多方案取舍** chapter inside the feasibility report, using a weighted decision matrix defined before scoring. It is a chapter — not an independent deliverable.

**Do not** make the final decision, silently update scope, design architecture, or assess solutions that differ only in implementation detail (those belong to engineering, not product). Feasibility assessment requires a concrete product-level solution to already exist — you cannot assess "can we build X" until X is concrete.

## Inputs And Outputs

Inputs: a concrete product-level solution (from `product-ux` or `function-description`) or an explicit feasibility decision request, upstream evidence (background-goal, cost/constraint/compliance inputs), and a named decision-owner. If the decision would change confirmed scope, cost, compliance, or risk posture, stop at `needs_user_input` until the decision owner is identified.

Output: a single `feasibility-report.md` using the template at `src/templates/support/feasibility-report.md` — 市场空间 / 技术可行性 / 投入产出 / 风险评估 / §多方案取舍（≥2 实质方案时）/ 结论（做/不做/有条件做）. The §多方案取舍 chapter, when present, follows the multi-solution comparison template at `src/templates/support/solution-comparison.md` as its chapter structure; it is embedded in the report, never produced as a separate artifact.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses) before analysis. Load `references/source-handling.md` at Intake. Load `references/question-patterns.md` at Clarify. Load `references/output-contract.md` before drafting. Load `references/anti-patterns.md` at Generate. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <artifact> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "Is there a feasibility question to answer across market / technical / cost-benefit / risk? Does a concrete product-level solution exist?"
- "Are there ≥2 genuinely different solutions for the same goal? If so, the §多方案取舍 chapter applies (weighted matrix inside the report)."
- "If solutions differ only in implementation detail, route to engineering, not product."
- Identify decision_owner. **If no decision owner exists, return a routing receipt and STOP at `needs_user_input`.**
- Assess maturity: L0 (no concrete solution) → L1 (vague idea) → L2 (product-level solution exists) → L3 (cost/constraint data present) → L4 (confirmed upstream).

### 2. Intake
- "What does each source actually say about cost, constraints, compliance, dependencies, and risk — not what I assume?"
- Gather four-dimension evidence: 市场空间 (target users, comparable penetration, theoretical space); 技术可行性 (each challenge → 已验证 / 待验证 / 不可行); 投入产出 (R&D + ops cost, expected revenue, payback period); 风险评估 (each risk → impact + probability + mitigation).
- When the §多方案取舍 chapter applies, for each candidate solution: approach summary, technical dependencies, resource estimate (people + time), key risks, reversibility.
- Classify knowledge states per `src/framework/contracts.md`: FACT / DECISION / ASSUMPTION / AI_INFERENCE / UNKNOWN / CONFLICT. Retain SRC-IDs.

### 3. Think (apply thinking-core.md §1 mandatory lenses + assessment domain lenses)
- **First Principles**: "What is the observable decision to make? Which costs and risks are assumptions disguised as requirements?"
- **Systems Thinking**: "Which upstream/downstream work items, roles, and dependencies does the decision affect?"
- **Adversarial**: "Could the obvious recommendation be a trap? Is the evidence one-sided? Is urgency asserted without a real deadline?"
- **Reverse Validation**: "From the preferred outcome backwards, what must be true for each solution to succeed?"
- Domain lenses (see `references/thinking-framework.md`): Occam's Razor (fewest dependencies when multiple solutions meet the goal), Opportunity Cost (what we give up by choosing), Reversibility (can we undo a wrong choice?).

### 4. Clarify
- Research discoverable facts first (cost benchmarks, public pricing, past project data).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when an answer changes the recommendation, a criterion weight, or a material cost/risk figure.
- Limit: ≤5 questions per session. Order by impact.

### 5. Generate
- 主线四维度：市场空间 → 技术可行性 → 投入产出 → 风险评估 → 结论（做/不做/有条件做，条件须具体可衡量）.
- **§多方案取舍 章节**（仅当存在 ≥2 个实质不同方案时）: 候选方案（等深描述）→ 权重在打分前定义 → 方案对比矩阵 → AI 推荐（HIGH/MEDIUM/LOW 置信度）→ 敏感度分析 → 人工决策. 该章节用 `src/templates/support/solution-comparison.md` 作为章节结构模板，嵌入 `feasibility-report.md`，不独立产出.
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Anchoring Check**: Were criteria defined before scores, or did the winning solution shape the weights?
- **Parity Check**: Is every candidate described at equal depth (no false equivalence, no inflated padding)?
- **Sensitivity**: Which criterion, if its weight changed by ±1, flips the recommendation? Stated explicitly?
- **Source Fidelity**: Does each cost/risk figure trace to a source or an explicit assumption?
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.

### 7. Human Gate
Present: 四维度证据摘要, §多方案取舍 矩阵（若适用）, sensitivity analysis, AI recommendation with confidence and key assumptions, audit result.
**Only the decision-owner may approve.** The human's choice is recorded as a `DecisionRecord` (DEC-XXX) with chosen option, rationale, date, and decision-maker. Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- If the decision changes scope → reflow to the earliest affected Work Item; never silently update scope.
- On changes to a confirmed artifact: record delta → update affected sections → re-run Audit → return to Human Gate.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| 评估没有具体方案对象的"可行性"（"我们想做邀请系统——可行"） | Require a concrete product-level solution before assessment |
| AI 替业务方做最终决定（"分析清楚表明…"） | AI 推荐并给置信度；人拍板 |
| 打分后才定权重 | 权重先于打分定义，防锚定 |
| 给偏爱的方案更多篇幅 | 每个候选等深描述 |
| 把明显劣质的选项包装成可比 | 如实呈现差距，让矩阵暴露差距 |
| 推荐不带置信度 | Always state: HIGH/MEDIUM/LOW confidence + key assumptions |
| 跳过敏感度分析 | Identify which assumption change flips the recommendation |
| 成本/风险估算当事实写死 | 标 `AI_INFERENCE`/`ASSUMPTION` + 责任人 + SRC-* |
| 只有单个方案也硬凑对比 | 单一方案时只做四维度可行性，不加 §多方案取舍 章节 |
| 把实现细节当产品方案评估 | Route detail-level choices to engineering |

## Example: Sufficient Input → Sufficient Output

**Input**: Concrete product solution exists (`function-description`), cost/constraint inputs registered, decision owner named. Decision: build vs buy an order-notification module (feasibility with a multi-solution tradeoff).
**Output**: Full `feasibility-report.md` — 市场空间（目标用户量 100 万，可比渗透率 30%，理论空间）→ 技术可行性（微信模板消息已验证兼容）→ 投入产出（自研 2 人×4 周 ≈ ¥X vs 外采年费 ¥Y，回本周期）→ 风险评估（供应商锁定：高/中 → 应对：退出条款）→ §多方案取舍（权重在打分前定义：业务匹配 5、用户影响 4、成本 4、时间 3、技术风险 3、可逆性 2；自研 86 vs 外采 65；AI 推荐 自研，MEDIUM 置信度；敏感度：时间权重 3→5 翻转）→ 结论：有条件做（自研，条件：2 周内确认技术栈）; 人工决策记录 DEC-001 → status `ready_for_human_review`.

## Example: Sparse Input → Degraded Output

**Input**: Slack message "帮我评估一下自研还是外采这个功能".
**Output**: Preflight finds no concrete product-level solution and no decision owner → Intake registers SRC-001 → Think identifies missing: which solution options? which criteria? who decides? what's the cost data? → Clarify generates 3 questions (solution candidates, decision owner, decision date/scope) → stops at `needs_user_input`.

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/thinking-framework.md` | 思考透镜（Common Core + 可行性领域 lens，必读） | 每次任务开始（必读） |
| `references/feasibility.md` | 可行性四维度主线模式细节 | 主线评估时 |
| `references/multi-solution.md` | §多方案取舍 章节细节（加权矩阵 + 决策记录） | 存在 ≥2 实质方案时 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/anti-patterns.md` | AI 常见反模式（可行性分析特有，写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |

## Completion

All four dimensions (市场空间 / 技术可行性 / 投入产出 / 风险评估) are analyzed with evidence; when ≥2 materially different solutions exist, the §多方案取舍 chapter documents each at equal depth with weighted criteria defined before scoring; sensitivity analysis identifies which assumption change could flip the recommendation; the conclusion is a clear 做 / 不做 / 有条件做 with specific measurable conditions; the AI recommendation carries explicit confidence; and the human decision-maker's choice is recorded as a `DecisionRecord`. If the decision changes scope, the earliest affected Work Item is reflowed.
