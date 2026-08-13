---
name: brainstorming
description: Diverge, cluster and converge sparse ideas (L0 idea only or thin materials) into an AI_INFERENCE candidate set, get human include/exclude/defer/research disposition, and write back only included candidates to the project-background-goal input package.
---

# Brainstorming（需求发散收敛）

## Purpose And Boundary

Triggered by the entry router at **L0（仅想法）** or when materials are too thin to enter the stage-1 baseline: the requirement exists only as a one-line idea, with roles, scenes, lifecycle, and alternatives undefined. This skill diverges candidates across 12 scenario dimensions (lifecycle, roles, normal/alternate/exception/failure/timeout, permission, data condition, handoff, dependency, cancellation, retry, rollback, change-recovery), clusters and deduplicates them, labels every candidate `AI_INFERENCE`, presents them to the responsible human for a four-value disposition (`include` / `exclude` / `defer` / `research`), and writes back **only included candidates** into the `project-background-goal` input package. It is an internal mode, not a stage and not an independently confirmed artifact.

**Do not** invent business facts, decide disposition on the human's behalf, present divergent candidates as requirement content before disposition, or let the record itself reach `confirmed`. A candidate survives only when the human marks it `include`.

## Inputs And Outputs

Inputs: L0 trigger signal from the entry router (`src/scripts/pipeline.py` entry stage), the raw one-line idea or thin materials, and an identifiable responsible human (business_owner) for disposition. Output: `brainstorming-output.md` using the template at `src/templates/others/brainstorming-output.md`, written to `99-review/support/`; the converged bundle is the input package for `project-background-goal` (resume work item).

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1+§2 mandatory lenses) before diverging. Load `references/source-handling.md` at Intake when materials exist. Load `references/question-patterns.md` at Clarify. Load `references/output-contract.md` before drafting. Load `references/anti-patterns.md` at Generate. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <artifact> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "Is this L0 (idea only) or thin material? What is the stuck point? What is the evidence boundary?"
- Confirm the trigger: L0 → brainstorming per the entry router; multi-source ambiguity → route to `requirement-restate` instead; well-supplied input → enter `project-background-goal` directly.
- State the question and the evidence boundary (what can and cannot be inferred). Identify the responsible human for disposition.
- **If the idea is empty or no responsible human is identifiable**, return a routing receipt and STOP at `needs_user_input`.

### 2. Intake
- Capture the raw idea verbatim — not what I think it means.
- If any material exists (message, email, meeting note), register it as SRC-* per `references/source-handling.md`.
- At pure L0 there is no source: record the raw idea text as the evidence basis, and be explicit that everything else is inference.

### 3. Think (apply thinking-core.md §1+§2 mandatory lenses + divergence lenses)
- **First Principles**: "剥离开所有提议做法，这个想法本身要改变什么可观察结果？"
- **Systems Thinking**: "这个想法涉及哪些上下游流程、角色和数据？"
- **Role Perspective**: "对每个可能角色——他们获得什么、失去什么、需要什么？"
- **Constraint Analysis**: "哪些硬约束（时间、预算、平台、合规）可能立刻生效？"
- **Adversarial**: "这个想法最不可能成立的地方在哪？什么证据能推翻它？"
- **Reverse Validation**: "从想要的结果倒推，什么必须先成立？"
- Divergence domain lenses: sweep the 12 dimensions — lifecycle, roles, normal/alternate/exception/failure/timeout, permission, data condition, handoff, dependency, cancellation, retry, rollback, change-recovery (see `references/thinking-framework.md`).
- Cluster and deduplicate overlapping candidates; each surviving distinct idea gets a stable ID `SCN-XXX`.

### 4. Clarify
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when an answer would change the candidate set or the disposition options materially.
- Limit: ≤5 questions per session. Order by impact.
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）并更新 §13 收口表；送审前 dor_check 会硬检查收口与引用。

### 5. Generate
- Fill the template: 候选清单（SCN-XXX，全部 `AI_INFERENCE`，每条含 Evidence 与 Impact）→ 人工处置表（8 列，Disposition 留给人工）→ Include 项写回 → 收敛后输入包。
- Status: use `draft`, `needs_user_input`, or `conditional_review` — the record itself **never** reaches `confirmed`.

### 6. Audit
- **Completeness**: all 12 dimensions swept or explicitly skipped? every candidate carries Evidence + Impact?
- **Inference Discipline**: every candidate labeled `AI_INFERENCE`; nothing presented as fact?
- **Disposition Readiness**: the disposition table is ready for human decision; each `include` candidate names a write-back target?
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.
- **B3 收口**：确认 issue-record 的 §13 收口表已更新本 skill 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Present: divergence coverage summary (which dimensions yielded what), candidate table with evidence and impact, recommended disposition for each candidate, deferral risks.
**Only the responsible human (business_owner) may dispose** each candidate: `include`（纳入正式产物）/ `exclude`（排除，给原因）/ `defer`（暂缓，给触发条件）/ `research`（待调研，登记 issue-record / QuestionRecord 跟进）。Approval of the write-back creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Write back **only `include` candidates** into the `project-background-goal` input package (综合为 ≥ 50 字的充分输入), then return to the current Work Item.
- If disposition is incomplete or a materially new idea arrives → re-enter this Skill from Preflight, do not patch downstream.
- Later contradiction in the written-back input → re-enter this Skill rather than silently revising the target artifact.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Turn the one-line idea into "facts" | Keep everything `AI_INFERENCE` until the human disposes it |
| Diverge in only one dimension (e.g. only roles) | Sweep all 12 dimensions (lifecycle/roles/normal-alternate-exception-failure-timeout/permission/data condition/handoff/dependency/cancellation/retry/rollback/change-recovery) |
| Ship 40 near-duplicate candidates | Cluster and deduplicate; one `SCN-XXX` per distinct idea |
| Decide include/exclude on the human's behalf | Present the disposition table; only the human marks include/exclude/defer/research |
| Let `include` candidates drift without a destination | Every include row names a write-back target in the input package |
| Treat `research` as closed | `research` becomes an issue-record entry / QuestionRecord and is followed up |
| Let the record ship as `confirmed` | The record maxes out at `ready_for_human_review`; only `pipeline.py review` may confirm the downstream work item |
| Write back excluded candidates too | Only `include` candidates enter the input package |

## Example: Sufficient Input → Sufficient Output

**Input**: L0 idea with a rich requestor — "客户邀约活动，名单约 500 人，预算 10 万，希望月底前上线"（无书面材料）。
**Output**: Full divergence across the 12 dimensions → cluster/dedupe to 5 candidates → candidate table with evidence + impact → disposition table fully marked (3 include / 1 defer / 1 research) → include write-back bundle ≥ 50 字 → `ready_for_human_review` → input package handed to `project-background-goal`.

## Example: Sparse Input → Degraded Output

**Input**: Slack message "想做客户邀约活动"（无更多信息）。
**Output**: Intake registers the message as the evidence basis → Preflight returns L0 → Think produces candidate skeletons with sparse evidence → Clarify generates 3 questions (活动目标 / 邀约对象范围 / 期望时间) → stops at `needs_user_input`; the disposition table stays partially filled until the human answers.

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（发散收敛特有，写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 SCN-XXX / 处置表契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（发散补全类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 处置用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（L0 无源与 SRC-* 登记） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 12 维度发散 lens + 稀疏降级，必读） | 每次任务开始（必读） |

## Completion

L0/稀疏触发确认且证据边界明确；12 维度全部扫过或显式跳过；候选已聚类去重并拥有稳定 `SCN-XXX` ID；每条候选带 Evidence、Impact 与 `AI_INFERENCE` 标注；处置表可供人工四值处置（或已处置）；仅 `include` 候选写回 `project-background-goal` 输入包（≥ 50 字）；issue-record §13 收口表已更新本 skill 行；人工完成 include/exclude/defer/research 处置且写回被授权。
