# Runtime Contracts

## Knowledge States

`FACT`, `DECISION`, `ASSUMPTION`, `AI_INFERENCE`, `UNKNOWN`, and `CONFLICT` are the only knowledge-state labels. Only sourced facts and recorded human decisions may be treated as confirmed business truth.

## Artifact States

`draft`, `needs_user_input`, `conditional_review`, `ready_for_human_review`, `confirmed`, `superseded`, and `simulated`.

`confirmed` requires `reviewer`, `reviewed_at`, and a human `ReviewRecord`. Automation may validate a candidate but may not confirm it.

## Shared Records

- `SourceRecord`: id, location, type, provider, captured_at, scope.
- `QuestionRecord`: id, question, initial_judgment, evidence, options, impact, owner, reflow_target.
- `DecisionRecord`: id, decision, alternatives, decider, rationale, decided_at, impact_scope.
- `ReviewRecord`: work_item, artifact_version, artifact_content_sha256, decision, reviewer, reviewer_id, reviewer_role, reviewed_at, comments.
- `ChangeRecord`: change_type, target, reason, source, downstream_impact.
- `TraceabilityLink`: source_id, target_id, relation, evidence_location.

## Confirmation Invariant

Machine checks, simulation, fixtures, and non-interactive flags cannot create or preserve formal confirmation without a reviewer matching `00-input/authorized-reviewers.json`. Each new review binds the decision to the reviewed version and SHA-256. A failed human or cross-artifact gate makes the overall command fail. Enterprise identity verification remains the responsibility of a future SSO or Feishu adapter.
