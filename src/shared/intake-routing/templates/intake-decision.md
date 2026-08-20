---
artifact_id: INTAKE-{REQ_NAME}
version: "v1"
status: draft
process_tier: {PROCESS_TIER}
decision_owner: "待填写"
decided_at: ""
source_materials: "待填写"
review_trigger: "命中硬升级条件、范围变化或新增 L2-only 能力时复审"
l2_only_pd: "pending"
l2_only_ix: "pending"
l2_only_vl: "pending"
l2_only_state: "pending"
l2_only_ex: "pending"
---

# 档位决策：{REQ_NAME}

> 本文件是本 REQ 的唯一档位事实源。README 仅作投影；命令不得用临时参数覆盖此处。

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
| VL 校验规则 | 待填写 | 待填写 |
| STATE 状态机 | 待填写 | 待填写 |
| EX 异常处理 | 待填写 | 待填写 |

机器校验投影（仅 L1 的最终 PRD 装配闸门使用）：五项 frontmatter 必须逐项写成
`not_applicable: <具体事实依据>`。例如 `not_applicable: 沿用现有设置页，无新增页面、字段、状态或失败恢复路径`。
不得写 `N/A`、`无`、`待填写` 或泛化的“本期不适用”。任一项实际适用时，将其写为
`applicable: <事实依据>` 并升级为 L2。

## 3. 决策与升级

- 选择档位：`{PROCESS_TIER}`
- 选择人：`待填写`
- 决策时间：`待填写`
- 升级理由（如有）：`无`
- 复审触发：范围、角色、状态、数据、合规或回退策略变化时重新评估。
