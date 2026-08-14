# PRD Scaffold Constitution

1. **Business truth remains human-owned.** AI may infer, research and recommend, but only authorized humans confirm facts, scope, choices and final delivery.
2. **Evidence and uncertainty stay visible.** Facts, decisions, assumptions, AI inferences, unknowns and conflicts are never collapsed into false certainty.
3. **Work follows the three-stage registry.** Stages provide context; five work-item Skills perform the work; artifacts do not define architecture. The registry must pass `registry_contract_check` (schema + template↔validator closure) before any pipeline run.
4. **Traceability is explicit.** Downstream functions and rules link to upstream stories and goals; changes reflow from the earliest affected item.
5. **PRD-only scope is enforced.** Research, diagrams, prototypes and analysis serve the PRD. Development planning, test suites and manuals remain downstream.
6. **Human gates cannot be bypassed.** Machine checks produce candidates, not approval. Rejection and trace failure block progression.
7. **Event sourcing is immutable.** Audit events (`.audit/events.jsonl`) are the single source of truth for review/change/confirm/reflow lifecycle. Tampering with `prev_hash`, `event_sha256`, or monotonic `recorded_at` is a CRITICAL break; `projection_cache` is a derived view that must be rebuildable from the event log alone.
8. **Validators speak one error language.** Every validator emits issues through `validation_errors.make_issue` (severity / check_id / expectation / actual / repair_hint). Raw Python tracebacks are never shown to users; unexpected exceptions are wrapped via `wrap_unexpected`.
