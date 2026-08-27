<!--
产物：字段规则说明（PRD §9.2 字段清单唯一上游）
本文件通过 validate_artifact.py —— 字段定义表 F-XXX 完整 + 与 VL 反向绑定。
-->

---
artifact_id: FIELDS-HIRE-001
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

# 字段规则说明

## 1. 字段清单总览

- field_count: 3 · required_count: 2 · optional_count: 1 · system_generated_count: 1
- baseline_version: v0.1

## 2. 字段定义表

| F-XXX | 中文名 | 英文名 | DB 字段 | 类型 | 长度/范围 | 必填 | 默认值 | 唯一性 | 来源 | 关联校验 VL |
|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | 手机号 | phone | phone | string | 11 | 是 | 无 | 全局唯一 | 用户填写 | VL-001 |
| F-002 | 申请日期 | apply_date | apply_date | date | YYYY-MM-DD | 是 | now() | 不唯一 | 系统生成 | VL-002 |
| F-003 | 备注 | note | note | string | 200 | 否 | 空 | 不唯一 | 用户填写 | TBD-VL |

## 3. 字段来源说明

| F-XXX | 业务含义 | 上游 skill | 来源 skill |
|---|---|---|---|
| F-001 | 用户联系方式 | feature-list FEA-001 | page-design PD-001 |
| F-002 | 申请提交日期 | functional-flow FF-001 | feature-list FEA-002 |
| F-003 | 申请补充说明 | interaction-rules IX-001 | page-design PD-002 |

## 4. 字段与校验（VL）反向绑定

| VL-XXX | 校验字段 | 校验类型 | 错误信息 |
|---|---|---|---|
| VL-001 | F-001 | 格式 + 唯一性 | 手机号格式不正确 |
| VL-002 | F-002 | 必填 + 日期范围 | 申请日期不能为空 |
