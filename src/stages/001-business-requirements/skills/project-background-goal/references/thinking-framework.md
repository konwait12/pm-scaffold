# Thinking Framework

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.


## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Testability before acceptance criteria, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.
## First Principles

- What observable result needs to change?
- What underlying problem exists without the proposed feature?
- Why now?
- Which claims are assumptions disguised as requirements?
- Would the stated goal still make sense if the proposed solution were removed?

## Current State

- How is the work handled today: system, manual process, workaround, or no process?
- Which roles perform which parts?
- What evidence shows the current state is inadequate?
- What cost, delay, risk, error, or lost opportunity results?
- What already works and must not be broken?

## Goal Quality

Separate:

- business outcome: what changes for the organization or user;
- delivery outcome: what capability must exist;
- success judgment: what evidence would show improvement;
- non-goal: what this effort does not attempt to solve.

Do not force a numeric KPI when the source cannot support one. State the provisional measure and ask the owner to confirm the baseline, target, and time horizon.

## Stakeholder And System Lens

Identify only what is needed for the background baseline:

- demand proposer and business owner;
- primary affected users and secondary affected roles;
- goal decision owner and final reviewer;
- operational, support, compliance, data, or integration stakeholders when material;
- related systems and external dependencies.

Leave detailed role journeys and permission matrices to downstream work.

## Systems Thinking

Check whether the intended change affects upstream/downstream processes, another role's workload, data ownership, external services, policy, timing, or operational support.

## Adversarial Review

Try to invalidate the current framing:

- Is the stated problem only a symptom?
- Could a policy/process change solve it without a product change?
- Does the evidence come from one interested party only?
- Does the goal optimize one role while harming another?
- Is urgency asserted without a real deadline or consequence?
- Is the requested solution predetermined before alternatives are understood?

Record only findings that affect the candidate or require confirmation.

## Reverse Validation

Starting from the intended outcome, ask what must be true for success. Use the result to reveal missing prerequisites, dependencies, baseline data, ownership, and constraints.

---

## Low-Density Degradation Mode

When the input is a single natural-language sentence with no attached materials (see `SKILL.md` §1.1 for the gate), the seven lenses above cannot do meaningful work. Applying them to insufficient information produces verbose but empty analysis. Switch to degradation mode:

```text
low-density input → skip all 7-lens ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) input sufficiency assessment (char count, attachments, business-domain guess)
                      b) batched clarifying questions (each: AI preliminary judgment + options + impact + owner)
                   → status = needs_user_input
                   → wait for human to fill in, then re-enter Preflight in sufficient mode
```

Degradation triggers (any one is enough):

- input length < 50 characters AND no attachments
- no business domain, no role mentioned, no time constraint
- the user only mentions a feature or implementation ("add a button", "implement X"), with no business context

This mode is not a failure state. It is the correct response to insufficient information — saving human review time and producing one clean batch of clarifying questions rather than a 14-section artifact full of `待确认`.

## Confirmation Bias Defense (Wave-1 specialization)

The background artifact is the first place the AI is most likely to mirror the requester's framing without questioning it:

1. Did I restate the requester's solution as if it were the business goal? Or did I separate "what they asked for" from "what problem it solves"?
2. If the requester's premise is wrong (e.g., the current state is actually fine), does my artifact make that visible — or does it quietly agree?
3. Am I labeling every claim from the source as FACT, or checking whether it is ASSUMPTION / AI_INFERENCE first?

## Knowledge Boundary (Wave-1 specialization)

1. Did I distinguish "source says X" (FACT), "I inferred X" (AI_INFERENCE), and "nobody knows X yet" (UNKNOWN)?
2. Did I mark provisional metrics as needing owner confirmation instead of presenting them as established KPIs?
3. Are constraints and unknowns separated into their own register, or buried in prose?
