# Source Handling · Competitive Research

## Source Register

Assign every competitor source a stable ID and record:

```text
source_id
title_or_description
format (official site / app store / user review / report / screenshot / video)
author_or_publisher
retrieved_at
authority_scope (e.g., "official pricing page — current" vs "vendor marketing")
location_or_link
notes
```

Use `SRC-001`, `SRC-002`, and so on. Record the retrieval date for every source so stale facts can be re-verified.

## Extraction Rules

1. Extract source statements before normalization — quote what the source says, then interpret.
2. Keep the publisher, page, and location for material claims.
3. Separate explicit statements (e.g., a published spec) from implied meaning (e.g., "their onboarding has 5 steps" inferred from a walkthrough video).
4. Record excluded material with a short reason when it appears relevant but is out of scope or duplicate.
5. Never treat "not found" as evidence that a competitor lacks a feature — that is `UNKNOWN`, not `FACT`.
6. A feature that exists only in a vendor's marketing copy is weaker evidence than one confirmed in a shipped product or user review.

## Authority And Conflicts

Evaluate authority using:

1. explicit human confirmation for this project;
2. directness of the source (shipped product > official docs > marketing > second-hand summary);
3. independence (a user review is stronger evidence of real-world behavior than the vendor's own claims);
4. recency and whether a later version explicitly supersedes an earlier one;
5. corroboration by independent sources.

When statements conflict (e.g., vendor claims a feature, user reviews say it does not work):

- preserve both statements and source IDs;
- explain the impact of each interpretation;
- identify the likely fact owner or decision owner;
- mark the item `CONFLICT` and stop if it changes a material conclusion;
- never pick the more convenient statement silently.

## Research Boundary

Competitive research is public-information research. It can establish what competitors visibly offer, but it cannot confirm:

- whether a competitor's internal product decision succeeded;
- our internal business intent, scope, or risk tolerance;
- the acceptability of copying a feature in our context.

Submit those to the responsible human. Findings that would change a material product decision stay at `needs_user_input` until confirmed.

## Mixed Media

- For official sites and docs: record the page and retrieve date; distinguish current vs archived versions.
- For app-store pages: distinguish the current listing from historical version notes.
- For user reviews: record the review platform and date; treat a single review as weak evidence, clusters as stronger.
- For screenshots/walkthrough videos: transcribe visible feature-bearing content and note uncertainty about what was not shown.
- For industry reports: record publisher, publication date, and whether the data is primary or secondary.
