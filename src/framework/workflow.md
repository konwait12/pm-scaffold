# Runtime Workflow

The machine-readable source for stage, work-item, Skill, and artifact paths is `workflow-registry.json`.

## Backbone

```text
001 Business Requirements
  project-background-goal
  → human confirmation
  user-journey-and-stories
  → human confirmation
002 Product Requirements
  product-ux
  → human confirmation
  function-description
  → human confirmation
003 PRD Output
  prd-assembly
  → final human confirmation
```

## Work-Item Cycle

```text
Preflight → Intake → Think → Clarify → Generate
→ Audit → Human Gate → Commit / Reflow
```

Clarification and reflow are states inside the current work item, not mandatory top-level branches. Brainstorming discovers candidates; a human decides which candidates become requirements.

Each transition through `Human Gate` and `Commit / Reflow` also appends an `AuditEvent` to `.audit/events.jsonl` (via `audit_log.append_event`) with event type `review` / `confirm` / `change` / `reflow` as appropriate — events precede state mutation so the cycle is always replayable from the log.

## Audit Layer

The scaffold maintains a three-tier audit foundation (Harness-inspired):

1. **`audit_log`** (`src/scripts/audit_log.py`) — append-only `.audit/events.jsonl` is the single source of truth for review/change/confirm/reflow/init lifecycle. Each event carries `prev_hash` (chain) + `event_sha256` (self-fingerprint) + `payload_sha256` (record-body binding) + monotonic `recorded_at`. `verify_chain` detects any tampering; `reconstruct_causality` rebuilds the full causal chain.
2. **`projection_cache`** (`src/scripts/projection_cache.py`) — folds the event log into `.audit/projection.json`, a materialized view of the latest status / artifact hash / reviewer / review record per work item. `is_stale` triggers rebuild; `latest_review_for` returns the latest review record path + hash.
3. **`registry_contract_check`** (`src/scripts/registry_contract_check.py`) — registry schema + template↔validator field closure (E3_drift). Run as the first check in `run_tests_mac.sh` (Phase 0); any failure aborts subsequent tests (fail loud).

Invariant: **event ⟺ model-visible state** — no review/change is considered real until it appears in `events.jsonl`. Validators read the projection, never glob+sort markdown directly (legacy requirements fall back to glob+sort with a warning).

## Entry And Exit

- A work item may start only when all registered predecessors are `confirmed`.
- Sparse or conflicting input routes to `needs_user_input` rather than fabricated output.
- Machine validation may produce `ready_for_human_review` but never `confirmed`.
- Human rejection and cross-artifact trace failure block progression and return failure.
- PRD assembly aggregates confirmed content and may not add requirements.
- Validators read the latest review record from `projection_cache.read_projection`, falling back to glob+sort only for legacy requirements (those without `.audit/events.jsonl`); the fallback emits a warning so the migration surface stays visible.

## Conditional Support

- `competitive-research`: business or function mode when external evidence is needed.
- `feasibility-analysis`: feasibility across market/technical/cost/risk before entering the main trunk; multi-solution tradeoffs handled as a chapter.
- `requirement-restate`: requirement restate capability (restate + diverge) when input is sparse, sources conflict, or L0 is idea-only.
- `tracking-plan`: data tracking / instrumentation plan when a feature needs measurement data.
- `issue-record`: cross-stage issue list; B3 closure before any work item is sent for review.

Visualization remains a toolkit capability. It is required only where the work-item contract explicitly requires a flow representation.
