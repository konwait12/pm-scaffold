---
name: issue-record
description: 跨阶段共享的问题清单 — 集中登记 BLK / RSK / DEC / INF / CLS / OUT 六类问题；任何阶段遇到需求不明确时 AI 主动询问是否登记。任何 Skill 都可以登记 / 引用 / 升级问题。
---

# Issue Record（跨阶段共享）

## Purpose And Boundary

维护一个**项目级**（不是阶段级）的问题清单 `issue-record.md`。每个问题有：类别、状态、Owner、知识状态、来源、目标关闭日期。任何阶段的任何 Skill 在 Clarify 阶段遇到**阻断（BLK）**、**风险（RSK）**、**待决（DEC）**、**信息缺口（INF）**、**歧义（CLS）**、**范围外（OUT）**时，可以登记到本清单；问题被阶段产物确认后才能关闭。它给业务方一个权威的"还有什么没解决"清单，也是 PRD 确认前必经的"问题清零"环节。

**Do not** 在 Issue Record 中写需求、设计方案、用户故事或 PRD 章节。Issue Record 只列"卡点 / 风险 / 待决"，方案交给后续 Skill。不要替决策者接受风险（`accepted` 状态只能由决策 Owner 设置）。

**AI 行为硬约束**：当用户输入或源材料出现"待确认 / 不明确 / 没说过 / 模糊 / 矛盾"等信号时，AI 必须在给出方案之前**主动询问**"是否登记为 Issue Record 问题"——而不是默默继续。

**PRD 归宿**：❌ **默认不进 PRD**。issue-record 是过程记录（Process Record），不是 PRD 产物。但 AI 在 `prd-assembly` 进入 §9 / §10 时**主动询问**业务方"要不要把 issue-record 的'未关闭问题摘要'或'已接受风险列表'暴露为 §9 未决风险摘要"——若业务方要求可见性则引用摘要，否则不出现。这是 **Human-in-the-Loop 配置**，问题清单本身永远不进入 PRD。

**本 Skill 属于 Branch**（参见 `src/framework/governance.md` §Human-In-The-Loop Inquiry Contract），跨阶段共享（001 / 002 / 003 均可触发）。触发条件：任何阶段的"待确认"信号、来源冲突、待决决策、风险、口头未签字、推导与 FACT 冲突、阶段产物遗留 UNKNOWN。

## Inputs And Outputs

Inputs:
- 任何阶段的产物（background-goal / journey / UX / function-description / PRD）中的"待确认" / UNKNOWN / CONFLICT 标记
- 任何阶段的 Clarify 会话中识别的新问题
- 业务方 / PM / 干系人主动提出的问题

Output: `issue-record.md`（项目级过程记录，`99-review/support/` 下，跨阶段共享），用模板 `assets/issue-record-template.md`（§1-§12），含按类别（BLK/RSK/DEC/INF/CLS/OUT）与状态分组的表。

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses + 领域 lens) before analysis. Load `references/output-contract.md` before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Load `references/source-handling.md` during Intake when登记 SRC-*。Run `scripts/validate_artifact.py <artifact> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "Which artifacts exist so far? Which '待确认' / UNKNOWN / CONFLICT markers should be promoted to ISS-NNN?"
- "Who owns each category of issue (decision owner, risk owner, fact owner)?"
- Register the upstream artifact references. Identify goal_decision_owner and the PRD 确认前"问题清零"责任人。
- **If no issue signal exists anywhere, return a routing receipt ("no new issues, list may be empty") and STOP** — do not invent issues.

### 2. Intake
- "Is this BLK, RSK, DEC, INF, CLS, or OUT? Which artifact does it come from? Who should own it?"
- 逐条提取问题信号（待确认 / 冲突 / 待决 / 风险 / 信息缺口 / 范围外），登记来源（上游产物 + SRC-*）。
- 标知识状态：`FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`。
- 查重：是否已在某阶段产物或本清单登记过（避免重复）。

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "这个问题是真的阻断，还是换个路径就能绕开？剥离方案后问题还存在吗？"
- **Systems Thinking**: "这个问题影响哪些下游 Work Item？不清零会导致哪些产物作废？"
- **Role Perspective**: "对每个可能的 owner——他有权解决这个问题吗？他需要什么才能解决？"
- **Constraint Analysis**: "哪些是硬约束（合规/法律/平台）导致的 blocker，无法用方案绕开？"
- **Adversarial**: "如果把这个问题当作非阻塞，最坏会发生什么？证据支持降级吗？"
- **Reverse Validation**: "从 PRD 确认反推——哪些问题必须在确认前清零，哪些可以带风险接受？"

### 4. Clarify
- 类别归属、owner、是否阻断不明确时：批量提问（≤5 per session），带 AI 初判 + 选项 + 影响 + owner。
- 触发"AI 主动询问契约"：先问"要不要登记为 ISS-NNN"，再继续生成。
- **Stop at `needs_user_input`** when an answer changes the issue's category, owner, or blocking status.

### 5. Generate
- 填模板。每个问题：ID（`ISS-NNN`）、category、state、title、description、owner、knowledge_state、source、affected_artifact、raised_at；BLK/DEC 加 target_close，RSK 加 mitigation，resolved 加 resolution，escalated 加 escalated_to。
- 登记必须先经用户确认（AI 主动询问）。
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Completeness**: 上游产物每个"待确认"都有 ISS-NNN 引用或 documented 关闭理由。
- **Ownership**: 每个 open 问题都有 owner。
- **Dating**: 每个 BLK / DEC 都有 target_close；30 天以上 open 有 escalation 记录。
- **State Integrity**: `accepted` 只能由决策者设；`resolved` 链接到关闭它的产物变更。
- **AI 询问合规**: 每个登记都先经用户确认，无"未询问即继续"。
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.

### 7. Human Gate
Present: 按类别与状态计数、critical top5、待决清单、accepted 风险、audit 结果。
**Only the goal decision owner / business sponsor may approve the closed-out list.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → re-Audit → re-validate → return to Human Gate.
- 跨阶段回流时，残留问题决定回流路径；问题被解决后链接到关闭它的产物变更。

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| 在 Issue Record 中写"应该如何设计" | 只列问题，方案交给后续 Skill |
| AI 主动替业务方决定接受风险 | `accepted` 状态只能由决策者设 |
| 默默忽略"待确认"信号 | 主动询问是否登记 |
| 让问题散落在 6 个产物中 | 集中维护一份问题清单 |
| 把问题清单当作需求清单 | Issue Record 是"未决"，不是"要做" |
| AI 自己发明不存在的问题 | 无信号就不登记，返回路由收据 |
| 让问题长期无 owner / 无 deadline | 每个 open 有 owner；BLK/DEC 有 target_close |

## Example: Sufficient Input → Sufficient Output

**Input**: 全流程产物：background-goal 遗留 2 个 UNKNOWN、project-scope 有 1 个边界争议、function-description 发现 1 个合规风险、prd-assembly 发现 1 个待决上线范围.
**Output**: 完整 issue-record.md——
- BLK-001（ISS-001）：上线范围待决，owner=业务负责人，target_close=本周五。
- RSK-101（ISS-002）：合规风险（跨境数据），mitigation=法务 review + 分阶段放开。
- DEC-201（ISS-003）：VIP 阈值，owner=VP CRM，target_close=下周二。
- INF-301（ISS-004）：缺客户分级数据，owner=数据团队。
- CLS-401（ISS-005）："所有角色" vs "仅经理"歧义。
- OUT-501（ISS-006）：积分机制，路由至下一版本。
每条带来源、知识状态、状态；accepted 均经决策者确认。

## Example: Sparse Input → Degraded Output

**Input**: 某阶段产物已完全 confirmed，无任何"待确认 / 冲突 / 风险"标记。
**Output**: Preflight 判定"无问题信号"→ 返回路由收据（问题清单可保持现状，不新增行）→ 不进入 Generate/Audit。若出现单个模糊口头表述（"这个之后再说吧"），则触发 AI 主动询问契约：先问"要不要登记为 CLS / DEC，由谁处理"，得到确认后才登记，status = `needs_user_input`。

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见问题清单反模式（写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约（ISS-NNN） | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |

## Completion

每个阶段的"待确认"都已收录到本清单（或记录关闭理由）；每个 open 问题都有 Owner；BLK / DEC 都有 target_close；30 天以上 open 都有 escalation；决策者已显式接受所有 `accepted` 状态；`resolved` 都链接到关闭它的产物变更；登记全部先经用户确认；PRD 确认前问题清单已"清零"或带显式接受的风险。
