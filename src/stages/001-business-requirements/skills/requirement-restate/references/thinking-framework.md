# Thinking Framework · Requirement Restate

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

## Source Fidelity

The restate artifact is worthless if it does not faithfully reflect the source:

- Does every RR-NNN row trace to a concrete SRC-ID, down to paragraph or timestamp?
- Is the `original_phrase` verbatim (dialect, colloquialisms preserved) rather than cleaned up?
- Is the restatement a translation of the source, not an interpretation on top of it?
- Is the "restate vs original" diff the whole point — not smoothed away?

## Atomicity

- Does any row bundle two distinct asks?
- Is every row testable as a single claim a stakeholder can say yes/no to?
- If a row needs "and also…" to be complete, split it.

## No Solution Leak

- Does any row contain a proposed solution, technology, or design ("build a mobile app", "use QR codes")?
- Is a solution mentioned in the source recorded as a *hint* with `solution_leak=true`, not as a decision?
- Would a developer reading the restatement start designing before the ask is confirmed?

## Stakeholder Recognition

- Would the stakeholder recognize their own words in every row?
- Is the phrasing the stakeholder's, or the AI's restatement in its own vocabulary?
- Can this artifact be sent back to the stakeholder verbatim and read as faithful?

## Confirmation Bias Defense (Restate specialization)

The AI is most likely to quietly "improve" or "align" the stakeholder's phrasing into what the AI believes the stakeholder meant:

1. Did I change their words to make them "cleaner"? (Fix: keep verbatim.)
2. Did I merge two similar-sounding but distinct asks into one row? (Fix: keep separate, note the overlap.)
3. Did I resolve a contradiction by picking the more convenient phrasing? (Fix: keep both, tag CONFLICT.)

## Knowledge Boundary (Restate specialization)

1. Did I distinguish "the source says X" (FACT), "I inferred what they meant" (AI_INFERENCE), and "nobody knows yet" (UNKNOWN)?
2. Are conflicts preserved with both phrasings instead of one being lost?
3. Are the limits of the restate (what we could not transcribe, what we guessed) visible?

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
- no source material, only a paraphrase from memory
- the user only mentions a feature or implementation, with no verifiable ask behind it

This mode is not a failure state. It is the correct response to insufficient information — a restatement built from nothing would just be the AI's own guess presented as the stakeholder's words.
