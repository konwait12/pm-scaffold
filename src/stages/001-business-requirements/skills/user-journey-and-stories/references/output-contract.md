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
11. **范围基线（In/Out/Deferred/Conditional 四分类）** (§10): In/Out/Deferred/Conditional 范围项 + 验收依据 + 来源追溯（见 Scope Baseline Section Format）
12. **来源追溯** (§11): Source traceability
13. **下游输入摘要** (§12): Handoff summary for product-ux
14. **Constitution Compliance** (§13): 4-principle compliance check
15. **版本变更摘要** (§14): Version history

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

## Scope Baseline Section Format（§范围基线 · In/Out/Deferred/Conditional 四分类）

The artifact must include a **范围基线** section — one of the three chapters of the `journey-and-stories.md` artifact（范围基线 / 旅程 / 故事）. It turns every stakeholder expectation or candidate into exactly **one of four categories**, each backed by a verifiable acceptance criterion, a knowledge-state label, and a source or decision:

| 子标题 | 含义 | 判定 |
|---|---|---|
| 范围总览 | In/Out/Deferred/Conditional 四分类计数 | 先给计数，再列明细 |
| In-Scope | **In · 本期做**（已确认纳入本期） | 必须有可验证验收依据，模糊项不得列入 |
| Out-of-Scope | **Out · 本期不做**（已确认排除 + 原因） | 原因 = 约束 / 决议 / 未来工作，不得静默丢弃 |
| Deferred | **Deferred · 延后**（暂缓做 + 触发/重开条件） | 记录触发条件；低成本高不确定项优先延后 |
| Conditional | **Conditional · 条件触发**（条件成立则纳入） | 如"预算通过则…"/"法务签字则…"，是真实范围，必须显式列出 |

若某类无已确认内容，写 `待确认` 并链接到 §8 待确认问题 或 §7 UNKNOWN ID，不得删除该子标题。

### Scope Item Schema（S-NNN）

Each scope item must have:

| Field | Required | Description |
|---|---|---|
| `S-NNN` (ID) | Yes | 本产物内单调递增 |
| `description` | Yes | 一句可测试的描述 |
| `knowledge_state` | Yes | FACT / DECISION / ASSUMPTION / AI_INFERENCE / UNKNOWN / CONFLICT |
| `source_or_decision` | Yes | SRC-* 或 DEC-*（可追溯） |
| `acceptance_criterion` | Yes (In) / Optional (Out/Deferred/Conditional) | 如何判定完成或排除 |
| `stakeholder` | Optional | 提出/负责该范围项的干系人 |
| `notes` | Optional | 边界情况、依赖 |

**Mutual Exclusivity**: 一项不得同时 In 且 Out，也不得同时 In 且 Deferred。争议边界必须显式路由到决策者（goal decision owner / business sponsor），AI 不得自行裁决。

**Downstream Handoff**: confirmed 后，范围基线随 `journey-and-stories.md` 交接 product-ux：`in_count / out_count / deferred_count / conditional_count` + 范围项清单（S-NNN）+ 开放非阻断未知。

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
