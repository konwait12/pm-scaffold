# Thinking Core · 通用思想引导核心层

> 本文件是所有 Work Item Skill（13 主干 + 3 分支 + 1 常驻 + 2 能力 = 19）**共享的通用思想引导层**。
> 各 Skill 的 `references/thinking-framework.md` 必须引用本文件并遵守本文件的使用协议。
> 与 `src/framework/workflow.md`（通用执行循环）一致；本文件是 AI 运行时权威。
> 变更顺序：先改本文件 → 再同步 `src/framework/workflow.md` → 再同步各 Skill 的 `thinking-framework.md` 引用。

## 使用协议（AI 必读，违反即工作流缺陷）

1. **循环强制（最高优先级）**：每个 Work Item（含 13 个主干项与分支/常驻/能力项）都必须完整走一遍 `Preflight → Intake → Think → Clarify → Generate → Audit → Human Gate → Commit / Reflow`（见 `src/framework/workflow.md`）。**没有任何产物可以绕过人工确认进入下游**——PRD 汇总产物同样必须人工确认后才能交付。机器校验只能产生 `ready_for_human_review`，不能产生 `confirmed`。
2. **三件套**：每个 lens 必须按"触发时机 → 核心问题（≤3 个）→ 产出落点"使用，禁止只读不产出。
3. **分层使用**：通用核心层（本文件 §1）每个 Work Item 必用；校验层（§2）在 Audit / Human Gate 前用；发散与决策层（§3）由各 Skill 按需挑用。
4. **单次上限**：一次产出最多应用 8-10 个 lens，宁缺毋滥。不把本文件全文塞进产物。
5. **防空转**：稀疏或冲突输入不进入发散，直接路由 `needs_user_input`（见 `src/framework/workflow.md` Entry And Exit）。

---

## §1 通用核心层（每个 Work Item 必用 · 6 个）

### 1. 第一性原理 / First Principles

- 触发时机：`Think` 阶段开始
- 核心问题：
  1. 需要改变的可观测结果是什么？根本问题是什么？
  2. 哪些声明是伪装成需求的假设？
  3. 如果去掉提议方案，目标是否仍然成立？
- 产出落点：产物目标章节（用词必须指向可观测结果，不从模板字段倒推需求）

### 2. 系统思考 / Systems Thinking

- 触发时机：旅程、功能、规则分析（Stage 1-2 全程）
- 核心问题：
  1. 这个变化影响上游/下游 Work Item、其他角色、数据归属、外部系统或依赖吗？
  2. 哪些已经有效、不能破坏？
- 产出落点：假设与依赖章节（显式列出受影响面）

### 3. 对抗性审查 / Adversarial Review

- 触发时机：`Audit` 阶段
- 核心问题：
  1. 前提不成立会怎样？我能否构造反例推翻当前方案？
  2. 证据是否只来自一个利益方？方案是否优化一方而伤害另一方？
  3. 是否在理解备选方案前就预设了解决方案？
- 产出落点：Audit 结果（只记录影响候选版本或需人工确认的发现，不灌水）

### 4. 逆向验证 / Reverse Validation

- 触发时机：`Audit` 阶段末 / Commit 前
- 核心问题：
  1. 从预期结果反推，哪些前提必须为真？
  2. 缺失哪些前置条件、依赖、基线数据、归属与约束？
- 产出落点：DoD 检查 / 下游输入摘要

### 5. 确认偏误防御 / Confirmation Bias Defense

- 触发时机：每步产出后（尤其 Intake → Generate 之间）
- 核心问题：
  1. 我是不是顺着用户/上游的方案在写？有没有独立质疑过它本身？
  2. 如果我把 AI_INFERENCE 当 FACT 写进去，后果是什么？
- 产出落点：知识状态标签（FACT / DECISION / ASSUMPTION / AI_INFERENCE / UNKNOWN / CONFLICT 必须逐条核实，见 `src/framework/contracts.md`）

### 6. 知识边界认知 / Knowledge Boundary

- 触发时机：全流程
- 核心问题：
  1. 已知 / 未知 / 自以为知道——三者分清了没？
  2. 没有证据支撑的推断标 AI_INFERENCE 了没？不确定的标 UNKNOWN 了没？冲突标 CONFLICT 了没？
- 产出落点：`Intake` 知识状态登记 + QuestionRecord 问题清单

### 6.1 证据强度分级 / Evidence Strength Grading

- 触发时机：`Intake` / `Generate` 标注 AI_INFERENCE 时（承接 §1.6 知识边界认知）
- 核心问题：
  1. 这条推断的证据强到什么程度？能支撑它进入评审基线吗？
  2. 什么证据出现会推翻或降级这个判断（可证伪条件是否写清）？
- 产出落点：AI_INFERENCE 标注附加分级（strong / medium / weak）+ 可证伪条件
- 来源吸收：work buddy `product-management/references/prioritization-frameworks.md` RICE Confidence 三级（100% = high / 80% = medium / 50% = low）的分层思路 + Kill Decision「Would we start this today knowing what we know?」的"证据改变判断"意识，作为 `contracts.md` Knowledge States 中 AI_INFERENCE 的内部细化，不改标签体系。

**三级分层**：

| 级别 | 判定 | 标注 | 产物行为 |
|---|---|---|---|
| strong | ≥2 条独立来源交叉支撑 | `AI_INFERENCE(strong)` | 可写入产物正文，进入评审基线 |
| medium | 单条来源或推断链成立但未交叉验证 | `AI_INFERENCE(medium)` | 写入正文但标 `待确认`，进 Clarify |
| weak | 无来源、凭经验补全 | `AI_INFERENCE(weak)` | 不写入产物正文，只进 Clarify 问题清单 |

**可证伪条件（必须写清什么证据会改变判断）**：每条 AI_INFERENCE 附带"若出现 X 证据，此判断降级/推翻"。例：`ASSUMPTION：销售每日录入跟进 1 次（AI_INFERENCE(medium)，若访谈 3 个客户中 ≥2 个反馈实际每日 3 次，则降级 UNKNOWN 并重走 Intake）`。写不出可证伪条件的推断视为 weak，不得进正文。

---

## §2 校验层（Audit / Human Gate 前 · 按需触发）

### 7. 事前验尸 / Pre-Mortem

- 触发时机：阶段收口 / B3 问题收口（`Audit` 阶段）
- 核心问题：假设这个需求做出来失败了，最可能的原因是什么？（逐条列出 3-5 条）
- 产出落点：问题清单 / 风险条目（每条失败原因 → 风险 + 责任人）

### 8. 空杯视角 / Fresh-Eyes Review

- 触发时机：产物提交 Human Gate 前
- 核心问题：假设我是刚入职的开发或业务方，只看这份产物，能直接理解并执行吗？缺了什么信息？
- 产出落点：Audit 清单（补充缺失信息，不靠对话记忆补全）
- 具体技法（PR-FAQ，吸收自 product-management / Amazon Working Backwards）：在空杯视角自检前，先写一份"假装产品已发布"的新闻稿（PR）+ 常见问题（FAQ）——用客观、数据详实的语言描述目标用户、痛点与解决方案，并加一个假想发布日期。若新闻稿无法打动读者或 FAQ 答不出关键问题，说明价值尚未想清楚。新闻稿/FAQ 是内部思考工具，不进入正式产物。


### 9. 可测试性校验 / Testability Check

- 触发时机：功能描述 / PRD 汇总
- 核心问题：每条需求/规则能写出可量化的验收判据吗？没有判据的标记为未完成
- 产出落点：AC-XXX 验收依据（每条款必须有明确判据，见 `contracts.md` Knowledge States）

### 10. 结论先行 / Conclusion First

- 触发时机：每个产物开头
- 核心问题：第一屏能否让读者做出判断？细节是否都放到了后面？
- 产出落点：产物开头结论段（不改变内容，只改变顺序）

### 11. 读者视角 / Reader Perspective

- 触发时机：写作全程
- 核心问题：业务方看决策、研发看实现、测试看判据——各自能在这份产物里读到吗？
- 产出落点：产物结构（按读者分组组织，不混写）

### 12. 大纲确认门禁 / Outline Gate

- 触发时机：Generate 前的功能要点展开
- 核心问题：
  1. 功能要点是否已用一句话概括并经人工确认，确认后才展开细节？
  2. 是否在未确认大纲前就深入到字段/交互细节？
- 产出落点：Generate 前的大纲确认记录（来源吸收自 prd-development「大纲确认强制卡点」）

### 13. 写作四原则 / Writing Principles

- 触发时机：Generate 全程
- 核心问题：
  1. 每条需求是否具体可执行（非"大致""基本"等模糊表述）？
  2. 是否从开发视角可理解、无歧义？
  3. 信息不足处是否标 `[待确认]` 而非编造？
- 产出落点：产物文字质量自检（来源吸收自 prd-development「写作四原则」）

### 14. 业务语言透镜 / Business Language

- 触发时机：Clarify 提问 / 复述确认
- 核心问题：
  1. 提问是否用业务语言（非方法论黑话），是否给出选项？
  2. 是否先说影响、一次只问一类、追问为什么？
- 产出落点：Clarify 问题措辞自检（来源吸收自 juloko「问题措辞 5 铁律」）

### 15. 证据追溯透镜 / Evidence Traceability

- 触发时机：Intake / Audit（deep_check 纪律）
- 核心问题：
  1. 每条判断是否只输出"问题 + 严重度 + 证据"三字段，而不夹带建议？
  2. 无证据的"建议"是否被当作事实写入了产物？
- 产出落点：Audit 问题条目（问题/严重度/证据，禁止夹带解决方案；来源吸收自 incremental-prd-collaboration「deep_check 纪律」）

### 16. 成本门禁透镜 / Cost Gate

- 触发时机：高消耗操作前（如 stage2 业务逻辑对标、批量检索）
- 核心问题：这个高 token/成本操作是否必须执行？是否已获用户明确确认？
- 产出落点：高消耗操作前置确认记录（来源吸收自 prd-competitor-check「stage2 需用户确认，省 60% token」）

### 17. 置信度标注透镜 / Confidence Labeling

- 触发时机：方案评估 / 结论产出
- 核心问题：每条结论是否标注置信度（高/中/低）？低置信项是否标记待验证？
- 产出落点：评估结论置信度标注（来源吸收自 product-solution-evaluator「置信度 3 级」）

### 18. 事实假设判断三态透镜 / Fact-Assumption-Judgment

- 触发时机：Intake / Generate 全程
- 核心问题：这句话是事实、假设还是判断？三者是否被混写在一起？
- 产出落点：产物中三态分离标注（来源吸收自 pm-master-prosl「区分事实/假设/判断」）

### 19. 出口闸门两问透镜 / Exit Gate Two Questions

- 触发时机：每条需求点/功能点收口
- 核心问题：
  1. 这条需求会误导实现或用户吗？
  2. 什么条件下这条需求会失效？
- 产出落点：需求点收口自检（来源吸收自 producrequirementanalyzer「出口闸门两问」）

---

## §3 发散与决策层（领域层 · 各 Skill 挑用）

| lens | 触发时机 | 核心问题 | 主要使用 Skill |
|---|---|---|---|
| 同理心视角 / Empathy | 旅程/UX/功能分析 | 换到每个角色身上，他的场景、挫败点、期望是什么？ | user-journey, user-stories, page-design, interaction-rules |
| MECE 穷举 / MECE Enumeration | 场景发散、功能清单 | 按角色×生命周期×路径类型切矩阵，先切分再填充，禁止直接列清单 | user-journey, user-stories |
| 边界扫描 / Boundary Scan | 范围基线、UX Scope | 哪些是本期不做但相邻的？边界在哪、谁负责交界处？ | page-design（Scope 层） |
| 奥卡姆剃刀 / Occam's Razor | 多方案取舍 | 两个方案都能达标时，哪个依赖最少、下游影响最小？ | feasibility-analysis |
| 机会成本视角 / Opportunity Cost | 范围收口 | 做这个的代价是放弃什么？值得吗？ | page-design, prd-assembly |
| 一致性校验 / Consistency Check | PRD 汇总 | 正向：每个产物都有章节；反向：每节都能追溯；有无自相矛盾？ | prd-assembly |
| 双重逻辑校验 / Dual Logic Audit | 业务规则 / PRD 汇总 | 准确性（目标-背景匹配、量化可行性）与闭环性（输入-处理-输出闭环、异常场景闭环、商业化链路闭环）是否都校验？ | business-rules, prd-assembly |
| 商业化合规 / Commercialization Compliance | 业务规则 / PRD 汇总 | 付费流程、数据收集、链路完整性、权限差异四项是否都显式处理？ | business-rules, prd-assembly |
| grill 对抗 / Grill Adversarial | PRD 汇总前 | section-grill 四阶段（静默重读→负载分级🔴🟡🟢风险挖掘→逐项 grill→判定 PASS/待澄清/冲突）是否逐节跑完？ | prd-assembly |
| 反例扫描 / Anti-Example Scan | 方案评估 | 15 类反例（伪需求/无场景/指标不闭环/AI 为了 AI/成本倒挂/依赖不可控/合规红线/解决方案先行/大而全平台/体验口号/数据不可得/运营缺位/边界不清/无验证路径/责任不清）是否逐类对照过？ | feasibility-analysis, prd-assembly |
| 预死亡分析 / Pre-Death Analysis | 方案评估 | 方案属于老虎（核心威胁）/纸老虎（伪威胁）/大象（趋势非威胁）？紧迫级（发布阻断/快速跟进/持续跟踪）？ | feasibility-analysis |
| 假设验证四维 / Assumption Validation | 方案评估 | 价值/可用性/商业可行/技术可行四维是否都有验证路径？ | feasibility-analysis |
| naysayer 三阶段 / Naysayer Three-Stage | 需求评审 | 基础第一性原理→真相证据审问→修剪奥卡姆顺序进行？命题漂移是否被追踪？证据四维（来源/规模/匹配/方向矛盾）是否检查？副作用是否审查？ | feasibility-analysis, prd-assembly |
| 决策预注册 / Decision Pre-registration | 决策记录 | 决策是否在四象限（技能/方差/运气/学费）中归属？事后是否复盘归因？ | prd-assembly |
| 西瓜防御 / Watermelon Defense | 状态汇报 | 状态预测是否为具名风险（🟢🟡🔴）而非情绪判断？ | prd-assembly |
| 二阶效应 / Second-Order Effects | 方案评估 | 方案的一阶后果之外，二阶连锁后果是什么？ | feasibility-analysis |
| 停做审查 / Stop-Doing Review | 功能清单评审 / 范围收口 | 哪些功能用量 < 5%、无可测业务结果、持续成本超值、或"一直这么做"？触发即降级/移出/回滚的判据写清了吗？ | feature-list（配 `feature-list/references/kill-criteria.md` 停止条件技法），prd-assembly |

---

## §4 与注册表 / 契约的绑定关系

| 本文件条目 | 绑定对象 | 校验方式 |
|---|---|---|
| §1 通用核心层 | `workflow-registry.json` work_items[*].required_outputs | `validate_artifact.py`（结构 + 语义红线） |
| §1.5 确认偏误 / §1.6 知识边界 | `contracts.md` Knowledge States（6 标签） | `validate_artifact.py`（ready/confirmed 必须含非 FACT 标签） |
| §2.7 事前验尸 | B3 问题收口（IssueRecord） | `branch_validator.py`（B3 记录完整性） |
| §2.9 可测试性 | AC-XXX 验收依据 | `validate_artifact.py`（AC 量化判据检查） |
| §3 发散决策 | support-skills（feasibility-analysis 等） | 人工触发，不设全局闸门 |


---

## §5 表达层技法注册（按需触发 · 不设全局闸门）

以下技法来自 Trae 生态 skill 的适配吸收，注册到对应子 Skill 的 `references/`，由 SKILL.md 按需加载。它们不新增业务阶段，只在需要原型/规则表达时增强产物质量。

| 技法 | 来源 | 注册位置 | 触发条件 | 产物 |
|---|---|---|---|---|
| 可点击原型技法 | interactive-demo-factory + flow2demo | `page-design/references/prototype-techniques.md` | P0 流程 ≥ 3 页 / 状态分支 / 需多方评审 | prototype/index.html + demo-flow.md |
| 规则写作规范 | 交互规则书写格式 | `interaction-rules/references/rule-writing-format.md` | 任何 IX-XXX 交互规则产出 | 段落式 IX 规则（含异常/边界） |
| PRD 原型嵌入 | agile-pm-workflow | `prd-assembly/references/prototype-embedding.md` | 上游已有可点击原型 | PRD §4 内嵌 iframe 切片 + 版本切换器 |
| 功能说明五要素 | prd-development | `functional-flow/references/functional-spec-five-elements.md` | 功能规格产出（含状态生命周期） | functional-flow 产物功能详述段 |
| 交互流程五段式 | prd-development | `interaction-rules/references/flow-five-stage.md` | 任何 IX-XXX 交互流程产出 | 段落式交互流程（触发/执行中/成功/失败/边界） |
| UML 用例规格 | prd-generator | `user-stories/references/use-case-spec-template.md` | 用例建模需求 | 用例规格表（前置/后置/基本流/备选流/业务规则/数据说明） |
| 数据字典 | prd-generator | `validation-rules/references/data-dictionary-pattern.md` | VL-XXX 字段定义产出 | 字段类型/状态枚举对齐 |
| RBAC 权限矩阵 | product-design-0to1 | `business-rules/references/rbac-permission-matrix.md` | to B 角色×资源×操作场景 | BR-XXX 权限差异矩阵 |
| 泳道图 + 状态机 | product-design-0to1 | `state-machine/references/swimlane-state-technique.md` | 多角色状态流转 | 泳道图 + Mermaid stateDiagram |
| MRC 门禁 / 确认信号 | prd-to-prototype | `shared/clarify/references/confirmation-signal-technique.md` | Clarify 阶段完整度阈值 | 白/灰/黑确认信号处理 |
| 范围谈判脚本 | product-management | `shared/clarify/references/scope-negotiation-scripts.md` | Clarify 范围争议 / 优先级摊平时 | 加需求/必须做/竞品对标/全P1 四类谈判脚本 |
| 信息架构图 | prd-fullstack / prd-to-design-doc | `page-design/references/information-architecture.md` | 页面层级与导航设计 | Mermaid 信息架构图 |
| AI 策略四要素 | prd-writer | `feature-list/references/ai-strategy-four-elements.md` | to B 智能化功能（推荐/排序/意图识别） | 输入信号/模型逻辑/输出形式/兜底规则 |
| 溯源标注技法 | prd-generator-cc | `thinking-core` §5.1 附录 | 撰写期信息不确定 | 【推测】/【待确认】/「需专业确认」三级标注 |
| 反合理化技法 | mimo-prd-generator | `thinking-core` §5.1 附录 | Generate 自检 | 6 项借口对照表（借口→正确做法） |
| 独立成文技法 | product-researching | `competitive-research/references/synthesis-craft.md` | 竞品/调研综合分析成文 | 5 段式综合成文（不写承接语言） |
| 认知透镜附录 | pm-cognition-coach | `thinking-core` §5.1 附录 | 系统思考深化 | 产品四层结构 + 苏格拉底 5 提问 |

使用规则：
1. **文本规则是权威，技法产物是增强**：原型/切片不替代 page-design §4、interaction-rules §5 及各独立 stage-2 技能产物的文字详述。
2. **按需触发，不设全局闸门**：与「图表不设必须先询问的全局闸门」原则一致（见 `src/framework/governance.md`）。
3. **忠于输入**：原型不发明页面、不静默补状态；缺失信息标记 `待确认` 交人工。
4. **版本联动**：PRD 内嵌切片路径必须与原型版本一一对应，绝不覆盖历史版本。

### §5.1 表达层附录（新批次吸收 · 按需使用）

**溯源标注三级规范**（来源 prd-generator-cc）：撰写期遇到信息不确定时，用三级标注显式化——
- `【推测】`：AI 基于上下文推断，未获人工确认；
- `【待确认】`：信息缺失，需人工补充；
- `「需专业确认」`：涉及税务/法务/隐私/支付/合规等高风险领域，须相关专业人员确认。
> 三级标注只用于撰写过程与草稿，进入正式产物前必须全部消解或转为 `DECISION / UNKNOWN` 知识状态。

**反合理化 6 项对照表**（来源 mimo-prd-generator）：Generate 后逐项自检，发现"合理化借口"即返工——

| 借口 | 正确做法 |
|---|---|
| 用户故事随便写几个，意思到了就行 | 每个核心功能必须有完整用户故事 + Given-When-Then 验收 |
| 功能清单列全就行，优先级以后再排 | 每条功能必须标 P0/P1/P2，P0 必须可定义 |
| 背景写个大概，大家都知道 | 背景必须能独立支撑目标，删掉模板字段后仍成立 |
| 验收标准写"能正常使用" | 验收标准必须可量化判据，杜绝空泛表述 |
| 异常流程不重要，先写主流程 | 主流程之外必须覆盖异常/边界/空状态/权限流程 |
| 指标先随便定个数字 | 指标必须可达成、可度量、与目标直接挂钩 |

**认知透镜附录**（来源 pm-cognition-coach，仅作系统思考深化）：
- **产品四层结构**：功能层 → 平台生态层 → 规则体系层 → 组织系统层。设计 to B 产品时自问"改动影响哪几层？是否只做了功能层而忽略了规则层？"
- **苏格拉底 5 提问**：假设检验（这成立的前提是什么？）/ 视角切换（换一个角色看还是这样吗？）/ 边界探索（边界在哪，越界会怎样？）/ 本质追问（真正的目标是什么？）/ 行动锚定（明天可做的最小一步是什么？）——用于 Clarify 探究与问题收敛。
