---
name: ux-flow
description: Map each P0 feature's end-to-end UX flow as Mermaid diagrams — entry points, sequential steps, decision branches, exit states, error/empty/loading variants — traceable to confirmed stories. Sub-skill of product-ux, fills §3.1/§3.2.
---

# UX Flow

## Purpose And Boundary

Produce the flow skeleton for every P0 `FEA-XXX`: how the user arrives, which screens/steps they traverse, where the path branches and under what condition, and where it ends — including error, empty, and loading variants. Every diagram must trace back to a confirmed story (`ST-XXX`) and a feature (`FEA-XXX`) so that `page-design` and `interaction-rules` can hang page and rule detail onto real steps.

**Do not** design page layouts, write interaction rules (`IX-*`), decide module/system boundaries, or define business rules (`BR`/`VL`/`AC`). A flow step may *reference* a handoff across a system boundary, but the boundary decision itself belongs upstream.

## Inputs And Outputs

Inputs: confirmed `user-journey-and-stories` artifact (stories `ST-XXX`, scope baseline, roles, lifecycle stages) and the parent product-ux §2 feature list (`FEA-XXX` with P0/P1/P2 priorities). Output: §3.1 主流程（P0）+ §3.2 分支与状态 of the parent `product-ux.md` — not a standalone artifact. Section layout follows `src/templates/stage-2-product/product-ux.md`.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses) before analysis. Load `references/output-contract.md` before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <product-ux.md> --json` before review. Load `references/question-patterns.md` when branches are ambiguous or states are missing.

## Thinking Prompts (per stage)

### 1. Preflight
- "Which FEA are P0? Which stories and lifecycle stages do they trace to? Is the scope baseline confirmed?"
- Verify upstream: every flow's FEA must exist in §2 and trace to ≥1 confirmed `ST-XXX`.
- **If the scope baseline or P0 list is missing**, return a routing receipt and STOP — do not invent features to draw.
- Assess density: L1 (one sentence, no flow material) → L2 (feature list exists) → L3 (stories + roles + lifecycle) → L4 (confirmed upstream).

### 2. Intake
- "What does each source actually say about how the user moves through the system — not what I imagine?"
- Collect entry points, steps, and exit states verbatim from confirmed stories and feature descriptions before structuring.
- Classify each flow claim as `FACT`, `DECISION`, `ASSUMPTION`, `AI_INFERENCE`, `UNKNOWN`, or `CONFLICT` per `src/framework/contracts.md`.
- A step I invented to make the diagram complete must be tagged `AI_INFERENCE`, never silently presented as confirmed.

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "What observable step does the user actually perform? Which flow steps are assumed but unstated?"
- **Systems Thinking**: "Does this path cross a system/module boundary, another role's touchpoint, or an external dependency?"
- **Adversarial**: "Could there be an alternate entry the diagram ignores? Would a user actually reach this branch?"
- **Reverse Validation**: "From the exit state backwards, what must be true at each step for the flow to complete?"
- **Confirmation Bias Defense**: "Am I only drawing the happy path the requester described, without testing failure routes?"
- **Knowledge Boundary**: "Which steps are confirmed facts and which are my structural inference?"

### 4. Clarify
- Attempt to resolve discoverable gaps first (review story text, role descriptions, lifecycle stages).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when the answer changes a P0 flow's entry, steps, branches, or exit.
- Limit: ≤5 questions per session. Order by impact. Do not ask about page layout or rules (downstream skills).
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）；送审前 dor_check 会硬检查收口与引用。

### 5. Generate
- Draw one Mermaid diagram per P0 FEA covering entry → steps → decisions → exit. Add error/empty/loading branches.
- Label every branch with a concrete condition. Reference `FEA-XXX` and `ST-XXX` in the diagram heading.
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Completeness**: every P0 FEA has ≥1 diagram; every diagram has ≥1 error/empty/loading branch.
- **Branch Soundness**: conditions are labeled, mutually exclusive, and exhaustive.
- **Traceability**: each step traces to a story/feature; no orphan steps.
- **Downstream Usability**: can page-design and interaction-rules enumerate pages from these steps?
- Run `scripts/validate_artifact.py <product-ux.md> --json`. Fix all errors. Warnings → document in audit notes.
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Present: per-FEA flow summary, the paths drawn, the states covered, branch conditions, and any steps tagged `AI_INFERENCE`.
**Product owner confirms flows; business owner confirms exits and cross-system handoffs.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → update affected diagrams → re-run Audit → return to Human Gate.
- A changed entry point or branch condition invalidates downstream page-design and interaction-rules → re-enter this Skill from the beginning, not patch downstream.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Draw only one happy path per FEA | Cover main + alternate + error/empty/loading paths |
| Leave branch arrows unlabeled | Label every branch with a concrete, testable condition |
| Compress "填写表单并提交" into one box | Split compound actions into real sequential steps |
| Skip empty/loading states ("dev will figure it out") | Draw every state — states are where PMs add the most value |
| Add pages/steps not present in confirmed stories | Every step traces to ST-XXX / FEA-XXX, else tag AI_INFERENCE |
| Mark cross-system handoff as a normal node | Annotate system boundary and the failure-rollback target |
| Write page layouts or IX/BR inside the diagram | Keep flows at step level; route layout/rules to downstream skills |

## Example: Sufficient Input → Sufficient Output

**Input**: confirmed stories + P0 FEA list (e.g., "场地预约" FEA-001 P0, "查询场地" ST-003), scope baseline with roles and lifecycle stages.
**Output**: one Mermaid diagram per P0 FEA — entry (首页→预约入口), steps (选日期→选时段→填信息→确认), branches (名额满→置灰+提示, 未登录→先登录再回跳), exit states (预约成功页 / 失败回退), each with ≥1 error/empty/loading variant and condition-labeled edges.

## Example: Sparse Input → Degraded Output

**Input**: a single Slack line "我们想让大家能在线上报名活动，流程还没想好。"
**Output**: Intake registers the source → Preflight returns L1 → Think lists missing material (入口? 步骤? 分支条件? 失败状态?) → Clarify generates ≤5 batched questions (each with AI preliminary judgment + options + owner) → stops at `needs_user_input`. No flow diagram is invented from a blank slate.

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（画流程时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | §3.1/§3.2 产出结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 上游追溯规则（ST-/FEA-/SRC- 引用） | Intake/追溯时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 流程领域 lens，必读） | 每次任务开始（必读） |

## Completion

All P0 FEA have Mermaid flow diagrams covering entry → steps → decisions → exit; every diagram includes at least one error/empty/loading state; every branch is condition-labeled; every step traces to a confirmed story/feature; flow steps stay at the structural layer without leaking layout, IX, or BR; the Mermaid syntax renders; and an authorized human approves the flows before downstream page-design starts.
