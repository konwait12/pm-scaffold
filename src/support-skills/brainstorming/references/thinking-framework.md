# Thinking Framework（Brainstorming）

Use these lenses to improve the candidate set. Do not dump the full analysis into the artifact — record only findings that become candidates.

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before disposition close, Fresh-Eyes before Human Gate, Testability before write-back, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate set — do not repeat core-lens analysis verbatim.

## First Principles

- What observable result does this idea want to change?
- What underlying problem exists without the proposed feature?
- Why now?
- Which claims are assumptions disguised as requirements?

## Divergence Domain Lenses（发散领域 lens）

Divergent exploration sweeps the **12 scenario dimensions** from `src/shared/brainstorming/SCENARIO_EXPANSION.md`. For each dimension, ask the corresponding question and emit candidate ideas; stop a dimension once candidates repeat (saturation):

| # | 维度 Dimension | 发散提问 |
|---|---|---|
| 1 | lifecycle 生命周期 | 这件事从开始到结束有哪些阶段？当前停留在哪个阶段？ |
| 2 | roles 角色 | 谁会发起、执行、受益、受扰？每类角色的动机与顾虑？ |
| 3 | normal / alternate / exception / failure / timeout 正常·备选·异常·失败·超时 | 主路径是什么？备选路径？系统失败与超时怎么处理？ |
| 4 | permission 权限 | 谁有权限做什么？不同角色看到的范围是否不同？ |
| 5 | data condition 数据条件 | 哪些数据必须存在才能继续？数据缺失/脏数据怎么办？ |
| 6 | handoff 交接 | 哪个节点从一个人/系统交接到另一个人/系统？ |
| 7 | dependency 依赖 | 依赖哪些内部系统、外部供应商、审批或时间窗口？ |
| 8 | cancellation 取消 | 事情中途取消的触发条件与善后是什么？ |
| 9 | retry 重试 | 哪些步骤需要重试？重试上限与策略？ |
| 10 | rollback 回滚 | 已生效的结果能否回滚？回滚的代价与边界？ |
| 11 | change-recovery 变更恢复 | 需求或方案变更后，如何恢复到一致状态？ |
| 12 | constraint 约束扫描 | 时间、预算、技术、合规四类约束的候选边界？ |

## Clustering And Deduplication

- Merge candidates that express the same distinct idea with different wording; keep the clearest phrasing.
- A candidate that spans two dimensions stays in its primary dimension; cross-reference the other dimension in the Candidate cell.
- Saturation rule: when a dimension produces no new distinct idea for two consecutive passes, stop that dimension.

## Adversarial Review

- Is the stated idea only a symptom of an unstated problem?
- Could a policy/process change satisfy it without any product change?
- Is the evidence for a candidate from one interested party only?
- Which candidate would survive if the idea were rewritten in the opposite direction?

## Reverse Validation

Starting from the intended outcome, ask what must be true for success; use the result to reveal missing prerequisites, dependencies, baseline data, and constraints as new candidates.

## Knowledge Boundary

- Every candidate is `AI_INFERENCE` until the human marks it `include`; nothing in the divergent set is a business fact.
- Evidence must state *why the AI thinks this* (from the raw idea, a registered source, or common practice) — never present inference as observation.
- `research` disposition means "not decidable now": register it in issue-record / a QuestionRecord instead of leaving it silently.

## Sparse Degradation Mode（稀疏降级）

When the input is a single sentence with no materials and the responsible human is unavailable or has not answered the first batch of questions, divergence still works but output degrades:

```text
sparse input → diverge into candidate skeletons (short evidence: "AI 推断，无书面来源")
             → do not force complete Evidence/Impact
             → batch ≤5 clarifying questions (each: AI preliminary judgment + options + impact + owner)
             → status = needs_user_input
             → wait for human answers, then re-enter Generate in sufficient mode
```

Degradation triggers (any one is enough):

- input length < 50 characters AND no materials
- no business domain, no role mentioned, no time constraint
- the idea mentions only a feature or implementation ("做一个打卡功能"), with no business context

This mode is not a failure state. It produces one clean batch of clarifying questions instead of a bloated candidate table full of `待确认`.
