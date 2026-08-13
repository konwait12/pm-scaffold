# Thinking Framework · Tracking Plan

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Testability before acceptance criteria, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

## Metric Traceability（指标追溯）

Every event must earn its place by supporting a metric and a goal:

- Which G-X (background-goal) does this event prove or measure?
- Which metric type does it feed: `north_star` / `funnel_step` / `counter` / `latency` / `conversion` / `retention`?
- If an event maps to no G-X, it is a candidate for deletion or `nice_to_track`.
- Walk backwards from each G-X: are the required events and properties present to verify it after launch?

## Event Fidelity（事件粒度）

- Is the event one user-meaningful action, not a bundle of several?
- Is the trigger condition precise enough that two engineers would instrument the same moment?
- Is the property set complete (each property has key / type / example / pii_flag / required)?
- Does the event fire at the right point in the user's action sequence (before/after validation, before/after success)?

## PII Discipline（PII 纪律）

- Which properties are personal identifiers, behavioral fingerprints, or sensitive content?
- `false` (non-PII) → standard upload; `quasi` (IP / device ID / location) → hash + consent; `true` (name / ID / phone) → encryption + business necessity; `sensitive` (health / finance / religion) → access control + minimization + explicit consent.
- Does every PII event carry an explicit data-retention rule in `notes`?
- Would collecting this property survive a data-protection review?

## Coverage vs Noise（覆盖 vs 噪声）

- Does every P0 FUN-XXX have at least one `must_track` event?
- Are there orphan events (no FUN-XXX, no G-X)?
- Is the event list free of "track everything" noise — events with no metric, goal, or decision use?
- Are duplicates merged under one consistent `event_name`?

## Naming Consistency

- Is every `event_name` snake_case verb_noun (`checkout_submit_click`), globally unique?
- Is `event_type` one of `page_view` / `click` / `submit` / `exposure` / `success` / `error` / `custom`?
- Do the same action and the same meaning reuse the same event across functions (no `click_btn` vs `button_click`)?

## Systems Thinking

- Does the event need server-side instrumentation (backend events), a third-party SDK, or a miniprogram bridge?
- Who collects, cleans, and owns the event stream? Is that responsibility visible in the plan?
- Does upload timing (realtime / near_realtime / batch / on_session_end) match what the metric needs?

---

## Low-Density Degradation Mode

When upstream is not confirmed (function-description FUN-XXX or its rules missing) or the tracking need is a single unqualified sentence, the lenses above cannot do meaningful work. Switch to degradation mode:

```text
low-density / upstream-not-confirmed input → skip lens ideation
                                             → do not enter Generate / Audit
                                             → output only:
                                                a) input sufficiency assessment (upstream confirmed? which G-X to prove? platforms?)
                                                b) batched clarifying questions (each: AI preliminary judgment + options + impact + owner)
                                             → status = needs_user_input
                                             → wait for upstream confirmation or human input, then re-enter Preflight
```

Degradation triggers (any one is enough):

- function-description (FUN-XXX) or its upstream rules are not confirmed
- no goals (G-X) to map events to
- the user only says "add tracking for X" with no metrics, platforms, or trigger context

This mode is not a failure state. An event contract built before upstream is confirmed would be invented data — worse than no plan.
