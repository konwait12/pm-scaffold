# Source Handling · Tracking Plan

## Source Register

Tracking-plan sources are primarily **upstream confirmed artifacts** rather than raw meeting minutes. Assign every source a stable ID and record:

```text
source_id
title_or_description
format                  (function-description / product-ux / business-rules / background-goal / 口头补充)
author_or_speaker
provided_by
created_at
retrieved_at
authority_scope
location_or_link        (artifact § / 章节 / 行号)
notes
```

Use `SRC-001`, `SRC-002`, and so on. Additionally, every event must carry the upstream functional references it derives from: `FUN-XXX` / `IX-XXX` / `BR-XXX` and the goal `G-X`.

## Extraction Rules

1. Extract candidate events from confirmed upstream functions and rules — do not invent events beyond what the confirmed functions imply.
2. For each event, record which upstream reference supports it (FUN-XXX for the action, IX-XXX for the interaction, BR-XXX for the rule that triggers an error/edge event).
3. Separate "upstream says this action happens" (FACT, already confirmed) from "I infer this needs tracking" (AI_INFERENCE).
4. Record excluded events with a short reason when they appear trackable but are out of scope or duplicate.
5. Never treat a missing event as evidence that no tracking is needed — a coverage gap is a blocking finding, not an assumption.

## Authority And Conflicts

Upstream confirmed artifacts (function-description, product-ux, business-rules, background-goal goals) are the authoritative sources for whether an action exists. Metrics and platform coverage are owned by the metric_owner / data_owner.

When upstream artifacts conflict (e.g., BR-XXX says an action is forbidden while FUN-XXX lists it):

- preserve both references;
- explain the impact on the event contract;
- mark the item `CONFLICT` and stop if it changes coverage or PII handling;
- never silently drop the conflict — route it to the parent function-description Skill.

## Research Boundary

Research only when an external fact could improve the contract (platform SDK event conventions, industry event naming, data-protection rules) and is discoverable. Record source, date, fact/inference status, confidence, applicability, and decision impact.

Research cannot confirm whether a function needs tracking, which metric the business wants, or acceptable PII handling for this product — submit those to the metric_owner / data_owner.

## Mixed Media / Upstream Artifact Handling

- For function-description, note the specific FUN-XXX and section the event derives from.
- For product-ux, note the IX-XXX interaction rule and the page/step in the flow.
- For business-rules, note the BR-XXX rule and the failure condition that produces an error event.
- For background-goal, note the G-X target that the event must help verify.
