---
name: user-journey
description: Build a lifecycle-by-role user journey map — lifecycle model, role personas, emotion mapping, pain-point → opportunity, and path diversity. Independent work_item, produces user-journey.md.
---

# User Journey · 用户旅程

## 目的与边界（Purpose And Boundary）

通过角色视角绘制用户完成生命周期目标所经历的路程/阶段，识别每个阶段的行为、触点、痛点与情绪波动，并将痛点转化为机会。输出独立的 `user-journey.md`，不填充任何其他产物的章节。

**Do not** 编写用户故事卡片（→ `user-stories`）、建立范围基线（→ `user-stories`）、设计功能清单（→ `feature-list`）、定义页面或交互（→ `page-design`/`interaction-rules`）。本 skill 只绘制"用户如何经历这段旅程"——行为与情绪的客观映射。

## 输入与输出（Inputs And Outputs）

输入：已确认的 `background-goal.md`（来源材料、业务背景、目标、角色）。输出：独立的 `user-journey.md`，使用 `src/templates/resolver.py user-journey.md` 解析出的模板。

分析前加载 `references/thinking-framework.md`（其中引用 `src/framework/thinking-core.md` §1 必用透镜）。起草前加载 `references/output-contract.md`。交接前加载 `references/audit-checklist.md` 与 `references/reviewer-checklist.md`。评审前运行 `scripts/validate_artifact.py <artifact> --json`。

## 思考提示词（按阶段）（Thinking Prompts per stage）

### 1. Preflight
- "已确认的背景与目标中，哪些角色需要完成什么生命周期目标？"
- 从 `background-goal.md` 枚举已识别的角色及其业务目标。检查每个角色是否有足够的来源支撑。
- **若没有可用角色或目标**，返回一张路由回执并 STOP——不要进入 Intake。
- 评估成熟度：L0（无角色）→ L1（单一角色）→ L2（多角色但无阶段）→ L3（角色+阶段+触点）→ L4（上游已确认）。

### 2. Intake
- "每个角色在实际工作中如何完成这个目标——而不是我假设的标准流程？"
- 从来源中逐字提取每个角色的：目标、动作、触点、决策点、异常退出、情绪线索。
- 按 `src/framework/contracts.md` 将每条主张分类为 `FACT`、`DECISION`、`ASSUMPTION`、`AI_INFERENCE`、`UNKNOWN` 或 `CONFLICT`。
- 保留来源 ID 与位置。不要把不同角色的旅程合并。

### 3. Think（应用 thinking-core.md §1 必用透镜）
- **第一性原理（First Principles）**："用户真正想完成的核心目标是什么？哪些步骤是伪装成需求的假设？"
- **系统思维（Systems Thinking）**："哪些触点跨系统/部门？旅程中哪些地方依赖外部系统或第三方？"
- **角色视角（Role Perspective）**："这个角色在旅程中获取什么、失去什么、什么让他们卡住或沮丧？"
- **约束分析（Constraint Analysis）**："时间、设备、环境、权限等硬约束如何影响旅程可选项？"
- **对抗性审视（Adversarial）**："旅程中哪些点最容易让用户放弃或出错？什么会让他们转向竞品？"
- **逆向验证（Reverse Validation）**："从目标倒推，旅程中哪些阶段/触点不可或缺？"

### 4. Clarify
- 先尝试调研可发现的缺口（复查来源、竞品旅程、行业基准）。
- 剩余问题批量提交，附带：AI 初步判断、证据、选项、影响、负责人、阻断标记。
- **当某个答案可能改变角色、阶段、触点或情绪判断时，停在 `needs_user_input`**。
- 数量限制：每轮 Session 至多 5 个问题，按影响排序。
- 遇到「待确认 / 冲突 / 信息缺口」信号：自动登记带来源的 issue-record `ISS-NNN`（只记录 PM/PRD 问题）；仅对业务决定、owner、接受或关闭动作提问。送审前 dor_check 会硬检查收口与引用。

### 5. Generate
- 填充模板。每个角色绘制一张旅程图：阶段 → 触点 → 行为 → 痛点 → 情绪曲线 → 机会。
- 情绪曲线：沿旅程标记高/中/低情绪点，关联痛点来源。
- 路径多样性：标注主路径、分支路径、异常退出路径。
- 痛点→机会：每个痛点对应至少一个可量化改进的机会。
- 状态：使用 `draft`、`needs_user_input` 或 `conditional_review`——**绝不用 `confirmed`**。

### 6. Audit
- **完整性（Completeness）**：所有已确认角色都有旅程图；每个阶段有触点/行为/情绪。
- **情绪一致性**：情绪曲线有来源依据；无凭空发明的高兴/沮丧。
- **机会有效性**：每个痛点对应 ≥1 个机会；机会可追踪到痛点根因。
- **路径覆盖**：主路径、分支、异常退出均有标注。
- **下游可用性**：`user-stories` 能否无需重新调研就直接从这些旅程产出故事？
- 运行 `scripts/validate_artifact.py <artifact> --json`。修复所有错误。警告 → 记录进 audit notes。
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
呈现：角色旅程摘要、情绪曲线与痛点分布、机会清单、证据摘要、审计结果、变更摘要。
**只有业务/产品负责人可以批准。** 批准会创建带 SHA-256 的 ReviewRecord。

### 8. Commit / Reflow
- 只有 `pipeline.py review --decision approve` 可以写入 `confirmed`。
- 发生变更时：记录 delta → 更新受影响的旅程章节 → 重新执行 Audit → 返回 Human Gate。
- 后续出现矛盾 → 从本 Skill 的开头重新进入（不在下游打补丁）。

## 反模式（Anti-Patterns）

| ❌ 不要 | ✅ 要做 |
|---|---|
| 画一条"完美用户"路径 | 覆盖主路径 + 分支路径 + 异常退出 |
| 把情绪写成"满意/不满意" | 用具体、可观察的行为描述情绪（"反复修改"、"询问同事"） |
| 一个角色只有一个情绪高点/低点 | 沿旅程多个触点标注情绪变化 |
| 痛点写"体验不好" | 写具体行为："在第3步找不到导出按钮，尝试3次" |
| 把机会写成功能方案 | 写可衡量的改进结果，如"减少50%表单填写时长" |
| 为每个角色画相同结构的旅程 | 按角色真实的目标/阶段差异绘制 |
| 把"用户行为"画成"产品功能/页面"（"看报表页""点按钮"） | 主语始终是角色、动词可观察（"监控项目进度""汇总业绩"）；见 `journey-behavior-vs-feature-jtbd.md` |

## 示例：充足输入 → 充足输出（Sufficient Input → Sufficient Output）

**输入**：已确认 `background-goal.md`，含 VIP 客户、业务负责人、运营人员三个角色，以及业务背景、目标与约束。
**输出**：每角色一张旅程图——含阶段（认知→探索→决策→使用→续费）、触点（APP/短信/邮件）、行为、痛点（注册复杂/找不到报表）、情绪曲线（从低到高到稳定）、机会（简化注册→引导视频→智能报表），以及主路径/分支/异常退出标注。

## 示例：稀疏输入 → 降级输出（Sparse Input → Degraded Output）

**输入**：`background-goal.md` 仅含"VIP 客户需要一个预约系统"。
**输出**：Preflight 返回 L1 → Intake 枚举单一角色为 `UNKNOWN` → Think 识别缺失：角色任务阶段？触点有哪些？情绪变化？→ Clarify 生成 3 个问题 → 停在 `needs_user_input`。不为凑图而编造旅程细节。

## 加载参考文档（Load References）

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（写旅程时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |
| `references/journey-matrix-and-mot.md` | 旅程矩阵与关键时刻技法（角色×阶段 MECE 矩阵 / 情绪曲线 MOT / 触点矩阵 / 痛点→机会） | 多角色多阶段旅程或定位 MOT 时（按需） |
| `references/journey-error-recovery-and-metrics.md` | 旅程错误恢复与指标技法（每步 Success Criteria 勾选 / 摩擦→缓解 / E1/E2 错误恢复四段式 / 旅程级 4 类指标） | 旅程需被验收/可测试、或含高风险异常路径、或需定义埋点指标时（按需） |
| `references/journey-behavior-vs-feature-jtbd.md` | 用户行为≠功能技法（行为三问测试 / 一句话结果导向 JTBD 叙事 / 骨架活动 3-5 条 / 层层下钻留接口） | Intake 判行为vs功能 / Generate 前搭叙事主线 / Audit 查功能泄漏时（按需） |

## 产品质量增强（L1 必须）

旅程必须把角色×阶段×触点的事实与未知分开，并完成“痛点→机会→故事”的覆盖。送审前填写产品质量增强记录；多角色冲突、替代路径不清或机会无法由证据支持时，先澄清或升级，不编造用户研究结论。

## 完成标准（Completion）

所有已确认角色都有完整的旅程图；每条旅程含阶段/触点/行为/痛点/情绪曲线/机会；情绪有来源依据；每个痛点对应可衡量的机会；主路径/分支/异常退出均有覆盖；旅程不包含用户故事卡片或范围基线；在启动 `user-stories` 前，获得授权的人类批准了用户旅程基线。

## 融合指引

旅程永远画在**用户行为层**，不画产品功能。分析前先想"角色在达成什么生活/业务结果"（一句 JTBD 叙事），再按行为→触点→情绪铺开；凡出现"看 X 页 / 点 X 按钮 / 系统怎么做"，即功能泄漏，路由到 `feature-list` / `functional-flow`，见 `references/journey-behavior-vs-feature-jtbd.md`。动机与优先级不在此展开（→ `user-stories/job-story-and-moat.md`、`feature-list/feature-priority-quant.md`）。
