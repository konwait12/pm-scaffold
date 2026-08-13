# Thinking Framework · state-machine

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Testability before acceptance criteria, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

## Domain Lens A: Entity & State Discovery (实体与状态盘点)

- What are all the legal states of this entity, and are they pairwise distinguishable?
- For each P0 FUN-XXX entity, list every state with its entry and exit conditions — do not pick a few from memory.
- States must be mutually exclusive and distinct (待审核 / 审核中 / 已通过 / 已驳回); a pseudo-state that only differs by an adverb is not a state.

## Domain Lens B: Trigger & Transition Completeness (触发与转移完备性)

- For every current-state × trigger-event combination, is a target state defined?
- Forbidden transitions (e.g. terminal-state rollback) are stated explicitly as 「不允许」, never left blank.
- Cover the branches: success, failure, cancel, timeout, retry, duplicate submit, rollback, concurrency — every path business allows has a destination.

## Domain Lens C: Condition & Side-Effect Precision (条件与副作用精确性)

- Is every guard condition decidable (expressible as a BR-checkable rule), not 「视情况」「合适时机」?
- Are side effects named one by one: notification, state linkage, related-entity update, audit, rollback action? If none, write 「无」 explicitly.

## Domain Lens D: Boundary Preservation (边界保持)

| Content characteristic | Owner |
|---|---|
| How a state looks in the UI (button grey, badge) | interaction-rules `IX-XXX` |
| Field storage, table schema, index | implementation — not here |
| Message queue, idempotency implementation | engineering — not here |
| Failure, timeout, retry, rollback, recovery narrative | exception-handling |
| State and state transitions | **this sub-skill** |

Any state-table cell containing 「按钮变灰」「存 int」「用 Redis 记录」 is out of bounds — remove or demote to a one-line side effect.

## Domain Lens E: Traceability & Knowledge State (可追溯性与知识状态)

- Every transition conclusion carries `FACT` / `DECISION` / `AI_INFERENCE` / `UNKNOWN`; inferred and unknown entries are registered in the 待确认 register, not silently treated as fact in the table.
- Every transition table row is reverse-traceable to its `FUN-XXX` and source document; state naming is consistent library-wide; terminal semantics agree with cancel/termination semantics.

---

## Low-Density Degradation Mode

When a function's confirmed source mentions states but names none of them, the lenses above cannot do meaningful work. Applying them to insufficient information produces verbose but empty transition tables. Switch to degradation mode:

```text
low-density input → skip domain-lens ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) input sufficiency assessment (which states/events are confirmed, which are missing)
                      b) batched clarifying questions (each: AI preliminary judgment + options + impact + owner)
                   → status = needs_user_input
                   → wait for human to fill in, then re-enter Preflight in sufficient mode
```

Degradation triggers (any one is enough):

- the source says "有状态 / 有生命周期" but lists no state names, events, or transitions
- the confirmed source only describes UI screen changes, not entity lifecycle
- the BR rules that gate transitions are unconfirmable

This mode is not a failure state. It is the correct response to insufficient information — one clean batch of questions instead of a transition table full of guessed states and invented events.

## Confirmation Bias Defense (state-machine specialization)

1. Did I model the happy path the story happened to mention, or did I enumerate all states the business actually has (including cancel/timeout/terminal)?
2. Am I labeling an inferred transition as `FACT`, or checking whether it is `AI_INFERENCE` first?
3. If a governing BR would forbid a transition I assumed, did I keep the conflict visible — or quietly allow it?

## Knowledge Boundary (state-machine specialization)

1. Did I distinguish "story names the state 待审核" (`FACT`), "I inferred a 审核中 state from the flow" (`AI_INFERENCE`), and "nobody defined cancel semantics" (`UNKNOWN`)?
2. Did I keep undefined transitions in the 待确认 register instead of inventing target states?
3. Are knowledge-state tags on each transition row, or buried in prose?
