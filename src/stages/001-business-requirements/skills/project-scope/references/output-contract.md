# Output Contract · Project Scope

## Artifact States

| Status | Meaning | Downstream use |
|---|---|---|
| `draft` | Initial candidate; Audit not complete | No |
| `needs_user_input` | A boundary decision blocks confirmation | No |
| `conditional_review` | Reviewable with explicit non-blocking unknowns | No |
| `ready_for_human_review` | Self-audit passed; waiting for authorized review | No |
| `confirmed` | Authorized human explicitly approved the scope | Yes |
| `superseded` | A newer confirmed scope replaces this version | No |

## Version Rules

- Start at `v0.1`. Increment minor on human-requested revision.
- `v1.0` for first confirmed baseline.
- Keep a concise change summary between human-facing versions.

## Knowledge-State Labels

Same as project-background-goal: `FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`.

## Required Sections

| § | Heading | Required |
|---|---|---|
| 1 | 项目元数据 | Yes |
| 2 | 范围总览（In/Out/Deferred/Conditional 计数） | Yes |
| 3 | In-Scope（已确认纳入本期） | Yes |
| 4 | Out-of-Scope（已确认不做 + 原因） | Yes |
| 5 | Deferred（暂缓做 + 触发条件） | Yes |
| 6 | Conditional（条件成立则纳入） | Yes |
| 7 | 来源追溯（SRC-IDs） | Yes |
| 8 | 待确认问题 | Yes |
| 9 | Constitution Compliance | Yes |

If a section has no confirmed content, write `待确认` and link it to a question or unknown ID; do not delete the heading.

## Scope Item Schema

Each item in §3-§6 must have:

| Field | Required | Description |
|---|---|---|
| `S-NNN` (ID) | Yes | Monotonic, scoped to this artifact |
| `description` | Yes | One sentence, testable |
| `knowledge_state` | Yes | One of 6 labels |
| `source_or_decision` | Yes | SRC-ID or DEC-ID |
| `acceptance_criterion` | Yes (In) / Optional (Out/Deferred/Conditional) | How we know it's done or excluded |
| `stakeholder` | Optional | Who raised/owns this item |
| `notes` | Optional | Edge cases, dependencies |

## Human Responsibilities

- Goal decision owner / business sponsor: approves the final boundary.
- Product manager: ensures completeness and consistency with background-goal.
- Final reviewer: authorizes the scope for downstream use.

## Downstream Handoff

Emit a compact handoff:

```text
confirmed_version
in_count
out_count
deferred_count
conditional_count
in_items (id list)
open_nonblocking_unknowns
source_ids
```

## Clarifications Session Contract

Same as project-background-goal: structured rows in `## Clarifications` section, one row per Session, ≤5 sessions, `accepted_answer` filled before `ready_for_human_review`.
