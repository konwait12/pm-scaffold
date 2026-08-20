<!--
产物：PRD 汇总 · L1 标准档（v8 结构）· process_tier=L1
L1 只走 7 个上游（BG/UJ/US/FL/FF/BR/AC）；§7 原型/UX、§8 交互规则、
以及 §9.2-§9.4 的 L2-only 子节均省略，不以“本期不适用”伪造缺失产物。
本 fixture 用于验证 prd-assembly validator 的 V8_L1 分叉。
-->
---
artifact_id: PRD-L1-001
version: v0.1
status: ready_for_human_review
owner: nova
business_fact_owner: nova
goal_decision_owner: nova
reviewer: nova
created_at: 2026-08-20
updated_at: 2026-08-20
confirmed_at: ""
prd_structure_version: "8"
process_tier: "L1"
issue_in_prd: false
upstream_artifact_ids: ["BG-001", "UJ-001", "US-001", "FL-001", "FF-001", "BR-001", "AC-001"]
upstream_work_item_statuses: "project-background-goal user-journey user-stories feature-list functional-flow business-rules acceptance-criteria"
---

# PRD（产品需求文档）

## 1. 项目背景

G-001 目标：提升活动提醒触达率。

## 2. 项目范围

In: 活动前 24h 红点提醒；Out: 跨端同步。

## 3. 用户旅程

UJ-001 生命周期表：邀请触达 → 预约登记 → 活动前提醒。

## 4. 用户故事

ST-001 As a 客人，我想要收到活动提醒，这样 不错过活动。

## 5. 功能清单

FEA-001 活动提醒红点（ST-001，P0）。

## 6. 功能流程

主流程 Mermaid：FEA-001 触发 → 展示 → 点击 → 消失。

## 9. 业务规则

### 9.1 计算与流程规则

BR-001 活动开始前 24h 触发提醒（FEA-001）。

## 10. 验收依据

AC-001 Given 活动开始前 24h，When 触发提醒，Then 红点展示且可点击。

## 需求追溯矩阵

| 目标 (G) | 故事 (ST) | 功能 (FEA) | 功能详述 (FUN) | 验收 (AC) | 适用证据 (BR/VL/STATE/EX/PD/IX) |
|---|---|---|---|---|---|
| G-001 | ST-001 | FEA-001 | FF-001 主流程 | AC-001 | BR-001 |

## 自审记录（Constitution Compliance）

| 原则 | 状态 | 证据 / 备注 |
|---|---|---|
| ① 业务事实分离 | PASS | 内容全部来自 7 个已确认上游 |
| ② AI 不替业务决定 | PASS | 无新增需求 |
| ③ 来源可追溯 | PASS | 每个 FEA/AC 追溯 ST/G |
| ④ 冲突显式保留并关闭 | PASS | 无冲突 |
