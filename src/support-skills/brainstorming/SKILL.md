---
name: brainstorming
description: 发散收敛能力（单一模式，SCN-XXX）。材料稀疏 / L0（仅一行想法）或方案发散时，按 12 个场景维度发散候选，聚类去重编号 SCN-XXX、全标 AI_INFERENCE，交人工四值处置（include/exclude/defer/research），仅 include 候选综合成输入包写入 project-background-goal。本 skill 是能力（output_kind=process），产物为过程记录 brainstorming-output.md，不进 PRD 正文。Use when the ask exists only as a thin one-line idea at L0, input material is sparse, or a stakeholder needs a divergence pass before converging on requirements.
---

# Brainstorming（发散收敛 · 头脑风暴能力）

## 目的与边界（Purpose And Boundary）

本 skill 是**能力（`output_kind=process`）**，不是产物型 skill：它产出的过程记录 `brainstorming-output.md`（SCN 发散候选与人工处置表）**永远不进 prd.md 正文**，只作为「收敛后的输入包」喂给后续工作项。注册表 `workflow-registry.json` 已将其标记为 `output_kind: process`。

本 skill 是**发散器**，只负责一件事：当输入**只停留在一行想法 / 材料稀疏 / 需要方案发散**时，把"这想法到底是什么"扩展成一组可被人工处置的候选。它**不做**需求复述确认（那是 `requirement-restate`）、不做冲突路由（CONFLICT 是复述阶段的职责）、不做可行性判断。

按 **12 个场景维度**发散候选（lifecycle / roles / normal-alternate-exception-failure-timeout / permission / data condition / handoff / dependency / cancellation / retry / rollback / change-recovery / constraint），聚类去重后编号 `SCN-XXX`、**全部标注 `AI_INFERENCE`**，交人工 **四值处置**（`include` / `exclude` / `defer` / `research`），**仅 `include` 候选**综合成 ≥50 字输入包写入 `project-background-goal` 输入包。

**Do not**：不发明业务事实、不替负责人做处置决定、不把发散候选当已确认需求、不让过程记录本身到达 `confirmed`、不把候选直接写回正式产物（只有 `include` 进输入包）。

**PRD 归宿**：❌ **永远不进 PRD 正文**。本 skill 是分析过程（Analysis Process），产物是过程记录。确认后仅 `include` 候选综合为输入包进入 `project-background-goal`。`brainstorming-output.md` 过程记录本身永远不进入 prd.md 正文。

**本 Skill 属于 Branch**（参见 `src/framework/governance.md` §Human-In-The-Loop Inquiry Contract）。仅当 stakeholder 显式要求可追溯 SCN-XXX 时，`prd-assembly` 才在 §0 加一行摘要；否则不出现。触发条件：L0 仅一行想法、材料稀疏到无法进入主干、需要方案发散与候选收敛。

## 输入与输出（Inputs And Outputs）

Inputs:
- L0 原始想法 / 稀疏材料（仅一行想法即可触发）
- 若有材料（消息 / 邮件 / 纪要）按 `references/source-handling.md` 登记 SRC-*
- Background artifact（`background-goal.md`，如有）
- 范围基线（journey 的 §范围基线，如有）

Output（均为**过程记录**，非 PRD 产物）:
- `brainstorming-output.md`（SCN-XXX 候选表 + 8 列人工处置表 + 收敛后输入包），模板 `src/templates/others/brainstorming-output.md`

Load `references/thinking-framework.md`（Common Core + 12 维度发散 lens）before analysis. Load `references/output-contract.md`（SCN 候选表 / 处置表契约）before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Load `references/source-handling.md` during Intake when登记 SRC-*。Run `scripts/validate_artifact.py <artifact> --json` before review.

## 思考提示词（按阶段）（Thinking Prompts per stage）

### 1. Preflight
- 确认触发：L0 / 稀疏 → 发散收敛；多源歧义 → 复述（requirement-restate）；材料充分 → 直接进入 `project-background-goal`。
- **需求三路径分类**（AI 初判、人工可覆盖，见 `references/thinking-framework.md` §三路径分类）：轻量澄清（范围小 → 短发散）／标准发散（常规 L0/稀疏 → 现有 12 维全流程）／全景发散（跨模块·多系统·多角色 → 全 12 维 + 分段呈现 + 可选 viz）。判定路径在开跑时口头宣告，供人工覆盖。
- 确认负责处置的人工（business_owner）与证据边界。评估成熟度：L0（无源）→ 稀疏（单行 + 少量材料）。
- **如果想法为空或无法识别负责人工 → 返回路由回执并在 `needs_user_input` 停下。**

### 2. Intake
- 捕获原始想法原文作为证据基础（纯 L0 无源时明示"其余皆为推断"）；若有材料（消息/邮件/纪要）按 `references/source-handling.md` 登记 SRC-*。verbatim 保留原始措辞，不翻译成"我们以为的意思"。

### 3. Think (apply thinking-core.md §1 mandatory lenses + 发散 lens)
- **First Principles**: "剥离所有提议方案后，这个想法本身是什么？"
- **Systems Thinking**: "这个想法是否隐含一个也在推进中的上游/下游系统？涉及哪些角色、数据、流程？"
- **Role Perspective**: "对每个可能角色——他们获得什么、失去什么、需要什么？"
- **Constraint Analysis**: "想法里嵌入的硬约束（时间/预算/平台/合规），我们是否不能静默忽略？"
- **Adversarial**: "最糟的想法展开方式是什么？候选是否防御了这种误读？"
- **Reverse Validation**: "从想要的结果倒推，什么必须先成立？"
- 额外：**12 维度发散 lens**（lifecycle/roles/normal-alternate-exception-failure-timeout/permission/data condition/handoff/dependency/cancellation/retry/rollback/change-recovery/constraint，见 `references/thinking-framework.md`）→ 聚类去重后每个独立想法得稳定 ID `SCN-XXX`。

### 4. Clarify
- **对话式逐问**（吸收自超能力启发范式）：**优先一次一问、选择题优先**（2-4 个互斥选项 + 「其他」），仅确有多个独立缺口时批量；每题带 AI 初判 + 证据 + 选项 + 影响 + owner + blocking flag；答案会实质改变候选集或处置选项时 **STOP at `needs_user_input`**。Limit ≤5 questions per session，按影响排序。
- 遇到「待确认 / 信息缺口」信号：自动登记带来源的 `issue-record` ISS-NNN（仅 PM/PRD 问题）并更新 §13 收口表；仅对业务决定、owner、接受或关闭动作提问。送审前 dor_check 会硬检查收口与引用。
- **当答案会实质改变候选集或处置选项时，停在 `needs_user_input`**。

### 5. Generate
- 聚类去重后、写回前做 **YAGNI 削减**（见 `references/thinking-framework.md` §YAGNI 削减）：把"对本需求目标无贡献 / 成本高收益低"的候选划入 `exclude`/`defer`（Reason 注明）；AI 仅初判，最终处置仍由人工拍板。
- 填 `src/templates/others/brainstorming-output.md`。填 SCN 候选表（全 `AI_INFERENCE`，每条含 Evidence 与 Impact）→ 8 列人工处置表（Disposition 留给人工）→ Include 项写回 → 收敛后输入包（≥50 字）。状态：使用 `draft`、`needs_user_input` 或 `conditional_review`——记录本身**永不** `confirmed`。

### 6. Audit
- **Completeness**：12 维度全部扫过或显式跳过；每条候选带 Evidence + Impact。
- **Inference Discipline**：每条候选标 `AI_INFERENCE`；无任何内容被当成事实。
- **Disposition Readiness**：处置表就绪；每个 `include` 候选命名写回目标。
- 运行 `scripts/validate_artifact.py <artifact> --json`。修复所有错误。警告 → 记录进 audit notes。
- **B3 收口**：确认 issue-record 的 §13 收口表已更新本 skill 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
- 发散覆盖摘要（哪些维度产出什么）、候选表（证据+影响）、每条候选的推荐处置、deferral risks。**呈现候选摘要后必须显式 `stop` 等人工处置，不得边展示边写回**（对齐 approval-gate 硬纪律）。**只有负责人工（business_owner）可以处置**每个候选（`include` / `exclude` / `defer` / `research`）。写回批准会创建带 SHA-256 的 ReviewRecord。

### 8. Commit / Reflow
- Write back **only `include` candidates** 综合为 ≥50 字充分输入，写入 `project-background-goal` 输入包，然后返回当前 Work Item。处置不完整或出现实质新想法 → 从 Preflight 重新进入本 skill，不补丁下游；写回后出现矛盾 → 重新进入而非静默修订目标产物。
- 过程记录本身最高 `ready_for_human_review`；只有 `pipeline.py review` 可确认下游工作项。

## 反模式（Anti-Patterns）

| ❌ 不要 | ✅ 要做 |
|---|---|
| 把一行想法变成"事实" | 保持全 `AI_INFERENCE` 直到人工处置 |
| 只在一个维度发散，如只看角色 | 扫全 12 维度（lifecycle/roles/normal-alternate-exception-failure-timeout/permission/data condition/handoff/dependency/cancellation/retry/rollback/change-recovery/constraint） |
| 出 40 条近似重复候选 | 聚类去重；一个独立想法一个 `SCN-XXX` |
| 替人工决定 include/exclude/defer/research | 展示处置表；只有人工标记处置 |
| 让 `research` 静默搁置 | `research` 成为 issue-record 条目 / QuestionRecord 并被跟进 |
| 把 excluded 候选也写回 | 仅 `include` 候选进入输入包 |
| 让过程记录以 `confirmed` 交付 | 记录最高 `ready_for_human_review`；仅 `pipeline.py review` 可确认下游工作项 |
| 在本 skill 里解决来源冲突 | 冲突是复述（requirement-restate）阶段的职责；这里只发散本想法 |

## Example: Sparse Input → Divergence + Disposition

**Input**: L0 想法——"做客户邀约活动，名单约 500 人，预算 10 万，希望月底前上线"（无书面材料）。
**Output**: 12 维度发散 → 聚类去重到 5 个候选 → SCN 候选表（证据+影响，全 AI_INFERENCE）→ 8 列处置表（3 include / 1 defer / 1 research）→ include 写回输入包 ≥50 字 → `ready_for_human_review` → 输入包交给 `project-background-goal`。

## Example: Degraded Output（稀疏降级）

**Input**: 消息 "想做客户邀约活动"（无更多信息）。
**Output**: Intake 登记消息为证据基础 → L0 判定 → 候选骨架（稀疏证据："AI 推断，无书面来源"）→ 3 个 Clarify 问题（活动目标 / 邀约对象范围 / 期望时间）→ 停于 `needs_user_input`，处置表待人工补齐。

## 加载参考文档（Load References）

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（发散收敛） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物契约：SCN-XXX 候选表 + 8 列处置表 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板 | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 12 维度发散 lens，必读） | 每次任务开始（必读） |
| `references/visual-companion.md` | 可选 viz 模式（仅全景发散 / 处置呈现时选用，纯增强不阻塞） | 全景发散 / Human Gate 呈现时（可选） |
| `references/compliance-keywords.md` | 合规/安全风险关键词库（位置/UGC/金融等候选风险提示） | SCN 候选涉及敏感关键词时（按需） |
| `references/v1-boundary.md` | V1 边界定义（必须 ≤3 个 + 三分类 + 轻量/中等/完整门槛） | 候选收敛定范围时（按需） |
| `references/mode-dispatch.md` | 三模式快速分流 + 5 类最小信息提取 + 定向补问 | Preflight 判断任务形态时（按需） |

## 完成标准（Completion）

- L0/稀疏触发确认且证据边界明确；12 维度全部扫过或显式跳过；候选已聚类去重并拥有稳定 `SCN-XXX` ID；每条候选带 Evidence、Impact 与 `AI_INFERENCE` 标注；处置表可供人工四值处置（或已处置）；仅 `include` 候选综合为 ≥50 字输入包写入 `project-background-goal`。
- issue-record §13 收口表已更新本 skill 行；过程记录从不进入 prd.md 正文；项目可进入 scope / journey / PRD 工作。
