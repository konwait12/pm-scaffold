# Thinking Framework · Requirement Restate（双模式能力）

Use these lenses to improve the candidate / candidate set. Do not dump the full analysis into the artifact — record only findings that change the restatement (模式一) or become candidates (模式二).

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

---

## 模式一 · 需求复述（RR-NNN）lens

### Source Fidelity

The restate artifact is worthless if it does not faithfully reflect the source:

- Does every RR-NNN row trace to a concrete SRC-ID, down to paragraph or timestamp?
- Is the `original_phrase` verbatim (dialect, colloquialisms preserved) rather than cleaned up?
- Is the restatement a translation of the source, not an interpretation on top of it?
- Is the "restate vs original" diff the whole point — not smoothed away?

### Atomicity

- Does any row bundle two distinct asks?
- Is every row testable as a single claim a stakeholder can say yes/no to?
- If a row needs "and also…" to be complete, split it.

### No Solution Leak

- Does any row contain a proposed solution, technology, or design ("build a mobile app", "use QR codes")?
- Is a solution mentioned in the source recorded as a *hint* with `solution_leak=true`, not as a decision?
- Would a developer reading the restatement start designing before the ask is confirmed?

### Stakeholder Recognition

- Would the stakeholder recognize their own words in every row?
- Is the phrasing the stakeholder's, or the AI's restatement in its own vocabulary?
- Can this artifact be sent back to the stakeholder verbatim and read as faithful?

### Confirmation Bias Defense (Restate specialization)

The AI is most likely to quietly "improve" or "align" the stakeholder's phrasing into what the AI believes the stakeholder meant:

1. Did I change their words to make them "cleaner"? (Fix: keep verbatim.)
2. Did I merge two similar-sounding but distinct asks into one row? (Fix: keep separate, note the overlap.)
3. Did I resolve a contradiction by picking the more convenient phrasing? (Fix: keep both, tag CONFLICT.)

### Knowledge Boundary (Restate specialization)

1. Did I distinguish "the source says X" (FACT), "I inferred what they meant" (AI_INFERENCE), and "nobody knows yet" (UNKNOWN)?
2. Are conflicts preserved with both phrasings instead of one being lost?
3. Are the limits of the restate (what we could not transcribe, what we guessed) visible?

---

## 模式二 · 发散收敛（SCN-XXX）lens

### First Principles

- What observable result does this idea want to change?
- What underlying problem exists without the proposed feature?
- Why now?
- Which claims are assumptions disguised as requirements?

### Divergence Domain Lenses（发散领域 lens）

Divergent exploration sweeps the **12 scenario dimensions** below。For each dimension, ask the corresponding question and emit candidate ideas; stop a dimension once candidates repeat (saturation):

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

### Clustering And Deduplication

- Merge candidates that express the same distinct idea with different wording; keep the clearest phrasing.
- A candidate that spans two dimensions stays in its primary dimension; cross-reference the other dimension in the Candidate cell.
- Saturation rule: when a dimension produces no new distinct idea for two consecutive passes, stop that dimension.

### Adversarial Review

- Is the stated idea only a symptom of an unstated problem?
- Could a policy/process change satisfy it without any product change?
- Is the evidence for a candidate from one interested party only?
- Which candidate would survive if the idea were rewritten in the opposite direction?

### Reverse Validation

Starting from the intended outcome, ask what must be true for success; use the result to reveal missing prerequisites, dependencies, baseline data, and constraints as new candidates.

### Knowledge Boundary (Divergence specialization)

- Every candidate is `AI_INFERENCE` until the human marks it `include`; nothing in the divergent set is a business fact.
- Evidence must state *why the AI thinks this* (from the raw idea, a registered source, or common practice) — never present inference as observation.
- `research` disposition means "not decidable now": register it in issue-record / a QuestionRecord instead of leaving it silently.

---

## 两模式通用 · Sparse Degradation Mode（稀疏降级）

**模式一**（单句无材料，见 `SKILL.md` § Preflight L1 gate）——lens 无法做有意义工作，切降级模式：

```text
low-density input → skip lens ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) input sufficiency assessment (char count, attachments, domain guess)
                      b) batched clarifying questions (each: AI preliminary judgment + options + impact + owner)
                   → status = needs_user_input
                   → wait for human to fill in, then re-enter Preflight in sufficient mode
```

**模式二**（单句无材料，且负责人不可得 / 首批问题未答）——发散仍可进行但输出降级：

```text
sparse input → diverge into candidate skeletons (short evidence: "AI 推断，无书面来源")
             → do not force complete Evidence/Impact
             → batch ≤5 clarifying questions (each: AI preliminary judgment + options + impact + owner)
             → status = needs_user_input
             → wait for human answers, then re-enter Generate in sufficient mode
```

Degradation triggers (any one is enough):

- input length < 50 characters AND no attachments
- no source material, only a paraphrase from memory（模式一）/ no business domain, no role mentioned, no time constraint（模式二）
- the user only mentions a feature or implementation, with no verifiable ask behind it（"做一个打卡功能"）

This mode is not a failure state. It produces one clean batch of clarifying questions instead of a bloated restatement/candidate table full of `待确认` — a restatement built from nothing would just be the AI's own guess presented as the stakeholder's words.
