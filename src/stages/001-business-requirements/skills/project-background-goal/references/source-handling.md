# Source Handling

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

Use `SRC-001`, `SRC-002`, and so on. For meetings, distinguish the transcript from an AI-generated summary.

## Extraction Rules

1. Extract source statements before normalization.
2. Keep the speaker or author and location for material claims.
3. Separate explicit statements from implied meaning.
4. Record excluded material with a short reason when it appears requirement-bearing but is out of scope or duplicate.
5. Never treat absence as evidence that a requirement does not exist.

## Authority And Conflicts

Do not define a universal source-type priority. Evaluate authority using:

1. explicit human confirmation for this project;
2. decision rights over the specific business fact or goal;
3. directness of the source;
4. recency and whether a later statement explicitly supersedes an earlier one;
5. corroboration by independent sources.

When statements conflict:

- preserve both statements and source IDs;
- explain the impact of each interpretation;
- identify the likely fact owner or decision owner;
- mark the item `conflict` and stop if it changes a material conclusion;
- never pick the more convenient statement silently.

## Research Boundary

Research only when an external fact could materially improve background understanding and is discoverable. Record source, date, fact/inference status, confidence, applicability, and decision impact.

Research cannot confirm internal business intent, project scope, business ownership, or the acceptability of risk. Submit those to the responsible human.

## Mixed Media

- For slides and documents, preserve slide/page/section locations.
- For images, transcribe visible requirement-bearing text and note uncertainty.
- For meeting records, distinguish speaker statements, decisions, suggestions, and unresolved discussion.
- For email threads, preserve sender, recipient context, date, and whether a later message supersedes an earlier one.