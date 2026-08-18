---
artifact_id: EX-CIA-001-001
version: v0.1
status: ready_for_human_review
owner: PM-Office
reviewer: 评审人
created_at: 2026-08-17
updated_at: 2026-08-17
confirmed_at: ""
upstream_artifact_id: "BG-001"
---

# 异常处理（违规样本）


## 1. 失败模式

| EX-XXX | 所属 FUN | 失败模式 | 恢复策略 |
|---|---|---|---|
| EX-001 |  | 网络超时 | 重试 3 次 |
| EX-002 | FUN-002 | 余额不足 | 中止流程并通知 |

### 解释
- EX-001 故意无 FUN 挂接 + 无来源 — 触发 C3 项 (2) 和 (3)
