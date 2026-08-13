# Thinking Framework · Competitive Research

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.


## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

## First Principles

- What observable user need does each competitor feature actually serve?
- Which competitor "best practices" are assumptions disguised as requirements?
- Would our confirmed goal still make sense if every competitor were removed?
- Which of our differences are real moats versus accidental gaps?

## Positioning Mapping (领域 lens)

For each competitor, determine:

- What market problem do they solve, for whom?
- Who is their primary user vs secondary user?
- What is their core value proposition — and the one thing they refuse to do?
- Where do they sit on the 2 axes that matter to OUR confirmed goals (e.g., 易用性 × 功能深度, 价格 × 定制化)?

Plot all competitors. Identify the empty quadrant, then ask: is it empty because it is an opportunity, or because it is a trap (no demand / no willingness to pay / high cost)?

## Differentiation Scan (领域 lens)

Compare competitors on the dimensions that matter to OUR confirmed goals, not on generic checklists:

- Feature completeness relative to our goal G#
- User experience quality on the flow we care about
- Price/cost structure and packaging model
- Domain specialization

Identify: what can we NOT easily replicate (moat) vs what gaps can we exploit? A feature competitors all lack is only an opportunity if our goal requires it.

## Pattern Extraction (领域 lens)

Extract reusable patterns (not copy):

- Interaction patterns that work well and reduce user effort
- Information architecture choices that clarify the same problem we face
- Pricing or packaging models that signal value

**Anti-pattern**: Listing competitor features without mapping them to our goals. "Competitor X has Y" is data; "Y serves our G2 goal because..." is analysis.

## Inference Discipline (领域 lens)

All competitive findings are **AI_INFERENCE** until the business owner confirms applicability. Competitor success in their context does not guarantee success in ours. When a competitor insight is used, record:

- the evidence (SRC-ID) behind it;
- the context that made it work there;
- what would have to be true here for it to apply.

**Anti-pattern**: Presenting "Competitor X does Y" as justification for "we should do Y" without mapping to our confirmed business context.

## Systems Thinking

Check whether a "we should copy X" conclusion affects upstream/downstream decisions: which segment, journey, or feature decision does it steer? Which other roles' work does it change? Does it create a dependency we cannot afford?

## Adversarial Review

Try to invalidate the research:

- Is the benchmark competitor really comparable, or a category mismatch?
- Does the evidence come from a single interested source (vendor marketing, a competitor's own blog)?
- Am I confirming an early hypothesis instead of letting the data speak?
- Is "differentiation" real or just feature noise users do not care about?

Record only findings that affect the candidate or require confirmation.

## Reverse Validation

Starting from our intended differentiation, ask what competitors must be failing at and what we must prove. Use the result to reveal missing evidence, unverified assumptions, and open questions.

---

## Low-Density Degradation Mode

When the input is a single natural-language sentence with no confirmed background, no research goal, and no sources (see `SKILL.md` §1.1 for the gate), the lenses above cannot do meaningful work. Applying them to insufficient information produces verbose but empty analysis. Switch to degradation mode:

```text
low-density input → skip all-lens ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) input sufficiency assessment (research goal missing? competitor scope missing? business baseline missing?)
                      b) batched clarifying questions (each: AI preliminary judgment + options + impact + owner)
                   → status = needs_user_input
                   → wait for human to fill in, then re-enter Preflight in sufficient mode
```

Degradation triggers (any one is enough):

- no confirmed `background-goal.md` or scope baseline to anchor the research
- no research goal (business-level vs functional-level not stated)
- no competitor candidates and no access to public sources
- the user only mentions a feature ("看看别人怎么做这个功能") with no decision it should inform

This mode is not a failure state. It is the correct response to insufficient information — saving human review time and producing one clean batch of clarifying questions rather than a 10-competitor artifact full of `待确认`.

## Confirmation Bias Defense (competitive specialization)

Competitive analysis is a magnet for confirmation bias — the AI finds the competitor that "proves" what the requester already wanted to build:

1. Did I search for evidence that the benchmark competitor is actually NOT doing well on our axis — or only evidence that supports copying?
2. Did I weight a competitor's official marketing as highly as independent user reviews?
3. If the requester named a competitor upfront, did I independently verify that competitor is the right benchmark, or quietly agree?

## Knowledge Boundary (competitive specialization)

1. Did I distinguish "official source says X" (FACT), "I inferred X from screenshots/reviews" (AI_INFERENCE), and "no public data" (UNKNOWN)?
2. Did I record retrieval dates so stale competitor facts can be re-verified?
3. Are unsupported "we should copy Y" conclusions separated from evidence-backed ones?
