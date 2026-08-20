---
name: issue-record
description: 跨阶段共享的 PM/PRD 问题清单 — 集中登记 BLK / RSK / DEC / INF / CLS / OUT 六类需求问题；AI 对有来源的发现自动登记为 draft/open，人工负责业务决定与关闭。任何 Skill 都可以登记 / 引用 / 升级问题。
---

# Issue Record（跨阶段共享）

## 目的与边界

维护一个**项目级**（不是阶段级）的问题清单 `issue-record.md`。它只记录 PM/PRD 需求过程中的澄清、冲突、待决、风险、信息缺口与范围外路由，**不记录仓库缺陷、测试失败、部署故障或实现任务**。每个问题有：类别、状态、Owner、知识状态、来源、目标关闭日期。任何阶段的任何 Skill 在 Clarify 阶段遇到**阻断（BLK）**、**风险（RSK）**、**待决（DEC）**、**信息缺口（INF）**、**歧义（CLS）**、**范围外（OUT）**时，AI 应基于来源自动登记为 draft/open；问题被阶段产物确认后才能关闭。它给业务方一个权威的"还有什么没解决"清单，也是 PRD 确认前必经的"问题清零"环节。

**不要**在 Issue Record 中写需求、设计方案、用户故事或 PRD 章节。Issue Record 只列"卡点 / 风险 / 待决"，方案交给后续 Skill。不要替决策者接受风险（`accepted` 状态只能由决策 Owner 设置）。

**AI 行为硬约束**：当用户输入或源材料出现"待确认 / 不明确 / 没说过 / 模糊 / 矛盾"等信号时，AI 必须在给出方案之前将其**自动登记**为带来源的 ISS-NNN（默认 `draft` / `open`），并向用户展示类别、影响、建议 owner 与待答 Q-NNN；不得默默继续。AI 不能自行设为 `accepted` / `resolved` / `confirmed`，也不能替业务方确定 owner 或业务决策。

**PRD 归宿**：❌ **默认不进 PRD**。issue-record 是过程记录（Process Record），不是 PRD 产物。但 AI 在 `prd-assembly` 进入 §9 / §10 时**主动询问**业务方"要不要把 issue-record 的'未关闭问题摘要'或'已接受风险列表'暴露为 §9 未决风险摘要"——若业务方要求可见性则引用摘要，否则不出现。这是 **Human-in-the-Loop 配置**，问题清单本身永远不进入 PRD。

**本 Skill 属于 Branch**（参见 `src/framework/governance.md` §Human-In-The-Loop Inquiry Contract），跨阶段共享（001 / 002 / 003 均可触发）。触发条件：任何阶段的"待确认"信号、来源冲突、待决决策、风险、口头未签字、推导与 FACT 冲突、阶段产物遗留 UNKNOWN。

## 输入与输出

输入：
- 任何阶段的产物（background-goal / user-journey / user-stories / feature-list / functional-flow / page-design / interaction-rules / business-rules / validation-rules / state-machine / exception-handling / acceptance-criteria / PRD）中的"待确认" / UNKNOWN / CONFLICT 标记
- 任何阶段的 Clarify 会话中识别的新问题
- 业务方 / PM / 干系人主动提出的问题

输出：`issue-record.md`（项目级 PM/PRD 过程记录，`99-review/support/` 下，跨阶段共享），用模板 `assets/issue-record-template.md`（§1-§13），含按类别（BLK/RSK/DEC/INF/CLS/OUT）与状态分组的表。

分析前加载 `references/thinking-framework.md`（其中引用 `src/framework/thinking-core.md` §1 必用透镜 + 领域 lens）。起草前加载 `references/output-contract.md`。移交前加载 `references/audit-checklist.md` 和 `references/reviewer-checklist.md`。在 Intake 登记 SRC-* 时加载 `references/source-handling.md`。在 Clarify 识别确认信号 / 跑 MRC 门禁时按需加载 `src/shared/clarify/references/confirmation-signal-technique.md`（见 `thinking-core.md §5` MRC 门禁/确认信号技法）。评审前运行 `scripts/validate_artifact.py <artifact> --json`。

## 思考提示（按阶段）

### 1. Preflight（预检）
- "目前有哪些产物？哪些'待确认' / UNKNOWN / CONFLICT 标记应升级为 ISS-NNN？"
- "每个类别的 issue 由谁负责（决策 owner、风险 owner、事实 owner）？"
- 登记上游产物引用。识别 goal_decision_owner 和 PRD 确认前"问题清零"责任人。
- **若任何地方都不存在问题信号**，返回路由收据（"无新问题，清单可保持现状"）并 STOP——不要发明问题。

### 2. Intake（输入）
- "这是 BLK、RSK、DEC、INF、CLS 还是 OUT？它来自哪个产物？应由谁负责？"
- 逐条提取问题信号（待确认 / 冲突 / 待决 / 风险 / 信息缺口 / 范围外），登记来源（上游产物 + SRC-*）。
- 标知识状态：`FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`。
- 查重：是否已在某阶段产物或本清单登记过（避免重复）。

### 3. Think（思考；应用 thinking-core.md §1 必用透镜）
- **First Principles（第一性原理）**："这个问题是真的阻断，还是换个路径就能绕开？剥离方案后问题还存在吗？"
- **Systems Thinking（系统思维）**："这个问题影响哪些下游 Work Item？不清零会导致哪些产物作废？"
- **Role Perspective（角色视角）**："对每个可能的 owner——他有权解决这个问题吗？他需要什么才能解决？"
- **Constraint Analysis（约束分析）**："哪些是硬约束（合规/法律/平台）导致的 blocker，无法用方案绕开？"
- **Adversarial（对抗性审查）**："如果把这个问题当作非阻塞，最坏会发生什么？证据支持降级吗？"
- **Reverse Validation（反向验证）**："从 PRD 确认反推——哪些问题必须在确认前清零，哪些可以带风险接受？"

### 4. Clarify（澄清）
- 类别归属、owner、是否阻断不明确时：批量提问（≤5 per session），带 AI 初判 + 选项 + 影响 + owner。
- 对有来源的信号自动生成 ISS-NNN，标注 AI 初判、影响与建议 owner；只就需要业务决策、owner 归属、阻断等级或关闭动作提问。
- **当答案会改变问题的类别、owner 或阻断状态时，停止在 `needs_user_input`**。

### 5. Generate（生成）
- 填模板。每个问题：ID（`ISS-NNN`）、category、state、title、description、owner、knowledge_state、source、affected_artifact、raised_at；BLK/DEC 加 target_close，RSK 加 mitigation，resolved 加 resolution，escalated 加 escalated_to。
- AI 可登记 `draft` / `open`，不得设置 `accepted` / `resolved` / `confirmed`；这些状态及业务 owner 由授权人工确认。
- **阶段收口（B3 强制）**：每个 work item 送审 `ready_for_human_review` 前，更新 §13 阶段收口表对应行（问题数 / 收口日期 / 状态）；空阶段也必须落行（问题数=0），这是审计证据。dor_check 会在 gate 时硬检查本表与引用。
- 状态：使用 `draft`、`needs_user_input`、`conditional_review` 或 `ready_for_human_review`。Issue Record 不是独立 work item；其存在、结构和 B3 收口由每个 work item 的 `pipeline.py ... gate` 校验，最终 PRD 由 `prd-assembly` 的人工 review 确认。

### 6. Audit（审计）
- **完整性（Completeness）**：上游产物每个"待确认"都有 ISS-NNN 引用或 documented 关闭理由。
- **责任归属（Ownership）**：每个 open 问题都有 owner。
- **时效（Dating）**：每个 BLK / DEC 都有 target_close；30 天以上 open 有 escalation 记录。
- **状态完整性（State Integrity）**：`accepted` 只能由决策者设；`resolved` 链接到关闭它的产物变更。
- **AI 自主登记合规**：每个登记均有来源与知识状态；AI 不得静默跳过信号，也不得无来源臆造问题、接受风险或关闭问题。
- 运行 `scripts/validate_artifact.py <artifact> --json`。修复所有错误。警告 → 记入审计备注。

### 7. Human Gate（人工关卡）
呈现：按类别与状态计数、critical top5、待决清单、accepted 风险、audit 结果。
**只有目标决策 owner / 业务发起人可批准 closed-out 清单。** 批准会创建带 SHA-256 的 ReviewRecord。

### 8. Commit / Reflow（提交 / 回流）
- Issue Record 的条目关闭与风险接受必须由具名业务 owner 记录；最终 PRD 的 `confirmed` 只能由 `pipeline.py review --decision approve` 写入。
- 变更时：记录 delta → 重新 Audit → 重新校验 → 回到 Human Gate。
- 跨阶段回流时，残留问题决定回流路径；问题被解决后链接到关闭它的产物变更。

## 反模式

| ❌ 不要 | ✅ 要做 |
|---|---|
| 在 Issue Record 中写"应该如何设计" | 只列问题，方案交给后续 Skill |
| AI 主动替业务方决定接受风险 | `accepted` 状态只能由决策者设 |
| 默默忽略"待确认"信号 | 自动登记为带来源的 ISS-NNN，再针对业务决定提问 |
| 让问题散落在 6 个产物中 | 集中维护一份问题清单 |
| 把问题清单当作需求清单 | Issue Record 是"未决"，不是"要做" |
| AI 自己发明不存在的问题 | 无信号就不登记，返回路由收据 |
| 让问题长期无 owner / 无 deadline | 每个 open 有 owner；BLK/DEC 有 target_close |

## 示例：充分输入 → 充分输出

**输入**：全流程产物：background-goal 遗留 2 个 UNKNOWN、user-journey 有 1 个边界争议、page-design 发现 1 个合规风险、prd-assembly 发现 1 个待决上线范围.
**输出**：完整 issue-record.md——
- ISS-001（BLK）：上线范围待决，owner=业务负责人，target_close=本周五。
- ISS-002（RSK）：合规风险（跨境数据），mitigation=法务 review + 分阶段放开。
- ISS-003（DEC）：VIP 阈值，owner=VP CRM，target_close=下周二。
- ISS-004（INF）：缺客户分级数据，owner=数据团队。
- ISS-005（CLS）："所有角色" vs "仅经理"歧义。
- ISS-006（OUT）：积分机制，路由至下一版本。
每条带来源、知识状态、状态；accepted 均经决策者确认。

## 示例：稀疏输入 → 降级输出

**输入**：某阶段产物已完全 confirmed，无任何"待确认 / 冲突 / 风险"标记。
**输出**：Preflight 判定"无问题信号"→ 返回路由收据（问题清单保持空清单，并完成当期 B3 收口）→ 不新增 issue。若出现单个模糊口头表述（"这个之后再说吧"），AI 自动登记为 CLS / DEC 候选，标建议 owner 与 Q-NNN，状态为 `needs_user_input`，等待人工决定类别、owner 与后续处置。

## 加载参考文献

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见问题清单反模式（写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约（ISS-NNN） | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |
| `src/shared/clarify/references/confirmation-signal-technique.md` | MRC 门禁与确认信号技法（白/灰/黑信号识别，Clarify 收敛） | Clarify 识别确认信号 / 跑门禁时（按需） |
| `references/issue-communication-and-escalation.md` | 问题沟通与升级技法（坏消息公式 / 冲突 4 模式 / 风险分级与 7-14 天升级阈值 / 四象限复盘 / Human Gate 呈现模板） | 通报坏消息、识别冲突、判断升级或 Human Gate 前（按需） |

## 完成标准

每个阶段的"待确认"都已收录到本清单（或记录关闭理由）；每个 open 问题都有 Owner；BLK / DEC 都有 target_close；30 天以上 open 都有 escalation；决策者已显式接受所有 `accepted` 状态；`resolved` 都链接到关闭它的产物变更；登记全部先经用户确认；PRD 确认前问题清单已"清零"或带显式接受的风险。
