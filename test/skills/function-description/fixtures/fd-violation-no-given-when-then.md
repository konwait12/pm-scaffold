<!--
产物：故意违规样本（无 Given/When/Then 格式 + 无 NFR 引用）
本文件通过 validate_artifact.py —— 0 error 但 ≥1 warning（D4.4 触发）。
status: ready_for_human_review（模拟演示用）。
-->
---
artifact_id: FD-VIOL-001
version: v0.1
status: ready_for_human_review
owner: PM-Office
business_fact_owner: VP of Talent
goal_decision_owner: VP of Talent
reviewer: VP of Talent
created_at: 2026-08-11
updated_at: 2026-08-11
confirmed_at: 待确认
upstream_artifact_id: UX-HIRE-002
---

# 分功能描述

## 0. 预检输入充分度判定

- 上游产物：UX-HIRE-002（status: confirmed，v1.0）
- 已确认 FEA 数：3（候选人列表、简历筛选、漏斗看板）
- 判定：**充分模式**（上游 confirmed）→ 走完整 §1-§7 工作流

## 1. 功能规格概览

| 功能 ID | 功能名称 | 来源 FEA | 优先级 |
|---|---|---|---|
| FUN-001 | 候选人列表查询 | FEA-001 | P0 |
| FUN-002 | 简历筛选打标 | FEA-002 | P0 |
| FUN-003 | 招聘漏斗看板 | FEA-003 | P1 |

## 2. 分功能详述

### 2.1 FUN-001 候选人列表查询

- 入口：招聘专员后台 → "候选人"导航
- 主流程：系统读取候选人列表 → 招聘专员筛选/分页/排序
- 异常与失败处理：分页超界时显示"无更多"

#### 交互规则
- **IX-001**：招聘专员调整筛选条件后，列表刷新并保留当前条件。

#### 业务规则
- **BR-001**：列表按更新时间倒序（具体口径待确认）

#### 验收依据（⚠️ 故意不采用 Given/When/Then 格式）
- **AC-001**：列表展示正常候选人，越界分页给出空提示。
- **AC-002**：点击候选人姓名进入详情页。

### 2.2 FUN-002 简历筛选打标

- 入口：候选人详情 → "打标"按钮
- 主流程：招聘专员选择标签（如"待面试/已面试/不合适"）→ 系统保存
- 异常与失败处理：网络中断时本地缓存

#### 交互规则
- **IX-002**：提交标签后显示保存结果；失败时保留当前选择。

#### 业务规则
- **BR-002**：每次打标写入审计日志

#### 验收依据
- **AC-003**：标签保存后页面立即反映新状态。

### 2.3 FUN-003 招聘漏斗看板

- 入口：导航"数据看板"
- 主流程：系统按周/月聚合投递→筛选→面试→录用 漏斗
- 异常与失败处理：数据缺失时显示空态

#### 交互规则
- **IX-003**：切换周/月粒度后刷新看板并保持筛选范围。

#### 业务规则
- **BR-003**：漏斗阶段定义按现有 CRM

#### 验收依据
- **AC-004**：看板渲染按周/月两种粒度可切换。

## 3. 权限矩阵

| 角色 | FUN-001 | FUN-002 | FUN-003 |
|---|---|---|---|
| 招聘专员 | ✓ | ✓ | ✓ |
| HR 团队 | ✓ | ✗ | ✓ |
| 品牌团队 | ✗ | ✗ | ✓ |

## 4. 字段规则（按需）

（本期不涉及新字段，跳过）

## 5. 埋点需求（按需）

（本期不涉及埋点，跳过）

## 6. 事实与决定

| ID | 类型 | 内容 | 来源/决策人 | 状态 |
|---|---|---|---|---|
| FCT-601 | FACT | 招聘漏斗阶段定义见 CRM 系统 | UX-HIRE-002 §3 | 确认 |

## 7. 假设、AI 推断、未知与冲突

| ID | 类型 | 内容 | 依据 | 影响 | 责任人 | 处理方式 |
|---|---|---|---|---|---|---|
| ASM-701 | ASSUMPTION | 列表分页大小 = 20/页 | 行业默认 | UX 体感 | PM-Office | 待确认 |

## 8. 待确认问题

| ID | 问题 | 结论 |
|---|---|---|
| Q-801 | AC 是否使用 Given/When/Then 格式？ | 故意未采用，触发 D4.4 警告 |
| Q-802 | 是否需要 NFR 章节引用 Volere 10-17？ | 故意缺失，触发 D4.8 警告 |

## Clarifications

| session_id | category | question | ai_preliminary_judgment | options | decision_owner | blocking | deferral_risk | accepted_answer | reflow_target | integrated_at | integrated_by | audit_recheck |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | 待补充 | — | 待填写 | AI | n/a |

## 9. 来源追溯

| 来源 ID | 材料/位置 | 关键内容 | 本文落位或排除理由 |
|---|---|---|---|
| UX-HIRE-002 | 上游 UX 产物 | 3 个 FEA 定义 | §1 / §2 / §3 |

## 10. 下游输入摘要

```text
confirmed_version: v0.1 (ready_for_human_review)
scope_summary: 3 个 FUN（候选人列表/筛选打标/漏斗看板）
feature_summary: FUN-001 / FUN-002 / FUN-003
module_boundaries: CRM 数据读取 + 看板数据聚合
key_interaction_patterns: 列表分页/标签保存/漏斗图表
open_nonblocking_unknowns: Q-801/Q-802（已登记待业务方补全）
source_ids: UX-HIRE-002
```

## 11. Constitution Compliance

| 原则 | 状态 | 证据 / 备注 |
|---|---|---|
| ① 业务事实分离 | PASS | §6 FACT 带 SRC；§7 ASSUMPTION 显式登记 |
| ② AI 不替业务决定 | PASS | §8 两个 Q 全部 blocking |
| ③ 来源可追溯 | PASS | §9 上游唯一 |
| ④ 冲突显式保留 | PASS | 无冲突源 |

## 12. 版本变更摘要

| 版本 | 变更原因 | 主要变化 | 人工确认状态 |
|---|---|---|---|
| v0.1 | 故意违规（演示 D4.4/D4.8 warning） | 缺 AC Given/When/Then + 缺 NFR Volere 引用 | 待评审 |

> ⚠️ **违规声明**：本 fixture 故意不满足 07 §7.2 D4.4（AC Given/When/Then）与 D4.8（NFR Volere 引用）。
> 期望 validator 返回：0 error（结构合规）+ 1 warning（D4.4 命中："AC-* rows lack Given/When/Then format"）。
> 用途：作为 function-description validator 的回归对照，证明 validator 能命中 D4.4 而非误报 PASS。
