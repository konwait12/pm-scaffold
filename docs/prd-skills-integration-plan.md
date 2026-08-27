# PRD Skill 精华整合实施计划（to B 偏向）

> 场景：产品需求能力整合（历史计划）
> 目标：将经过评估的 PRD 能力以最小侵入方式融入现有 PM 脚手架，强化 to B 场景，不引发大规模重构。
> 状态：**历史记录**；现行规则以 `docs/tier-l0-l1-rebuild-plan.md` 为准。

---

## 一、调研结论：PRD 能力盘点

按与现有脚手架的 to B 契合度从高到低排序。脚手架特征：三阶段、19 skill、强人工确认、事件溯源审计、知识状态标注（FACT/DECISION/ASSUMPTION/AI_INFERENCE/UNKNOWN/CONFLICT）、产物为中文 `prd.md`、PRD-only（不做技术架构/测试用例/研发任务拆分）。

| # | 能力模块 | to B 契合度 | 核心能力（可复用精华） | 处置 |
|---|---|---|---|---|
| 1 | product-design-0to1 | ★★★ 原生适配 | AI 推断显式化（对应 AI_INFERENCE）、`[TODO:]` 占位（对应 UNKNOWN）、回退即重生成（对应事件溯源）、RBAC 权限矩阵、字段决策清单、泳道图+状态机、埋点规划、领域偏移检测 | 重点融入 |
| 2 | prd-development | ★★★ 原生适配 | 功能说明五要素（前置条件/实现逻辑/核心字段含**状态生命周期**/数据校验）、交互流程五段式（触发/执行中/成功/失败/边界）、大纲确认卡点、写作四原则（具体可执行/开发视角/无歧义/`[待确认]`）、用户故事四字段+"并且则拆分" | 重点融入 |
| 3 | prd-to-prototype（非 skillhub） | ★★★ 原生适配 | MRC 门禁（G1-G6 完整度阈值）、白/灰/黑确认信号识别、业务约束五分类（合规/时间/预算/组织/历史）、模块间交接校验清单、13 要素 PRD、七维场景诊断 | 重点融入（流程层） |
| 4 | prd-review-design | ★★★ 原生适配 | 双重逻辑校验（准确性+闭环性：输入-处理-输出闭环/异常场景闭环/商业化链路闭环）、设计要点四维（界面/交互/视觉/状态）、商业化合规四检查（付费流程/数据收集/链路完整/权限差异）、优先级三级划分 | 重点融入（审计层） |
| 5 | prd-reviewer | ★★ 需轻量适配 | 10 分制 7 模块评分体系、17 项快速检查清单、灰度方案要求、数据报表要求、风险合规三检查（资金/数据泄露/合规）、量化数据强制、模板不符上限 6 分机制 | 融入审计层（剔除 tapd 地址等待定工具字段） |
| 6 | prd-generator | ★★★ 原生适配 | UML 用例驱动方法论、用例规格模板（前置/后置/基本流/备选流/业务规则/数据说明表）、时序图模板、数据字典（字段类型/状态枚举）、UI 规范、非功能需求 | 融入参考文档层 |
| 7 | prd-fullstack | ★★ 需轻量适配 | 14 章 PRD 结构、6 种产品类型配置（含 SaaS/B 端）、信息架构图方法论、PRD 审查清单、构建系统、协作原则（可视化/可回退） | 取 SaaS/B 端配置+信息架构+审查清单，舍技术方案/测试方案/运营方案/管理篇 |
| 8 | prd-writer | ★★ 需轻量适配 | 策略导向（why before what）、AI 策略四要素（输入信号/模型逻辑/输出形式/兜底规则）、A/B 测试方案、MoSCoW、风险与降级 | 融入参考文档层（AI 策略四要素适配 to B 智能化场景） |
| 9 | prd-writing-expert | ★★ 需轻量适配 | 问题陈述四要素、用户故事标准写法、MoSCoW+价值复杂度矩阵、北极星指标、MVP 范围、验收可测试性 | 融入参考文档层（部分已被现有 skill 覆盖） |
| 10 | prd-to-design-doc | ★★ 需轻量适配 | 信息架构图（Mermaid）、核心交互流程图、异常状态处理、埋点需求表、设计交付清单、设计风险评估 | 融入参考文档层（page-design/exception-handling/tracking-plan） |
| 11 | prd（skillhub） | ★ 方法论可借鉴 | 故事切片原则、依赖排序铁律、验收标准可验证性（好/坏对比）、`passes: false→true` 状态机 | 仅取验收可验证性检查，其余偏研发任务管理不迁入 |
| 12 | PRD to Prototype（skillhub） | ★ 仅作参考 | 审美自检清单、PC 端 SaaS 风格指引、设计系统规范（中性色+品牌色仅 CTA） | 仅取审美自检清单+B 端 SaaS 风格，零提问理念相悖不迁入 |
| 13 | prd-skill | △ 不建议迁入 | PRD 五段、P0-P2、用户故事+验收、MVP、假设显式记录 | 偏 to C 含技术架构（SwiftUI/CoreData），与 PRD-only 冲突，价值低 |

**结论**：1-6 为重点融入对象（6 个原生/轻量适配），7-10 为选择性融入（4 个轻量适配），11-12 仅取单点技法（2 个），13 不迁入。覆盖 12/13 个 skill 的精华，避免"只迁入一点"。

---

## 二、整合范围与取舍原则

### 取（融入脚手架的精华类型）
- **方法论与思考透镜**：双重逻辑校验、第一性原理补充、大纲确认卡点、写作四原则、AI 推断显式化、MECE/价值复杂度矩阵
- **结构化模板**：UML 用例规格模板、功能说明五要素、交互流程五段式、数据字典、信息架构图
- **to B 专项技法**：RBAC 权限矩阵、字段决策清单、泳道图+状态机、业务约束五分类、商业化合规四检查、灰度/报表/风险三检查
- **确认与门禁机制**：MRC 门禁、白/灰/黑确认信号识别、模块间交接校验清单、大纲确认强制卡点、验收可验证性好/坏对比
- **审计评分**：10 分制评分卡、17 项检查清单、闭环性审查标签

### 舍（不迁入，超出 PRD-only 范围或与脚手架理念冲突）
- 技术架构设计、技术选型、接口文档、部署方案（prd-fullstack §10、prd-skill 技术规格）
- 测试用例代码、测试套件（prd-fullstack §12）
- 运营推广策略、用户增长、活动策划（prd-fullstack §14）
- 项目排期、里程碑、资源管理（prd-fullstack §15）
- 研发任务拆分、依赖排序、进度追踪（prd skillhub 的 `prd.json` 故事管理）
- 零提问直出理念（PRD to Prototype skillhub）——与脚手架"强人工确认+知识状态标注"宪法相悖

---

## 三、零改动策略（核心）

### 红线：以下一律不触碰
1. `src/framework/workflow-registry.json`（注册表）——不新增 work_item、不新增 stage、不改 predecessors
2. 任何 `SKILL.md` 的主干 8 步循环（Preflight→Intake→Think→Clarify→Generate→Audit→Human Gate→Commit/Reflow）
3. 任何模板的 frontmatter 字段（`src/templates/`）
4. 任何 `validate_artifact.py` 的 AST 校验字段引用

**为什么安全**：注册表契约（`registry_contract_check.py`）的 E3_drift 检查只校验"模板 frontmatter 字段 ↔ validate_artifact.py AST 引用"的闭环。本计划只注入 `references/` 参考文档与 `thinking-core.md`/`review-taxonomy.md` 的章节内容，不新增 frontmatter 字段，因此**不触发 E3_drift，`registry_contract_check` 保持绿灯**。这与 `thinking-core.md §5` 的"表达层技法注册"机制一致：可复用技法以独立参考文档方式沉淀，不改变主流程契约。

### 三档接入方式

| 档位 | 接入位置 | 接入物 | 侵入度 | 闸门性 |
|---|---|---|---|---|
| **A 档 · 思想层** | `src/framework/thinking-core.md` §3 发散决策层 + §5 表达层技法注册表 | 新增 3-5 个 to B 透镜、登记新技法 | 仅追加章节，不改 §1/§2 强制层 | 按需触发，不设全局闸门 |
| **B 档 · 参考文档层** | 各 skill 的 `references/` 目录新增 to B 技法文档 | 9 个新 references 文件 | 仅新增文件，不改 SKILL.md 主干 | 按需加载，不设全局闸门 |
| **C 档 · 审计层** | `src/shared/audit/review-taxonomy.md` + 各 skill `audit-checklist.md`/`reviewer-checklist.md` | 新增审查标签、扩展检查项、新增评分卡 | 追加条目，不删原有 | 新增项默认 advisory 级（非阻断），不阻断现有 gate |

---

## 四、模块映射表（精华 → 接入点 → to B 适配）

| 精华能力 | 能力主题 | 接入档位 | 接入点（文件路径） | to B 适配 | 接入物 |
|---|---|---|---|---|---|
| AI 推断显式化、`[TODO:]` 占位、回退即重生成 | product-design-0to1 | A 档 | `thinking-core.md §1.5/§1.6 注释` + `contracts.md` 知识状态引用 | 原生 | 补充技法说明（脚手架已支持 AI_INFERENCE/UNKNOWN，强化用法指引） |
| 大纲确认卡点 | prd-development | A 档 | `thinking-core.md §2` 新增 lens "大纲确认门禁" | 原生 | 新 lens：功能要点一句话概括→人工确认→方可展开细节 |
| 写作四原则 | prd-development | A 档 | `thinking-core.md §2` 新增 lens "写作四原则" | 原生 | 新 lens：具体可执行/开发视角/无歧义/`[待确认]` 标注 |
| 双重逻辑校验（准确性+闭环性） | prd-review-design | A 档 | `thinking-core.md §3` 新增 lens "双重逻辑校验" | 原生 | 新 lens：目标-背景匹配、输入-处理-输出闭环、异常场景闭环、商业化链路闭环 |
| 商业化合规透镜 | prd-review-design | A 档 | `thinking-core.md §3` 新增 lens "商业化合规" | 原生 | 新 lens：付费流程合规、数据收集合规、链路完整性、权限差异 |
| 功能说明五要素（含状态生命周期） | prd-development | B 档 | `functional-flow/references/functional-spec-five-elements.md` | 原生 | 新技法文档：前置条件/实现逻辑/核心字段（状态生命周期）/数据校验/后置 |
| 交互流程五段式 | prd-development | B 档 | `interaction-rules/references/flow-five-stage.md` | 原生 | 新技法文档：触发/执行中/成功/失败/边界条件 |
| UML 用例规格模板 | prd-generator | B 档 | `user-stories/references/use-case-spec-template.md` | 原生 | 新技法文档：参与者/前置后置/基本流/备选流/业务规则/数据说明表 |
| 数据字典（字段类型/状态枚举） | prd-generator | B 档 | `validation-rules/references/data-dictionary-pattern.md` | 原生 | 新技法文档：字段类型枚举、状态字段枚举、VL-XXX 对齐 |
| RBAC 权限矩阵 | product-design-0to1 | B 档 | `business-rules/references/rbac-permission-matrix.md` | 原生 | 新技法文档：角色×资源×操作矩阵、权限差异显式化 |
| 字段决策清单 | product-design-0to1 | B 档 | `validation-rules/references/field-decision-checklist.md` | 原生 | 新技法文档：字段来源/类型/必填/状态/归属决策记录 |
| 泳道图+状态机 | product-design-0to1 | B 档 | `state-machine/references/swimlane-state-technique.md` | 原生 | 新技法文档：泳道图（角色×状态）+ Mermaid stateDiagram |
| MRC 门禁+白/灰/黑确认信号 | prd-to-prototype | B 档 | `src/shared/clarify/references/confirmation-signal-technique.md` | 原生 | 新技法文档：G1-G6 完整度阈值、白/灰/黑名单回复处理、二次询问 |
| 业务约束五分类 | prd-to-prototype | B 档 | `project-background-goal/references/business-constraint-taxonomy.md` | 原生 | 新技法文档：合规/时间/预算/组织/历史五类约束 |
| 10 分制评分卡 | prd-reviewer | C 档 | `prd-assembly/references/prd-scoring-rubric.md` | 需轻量适配 | 新评分卡：7 模块评分（剔除 tapd 地址/设计师等待定工具字段，保留背景四要素/量化目标/灰度/报表/风险合规） |
| 17 项快速检查清单 | prd-reviewer | C 档 | `prd-assembly/references/reviewer-checklist.md`（追加） | 需轻量适配 | 追加 to B 检查项：权限矩阵/状态生命周期/商业化闭环 |
| 商业化合规四检查 | prd-review-design | C 档 | `prd-assembly/references/audit-checklist.md`（追加） | 原生 | 追加审计项：付费流程/数据收集/链路完整/权限差异 |
| 闭环性审查标签 | prd-review-design | C 档 | `src/shared/audit/review-taxonomy.md`（追加标签） | 原生 | 新增标签 `[CommercializationGap]` 商业化链路缺口 |
| 验收可验证性好/坏对比 | prd（skillhub） | C 档 | `acceptance-criteria/references/audit-checklist.md`（追加） | 原生 | 追加：好/坏验收标准对比样例、"Works correctly"判为不合格 |
| AI 策略四要素 | prd-writer | B 档 | `feature-list/references/ai-strategy-four-elements.md` | 需轻量适配 | 新技法文档：输入信号/模型逻辑/输出形式/兜底规则（适配 to B 智能化场景） |
| 信息架构图方法论 | prd-fullstack / prd-to-design-doc | B 档 | `page-design/references/information-architecture.md` | 原生 | 新技法文档：产品结构/页面层级/导航设计（Mermaid） |
| B 端 SaaS 审美自检清单 | PRD to Prototype skillhub | B 档 | `page-design/references/prototype-techniques.md`（追加章节） | 需轻量适配 | 追加 §10：PC 端 SaaS 风格指引（Sidebar+Header/中性色/品牌色仅 CTA） |
| 异常状态处理+埋点需求表 | prd-to-design-doc | B 档 | `exception-handling/references/exception-and-tracking.md` | 原生 | 新技法文档：网络异常/业务异常分类+埋点事件表 |
| 价值复杂度矩阵+北极星指标 | prd-writing-expert | B 档 | `project-background-goal/references/value-complexity-matrix.md` | 原生 | 新技法文档：价值×复杂度四象限+北极星指标定义 |

---

## 五、接入方式与文件清单

### A 档 · 思想层（修改 1 个文件，追加章节）
**文件**：`src/framework/thinking-core.md`
- §2 校验层追加 2 个 lens：「大纲确认门禁」「写作四原则」
- §3 发散决策层追加 2 个 lens：「双重逻辑校验」「商业化合规」
- §5 表达层技法注册表追加登记 9 个新技法（指向 B 档新文件）
- 同步：`src/framework/workflow.md` 的条件支持章节补充对 to B 技法的引用（仅文档同步，不改流程）

> 注：A 档只追加 lens 与技法登记，**不改 §1 通用核心层 6 个强制透镜**，因此不增加任何 Work Item 的强制开销。

### B 档 · 参考文档层（新增 9 个文件 + 追加 2 个章节）
**新增文件**（按 skill 分布）：
1. `src/stages/002-product-requirements/skills/functional-flow/references/functional-spec-five-elements.md`
2. `src/stages/002-product-requirements/skills/interaction-rules/references/flow-five-stage.md`
3. `src/stages/001-business-requirements/skills/user-stories/references/use-case-spec-template.md`
4. `src/stages/002-product-requirements/skills/validation-rules/references/data-dictionary-pattern.md`
5. `src/stages/002-product-requirements/skills/business-rules/references/rbac-permission-matrix.md`
6. `src/stages/002-product-requirements/skills/validation-rules/references/field-decision-checklist.md`
7. `src/stages/002-product-requirements/skills/state-machine/references/swimlane-state-technique.md`
8. `src/shared/clarify/references/confirmation-signal-technique.md`
9. `src/stages/001-business-requirements/skills/project-background-goal/references/business-constraint-taxonomy.md`
10. `src/stages/002-product-requirements/skills/feature-list/references/ai-strategy-four-elements.md`
11. `src/stages/002-product-requirements/skills/page-design/references/information-architecture.md`
12. `src/stages/002-product-requirements/skills/exception-handling/references/exception-and-tracking.md`
13. `src/stages/001-business-requirements/skills/project-background-goal/references/value-complexity-matrix.md`

**追加章节**（不改主干）：
- `src/stages/002-product-requirements/skills/page-design/references/prototype-techniques.md` 追加 §10「B 端 SaaS 审美自检」

> 每个 B 档文件遵循 `prototype-techniques.md` 既定格式：能力背景说明 → 输入映射（候选能力输入 → 脚手架对应产物）→ 工作流程 → 核心硬规则 → 边界（Do Not）→ 质量自检清单。所有文件标注“按需加载，不设全局闸门”。

### C 档 · 审计层（新增 1 个文件 + 追加 3 个文件条目）
**新增文件**：
- `src/stages/003-prd-output/skills/prd-assembly/references/prd-scoring-rubric.md`（10 分制评分卡，advisory 级）

**追加条目**：
- `src/shared/audit/review-taxonomy.md`：新增标签 `[CommercializationGap]`（商业化链路缺口）
- `src/stages/003-prd-output/skills/prd-assembly/references/audit-checklist.md`：追加 to B 审计项（商业化合规四检查）
- `src/stages/003-prd-output/skills/prd-assembly/references/reviewer-checklist.md`：追加 to B 检查项（权限矩阵/状态生命周期/商业化闭环）
- `src/stages/002-product-requirements/skills/acceptance-criteria/references/audit-checklist.md`：追加验收可验证性好/坏对比样例

> C 档新增检查项**默认 advisory 级（非阻断）**，不改变现有 gate 的 blocking 行为。评分卡仅作为 Human Gate 的参考工具，不写入产物状态机。

---

## 六、验证标准

### 6.1 架构零改动验证（必须通过）
- [ ] `bash run_tests_mac.sh` 全绿（`registry_contract_check` Phase 0 + `consistency_check` + 全部回归测试）
- [ ] `python3 src/scripts/consistency_check.py` 无新增 error
- [ ] `workflow-registry.json` 的 `schema_version` 不变（仍为 7）
- [ ] 注册表的 `work_items` 数量不变（仍为 13 主干）、`stages` 数量不变（仍为 3）
- [ ] 无任何 `SKILL.md` 的 8 步循环被修改
- [ ] 无任何模板 frontmatter 字段被新增/删除
- [ ] 无任何 `validate_artifact.py` 的 AST 校验逻辑被修改

### 6.2 内容接入验证
- [ ] A 档：`thinking-core.md` §2/§3/§5 追加内容与 §1 强制层不冲突，新 lens 均标注"按需触发"
- [ ] B 档：9+ 个新 references 文件均符合 `prototype-techniques.md` 格式，含"来源吸收说明"与"输入映射"表，均标注"按需加载，不设全局闸门"
- [ ] B 档：每个新文件在对应 `SKILL.md` 的"加载参考"表中登记一行
- [ ] C 档：新增标签/检查项均标注 severity 为 INFO/MEDIUM（advisory），不新增 CRITICAL/HIGH 阻断项
- [ ] C 档：评分卡文档明确声明"参考工具，不影响产物状态机"

### 6.3 to B 适配验证
- [ ] 所有标注"原生适配 to B"的技法，其样例/模板使用 to B 场景（角色权限/审批流/组织架构/多租户）
- [ ] 所有"需轻量适配"的技法，已剔除 to C 专属字段（如 tapd 地址待定工具字段、消费者增长指标），替换为 to B 对等项
- [ ] RBAC 权限矩阵、商业化合规、灰度方案三类技法有 to B 专项样例

### 6.4 知识状态一致性验证
- [ ] 所有新技法文档引用 `contracts.md` 的 6 个知识状态标签，不发明新标签
- [ ] AI 推断显式化技法明确要求：非用户明示的细节必须标 `AI_INFERENCE` 并经人工拍板（与 product-design-0to1 的 Step 5.5/6.5 一致）
- [ ] `[TODO:]` 占位技法明确要求：信息不足时占位标 `UNKNOWN`，不编造

---

## 七、to B 适配标注汇总

| 适配类型 | 数量 | 说明 |
|---|---|---|
| 原生适配 to B | 18 项 | RBAC/状态生命周期/商业化合规/泳道图/用例规格/数据字典/双重逻辑校验/大纲确认/写作原则/MRC门禁/确认信号/业务约束/异常埋点/信息架构/价值矩阵/闭环标签/验收可验证性/AI推断显式化 |
| 需轻量适配 | 4 项 | 10 分评分卡（剔除 tapd 字段）、17 项检查清单（追加 to B 项）、AI 策略四要素（适配 to B 智能化）、B 端审美自检（PC SaaS 风格） |
| 偏 to C/不建议迁入 | 1 项 | prd-skill（含 SwiftUI/CoreData 技术架构） |
| 仅取单点技法 | 2 项 | prd skillhub（验收可验证性）、PRD to Prototype skillhub（审美自检） |

---

## 八、实施顺序与里程碑

按"先框架后细节、先验证后铺开"原则，分 4 个里程碑。每个里程碑结束均跑 `run_tests_mac.sh` 确认零回归。

| 里程碑 | 内容 | 验证点 |
|---|---|---|
| **M1 · 思想层注入** | A 档：修改 `thinking-core.md`（追加 4 lens + §5 登记 9 技法）+ 同步 `workflow.md` 引用 | run_tests_mac.sh 全绿；新 lens 标注按需触发 |
| **M2 · 核心参考文档** | B 档前 6 个文件：功能五要素、交互五段式、用例规格、数据字典、RBAC 矩阵、泳道图状态机 | 6 文件符合格式；SKILL.md 加载参考表已登记 |
| **M3 · 辅助参考文档** | B 档后 7 个文件：字段决策、MRC门禁、业务约束、AI策略、信息架构、异常埋点、价值矩阵 + prototype-techniques §10 | 全部 B 档完成；13 skill 加载参考表已登记 |
| **M4 · 审计层扩展** | C 档：评分卡 + review-taxonomy 新标签 + 3 个 checklist 追加 + 验收可验证性 | 新项均 advisory 级；评分卡声明不影响状态机 |

每个里程碑内部：写文件 → 在对应 SKILL.md 的"加载参考"表登记 → 跑 run_tests_mac.sh → 确认绿灯 → 进入下一里程碑。

---

## 九、风险与缓解

| 风险 | 等级 | 缓解措施 |
|---|---|---|
| references 文件过多导致 AI 加载膨胀 | 中 | 严守"按需加载，不设全局闸门"；每个 SKILL.md 加载参考表只登记、不强制；单次 Work Item 最多应用 8-10 lens（thinking-core §4 单次上限不变） |
| 评分卡被误用为阻断闸门 | 中 | 评分卡文档首行声明"advisory 参考工具，不写入产物状态机"；不接入 `validate_artifact.py` |
| 新 lens 与 §1 强制层冲突 | 低 | A 档只追加到 §2/§3，不改 §1 6 个强制透镜；新 lens 均标注"按需触发" |
| to B 适配遗漏 to C 残留 | 低 | 每个新技法文档经 to B 适配验证（§6.3）；剔除 tapd/消费者增长等待定字段 |
| 脚手架未来升级导致技法失效 | 低 | 每个技法文档含"来源吸收说明"与"输入映射"表，升级时按映射表同步；技法是增强非主干，失效不阻断流程 |

---

## 十、确认事项

请人工确认以下 4 点后启动 M1：
1. 整合范围（12/13 skill 精华，舍 prd-skill）是否认可？
2. 零改动三档策略（A 思想/B 参考/C 审计，不碰注册表/主干/模板/AST）是否认可？
3. to B 适配标注（18 原生 + 4 轻量适配）是否需调整范围？
4. 实施顺序（M1 思想层 → M2 核心参考 → M3 辅助参考 → M4 审计层）是否认可？
