---
artifact_id: VL-CIA-001-001
version: v0.1
status: ready_for_human_review
owner: PM-Office
reviewer: 评审人
created_at: 2026-08-17
updated_at: 2026-08-17
confirmed_at: ""
upstream_artifact_id: "BG-001"
---

# 字段校验规则（违规样本）


## 1. 字段校验

| VL-XXX | 所属 FUN | 字段 | 校验规则 | 来源 |
|---|---|---|---|---|
| VL-001 |  | age | 18 ≤ age ≤ 100 | BR-002 |
| VL-002 | FUN-001 | email | 必须符合 RFC 5322 | FEA-005 |

### 解释
- VL-001 故意无 FUN 挂接 — 触发 C3 项 (2)
