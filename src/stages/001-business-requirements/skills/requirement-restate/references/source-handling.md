# Source Handling · Requirement Restate

## Source Register

Assign every source a stable ID and record:

```text
source_id
title_or_description
format
author_or_speaker
provided_by
created_at
retrieved_at
authority_scope
location_or_link
notes
```

Use `SRC-001`, `SRC-002`, and so on. For meetings, distinguish the transcript from an AI-generated summary. For chat/tickets, preserve the thread context and timestamps.

## Extraction Rules

1. Extract candidate asks **verbatim** before normalization — the original phrasing is the artifact's raw material.
2. Keep the speaker or author and location for every ask; a later restatement must be able to trace back.
3. Separate explicit statements from implied meaning; implied meaning becomes `AI_INFERENCE`, never `FACT`.
4. Merge duplicates across sources explicitly: note "same ask, different words (SRC-001 vs SRC-002)" instead of silently dropping one.
5. Never treat absence as evidence that a requirement does not exist.

## Term Unification

Different sources may use different terms for the same object or action. Do not silently unify:

- record both terms with a mapping (`客户` = `会员`, `核销` = `销核`);
- flag a term difference for stakeholder confirmation if it might hide a scope/object difference (e.g., `客户` includes anonymous visitors but `会员` does not);
- keep the stakeholder's preferred term as the primary label in the restatement.

## Authority And Conflicts

Do not define a universal source-type priority. Evaluate authority using:

1. explicit human confirmation for this project;
2. decision rights over the specific ask;
3. directness of the source;
4. recency and whether a later statement explicitly supersedes an earlier one;
5. corroboration by independent sources.

When statements conflict:

- preserve both phrasings and source IDs in the CONFLICT list;
- explain the impact of each interpretation;
- identify the stakeholder who should choose;
- mark the item `CONFLICT` — do **not** resolve it here;
- never pick the more convenient statement silently.

## Research Boundary

Research only when an external fact could disambiguate an ask (industry definition of a term, a standard the ask references) and is discoverable. Record source, date, fact/inference status, confidence, applicability, and decision impact.

Research cannot confirm what the stakeholder meant or which phrasing they approve. That is a human decision; submit it to the stakeholder.

## Mixed Media

- For slides and documents, preserve slide/page/section locations.
- For audio/video transcripts, preserve the timestamp of each ask; note if the transcript is AI-generated.
- For chat/tickets, preserve sender, thread context, date, and whether a later message supersedes an earlier one.
- For images, transcribe visible requirement-bearing text and note uncertainty.
