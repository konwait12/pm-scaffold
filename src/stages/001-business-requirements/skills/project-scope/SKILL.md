---
name: project-scope
description: Standalone project scope definition — explicitly enumerate In-Scope, Out-of-Scope, Deferred, and Conditional-Scope items with clear acceptance criteria and traceability. Use when the project boundary is ambiguous, when business needs to confirm "what we are NOT doing", or when scope creep is a risk.
---

# Project Scope

## Purpose And Boundary

Produce a standalone `project-scope.md` that turns every stakeholder expectation into one of four explicit scope categories — **In**（本期做）、**Out**（本期不做）、**Deferred**（暂缓做）、**Conditional**（条件成立则做）——each backed by a verifiable acceptance criterion, a knowledge-state label, and a source or decision. The artifact locks the boundary before journey / UX / feature work begins so downstream phases do not re-litigate "what is in this project". It is **standalone**: it does not depend on the background-goal artifact, but can reference it.

**Do not** define requirements, design solutions, write user stories, or draft PRD sections. Scope is about **what is and is not part of this project**, not **how to build it**. Do not silently resolve contested items yourself — contested boundaries are exactly what the decision owner must rule on.

**PRD 归宿**：✅ **按需**。当 `prd-assembly` 进入 §5 按需章节时，AI 必须主动询问"要不要把 project-scope 的 In/Out/Deferred/Conditional 列表聚合为 §5.1 项目范围基线"。若业务方回答"要"，则 §3-§6 内容 verbatim 进入 prd.md；若回答"不要"，则 prd.md 不出现范围章节，project-scope.md 作为过程证据存档于 `99-review/support/`。

**本 Skill 属于 Branch**（参见 `src/framework/governance.md` §Human-In-The-Loop Inquiry Contract）。Trunk 内容（background / journey / UX / functions）永不询问；Branch（项目范围基线）必须询问。触发条件：项目边界不清 / 多团队范围重叠 / 需要"明确不做什么"的书面承诺 / 历史出现过 scope creep / 签约、预算或资源决策前需要正式范围文件。

## Inputs And Outputs

Inputs:
- Background artifact (`background-goal.md`, if available)
- Original source materials (meeting minutes, emails, BRD)
- Stakeholder intent (what business hopes to achieve)
- Known constraints (timeline, budget, technology, team)

Output: `project-scope.md` with §1-§9 sections, using the template `assets/project-scope-template.md`, including explicit In/Out/Deferred/Conditional lists.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses + 领域 lens) before analysis. Load `references/output-contract.md` before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Load `references/source-handling.md` during Intake when登记 SRC-*。Run `scripts/validate_artifact.py <artifact> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "Who is asking for scope clarity, and why now? What problem does this project actually solve?"
- "Which candidate items exist before classification? Who are the decision owners for contested boundaries?"
- Register every source with an SRC-ID. Identify goal_decision_owner and business_sponsor.
- **If no usable source and no stakeholder intent exists**, return a routing receipt and STOP — do not proceed to Intake.
- Assess maturity: L0（无范围信息）→ L1（单条稀疏表述）→ L2（已有部分分类）→ L3（候选范围完整）→ L4（可锁定 confirmed）。

### 2. Intake
- "For each candidate item — is it In, Out, Deferred, or Conditional? What evidence or decision drives that classification?"
- 逐条提取候选范围项，不得把干系人期望静默合并或丢弃。
- 每条标知识状态：`FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`。
- Register sources with SRC-IDs. Do not merge different sources' claims into one item.

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "达到核心目标的最小范围是什么？哪些项只是伪装成范围的实现手段？"
- **Systems Thinking**: "哪些上游/下游系统、角色、数据受影响？我们处在其范围内还是范围外？"
- **Role Perspective**: "对每个角色——他期待哪些在范围内、哪些不在？"
- **Constraint Analysis**: "哪些硬约束（时间/团队/技术/合规）强制把项排除出范围？"
- **Adversarial**: "干系人能否合理地声称该项在范围内？什么证据能证明它不在？"
- **Reverse Validation**: "从项目成功判据反推——哪些必须在本期范围内才可能成功？"

### 4. Clarify
- 边界模糊的项：把选项、AI 初判、证据、影响、owner、blocking 批量提问（≤5 per session，按影响排序）。
- 先做可发现事实的检索（公开范围口径、既有协议、历史迭代范围），再问人。
- **Stop at `needs_user_input`** when ambiguity can change the deliverable, timeline, cost, or who approves.
- 争议项必须路由到决策者，AI 不得选边。

### 5. Generate
- 填模板。每个范围项必须有：ID（`S-NNN`）、描述、知识状态、来源/决议、验收依据（In 项必填）、干系人、备注。
- Out/Deferred 项必须写"不做/暂缓的原因"（约束 / 决议 / 未来工作）。
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Coverage**: 每条干系人期望都被分到 In / Out / Deferred / Conditional 之一（不得缺失）。
- **Source Fidelity**: 每条 In/Out 决定都可追溯到 SRC-* 或具名 DECISION。
- **Mutual Exclusivity**: 一项不得同时 In 且 Out；不得同时 In 且 Deferred。
- **Acceptance**: 每个 In 项都有可验证验收依据；Out/Deferred 项都有原因。
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.

### 7. Human Gate
Present: 范围总览（In/Out/Deferred/Conditional 计数）、争议项、来源覆盖、audit 结果、待决清单。
**Only the goal decision owner / business sponsor may approve.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → re-Audit → re-validate → return to Human Gate.
- 后续阶段出现的范围冲突 → 本 Skill 从头重跑，不在下游打补丁。

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| 因为省事把所有项都写进 In | 强制每个候选项说明为何 In/Out/Deferred |
| 写"提升体验"这类模糊 In 项 | 每个 In 项有可衡量验收依据 |
| 把 Out 项当"垃圾"静默丢弃 | 带原因记录 Out 项（约束/决议/未来） |
| 跳过 Conditional 清单 | Conditional 项（如"预算通过则…"）是真实范围，要列出 |
| 让干系人拖到设计阶段才吵范围 | 在 journey/UX/功能工作前锁定范围 |
| 自己替决策者裁决争议项 | 争议项显式列出，交决策者裁决 |
| 把范围写成项目目标 | 范围是实现目标的手段，先有目标后有范围 |

## Example: Sufficient Input → Sufficient Output

**Input**: 5-stakeholder meeting about migrating from on-prem CRM to SaaS + BRD + timeline constraint（Q4 前完成）.
**Output**: 完整 project-scope.md——
- In（7 项）：3 个核心实体数据迁移、SSO、基础报表、角色映射、审计日志、培训材料、30 天并行运行。
- Out（5 项）：自定义工作流引擎（用厂商内置）、移动端（Phase 2）、>5 年历史数据（归档）、AI 功能（Deferred）、超 2 家厂商的三方集成（Deferred）。
- Deferred（3 项）：高级分析、自定义 dashboard、非 IdP 的 SSO。
- Conditional（2 项）："预算通过则加 Salesforce 同步" / "法务签字则放开跨境数据"。
每条均带 SRC-*/DEC-* 来源与验收依据，争议项已交决策者裁决。

## Example: Sparse Input → Degraded Output

**Input**: Slack message "we need an event invitation system for VIP customers."
**Output**: Preflight returns L1（单条稀疏源）→ Intake 登记 SRC → Think 识别缺失：范围候选项、当前系统、排期、预算、成功判据 → 不进入 Generate/Audit → Clarify 批量产出 3 个问题（含 AI 初判 + 选项 + 影响 + owner）→ status = `needs_user_input`，等人工补齐后按充分模式重新进入。

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见范围反模式（写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约（S-NNN） | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |

## Completion

每条干系人期望都被分类为 In / Out / Deferred / Conditional 之一；每个 In 项有可验证验收依据；每个 Out/Deferred 项有"不做/暂缓"的原因；争议项已交决策者裁决；goal_decision_owner / business_sponsor 显式批准边界；范围已锁定，可进入 journey/UX 工作。
