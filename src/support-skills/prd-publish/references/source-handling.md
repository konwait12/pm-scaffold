# Source Handling · PRD Publish

## Source Register

Assign every source a stable ID and record:

```text
source_id
title_or_description
format (confirmed PRD file / ReviewRecord / authorized-reviewers.json / export tool output / channel link)
author_or_publisher
provided_by
retrieved_at
authority_scope (e.g., "confirmed v1.0 baseline — sha256:...")
location_or_link
notes
```

Use `SRC-001`, `SRC-002`, and so on. The confirmed PRD file is `SRC-001` by convention; its SHA-256 is the anchor every delivered copy is checked against.

## Extraction Rules

1. Extract the confirmed baseline verbatim — never paraphrase the PRD content.
2. Keep the artifact ID, version, and SHA-256 for every material reference.
3. Separate explicit statements (confirmed PRD content, ReviewRecord fields) from implied meaning (e.g., "the export succeeded" inferred from a tool message).
4. Record excluded material with a short reason when it appears relevant but is out of scope or duplicate.
5. Never treat an unverified export as a verified delivery — a tool's success message is `AI_INFERENCE` until the destination is checked.
6. The publish record is not a content source; it is an audit trail of what was delivered and verified.

## Authority And Conflicts

Evaluate authority using:

1. explicit human confirmation (ReviewRecord) — the single source of truth;
2. decision rights over the publish (authorized reviewers list);
3. directness (confirmed PRD file > export output > tool status message);
4. recency and whether a later confirmation supersedes an earlier one;
5. corroboration (destination copy matches source hash).

When statements conflict (e.g., source hash vs current file content — possible post-confirmation tampering):

- preserve both statements and source IDs;
- explain the impact of each interpretation;
- identify the likely owner;
- mark the item `CONFLICT` and STOP publishing if it changes the confirmation state;
- never pick the more convenient version silently.

## Research Boundary

Publish can read the confirmed PRD, ReviewRecord, and authorized-reviewers list, and can verify destination copies. It cannot confirm:

- whether the business still agrees with the PRD content (that is change-management);
- whether recipients actually read the notification (that is delivery confirmation);
- whether a target channel is compliant for external distribution (that is a human decision).

Submit those to the responsible human. A delivery claim that depends on an unverified fact stays at `needs_user_input`.

## Mixed Media

- For the confirmed PRD: record artifact ID, version, SHA-256, and the confirmed date — the fidelity baseline.
- For ReviewRecord: record reviewer, reviewer role, decision, and reviewed timestamp.
- For `authorized-reviewers.json`: record id, name, and allowed roles — match the publisher against it.
- For export tool output: record the tool, the command, and treat its success claim as unverified until the destination is checked.
- For channel links: record the link/path and the verification result (title, headings, tables, diagrams, metadata).
