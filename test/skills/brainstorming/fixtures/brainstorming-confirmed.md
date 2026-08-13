<!--
⚠️ Fixture 声明：本文件是回归演示样本，非真实需求产物。所有人物姓名、公司名、城市名、财务数字、业务指标均为通用占位符，仅用于演示产物结构。任何与现实业务的相似性纯属巧合。
-->
---
artifact_id: BS-INVITE-001
version: v0.1
status: ready_for_human_review
owner: 产品经理A（占位）
reviewer: 业务方负责人B（占位）
created_at: 2026-08-13
updated_at: 2026-08-13
confirmed_at: （授权人工 review 后填写）
---

# 头脑风暴输出（Brainstorming Output）

## 1. 原始输入

一句话原始输入：业务方代表A 提出「做客户邀约活动」，客户名单约 500 人，但邀约方式、邀约内容、活动目标均未定义。

- 触发路径：L0 仅想法（00-input 无源材料）→ 入口路由建议 brainstorming 发散收敛
- 证据边界：仅上述一句话，无附件、无书面材料；除原始想法原文外全部候选均为 AI_INFERENCE

## 2. 发散结果

按 12 维度发散（lifecycle / roles / normal-alternate-exception-failure-timeout / permission / data condition / handoff / dependency / cancellation / retry / rollback / change-recovery），聚类去重后得 4 条候选：

- 生命周期：名单准备 → 邀请发出 → RSVP 回收 → 到场签到 → 会后回访
- 角色：业务方活动组织者（发起与处置）、受邀客户（参加/不参加）、现场接待人员（签到执行）
- 异常：邀约名单中有客户联系失败（号码失效/拒收）；活动当天临时缺席
- 依赖：邀约渠道（短信/邮件）供应商接口与发送配额

## 3. 候选清单（全部 AI_INFERENCE）

| Candidate ID | 发散维度 | Candidate | Evidence | Impact | 知识状态 |
|---|---|---|---|---|---|
| SCN-001 | lifecycle | 邀约生命周期五阶段：名单准备→邀请发出→RSVP→到场签到→会后回访 | 原始输入仅提到「邀约活动」，生命周期为 AI 按标准活动流程推断 | 为后续旅程与功能划分提供骨架，直接影响范围基线 | AI_INFERENCE |
| SCN-002 | roles | 三类角色：活动组织者 / 受邀客户 / 现场接待 | 原始输入未提及角色，为 AI 按活动流程推断 | 决定下游角色清单与权限视角 | AI_INFERENCE |
| SCN-003 | exception | 联系失败与临时缺席两类异常场景 | 邀约类业务常见失败模式推断 | 影响异常处理与到场率目标设计 | AI_INFERENCE |
| SCN-004 | dependency | 邀约渠道（短信/邮件）供应商接口与发送配额 | AI 推测，需调研确认渠道现状 | 决定邀约发放的可行性与时间约束 | AI_INFERENCE |

## 4. 人工处置表

| Candidate ID | Role-Lifecycle | Candidate | Evidence | Impact | Human Disposition | Reason | Write-back Target |
|---|---|---|---|---|---|---|---|
| SCN-001 | lifecycle | 邀约生命周期五阶段 | 同 §3 SCN-001（AI_INFERENCE） | 旅程与功能骨架 | include | 业务方代表A 确认符合活动预期 | 输入包 §生命周期线索 |
| SCN-002 | roles | 三类角色 | 同 §3 SCN-002（AI_INFERENCE） | 角色清单与权限视角 | include | 业务方代表A 确认三类角色成立 | 输入包 §角色候选 |
| SCN-003 | exception | 联系失败与临时缺席 | 同 §3 SCN-003（AI_INFERENCE） | 异常与到场率目标 | defer | 本期先做基线流程，异常场景二期评估 | 输入包 §约束候选（暂缓） |
| SCN-004 | dependency | 短信/邮件渠道依赖 | 同 §3 SCN-004（AI_INFERENCE） | 邀约可行性与时间约束 | research | 渠道现状与供应商能力待调研 | 登记 issue-record ISS-301（待调研） |

## 5. Include 项写回（写回 `project-background-goal` 输入包）

| SCN-ID | 写回内容 | 写回目标章节 |
|---|---|---|
| SCN-001 | 邀约生命周期五阶段：名单准备→邀请发出→RSVP→到场签到→会后回访 | 输入包 §生命周期线索 |
| SCN-002 | 活动组织者 / 受邀客户 / 现场接待三类角色 | 输入包 §角色候选 |

## 6. 收敛后输入包（交付 `project-background-goal`）

业务方代表A 提出客户邀约活动，名单约 500 人，邀约方式与内容未定义。人工处置确认：邀约生命周期五阶段（名单准备→邀请发出→RSVP→到场签到→会后回访）与三类角色（活动组织者/受邀客户/现场接待）纳入输入包；联系失败与临时缺席异常场景暂缓（二期）；短信/邮件渠道依赖待调研（已登记 issue-record ISS-301）。建议 background-goal 沿生命周期与角色展开现状、问题与目标。

## 7. 版本变更摘要

- v0.1: 初稿（L0 触发，12 维度发散聚类得 4 条候选，人工处置 2 include / 1 defer / 1 research）
