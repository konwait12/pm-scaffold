<!--
产物：故意违规样本（缺上游 4 个 confirmed artifacts，触发 G_CROSS D5.2）
本文件通过 validate_artifact.py —— 故意制造 error 触发 D5.2。
status: ready_for_human_review（演示用）。
-->
---
artifact_id: PRD-VIOL-001
version: v0.1
status: ready_for_human_review
owner: PM-Office
business_fact_owner: VP of Talent
goal_decision_owner: VP of Talent
reviewer: VP of Talent
created_at: 2026-08-11
updated_at: 2026-08-11
confirmed_at: 待确认
---

# PRD 汇总

## 1. 上游产物清单

| 上游步骤 | artifact_id | 状态 | 备注 |
|---|---|---|---|
| `project-background-goal` 项目背景与目标 | BG-PDM-001 | confirmed | 实际存在（演示用） |
| `user-journey-and-stories` 用户旅程与用户故事 | JS-PDM-001 | confirmed | 实际存在（演示用） |
| `product-ux` 产品 UX | （缺失） | — | 故意空缺以触发 D5.2 |
| `function-description` 功能描述 | （缺失） | — | 故意空缺以触发 D5.2 |

> ⚠️ **违规声明**：本 fixture 故意缺 UX-XXX 与 FD-XXX 两个上游，以触发 PRD DoD D5.2 强校验。
> 期望 validator 返回：1 error（"PRD DoD D5.2 failed: missing upstream artifact IDs for ['UX', 'FD']"）。

## 2. 项目背景与目标

（来自 BG-PDM-001 confirmed v1.0，摘要省略）

## 3. 业务角色、用户旅程与用户故事

（来自 JS-PDM-001 confirmed v1.0，摘要省略）

## 4. UX：功能范围、功能流程与关键状态

（本应来自 UX-PDM-XXX，本 fixture 故意缺）

## 5. 分功能描述

（本应来自 FD-PDM-XXX，本 fixture 故意缺）

## 6. 按需章节

（本期无 NFR / 字段规则 / 埋点等按需扩展，跳过）

## 7. 需求追溯矩阵

| 目标 G | 故事 ST | 功能 FEA | 功能详述 FUN | 验收标准 AC | 业务规则 BR |
|---|---|---|---|---|---|
| G1 | ST-001 | ⏸ | ⏸ | ⏸ | ⏸ |
| G2 | ST-002 | ⏸ | ⏸ | ⏸ | ⏸ |

> 故意留 ⏸ 占位以同时命中 D5.3 RTM P0 链断裂校验。

## 8. 正向追溯检查

G→ST→FEA→FUN→AC→BR 链：5 个 G → 10 个 ST → 0 个 FEA → 0 个 FUN → 0 个 AC → 0 个 BR。
链断裂：CRITICAL。

## 9. 反向追溯检查

0 个 BR / 0 个 AC / 0 个 FUN / 0 个 FEA — 全链空。

## 10. 不一致报告

（无新增不一致项；上游缺位属 DoD 阻断，不是 inconsistent 范畴）

## 11. 事实与决定

| ID | 类型 | 内容 | 来源/决策人 | 状态 |
|---|---|---|---|---|
| — | — | 无上游确认产物可引用 | — | 待确认 |

## 12. Constitution Compliance

| 原则 | 状态 | 证据 / 备注 |
|---|---|---|
| ① 业务事实分离 | PASS | §11 显式登记 |
| ② AI 不替业务决定 | PASS | 无新需求引入 |
| ③ 来源可追溯 | FAIL | D5.2 缺 UX-/FD- 前缀上游 → validator error |
| ④ 冲突显式保留 | PASS | 无冲突源 |

## 13. 验收依据与变更记录

| 版本 | 变更原因 | 主要变化 | 人工确认状态 |
|---|---|---|---|
| v0.1 | 故意违规（演示 D5.2 + RTM P0 链断裂） | 缺 UX-/FD- 上游 + RTM ⏸ 占位 | 待评审 |