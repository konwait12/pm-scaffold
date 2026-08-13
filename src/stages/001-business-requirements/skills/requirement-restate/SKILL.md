---
name: requirement-restate
description: Restate original requirements in the stakeholder's own words back to them as a structured list, before any design or PRD writing — to verify shared understanding and surface hidden assumptions. Use when stakeholder language is ambiguous, when multiple sources use different terms for the same thing, or when a "do we really agree on what you asked for?" checkpoint is required.
---

# Requirement Restate

## Purpose And Boundary

Restate the original requirement(s) in the **stakeholder's own words**, structured as a verifiable list, **before** any design, journey, or PRD work begins. The output `requirement-restate.md` is a **shared-understanding checkpoint**: the stakeholder reads the restatement and confirms "yes, that is what I meant" or "no, you missed X / misread Y". The diff between "what they said" and "what we restated" is the value — it surfaces hidden assumptions early, when fixing them is cheap.

**Do not** propose solutions, define journeys, write user stories, or design fields. This Skill only **restates** what was asked. Solutions come in later Skills. Do not resolve conflicts here — flag them and route to issue-record.

**PRD 归宿**：❌ **默认不进 PRD**。requirement-restate 是分析过程（Analysis Process），不是 PRD 产物。Stakeholder 确认通过后：重举通过的需求行进入 `project-background-goal` 和 `user-journey-and-stories` 草案；冲突（CONFLICT）进入 `issue-record` 的 ISS-XXX（CLS 类别）；未知（UNKNOWN）进入 `issue-record` 的 Q-XXX（INF 类别）。`requirement-restate.md` 本身永远不进入 prd.md 正文。

**本 Skill 属于 Branch**（参见 `src/framework/governance.md` §Human-In-The-Loop Inquiry Contract）。`prd-assembly` 进入 §0 上游清单时会**主动询问**"要不要在 §0 标注 requirement-restate 来源链"——若 stakeholder 显式要求可追溯到 restate，则 §0 加一行 RR-XXX 摘要；否则不出现。触发条件：原始需求被多团队/多语言/多源转述、多源术语不一致、误读代价高（合规/法律/昂贵构建）、需要正式的"我们真的同意了吗"检查位、新 stakeholder 加入需重新锚定。

## Inputs And Outputs

Inputs:
- Original source materials (meeting minutes, emails, BRD, audio/video transcripts, chat, tickets)
- Background artifact (`background-goal.md`, if available)
- Scope artifact (`project-scope.md`, if available)
- The full chain of prior conversation (chat, ticket, ticket comments)

Output: `requirement-restate.md` with §1-§9 sections, using the template `assets/requirement-restate-template.md`, including a list of restated requirements (RR-NNN), each tagged with its source and the original phrasing.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses + 领域 lens) before analysis. Load `references/output-contract.md` before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Load `references/source-handling.md` during Intake when登记 SRC-*。Run `scripts/validate_artifact.py <artifact> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "What did the stakeholder actually say, in their own words?"
- "Which sources are we restating from? Are there audio / video / chat that have not been transcribed?"
- Identify: project name, project ID (REQ-XXX), stakeholder(s), sources. Register each source with an SRC-ID.
- **If no source exists and the ask is only a paraphrase from memory**, return a routing receipt and STOP.
- Assess maturity: L0（无源）→ L1（单条口头表述）→ L2（单源书面）→ L3（多源一致）→ L4（多源冲突，需消歧）。

### 2. Intake
- "What did each source literally say — not what I think it means?"
- 逐源提取候选需求，verbatim 保留原始措辞（方言、口语、术语照抄）。跨源合并重复项（同一诉求、不同措辞）并注明。
- 矛盾标记为 `CONFLICT` —— **不解决，只标记**。
- 每条标知识状态：`FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`。登记 SRC-*。

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "剥离所有提议方案后，这个诉求本身是什么？"
- **Systems Thinking**: "这个诉求是否隐含了一个也在推进中的上游/下游系统？"
- **Role Perspective**: "stakeholder 能否在重述里认出他们自己的话？"
- **Constraint Analysis**: "stakeholder 在诉求里嵌入的约束，我们是否不能静默移除？"
- **Adversarial**: "最糟糕的误读方式是什么？重述是否防御了这种误读？"
- **Reverse Validation**: "如果 stakeholder 只读重述，他们看到的正是他们想说的吗？"

### 4. Clarify
- 每个 `CONFLICT`：列出双方措辞，路由给 stakeholder 选择（含 AI 初判 + 选项 + 影响 + owner）。
- 每个 `UNKNOWN`：请 stakeholder 补全。Batch questions：≤5 per session，按影响排序。
- **Stop at `needs_user_input`** when a conflict or unknown changes the ask itself.

### 5. Generate
- 填模板。每条重述需求：ID（`RR-NNN`）、重述（stakeholder 的话）、原始措辞（verbatim）、来源、知识状态、提出方、confidence。
- 发现"方案泄露"（重述夹带方案）→ 标 `solution_leak`，需 stakeholder 重新确认。
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Source Coverage**: 每条 Intake 登记的 SRC-ID 都反映在重述清单中。
- **Atomicity**: 没有一行塞两个诉求。
- **No Solution Leak**: 没有一行含方案/技术/设计。
- **Conflict Visibility**: 所有冲突被标记，未被解决。
- **Stakeholder Recognition**: 重述可原样发回给 stakeholder 且读起来忠实。
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.

### 7. Human Gate
Present: 重述条数、冲突条数、未知条数、来源覆盖、audit 结果。
**The original stakeholder (or their named delegate) must confirm the restatement.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → re-Audit → re-validate → return to Human Gate.
- 这里浮现的冲突必须升级到 `issue-record.md` 解决，不在 restate 内解决。

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| 用自己的话重述诉求 | 用 stakeholder 的话；能引用就引用原文 |
| 隐藏来源（"业务方说要…"） | 始终引用 SRC-ID，具体到段落/时间戳 |
| 加一层"我们猜他们意思是…" | 要么重述要么提问，不发明第三个版本 |
| 在重述阶段解决冲突 | 标 `CONFLICT` 并路由到 issue-record |
| 夹带方案（"这应该是个移动端 app"） | 剥离方案；方案属于 journey / function-description |
| 把相关诉求合并成一行 | 一行一个诉求，没有例外 |
| 把 AI 推断当 stakeholder 原话 | 重述只含来源支持的内容，推断标 AI_INFERENCE |

## Example: Sufficient Input → Sufficient Output

**Input**: 3 sources — a meeting transcript, a follow-up email, and a ticket comment — all describing the same ask.
**Output**: 完整 requirement-restate.md——
- 7 条重述需求（RR-001…RR-007），每条链接到来源。
- 1 个 CONFLICT：会议说"所有角色"，邮件说"仅经理" → 路由给 stakeholder 选择。
- 2 个 UNKNOWN：deadline 未指定、成功指标未指定 → 路由给 stakeholder 补全。
- 0 个方案：尽管会议提到"dashboard"，重述仅记为 hint，不当作决议。

## Example: Sparse Input → Degraded Output

**Input**: Chat message "make it faster for our VIPs"（无附件、无来源）.
**Output**: Preflight 判定 L1（单条口头表述，无源）→ 不进入 Generate/Audit → Clarify 批量产出：这是指哪个流程更快？VIP 的定义？"更快"的成功判据？当前耗时基线？——每条带 AI 初判 + 选项 + 影响 + owner → status = `needs_user_input`，等待补充来源或澄清后再进入充分模式。

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见重述反模式（写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约（RR-NNN） | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |

## Completion

每条来源里的诉求都用 stakeholder 的话重述；每行都有来源绑定与原始措辞；冲突全部标记并路由到 issue-record；未知全部路由给 stakeholder；原 stakeholder（或其指定代理）确认"是的，这就是我说的"；项目可进入 scope / journey / PRD 工作。
