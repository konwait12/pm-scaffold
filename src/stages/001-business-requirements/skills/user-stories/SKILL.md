---
name: user-stories
description: Transform confirmed user journey into story cards with MoSCoW prioritization and scope baseline (In/Out/Deferred/Conditional). Independent work_item, produces user-stories.md.
---

# User Stories · 用户故事与范围基线

## 目的与边界（Purpose And Boundary）

把已确认的用户旅程转化为规范格式的用户故事卡片、优先级排序与范围基线（In/Out/Deferred/Conditional）。每个故事必须可追溯到旅程中的某个痛点或机会。输出独立的 `user-stories.md`，不重新设计旅程或情绪映射。

**Do not** 重新绘制旅程图（→ `user-journey`）、重新做情绪映射（→ `user-journey`）、设计功能清单（→ `feature-list`）、定义页面或交互（→ `page-design`/`interaction-rules`）。本 skill 只负责"把旅程翻译成故事 + 排优先级 + 定边界"。

## 输入与输出（Inputs And Outputs）

输入：已确认的 `user-journey.md`（角色、阶段、触点、痛点、机会）。输出：独立的 `user-stories.md`，使用 `src/templates/resolver.py user-stories.md` 解析出的模板。

分析前加载 `references/thinking-framework.md`（其中引用 `src/framework/thinking-core.md` §1 必用透镜）。起草前加载 `references/output-contract.md`。交接前加载 `references/audit-checklist.md` 与 `references/reviewer-checklist.md`。评审前运行 `scripts/validate_artifact.py <artifact> --json`。

## 思考提示词（按阶段）（Thinking Prompts per stage）

### 1. Preflight
- "已确认的旅程中，哪些痛点和机会需要转化为故事？每个故事追溯到哪个旅程节点？"
- 从 `user-journey.md` 枚举已识别的角色、阶段、痛点与机会。检查每个机会是否有足够来源支撑。
- **若没有可用旅程或机会**，返回一张路由回执并 STOP——不要进入 Intake。
- 评估成熟度：L0（无旅程）→ L1（单一角色无机会）→ L2（多角色但无优先级）→ L3（已划分优先级）→ L4（上游已确认）。

### 2. Intake
- "每个机会真正需要系统做什么——而不是我认为故事应该是什么格式？"
- 从旅程的痛点/机会逐字提取故事候选。按 `src/framework/contracts.md` 将每条分类为 `FACT`、`DECISION`、`ASSUMPTION`、`AI_INFERENCE`、`UNKNOWN` 或 `CONFLICT`。
- 保留来源 ID（旅程节点引用）。不要把不同角色的机会合并成一个故事。

### 3. Think（应用 thinking-core.md §1 必用透镜）
- **第一性原理（First Principles）**："用户真正想达成什么可观察的结果？哪些故事伪装成了功能？"
- **系统思维（Systems Thinking）**："哪些故事相互依赖？哪些需要先完成才能解锁其他？"
- **角色视角（Role Perspective）**："这个故事对谁有价值？谁会因此少痛？"
- **约束分析（Constraint Analysis）**："时间、资源、技术限制如何影响故事范围？"
- **对抗性审视（Adversarial）**："这个故事的反面是否可能成立？什么会让它不重要？"
- **逆向验证（Reverse Validation）**："从期望的用户结果倒推，什么必须作为独立故事存在？"

### 4. Clarify
- 先尝试调研可发现的缺口（复查旅程节点、机会定义、来源材料）。
- 剩余问题批量提交，附带：AI 初步判断、证据、选项、影响、负责人、阻断标记。
- **当某个答案可能改变故事范围、优先级或归属时，停在 `needs_user_input`**。
- 数量限制：每轮 Session 至多 5 个问题，按影响排序。
- 遇到「待确认 / 冲突 / 信息缺口」信号：自动登记带来源的 issue-record `ISS-NNN`（只记录 PM/PRD 问题）；仅对业务决定、owner、接受或关闭动作提问。送审前 dor_check 会硬检查收口与引用。
- 范围边界或优先级存在取舍时，使用 `src/shared/clarify/references/scope-negotiation-scripts.md` 记录选项、代价、负责人和回滚条件，不得静默扩大 In 范围。

### 5. Generate
- 填充模板。每个故事一行规范卡片：ID（ST-XXX）/ 角色 / 故事描述（As a...I want...so that...）/ 验收条件 / 来源（旅程节点）/ 优先级（MoSCoW）。
- MoSCoW：Must（缺失则旅程无法完成）/ Should（显著提升满意度）/ Could（增强体验）/ Won't（本版不做，说明原因）。
- 范围基线：In（本版必须）/ Out（本版不做）/ Deferred（暂搁，有条件触发）/ Conditional（依赖某前提成立）。
- 旅程→故事覆盖矩阵：每行一个旅程痛点/机会，对应 ST-XXX。
- 状态：使用 `draft`、`needs_user_input` 或 `conditional_review`——**绝不用 `confirmed`**。

### 6. Audit
- **完整性（Completeness）**：每个已确认的旅程痛点/机会都有对应故事；无孤儿机会。
- **格式规范性（Format）**：每个故事符合 As a / I want / so that 格式，验收条件可测试。
- **MoSCoW 合理性**：Must 有清晰"缺失→旅程失败"判定；Should/Could 有理由说明。
- **范围基线一致性**：In/Out/Deferred/Conditional 划分有依据；无静默降级。
- **可追溯性（Traceability）**：每个故事回溯到旅程节点（user-journey.md 中的阶段/触点/痛点）。
- **下游可用性**：`feature-list` 能否无需重新解读故事就直接分解功能？
- 运行 `scripts/validate_artifact.py <artifact> --json`。修复所有错误。警告 → 记录进 audit notes。
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
呈现：故事卡片清单、MoSCoW 分布、范围基线、旅程→故事覆盖矩阵、证据摘要、审计结果、变更摘要。
**只有产品/业务负责人可以批准。** 批准会创建带 SHA-256 的 ReviewRecord。

### 8. Commit / Reflow
- 只有 `pipeline.py review --decision approve` 可以写入 `confirmed`。
- 发生变更时：记录 delta → 更新受影响的故事章节 → 重新执行 Audit → 返回 Human Gate。
- 后续出现矛盾 → 从本 Skill 的开头重新进入（不在下游打补丁）。

## 反模式（Anti-Patterns）

| ❌ 不要 | ✅ 要做 |
|---|---|
| 把故事写成功能描述（"系统应支持 X"） | 写用户视角的结果（"我能够 X，这样 Y"） |
| 所有故事都是 Must | 用 MoSCoW 区分；Must = 缺失则旅程失败 |
| 一个故事覆盖多个独立诉求 | 一个故事对应一个可测试的用户结果 |
| 把旅程中没有来源的机会写成故事 | 机会无来源时标 UNKNOWN，不编故事 |
| 把 Out 的故事删掉 | Out 进范围基线的 Out 列表；Deferred 进 Deferred 列表 |
| 不做旅程→故事覆盖矩阵 | 逐行对照，确保每个痛点/机会都有故事承接 |

## 示例：充足输入 → 充足输出（Sufficient Input → Sufficient Output）

**输入**：已确认 `user-journey.md`，含"注册复杂"（痛点）、"找不到报表"（痛点）、"简化注册引导"（机会）。
**输出**：ST-001（As a 潜在客户，我想要一键注册，这样 30 秒内完成注册）→ Must；ST-002（As a 运营人员，我想要自动生成报表，这样 无需手动汇总）→ Should；In: ST-001/ST-002；Out: ST-003（高级数据分析，本版不做）；覆盖矩阵：注册复杂→ST-001，找不到报表→ST-002。

## 示例：稀疏输入 → 降级输出（Sparse Input → Degraded Output）

**输入**：`user-journey.md` 仅含一行"VIP 客户预约体验不好"。
**输出**：Preflight 返回 L1 → Intake 枚举单一机会为 `UNKNOWN` → Think 识别缺失：具体痛点？期望结果？验收条件？→ Clarify 生成 3 个问题 → 停在 `needs_user_input`。不为凑故事卡片而编造 As a / I want / so that。

## 加载参考文档（Load References）

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（写故事时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |
| `references/use-case-spec-template.md` | UML 用例规格技法（参与者/前置后置/基本流/备选流/业务规则/数据说明） | Generate 用例规格时（按需） |
| `references/job-story-and-moat.md` | JTBD 三层动机 + 竞争替代护城河矩阵 + Job Story 范式 + 出口闸门两问 | Generate 故事动机/优先级时（按需） |
| `references/scenario-5elements.md` | 情景五要素（罗列/标题/描述/痛点快点/功能启发）驱动故事写法 | Generate 故事候选/场景上下文时（按需） |
| `references/user-story-4elements.md` | 用户故事四要素模板（角色/场景/意图/动机）强化结构化写法 | Generate 故事卡片补齐四要素时（按需） |
| `src/shared/clarify/references/scope-negotiation-scripts.md` | In/Out/Deferred/Conditional 的范围谈判脚本 | Clarify 发生范围或优先级取舍时（必查） |

## 产品质量增强（L1 必须）

每个故事要说明用户结果而非功能口号，记录至少一个被排除/延期的替代范围及理由。送审前填写产品质量增强记录，并确保 MoSCoW、In/Out/Deferred/Conditional 的取舍都有来源或业务决策；不能让所有故事默认 Must。

## 完成标准（Completion）

每个已确认旅程痛点/机会都有对应故事卡片；每个故事符合 As a / I want / so that 格式且可测试；MoSCoW 有清晰判定理由；范围基线（In/Out/Deferred/Conditional）有依据；每个故事回溯到旅程节点；故事不重新设计旅程或情绪映射；在启动 `feature-list` 前，获得授权的人类批准了用户故事与范围基线。
