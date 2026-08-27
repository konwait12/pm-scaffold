<!--
产物模板：PRD 汇总（v8 reader-facing contract）

本文件只定义最终 PRD 的产品交付边界：它必须能独立阅读、可执行、可验收，
但不能把上游产物全文、过程审查、AI 自审或审计记录复制进正文。
完整来源、段落选择、哈希、追溯报告和评审证据由 prd-assembly-manifest.json、
99-review/ 与 .audit/ 保存。

三档边界：
- L0：mini-prd 六类事实的精简确定性投影；不制造 L2 深度章节。
- L1：7 个上游的产品摘要；页面、交互、字段校验、状态、异常实际适用时升级 L2。
- L2：12 个上游的完整产品规格；按职责去重整合，不逐篇复制上游全文。

v7 存量产物保持只读兼容；新产物使用 v8。
-->
---
artifact_id: ""
version: "v0.1"
status: "draft"
owner: ""
business_fact_owner: ""
goal_decision_owner: ""
reviewer: ""
created_at: ""
updated_at: ""
confirmed_at: ""
prd_structure_version: "8"
reader_contract_version: "2"
process_tier: "L2"
applicability_contract_version: "1"
upstream_artifact_ids: []
upstream_work_item_statuses: ""
---

# PRD（产品需求文档）

> 本文只呈现已确认的产品事实、决定、范围、行为、规则、失败边界和验收标准。
> FACT / DECISION / ASSUMPTION / AI_INFERENCE / UNKNOWN / CONFLICT 必须保留在业务声明旁。
> 来源 artifact ID 与 Trace ID 保留在正文；完整选择器、哈希和审计证据见项目侧 manifest 与评审记录。

## 1. 项目背景

<!-- applicability: status=required; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

<!-- 只放问题、现状、目标、成功标准和约束的业务摘要；不得复制上游质量记录。 -->

待生成

## 2. 项目范围

<!-- applicability: status=required; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

<!-- 明确 In / Out / Deferred / Conditional、假设与依赖；不把治理边界伪装成业务范围。 -->

待生成

## 3. 用户与用户旅程

<!-- applicability: status=required; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

<!-- 只保留受影响角色、关键生命周期、入口、正常/备选/异常/恢复路径。 -->

待生成

## 4. 用户故事与优先级

<!-- applicability: status=required; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

<!-- 保留 ST、价值、优先级和必要的覆盖关系；不要再次复制整份 user-stories。 -->

待生成

## 5. 功能清单

<!-- applicability: status=required; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

<!-- 只保留功能总账、边界、优先级、入口和关键依赖；每项应能回到故事。 -->

待生成

## 6. 功能流程

<!-- applicability: status=required; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

<!-- 只保留可执行的主流程、必要分支、失败/恢复路径和跨系统交接；图按需保留。 -->

待生成

## 7. 页面与体验

<!-- applicability: status=conditional; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

<!-- 仅当页面结构、布局、字段或体验实际变化时生成；L1 无依据时不生成本节。 -->

按需生成

## 8. 交互规则

<!-- applicability: status=conditional; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

<!-- 仅保留新的操作、反馈、表单、弹窗、加载/空/错态和可观察交互。 -->

按需生成

## 9. 业务规则

<!-- applicability: status=required; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

### 9.1 计算与流程规则

<!-- applicability: status=required; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

待生成

### 9.2 校验规则

<!-- applicability: status=conditional; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

按需生成

### 9.3 状态变化

<!-- applicability: status=conditional; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

按需生成

### 9.4 异常处理与恢复

<!-- applicability: status=conditional; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

按需生成

## 10. 验收标准

<!-- applicability: status=required; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

<!-- AC 必须可观察、可判定，并回到故事/功能；不要在这里重复全量流程或规则。 -->

待生成

## 11. 依赖与待决业务问题

<!-- applicability: status=conditional; basis=; source=; decided_by=; decided_at=; trigger=; current_judgment=; review_trigger= -->

<!-- 只有存在真实 Q-/UNK-/ISS-/DEC- 事实时生成；问题的完整收口记录不在 PRD。 -->

按需生成
