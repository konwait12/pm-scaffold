# Audit Checklist（Brainstorming）

## Structural Gate

- Required headings exist: 原始输入 / 发散结果 / 候选清单 / 人工处置表 / 收敛后输入包 / 版本变更摘要.
- Metadata includes artifact ID, version, status, owner, reviewer, and dates or `待确认` / `TBD`.
- 候选清单 contains SCN-XXX rows with non-placeholder Evidence and Impact.
- 处置表 contains exactly the 8 canonical columns (Candidate ID / Role-Lifecycle / Candidate / Evidence / Impact / Human Disposition / Reason / Write-back Target).
- `Human Disposition` values are only `include` / `exclude` / `defer` / `research`; `include` rows carry a non-placeholder Write-back Target.
- Status is one of `draft` / `needs_user_input` / `conditional_review` / `ready_for_human_review` — **never `confirmed`**.

## Divergence Coverage Gate

- All 12 dimensions swept (lifecycle / roles / normal-alternate-exception-failure-timeout / permission / data condition / handoff / dependency / cancellation / retry / rollback / change-recovery) or explicitly skipped with a reason.
- No dimension stopped before saturation unless skipped.
- Candidates are clustered and deduplicated; one SCN-XXX per distinct idea; no near-duplicates.

## Inference Discipline Gate

- Every candidate is labeled `AI_INFERENCE`; nothing in the divergent set is presented as a business fact.
- Every Evidence cell explains *why the AI thinks this* — raw idea quote, SRC-*, or stated common practice.
- The raw one-line idea is preserved verbatim in 原始输入 and quoted in Evidence, not paraphrased into "fact".

## Disposition Readiness Gate

- The disposition table is complete enough for a human decision: each row has evidence, impact, and a recommendation, with deferral risks visible.
- `research` rows reference an issue-record / QuestionRecord destination; `defer` rows name a trigger.
- Every `include` row names a Write-back Target in the `project-background-goal` input package.

## Quality Lenses

- First principles: the included candidates survive removal of any proposed implementation.
- Systems thinking: affected roles, processes, systems, and dependencies were considered as candidates.
- Adversarial review: at least one plausible counterexample or failure candidate was generated and shown.
- Reverse validation: prerequisites for success were diverged as candidates.
- Minimal sufficiency: the input package contains what `project-background-goal` needs and excludes designed solutions.

## Human Gate

Set `needs_user_input` when an unresolved answer could change the candidate set or disposition options. Set `conditional_review` only when remaining unknowns are non-blocking, have owners, and include deferral risks. Set `ready_for_human_review` only when all other gates pass. Never set `confirmed`.

## B3 收口

- Confirm the issue-record §13 阶段收口表 has a row for this skill（问题数 / 收口日期 / 状态；空阶段也落行）before handoff; dor_check hard-checks closure and references at gate time.

## Audit Report Shape

```text
status_recommendation
passed_checks
failed_checks
repairs_applied
divergence_gaps            # 未扫描或过早饱和的维度
blocking_questions
nonblocking_unknowns
disposition_pending        # 尚未处置的候选
traceability_gaps
downstream_risks
```
