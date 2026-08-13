# Audit Checklist · Competitive Research

## Structural Gate

- All required headings exist (`竞品列表`, `逐品分析`, `横向对比`, `结论`) before the version-change summary.
- Metadata includes artifact ID, version, status, owner, reviewer, and dates or `待确认` / `TBD`.
- Material claims cite source IDs (SRC-*).
- Each competitor has a selection rationale (direct / indirect / aspirational).
- Research goal (business-level / functional-level) is recorded.
- Blocking questions are marked explicitly.

## Source Coverage Gate

- Every competitor studied is registered with an SRC-ID and retrieval date.
- Material source statements have an artifact location or an exclusion reason.
- Official claims and AI interpretations (from screenshots/reviews) are distinguishable.
- Stale sources are flagged; conflicts between vendor claims and user reviews remain visible until an authorized human resolves them.

## Semantic Gate

- The research goal is stated and every comparison dimension traces to it (no generic feature checklists).
- The "So What" section answers: what we should do, do differently, ignore, and not know yet.
- Every "we should do Y" recommendation maps to a confirmed goal ID and carries `AI_INFERENCE`.
- At least one market-standard signal (competitors agree) and one divergence (differentiation opportunity) are identified.
- Confirmation bias is checked: disconfirming evidence was actively sought, not only supporting evidence.

## Quality Lenses

- First principles: each recommendation survives the removal of the benchmark competitor.
- Systems thinking: affected segments, journeys, and downstream decisions were considered.
- Adversarial review: at least one "competitor X is NOT the right benchmark" counterexample was tested.
- Reverse validation: prerequisites for our differentiation were checked.
- Minimal sufficiency: the artifact contains what the next step needs and excludes full product design.

## Human Gate

Set `needs_user_input` when an unresolved item could change competitor selection, comparison dimensions, or a material recommendation.

Set `conditional_review` only when remaining unknowns are non-blocking, have owners, and include deferral risks.

Set `ready_for_human_review` only when all other gates pass. Never set `confirmed`; only the authorized human can do so.

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
