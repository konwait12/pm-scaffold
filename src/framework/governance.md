# Governance And Quality Gates

## Quality Sequence

Each work item runs structural validation, semantic/domain audit, communication check and human review. PRD assembly additionally runs cross-artifact relationship and record validation.

## Confirmation

`confirmed` requires a reviewer authorized by the requirement's `00-input/authorized-reviewers.json`; the selected role must also appear in the Work Item's registry `reviewer_roles`. The ReviewRecord binds timestamp, stable reviewer ID, role and reviewed artifact version/hash. `ready_for_human_review`, `conditional_review`, `simulated` and `needs_user_input` are not completion. Human rejection or any blocking machine gate returns failure.

## Quality Dimensions

Completeness, correctness, clarity, traceability, consistency, verifiability, role/scene coverage, and downstream usability. Keyword presence alone is not evidence that a contract is satisfied.

## Work In Progress

Only one work item is active for a requirement. A blocked item remains visible with owner, impact and reflow target. Repeated revision of the same issue triggers escalation and direction review.

## Change Control

Scope freezes after confirmed product UX. New features require an upstream story or explicit upstream reflow. A changed confirmed artifact invalidates affected downstream confirmation until rerun.

## Human-In-The-Loop Inquiry Contract (Global)

The scaffold is not a "one PRD fits all" generator. Every branch and every artifact has a **default behavior** and an **inquiry gate** that asks the user whether to override.

### Inquiry Gate — When To Ask

Every Skill must trigger a structured inquiry when ANY of these conditions occur:

1. **PRD section inclusion**: when the Skill produces content that *could* be embedded into `prd.md` but is not strictly required (e.g., scope baseline, tracking plan, issue-record risk summary, requirement-restate provenance).
2. **Decision-shaped input**: when the user input contains "待确认 / 不确定 / 可能 / 也许 / ? / TODO / TBD / 再看看 / 之后再说" markers.
3. **Cross-source conflict**: when two sources give different statements on the same fact.
4. **Optional capability branch**: when entering a conditional branch (e.g., "do we need brainstorming? do we need solution assessment? do we need competitive research?").

### Inquiry Template

> I notice we are at [branch / artifact X]. The default behavior is [Y].
> Do you want to:
> 1. Keep default (Y)
> 2. Include / exclude [artifact X] in / from prd.md §N
> 3. Defer this decision to a later stage
> 4. Cancel this branch

### Main Trunk vs. Branch — Strict Distinction

| Class | Definition | PRD Treatment |
|---|---|---|
| **Main Trunk**（5 work_items） | `project-background-goal` / `user-journey-and-stories` / `product-ux` / `function-description` / `prd-assembly` itself | **Required, no inquiry.** Trunk content goes into the corresponding fixed PRD section without asking. |
| **Branch / Optional**（everything else） | sub-skills of function-description, shared mechanisms (clarify, brainstorming, change-management, decision-log, intake-routing, project-init, human-gate, audit, traceability), optional support skills (project-scope, tracking-plan, requirement-restate, issue-record, competitive-research, solution-assessment, ...) | **Inquiry required.** Every branch entry triggers the inquiry template. Default behavior per artifact (see table below). |

The main trunk is **non-negotiable** because the PRD cannot exist without background, journey, UX, functions, and assembly. Branches are **configurable** because each requirement genuinely has different scope, depth, and visibility needs.

### Default Behaviors By Artifact

| Artifact | Class | Default PRD inclusion | Inquiry gate | Override effect |
|---|---|---|---|---|
| `project-background-goal` | Trunk §1 | Required (§1) | None | — |
| `user-journey-and-stories` | Trunk §2 | Required (§2) | None | — |
| `product-ux` | Trunk §3 | Required (§3) | None | — |
| `function-description` | Trunk §4 | Required (§4) | None | — |
| `prd-assembly` | Trunk §5-§10 | Required (§5-§10) | None | — |
| `business-rules` | Sub of §4 | **Aggregate into §4** | Inquiry at sub-skill entry | User can split or omit BR detail |
| `validation-rules` | Sub of §4 | **Aggregate into §4** | Inquiry at sub-skill entry | User can split or omit VL detail |
| `state-machine` | Sub of §4 | **Aggregate into §4** | Inquiry at sub-skill entry | User can inline or skip |
| `exception-handling` | Sub of §4 | **Aggregate into §4** | Inquiry at sub-skill entry | User can inline or skip |
| `acceptance-criteria` | Sub of §4 | **Aggregate into §4** | Inquiry at sub-skill entry | User can split or omit AC detail |
| `tracking-plan` | Sub of §4 (optional) | Optional (§5.2 埋点) | Inquiry at sub-skill entry + prd-assembly §5 | Verbatim event table in §5.2 if user accepts |
| `project-scope` | Branch (001) | Optional (§5.1 范围) | Inquiry at Skill entry + prd-assembly §5 | In/Out/Deferred/Conditional lists in §5.1 if user accepts |
| `requirement-restate` | Branch (001) | Default NOT in PRD | Inquiry at Skill entry | User can attach RR-XXX provenance to §0 |
| `issue-record` | Branch (shared) | Default NOT in PRD | Inquiry at Skill entry + prd-assembly §9 | User can expose risk summary in §9 / §10 if visibility is needed |
| `competitive-research` | Branch (support) | Optional (supporting evidence) | Inquiry at Skill entry | User can attach comparison table to §0 or as appendix |
| `solution-assessment` | Branch (support) | Optional (supporting evidence) | Inquiry at Skill entry | User can attach trade-off analysis to §0 or as appendix |
| `brainstorming` | Branch (shared) | Optional (process record) | Inquiry at Skill entry | User can attach distilled outcomes to §0 |
| `clarify` cycle | Branch (shared) | Internal; not a PRD artifact | (n/a) | Its results feed issue-record or upstream artifacts |
| `change-management` | Branch (shared) | Triggers reflow, not PRD content | (n/a) | Changes upstream artifacts → invalidates affected downstream until rerun |
| `decision-log` | Branch (shared) | Optional (DEC-XXX in §11 事实与决定) | Inquiry at Skill entry | User can consolidate decisions into §11 |
| `intake-routing` | Branch (shared) | Pre-flow; not a PRD artifact | (n/a) | Routes incoming request to background-goal or reflow |
| `project-init` | Branch (shared) | Pre-flow; not a PRD artifact | (n/a) | Creates REQ-DIR skeleton |
| `human-gate` | Branch (shared) | Governance; not a PRD artifact | (n/a) | Each Trunk / Branch needs a review record before `confirmed` |
| `audit` | Branch (shared) | Triggers §10 inconsistency report | (n/a) | Findings in §10 |
| `traceability` | Branch (shared) | Required for §7 / §8 / §9 | (n/a) | — |

### Why This Is Global

PRD-only scope and "no fixed PRD template" are both constitutional principles. The Inquiry Contract is the operational form of "every decision is a human decision" — it does not hard-code the PRD structure, it lets the human configure it per requirement. The Main Trunk vs. Branch distinction lets us guarantee the PRD always has the 5 required sections, while every other artifact gets a deliberate "do you want this visible?" gate.
