# DDD 设计指南（PRD → 领域设计交接）

> 本指南提供独立、可验证的领域交接提示；不依赖任何本地索引或特定工具。
> 定位：与 `domain-mapping-hint.md`（信号→候选映射表）互补——本文档提供**从 PRD 到可实施 DDD 设计的 7 阶段方法**，作为研发接手 PRD 后的可选设计交接提示。
> 触发：prd.md confirmed 后、研发开始领域建模/技术设计时按需加载。**advisory 级，不设闸门、不动流程引擎、不新增 work_item。**

## 1. 与项目契约的关系（不制造矛盾）

| 项目契约 | 本文档的处理 |
|---|---|
| 13 产物 + mini-prd 不增不减 | **不新增产物**；仅作为 `prd-assembly/references/` 下的一篇交接提示文档 |
| 宪法"AI 不替业务决定" | 本文档只做**信号映射提示**，不做设计决策；研发保留领域设计自主权 |
| prd-assembly"不写指针" | 本文档是**独立交接文档**，不进 prd.md 正文（不写"详见"） |
| 状态机产物 STATE-XXX | 本文档把 STATE 产物映射为 DDD 状态模式（见 §4） |

## 2. 7 阶段方法（蒸馏 E2）

```
Phase 1 事件风暴   ← 从 functional-flow / state-machine 提取领域事件
Phase 2 领域发现   ← 从 background-goal / user-journey 提取限界上下文与子域
Phase 3 战略设计   ← 上下文映射（上下游依赖）
Phase 4 战术设计   ← Entity / VO / Aggregate / Repository / Domain Service
Phase 5 ER 与库表  ← 从 VL / BR 字段映射表结构（可选）
Phase 6 跨层契约   ← 从 AC / IX 映射接口入参出参（可选）
Phase 7 行为建模   ← 从 BR / STATE 映射状态机 + 不变量
```

每阶段产物标注"PRD 上游来源"（FEA / BR / STATE / VL / AC），保持追溯。

## 3. 阶段入口对照（研发从哪里开始）

| 研发关心 | 读 PRD 哪里 | 阶段 |
|---|---|---|
| 领域事件有哪些 | §6 功能流程（主/支/异常）+ §10 状态变化（STATE 转移）| Phase 1 |
| 领域上下文边界 | §1 项目背景 + §3 用户旅程（角色/触点）| Phase 2 |
| 聚合与实体 | §5 功能清单（FEA 粒度）+ §8 业务规则（BR 归属）| Phase 4 |
| 状态不变量 | §10 状态变化（STATE 守卫）| Phase 7 |

> 若 PRD 是 L1 档（无 page-design / state-machine / validation-rules / exception-handling 上游），研发应从 §6 功能流程 + §8 业务规则自行识别状态与校验（PRD §9.1 已按 intake-decision 事实化"不适用"），**不强制要求缺失产物**。

## 4. 状态机 → DDD 状态模式映射（蒸馏 E2 行为建模）

| PRD STATE 产物 | DDD 落点 |
|---|---|
| STATE-XXX 状态枚举 | 领域对象的状态字段（Enum）|
| STATE 转移（事件 + 守卫）| 领域事件 + 聚合内状态变更方法 |
| STATE 副作用 | Domain Service / 事件监听器 |
| 禁止转移（STATE 表"不允许"行）| 状态机守卫抛业务异常（对应 EX 异常恢复）|

**贫血模型检查（蒸馏 E2 硬标准）**：若聚合只有 getter/setter、业务规则全在外层 Service → 标记 [Gap]，提示回 PRD §8 业务规则补领域行为归属。

## 5. 反模式（对照规避）

| ❌ 不要 | ✅ 要做 |
|---|---|
| 研发直接拿 PRD 字段名当 DB 列名（不先做领域发现）| 先 Phase 2 定上下文边界，再落库表 |
| 状态逻辑散落在多个 Service | 状态变更收敛进聚合，守卫进领域方法 |
| 用 PRD "验收依据"当领域测试，不补单元测试 | AC 是验收基线，领域测试须补业务规则用例 |
| 无视 L1 的"本期不适用"事实化依据 | L1 需求直接复用 L2 全套产物（须按 intake-decision 说明补足）|

## 6. 与 domain-mapping-hint.md 的分工

| 文档 | 回答的问题 |
|---|---|
| `domain-mapping-hint.md` | PRD 信号 → 领域**候选**（名词/动词/约束 → Entity/VO/Event/Enum）|
| 本文档 `ddd-design-guide.md` | 候选 → 可实施 DDD **设计流程**（7 阶段 + 状态模式 + 贫血检查）|

两篇都是 advisory 交接提示，不阻断任何 gate。
