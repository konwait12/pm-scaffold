# 审计清单 · Brainstorming（发散收敛）

## 结构闸门（Structural Gate）

- 所有必需标题存在：按 `src/templates/others/brainstorming-output.md` 的 `## 原始输入` / `## 发散结果` / `## 候选清单` / `## 人工处置表` / `## Include 项写回` / `## 收敛后输入包`，并包含 `## Constitution Compliance` 与 `## 版本变更摘要`。
- frontmatter 完整：含产物 ID、版本（起 `v0.1`）、状态（绝不 `confirmed`）、负责人、stakeholder、评审人，以及日期或 `待确认` / `TBD`。
- `## 原始输入` 注明触发路径与证据边界（L0 无源时明示"其余皆为推断"）；如登记了来源，能指向 `SRC-*`。
- `## Constitution Compliance` 存在（即使结论为 N/A）。

## 发散覆盖闸门（Divergence Coverage Gate）

- 12 维度全部扫过或显式跳过：lifecycle / roles / normal-alternate-exception-failure-timeout / permission / data condition / handoff / dependency / cancellation / retry / rollback / change-recovery / constraint。
- 每个被跳过的维度都在 `## 发散结果` 注明"为何跳过"，而非默认省略。
- 每个独立想法都有稳定 ID `SCN-XXX`，去重后单调递增。

## 语义闸门（Semantic Gate）

- **候选原子性**：一行一个候选；没有候选塞进两条独立诉求。
- **全表 AI_INFERENCE**：每条候选知识状态均为 `AI_INFERENCE`；无任何内容被当成事实（仅在显式 `SRC-*` 支持时才可有 FACT）。
- **无内容当事实**：Evidence 说明 AI 为什么这么想，不是陈述业务事实；绝无占位或空。
- **无方案泄露**：候选里若夹带方案（"做个兑换页"），它是一行候选的提示，不是已确认决策。
- **处置表就绪**：8 列处置表已生成；每个 `include` 行都给了**非占位** Write-back Target；`exclude` 有原因、`defer` 有触发条件、`research` 已登记 issue-record / QuestionRecord。

## 人工闸门（Human Gate）

- **发散覆盖摘要**就绪：哪些维度产出什么，交代清楚。
- 处置表准备好供业务方自行填写 `include` / `exclude` / `defer` / `research`。
- 本记录状态**仅 `ready_for_human_review`**，**绝不 `confirmed`**；`confirmed` 只可来自 `pipeline.py review --decision approve` 对下游工作项的确认。

## 审计报告形态（Audit Report Shape）

```text
status_recommendation
passed_checks
failed_checks
repairs_applied
scn_count
divergence_coverage
included_candidates
deferred_candidates
research_count
downstream_risks
```