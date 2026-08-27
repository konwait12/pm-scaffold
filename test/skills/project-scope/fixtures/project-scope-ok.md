<!--
产物：项目范围基线（PRD §2 唯一上游）
本文件通过 validate_artifact.py —— 四态范围 + 假设/依赖/风险姿态完整。
-->

---
artifact_id: SCOPE-HIRE-001
version: v0.1
status: ready_for_human_review
owner: PM-Office
business_fact_owner: VP of Talent
goal_decision_owner: VP of Talent
reviewer: 待评审
created_at: 2026-08-11
updated_at: 2026-08-11
confirmed_at: 待评审
---

# 项目范围基线

## 1. 结论摘要

- scope_baseline_version: v0.1
- in_count: 3 · out_count: 2 · deferred_count: 1 · conditional_count: 1
- baseline_owner: VP of Talent · baseline_date: 2026-08-11

## 2. In Scope（本期做）

| 范围 ID | 名称 | 描述 | 成功信号 | 优先级 |
|---|---|---|---|---|
| SCOPE-IN-001 | 招聘网站核心流程 | 职位发布 / 申请 / 审核 | 申请完成率 ≥ 90% | P0 |

## 3. Out of Scope（本期不做）

| 范围 ID | 名称 | 不做原因 | 预计回访 |
|---|---|---|---|
| SCOPE-OUT-001 | 第三方平台迁移 | 仅新平台自建，不迁移存量 | 下期评估 |

## 4. Deferred（暂缓）

| 范围 ID | 名称 | 暂缓原因 | 扩展点设计 |
|---|---|---|---|
| SCOPE-DEF-001 | 移动端 App | 本期仅 Web | 预留移动端 API |

## 5. Conditional（条件性）

| 范围 ID | 名称 | 触发条件 | 负责人 | 升级规则 |
|---|---|---|---|---|
| SCOPE-COND-001 | 国际站 | 合规审批通过后纳入 | VP of Talent | 审批通过即转入 In |

## 6. 假设清单

| 假设 ID | 内容 | 知识状态 | 可证伪测试 | 负责人 |
|---|---|---|---|---|
| SCOPE-ASM-001 | 自建招聘网站不依赖第三方平台 | FACT | 部署后核验无外部依赖 | PM-Office |

## 7. 依赖清单

| 依赖 ID | 名称 | 类型 | 负责人 | 计划落地日期 | 单点故障 |
|---|---|---|---|---|---|
| SCOPE-DEP-001 | 招聘 API | 系统 | 后端团队 | 2026-09-30 | 是 |

## 8. 风险姿态

| 轴 | 强度 | 依据 | 缓解 |
|---|---|---|---|
| 合规 | LOW | 本期无跨境数据 | 无 |
| 数据安全 | MEDIUM | 简历含 PII | 加密存储 |
| 资金 | LOW | 自研为主 | 无 |
| 隐私 | MEDIUM | 简历数据 | 最小化采集 |
