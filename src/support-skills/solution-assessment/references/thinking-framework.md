# Thinking Framework · Solution Assessment

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.

Two modes — feasibility analysis and solution comparison. Both require a **product-level solution** to already exist (from Stage 2); you cannot assess "can we build X" until X is concrete.


## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

## First Principles

- What is the observable decision we are being asked to help make?
- Which costs, risks, and "must-haves" are assumptions disguised as requirements?
- Would the recommended solution still be preferred if a cheap partial fix existed?
- Is the question truly "which solution" or actually "should we do this at all" (feasibility)?

## Feasibility Lens

Answer 4 questions with evidence:

1. **Market space**: target users, comparable penetration, theoretical space.
2. **Technical**: each challenge → Verified / Needs Verification / Not Feasible.
3. **Cost-benefit**: R&D cost, ops cost, expected revenue, payback period.
4. **Risk**: each risk → impact + mitigation.

Conclude with: 做 / 不做 / 有条件做 (state the conditions specifically and measurably).

**Anti-pattern**: "We want to build an invitation system" → "Yes it's feasible" is meaningless. Any system can be built. Feasibility only matters at the level of "can we implement subscription notifications via WeChat mini-program templates given our architecture?"

## Occam's Razor (领域 lens, from thinking-core.md §3)

When two solutions both meet the goal, prefer the one with fewer dependencies and less downstream impact. State which solution is simpler and why — do not let "more impressive" outweigh "simpler".

## Opportunity Cost Lens (领域 lens, from thinking-core.md §3)

- What do we give up (other features, other work items) by choosing each solution?
- Is the marginal benefit of the richer solution worth the marginal cost?

## Reversibility Lens

- Can we undo this decision if it turns out wrong?
- What is the cost of being wrong, and how fast can we detect it?
- A reversible decision deserves a faster, cheaper path; an irreversible one demands more evidence.

## Systems Thinking

Check whether each candidate affects upstream/downstream processes, another role's workload, data ownership, external services, or operational support. A solution that is cheaper but adds permanent ops burden is not cheaper.

## Adversarial Review

Try to invalidate each candidate:

- Is the "obvious winner" favored because it is the first one heard (anchoring)?
- Does the evidence for one option come from a single interested party?
- Is urgency asserted without a real deadline or consequence?
- Is the analysis optimizing one role while harming another?

Record only findings that affect the candidate or require confirmation.

## Reverse Validation

Starting from the preferred outcome, ask what must be true for each solution to succeed: prerequisites, baseline data, dependencies, ownership, and constraints. Use the result to reveal what the assessment has not yet verified.

---

## Low-Density Degradation Mode

When the input is a single natural-language sentence with no concrete product-level solution, no cost/constraint data, and no decision owner (see `SKILL.md` §1.1 for the gate), the lenses above cannot do meaningful work. Applying them to insufficient information produces verbose but empty analysis. Switch to degradation mode:

```text
low-density input → skip all-lens ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) input sufficiency assessment (concrete solution? cost/constraint data? decision owner?)
                      b) batched clarifying questions (each: AI preliminary judgment + options + impact + owner)
                   → status = needs_user_input
                   → wait for human to fill in, then re-enter Preflight in sufficient mode
```

Degradation triggers (any one is enough):

- no concrete product-level solution exists to assess (only a vague idea or feature name)
- no cost / constraint / compliance / resource data available
- no named decision owner
- the user only mentions a feature ("评估一下做不做这个") with no decision it should inform

This mode is not a failure state. It is the correct response to insufficient information — saving human review time and producing one clean batch of clarifying questions rather than a 4-section feasibility report full of `待确认`.

## Confirmation Bias Defense (assessment specialization)

Assessment is vulnerable to anchoring on the first solution heard and to AI's tendency to produce "balanced-sounding" comparisons that hide real tradeoffs:

1. Were criteria defined before any solution was scored — or did I pick weights that favor an early favorite?
2. Are all options described at equal depth, or did I silently pad a favorite?
3. Does my recommendation actually follow from the matrix, or did I pick the matrix numbers to match a conclusion I already formed?

## Knowledge Boundary (assessment specialization)

1. Did I distinguish "source says cost = ¥X" (FACT), "I estimated cost" (AI_INFERENCE), and "no cost data" (UNKNOWN)?
2. Are provisional figures marked as needing owner confirmation instead of presented as established numbers?
3. Are the assumptions that could flip the recommendation listed explicitly, not buried in prose?
