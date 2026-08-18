---
artifact_id: STATE-HIRE-001
version: v0.1
status: ready_for_human_review
owner: PM-Office
business_fact_owner: VP of Talent
goal_decision_owner: VP of Talent
reviewer: VP of Talent
created_at: 2026-08-11
updated_at: 2026-08-11
confirmed_at: ""
upstream_artifact_id: "FEA-HIRE-001, BR-HIRE-001"
---

# 状态机（STATE）

> 5 个核心实体状态机 · 15 个 STATE-XXX 状态 · 完整转移 + 禁止转换

## 0. 预检输入充分度判定

- 输入：FEA-HIRE-001 + BR-HIRE-001（22 条规则）
- 判定：**充分模式** → 走 §1-§5 完整工作流

## 1. 简历投递状态机（Application）

### FUN-003: 投递流程

#### 1.1 状态定义

| STATE | 状态名 | 触发进入 | 初始 | 所属 FUN |
|---|---|---|---|---|
| STATE-001 | 待审（pending） | HR 收到投递，未处理 | ✓ | FUN-003 |
| STATE-002 | 面试中（interview） | HR 安排面试 | | FUN-003 |
| STATE-003 | 录用（offer） | HR 发 offer | | FUN-003 |
| STATE-004 | 拒绝（rejected） | HR 拒绝 | | FUN-003 |
| STATE-005 | 撤回（withdrawn） | 候选人在 24h 内撤回 | | FUN-003 |

#### 1.2 转移表

| STATE-XXX | 事件 | 目标状态 | guard | 副作用 | 所属 FUN |
|---|---|---|---|---|---|
| STATE-001 | HR 安排面试 | STATE-002 | reason 已记录 | 通知候选人 + 日历邀请 | FUN-003 |
| STATE-001 | HR 拒绝 | STATE-004 | reason ≥ 10 字（VL-022） | 通知候选人 + 记录拒绝原因 | FUN-003 |
| STATE-001 | 候选人撤回 | STATE-005 | 投递时间 < 24h | 删除投递记录 + 通知 HR | FUN-003 |
| STATE-002 | HR 发 offer | STATE-003 | 薪酬已确认 | 通知候选人 + 启动背调 | FUN-003 |
| STATE-002 | HR 拒绝 | STATE-004 | reason ≥ 10 字 | 通知候选人 | FUN-003 |
| STATE-003 | 候选人接受 | (终态) | 24h 内未拒 | 入职流程启动 | FUN-003 |
| STATE-003 | 候选人拒绝 | STATE-004 | — | 通知 HR + 标记 | FUN-003 |
| STATE-005 | (终态) | — | — | — | FUN-003 |

### 1.3 禁止转换

- STATE-002 → STATE-001（不可从面试中回到待审）
- STATE-003 → STATE-001（不可从 offer 回待审）
- STATE-003 → STATE-002（不可从 offer 回面试中）
- STATE-004 → STATE-001（拒绝不可逆，候选人需 HR 手动重开）
- STATE-004 → STATE-003（拒绝不可逆）

### 1.4 终态

- STATE-003（候选人接受 offer 后 → 入职流程）
- STATE-004（拒绝，不可逆）
- STATE-005（候选人主动撤回）

## 2. 简历本身状态机（Resume）

### FUN-009: 简历解析

#### 2.1 状态定义

| STATE | 状态名 | 说明 | 所属 FUN |
|---|---|---|---|
| STATE-006 | 上传中（uploading） | 文件正在传输 | FUN-009 |
| STATE-007 | 解析中（parsing） | OCR 识别中 | FUN-009 |
| STATE-008 | 解析失败（parse_failed） | OCR 置信度 < 0.7 | FUN-009 |
| STATE-009 | 待补全（incomplete） | 解析后部分字段缺失 | FUN-009 |
| STATE-010 | 可用（active） | 解析成功，可用于投递 | FUN-009 |

#### 2.2 转移表

| STATE-XXX | 事件 | 目标状态 | guard | 副作用 | 所属 FUN |
|---|---|---|---|---|---|
| STATE-006 | 上传完成 | STATE-007 | 文件 > 0 字节 | 触发 OCR | FUN-009 |
| STATE-007 | 解析成功 | STATE-010 | confidence > 0.7（BR 待定） | 存储结构化字段 | FUN-009 |
| STATE-007 | 解析失败 | STATE-008 | confidence ≤ 0.7 | 标记需人工补全 | FUN-009 |
| STATE-008 | 用户重新上传 | STATE-006 | — | 删除原文件 | FUN-009 |
| STATE-009 | 用户手动补全 | STATE-010 | 关键字段完整 | 标记 active | FUN-009 |
| STATE-009 | 用户放弃 | STATE-008 | — | 标记归档 | FUN-009 |

## 3. 职位发布状态机（Job）

### FUN-011: 雇主职位管理

#### 3.1 状态定义

| STATE | 状态名 | 说明 | 所属 FUN |
|---|---|---|---|
| STATE-011 | 草稿（draft） | 雇主编辑中，未发布 | FUN-011 |
| STATE-012 | 招聘中（open） | 已发布，接收投递 | FUN-011 |
| STATE-013 | 暂停（paused） | 雇主临时关闭，HR 仍可看 | FUN-011 |
| STATE-014 | 已关闭（closed） | 招聘完成或取消 | FUN-011 |
| STATE-015 | 已归档（archived） | 超过保留期（BR-013 7 年） | FUN-011 |

#### 3.2 转移表

| STATE-XXX | 事件 | 目标状态 | guard | 副作用 | 所属 FUN |
|---|---|---|---|---|---|
| STATE-011 | 雇主发布 | STATE-012 | 必填字段完整 | 上线职位搜索 | FUN-011 |
| STATE-012 | 雇主暂停 | STATE-013 | — | 隐藏职位搜索 | FUN-011 |
| STATE-013 | 雇主恢复 | STATE-012 | — | 重新上线 | FUN-011 |
| STATE-012 | 雇主关闭 | STATE-014 | — | 隐藏职位 + 通知已投递候选人 | FUN-011 |
| STATE-014 | 超过 30 天 | STATE-015 | — | 自动归档（BR-013） | FUN-011 |

## 4. 通用约束

- **不可跳状态**：除「终态」外，必须经顺序（如 STATE-001 → STATE-002 → STATE-003，不可直接 001 → 003）
- **终态不可回退**：STATE-003/004/005 一旦进入不可逆
- **每次转移写 audit log**（BR-021）

## 5. 与上游一致性

| 上游 | 引用 |
|---|---|
| FEA-002/003 | Application 状态机（投递流程） |
| FEA-006 | HR 标记状态（F-006-2） |
| FEA-009 | Resume 解析状态机（F-002-3） |
| FEA-011 | Job 发布状态机 |
| BR-014/021 | withdrawn 不计漏斗 / 状态变更写 audit |

## 6. 知识状态标注

- 三个状态机（Application / Resume / Job）的状态与转移均源于 FEA 与 FUN 流程的明确行为定义 → **FACT**
- guard 阈值（如 confidence > 0.7、reason ≥ 10 字）为 PM-Office 设定 → **DECISION**
- STATE-015 归档"超过 30 天自动执行"的具体触发时点属运营假设 → **AI_INFERENCE**
- 各终态在入职流程中的后续步骤待 HR 流程确认 → **UNKNOWN**
