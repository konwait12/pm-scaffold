---
artifact_id: STATE-CIA-001-001
version: v0.1
status: ready_for_human_review
owner: PM-Office
reviewer: 评审人
created_at: 2026-08-17
updated_at: 2026-08-17
confirmed_at: ""
upstream_artifact_id: "BG-001"
---

# 状态机（违规样本）


## 1. 状态定义

| STATE-XXX | 状态名 | 所属 FUN |
|---|---|---|
| STATE-001 | 待支付 | FUN-001 |
| STATE-002 | 已支付 | FUN-001 |

## 2. 转移表

| STATE-XXX | 事件 | 目标 | guard |
|---|---|---|---|
| STATE-001 | 用户付款 | STATE-002 | amount > 0 |
| STATE-002 |  | STATE-001 |  |

### 解释
- 第二条故意无事件名 + 无来源 — 触发 C3 项 (3)
