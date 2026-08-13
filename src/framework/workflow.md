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

## Entry And Exit

- A work item may start only when all registered predecessors are `confirmed`.
- Sparse or conflicting input routes to `needs_user_input` rather than fabricated output.
- Machine validation may produce `ready_for_human_review` but never `confirmed`.
- Human rejection and cross-artifact trace failure block progression and return failure.
- PRD assembly aggregates confirmed content and may not add requirements.

## Conditional Support

- `competitive-research`: business or function mode when external evidence is needed.
- `feasibility-analysis`: feasibility across market/technical/cost/risk before entering the main trunk; multi-solution tradeoffs handled as a chapter.

Visualization remains a toolkit capability. It is required only where the work-item contract explicitly requires a flow representation.
