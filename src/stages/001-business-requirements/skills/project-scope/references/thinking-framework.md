# Thinking Framework · Project Scope

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

## First Principles (Scope-Adapted)

- What is the minimum scope that can still achieve the core goal?
- Which items are really "scope" and which are implementation means disguised as scope?
- Would the project still succeed if a proposed In item were removed? If yes, it may belong in Out/Deferred.
- Is a stated constraint real (hard deadline, contract, compliance) or merely a preference?

## Boundary Scan（边界扫描 · thinking-core §3 领域 lens）

Scope work is boundary work. Enumerate the adjacent items even when they are NOT in scope:

- What is in this project, what is adjacent but out, and who owns the seams between them?
- Which ongoing or neighboring projects could overlap, conflict, or double-count this work?
- For each adjacent item: is it OUT (not ours), DEFERRED (ours later), or CONDITIONAL (ours if X holds)?

Mapping the full neighborhood prevents both scope creep and silent coverage gaps.

## Opportunity Cost（机会成本 · thinking-core §3 领域 lens）

Every In item spends the same budget, team, and timeline. Ask:

- What are we giving up by including this item this phase?
- Is the item a must-have for the success criteria, or a nice-to-have that crowds out a must-have?
- What is the cheapest deferral (Conditional/Deferred) for low-certainty, high-cost items?

## Systems Thinking

Check whether including or excluding an item shifts work onto an upstream/downstream team, another role's workload, data ownership, external services, policy, timing, or operational support.

## Adversarial Review

Try to invalidate each classification:

- Could a stakeholder reasonably claim this item is In? What evidence proves it is not?
- Is the In list bloated because "it is easier to say yes"?
- Is an Out item being dropped silently because it is inconvenient, rather than decided?
- Is the boundary being set by the loudest stakeholder rather than the decision owner?

## Reverse Validation

Starting from the project's success criteria, ask what must be true for success. Use the result to reveal must-have In items that were missing, and to demote items that do not serve the criteria.

---

## Low-Density Degradation Mode

When the input is a single natural-language sentence with no attached materials (see `SKILL.md` § Preflight for the L1 gate), the lenses above cannot do meaningful work. Switch to degradation mode:

```text
low-density input → skip lens ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) input sufficiency assessment (char count, attachments, domain guess)
                      b) batched clarifying questions (each: AI preliminary judgment + options + impact + owner)
                   → status = needs_user_input
                   → wait for human to fill in, then re-enter Preflight in sufficient mode
```

Degradation triggers (any one is enough):

- input length < 50 characters AND no attachments
- no candidate scope items, no constraints, no success criteria mentioned
- the user only mentions a feature or implementation ("add a button"), with no project boundary context

This mode is not a failure state. It is the correct response to insufficient information — one clean batch of clarifying questions beats a scope document full of 待确认.

## Confirmation Bias Defense (Scope specialization)

1. Did I restate a stakeholder's demand as In just because it was asserted loudly?
2. Did I classify an item as Out to please one team while another team expects it In — and hide the conflict?
3. Am I treating an existing habit ("we always include X") as a decision rather than checking it against the goal?

## Knowledge Boundary (Scope specialization)

1. Did I distinguish "source says this is in scope" (FACT), "I inferred the boundary" (AI_INFERENCE), and "nobody decided yet" (UNKNOWN)?
2. Are contested items flagged as CONFLICT and routed to the decision owner, not silently resolved?
3. Are Out/Deferred reasons separated into their own column, or buried in prose?
