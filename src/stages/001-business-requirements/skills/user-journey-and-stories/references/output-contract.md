# Output Contract · user-journey-and-stories

Defines the structure, field semantics, and state transitions of the artifact produced by this Skill. All AI implementations must conform to this contract.

## Status Machine

Same 6 states as the project-background-goal Skill:

| State | Meaning | Who Sets |
|---|---|---|
| `draft` | AI is still working; not ready for review | AI |
| `needs_user_input` | Blocked on human answer; cannot proceed | AI |
| `conditional_review` | Ready for review with non-blocking caveats | AI |
| `ready_for_human_review` | AI work complete; awaiting human confirmation | AI |
| `confirmed` | Human explicitly approved | Human only |
| `superseded` | Replaced by a newer confirmed version | Human or AI |

Valid transitions:
- `draft` → `needs_user_input` | `conditional_review` | `ready_for_human_review`
- `needs_user_input` → `draft` | `conditional_review` | `ready_for_human_review`
- `conditional_review` → `needs_user_input` | `ready_for_human_review` | `draft`
- `ready_for_human_review` → `confirmed` | `draft` | `superseded`
- `confirmed` → `superseded`
- `superseded` → (terminal)

## Knowledge State Tags

| Tag | Meaning |
|---|---|
| `FACT` | Verifiable statement with source evidence |
| `DECISION` | Human-made choice recorded as such |
| `ASSUMPTION` | Working hypothesis, not yet confirmed |
| `AI_INFERENCE` | AI-derived from evidence, needs human check |
| `UNKNOWN` | Genuinely unknown; requires investigation |
| `CONFLICT` | Two or more sources disagree |

## Artifact Sections

1. **预检输入充分度判定** (§0): Upstream artifact verification + mode classification
2. **业务生命周期分解** (§1): Business lifecycle stages × roles
3. **用户旅程图** (§2): Journey map by stage (row) × role (column)
4. **用户故事卡片** (§3): Derived story cards with canonical format + role-grouped listing
5. **旅程→故事覆盖矩阵** (§4): Traceability from journey entries to story cards
6. **路径类型覆盖检查** (§5): Coverage of normal/alt/exception/failure/handoff/recovery
7. **事实与决定** (§6): FACT/DECISION register
8. **假设、AI 推断、未知与冲突** (§7): ASSUMPTION/AI_INFERENCE/UNKNOWN/CONFLICT register
9. **待确认问题** (§8): Pending questions with conclusions
10. **Clarifications**: Session log (see Clarifications Session Contract)
11. **来源追溯** (§9): Source traceability
12. **下游输入摘要** (§10): Handoff summary for product-ux
13. **Constitution Compliance** (§11): 4-principle compliance check
14. **版本变更摘要** (§12): Version history

## Story Card Format (Canonical)

```
在〈前提/场景〉下，作为〈角色〉，我希望〈动作〉，以便〈目标/价值〉
```

Fields:
- `前提/场景`: The situation or context in which the need arises
- `角色`: The specific role (from confirmed background §6)
- `动作`: What the role wants to do
- `目标/价值`: Why they want to do it — the outcome or value

## Journey Entry Format

Each (stage × role) cell must contain:
- `触发` (trigger): What event initiates this stage for this role
- `动作` (actions): What the role does
- `触点` (touchpoints): Where the interaction happens
- `痛点` (pain points): Known problems from background §4
- `期望` (expected outcome): What success looks like
- `类型` (path type): normal / alternative / exception / failure / handoff / recovery
- `来源` (source): SRC-* reference from upstream background
- `知识状态` (knowledge state): FACT / DECISION / ASSUMPTION / AI_INFERENCE / UNKNOWN / CONFLICT

## Clarifications Session Contract

Same format as project-background-goal:

| Field | Required | Description |
|---|---|---|
| `session_id` | Yes | CL-XXX, sequential |
| `category` | Yes | scope / roles / lifecycle / coverage / priority |
| `question` | Yes | The single question asked |
| `ai_preliminary_judgment` | Yes | AI's best guess before human answer |
| `options` | Yes | A/B/C choices when applicable |
| `decision_owner` | Yes | Who must answer |
| `blocking` | Yes | yes/no — does this block confirmation? |
| `deferral_risk` | Yes | What happens if deferred |
| `accepted_answer` | No | Filled after human answers |
| `reflow_target` | Yes | Which section receives the answer |
| `integrated_at` | No | ISO timestamp |
| `integrated_by` | No | AI / 人工 |
| `audit_recheck` | No | pass / fail |

Maximum 5 sessions per Skill invocation. If more are needed, set `needs_user_input`.

## Coverage Requirements

The journey + story set together must cover:

1. **All confirmed roles** from the upstream background
2. **All lifecycle stages** implied by the business domain
3. **Six path types** where applicable: normal, alternative, exception, failure, handoff, recovery
4. **No unexplained gaps** in the journey → story coverage matrix
