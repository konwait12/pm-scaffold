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
- `ReviewRecord`: work_item, artifact_version, artifact_content_sha256, decision, reviewer, reviewer_id, reviewer_role, reviewed_at, record_created_at, record_sha256, comments.
- `ChangeRecord`: change_type, target, reason, source, downstream_impact.
- `TraceabilityLink`: source_id, target_id, relation, evidence_location.
- `AuditEvent`: event_id, session_id, event_type, prev_hash, payload, payload_sha256, recorded_at, event_sha256.
  - event_id: monotonically increasing per session, used for hash-chain verification.
  - session_id: requirement directory name (REQ-NNN-*), groups events by work item.
  - event_type: review | change | decision | confirm | reject | reflow | init.
  - prev_hash: SHA-256 of the previous event's canonical JSON; first event uses sentinel.
  - payload: path to the referenced record (ReviewRecord / ChangeRecord / DecisionRecord) or inline dict.
  - payload_sha256: SHA-256 of the referenced record body (detects tamper of both event + record in lockstep).
  - recorded_at: ISO-8601 UTC timestamp; must be monotonic within a session.
  - event_sha256: self-fingerprint covering all fields except event_sha256 itself.
- `ProjectionCache`: schema_version, session_id, generated_at, event_count_snapshot, audit_chain_ok, work_items, derived_from_events.
  - schema_version: projection format version (currently 1).
  - session_id: requirement directory name, mirrors AuditEvent.session_id.
  - generated_at: ISO-8601 UTC timestamp of the last rebuild.
  - event_count_snapshot: number of events folded in; compared against `len(replay_events)` to detect staleness.
  - audit_chain_ok: whether `audit_log.verify_chain` passed cleanly at build time.
  - work_items: per-work-item bucket (see below); folded from AuditEvent stream + artifact frontmatter ground truth.
  - derived_from_events: list of event_ids that contributed to the projection (provenance for replay).
  - Work-item bucket fields: status, artifact_path, artifact_content_sha256, artifact_version, artifact_id_frontmatter, reviewer, reviewer_id, reviewer_role, reviewed_at, confirmed_at, latest_review_record, latest_review_decision, superseded, superseded_reason, last_change_reason, last_changed_at, _legacy_fallback.
  - `_legacy_fallback: true` marks a work item whose latest_review_record came from glob+sort fallback (pre-audit_log requirement); validators may surface a WARN.
- `ValidatorIssue`: severity, blocking, check_id, check_family, location, field_path, message, expectation, actual, repair_hint, source_ref.
  - severity: `CRITICAL` | `HIGH` | `MEDIUM` | `INFO` (capital tag; never lowercase).
  - blocking: bool; defaults to True for CRITICAL/HIGH, False for MEDIUM/INFO.
  - check_id: stable machine-readable check tag (e.g. `state_machine.no_outgoing`); survives code refactors so users can track recurrence.
  - check_family: validator family (e.g. `property_check`, `branch_validator`); used for grouping in test summaries.
  - location: artifact path relative to req_dir (or `<artifact>` placeholder).
  - field_path: dotted path to the offending field (e.g. `frontmatter.status`, `tables.BR-007.规则内容`, `sections.3`).
  - message: human-readable one-liner; auto-derived from expectation/actual if omitted.
  - expectation: what the validator expected ( Wanted state).
  - actual: what the validator found (observed state).
  - repair_hint: actionable fix instruction (not just "X is missing" but HOW to fix it).
  - source_ref: constitution clause / skill output-contract section / DEC-SRC id that justifies the check.
- `RegistryContract`: schema + closure invariants enforced by `registry_contract_check.py`.
  - Schema shape: `workflow-registry.json` must declare `stages[]` (each with `id`, `name`, `skills[]`), `work_items[]` (each with `id`, `name`, `stage_id`, `artifact_path`, `reviewer_roles`, `entry_material`, `required_inputs`, `predecessors`, `depends_on`, `produces`), and `internal_capabilities[]`.
  - Reference integrity: every `predecessors` / `depends_on` / `parent_work_item` must resolve to an existing work_item id.
  - Template↔validator closure: every frontmatter field declared in a skill's template must be referenced in that skill's `validate_artifact.py` (AST-verified); drift is E3_drift.
  - Run order: `registry_contract_check.py` is the first phase of `run_tests_mac.sh`; any failure aborts before consistency_check runs.

## Validator Issue Format

Every validator must emit issues through `validation_errors.make_issue`. Raw Python tracebacks are never shown to users; unexpected exceptions are wrapped via `validation_errors.wrap_unexpected`. The `--json` output of every validator must expose `errors` (blocking issues), `warnings` (non-blocking), and `info` (diagnostic) arrays, each containing `ValidatorIssue` dicts. `validation_errors.aggregate_by_check_id` provides cross-validator rollup for test summaries.

## Registry Contract

The `workflow-registry.json` is the single source of truth for the three-stage pipeline shape. `registry_contract_check.py` enforces schema shape, reference integrity, and template↔validator closure before any other test runs. Adding a new skill requires: (1) declaring it in the registry, (2) providing a template with frontmatter fields, (3) referencing every frontmatter field in `validate_artifact.py`. Any drift fails E3_drift and blocks the pipeline.

## Confirmation Invariant

Machine checks, simulation, fixtures, and non-interactive flags cannot create or preserve formal confirmation without a reviewer matching `00-input/authorized-reviewers.json`. Each new review binds the decision to the reviewed version and SHA-256, and appends an `AuditEvent` to `.audit/events.jsonl` before the artifact's frontmatter status is flipped — events are written first, status changes second, so the log can always replay the decision. A failed human or cross-artifact gate makes the overall command fail. Enterprise identity verification remains the responsibility of a future SSO or Feishu adapter.
