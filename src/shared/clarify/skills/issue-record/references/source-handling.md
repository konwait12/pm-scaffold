# Source Handling · Issue Record（跨阶段共享）

## Source Register

Issue-record sources are the phase artifacts plus raw materials that carry issue signals. Assign every source a stable ID and record:

```text
source_id
title_or_description
format                  (background-goal / 范围基线 / journey / UX / function-description / prd / 会议 / 邮件 / 口头)
author_or_speaker
provided_by
created_at
retrieved_at
authority_scope
location_or_link        (产物 § / 章节 / 行号 / 时间戳)
notes
```

Use `SRC-001`, `SRC-002`, and so on. Every issue also records its `affected_artifact` (which upstream artifact it came from).

## Extraction Rules

1. Extract issue signals as they appear: 待确认 / UNKNOWN / CONFLICT / 待决决策 / 风险 / 范围外.
2. For each signal, keep the exact trigger (the sentence or marker that raised it) and the artifact location — an issue without a traceable source cannot be verified or closed.
3. Separate "the artifact explicitly flags this" (FACT) from "I noticed a risk" (AI_INFERENCE) — the AI must not turn its own observation into a business fact.
4. Record excluded signals with a short reason (duplicate, already tracked, out of scope of the list).
5. Never treat an unrecorded 待确认 marker as resolved — the upstream mapping is an audit gate.

## Cross-Artifact Dedup

The same issue may surface in several phase artifacts (e.g., a conflict flagged in requirement-restate AND in background-goal). Rules:

- register one canonical ISS-NNN;
- cross-link the other occurrences to it;
- record each occurrence's location so the issue remains findable from every artifact;
- do not create a duplicate row per artifact.

## Authority And Conflicts

Decision authority is hierarchical: the goal decision owner / business sponsor owns `accepted` risks and the closed-out list; issue owners own their issue's state and target_close; verifiers confirm `resolved`.

When two artifacts conflict about whether an issue is real (e.g., one marks it BLK, another shows a workaround):

- preserve both claims and their locations;
- explain the impact of each interpretation;
- route the discrepancy to the issue owner or decision owner;
- never silently downgrade an issue to empty the list.

## Research Boundary

Research only when an external fact could resolve or mitigate an issue (regulatory text, platform capability, vendor contract) and is discoverable. Record source, date, fact/inference status, confidence, applicability, and decision impact.

Research cannot accept a risk, set a target close, or assign an owner — those are human decisions for the issue / decision owner.

## Mixed Media

- For phase artifacts, cite the exact section (§) and heading of the 待确认 / UNKNOWN / CONFLICT marker.
- For meetings, distinguish a stated decision from an unresolved discussion; keep the timestamp.
- For chat/tickets, preserve sender, thread context, and whether a later message supersedes an earlier one.
- For oral inputs, note the speaker and that it is not yet signed.
