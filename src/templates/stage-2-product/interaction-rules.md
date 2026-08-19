<!--
产物模板：交互规则
本模板由 interaction-rules SKILL.md 驱动。
待确认 是唯一占位符。

v2 拆分说明：自 page-design + interaction-rules.md §3（交互规则）独立。
页面设计部分 → page-design.md。
业务规则部分 → business-rules.md。
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

# 交互规则

## 0. 预检输入充分度判定

- 上游产物：`待确认`
- 已确认页面设计数：`待确认`
- 已确认功能数：`待确认`
- 判定：`待确认`

## 1. 范围引用（上游）

> 上游功能流程已在 functional-flow 确认。本步骤只引用，不重新定义功能。

| 引用 | 内容 |
|---|---|
| 上游页面设计 | `待确认`（引用 page-design PD-XXX） |
| 上游功能流程 | `待确认`（引用 functional-flow FEA-XXX） |

## 2. 交互规则

> 用户操作后系统怎么反应：操作反馈、跳转逻辑、弹窗规则、表单交互。仅描述页面层交互，不包含业务规则（属于 business-rules）。

| ID | 规则描述 | 触发条件 | 系统响应 | 适用页面/功能 | 来源 |
|---|---|---|---|---|---|
| IX-001 | `待确认` | `待确认` | `待确认` | `待确认` | `待确认` |

### 2.1 状态覆盖检查

| 状态类型 | 是否覆盖 | 对应 IX 规则 | 备注 |
|---|---|---|---|
| 加载态 (loading) | 待确认 | 待确认 | |
| 空态 (empty) | 待确认 | 待确认 | |
| 错误态 (error) | 待确认 | 待确认 | |
| 禁用态 (disabled) | 待确认 | 待确认 | |
| 超时态 (timeout) | 待确认 | 待确认 | |

> 备注：本状态覆盖集合与 interaction-rules 校验器 `scripts/validate_artifact.py`（`_five_states_coverage`）保持一致：loading/empty/error/disabled/timeout。起草时按该集合逐态核对，避免与校验器脱节。

## 3. 事实与决定

| ID | 类型 | 内容 | 来源/决策人 | 状态 |
|---|---|---|---|---|
| 待确认 | 待确认 | 待确认 | 待确认 | 待确认 |

## 4. 假设、AI 推断、未知与冲突

| ID | 类型 | 内容 | 依据 | 影响 | 责任人 | 处理方式 |
|---|---|---|---|---|---|---|
| 待确认 | 待确认 | 待确认 | 待确认 | 待确认 | 待确认 | 待确认 |

## 5. 待确认问题

| ID | 问题 | 结论 |
|---|---|---|
| 待确认 | 待确认 | 待确认 |

## Clarifications

| session_id | category | question | ai_preliminary_judgment | options | decision_owner | blocking | deferral_risk | accepted_answer | reflow_target | integrated_at | integrated_by | audit_recheck |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |

## 6. 来源追溯

| 来源 ID | 材料/位置 | 关键内容 | 本文落位或排除理由 |
|---|---|---|---|
| 待确认 | 待确认 | 待确认 | 待确认 |

## 7. 下游传导摘要

承接上游 page-design，向下传递给 business-rules 的关键交接：

- 确认的 `IX-XXX` 列表（来自 §2）
- 已锁定的页面/状态枚举（来自 §2.1）
- 范围基线 In/Out/Deferred/Conditional（无变更入口——发现越界需回流 page-design）

## 8. 下游输入摘要

```text
confirmed_version: 待确认
interaction_rule_count: 待确认
state_coverage: 待确认
open_nonblocking_unknowns: 待确认
source_ids: 待确认
```

## 9. Constitution Compliance

| 原则 | 状态 | 证据 / 备注 |
|---|---|---|
| ① 业务事实分离 | 待确认 | |
| ② AI 不替业务决定 | 待确认 | |
| ③ 来源可追溯 | 待确认 | |
| ④ 冲突显式保留并关闭 | 待确认 | |

## 10. 版本变更摘要

| 版本 | 变更原因 | 主要变化 | 人工确认状态 |
|---|---|---|---|
| v0.1 | 初始候选 | 待确认 | 待确认 |
