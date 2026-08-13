# Thinking Framework · business-rules

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Testability before acceptance criteria, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

## Domain Lens A: Domain Policy Extraction

- What must the system compute, validate, and enforce for this function to hold — not what does the UI show?
- Which confirmed story/UX statements hide an implied constraint the system must enforce even though it is not stated?
- Which candidate "rules" are really screen-flow narrative (button order, redirect, toast) and belong to interaction-rules?

## Domain Lens B: Rule Classification

For each candidate rule, force exactly one class:

- 计算 Calculation: derived value (amount, count, score, deadline) — write formula + unit + rounding/boundary handling
- 约束 Constraint: allowed range, uniqueness, business prohibition — write the reject behavior
- 条件 Condition: the judgment that decides a state/scenario holds
- 权限 Permission: who may / who may not, by role or data scope
- 时序 Timing: ordering, dependency, allowed/forbidden sequencing

Do not fill the class column with 「待确认」— an unclassified rule cannot be consumed by validation-rules or state-machine downstream.

## Domain Lens C: Determinism

- Can a developer turn this rule into code without a follow-up question?
- Is the trigger exact and the logic closed (same input → same output)?
- Are boundaries and rejection paths spelled out?
- Any word like 「合理」「适当」「尽快」「视情况」→ the rule is not thought through; split it or mark `UNKNOWN`.

## Domain Lens D: Traceability

- Every BR-XXX `来源` points to a `ST-XXX` or `FEA-XXX`.
- Reverse check: every P0 FUN-XXX has ≥1 BR-XXX supporting it.
- Confirmed rules → `FACT` / `DECISION`; AI-derived additions → `AI_INFERENCE`; unconfirmable → `UNKNOWN`.

## Domain Lens E: Boundary Discipline

| Content characteristic | Owner |
|---|---|
| User action → system response, page behavior | interaction-rules `IX-XXX` |
| Field format, length, required, regex | validation-rules `VL-XXX` |
| State transitions, trigger events, side effects | state-machine |
| Failure, timeout, retry, rollback, recovery | exception-handling |
| Verifiable acceptance condition | acceptance-criteria `AC-XXX` |
| System must compute / enforce at domain level | **this sub-skill `BR-XXX`** |

---

## Low-Density Degradation Mode

When a P0 function's confirmed story/UX is a single sentence with no rule-bearing content, the lenses above cannot do meaningful work. Applying them to insufficient information produces verbose but empty analysis. Switch to degradation mode:

```text
low-density input → skip domain-lens ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) input sufficiency assessment (what is confirmed, what is missing)
                      b) batched clarifying questions (each: AI preliminary judgment + options + impact + owner)
                   → status = needs_user_input
                   → wait for human to fill in, then re-enter Preflight in sufficient mode
```

Degradation triggers (any one is enough):

- a function's story/UX contains no rule-bearing content (no threshold, no policy, no computation)
- the confirmed source only restates UI flow with no domain logic
- the constraint that determines a rule's outcome is unconfirmable by any source

This mode is not a failure state. It is the correct response to insufficient information — saving human review time and producing one clean batch of clarifying questions rather than a §业务规则 table full of `待确认` rows.

## Confirmation Bias Defense (business-rules specialization)

1. Did I restate the confirmed UX flow as "rules" without separating domain logic from screen narrative?
2. Am I labeling every inferred constraint as `FACT`, or checking whether it is `ASSUMPTION` / `AI_INFERENCE` first?
3. If two rules would contradict (one permits, one forbids the same case), did I keep the conflict visible — or silently pick one?

## Knowledge Boundary (business-rules specialization)

1. Did I distinguish "story says the threshold is X" (`FACT`), "I inferred X from the flow" (`AI_INFERENCE`), and "nobody decided X yet" (`UNKNOWN`)?
2. Did I keep missing constraints in the parent artifact's 待确认问题 register instead of inventing values?
3. Are knowledge-state tags on each rule row, or buried in prose?
