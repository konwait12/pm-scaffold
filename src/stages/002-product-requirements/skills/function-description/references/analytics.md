---
name: analytics-requirements
description: Define analytics and tracking requirements when there are explicit metrics, experiments, or operational decisions that need data. Triggered from `function-description` (function-description). NOT mandatory for projects without measurement needs.
trigger: Any of: (1) explicit success metrics requiring tracking, (2) A/B experiments planned, (3) operational decisions need data support, (4) funnel analysis required.
when_in_flow: During `function-description` (function-description) as conditional §5 chapter.
---

# Analytics Requirements (Content Branch)

> NOT mandatory. Trigger from `function-description` when measurement and tracking needs exist.
> Output flows into `function-description` artifact §5 埋点需求.

## Trigger Conditions (any one)

1. Success metrics (G-X goals from `project-background-goal`) require user behavior tracking
2. A/B experiments or feature flags planned
3. Operational decisions need data (e.g., "which channel drives most applicants?")
4. Funnel analysis required (e.g., visit → apply → screen → hire conversion)

## Boundary

**Do**: Define events, trigger timing, properties, analysis dimensions, and priority. Link each tracking requirement to a specific goal (G-X) or decision.

**Do NOT**: Design the data warehouse schema. Define implementation details (SDK, event bus). Create tracking for tracking's sake — every event must have a clear purpose.

## Workflow

```
`function-description` function description in progress, trigger condition met
    ↓
1. Review `project-background-goal` §5 goals (G-X) for quantifiable metrics
    ↓
2. Review `user-journey-and-stories` §3 story cards for user actions needing measurement
    ↓
3. For each metric/decision, define tracking event:
   - Event name and trigger timing
   - Properties (what data to capture)
   - Analysis dimension (by channel / by role / by time / by feature)
   - Priority (P0 = essential for core metrics, P1 = nice to have)
   - Linked goal (G-X) or decision
    ↓
4. Draft → Self-Audit → Human Review
    ↓
5. Insert into `function-description` artifact §5 埋点需求
```

## Output

See `templates/analytics-requirements.md`. Insert into `function-description` artifact §5.

## Completion

- Every event traces to a G-X goal or business decision
- No "track everything" events — each has specific purpose
- Priority assigned (P0/P1/P2)
- Human confirms tracking plan
