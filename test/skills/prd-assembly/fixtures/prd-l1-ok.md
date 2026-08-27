<!--
产物：PRD 汇总 · L1 标准档（v8 结构）· process_tier=L1
L1 走 7 个上游（BG/UJ/US/FL/FF/BR/AC）；PRD 汇总章节结构与 L2 完全同构，
§7 原型/UX、§8 交互规则、§9.2-§9.4 校验规则/状态变化/异常处理均保留章节骨架，
以「本期不适用 + 承接依据」从简承载（依据源自 intake-decision.md），不整章省略，
也不内嵌真实 L2-only 规则（无 VL-/STATE-/EX- ID）。
本 fixture 用于验证 prd-assembly validator 的 V8_L1 分叉。
-->
---
artifact_id: PRD-L1-001
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
applicability_contract_version: "1"
upstream_artifact_ids: ["BG-001", "UJ-001", "US-001", "FL-001", "FF-001", "BR-001", "AC-001"]
upstream_work_item_statuses: "feasibility-analysis project-background-goal project-scope user-journey user-stories feature-list functional-flow business-rules acceptance-criteria"
---

# PRD（产品需求文档）

## 1. 项目背景

<!-- applicability: status=required; basis=目标背景是 PRD 的共同事实基线; source=BG-001; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=必须提供; review_trigger=目标变化时复审 -->

G-001 目标：提升活动提醒触达率。

## 2. 项目范围

<!-- applicability: status=required; basis=范围边界决定交付; source=US-001/FL-001; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=必须提供; review_trigger=范围变化时复审 -->

In: 活动前 24h 红点提醒；Out: 跨端同步。

## 3. 用户旅程

<!-- applicability: status=required; basis=需要说明受影响角色路径; source=UJ-001; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=必须提供; review_trigger=角色变化时复审 -->

UJ-001 生命周期表：邀请触达 → 预约登记 → 活动前提醒。

## 4. 用户故事

<!-- applicability: status=required; basis=需求需追溯到用户价值; source=US-001; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=必须提供; review_trigger=目标变化时复审 -->

ST-001 As a 客人，我想要收到活动提醒，这样 不错过活动。

## 5. 功能清单

<!-- applicability: status=required; basis=功能范围需可实施; source=FL-001; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=必须提供; review_trigger=功能变化时复审 -->

FEA-001 活动提醒红点（ST-001，P0）。

## 6. 功能流程

<!-- applicability: status=required; basis=行为需可观察和验收; source=FF-001; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=必须提供; review_trigger=流程变化时复审 -->

主流程 Mermaid：FEA-001 触发 → 展示 → 点击 → 消失。

## 7. 原型/UX

<!-- applicability: status=not_applicable; basis=本次只修改既有提醒配置，不改变页面结构或用户体验; source=intake-decision.md#PD; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=不引入页面或体验变化; review_trigger=新增页面、布局或导航时升级 L2 -->

本期不适用：本次需求仅修改既有活动提醒设置，无新增页面（依据：intake-decision.md §L2-only-inapplicable）。

## 8. 交互规则

<!-- applicability: status=not_applicable; basis=既有页面交互不变，本需求不新增操作反馈或表单规则; source=intake-decision.md#IX; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=不引入新交互; review_trigger=新增交互或反馈状态时升级 L2 -->

本期不适用：涉及交互的既有页面已上线，本 REQ 不引入新交互（依据：intake-decision.md §L2-only-inapplicable）。

## 9. 业务规则

### 9.1 计算与流程规则

<!-- applicability: status=required; basis=提醒触发规则必须可验证; source=BR-001; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=必须提供; review_trigger=阈值变化时复审 -->

BR-001 活动开始前 24h 触发提醒（FEA-001）。

### 9.2 校验规则

<!-- applicability: status=not_applicable; basis=本需求无新增输入字段或跨字段约束; source=intake-decision.md#VL; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=不引入新校验; review_trigger=新增字段或校验时升级 L2 -->

本期不适用：输入字段定义由既有系统规则承接（依据：intake-decision.md §L2-only-inapplicable）。

### 9.3 状态变化

<!-- applicability: status=not_applicable; basis=本需求不新增持久状态、事件、守卫或副作用; source=intake-decision.md#STATE; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=状态语义保持不变; review_trigger=出现状态模型时升级 L2 -->

本期不适用：本 REQ 不涉及状态变更（依据：intake-decision.md §L2-only-inapplicable）。

### 9.4 异常处理

<!-- applicability: status=not_applicable; basis=失败语义和既有兜底逻辑不变，不新增恢复或人工升级路径; source=intake-decision.md#EX; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=不引入新异常语义; review_trigger=新增失败模式时升级 L2 -->

本期不适用：失败语义不变，由既有兜底逻辑承接（依据：intake-decision.md §L2-only-inapplicable）。

## 10. 验收依据

<!-- applicability: status=required; basis=发布必须有可判定验收; source=AC-001; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=必须提供; review_trigger=验收行为变化时复审 -->

AC-001 Given 活动开始前 24h，When 触发提醒，Then 红点展示且可点击。

## 11. 按需章节

<!-- applicability: status=not_applicable; basis=本 REQ 没有竞品、埋点、术语或职责等额外已确认来源; source=intake-decision.md#canonical-11; decided_by=nova; decided_at=2026-08-20; trigger=; current_judgment=当前无需额外按需章节; review_trigger=出现新的已确认按需来源时补齐 -->

当前没有可装配的按需章节事实；如新增竞品、埋点、可行性、术语或职责来源，则在装配前复审。

## 需求追溯矩阵

| 目标 (G) | 故事 (ST) | 功能 (FEA) | 功能详述 (FUN) | 验收 (AC) | 适用证据 (BR/VL/STATE/EX/PD/IX) |
|---|---|---|---|---|---|
| G-001 | ST-001 | FEA-001 | FF-001 主流程 | AC-001 | BR-001 |

## 自审记录（Constitution Compliance）

| 原则 | 状态 | 证据 / 备注 |
|---|---|---|
| ① 业务事实分离 | PASS | 内容全部来自 7 个已确认上游；L2-only 章节为不适用承载 |
| ② AI 不替业务决定 | PASS | 无新增需求 |
| ③ 来源可追溯 | PASS | 每个 FEA/AC 追溯 ST/G |
| ④ 冲突显式保留并关闭 | PASS | 无冲突 |
