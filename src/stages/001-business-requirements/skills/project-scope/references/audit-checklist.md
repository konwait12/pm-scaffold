# Audit Checklist · Project Scope

## Structural Gate

- All required headings exist (§1-§9 + `## Constitution Compliance` + `## 版本变更摘要`).
- Metadata includes artifact ID, version, status, owner, reviewer, and dates or `待确认` / `TBD`.
- Every scope item has a stable ID (`S-NNN`), description, knowledge state, source/decision, and (for In items) an acceptance criterion.
- Material claims cite source IDs. Blocking questions are marked explicitly.

## Coverage Gate

- Every stakeholder expectation is classified as In / Out / Deferred / Conditional — none missing, none silently dropped.
- Every source that carries a scope-bearing statement is registered as SRC-* and represented in the artifact.
- Direct statements and AI interpretations are distinguishable (FACT vs AI_INFERENCE).
- Out/Deferred items each carry a reason (constraint / decision / future work).

## Mutual Exclusivity Gate

- An item is never both In and Out.
- An item is never both In and Deferred.
- An item is never both Deferred and Conditional.
- Two items do not describe the same work under different labels without a cross-reference.

## Semantic Gate

- Scope describes "what is/is not in this project", not "how to build it".
- Scope does not silently become a project goal or a feature list.
- Conditional items carry a concrete condition (budget / legal / tech-ready), not a vague "maybe".
- Deferred items carry a trigger or planned phase (V2/V3/未排期), not just "later".
- Acceptance criteria are verifiable, not adjectives ("提升体验" is not an acceptance criterion).

## Quality Lenses

- First principles: the In list is the minimum needed for the success criteria.
- Boundary scan: adjacent/overlapping projects and seams were considered.
- Adversarial review: at least one plausible counter-claim per contested item was tested.
- Reverse validation: prerequisites for success are in scope or explicitly deferred.
- Minimal sufficiency: the artifact contains what downstream needs and excludes downstream design.

## Human Gate

Set `needs_user_input` when a contested boundary, a missing success criterion, or an unresolved item could change the deliverable, timeline, or cost.

Set `conditional_review` only when remaining unknowns are non-blocking, have owners, and include deferral risks.

Set `ready_for_human_review` only when all other gates pass. Never set `confirmed`; only the goal decision owner / business sponsor can do so.

## Audit Report Shape

```text
status_recommendation
passed_checks
failed_checks
repairs_applied
blocking_questions
contested_items
nonblocking_unknowns
decisions_required
traceability_gaps
downstream_risks
```
