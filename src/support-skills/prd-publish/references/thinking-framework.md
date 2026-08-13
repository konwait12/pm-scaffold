# Thinking Framework · PRD Publish

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.


## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Testability before acceptance, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

## First Principles

- What is the deliverable: exact content fidelity of a confirmed PRD, nothing more?
- What must never change during export — content, decisions, knowledge states, confirmation metadata?
- Which "improvements" during export are actually unapproved changes in disguise?

## Medium-Aptation Fidelity (领域 lens)

The core publish discipline. Two axes:

1. **Formatting may adapt**: fonts, page breaks, layout, color, code-block wrapping, link styles — whatever a target medium requires.
2. **Content is immutable**: every sentence, heading, table cell, number, diagram, and metadata value stays byte-identical to the confirmed source.

For each target medium, ask:

- Feishu Docx: do headings, tables, and Mermaid diagrams render correctly?
- Feishu Markdown: does Mermaid render? (If not, record the limitation and prefer Docx + whiteboard.)
- PDF: do page breaks split tables? Are CJK fonts embedded?
- HTML: is it self-contained (inline CSS/JS)? Are links absolute?
- Markdown: are relative paths adjusted for the target location?

## Reader Perspective (领域 lens, from thinking-core.md §2)

Who reads each delivered copy and what must they find intact?

- Development: the traceability matrix (§7) and acceptance criteria.
- Testing: the exact wording of rules and acceptance criteria.
- Business: goals, scope, and confirmation metadata (version, reviewer, date).
- If one reader's section is missing or mangled, the publish is incomplete even if everything else looks fine.

## Systems Thinking

Check which downstream consumers depend on this published copy and what each needs intact. Check that publishing to one channel does not invalidate another (e.g., a PDF regenerated from an older source after HTML was already published).

## Adversarial Review

Try to invalidate the publish:

- Am I about to "helpfully" edit content during export?
- Does the source hash still match the confirmed SHA-256, or has tampering happened after confirmation?
- Am I declaring success without checking the destination, trusting the export tool's claim?

Record only findings that affect the candidate or require confirmation.

## Reverse Validation

Starting from the stakeholder reading the delivered copy, ask what must be true for the publish to be considered done: title correct, all headings present and ordered, tables intact, diagrams rendered, traceability intact, metadata visible, zero content drift. Check each against the actual destination, not the source file.

---

## Low-Density Degradation Mode

When the input is a single natural-language sentence with no confirmed PRD, no channel list, and no authorized publisher (see `SKILL.md` §1.1 for the gate), the lenses above cannot do meaningful work. Applying them to insufficient information produces verbose but empty analysis. Switch to degradation mode:

```text
low-density input → skip all-lens ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) input sufficiency assessment (PRD confirmed? channel list? authorized publisher?)
                      b) batched clarifying questions (each: AI preliminary judgment + options + impact + owner)
                   → status = needs_user_input
                   → wait for human to fill in, then re-enter Preflight in sufficient mode
```

Degradation triggers (any one is enough):

- the PRD's confirmation state is unknown or unverifiable
- no channel list (Feishu / PDF / HTML / Markdown) specified
- no authorized publisher identified in `authorized-reviewers.json`
- the user only says "发布一下 / 发出去" with no further context

This mode is not a failure state. It is the correct response to insufficient information — and for a publish skill it is especially important: publishing on insufficient information means shipping an unconfirmed or unverified document.

## Confirmation Bias Defense (publish specialization)

The publish step is where the AI is most tempted to "make things nicer" or "helpfully" correct the PRD while exporting:

1. Did I change any content during export, even a typo? If so, I have produced an unconfirmed copy.
2. Did I trust the export tool's success message, or verify the destination?
3. Am I declaring "published" for the user instead of requiring the authorized publisher's signature?

## Knowledge Boundary (publish specialization)

1. Did I distinguish "source PRD says X" (confirmed baseline) from "what I exported" (must be byte-identical)?
2. Did I record rendering limitations as `AI_INFERENCE`/advisory notes rather than silently accepting a mangled deliverable?
3. Are unverified delivery claims (e.g., "Feishu received it") marked as needing human confirmation, not asserted?
