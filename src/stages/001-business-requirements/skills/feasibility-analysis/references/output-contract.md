# Output Contract · 可行性分析产物

## 产物标识

- **文件路径**：`001-business-requirements/00-feasibility-analysis/feasibility-report.md`
- **ID 前缀**：`FA-`（按子章节有 `FA-MKT-`、`FA-TECH-`、`FA-COST-`、`FA-RISK-`、`FA-MULTI-`）
- **状态**：`draft` / `needs_user_input` / `conditional_review`（**绝不 `confirmed`**）

## 主干章节契约

```yaml
required_sections:
  - id: §1
    title: 结论摘要
    must_contain: [decision_go/no_go/conditional_go, ai_confidence, decision_owner, decision_date]
  - id: §2
    title: 市场空间
    must_contain: [target_users, market_size_estimate, source_refs]
  - id: §3
    title: 技术可行性
    must_contain: [challenges_table, validation_status]
  - id: §4
    title: 投入产出
    must_contain: [cost_estimate, revenue_estimate, payback_period, knowledge_state_labels]
  - id: §5
    title: 风险评估
    must_contain: [risk_table_with_impact_probability_mitigation]
  - id: §6 (conditional)
    title: 多方案取舍
    trigger: 当存在 ≥2 个实质不同的方案时强制出现
    must_contain: [weighted_decision_matrix, weights_defined_before_scoring, sensitivity_analysis]
  - id: §7
    title: 附录：来源与未决项
    must_contain: [src_register, open_questions, conflict_log]

validation:
  - 四维度每个都必须有证据来源或显式假设（不能空）
  - §6 权重必须在打分前定义（锚定检查）
  - 推荐必须带 HIGH/MEDIUM/LOW 置信度 + 关键假设列表
  - 至少一条 DECISION 记录（DecisionRecord DEC-XXX）落 DecisionOwner
```

## 与下游关系

- `project-background-goal.predecessors` 含 `feasibility-analysis`
- FA 产出 `decision: no_go` → BG 不能开始；整个 REQ 终止
- FA 产出 `decision: conditional_go` → BG 必须引用 FA 的"条件"作为前置约束
- FA 产出 `decision: go` → BG 可以引用 FA 摘要作为"项目立项依据"

## 与 PRD 章节映射

`artifact_types` 中 `feasibility-report.prd_destination` 是「§1 立项背景（含市场/技术/投入产出/风险四维评估）」——FA 摘要进入 prd.md §1 顶部。
