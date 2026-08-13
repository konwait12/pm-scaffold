# Thinking Framework · feature-list

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Testability before acceptance criteria, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

## Domain Lens A: Single Responsibility

- Is each FEA-XXX one cohesive capability a developer can name and build independently?
- Which candidate "features" are really UX steps, page areas, or sub-actions that belong inside a bigger feature or to product-ux?
- Split only when two capabilities have different users, different data, or different trigger paths; otherwise merge.

## Domain Lens B: Boundary Clarity & Non-Overlap

- Does every FEA-XXX have an explicit in/out? A feature with no boundary is a black box.
- Do FEA-A and FEA-B overlap so a user or a downstream sub-skill cannot tell where one ends and the other begins?
- Boundary test: can I describe one action and point to exactly one FEA? If two FEA both claim it, merge or redraw.

## Domain Lens C: Traceability

- Every FEA-XXX `来源` points to a confirmed `ST-XXX`.
- Reverse check: every P0 ST-XXX has ≥1 FEA-XXX supporting it.
- Confirmed features → `FACT` / `DECISION`; AI-derived additions → `AI_INFERENCE`; unconfirmable → `UNKNOWN`.

## Domain Lens D: Priority Discipline

- P0: a confirmed story cannot be satisfied without it (no workaround) — MVP must-have.
- P1: important, a workaround exists — should-have.
- P2: nice-to-have — could-have.
- Every row states WHY this priority; deferring a P0 breaks a story, deferring a P1 costs efficiency.

## Domain Lens E: Downstream Consumability

- Can functional-flow / business-rules consume this FEA without re-researching the story?
- Is the 一句话描述 specific enough to seed §分功能详述 and §业务规则 later?
- Any FEA so vague it would need a follow-up question to define → mark `UNKNOWN` or split.

---

## Low-Density Degradation Mode

When the confirmed story set is a single sentence with no scope-bearing content, the lenses above cannot do meaningful work. Applying them to insufficient information produces verbose but empty analysis. Switch to degradation mode:

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

- the confirmed story set contains no scope-bearing content (no list source, no boundary, no priority signal)
- the source only restates a UX wish with no feature-level decision
- the feature boundary that determines the FEA set is unconfirmable by any source

This mode is not a failure state. It is the correct response to insufficient information — saving human review time and producing one clean batch of clarifying questions rather than a §功能清单 table full of `待确认` rows.

## Confirmation Bias Defense (feature-list specialization)

1. Did I inflate the story into features the story never asked for (overreach), or quietly drop a story that has no obvious feature (gap)?
2. Am I marking every inferred feature boundary as `FACT`, or checking whether it is `ASSUMPTION` / `AI_INFERENCE` first?
3. If two stories would imply overlapping features, did I keep the overlap visible — or silently pick one boundary?

## Knowledge Boundary (feature-list specialization)

1. Did I distinguish "story says the feature exists" (`FACT`), "I inferred the boundary from the flow" (`AI_INFERENCE`), and "nobody decided the scope yet" (`UNKNOWN`)?
2. Did I keep missing boundaries in the parent artifact's 待确认问题 register instead of inventing them?
3. Are knowledge-state tags on each FEA row, or buried in prose?
