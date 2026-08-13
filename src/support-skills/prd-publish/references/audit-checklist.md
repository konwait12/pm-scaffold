# Audit Checklist · PRD Publish

## Structural Gate

- All required headings exist (`发布前检查`, `发布渠道`, `通知`) before the version-change summary.
- Metadata includes artifact ID, version, status, publisher, reviewer, and dates or `待确认` / `TBD`.
- Publish record contains: source PRD artifact ID + SHA-256, destination links/paths per channel, verifier, timestamp.
- Blocking questions are marked explicitly.

## Confirmation Gate

- PRD status is `confirmed` with a valid ReviewRecord.
- Source file hash matches the confirmed SHA-256 (tamper check).
- All upstream artifacts (5 main Work Items) are `confirmed`.
- No open REVISION-level review findings.
- The publisher is present in `00-input/authorized-reviewers.json` with the right role.

## Destination Fidelity Gate

Checked against the actual destination, not the source file:

- Document title matches PRD title.
- All section headings present and in correct order.
- All tables rendered (no missing columns/rows).
- All Mermaid/flowchart diagrams visible (or limitation recorded).
- Traceability matrix (§7) intact.
- Version and confirmation metadata visible.
- No content added, removed, or reworded — byte-identical check against source.

## Semantic Gate

- Only formatting adapted to the medium; content is immutable.
- Rendering limitations are recorded explicitly, not silently accepted.
- Delivery claims (e.g., "Feishu received it") are verified or marked `AI_INFERENCE` pending human confirmation.
- No content change was made during export (typo fixes included).

## Quality Lenses

- First principles: the deliverable is exact fidelity of confirmed content — nothing else.
- Systems thinking: downstream consumers (dev/test/business) each have their sections intact.
- Adversarial review: at least one "silent drift / tampered source / tool lied" scenario was checked.
- Reverse validation: every reader-facing element was verified at the destination.
- Minimal sufficiency: the record contains what verification needs and excludes new content.

## Human Gate

Set `needs_user_input` when confirmation state, channel list, or publisher is unresolved.

Set `conditional_review` only when remaining unknowns are non-blocking, have owners, and include deferral risks (e.g., a known Mermaid limitation in one channel).

Set `ready_for_human_review` only when all other gates pass. Never set `confirmed` — only the authorized publisher can sign the record.

## Audit Report Shape

```text
status_recommendation
passed_checks
failed_checks
repairs_applied
blocking_questions
nonblocking_unknowns
decisions_required
traceability_gaps
downstream_risks
```
