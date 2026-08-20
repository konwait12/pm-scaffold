<!--
产物模板：PRD 汇总（v8 结构）
prd-assembly SKILL.md 驱动 · 只聚合不新增 · 待确认 是唯一占位符。

v8 章节编排（与 v7 的差异见 prd-assembly/output-contract.md §兼容）：
  L2 的 §1-§10 为 10 个主干章节，与图中 10 个主干产物一一对应；§11 按需章节按需落章（上游无内容标"本期不适用"）；
  L1 装配时仅保留其 7 个已确认来源对应的 §1-§6、§9.1、§10，删除 §7、§8、§9.2-§9.4；
  L1 的 L2-only 能力依据在 intake-decision.md 和 assembly manifest，不能用 PRD 中的 N/A 伪造。
  附录 A/B 必含；附录 C 仅在 frontmatter issue_in_prd=true 时生成。
-->
---
artifact_id: ""
version: "v0.1"
status: "draft"
owner: ""
business_fact_owner: ""
goal_decision_owner: ""
reviewer: ""
created_at: ""
updated_at: ""
confirmed_at: ""
prd_structure_version: "8"
process_tier: "L2"
issue_in_prd: false
upstream_artifact_ids: []
---

<!--
🤖 AGENT INSTRUCTION BLOCK (for downstream AI consumers of this PRD):

1. DO NOT GUESS. If any requirement, rule, or constraint is ambiguous, STOP and ask the human product owner before proceeding.
2. Knowledge states are tagged inline:
   - FACT = verified business truth (do not reinterpret)
   - DECISION = confirmed human decision (binding)
   - ASSUMPTION = unverified premise (may change)
   - AI_INFERENCE = AI-generated, NOT human-confirmed (treat as suggestion)
   - UNKNOWN = explicitly marked gap (ask before acting)
   - CONFLICT = known contradiction (resolve before implementing)
3. The traceability matrix (附录A) is authoritative — every acceptance criterion traces to a story, which traces to a goal. Do not implement anything without traceability.
4. If you need to change this PRD, create a change proposal (see src/shared/change-management/proposal-template.md) — do not edit confirmed content directly.
5. Version history is in the frontmatter (version / updated_at). Always check you're reading the latest version.
-->

# PRD（产品需求文档）

> 上游：本 PRD 基于 REQ-XXX 的已确认上游产物（版本与评审记录见 99-review/ 与 frontmatter `upstream_artifact_ids`）。
> 结构：`prd_structure_version: 8` · `process_tier: L2`。L2 图中 10 个主干产物一一对应 §1-§10；L1 仅装配 §1-§6、§9.1、§10 并省略所有无来源的 L2-only 章节；§11 按需；附录 A/B 必含、附录 C 条件生成。

## 1. 项目背景

（内嵌 `project-background-goal` 已确认产物完整全文，逐字搬运、不写「详见 XX-XXX」指针；含业务背景/现状/问题/目标 G-XXX/KPI/约束/角色，缺则标 `待确认`）

`待确认`

## 2. 项目范围

（内嵌 `user-stories` §项目范围基线 完整全文：In/Out/Deferred/Conditional 范围基线 + `feature-list` 边界说明，逐字搬运、不写指针；含假设与依赖）

`待确认`

## 3. 用户旅程

（内嵌 `user-journey` 已确认产物完整全文：生命周期分解表、用户旅程图、路径类型覆盖检查，逐字搬运、不写指针）

`待确认`

## 4. 用户故事

（内嵌 `user-stories` 已确认产物完整全文：故事卡片 ST-XXX、旅程→故事覆盖矩阵、MoSCoW 优先级，逐字搬运、不写指针）

`待确认`

## 5. 功能清单

（内嵌 `feature-list` 已确认产物完整全文：功能总账 FEA-XXX、功能→故事追溯矩阵、优先级 P0/P1/P2，逐字搬运、不写指针）

`待确认`

## 6. 功能流程

（内嵌 `functional-flow` 已确认产物完整全文：主流程、分支流程、异常流程与入口，逐字搬运、不写指针；Mermaid 图整图内嵌）

`待确认`

## 7. 原型/UX

（仅 L2：内嵌 `page-design` 已确认产物完整全文：信息架构、页面结构、导航逻辑、用户体验路径、页面原型、交互标注、状态描述，逐字搬运、不写指针。L1 装配时删除整个 §7，不得标「本期不适用」。）

`待确认`

## 8. 交互规则

（仅 L2：内嵌 `interaction-rules` 已确认产物完整全文：IX-XXX 交互规则逐条、操作反馈、跳转逻辑、弹窗规则、表单交互、5 状态覆盖，逐字搬运、不写指针。L1 装配时删除整个 §8，不得标「本期不适用」。）

`待确认`

## 9. 业务规则

> L2 呈现合并、产物独立：§9.1-§9.4 分别逐字内嵌 4 个已确认上游产物全文，不写「详见 XX-XXX」指针。L1 仅保留 §9.1；装配时删除 §9.2-§9.4。

### 9.1 计算与流程规则

（内嵌 `business-rules` 已确认产物完整全文：BR-XXX 规则决策表整表、规则→功能追溯矩阵，逐字搬运）

`待确认`

### 9.2 校验规则

（仅 L2：内嵌 `validation-rules` 已确认产物完整全文：VL-XXX 字段与跨字段约束整表、错误提示，逐字搬运。L1 装配时删除此小节，不得标「本期不适用」。）

`待确认`

### 9.3 状态变化

（仅 L2：内嵌 `state-machine` 已确认产物完整全文：STATE-XXX 状态表、转移、守卫与副作用，逐字搬运。L1 装配时删除此小节，不得标「本期不适用」。）

`待确认`

### 9.4 异常处理

（仅 L2：内嵌 `exception-handling` 已确认产物完整全文：EX-XXX 分级、失败模式、恢复与人工升级，逐字搬运。L1 装配时删除此小节，不得标「本期不适用」。）

`待确认`

## 10. 验收依据

（内嵌 `acceptance-criteria` 已确认产物完整全文：AC-XXX 验收标准整表 Given/When/Then、量化阈值、G 目标追溯，逐字搬运、不写指针）

`待确认`

## 11. 按需章节

> 以下小节仅在上游有非空内容时落章；无内容标注「本期不适用」，不得以「详见 XX-XXX」指针了事。

### 11.1 竞品分析

（内嵌 `competitive-research` 支持产物对比结论；如无竞品分析需求标「本期不适用」）

`待确认`

### 11.2 字段规则说明

（内嵌 `validation-rules` 字段定义表整表；如无字段定义需求标「本期不适用」）

`待确认`

### 11.3 埋点需求分析

（内嵌 `tracking-plan` 分支产物的埋点/事件表整表；如无埋点需求标「本期不适用」）

`待确认`

### 11.4 可行性分析

（内嵌 `feasibility-analysis` 支持产物结论摘要：市场空间/技术可行性/投入产出/风险评估；如未做可行性分析标「本期不适用」）

`待确认`

### 11.5 名词解释 / 术语表

（从各上游已确认产物中汇总术语/缩略词定义，逐条摘录不自造；如无术语可标注「本期不适用」）

| 术语 / 缩略词 | 说明 |
|---|---|
| 待补充 | 待补充 |

### 11.6 涉及团队及职责

（汇总各上游产物中涉及的团队/系统职责，只写上游已提及的团队、不推断；如无明确职责划分可标注「本期不适用」）

| 团队 / 系统 | 职责 |
|---|---|
| 待补充 | 待补充 |

## 需求追溯矩阵

> 机器可读追溯链；每行一条核心追溯链。P0 项必须有 G→ST→FEA→FUN→AC；BR/VL/STATE/EX/PD/IX 仅在适用时附入，不强制线性穿越。

| 目标 (G) | 故事 (ST) | 功能 (FEA) | 功能详述 (FUN) | 验收 (AC) | 适用证据 (BR/VL/STATE/EX/PD/IX) |
|---|---|---|---|---|---|
| `待确认` | `待确认` | `待确认` | `待确认` | `待确认` | `待确认` |

## 自审记录（Constitution Compliance）

> 评审用附录：AI 的自审证明，非 PRD 正文。正向/反向追溯检查与不一致报告由机器在 gate 时产出、进 99-review 评审记录，不写进 PRD。

| 原则 | 状态 | 证据 / 备注 |
|---|---|---|
| ① 业务事实分离 | 待确认 | |
| ② AI 不替业务决定 | 待确认 | |
| ③ 来源可追溯 | 待确认 | |
| ④ 冲突显式保留并关闭 | 待确认 | |

## 附录 C. 问题清单

> 仅在 frontmatter `issue_in_prd: true` 时生成；默认问题清单只进 issue-record.md，不进 PRD。

（内嵌 `issue-record` 已关闭/待办问题汇总表：ISS-NNN 标题/类别/状态/owner/来源；若未选择生成本节标「本期不适用」）

`待确认`
