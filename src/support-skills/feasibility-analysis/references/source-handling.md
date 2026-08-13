# Source Handling · Feasibility Analysis

## Source Register

Assign every source a stable ID and record:

```text
source_id
title_or_description
format (vendor quote / proposal / contract / past-project data / public pricing / compliance doc / internal estimate)
author_or_publisher
provided_by
created_at
retrieved_at
authority_scope (e.g., "official vendor quote — valid 30 days")
location_or_link
notes
```

Use `SRC-001`, `SRC-002`, and so on. Cost and compliance sources are time-sensitive — record retrieval dates.

## Extraction Rules

1. Extract source statements before normalization — quote figures, then interpret.
2. Keep the provider and location for material claims (who quoted the price, which proposal).
3. Separate explicit statements (a written quote, a compliance rule) from implied meaning (an estimate from a similar past project).
4. Record excluded material with a short reason when it appears relevant but is out of scope or duplicate.
5. Never treat the absence of a quoted price as "free" — that is `UNKNOWN`, not `FACT`.
6. Estimates are not facts: an AI-drafted budget is `AI_INFERENCE` or `ASSUMPTION` until the decision owner confirms it.

## Authority And Conflicts

Evaluate authority using:

1. explicit human confirmation for this project;
2. decision rights over the specific cost or constraint;
3. directness of the source (written quote > verbal estimate > AI estimate);
4. recency — a 3-month-old quote may not reflect current pricing;
5. corroboration by independent sources (two vendors quoting similar prices).

When statements conflict (e.g., vendor quotes differ, or finance vs product disagree on budget):

- preserve both statements and source IDs;
- explain the impact of each interpretation;
- identify the likely decision owner;
- mark the item `CONFLICT` and stop if it changes a material conclusion;
- never pick the more convenient figure silently.

## Research Boundary

Assessment can research publicly available facts (comparable products, industry cost benchmarks, published pricing), but it cannot confirm:

- internal budget authorization or procurement approvals;
- the acceptability of a compliance or data-security risk;
- internal resource availability.

Submit those to the responsible human. A recommendation that depends on an unconfirmed figure stays at `needs_user_input`.

## Mixed Media

- For vendor quotes/proposals: record quote date, validity window, and what is included vs excluded (hidden costs).
- For past-project data: record the project, its similarity to the current one, and the confidence of extrapolation.
- For compliance documents: record the regulation version and which requirement it constrains.
- For internal estimates: distinguish who estimated (AI / PM / engineering) and the evidence base.
