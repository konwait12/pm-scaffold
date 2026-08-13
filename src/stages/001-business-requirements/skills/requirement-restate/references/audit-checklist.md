# Audit Checklist · Requirement Restate

## Structural Gate

- All required headings exist (§1-§9 + `## Constitution Compliance` + `## 版本变更摘要`).
- Metadata includes artifact ID, version, status, owner, stakeholder, reviewer, and dates or `待确认` / `TBD`.
- Every restated requirement has a stable ID (`RR-NNN`), restated phrasing, original phrasing, source, knowledge state, stakeholder, and confidence.
- Material claims cite source IDs. Blocking questions are marked explicitly.

## Source Coverage Gate

- Every requirement-bearing source is registered as SRC-*.
- Every SRC-ID mentioned in Intake is reflected in the restatement.
- Every RR-NNN row traces to a source location (paragraph / timestamp).
- Original phrasing is preserved verbatim — no silent cleanup.

## Semantic Gate

- **Atomicity**: no row bundles two asks; every row is one testable claim.
- **No Solution Leak**: no row contains a proposed solution, technology, or design. A source-mention solution is a hint with `solution_leak=true`, not a decision.
- **Stakeholder Voice**: the restatement reads in the stakeholder's words, not the AI's.
- **Conflict Visibility**: all conflicts are flagged, none resolved.
- **Unknowns Routed**: every UNKNOWN is linked to a question or issue-record entry.

## Quality Lenses

- First principles: the ask survives removal of any proposed solution.
- Adversarial review: at least one plausible misreading was tested against the restatement.
- Reverse validation: the stakeholder sees exactly what they meant when reading only the restatement.
- Confirmation bias defense: no phrasing was "improved" or "aligned" by the AI.

## Human Gate

Set `needs_user_input` when a conflict or unknown changes the ask itself, or when the restatement cannot be sent back verbatim.

Set `conditional_review` only when remaining unknowns are non-blocking, have owners, and include deferral risks.

Set `ready_for_human_review` only when all other gates pass. Never set `confirmed`; only the original stakeholder (or their named delegate) can do so.

## Audit Report Shape

```text
status_recommendation
passed_checks
failed_checks
repairs_applied
blocking_questions
conflict_count
unknown_count
solution_leak_count
traceability_gaps
downstream_risks
```
