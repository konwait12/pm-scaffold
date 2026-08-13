# Thinking Framework · Issue Record

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

## Triage（问题分诊）

The first decision for any signal is category. Ask in order:

- **BLK（Blocker）**: Does this truly block progress, or is there a workaround? If a workaround exists, it may be RSK, not BLK.
- **RSK（Risk）**: Could this become a blocker? Does it have a mitigation?
- **DEC（Decision-in-waiting）**: Does a named person need to decide? Who, and by when?
- **INF（Information gap）**: Is a source, datum, or permission missing?
- **CLS（Clarification）**: Is the wording ambiguous and needs an owner to disambiguate?
- **OUT（Out-of-band）**: Was it raised but is outside this project's scope?

Mis-triage (BLK when it is really DEC, INF when it is really CLS) sends the issue to the wrong owner and stalls it.

## Ownership（责任归属）

- Does every open issue have an owner with the authority to resolve it?
- Is the owner a person or a role, not "TBD"? (Fix: ask for the owner in Clarify.)
- For `accepted` risks: only the decision owner may accept. Did a named decision owner accept, or did the AI?

## Aging And Escalation（时效与升级）

- Does every BLK / DEC carry a `target_close`? Without one, it can drift forever.
- Are issues older than 30 days reviewed for escalation? Stale issues are a project-health signal.
- Is each escalation routed to a new owner with the authority to act?

## Closed-Loop Verification（闭环验证）

- Is a `resolved` issue linked to the artifact change that closed it — or just declared resolved?
- Was the resolution verified by a verifier distinct from the implementer?
- Do accepted risks carry the acceptance condition and date, not just "accepted"?

## Pre-Mortem（事前验尸 · thinking-core §2 领域 lens）

Issue Record is the natural home for the failure rehearsal. Before PRD confirmation, run it:

- If this project ships as-is, what is the most likely thing to fail? Which open issue would cause it?
- What are the 3-5 most probable failure causes? Do they each have an owner and a mitigation (or an accepted risk)?

## Adversarial Review

- Is a BLK really blocking, or was it labeled BLK because it is uncomfortable?
- Is a risk being downgraded because it is inconvenient to track?
- Is an issue being closed without evidence, just to empty the list?

## Confirmation Bias Defense (Issue specialization)

The AI must not quietly absorb "待确认" signals into the artifact without a decision:

1. Did I ask "要不要登记为 ISS-NNN" before continuing, or did I silently continue?
2. Did I assign a category that flatters the story (INF instead of DEC, RSK instead of BLK) to avoid escalation?
3. Did I accept a risk on the user's behalf, or did a named decision owner accept it?

## Knowledge Boundary (Issue specialization)

1. Did I distinguish "the upstream artifact explicitly flags this" (FACT) from "I noticed a risk" (AI_INFERENCE)?
2. Are unknown facts marked UNKNOWN, not written as assumptions?
3. Are conflicts preserved with both sides, not collapsed into one?

---

## Low-Density Degradation Mode

When no issue signal exists (no 待确认 / UNKNOWN / CONFLICT / risk anywhere), the lenses above have nothing to work on. Switch to degradation mode:

```text
no-issue-signal input → skip lens ideation
                       → do not invent issues
                       → return a routing receipt:
                          "issue-record has no new entries; list may stay as-is"
                       → no status change, no Generate / Audit
```

Degradation triggers (any one is enough):

- all upstream artifacts are confirmed with no pending markers
- no contradiction, no decision-in-waiting, no risk signal anywhere
- the user only confirms existing issues without raising new ones

This mode is not a failure state. Invented issues pollute the list and waste the decision owner's attention. An empty list that is honest beats a full list that is fiction.

## Clarify 是独立闭环

每次 Clarify Session 一行一 session（≤5），`accepted_answer` 在 `ready_for_human_review` 前必填；答案回写目标产物章节（`reflow_target`）。登记问题本身必须先经用户确认——这是 issue-record 的独特契约，违反即反模式。
