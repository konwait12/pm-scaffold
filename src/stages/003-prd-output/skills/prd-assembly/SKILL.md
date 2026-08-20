---
name: prd-assembly
description: Assemble all confirmed upstream baselines into one traceable PRD without introducing new requirements. Independent work_item, produces prd.md. Applies structured review taxonomy and traceability audit.
---

# PRD 汇总（PRD Assembly）

## 目的与边界（Purpose And Boundary）

通过组织已确认的上游内容、校验跨产物一致性、应用结构化评审分类法、让未决风险可见，产出唯一的最终 `prd.md`。

**不要**：发明、静默解决、概括删减、润色成改变含义、或添加任何新需求。PRD 汇总 = **聚合 + 审计**，不是设计。

## 输入与输出（Inputs And Outputs）

**输入**：按持久化 `00-input/intake-decision.md` 的档位读取已确认上游。L2 为 12 个上游 work_item，按执行顺序：
`background-goal.md` → `user-journey.md` → `user-stories.md` → `feature-list.md` → `functional-flow.md` → `page-design.md` → `interaction-rules.md` → `business-rules.md` → `validation-rules.md` → `state-machine.md` → `exception-handling.md` → `acceptance-criteria.md`

L1 为 7 个上游：`project-background-goal`、`user-journey`、`user-stories`、`feature-list`、`functional-flow`、`business-rules`、`acceptance-criteria`。加上本 work item，L1 共 8 个 work item。核心追溯链：G → ST → FEA → FUN → AC（P0 可交付能力必须可回到目标、故事与可验证验收）。页面、交互、规则、校验、状态、异常是按适用场景连接的横向证据，不是每条需求都必须经过的线性节点。

**输出**：
- `prd.md`（v8 结构，`prd_structure_version: 8`）：10 主干正文节（项目背景 → 项目范围 → 用户旅程 → 用户故事 → 功能清单 → 功能流程 → 原型/UX → 交互规则 → 业务规则 → 验收依据）+ 按需章节（§11：竞品分析/字段规则/埋点/可行性分析/术语表/团队职责）+ 附录（需求追溯矩阵 + 自审记录 + 问题清单[条件]）
- L2 章节与图中 10 个主干产物一一对应；§7 原型/UX ← page-design、§8 交互规则 ← interaction-rules、§9 业务规则以 9.1-9.4 子节分别逐字内嵌 business-rules / validation-rules / state-machine / exception-handling（呈现合并、产物独立）。L1 只生成有确认来源的 §1-§6、§9.1、§10；省略 §7、§8、§9.2-§9.4。五项 L2-only 能力的不适用依据只保留在 intake 决策与 assembly manifest，绝不在 PRD 用泛化 N/A 填充。
- 正向/反向追溯检查、不一致报告、Review taxonomy 结论 → 进 `99-review/` 评审记录，**不写进 prd.md 正文**（由机器在 gate 时产出）

汇总前加载 `references/thinking-framework.md`（→ `thinking-core.md` §1 必用 + §2 检查 + §3 pre-mortem）。审计前加载 `src/shared/audit/review-taxonomy.md`。若上游产出了可点击原型，加载 `references/prototype-embedding.md`（原型嵌入 iframe 切片 + 版本切换器；可选，文本规则仍权威）。

## 工作流（Workflow）

### 1. Preflight
- "所有本档位上游产物都由合法的人工评审记录确认了吗？（L2 完整档=12 个；L1 标准档=7 个：project-background-goal / user-journey / user-stories / feature-list / functional-flow / business-rules / acceptance-criteria）"
- 核验：所有前置产物 `confirmed`，无 simulated/superseded/blocked 基线。
- **只要任一基线缺失或未确认就 STOP**。路由回最早未确认的 Work Item。

### 2. Intake
在不改变知识状态的情况下加载：背景目标（G-XXX）、角色、旅程（UJ-XXX）、故事（ST-XXX）、范围基线、功能（FEA-XXX）、功能流程（FUN/FEA-XXX）、业务规则（BR-XXX）、验收标准（AC-XXX）、决策（DEC-XXX）、假设（ASSUMPTION）、未知（UNK-XXX）。仅 L2 加载页面设计（PD-XXX）、交互规则（IX-XXX）、校验（VL-XXX）、状态转移（STATE-XXX；兼容历史 SM-XXX）与异常（EX-XXX）。

### 3. Think（跨产物分析）
- **正向追溯（Forward trace）**：对 P0 检查 G→ST→FEA→FUN→AC；按需检查 UI、规则、状态、异常的横向链接。每条链接必须有业务依据，不能用格式填充。
- **反向追溯（Reverse trace）**：从 AC、BR、VL、STATE、EX 等条目回看其适用的 FEA/ST/G 或明确 GLOBAL 范围；没有无上游存在理由的元素。
- **一致性检查（Consistency check）**：对比 12 个产物间的术语、范围、优先级、约束、角色、状态与依赖。标记每个不匹配。
- **Pre-Mortem**（thinking-core §2.7）："如果这份 PRD 上线 3 个月后失败，最可能的原因是什么？" → 列出 3-5 个失败场景 → 检查 PRD 是否应对。

### 4. Clarify
- **不要在本 Skill 回答新的业务问题**。
- 记录带证据的不一致。路由回最早受影响的 Work Item。
- 存在实质性不一致时，阻断最终确认。
- 遇到「待确认 / 冲突 / 信息缺口」信号：自动登记带来源的 issue-record `ISS-NNN`（只记录 PM/PRD 问题）；仅对业务决定、owner、接受或关闭动作提问。送审前 dor_check 会硬检查收口与引用。

### 5. Generate
填模板（由 `src/templates/resolver.py prd.md` 解析）。
L2 正文 10 节：项目背景 → 项目范围 → 用户旅程 → 用户故事 → 功能清单 → 功能流程 → 原型/UX → 交互规则 → 业务规则 → 验收依据。L1 正文只保留其七个确认来源对应的 §1-§6、§9.1 和 §10；不得生成 §7、§8 或 §9.2-§9.4，更不得以“本期不适用”替代它们。
按需章节 §11：竞品分析 / 字段规则说明 / 埋点需求分析 / 可行性分析 / 术语表 / 团队职责（上游无内容标「本期不适用」）
附录 3 节：需求追溯矩阵、自审记录（Constitution Compliance）、问题清单（仅 frontmatter `issue_in_prd: true` 时生成）
正向/反向追溯检查与不一致报告**不写进正文**——它们在 Audit 阶段由机器产出、进 99-review 评审记录。
Process Tier 兼容：L1 标准档无 page-design / interaction-rules / validation-rules / state-machine / exception-handling 上游 → §7、§8、§9.2-§9.4 **一律省略**；五项能力的明确不适用事实由 `intake-decision.md` 和 assembly manifest 承载。L2 完整档全 10 节。`validate_artifact.py` 按 `prd_structure_version` + `process_tier` 分叉必含章节，L1 还校验不得混入 L2-only 上游或子节。

### 5.1 状态不变式（仅 L2；蒸馏 A2 prd-development）

L2 中，每个被记录的字段（含 BR / VL / STATE / EX 字段）必须写出：
- 字段的**状态枚举**（如 `enabled/disabled`）
- 状态间的**转移条件**（事件 + 守卫）

这些内容分别由 `business-rules`、`state-machine`、`exception-handling` 上游产物承载，并逐字装配。L1 不存在 `state-machine` 上游，故不得在 §9.1 以表格、枚举或文字补写状态模型；一旦需求需要状态枚举、状态转移、触发事件与守卫条件，必须在 `intake-decision.md` 记录适用性并升级为 L2。普通业务条件（例如时间阈值）仍属于 L1 的 `business-rules` 范围。

### 6. Audit（应用评审分类法）
按顺序运行：
1. `scripts/validate_artifact.py <prd> --json` → 结构校验
2. `src/scripts/traceability_check.py <REQ-DIR> --json` → 显式边审计
3. `src/scripts/branch_validator.py <REQ-DIR> --json` → 共享记录校验
4. **评审分类法扫描**（应用 `src/shared/audit/review-taxonomy.md`）：
   - 扫描 [Contradiction]：跨章节逻辑冲突
   - 扫描 [Gap]：缺失关键信息
   - 扫描 [Fallacy]：错误前提
   - 扫描 [Redundancy]：重复内容
   - 扫描 [Dangling]：断裂的引用
   - 扫描 [Overreach]：范围外的实现细节
   - 扫描 [Unowned]：未分配的责任
   - 对每条发现 → 裁定：APPROVED / CONDITIONS / REVISION
   - **发现进 99-review 评审记录，不写进 prd.md 正文**
5. 对抗性审视（thinking-core §1.3）："我能构造一个让这份 PRD 导向错误产品的场景吗？"
6. **B3 收口**：本 Skill 仅用于 L1/L2；两档均须确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。L0 使用 mini-prd，不进入本汇总链。
- 对 PRD 中的 FACT 与关键 DECISION 执行四维证据检查（来源、规模、匹配、方向），见 `src/shared/audit/evidence-four-dimension-check.md`；无法通过的项必须进入审计问题而不是写成确定性结论。

任何断裂的关系、未经批准的添加或 REVISION 级发现 → 闸门失败。

### 7. Human Gate
呈现给授权的最终批准人：
- PRD
- 追溯报告（正向 + 反向、边计数、孤儿检测）
- 不一致报告（带 [Contradiction]/[Gap] 等标签）
- 未决风险（已变得实质性的 UNK-XXX）
- 上游 delta（自上次汇总以来的变更）
- 评审分类法发现与裁定

**禁止自动批准与模拟批准。** 只有来自 `00-input/authorized-reviewers.json` 的授权人工评审人可以批准。

### 8. Commit / Reflow
- 批准时 → `prd.md` 变为 `confirmed`，带 SHA-256 绑定。
- 拒绝时 → 写 reflow 记录 → 返回最早受影响的 Work Item → 重建 PRD。
- CONDITIONS 时 → 带条件清单批准 → 下游标记为 `conditional_review`。

## 评审分类法速查（Review Taxonomy Quick Reference）

来自 `src/shared/audit/review-taxonomy.md`：

| 标签 | 在 PRD 中找什么 |
|---|---|
| [Contradiction] | 两个章节说相反的事 |
| [Gap] | 缺失阻断实现的信息 |
| [Fallacy] | 基于错误假设的主张 |
| [Redundancy] | 同一信息在 >1 处出现，可能漂移 |
| [Dangling] | 引用不存在的 ST/FEA/BR |
| [Overreach] | PRD 指定实现细节 |
| [Unowned] | 某个决策无人类负责人 |

## 反模式（Anti-Patterns）

| ❌ 不要 | ✅ 要做 |
|---|---|
| 在汇总阶段添加一个"锦上添花"功能 | 把想法路由回 project-background-goal |
| 静默修复不一致的术语 | 在评审记录中标为 [Redundancy] 或 [Contradiction] |
| 因为"很明显"就跳过追溯 | 运行 traceability_check.py——它能找出不明显的孤儿 |
| 带着未决的 CRITICAL [Gap] 批准 | 用 REVISION 裁定阻断 |
| 不运行 traceability_check 就生成 PRD | 始终运行显式边审计 |

## 加载参考文档（Load References）

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/prd-structure-reference.md` | PRD 结构参考（章节组织方法论） | Generate 前 |
| `references/prototype-embedding.md` | PRD 原型嵌入技法（上游有原型时用） | 上游有原型时 |
| `src/shared/audit/evidence-four-dimension-check.md` | 聚合后事实与决策的证据质量检查 | Audit 与 Human Gate 前（必查） |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |
| `references/prd-scoring-rubric.md` | PRD 评分卡（10 分制，advisory 参考工具） | Human Gate 前自检（按需，advisory） |
| `references/review-engine-5step.md` | 统一评分引擎 5 步流水线（fetch/inspect/deep_check/scoring/decision + 按来源切换规则集） | Human Gate 前结构化自评（按需，advisory） |
| `references/downstream-handoff.md` | 下游交接三视角（设计/研发/测试各自先看/产出/缺口）+ 产品边界红线 | Generate 附录/交接清单时（按需） |
| `references/structure-9q.md` | PRD 结构 9 问最小判断 + 章节职责路由 | Generate 前后结构自查（按需） |
| `references/grill-me.md` | 对抗复审（签发前人工一道 + 四阶段 grill + 结构/一致性/幻觉三维自检） | Human Gate 前对抗复审时（按需） |
| `references/iteration-pattern.md` | 迭代双 case 变更文档（有基线 delta / 无基线自包含 + chg 日志块） | 收到增量变更需生成变更记录时（按需） |
| `references/adr-and-sourcing.md` | ADR 内联模板 + Sourcing 6 级标注 + Handoff Context + 决策预注册四象限 + 坏消息公式 | Intake 来源登记 / Human Gate 沟通时（按需） |
| `references/competitor-three-state.md` | 竞品矩阵三态（行选择即分析，权重/出处/结论列） | 范围取舍需竞品依据时（按需） |
| `references/domain-mapping-hint.md` | PRD 信号→领域候选映射提示（仅交接提示，不做 DDD 设计） | 下游研发开始领域建模时（按需） |
| `references/ddd-design-guide.md` | DDD 设计 7 阶段交接提示（事件风暴→行为建模，含贫血模型检查，advisory） | 研发开始 DDD 设计时（按需，蒸馏 E2） |
| `references/incre-prd-checklist.md` | 增量 PRD 高频遗漏检查（文案、阻断/降级、时间窗与回滚依据） | 增量需求或局部改动汇总前（按需） |
| `src/shared/audit/red-team-naysayer.md` | 红队压力测试（10 铁律 + 三阶段 + 合理化借口对照，advisory 只提问） | Human Gate 前作者自查/评审人选用（按需，蒸馏 G1） |

## 完成标准（Completion）

所有本档位上游基线合法且已确认；L2 每条必需的 G→UJ→US→ST→FEA→FL→PD→IX→BR→VL→SM→EX→AC 关系显式，L1 则验证其实际链 G→ST→FEA→FUN→BR→AC；没有引入新需求；评审分类法发现已带裁定记录；风险与冲突可见；机器检查（校验器 + 追溯 + branch）通过；且授权的人类显式批准 `prd.md`。
