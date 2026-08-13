---
name: solution-assessment
description: Compare materially different product solutions and assess feasibility using weighted decision matrix when scope, cost, compliance, dependencies, or risk require a human choice.
---

# Solution Assessment

## Purpose And Boundary

When a product decision has ≥2 materially different solutions (build vs. buy, different technical approaches, different scope tradeoffs) or when feasibility (market/technical/cost/risk) is in question, this skill frames the assessment objectively, applies weighted criteria, and presents a recommendation with confidence — but **never makes the final decision**. The human decision-maker owns the choice.

**Do not** make the final decision, silently update scope, design architecture, or assess solutions that differ only in implementation detail (those belong to engineering, not product). Feasibility assessment requires a concrete product-level solution to already exist — you cannot assess "can we build X" until X is concrete.

## Inputs And Outputs

Inputs: a concrete product-level solution (from `product-ux` or `function-description`) or an explicit feasibility/multi-solution decision request, upstream evidence (background-goal, cost/constraint/compliance inputs), and a named decision-owner. If the decision would change confirmed scope, cost, compliance, or risk posture, stop at `needs_user_input` until the decision owner is identified.

Output: `feasibility-report.md` using the template at `src/templates/support/feasibility-report.md` (Go/No-Go/Conditional-Go), or `solution-comparison.md` using the template at `src/templates/support/solution-comparison.md` (multi-solution weighted comparison).

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses) before analysis. Load `references/source-handling.md` at Intake. Load `references/question-patterns.md` at Clarify. Load `references/output-contract.md` before drafting. Load `references/anti-patterns.md` at Generate. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <artifact> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "Is there a material choice to assess? Are there ≥2 genuinely different solutions with different cost/risk/scope profiles, or an explicit feasibility question?"
- "Which mode applies: feasibility (market/technical/cost/risk → Go/No-Go) or solution comparison (weighted matrix → recommendation)?"
- "If solutions differ only in implementation detail, route to engineering, not product."
- Identify decision_owner. **If no decision owner exists, return a routing receipt and STOP at `needs_user_input`.**
- Assess maturity: L0 (no concrete solution) → L1 (vague idea) → L2 (product-level solution exists) → L3 (cost/constraint data present) → L4 (confirmed upstream).

### 2. Intake
- "What does each source actually say about cost, constraints, compliance, dependencies, and risk — not what I assume?"
- For each candidate solution: approach summary, technical dependencies, resource estimate (people + time), key risks, reversibility.
- Classify knowledge states per `src/framework/contracts.md`: FACT / DECISION / ASSUMPTION / AI_INFERENCE / UNKNOWN / CONFLICT. Retain SRC-IDs.

### 3. Think (apply thinking-core.md §1 mandatory lenses + assessment domain lenses)
- **First Principles**: "What is the observable decision to make? Which costs and risks are assumptions disguised as requirements?"
- **Systems Thinking**: "Which upstream/downstream work items, roles, and dependencies does each solution affect?"
- **Adversarial**: "Could the recommended solution be a trap? Is the evidence one-sided? Is urgency asserted without a real deadline?"
- **Reverse Validation**: "From the preferred outcome backwards, what must be true for each solution to succeed?"
- Domain lenses (see `references/thinking-framework.md`): Occam's Razor (fewest dependencies when both solutions meet the goal), Opportunity Cost (what we give up by choosing), Reversibility (can we undo a wrong choice?).

### 4. Clarify
- Research discoverable facts first (cost benchmarks, public pricing, past project data).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when an answer changes the recommendation, a criterion weight, or a material cost/risk figure.
- Limit: ≤5 questions per session. Order by impact.

### 5. Generate
- **Feasibility mode**: 市场空间 → 技术可行性 → 投入产出 → 风险评估 → 结论 (做/不做/有条件做 with conditions).
- **Comparison mode**: 候选方案 (equal depth each) → 方案对比矩阵 (criteria defined BEFORE scoring) → AI 推荐 (with HIGH/MEDIUM/LOW confidence) → 人工决策.
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Anchoring Check**: Were criteria defined before scores, or did the winning solution shape the weights?
- **Parity Check**: Is every solution described at equal depth (no false equivalence, no inflated padding)?
- **Sensitivity**: Which criterion, if its weight changed by ±1, flips the recommendation? Stated explicitly?
- **Source Fidelity**: Does each cost/risk figure trace to a source or an explicit assumption?
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.

### 7. Human Gate
Present: candidate summary, weighted matrix / feasibility dimensions, sensitivity analysis, AI recommendation with confidence and key assumptions, audit result.
**Only the decision-owner may approve.** The human's choice is recorded as a `DecisionRecord` (DEC-XXX) with chosen option, rationale, date, and decision-maker. Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- If the decision changes scope → reflow to the earliest affected Work Item; never silently update scope.
- On changes to a confirmed artifact: record delta → update affected sections → re-run Audit → return to Human Gate.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Define criteria after seeing which solution wins | Define criteria first, score second — prevents anchoring |
| Give favored solution more depth than alternatives | Every solution gets equal-depth description |
| Recommend without confidence level | Always state: HIGH/MEDIUM/LOW confidence + key assumptions |
| AI makes the decision ("The analysis clearly shows...") | AI recommends; human decides |
| Treat a vague idea as assessable ("we want an invitation system — yes it's feasible") | Require a concrete product-level solution before assessment |
| Pad a clearly inferior option to look comparable | Surface real tradeoffs; let the matrix show the gap |
| Skip sensitivity analysis | Identify which assumption change flips the recommendation |
| Assess implementation details as product solutions | Route detail-level choices to engineering |

## Example: Sufficient Input → Sufficient Output

**Input**: Concrete product solution exists (`function-description`), cost/constraint inputs registered, decision owner named. Decision: build vs buy an order-notification module.
**Output**: Full `solution-comparison.md` — criteria (business fit 5, user impact 4, cost 4, time 3, tech risk 3, reversibility 2) defined before scoring; both options at equal depth; weighted totals 86 (自研) vs 65 (外采); AI 推荐 自研 with MEDIUM confidence; sensitivity: time weight 3→5 flips to 外采; human decision recorded as DEC-001 → status `ready_for_human_review`.

## Example: Sparse Input → Degraded Output

**Input**: Slack message "帮我评估一下自研还是外采这个功能".
**Output**: Preflight finds no concrete product-level solution and no decision owner → Intake registers SRC-001 → Think identifies missing: which solution options? which criteria? who decides? what's the cost data? → Clarify generates 3 questions (solution candidates, decision owner, decision date/scope) → stops at `needs_user_input`.

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（方案评估特有，写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/feasibility.md` | 可行性分析模式细节（四维度 + 触发条件） | 可行性模式时 |
| `references/multi-solution.md` | 多方案对比模式细节（等深描述 + 决策记录） | 多方案模式时 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 方案评估领域 lens，必读） | 每次任务开始（必读） |

## Completion

All materially different solutions are documented with equal depth (or the feasibility question is answered across market/technical/cost/risk); weighted criteria are defined before scoring; sensitivity analysis identifies which assumption changes could flip the recommendation; AI recommendation carries explicit confidence; and the human decision-maker's choice is recorded as a `DecisionRecord`. If the decision changes scope, the earliest affected Work Item is reflowed.
