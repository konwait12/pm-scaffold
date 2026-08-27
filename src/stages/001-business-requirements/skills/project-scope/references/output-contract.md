# Output Contract · 项目范围产物

## 产物标识

- **文件路径**：`001-business-requirements/02-project-scope/project-scope.md`
- **ID 前缀**：`SCOPE-`（如 `SCOPE-001`、`SCOPE-IN-001`、`SCOPE-OUT-001`、`SCOPE-DEF-001`、`SCOPE-COND-001`）
- **状态**：`draft` / `needs_user_input` / `conditional_review` / `ready_for_human_review`（**绝不 `confirmed`**）

## 主干章节契约

```yaml
required_sections:
  - id: §1
    title: 结论摘要
    must_contain: [scope_baseline_version, in_count, out_count, deferred_count, conditional_count, baseline_owner, baseline_date]
  - id: §2
    title: In Scope（本期做）
    must_contain: [scope_id, name, description, success_signal, priority]
  - id: §3
    title: Out of Scope（本期不做）
    must_contain: [scope_id, name, reason_for_out, anticipated_revisit]
  - id: §4
    title: Deferred（暂缓）
    must_contain: [scope_id, name, deferral_reason, extension_point_design]
  - id: §5
    title: Conditional（条件性）
    must_contain: [scope_id, name, trigger_condition, owner, escalation_rule]
  - id: §6
    title: 假设清单
    must_contain: [assumption_id, content, knowledge_state_labels, falsifiable_test, owner]
  - id: §7
    title: 依赖清单
    must_contain: [dep_id, name, type, owner, planned_landing_date, single_point_of_failure]
  - id: §8
    title: 风险姿态
    must_contain: [axis=合规/数据安全/资金/隐私, level=HIGH/MEDIUM/LOW, rationale, mitigation]

validation:
  - §2 / §3 / §4 / §5 四态每态至少 1 行（除非显式声明"无 Conditional 项"）
  - §6 每条假设必须标 F/D/A/AI/U/C 知识状态 + 可证伪测试
  - §7 每个关键依赖必须有 Owner + 计划落地日期
  - §8 四轴每轴必须给 HIGH/MEDIUM/LOW 强度
  - 范围变化（任一 In/Out/Deferred/Conditional 行被改/增/删）→ 必须回流到本 skill 改 §1 的 scope_baseline_version
```

## 与下游关系

- `user-journey` 引用 `project-scope.In` 作为旅程触点边界
- `user-stories` 引用 `project-scope.In` 作为故事范围，引用 `Out` 作为非故事依据
- `feature-list` 引用 `project-scope.In + Conditional` 作为功能点来源
- `functional-flow` 不在本 scope 内但只在 `In` 范围内展开
- `prd-assembly` 投影本 skill 全部到 prd.md §2 项目范围

## 与上游关系

- `project-background-goal.predecessors` 含本 skill
- `feasibility-analysis` 的"风险姿态"章节是本 skill §8 输入

## 与 PRD 章节映射

`artifact_types` 中 `project-scope.prd_destination` 是「§2 项目范围（In/Out/Deferred/Conditional + 假设 + 依赖 + 风险姿态）」——这是 prd.md §2 的唯一上游。

`artifact_types` 中 `project-background-goal.prd_destination` 由 "§1 业务一句话 + §1.1 立项依据（含市场/技术/投入产出/风险四维评估）+ §1.2 项目背景 + §1.3 目标" 改为 "§1 业务一句话 + §1.1 立项依据 + §1.2 项目背景 + §1.3 目标"（去掉"范围基线"字样，因为 §2 已独立）。

## 范围变更回流机制

当后续 UJ/US/FE 中任一项发现"实际需要 §X 范围外能力"时：
1. 在对应 work item 产物末尾标注 `## scope_ref: SCOPE-XXX` 引用本 skill
2. 由 reviewer 在 `99-review/support/reflow.md` 记录回流决策
3. project-scope 重做 → §1 `scope_baseline_version` 升级 → 全部下游 rebi