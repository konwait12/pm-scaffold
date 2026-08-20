---
artifact_id: "MP-001"
version: "v0.1"
status: "draft"
owner: "nova"
business_fact_owner: "nova"
goal_decision_owner: "nova"
reviewer: "nova"
created_at: "2026-08-20"
updated_at: "2026-08-20"
confirmed_at: ""
process_tier: "L0"
upstream_artifact_ids: ["SRC-003"]
---

# 轻量 PRD（Mini PRD）

## 1. 改什么

活动详情页「报名截止」文案由「2026-08-31」改为「2026-08-30」。文件：src/pages/activity/detail.tsx 字段 deadlineLabel。目标：截止时间展示与后端配置一致。

## 2. 为什么

后端 RSVP 服务返回的活动截止时间为 2026-08-30（SRC-003 活动配置），前端硬编码文案少一天，用户会按错误日期操作。

## 3. 影响范围

仅活动详情页文案展示。影响入口：活动详情页。角色：客人（查看）。回滚：恢复原文案即可，无数据写入。

## 4. 行为需求与验收

Given 活动截止时间为 2026-08-30，When 用户打开活动详情页，Then 展示「报名截止 2026-08-30」，通过截图比对可判定。

## 5. 异常与边界

后端返回空截止时间时，展示「报名截止时间待定」，不展示硬编码日期。

## 6. 依赖与开口问题

无外部依赖。开口问题：文案是否需要按用户时区格式化（owner：nova，影响：展示粒度）。
