# Output Contract（Brainstorming）

## Artifact Identity

- File: `99-review/support/brainstorming-output.md`
- Template: `src/templates/others/brainstorming-output.md`
- The record is a **support record**, not a stage artifact and not an independently confirmed baseline.

## Artifact States

| Status | Meaning | 何时可用 |
|---|---|---|
| `draft` | Initial candidate set; Audit not complete | 初始 |
| `needs_user_input` | A material answer would change the candidate set or disposition options | 有阻断性澄清问题 |
| `conditional_review` | Structurally reviewable with explicit non-blocking unknowns | 有非阻断未知 |
| `ready_for_human_review` | Self-audit passed; waiting for disposition by the responsible human | 送审 |
| `confirmed` | **NOT allowed for this record** | 永远不产 `confirmed` |

The brainstorming record never reaches `confirmed`: the human's `include` decision flows into the `project-background-goal` input package, and only `pipeline.py review --decision approve` may confirm the downstream work item itself.

## Candidate Table Contract（候选表 SCN-XXX）

Every distinct idea after clustering gets a stable ID `SCN-001`, `SCN-002`, …

| 列 | 内容 | 规则 |
|---|---|---|
| Candidate ID | `SCN-XXX` | 单调递增，去重后编号，不随排序变化 |
| 发散维度 | 12 维度之一（lifecycle / roles / normal-alternate-exception-failure-timeout / permission / data condition / handoff / dependency / cancellation / retry / rollback / change-recovery / constraint） | 主维度 |
| Candidate | 候选内容一句话 | 单一诉求，不塞多条 |
| Evidence | 为什么 AI 这么想 | 引用原始想法原文 / SRC-* / 常识推断；不得为空或占位 |
| Impact | 若纳入会产生什么影响 | 面向后续旅程/功能/范围的影响；不得为空或占位 |
| 知识状态 | `AI_INFERENCE` | 全表统一；未处置前不得升级为 FACT |

## Disposition Table Contract（处置表）

The disposition table has **8 columns** — this is the canonical shape agreed in `src/shared/brainstorming/rediscovery-templates/scenario-disposition.md`:

| Candidate ID | Role-Lifecycle | Candidate | Evidence | Impact | Human Disposition | Reason | Write-back Target |
|---|---|---|---|---|---|---|---|
| `SCN-001` | 维度/阶段 | 候选内容 | 依据 | 影响 | include / exclude / defer / research | 原因 | 写回目标 |

Rules:

- **Human Disposition** is one of exactly four values: `include` / `exclude` / `defer` / `research`. The AI fills everything else; only the responsible human fills this column.
- `include` → 候选进入正式产物；**必须**给出非占位的 Write-back Target（写回 `project-background-goal` 输入包的哪个段：§生命周期线索 / §角色候选 / §约束候选 …）。
- `exclude` → 排除；Reason 必须说明排除原因。
- `defer` → 暂缓；Reason 给出触发条件或计划周期。
- `research` → 待调研；登记 issue-record / QuestionRecord，不静默搁置。

## Knowledge-State Labels

| Label | Definition |
|---|---|
| `AI_INFERENCE` | AI-derived interpretation supported by evidence but not a business fact（发散候选唯一允许的标注） |
| `FACT` | Explicit source statement（仅在有 SRC-* 材料时可出现） |
| `UNKNOWN` | Missing information |
| `CONFLICT` | Incompatible source statements require resolution |

## Write-back Contract

- Only `include` candidates are written back, and **only** into the `project-background-goal` input package（综合为 ≥ 50 字的充分输入）。
- The write-back bundle must be plain requirement input (what to explore), not a designed solution.
- After write-back, the work item resumes at `project-background-goal` (registry `resume_work_item`).

## Human Responsibilities

- Business owner: disposes every candidate (`include` / `exclude` / `defer` / `research`), confirms write-back targets.
- Product manager: checks divergence coverage, evidence quality, and downstream usability of the input package.

## Clarifications Session Contract

Each Clarify session follows the same contract as `project-background-goal`（`CL-NNN` 单调编号；AI 初判 + 选项 + 影响 + owner + blocking；≤5 问题/轮；`accepted_answer` 在 `ready_for_human_review` 前必须填写；答案回写进候选表/处置表对应行）。未知答案成为普通 QuestionRecord / issue-record 条目，不额外开分支。

## Downstream Handoff

Emit a compact handoff containing:

```text
trigger_signal            # L0 / 材料稀疏
divergence_coverage       # 12 维度扫描摘要
candidate_ids             # SCN-* 全集
included_candidates       # 仅 include 项
deferred_candidates       # defer 项 + 触发条件
research_items            # research 项 + issue-record 引用
input_package             # ≥50 字综合输入（交付 project-background-goal）
source_ids                # 若有材料
```
