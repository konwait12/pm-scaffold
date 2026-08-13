# Source Handling（Brainstorming）

## L0: No Source Is The Normal Case

At L0 the requirement is a one-line idea with **no source materials**. This is the skill's default environment, not an error:

- Preserve the raw idea text **verbatim** in `§1 原始输入` and quote it inside Evidence cells. Do not polish it into "facts".
- Everything beyond the raw idea is `AI_INFERENCE` — including roles, lifecycle stages, and constraints the AI finds "obvious".
- Do not invent SRC-IDs for materials that do not exist. Evidence cells may cite `原始想法原文` or state `AI 推断，无书面来源`.

## Source Register (when materials do exist)

Materials that appear while diverging (a message, email, meeting note) are registered as `SRC-001`, `SRC-002`, … with the same record fields as the stage skills:

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

For a chat/email, distinguish the original wording from an AI summary. Add the SRC-ID to the Evidence cells that rely on it.

## Extraction Rules

1. Extract the raw idea before interpreting it.
2. Keep the speaker/author and location for material claims.
3. Separate explicit statements from implied meaning — implied meaning is `AI_INFERENCE`.
4. Record excluded material with a short reason when it appears requirement-bearing but is out of the current boundary.
5. Never treat absence of evidence as evidence of absence.

## Authority And Conflicts

Do not define a universal source-type priority. Evaluate authority using:

1. explicit human confirmation for this project;
2. decision rights over the specific business fact;
3. directness of the source;
4. recency and whether a later statement explicitly supersedes an earlier one;
5. corroboration by independent sources.

When statements conflict:

- preserve both statements and source IDs;
- explain the impact of each interpretation;
- identify the likely fact owner or decision owner;
- mark the item `CONFLICT` and stop if it changes a material candidate;
- never pick the more convenient statement silently.

## Research Boundary

- Research only when an external fact could materially improve divergence and is discoverable. Record source, date, fact/inference status, confidence, applicability, and decision impact.
- Research **cannot** confirm internal business intent, audience definition, business ownership, or the acceptability of risk. Those go to the responsible human as Clarify questions.
- `research` disposition means the item needs follow-up (owner + question + deadline); register it in issue-record / a QuestionRecord instead of leaving it unowned.

## Mixed Media

- For slides/documents: preserve slide/page/section locations.
- For meeting records: distinguish speaker statements, decisions, suggestions, and unresolved discussion.
- For chat/email threads: preserve sender, context, date, and whether a later message supersedes an earlier one.
