# 新批次 PRD/PM Skill 择优整合实施计划（v1）

> 本计划针对 2026-08-18 13:32–13:34 新下载的 35 个 PRD/PM 类 Skill（与上一轮 scene#18 已整合的 13 个区分）。
> 目标：系统评估、择优、零改动三档注入 pm 脚手架（to B 偏向）。所有有价值能力点**一个不漏**映射到脚手架接入点。

---

## 1. 背景与范围

- **上一轮已整合 13 skill**（已注入精华，勿重复）：prd-fullstack、prd-generator、prd-writer、prd-writing-expert、prd-reviewer、prd-to-design-doc、prd-to-prototype、PRD to Prototype、prd-skill、prd、prd-development、prd-review-design、product-design-0to1。
- **本轮新批次 35 skill**（位于 `~/.workbuddy/skills/`，2026-08-18 13:32–13:34 下载）。
- **脚手架硬边界**：PRD-only，不做研发拆分/技术架构/测试用例/API 合约/用户手册；唯一交付物 `prd.md`。
- **吸收通道（零改动三档）**：
  - **A 档 思想层** = `src/framework/thinking-core.md` 的 §2 检查透镜 / §3 pre-mortem 透镜 / §5 表达层技法注册表
  - **B 档 参考文档层** = 各 skill 的 `references/*.md` 技法文件（SKILL.md「加载参考」表登记）
  - **C 档 审计层** = `src/shared/audit/review-taxonomy.md` 标签 + 各 skill 的 `references/audit-checklist.md`
- **红线**：不碰 `workflow-registry.json` / SKILL.md 主干 8 步 / 模板 frontmatter / `validate_artifact.py` AST。

---

## 2. 评估方法与维度

对每个 skill 逐一深读 SKILL.md 全文及核心 references，按 8 维度评估：

| 维度 | 判定要点 |
|---|---|
| 功能价值 | 是否填补脚手架现有能力缺口 |
| 实用性 | 能力点是否可落地为产物技法/透镜/审计项 |
| 稳定性 | 方法论是否经得起 to B 场景检验 |
| 与脚手架兼容性 | 是否符合 PRD-only 边界与三档吸收通道 |
| 学习成本 | 接入后是否需要主干改动或大量新概念 |
| 可维护性 | 技法文件是否自包含、可独立演进 |
| to B 契合度 | 原生适配 / 需轻量适配 / 不适用 |
| 与上一轮重复 | 是否含上一轮未吸收的新内容 |

处置分级：**整合**（多能力点全档接入）/ **部分吸收**（取若干能力点）/ **不整合**（超范围或重复无新内容）。

---

## 3. 全量评估表（35 个）

| # | Skill 目录 | 定位 | 丰厚度 | 契合度 | 重复上一轮 | to B | 处置 |
|---|---|---|---|---|---|---|---|
| 1 | juloko | 调研素材→框架性 PRD | 丰厚 | 高 | 否 | 原生 | 整合 |
| 2 | product-spec-generator | 受控 PRD 生成器+grill 自检 | 丰厚 | 高 | 否 | 原生 | 整合 |
| 3 | incremental-prd-collaboration | 渐进式 PRD+评分引擎 | 丰厚 | 高 | 否 | 原生 | 整合 |
| 4 | product-solution-evaluator | 方案评估专家 | 丰厚 | 高 | 否 | 原生 | 整合 |
| 5 | prd-competitor-check | PRD 竞品对标校验 v4 | 丰厚 | 高 | 否 | 原生 | 整合 |
| 6 | pm888 | B 端产品专家 5 角色/5Phase | 丰厚 | 高 | 部分 | 原生 | 整合 |
| 7 | pm-master-prosl | 研发评审版 PRD 硬标准 | 丰厚 | 高 | 部分 | 原生 | 整合 |
| 8 | product-copywriting | UI 文案专家 | 中等 | 高 | 否 | 原生 | 整合 |
| 9 | daedalus-skill | 对话式产品孵化 | 中等 | 中 | 否 | 轻量 | 部分吸收 |
| 10 | mimo-prd-generator | 6 步 PRD+RICE | 骨架 | 低 | 是(含1新点) | 轻量 | 部分吸收 |
| 11 | prd-generator-cc | 轻量 PRD 三模式 | 骨架 | 中 | 是(含2新点) | 轻量 | 部分吸收 |
| 12 | prd-writter | 北极星+AI 项目增强 | 中等 | 中 | 是(含3新点) | 原生 | 部分吸收 |
| 13 | prd-to-ddd-design | PRD→DDD 领域设计 | 丰厚 | 超范围 | 否 | 原生 | 部分吸收(仅交接提示) |
| 14 | product-researching | chanpin 六维产品分析 | 丰厚 | 中 | 否 | 轻量 | 部分吸收 |
| 15 | producrequirementanalyzer | 心理需求四维映射 | 丰厚 | 中 | 部分 | 轻量 | 部分吸收 |
| 16 | product-positioning-master | ST×SWOT+定位三角 | 中等 | 中 | 否 | 原生 | 部分吸收 |
| 17 | product-manager-senior-engineer | PM×RDM 双职能+22 表 | 丰厚 | 低-中 | 否 | 原生 | 部分吸收 |
| 18 | pmskills | 网龙 PDM 方法论 | 中等 | 中 | 部分 | 轻量 | 部分吸收 |
| 19 | pmaster | 40+框架全栈工具箱 | 丰厚 | 中 | 部分 | 轻量 | 部分吸收 |
| 20 | pm-chief-naysayer | 逻辑压力测试 3 阶段 | 丰厚 | 高(透镜) | 否 | 原生 | 部分吸收 |
| 21 | pm-cognition-coach | PM 认知跃迁教练 | 丰厚 | 低(仅透镜) | 否 | 不适用 | 部分吸收(仅透镜) |
| 22 | product-planning-assistant | 产品规划 5 步法 | 中等 | 中 | 部分 | 原生 | 部分吸收 |
| 23 | arch-diagram-pro | 架构图 HTML 生成器 | 丰厚 | 低-中 | 否 | 原生 | 部分吸收(产品图技法) |
| 24 | prd-writer-new-plus | 简版 PRD 9 章 | 中等 | 低 | 是(重复) | 轻量 | 不整合 |
| 25 | pm-prd-workflow | 需求→Demo/Word 工作流 | 骨架 | 低 | 是(重复) | 轻量 | 不整合 |
| 26 | prd-skill-workflow2 | prd-fullstack 变体 | 丰厚 | 超范围 | 是(重复) | 原生 | 不整合 |
| 27 | prd-skill2026 | prd.json 面向研发执行 | 骨架 | 超范围 | 是(重复) | 不适用 | 不整合 |
| 28 | prd-skill202603 | 同 2026 变体 | 骨架 | 超范围 | 是(重复) | 不适用 | 不整合 |
| 29 | prd-skill20260303 | prd-2 变体 | 骨架 | 超范围 | 是(重复) | 不适用 | 不整合 |
| 30 | prd-skill2026030303 | 同上变体 | 骨架 | 超范围 | 是(重复) | 不适用 | 不整合 |
| 31 | product-analysis-zh | 5 维度产品审查 | 骨架 | 低 | 否 | 不适用 | 不整合 |
| 32 | product-manager-ai | PM 视角综合 | 中等 | 低 | 是(重复) | 轻量 | 不整合 |
| 33 | pmproducer | PM 求职辅导 | 骨架 | 超范围 | 否 | 不适用 | 不整合 |
| 34 | product-cost-analyzer | 实体成本核算 | 骨架 | 超范围 | 否 | 不适用 | 不整合 |
| 35 | linkfox-product-title-analyze | 亚马逊 Listing 分词 | 中等 | 超范围 | 否 | 不适用 | 不整合 |

**汇总：整合 8 个、部分吸收 15 个、不整合 12 个。**

---

## 4. 能力点 → 脚手架接入点映射总表

> 经与上一轮 13 个已注入精华去重后的**净增能力点**。每条对应一个新建技法文件/透镜登记/审计标签，**一个不漏**。

### 4.1 A 档：思想层（thinking-core 透镜/技法登记）

| 编号 | 透镜/技法 | 核心内容 | 来源 skill | 注入位置 |
|---|---|---|---|---|
| A1 | 业务语言透镜 | 问题措辞 5 铁律：业务语言/给选项/先说影响/一次一类/追问为什么 | juloko | thinking-core §2 |
| A2 | 证据追溯透镜 | deep_check 纪律：只输出问题+严重度+证据，禁止输出建议 | incremental-prd-collaboration | thinking-core §2 |
| A3 | 成本门禁透镜 | 高消耗操作（如 stage2 对标）须用户明确确认才执行 | prd-competitor-check | thinking-core §2 |
| A4 | 置信度标注透镜 | 每条结论标置信度 3 级（高/中/低） | product-solution-evaluator | thinking-core §2 |
| A5 | 事实假设判断三态透镜 | 区分事实/假设/判断，不混写 | pm-master-prosl | thinking-core §2 |
| A6 | 出口闸门两问透镜 | 每条需求问：会误导吗？何时失效？ | producrequirementanalyzer | thinking-core §2 |
| A7 | grill 对抗透镜 | section-grill 四阶段：静默重读→负载分级🔴🟡🟢风险挖掘→逐项 grill→判定 PASS/待澄清/冲突 | product-spec-generator | thinking-core §3 |
| A8 | 反例扫描透镜 | 15 类反例库（伪需求/无场景/指标不闭环/AI 为了 AI/成本倒挂/依赖不可控/合规红线/解决方案先行/大而全平台/体验口号/数据不可得/运营缺位/边界不清/无验证路径/责任不清） | product-solution-evaluator | thinking-core §3 |
| A9 | 预死亡分析透镜 | 老虎/纸老虎/大象分类 + 紧迫 3 级（发布阻断/快速跟进/持续跟踪） | pmaster | thinking-core §3 |
| A10 | 假设验证 4 维透镜 | 价值/可用性/商业可行/技术可行 四维验证 | pmaster | thinking-core §3 |
| A11 | naysayer 3 阶段透镜 | 基础第一性原理→真相证据审问→修剪奥卡姆 + 命题漂移检测 + 4 维证据可信度（来源/规模/匹配/方向矛盾）+ 副作用检查 | pm-chief-naysayer | thinking-core §3 |
| A12 | 决策预注册四象限透镜 | 技能/方差/运气/学费 四象限复盘 | pm888 | thinking-core §3 |
| A13 | 西瓜防御透镜 | 状态预测非情绪，🟢🟡🔴+具名风险 | pm888 | thinking-core §3 |
| A14 | 二阶效应透镜 | 分析方案的二阶连锁后果 | pm888 | thinking-core §3 |
| A15 | 溯源标注技法 | 【推测】/【待确认】/「需专业确认」三级标注（撰写期） | prd-generator-cc | thinking-core §5 |
| A16 | 反合理化技法 | 6 项 Anti-rationalization 借口表（借口→正确做法） | mimo-prd-generator | thinking-core §5 |
| A17 | 独立成文技法 | 综合成文不写"如维度 X 所述"等承接语言 | product-researching | thinking-core §5 |
| A18 | 认知透镜（附录） | 产品四层结构（功能/平台生态/规则体系/组织系统）+ 苏格拉底 5 提问（假设检验/视角切换/边界探索/本质追问/行动锚定） | pm-cognition-coach | thinking-core §5 附录 |

### 4.2 B 档：参考文档层（各 skill references 技法文件）

| 编号 | 技法文件 | 核心内容 | 来源 skill | 接入 skill |
|---|---|---|---|---|
| B1 | gap-checklist-14d.md | 14 维度缺口扫描：角色权限/流程完整性/规则边界/状态机/数据字段/集成/存量迁移/性能/合规/异常/报表/审计/术语/验收 | juloko | requirement-restate |
| B2 | fact-ledger.md | 事实台账五分型 F/D/A/W/O（事实/决议/假设/诉求/意见）+ 三色标注✅⚠️❌ + 覆盖度徽标 | juloko | requirement-restate |
| B3 | interview-synthesis.md | 访谈五步提炼：目标/角色/场景/功能点/规则风险 | incremental-prd-collaboration | requirement-restate |
| B4 | compliance-keywords.md | 6 类合规风险关键词库：位置追踪/UGC/匿名/金融/健康/未成年人/境外地图 | daedalus-skill | brainstorming |
| B5 | v1-boundary.md | V1≤3 + 边界三分类：必须有/延后/不做 | daedalus-skill | brainstorming |
| B6 | mode-dispatch.md | 三模式快速分流：起草/评审/解释（按用户意图切换输出形态） | prd-generator-cc | brainstorming |
| B7 | scoring-7d.md | 7 维度 100 分制评分模型（用户问题 20%+方案闭环 15%+市场重复性 15%+商业 ROI 20%+可交付 10%+风险合规 10%+验证质量 10%） | product-solution-evaluator | feasibility-analysis |
| B8 | idea-filtering.md | Idea Filtering 6 类替代方案（直接竞品/间接替代/平台内置/开源/垂直/大厂生态）+ Build/Buy/Partner/Integrate/Abandon 五路径 | product-solution-evaluator | feasibility-analysis |
| B9 | ai-product-check.md | AI 产品专项 6 检查 | product-solution-evaluator | feasibility-analysis |
| B10 | review-threshold-7d.md | 研发评审 7 维度可行性门槛（产品/技术/数据/体验/研发拆解/风险/验收） | product-solution-evaluator | feasibility-analysis |
| B11 | threshold-tier.md | 轻量/中等/完整三档门槛（成本 <500/几千/万元以上） | daedalus-skill | feasibility-analysis |
| B12 | rtm-and-market-sizing.md | 需求追溯矩阵 RTM + TAM/SAM/SOM 市场分析表 + PM-T1~T8 产品管理表格 | product-manager-senior-engineer | feasibility-analysis |
| B13 | two-stage-check.md | 两阶段对标流程：stage1 原型/设计对标默认执行；stage2 业务逻辑校验需用户确认（省 60% token） | prd-competitor-check | competitive-research |
| B14 | competitor-refs-pattern.md | 竞品参考库四字段结构：主链接+alt_urls+search_keywords+screenshot | prd-competitor-check | competitive-research |
| B15 | link-validation.md | 链接验证三层降级（主链接→alt_urls→search_keywords） | prd-competitor-check | competitive-research |
| B16 | synthesis-craft.md | 综合分析 5 段式（六维速读/设计逻辑/增长壁垒/演进推演/犀利洞察）+ 犀利洞察"被点醒"标准 | product-researching | competitive-research |
| B17 | competitor-teardown.md | 竞品拆解 3 法（菜单/流程/重要操作）+ 竞品 3 类分类 | pmskills | competitive-research |
| B18 | positioning-stxswot.md | ST×SWOT 交叉复合矩阵 + 定位声明模板（目标客户/品类/差异化价值/价值承诺/信任状） | product-positioning-master | project-background-goal |
| B19 | stakeholder-power-interest.md | 干系人权力×利益方格 | pmaster | project-background-goal |
| B20 | stakeholder-4class.md | 干系人 4 类分类（出资方/权力部门/客户/合作方）+ 高/中/低优先级 | pmskills | project-background-goal |
| B21 | planning-report.md | 对齐汇报 4 要素（业务价值量化/投入产出/资源需求/决策事项）+ 风险预案表结构 | product-planning-assistant | project-background-goal |
| B22 | job-story-and-moat.md | JTBD 三层 + 竞争替代护城河矩阵 + Job Story 范式 | producrequirementanalyzer | user-stories |
| B23 | scenario-5elements.md | 情景五要素（罗列要素/情景标题/情景描述/痛点和快点/功能启发） | pmskills | user-stories |
| B24 | rule-decision-table.md | 规则决策表完备性 6 项检查（组合穷尽/规则冲突/空规则/边界归属/默认动作/优先级消解） | juloko | business-rules |
| B25 | ai-task-types.md | AI 任务类型 6 分类（分类/抽取/生成/推理/RAG/Agent） | prd-writter | business-rules |
| B26 | tob-dimension-matcher.md | ToB 维度库四类映射（内部后台/管理后台/数据看板/表单流程 → RBAC/多租户/审批流/审计） | product-spec-generator | page-design |
| B27 | ui-copywriting-rules.md | UI 文案 5 原则 + 9 场景检查清单（错误异常/表单输入/按钮/弹窗/空状态/加载/成功反馈/权限请求/破坏性操作确认）+ 每场景❌✅对照 | product-copywriting | interaction-rules（+page-design） |
| B28 | high-freq-missing-10.md | 高频遗漏 10 项（页面标题/副标题/主按钮文案/倒计时/输入限制/可点击条件/成功失败异常状态/自动处理 vs 强拦截/账号限制与会话有效性/阻断文案与报错文案） | incremental-prd-collaboration | page-design（+interaction-rules） |
| B29 | architecture-diagram-craft.md | 模块组成图分区结构（标题带→特征徽章→模块卡片网格→流程带→指标区）+ 产品全景图布局思路 + 信息密度原则 | arch-diagram-pro | page-design（+prd-assembly） |
| B30 | cross-ref-check.md | 字段三元组一致性（定义/使用/枚举三处对齐）+ 引用完整性（BR/AC/E/FR 交叉引用悬空检查）+ 状态机三元一致性（状态机↔异常↔规则） | product-spec-generator | validation-rules |
| B31 | ai-fallback.md | AI 兜底 4 类（格式异常/低置信/幻觉/安全合规） | prd-writter | exception-handling |
| B32 | ai-eval-dimensions.md | AI 模型评估 4 维度（准确性/完整性/稳定性/幻觉率） | prd-writter | acceptance-criteria |
| B33 | review-engine-5step.md | 统一评分引擎 5 步流水线（fetch/inspect/deep_check/scoring/decision）+ 三类评分规则集（AI PRD/公司需求/混合） | incremental-prd-collaboration | prd-assembly |
| B34 | downstream-handoff.md | 下游交接三视角（设计/研发/测试各看"先看什么/产出什么/缺什么"） | incremental-prd-collaboration | prd-assembly |
| B35 | structure-9q.md | PRD 结构 9 问最小判断 | incremental-prd-collaboration | prd-assembly |
| B36 | grill-me.md | grill-me 人工一道（受控触发，签发前业务层复审） | product-spec-generator | prd-assembly |
| B37 | iteration-pattern.md | iteration 双 case（有基线 delta / 无基线自包含） | product-spec-generator | prd-assembly |
| B38 | adr-and-sourcing.md | ADR 内联模板 + Sourcing Rules 6 级标注（事实/输入/模型知识/推断/假设/禁编造）+ Handoff Context 机器可读契约 | pm888 | prd-assembly |
| B39 | competitor-three-state.md | 行选择就是分析：竞品矩阵三态✅🟡❌ + 权重列 deal-breaker + 出处 | pm888 | prd-assembly（+competitive-research） |
| B40 | domain-mapping-hint.md | PRD 信号→领域候选映射表（Nouns→Entity/VO，Verbs→Event/Command，"Must"→Invariant，Closed set→Enum）——仅作交接提示，不做完整 DDD | prd-to-ddd-design | prd-assembly |
| B41 | dev-review-prd-standard-13.md | 研发评审版 PRD 硬标准 13 项（版本/目标/北极星+过程+反向指标/角色场景任务流/组件级需求/任务配置表/状态机/主路径+分支+异常+空状态+权限流程/埋点字段/接口配置建议/异常降级安全边界/验收用例/结果交付路径） | pm-master-prosl | feature-list（跨 002） |
| B42 | north-star-and-good-metric.md | 北极星指标框架 + 好指标 4 标准（易理解/可比较/是比率/能改变行为）+ AARRR 海盗指标 | pmaster | tracking-plan |

### 4.3 C 档：审计层（review-taxonomy 标签 + audit-checklist 追加）

| 编号 | 审计项 | 核心内容 | 来源 skill | 注入位置 |
|---|---|---|---|---|
| C1 | 标签 `[HarddownRule]` | 硬性降级 9 条 | product-solution-evaluator | review-taxonomy.md |
| C2 | 标签 `[P0P1P2Misgraded]` | P0/P1/P2 优先级定级错误 | product-spec-generator | review-taxonomy.md |
| C3 | 标签 `[QualityGate]` | 三道质量门（Q-Gate 启动→执行→交付） | product-manager-senior-engineer | review-taxonomy.md |
| C4 | 标签 `[ScoreMatrix]` | 0-40 评分 4 维矩阵（问题接地/需求可测/指标严谨/范围风险诚实） | pm888 | review-taxonomy.md |
| C5 | 标签 `[AntiPattern]` | 反模式 24 条（pm888）+ 反模式 8 条（pm-master-prosl：老板意见直写需求/只写功能不写用户价值/PRD 背景模糊/验收不可测试/只写正常不写异常/优先级伪精确/指标只看增长/发布说明只写技术） | pm888 + pm-master-prosl | review-taxonomy.md |
| C6 | prd-assembly audit-checklist 追加 | grill 对抗自检 + 下游交接三视角 + ADR 追溯 + 0-40 评分 + 研发评审版 13 项 | pm888/incremental/product-spec | audit-checklist §6 扩展 |
| C7 | interaction-rules audit-checklist 追加 | UI 文案最终自检 5 问 + 高频遗漏 10 项 | product-copywriting/incremental | audit-checklist 追加 |
| C8 | acceptance-criteria audit-checklist 追加 | AI 模型评估 4 维度 + 字段三元组一致性 | prd-writter/product-spec | audit-checklist 追加 |
| C9 | feasibility-analysis audit-checklist 追加 | 7 维度评分 + 15 类反例 + 硬性降级 9 条 + AI 专项 6 检查 | product-solution-evaluator | audit-checklist 追加 |

> **小计**：A 档 18 项透镜/技法 + B 档 42 个技法文件 + C 档 9 项审计扩展 = **69 个注入点**（含上一轮已建通道复用）。

---

## 5. 实施里程碑（M1–M6）

> 每个 milestone 完成后跑 `run_tests_mac.sh` + `consistency_check.py` + 悬空引用扫描，确认 84 passed / 0 failed、0 errors。

| 里程碑 | 范围 | 注入点 | 风险 | 产出 |
|---|---|---|---|---|
| **M1 思想层** | thinking-core §2/§3/§5 新增 18 透镜/技法登记 | A1–A18 | 低（纯文档） | thinking-core.md 更新 + workflow.md 同步引用 |
| **M2 调研与评估层** | requirement-restate/brainstorming/feasibility-analysis/competitive-research/project-background-goal/user-stories 的 B 档技法 | B1–B23 | 低 | 23 个 references + 6 SKILL.md 加载表登记 |
| **M3 产品需求层** | business-rules/page-design/interaction-rules/validation-rules/exception-handling/acceptance-criteria 的 B 档技法 | B24–B32 | 低 | 9 个 references + 6 SKILL.md 登记 |
| **M4 汇总交接层** | prd-assembly/feature-list/tracking-plan 的 B 档技法 | B33–B42 | 中（prd-assembly 文档量大） | 10 个 references + 3 SKILL.md 登记 |
| **M5 审计层** | review-taxonomy 新标签 + 各 audit-checklist 追加 | C1–C9 | 低 | review-taxonomy 更新 + 4 checklist 追加 |
| **M6 验证收口** | 全量回归 + 注册登记核对 + 悬空引用清零 | — | — | QA 报告 |

### 5.1 各 milestone 执行步骤（以 M1 为模板，其余同构）

1. Read 目标文件当前状态（thinking-core.md §2/§3/§5 区域）
2. Edit 追加透镜/技法登记（每条一行核心问题，避免膨胀）
3. workflow.md 条件支持章节同步「新批次技法」引用
4. 跑 `run_tests_mac.sh` + `consistency_check.py`
5. 悬空引用扫描（确认新登记路径指向真实文件——M1 为 §5 登记，路径在 M2-M4 创建后才有文件，故 M1 仅登记不验证路径；M4 完成后统一验证）
6. 更新工作日志

---

## 6. 优先级排序

1. **P0（必做，M1–M5）**：当前 95 个已登记注入点。理由：用户明确"任何有价值能力不得遗漏/删减"；实际数量以各 SKILL.md 加载表和审计报告为准。
2. **M1 优先于 M2–M5**：思想层透镜是技法运用的前提，先建思考框架再填技法。
3. **M2 优先于 M3/M4**：调研评估层在上游，技法先于产物技法。
4. **M5 在 M2–M4 之后**：审计标签引用技法产物，需技法先就位。
5. **M6 最后**：全量验证。

---

## 7. 时间安排

| 里程碑 | 预估工作量 | 依赖 |
|---|---|---|
| M1 思想层 | 0.5 天 | 无 |
| M2 调研评估层 | 1 天 | M1 |
| M3 产品需求层 | 0.5 天 | M1 |
| M4 汇总交接层 | 1 天 | M1 |
| M5 审计层 | 0.5 天 | M2–M4 |
| M6 验证收口 | 0.5 天 | M1–M5 |
| **合计** | **约 4 天**（可压缩并行至 2.5–3 天） | |

> M2/M3/M4 在 M1 完成后可并行（不同 skill 目录互不冲突）。

---

## 8. 资源需求

- **执行人**：1 名（本 Agent）
- **源材料**：35 个新批次 skill 全文（评估阶段已深读完毕，能力点已提取）
- **目标仓库**：pm 脚手架（`src/framework/` + `src/stages/` + `src/support-skills/` + `src/shared/`）
- **验证工具**：`run_tests_mac.sh`、`consistency_check.py`、悬空引用扫描脚本
- **无需**：主干代码改动、新依赖、外部服务

---

## 9. 风险与应对措施

| 风险 | 等级 | 应对 |
|---|---|---|
| thinking-core 透镜膨胀（§2/§3 新增 11 透镜） | 中 | 每透镜一行核心问题 + 触发时机；§5 技法按需加载不设全局闸门；§1 强制 6 透镜不变 |
| references 文件达 42 个，登记易遗漏 | 中 | 每 milestone 末跑悬空引用扫描 + SKILL.md 加载表登记核对（脚本化） |
| 与上一轮 13 个已注入精华重复 | 中 | 评估阶段已逐条去重；实施时每条映射前再比对（上一轮已注入清单见 §1） |
| E3_drift 触发 | 高 | 坚持零改动三档：不碰 registry/主干 8 步/frontmatter/AST；每 milestone 跑 registry_contract_check |
| 内容过薄（上一轮用户已批评） | 中 | 每个 references 搬入原 skill 完整模板/字段表/示例/规则，~100–170 行，非骨架 |
| 新技法标签与既有知识状态 6 标签冲突 | 低 | 仅用 FACT/DECISION/ASSUMPTION/AI_INFERENCE/UNKNOWN/CONFLICT；新审计标签走 review-taxonomy 不走知识状态 |
| prd-assembly 文档量过大 | 低 | B33–B42 拆为 8 个独立 references，不堆进单一文件 |

---

## 10. 验证标准

每个 milestone 与最终收口须满足：

1. `run_tests_mac.sh` ≥ 84 passed / 0 failed（含 registry_contract_check E3_drift 关卡）
2. `consistency_check.py` 0 errors / 0 warnings
3. 悬空引用扫描清零（所有 SKILL.md 登记的 references 路径指向真实文件）
4. 新建 references 全部在对应 SKILL.md「加载参考」表登记
5. thinking-core §5 登记的技法路径全部存在
6. 知识状态标签仅用 6 标准，无发明新标签
7. 红线零触碰：workflow-registry.json / SKILL.md 主干 8 步 / 模板 frontmatter / validate_artifact.py AST 未改
8. 内容丰厚度：每 references 文件 ≥80 行，含原 skill 模板/示例/规则

---

## 11. 不整合清单与理由（12 个）

| Skill | 理由 |
|---|---|
| prd-writer-new-plus | 重复变体，9 章模板与 8 项自检已被上一轮评分卡/写作四原则覆盖，无新内容 |
| pm-prd-workflow | Demo/Word 导出超 PRD-only 边界；需求列表 P0-P3 已被 feature-list 覆盖 |
| prd-skill-workflow2 | prd-fullstack 重复变体；14 章中 5 章（数据模型/技术方案/测试/运营/项目计划）超边界 |
| prd-skill2026 / 202603 / 20260303 / 2026030303 | prd.json 格式面向 AI agent 研发执行（涉及 schema/migration/backend），超 PRD-only 边界；4 个互为版本号变体，无新内容 |
| product-analysis-zh | 骨架文件（1.4KB）仅罗列维度名称，无可落地方法论；API/架构维度超边界 |
| product-manager-ai | 与上一轮 prd-generator/prd-writer 完全重叠且更浅，6 个 references 无独特方法论 |
| pmproducer | 纯 PM 求职辅导（JD/简历/模拟面试），与 PRD 产物完全无关 |
| product-cost-analyzer | 实体产品成本核算（原料/包装/制造费用），脚手架是软件 PRD-only |
| linkfox-product-title-analyze | 亚马逊 Listing 分词工具，依赖外部 API 与积分，与软件 PRD 无关 |

---

## 12. 里程碑检查清单

- [ ] M1：thinking-core §2 +6 透镜、§3 +6 透镜、§5 +6 技法登记 + 附录认知透镜；workflow.md 同步
- [ ] M2：23 个 references（B1–B23）创建 + 6 SKILL.md 加载表登记
- [ ] M3：9 个 references（B24–B32）创建 + 6 SKILL.md 登记
- [ ] M4：10 个 references（B33–B42）创建 + 3 SKILL.md 登记
- [ ] M5：review-taxonomy +5 标签（C1–C5）+ 4 audit-checklist 追加（C6–C9）
- [ ] M6：84 passed / 0 failed、0 errors、悬空引用清零、登记完整、红线零触碰
- [ ] 工作日志与 MEMORY 更新

---

## 13. 启动确认

本计划已就绪，可直接从 **M1 思想层** 推进。一句话即可启动执行（如"按计划推进"或"开始 M1"）。
执行中如发现某能力点与既有技法高度重叠，会标注并保留为"补充说明"而非丢弃，确保内容量不减少。
