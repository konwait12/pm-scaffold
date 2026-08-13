---
name: competitive-research
description: Conduct competitive analysis when business solution is unclear and reference is lacking. Use structured frameworks (feature matrix, positioning map, SWOT) to inform product decisions. All findings are AI_INFERENCE until human-confirmed.
---

# Competitive Research

## Purpose And Boundary

When the product direction lacks reference — "what do competitors do?", "is there a market standard?", "how do we differentiate?" — this skill systematically analyzes competitors and synthesizes actionable insights for product decisions. Output is the `competitive-analysis.md` artifact consumed by `user-journey-and-stories`, `product-ux`, or `function-description`.

**Do not** copy competitor features without understanding their context, present findings as confirmed facts, replace user-journey or product-ux work, or conclude "we should do what competitor X does" without differentiation analysis. A competitor's success in their market does not transfer to ours without evidence.

## Inputs And Outputs

Inputs: a confirmed business baseline (`background-goal.md` with confirmed goals) or scope baseline, a research goal (business-level vs functional-level), and registered competitor sources (official sites, app-store pages, user reviews, public docs, industry reports). If no confirmed background or research goal exists, stop at `needs_user_input` — do not research in a vacuum.

Output: `competitive-analysis.md` using the template at `src/templates/support/competitive-analysis.md`.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses) before analysis. Load `references/source-handling.md` at Intake. Load `references/question-patterns.md` at Clarify. Load `references/output-contract.md` before drafting. Load `references/anti-patterns.md` at Generate. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <artifact> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "What decision does this research inform? Is the research goal business-level (solution direction) or functional-level (feature design)?"
- "Which competitors should be studied — direct (same category), indirect (same need, different solution), or aspirational (best-in-class elsewhere)?"
- Register every competitor source with an SRC-ID. Identify research_owner and decision_owner.
- **If no confirmed background-goal or research goal exists**, return a routing receipt and STOP at `needs_user_input`.
- Limit to 3-5 competitors. Assess maturity: L0 (no direction) → L1 (single vague question) → L2 (business direction clear) → L3 (scope defined) → L4 (confirmed upstream).

### 2. Intake
- "What does each source actually say about the competitor — not what I assume about their product?"
- Extract competitor statements verbatim (feature set, pricing, target user, positioning). Classify each as `FACT`, `AI_INFERENCE`, `UNKNOWN`, or `CONFLICT` per `src/framework/contracts.md`.
- Retain SRC-IDs and locations. Do not merge two competitors' claims into one row.

### 3. Think (apply thinking-core.md §1 mandatory lenses + competitive domain lenses)
- **First Principles**: "What user need does each feature actually serve? Would our confirmed goal survive if competitor X were removed as a reference?"
- **Systems Thinking**: "Which segments, user flows, and downstream decisions does this research affect?"
- **Adversarial**: "Could the opposite of my hypothesis be true — is competitor X actually not the benchmark? Is the evidence from one interested party only?"
- **Reverse Validation**: "From our desired differentiation backwards, what must competitors be failing at?"
- Domain lenses: Positioning Mapping, Differentiation Scan, Pattern Extraction, Inference Discipline (see `references/thinking-framework.md`).

### 4. Clarify
- Research discoverable facts first (official sites, app reviews, public reports).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when the answer changes competitor selection, comparison dimensions, or a material conclusion.
- Limit: ≤5 questions per session. Order by impact.

### 5. Generate
- Fill the template: §1 竞品列表 → §2 逐品分析 → §3 横向对比 → §4 结论 ("So What").
- Every insight maps to OUR goal (goal ID). All findings tagged `AI_INFERENCE`.
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Completeness**: All selected competitors covered? All material claims sourced? "So What" present?
- **Confirmation Bias**: Did I actively search for disconfirming evidence, or only cherry-pick?
- **Source Fidelity**: Does each claim trace to an SRC-ID? `FACT` vs `AI_INFERENCE` distinct?
- **Downstream Usability**: Can user-journey-and-stories / product-ux pick this up without re-researching?
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.

### 7. Human Gate
Present: competitor selection rationale (direct/indirect/aspirational), applied framework analysis, cross-competitor patterns and divergences, "So What" synthesis, audit result.
**Only the business owner may confirm applicability.** All findings remain `AI_INFERENCE` until then. Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes to a confirmed background-goal: record delta → update affected sections → re-run Audit → return to Human Gate.
- Later contradiction (a competitor changed direction or a new competitor appeared) → re-enter this Skill from Preflight, not patched downstream.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| "Competitor X does it, so we should too" | Understand WHY they do it — same user need? same context? map to our goal |
| List 20 competitors with one-line descriptions | Limit to 3-5 with deep analysis |
| Skip the "So What" synthesis | Every competitive research must answer: what do WE do with this information? |
| Present findings as facts | Tag everything `AI_INFERENCE` until human confirms |
| Only look at direct competitors | Include indirect (different solution, same need) and aspirational (best UX) |
| Judge a feature without knowing its goal | Score every feature against OUR confirmed goal ID, not in a vacuum |
| Treat a stale source as current | Record retrieval date; re-verify competitor facts before reuse |

## Example: Sufficient Input → Sufficient Output

**Input**: Confirmed `background-goal.md` (goal G1: shorten customer onboarding), business-level research goal, 3 competitor sources registered with SRC-IDs (two direct, one indirect).
**Output**: Full template — 竞品列表 with selection rationale, 逐品分析 via Positioning Map + Feature Matrix, 横向对比 identifying one market-standard pattern and one gap, 结论 "So What" mapping each insight to G1 with `AI_INFERENCE` tags → status `ready_for_human_review`.

## Example: Sparse Input → Degraded Output

**Input**: Slack message "看看竞品怎么做会员等级的".
**Output**: Preflight finds no confirmed background-goal and no research goal → Intake registers the message as SRC-001 → Think identifies missing: which competitors? which level (business vs functional)? which dimensions matter? → Clarify generates 3 questions (research goal, competitor candidate list, decision this informs) → stops at `needs_user_input`.

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（竞品分析特有，写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 竞品领域 lens，必读） | 每次任务开始（必读） |

## Completion

Competitors are selected with rationale (direct/indirect/aspirational) and limited to 3-5; at least one framework is applied and analyzed; cross-competitor patterns and divergences are identified; every insight maps back to a confirmed goal; "So What" synthesis provides actionable, specific recommendations; all findings carry explicit knowledge state (`AI_INFERENCE` until confirmed); and the business owner confirms or revises insights.
