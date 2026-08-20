<!--
产物模板：状态机
本模板由 state-machine SKILL.md 驱动。
待确认 是唯一占位符。

v2 拆分说明：自 feature-list (et al.).md §5（状态变化）独立。
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
upstream_artifact_id: ""
---

# 状态机

## 0. 预检输入充分度判定

- 上游产物：`待确认`
- 已确认业务规则数：`待确认`
- 判定：`待确认`

## 1. 状态定义

| STATE | 状态名称 | 描述 | 终态标记 |
|---|---|---|---|
| STATE-001 | `待确认` | `待确认` | 是/否 |

## 2. 状态转换表

| 当前状态 | 触发事件 | 目标状态 | 条件 | 副作用 | 适用范围 / 追溯锚点 |
|---|---|---|---|---|---|
| `待确认` | `待确认` | `待确认` | `待确认` | `待确认` | `待确认` |

## 3. 禁止转换显式声明

| 转换 | 原因 | 适用范围 / 追溯锚点 |
|---|---|---|
| `待确认` | `待确认` | `待确认` |

## 4. 状态覆盖穷尽检查

> 每个 FEA-XXX 的所有已知事件都有对应的目标状态。

| FEA | 事件 | 状态覆盖 | 缺失处理 |
|---|---|---|---|
| FEA-XXX | `待确认` | 待确认 | `待确认` |

## 5. 事实与决定

| ID | 类型 | 内容 | 来源/决策人 | 状态 |
|---|---|---|---|---|
| 待确认 | 待确认 | 待确认 | 待确认 | 待确认 |

## 6. 假设、AI 推断、未知与冲突

| ID | 类型 | 内容 | 依据 | 影响 | 责任人 | 处理方式 |
|---|---|---|---|---|---|---|
| 待确认 | 待确认 | 待确认 | 待确认 | 待确认 | 待确认 | 待确认 |

## 7. 待确认问题

| ID | 问题 | 结论 |
|---|---|---|
| 待确认 | 待确认 | 待确认 |

## Clarifications

| session_id | category | question | ai_preliminary_judgment | options | decision_owner | blocking | deferral_risk | accepted_answer | reflow_target | integrated_at | integrated_by | audit_recheck |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |

## 8. 来源追溯

| 来源 ID | 材料/位置 | 关键内容 | 本文落位或排除理由 |
|---|---|---|---|
| 待确认 | 待确认 | 待确认 | 待确认 |

## 9. 下游输入摘要

```text
confirmed_version: 待确认
state_count: 待确认
transition_count: 待确认
forbidden_transition_count: 待确认
state_coverage_gaps: 待确认
open_nonblocking_unknowns: 待确认
source_ids: 待确认
```

## 10. Constitution Compliance

| 原则 | 状态 | 证据 / 备注 |
|---|---|---|
| ① 业务事实分离 | 待确认 | |
| ② AI 不替业务决定 | 待确认 | |
| ③ 来源可追溯 | 待确认 | |
| ④ 冲突显式保留并关闭 | 待确认 | |

## 11. 版本变更摘要

| 版本 | 变更原因 | 主要变化 | 人工确认状态 |
|---|---|---|---|
| v0.1 | 初始候选 | 待确认 | 待确认 |
