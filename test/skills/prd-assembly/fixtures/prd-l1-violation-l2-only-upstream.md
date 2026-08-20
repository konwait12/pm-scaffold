<!--
产物：PRD 汇总 · L1 标准档（v8 结构）· 违规 fixture
声明了 L2-only 上游（page-design/interaction-rules/validation-rules/state-machine/exception-handling）——
L1 档不得混入，validate_artifact.py 应报 D5.2 双查错误。
-->
---
artifact_id: PRD-L1-BAD
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
upstream_artifact_ids: ["BG-001", "UJ-001", "US-001", "FL-001", "FF-001", "BR-001", "AC-001", "PD-001", "IX-001"]
upstream_work_item_statuses: "project-background-goal user-journey user-stories feature-list functional-flow page-design interaction-rules business-rules validation-rules state-machine exception-handling acceptance-criteria"
---

# PRD（产品需求文档）

## 1. 项目背景

G-001 目标说明。

## 2. 项目范围

In: 范围。

## 3. 用户旅程

UJ-001 旅程。

## 4. 用户故事

ST-001 故事。

## 5. 功能清单

FEA-001 功能。

## 6. 功能流程

FEA-001 主流程。

## 9. 业务规则

### 9.1 计算与流程规则

BR-001 规则。

## 10. 验收依据

AC-001 验收。

## 需求追溯矩阵

| 目标 (G) | 故事 (ST) | 功能 (FEA) | 功能详述 (FUN) | 验收 (AC) | 适用证据 (BR/VL/STATE/EX/PD/IX) |
|---|---|---|---|---|---|
| G-001 | ST-001 | FEA-001 | FF-001 主流程 | AC-001 | BR-001 |

## 自审记录（Constitution Compliance）

| 原则 | 状态 | 证据 / 备注 |
|---|---|---|
| ① 业务事实分离 | PASS | |
| ② AI 不替业务决定 | PASS | |
| ③ 来源可追溯 | PASS | |
| ④ 冲突显式保留并关闭 | PASS | |
