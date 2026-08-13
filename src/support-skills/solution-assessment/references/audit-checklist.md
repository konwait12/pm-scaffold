# Audit Checklist · Solution Assessment

## Structural Gate

- All required headings exist for the active mode (feasibility: 市场空间 / 技术可行性 / 投入产出 / 风险评估 / 结论; comparison: 候选方案 / 方案对比矩阵 / AI 推荐 / 人工决策) before the version-change summary.
- Metadata includes artifact ID, version, status, owner, decision-owner, reviewer, and dates or `待确认` / `TBD`.
- Material cost/risk figures cite source IDs (SRC-*) or are explicitly labeled `AI_INFERENCE` / `ASSUMPTION` with an owner.
- Decision owner is identified; `DEC-XXX` decision record slot exists.
- Blocking questions are marked explicitly.

## Method Gate (comparison mode)

- Criteria were defined BEFORE scoring (anchoring check) — evidence that weights were not reverse-engineered from a preferred outcome.
- Every solution is described at equal depth; no option is padded or starved.
- Weighted scores are arithmetically correct (weight × score per criterion → total).
- Sensitivity analysis states which criterion, if its weight changed by ±1, flips the recommendation.

## Method Gate (feasibility mode)

- All 4 dimensions (market / technical / cost-benefit / risk) analyzed with evidence.
- Technical challenges each resolved to Verified / Needs Verification / Not Feasible.
- Recommendation is 做 / 不做 / 有条件做, and conditions (if any) are specific and measurable.

## Semantic Gate

- The assessment answers a real decision, not a description ("we could do X or Y" is not a conclusion).
- The AI recommendation carries a confidence level (HIGH/MEDIUM/LOW) and lists the assumptions that could flip it.
- No silent scope change: if the preferred solution changes scope, the affected Work Items are named.
- Implementation-detail choices are routed to engineering, not padded into the product comparison.

## Quality Lenses

- First principles: the root decision survives removing the "obvious" solution.
- Systems thinking: affected roles, processes, systems, and operational dependencies were considered.
- Adversarial review: at least one "the recommended option is a trap" counterexample was tested.
- Reverse validation: prerequisites for the recommended solution's success were checked.
- Minimal sufficiency: the artifact contains what the decision needs and excludes architecture design.

## Human Gate

Set `needs_user_input` when an unresolved item could change the recommendation, a criterion weight, or a material cost/risk figure.

Set `conditional_review` only when remaining unknowns are non-blocking, have owners, and include deferral risks.

Set `ready_for_human_review` only when all other gates pass. Never set `confirmed`; only the authorized decision owner can do so.

## Audit Report Shape

```text
status_recommendation
passed_checks
failed_checks
repairs_applied
blocking_questions
nonblocking_unknowns
decisions_required
traceability_gaps
downstream_risks
```
