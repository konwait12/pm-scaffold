# Thinking Framework · validation-rules

Use these lenses to improve the candidate. Do not dump the full analysis into the artifact.

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Testability before acceptance criteria, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

## Domain Lens A: Input Enumeration (输入完整)

- Have I enumerated the complete user input surface: form fields, search/filter params, uploaded files, query params, batch-pasted data?
- Are there hidden inputs — URL-state params, defaults the user can overwrite — that also need checks?
- Am I writing checks on read-only / system-generated fields that can never fail (never-trigger rules)?

## Domain Lens B: Boundary Precision (边界清晰)

For each input field, write both the legal side and the illegal side:

- format (regex / mask), range (open/closed intervals and the equals sign), length cap, required / optional, allowed value set
- boundary values: min, max, empty string, over-length, special chars, Unicode — which side do they fall on?

A check like "校验手机号格式" or "金额不能太大" is **not decidable** — no executable value domain, no pass/fail case. Rewrite it.

## Domain Lens C: Cross-Field & Referential Integrity (跨字段)

- Does a field's validity depend on other fields or existing data: conditional-required (select A → B required), mutual exclusion (A and B cannot both be filled), composite uniqueness, referential integrity (FK/code must exist upstream)?
- Do the direction and granularity of these dependencies match the referenced `BR-XXX` / UX — or did I invent a cross-field rule that contradicts them?

## Domain Lens D: User-Facing Error (用户可读错误)

- Does every VL carry a Chinese, natural-language, actionable message — what is wrong, what value is expected, how to fix?
- Does the message distinguish 必填缺失 / 格式错误 / 超出范围 / 已存在冲突, instead of one blanket "输入无效"?
- Is the message product copy, not a dev error code or English translation?

## Domain Lens E: Traceability & Knowledge State (可追溯)

- Does every VL-XXX trace to a confirmed `FUN-XXX` → `FEA-XXX` / `ST-XXX` / `BR-XXX`?
- Is the value domain a business fact (`FACT`), a decided policy (`DECISION`), my inference (`AI_INFERENCE`), or unknown (`UNKNOWN`)?
- Are inferred or unknown value domains hung on the 待确认问题 register instead of written as settled facts?

---

## Low-Density Degradation Mode

When a function's confirmed source contains only a bare field name with no format, length, or rule, the lenses above cannot do meaningful work. Applying them to insufficient information produces verbose but empty checks. Switch to degradation mode:

```text
low-density input → skip domain-lens ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) input sufficiency assessment (which fields are confirmed, which rules are missing)
                      b) batched clarifying questions (each: AI preliminary judgment + options + impact + owner)
                   → status = needs_user_input
                   → wait for human to fill in, then re-enter Preflight in sufficient mode
```

Degradation triggers (any one is enough):

- a field is listed with no format, range, length, or required flag anywhere in the confirmed source
- the only "rule" for an input is a bare field name and a button label
- the value domain that determines a check is unconfirmable by any source

This mode is not a failure state. It is the correct response to insufficient information — one clean batch of questions instead of a §系统校验 table full of `待确认` and guessed regexes.

## Confirmation Bias Defense (validation-rules specialization)

1. Did I copy the value domains the user happened to mention, or did I ask whether they are the business rule?
2. Am I labeling an inferred format as `FACT`, or checking whether it is `AI_INFERENCE` first?
3. If the check would reject a legitimate business value (over-validation), did I flag it or quietly accept the strictness?

## Knowledge Boundary (validation-rules specialization)

1. Did I distinguish "UX defines the format as X" (`FACT`), "I inferred a reasonable format" (`AI_INFERENCE`), and "nobody specified the format" (`UNKNOWN`)?
2. Did I keep unconfirmed error-message wording in the 待确认问题 register instead of inventing final copy?
3. Are knowledge-state tags on each VL row, or buried in prose?
