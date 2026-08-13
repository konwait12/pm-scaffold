# Source Handling · Project Scope

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

1. Extract candidate scope items before classification — capture what each stakeholder actually asked for.
2. Keep the speaker or author and location for each item; do not merge different sources' items into one.
3. Separate explicit scope statements ("we are NOT doing X") from implied scope ("we focus on X").
4. Record excluded material with a short reason when it appears scope-bearing but is duplicate or out of this project.
5. Never treat absence as evidence that a scope item does not exist.

## Authority And Conflicts

Do not define a universal source-type priority. Evaluate authority using:

1. explicit human confirmation for this project;
2. decision rights over the specific boundary (goal decision owner > requester);
3. directness of the source;
4. recency and whether a later statement explicitly supersedes an earlier one;
5. corroboration by independent sources.

When statements conflict on a boundary:

- preserve both statements and source IDs;
- explain the impact of each interpretation on the In/Out/Deferred/Conditional lists;
- identify the likely decision owner;
- mark the item `CONFLICT` and stop if it changes a material scope conclusion;
- never pick the more convenient statement silently.

## Research Boundary

Research only when an external fact could materially improve the boundary (public product documentation, vendor capability, existing contracts) and is discoverable. Record source, date, fact/inference status, confidence, applicability, and decision impact.

Research **cannot** confirm whether something is in this project's scope — scope is a business decision owned by the goal decision owner / business sponsor. Submit boundary questions to the responsible human.

## Decision Records As Sources

A named DECISION (from Human Gate or issue-record) is a legitimate source for an In/Out/Deferred/Conditional classification. Record `DEC-XXX` alongside `SRC-XXX` so downstream can trace "who decided this boundary, when, and why".

## Mixed Media

- For slides and documents, preserve slide/page/section locations.
- For images, transcribe visible scope-bearing text and note uncertainty.
- For meeting records, distinguish statements, decisions, suggestions, and unresolved discussion.
- For email threads, preserve sender, recipient context, date, and whether a later message supersedes an earlier one.
