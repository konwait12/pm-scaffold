<!--
产物：故意含空泛词 / 无量化阈值的 AC 样本（回归护栏用）
本文件通过 validate_artifact.py —— 结构合规（AC-ID + Given/When/Then + G-X 追溯），
但 AC-001~003 命中「空泛词 advisory」与「无量化阈值 advisory」：
  - ac.vague_language（MEDIUM，blocking=False）
  - ac.no_quantified_threshold（MEDIUM，blocking=False）
advisory 非阻断：ok 仍为 True（run_tests_mac.sh 按正向 fixture 通过），
单测负责断言「命中即出 advisory」，防止 check 被无意删除/弱化。
-->
---
artifact_id: AC-VAGUE-001
version: v0.1
status: draft
owner: ""
business_fact_owner: ""
goal_decision_owner: ""
reviewer: ""
created_at: "2026-08-18"
updated_at: "2026-08-18"
confirmed_at: ""
upstream_artifact_id: "FEA-001, BR-001"
---

# 验收标准

## 1. 验收标准

> 故意含空泛词与无量化阈值的 AC 行（回归护栏样本）。AC-004 为对照行（已量化、无空泛词）。

| ID | 验收标准（Given/When/Then） | 量化阈值 | 来源目标 G | 所属 FEA | 优先级 |
|---|---|---|---|---|---|
| AC-001 | Given 用户点击按钮, When 系统响应, Then 系统应快速响应用户操作 | 无 | G-001 | FEA-001 | P0 |
| AC-002 | Given 数据加载, When 请求发出, Then 数据应及时返回结果 | 无 | G-001 | FEA-001 | P1 |
| AC-003 | Given 列表渲染, When 用户滚动, Then 页面保持稳定流畅不卡顿 | 无 | G-002 | FEA-002 | P1 |
| AC-004 | Given 用户发起查询, When 请求发出, Then P99 响应时间 ≤ 500ms 内返回结果 | P99 ≤ 500ms | G-001 | FEA-001 | P0 |

## 2. 知识状态标注

| 内容 | 状态 | 说明 |
|---|---|---|
| 需求范围 | FACT | 来自上游 FEA-001 / FEA-002 |
| 性能指标口径 | DECISION | 待业务方复核 P99 ≤ 500ms 是否达标 |

## 3. 版本变更摘要

| 版本 | 变更原因 | 主要变化 | 人工确认状态 |
|---|---|---|---|
| v0.1 | 回归护栏样本 | 故意含空泛词 / 无阈值行 | 待评审 |

> ⚠️ **样本声明**：本 fixture 故意保留空泛词（快速/及时/稳定流畅）与「无」量化阈值行，
> 期望 validator 返回 ok=True 且 issues 中同时出现 `ac.vague_language` 与 `ac.no_quantified_threshold`
> （MEDIUM / blocking=False）。用途：作为 acceptance-criteria 模糊词 advisory 检查的回归对照，
> 防止该 check 被删除或不再命中。AC-004 为负向对照，不应触发任何 advisory。
