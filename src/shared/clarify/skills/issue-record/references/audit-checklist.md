# Audit Checklist · Issue Record（跨阶段共享）

## Structural Gate

- All required headings exist (§1-§12 + `## Constitution Compliance` + `## 版本变更摘要`).
- Metadata includes artifact ID, version, status, owner, reviewer, and dates or `待确认` / `TBD`.
- Every issue has a stable ID (`ISS-NNN`), category, state, title, description, owner, knowledge state, source, and raised_at.
- Material claims cite source IDs. Blocking questions are marked explicitly.

## Coverage Gate

- Every upstream artifact's "待确认" / UNKNOWN / CONFLICT marker maps to an ISS-NNN or has a documented close reason (`closed_at_intake`).
- No phase-leftover unknown is silently unrecorded.
- Issues are project-level: nothing is stranded in a single phase artifact without a register entry.

## Ownership Gate

- Every `open` issue has an owner (person or role, not "TBD").
- Every BLK / DEC has a `target_close`.
- Every RSK has a `mitigation`.
- Every `resolved` issue links to the artifact change that closed it.
- Every `escalated` issue has an `escalated_to` (new owner or authority).
- Issues older than 30 days have an escalation record or a documented reason they are still open.

## State Integrity Gate

- `accepted` state is set only by the decision owner, never by the AI.
- `resolved` was verified by a verifier distinct from the implementer (or that fact is noted).
- No issue is closed without evidence (no "just to empty the list" closures).
- Category is stable: BLK is truly blocking, INF is a missing source/datum, CLS is wording ambiguity, DEC has a named decider, OUT has a routing target.

## AI Inquiry Compliance Gate

- Every registration was preceded by the AI asking "要不要登记为 ISS-NNN" — no "silently continued past a 待确认 marker".
- The AI did not accept risks on the user's behalf.
- New issues entered without user confirmation are flagged as violations.

## Quality Lenses

- First principles: an issue stripped of its proposed solution still exists.
- Systems thinking: downstream Work Items affected by each open issue were considered.
- Adversarial review: at least one plausible downgrade/upgrade of an issue's severity was tested.
- Reverse validation: walking back from PRD confirmation, the "问题清零" list is complete or explicitly accepted as risk.
- Pre-mortem: the top 3-5 failure causes each have an owner and mitigation or accepted risk.

## Human Gate

Set `needs_user_input` when a category, owner, or blocking status is unresolved, or when a decision-in-waiting has no target close.

Set `conditional_review` only when remaining unknowns are non-blocking, have owners, and include deferral risks.

Set `ready_for_human_review` only when all other gates pass. Never set `confirmed`; only the goal decision owner / business sponsor can approve the closed-out list.

## Audit Report Shape

```text
status_recommendation
passed_checks
failed_checks
repairs_applied
open_count
in_progress_count
blocked_count
accepted_count
resolved_count
escalated_count
open_blk_ids
open_dec_ids
critical_top5
blocking_questions
downstream_risks
```
