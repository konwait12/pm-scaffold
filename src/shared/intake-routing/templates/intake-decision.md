---
artifact_id: INTAKE-{REQ_NAME}
version: "v1"
status: draft
process_tier: {PROCESS_TIER}
difficulty_level: "{DIFFICULTY_LEVEL}"
tier_recommendation: "{TIER_RECOMMENDATION}"
tier_selection: "{TIER_SELECTION_MODE}"
decision_owner: "待填写"
decided_at: ""
source_materials: "待填写"
review_trigger: "命中硬升级条件、范围变化或新增 L2-only 能力时复审"
applicability_contract_version: "1"
l2_only_pd: "pending"
l2_only_ix: "pending"
l2_only_fields: "pending"
l2_only_vl: "pending"
l2_only_state: "pending"
l2_only_ex: "pending"
---

# 档位决策：{REQ_NAME}

> 本文件是本 REQ 的唯一档位事实源。README 仅作投影；命令不得用临时参数覆盖此处。
> 需求难度只是入口建议触发器：低难度不展示档位建议；中/高难度仅展示建议，最终档位必须由人工确认并以 `process_tier` 为准。

## 1. 资格矩阵

| 维度 | L0 资格 | L1 资格 | 本 REQ 证据/结论 |
|---|---|---|---|
| 变更范围 | 单一可定位变更 | 单模块标准交付 | 待填写 |
| 角色与流程 | 单角色、无持久状态 | 无 L2-only 能力 | 待填写 |
| 风险 | 无敏感/资金/合规影响 | 五项 L2-only 均有不适用依据 | 待填写 |
| 回退 | 单一简单回退 | 可实施且有边界 | 待填写 |

## 2. L2-only 能力适用性

逐项填写事实依据；任一项“适用”即升级 L2。

| 能力 | 结论（适用/不适用） | 事实依据 |
|---|---|---|
| PD 页面/原型 | 待填写 | 待填写 |
| IX 交互规则 | 待填写 | 待填写 |
| FIELDS 字段规则 | 待填写 | 待填写 |
| VL 校验规则 | 待填写 | 待填写 |
| STATE 状态机 | 待填写 | 待填写 |
| EX 异常处理 | 待填写 | 待填写 |

机器校验投影（仅 L1 的最终 PRD 装配闸门使用）：五项 frontmatter 必须逐项写成
`not_applicable: <具体事实依据>`。例如 `not_applicable: 沿用现有设置页，无新增页面、字段、状态或失败恢复路径`。
不得写 `N/A`、`无`、`待填写` 或泛化的“本期不适用”。任一项实际适用时，将其写为
`applicable: <事实依据>` 并升级为 L2。

## 3. Canonical PRD 章节适用性矩阵

L0、L1、L2 的最终 PRD 使用同一组章节。本表是新 REQ 的初始适用性判断；不得删除行，不能只写 `N/A`、`暂无` 或“本期不做”。状态只能是 `required`、`conditional` 或 `not_applicable`。

| 章节 | 状态 | 事实依据 | 来源引用 | 判断人 | 判断时间 | 触发条件 / 当前判断 | 复审触发点 |
|---|---|---|---|---|---|---|---|
| §1 项目背景 | required | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 当前判断：必须提供 | 目标或背景变化 |
| §2 项目范围 | required | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 当前判断：必须提供 | 范围变化 |
| §3 用户旅程 | required | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 当前判断：必须说明受影响路径 | 角色或路径变化 |
| §4 用户故事 | required | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 当前判断：必须追溯用户价值 | 角色或目标变化 |
| §5 功能清单 | required | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 当前判断：必须提供可实施功能 | 功能边界变化 |
| §6 功能流程 | required | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 当前判断：必须提供可观察行为 | 入口或分支变化 |
| §7 原型/UX | conditional | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 触发条件：页面结构或体验变化；当前判断：待判断 | 出现页面、布局或导航变化 |
| §8 交互规则 | conditional | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 触发条件：新增交互、表单或反馈；当前判断：待判断 | 出现交互规则变化 |
| §9 业务规则 | required | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 当前判断：必须说明流程约束 | 规则或阈值变化 |
| §9.1 计算与流程规则 | required | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 当前判断：必须提供适用业务规则 | 规则或阈值变化 |
| §9.2 字段清单 | conditional | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 触发条件：新增字段、字段属性或数据模型；当前判断：待判断 | 出现字段或数据模型变化 |
| §9.3 校验规则 | conditional | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 触发条件：新增字段或跨字段约束；当前判断：待判断 | 出现校验需求 |
| §9.4 状态变化 | conditional | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 触发条件：新增状态、事件、守卫或副作用；当前判断：待判断 | 出现状态模型 |
| §9.5 异常处理 | conditional | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 触发条件：新增失败、恢复或人工升级；当前判断：待判断 | 出现新失败语义 |
| §10 验收依据 | required | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 当前判断：必须可判定 | 目标或行为变化 |
| §11 按需章节 | conditional | 待填写 | 待填写 | 待填写 | YYYY-MM-DD | 触发条件：竞品、字段、埋点、可行性、术语或职责有事实来源；当前判断：待判断 | 新增按需来源 |

L0 也必须完成此表。mini-prd 只能提供事实草稿，不能替代此矩阵；L1 的 PD/IX/VL/STATE/EX 还必须与上表结论一致。

## 4. 决策与升级

- 选择档位：`{PROCESS_TIER}`
- 选择人：`待填写`
- 决策时间：`待填写`
- 升级理由（如有）：`无`
- 复审触发：范围、角色、状态、数据、合规或回退策略变化时重新评估。
