<!--
产物模板：PRD 汇总
prd-assembly SKILL.md 驱动 · 只聚合不新增 · 待确认 是唯一占位符。
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
upstream_artifact_ids: []
---

<!--
🤖 AGENT INSTRUCTION BLOCK (for downstream AI consumers of this PRD):

This PRD is a living source of truth — not a static document. When consuming this file:

1. DO NOT GUESS. If any requirement, rule, or constraint is ambiguous, STOP and ask the human product owner before proceeding.
2. Knowledge states are tagged inline:
   - FACT = verified business truth (do not reinterpret)
   - DECISION = confirmed human decision (binding)
   - ASSUMPTION = unverified premise (may change)
   - AI_INFERENCE = AI-generated, NOT human-confirmed (treat as suggestion)
   - UNKNOWN = explicitly marked gap (ask before acting)
   - CONFLICT = known contradiction (resolve before implementing)
3. The traceability matrix (§7) is authoritative — every acceptance criterion traces to a story, which traces to a goal. Do not implement anything without traceability.
4. If you need to change this PRD, create a change proposal (see src/shared/change-management/proposal-template.md) — do not edit confirmed content directly.
5. Version history is in §13. Always check you're reading the latest version.
-->

# PRD（产品需求文档）

## 0. 上游产物清单

| 步骤 | Artifact ID | 版本 | 状态 | 确认时间 |
|---|---|---|---|---|
| 1. 项目背景与目标 | `待确认` | `待确认` | confirmed | `待确认` |
| 2. 用户旅程与用户故事 | `待确认` | `待确认` | confirmed | `待确认` |
| 3. 产品 UX | `待确认` | `待确认` | confirmed | `待确认` |
| 4. 功能描述 | `待确认` | `待确认` | confirmed | `待确认` |

## 1. 项目背景与目标

（从 `project-background-goal` 已确认产物完整引用）

`待确认`

## 2. 业务角色、用户旅程与用户故事

（从 `user-journey-and-stories` 已确认产物完整引用）

`待确认`

## 3. UX：功能范围、功能流程与关键状态

（从 `product-ux` 已确认产物完整引用）

`待确认`

## 4. 分功能描述

（从 `function-description` 已确认产物完整引用）

`待确认`

## 5. 按需章节

### 5.1 字段规则

（从 `function-description` §4 引用，如无内容标注"本期不适用"）

### 5.2 埋点需求

（从 `function-description` §5 引用，如无内容标注"本期不适用"）

### 5.3 依赖与约束

（汇总各工作事项 中的依赖与约束）

### 5.4 未决问题与风险

（汇总各工作事项 中的 UNKNOWN 项和开放风险）

## 6. 需求追溯矩阵

| 目标 (G) | 故事 (ST) | 功能 (FEA) | 功能详述 (FUN) | 验收标准 (AC) | 业务规则 (BR) |
|---|---|---|---|---|---|
| `待确认` | `待确认` | `待确认` | `待确认` | `待确认` | `待确认` |

## 7. 正向追溯检查

| 检查项 | 结果 | 差距说明 |
|---|---|---|
| 所有 G-X → ≥ 1 ST-XXX | 待确认 | |
| 所有 P0 ST → ≥ 1 FEA-XXX | 待确认 | |
| 所有 P0 FEA → ≥ 1 FUN-XXX | 待确认 | |
| 所有 P0 FUN → ≥ 1 AC-XXX | 待确认 | |

## 8. 反向追溯检查

| 检查项 | 结果 | 说明 |
|---|---|---|
| 所有 AC-XXX → FUN-XXX | 待确认 | |
| 所有 FUN-XXX → FEA-XXX | 待确认 | |
| 所有 FEA-XXX → ST-XXX | 待确认 | |
| 无孤儿元素 | 待确认 | |

## 9. 不一致报告

| 类型 | 元素 | 问题 | 建议处理 |
|---|---|---|---|
| 待确认 | 待确认 | 待确认 | 待确认 |

## 10. 事实与决定

（汇总各工作事项 的关键事实与决定）

## 11. Constitution Compliance

| 原则 | 状态 | 证据 / 备注 |
|---|---|---|
| ① 业务事实分离 | 待确认 | |
| ② AI 不替业务决定 | 待确认 | |
| ③ 来源可追溯 | 待确认 | |
| ④ 冲突显式保留并关闭 | 待确认 | |

## 12. 验收依据与变更记录

### 12.1 关键验收基准

（汇总各工作事项 的验收标准）

### 12.2 版本变更摘要

| 版本 | 变更原因 | 主要变化 | 人工确认状态 |
|---|---|---|---|
| v1.0 | 初始正式 PRD | 汇总 前四个工作事项 全部已确认内容 | 待确认 |
