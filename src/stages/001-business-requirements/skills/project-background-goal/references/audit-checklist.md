# Audit Checklist

## Structural Gate

- All required headings exist, including `## Constitution Compliance` before `## 版本变更摘要` (`## Version Change Summary`).
- Metadata includes artifact ID, version, status, owner, reviewer, and dates or `待确认` / `TBD`.
- Material claims cite source IDs.
- All knowledge-state registers use stable IDs.
- Blocking questions are marked explicitly.
- `Constitution Compliance` section: every row's `status` field is non-empty and no row is `FAIL`. If deviation is needed, status must be `JUSTIFIED` with a stated reason.

## Source Coverage Gate

- Every requirement-bearing source is registered.
- Material source statements have an artifact location or an exclusion reason.
- Direct statements and AI interpretations are distinguishable.
- Conflicts remain visible until an authorized human resolves them.

## Semantic Gate

- Background explains why the request exists and why now.
- Current state describes actual work or workaround, not only complaints.
- Core problem is separate from the proposed solution.
- Goal describes intended change, not merely feature delivery.
- Success judgment has evidence, a provisional measure, or an explicit question.
- Roles and stakeholders are sufficient for the next workflow step without becoming a full journey.
- Timing, constraints, dependencies, and non-goals are addressed or marked unknown.

## Quality Lenses

- First principles: the root problem survives removal of the proposed solution.
- Systems thinking: affected roles, processes, systems, and dependencies were considered.
- Adversarial review: at least one plausible counterexample or failure assumption was tested.
- Reverse validation: prerequisites for success were checked.
- Minimal sufficiency: the artifact contains what the next step needs and excludes downstream design.

## Requirement Quality Gate (ISO/IEC/IEEE 29148)

Each material claim or goal stated in the artifact should be checked against the nine single-requirement characteristics (ISO/IEC/IEEE 29148:2018 §5.2.5):

| # | Characteristic | Check question | Pass criteria |
|---|---|---|---|
| 1 | Appropriate | Is it relevant to this project? | Yes, traces to a source or decision |
| 2 | Complete | Does it include all necessary conditions? | No dangling references to missing info |
| 3 | Conforming | Does it follow the template and source rules? | Heading + SRC-* rules met |
| 4 | Correct | Is it accurate against the source? | Matches SRC-* statement |
| 5 | Feasible | Can it be delivered within constraints? | No known blocker |
| 6 | Necessary | Would the goal still hold without it? | Yes |
| 7 | Singular | Is it one statement, not several? | Single claim per row |
| 8 | Unambiguous | Could two readers disagree? | No, terms defined |
| 9 | Verifiable | Is there a measurable fit criterion? | Numeric baseline + target OR explicit 待确认 with owner |

Recommended sentence shape: `The [system] shall [verb] [object] [constraint] [condition]` (29148 §5.2.5). In the Chinese artifact convention, keep the narrative but ensure each material claim is singular, traceable, and verifiable.

A `FAIL` on Verifiable for a material goal is a blocking item: either quantify it (baseline + target + time horizon) or set `needs_user_input` with the owner identified.

## Human Gate

Set `needs_user_input` when an unresolved item could change the problem, goal, success judgment, key roles, timing, boundary, cost, or material risk.

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