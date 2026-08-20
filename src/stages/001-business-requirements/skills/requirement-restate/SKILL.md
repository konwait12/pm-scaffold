---
name: requirement-restate
description: 需求复述能力（单模式，RR-NNN）：用 stakeholder 原话 verbatim 重述确认，冲突路由 issue-record（CLS）、未知路由 Q-XXX（INF）。本 skill 是能力（output_kind=process），产物为过程记录，不进 PRD 正文。Use when 多源术语不一致 / 需要"我们真的同意了吗"检查位 / 新 stakeholder 重新锚定，且材料有可追溯来源 L1-L4。（发散收敛已拆出为独立 brainstorming skill。）
---

# Requirement Restate（需求重举 · 复述确认能力）

## 目的与边界（Purpose And Boundary）

本 skill 是**能力（`output_kind=process`）**，不是产物型 skill：它产出的过程记录（RR 重述清单）**永远不进 prd.md 正文**，只作为「共享理解检查点」喂给后续工作项。注册表 `workflow-registry.json` 已将其标记为 `output_kind: process`。

本 skill **只做收敛确认（verbatim 复述）**，仅在有可追溯来源（L1-L4）时运行。**发散收敛已拆出为独立的 `brainstorming` skill**（材料稀疏 / L0 时的候选发散与人工四值处置，不再属于本 skill）。

- **需求复述 RR-NNN**：原始需求可追溯（L1-L4，至少存在口头或书面来源）时，用 **stakeholder 原话 verbatim** 逐条复述确认，建立共享理解检查点。矛盾标 `CONFLICT` → 路由项目级 `issue-record` 的 `ISS-NNN`（通常为 CLS 或 DEC）；未知标 `UNKNOWN` → 写 `Q-NNN` 提问并路由 `issue-record` 的 `ISS-NNN`（通常为 INF）。

**Do not**：不发明业务事实、不替 stakeholder / 负责人做处置决定、不把 AI 推断当已确认需求、不让过程记录本身到达 `confirmed`。本 skill 不在此解决冲突（只标记并路由到 issue-record）。

**PRD 归宿**：❌ **永远不进 PRD 正文**。本 skill 是分析过程（Analysis Process），产物是过程记录。复述确认通过后：重述通过的需求行进入 `project-background-goal` 和 `user-journey` / `user-stories` 草案；CONFLICT → `issue-record` 的 ISS-XXX（CLS / DEC）；UNKNOWN → Q-XXX 提问 + `issue-record` 的 ISS-XXX（INF）。`requirement-restate.md` 过程记录本身永远不进入 prd.md 正文。

**本 Skill 属于 Branch**（参见 `src/framework/governance.md` §Human-In-The-Loop Inquiry Contract）。`prd-assembly` 进入 §0 上游清单时会**主动询问**"要不要在 §0 标注 requirement-restate 来源链"——若 stakeholder 显式要求可追溯到 restate，则 §0 加一行 RR-XXX 摘要；否则不出现。触发条件：原始需求被多团队/多语言/多源转述、多源术语不一致、误读代价高（合规/法律/昂贵构建）、需要正式的"我们真的同意了吗"检查位、新 stakeholder 加入需重新锚定、材料稀疏到无法进入主干（L0，此时交给 brainstorming skill）。

## 输入与输出（Inputs And Outputs）

Inputs:
- Original source materials（meeting minutes, emails, BRD, audio/video transcripts, chat, tickets）——源材料必需（L1-L4）
- Background artifact（`background-goal.md`，如有）
- 范围基线（journey 的 §范围基线，如有）
- The full chain of prior conversation（chat, ticket, ticket comments）

Output（均为**过程记录**，非 PRD 产物）:
- `requirement-restate.md`（§1-§9，RR-NNN 重述清单 + CONFLICT→ISS / UNKNOWN→Q+ISS 路由），模板 `assets/requirement-restate-template.md`

Load `references/thinking-framework.md`（Common Core + 需求复述 lens）before analysis. Load `references/output-contract.md`（RR 行契约）before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Load `references/source-handling.md` during Intake when登记 SRC-*。Run `scripts/validate_artifact.py <artifact> --json` before review.

## 思考提示词（按阶段）（Thinking Prompts per stage）

### 1. Preflight
- 有可追溯来源（L1+）→ 运行本 skill（RR-NNN）；L0 仅想法 / 材料稀疏 → 交给 `brainstorming` skill；多源歧义 → 先收敛来源。
- "stakeholder 实际说了什么，用他们自己的话？""我们依据哪些来源重述？有没有未被转写的音频/视频/聊天？"识别：项目名、项目 ID（REQ-XXX）、stakeholder(s)、来源。为每个来源登记 SRC-ID。评估成熟度：L1（单条口头表述）→ L2（单源书面）→ L3（多源一致）→ L4（多源冲突，需消歧）。
- **如果无来源且诉求只是记忆转述 → 返回路由回执并建议送入 `brainstorming` skill，在 `needs_user_input` 停下。**

### 2. Intake
- verbatim 保留原始措辞（方言、口语、术语照抄），不翻译成"我们以为的意思"。
- "每个来源实际上说了什么——不是我认为它是什么意思？"逐源提取候选需求；跨源合并重复项（同一诉求、不同措辞）并注明；矛盾标 `CONFLICT`（**不解决，只标记**）；每条标知识状态：`FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`；登记 SRC-*。

### 3. Think (apply thinking-core.md §1 mandatory lenses + 复述专属 lens)
- **First Principles**: "剥离所有提议方案后，这个诉求本身是什么？"
- **Systems Thinking**: "这个诉求是否隐含一个也在推进中的上游/下游系统？涉及哪些角色、数据、流程？"
- **Role Perspective**: "stakeholder 能否在重述里认出他们自己的话？"
- **Constraint Analysis**: "stakeholder 在诉求里嵌入的硬约束（时间/预算/平台/合规），我们是否不能静默移除？"
- **Adversarial**: "最糟糕的误读方式是什么？重述是否防御了这种误读？"
- **Reverse Validation**: "如果 stakeholder 只读重述，他们看到的正是他们想说的吗？"

### 4. Clarify
- 每个 `CONFLICT`：列出双方措辞，路由给 stakeholder 选择（含 AI 初判 + 选项 + 影响 + owner），并在 `issue-record` 创建或引用 ISS-NNN。每个 `UNKNOWN`：创建 Q-NNN 请 stakeholder 补全，并在 `issue-record` 创建或引用 ISS-NNN。Batch questions：≤5 per session，按影响排序。
- 遇到「待确认 / 冲突 / 信息缺口」信号：自动登记带来源的 `issue-record` ISS-NNN，并更新 §13 收口表；仅对业务决定、owner、接受或关闭动作提问。送审前 dor_check 会硬检查收口与引用。
- **当冲突或未知会改变诉求本身时，停在 `needs_user_input`。**

### 5. Generate
- 填模板 `assets/requirement-restate-template.md`。每条重述需求：ID（`RR-NNN`）、重述（stakeholder 的话）、原始措辞（verbatim）、来源、知识状态、提出方、confidence。发现"方案泄露"（重述夹带方案）→ 标 `solution_leak=true`，需 stakeholder 重新确认。状态：使用 `draft`、`needs_user_input` 或 `conditional_review`——**绝不用 `confirmed`**。

### 6. Audit
- **Source Coverage**：每条 Intake 登记的 SRC-ID 都反映在重述清单中。
- **Atomicity**：没有一行塞两个诉求。
- **No Solution Leak**：没有一行含方案/技术/设计。
- **Conflict Visibility**：所有冲突被标记，未被解决。
- **Stakeholder Recognition**：重述可原样发回给 stakeholder 且读起来忠实。
- 运行 `scripts/validate_artifact.py <artifact> --json`。修复所有错误。警告 → 记录进 audit notes。
- **B3 收口**：确认 issue-record 的 §13 收口表已更新本 skill 行（问题数 / 收口日期 / 状态；空阶段也落行），且本文件每个 CON-/UNK- 行均链接对应 ISS-NNN。

### 7. Human Gate
- Present 重述条数、冲突条数、未知条数、来源覆盖、audit 结果。**原 stakeholder（或其指定代理）必须确认重述。** 批准会创建带 SHA-256 的 ReviewRecord。

### 8. Commit / Reflow
- 只有 `pipeline.py review --decision approve` 可以写入 `confirmed`。发生变更时：记录 delta → 重新 Audit → 重新校验 → 返回 Human Gate。这里浮现的冲突必须升级到 `issue-record.md` 解决，不在本 skill 内解决。
- 过程记录本身最高 `ready_for_human_review`；只有 `pipeline.py review` 可确认下游工作项。

## 反模式（Anti-Patterns）

| ❌ 不要 | ✅ 要做 |
|---|---|
| 用自己的话重述诉求 | 用 stakeholder 的话；能引用就引用原文 |
| 隐藏来源（"业务方说要…"） | 始终引用 SRC-ID，具体到段落/时间戳 |
| 在重述阶段解决冲突 | 标 `CONFLICT` 并路由到 issue-record |
| 把 AI 推断当 stakeholder 原话 | 重述只含来源支持的内容，推断标 AI_INFERENCE |
| 让过程记录以 `confirmed` 交付 | 记录最高 `ready_for_human_review`；仅 `pipeline.py review` 可确认下游工作项 |

## Example: Sufficient Input → Sufficient Output

**输入**：3 个来源——一份会议纪要、一封跟进邮件、一条工单评论——都在描述同一个诉求。
**Output**: 完整 requirement-restate.md——
- 7 条重述需求（RR-001…RR-007），每条链接到来源。
- 1 个 CONFLICT：会议说"所有角色"，邮件说"仅经理" → 路由给 stakeholder 选择。
- 2 个 UNKNOWN：deadline 未指定、成功指标未指定 → 路由给 stakeholder 补全。
- 0 个方案：尽管会议提到"dashboard"，重述仅记为 hint，不当作决议。

## Example: Degraded Output（稀疏降级·复述版）

**Input**: 聊天消息 "make it faster for our VIPs"（无附件、无来源）。
**Output**: Preflight 判定 L1（单条口头表述，无源，材料不足以做复述）→ 不进入 Generate/Audit → Clarify 批量产出：这是指哪个流程更快？VIP 的定义？"更快"的成功判据？当前耗时基线？——每条带 AI 初判 + 选项 + 影响 + owner → status = `needs_user_input`。

## 加载参考文档（Load References）

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（复述） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物契约：RR-NNN 行 + Artifact States | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 需求复述 lens，必读） | 每次任务开始（必读） |
| `src/shared/clarify/references/confirmation-signal-technique.md` | MRC 门禁与确认信号技法（白/灰/黑信号识别，复述确认收敛） | Clarify 识别复述确认信号时（按需） |
| `references/gap-checklist-14d.md` | 14 维度缺口扫描清单（结构性遗漏检测，P0/P1/P2 定级） | Intake 后 RR 定稿前扫描时（按需） |
| `references/fact-ledger.md` | 事实台账五分型 F/D/A/W/O + 三色标注 + 来源可信度仲裁链 | Intake 多源素材/冲突仲裁时（按需） |
| `references/interview-synthesis.md` | 访谈五步提炼法 + 问题措辞 5 铁律（口语化描述转结构化需求） | 处理访谈原话/生成 Clarify 问题时（按需） |

## 完成标准（Completion）

- 每条来源里的诉求都用 stakeholder 的话重述；每行都有来源绑定与原始措辞；冲突全部标记并回链 issue-record 的 ISS-NNN；未知全部以 Q-NNN 提问并回链 issue-record 的 ISS-NNN；原 stakeholder（或其指定代理）确认"是的，这就是我说的"。
- issue-record §13 收口表已更新本 skill 行；过程记录从不进入 prd.md 正文；项目可进入 scope / journey / PRD 工作。
