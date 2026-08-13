---
name: project-background-goal
description: Turn raw requirement materials into a sourced, human-confirmed business background and goal baseline before journey or product design begins.
---

# Project Background And Goal

## Purpose And Boundary

Establish why the requirement exists, what happens today, what problem matters, who is involved, what outcome is expected, and which constraints or unknowns affect later work.

**Do not** design journeys, features, screens, fields, APIs, architecture, or implementation tasks. A supplied product solution is evidence to examine, not a substitute for understanding the business need.

## Inputs And Outputs

Inputs: registered source materials (meeting minutes, emails, BRDs, PPTs, images) and identifiable business fact/goal owners. Output: `background-goal.md` using the template resolved by `src/templates/resolver.py background-goal.md`.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses) before analysis. Load `references/output-contract.md` before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <artifact> --json` before review. Load `references/elicitation-techniques.md` when source materials are sparse (访谈/观察主动采集).

## Thinking Prompts (per stage)

### 1. Preflight
- "What sources do I have? Who owns the business facts? What's the information density?"
- Register every source with an SRC-ID. Identify business_fact_owner and goal_decision_owner.
- **If no usable source or fact owner exists**, return a routing receipt and STOP — do not proceed to Intake.
- Assess maturity: L0 (no source) → L1 (single sparse source) → L2 (business solution exists) → L3 (well-specified) → L4 (confirmed upstream).

### 2. Intake
- "What does each source actually say — not what I think it means?"
- Extract source statements verbatim before interpreting. Classify each as `FACT`, `DECISION`, `ASSUMPTION`, `AI_INFERENCE`, `UNKNOWN`, or `CONFLICT` per `src/framework/contracts.md`.
- Retain source IDs and locations. Do not merge different sources' claims into one statement.

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "What's the observable outcome we want to change? What assumptions are disguised as requirements?"
- **Systems Thinking**: "What upstream/downstream systems, roles, and data are affected?"
- **Role Perspective**: "For each identified role — what do they gain, lose, or need to change?"
- **Constraint Analysis**: "What are the hard constraints (legal, platform, brand, timeline)?"
- **Adversarial**: "Could the opposite of any claim be true? What evidence would disprove it?"
- **Reverse Validation**: "From the desired outcome backwards, what must be true?"

### 4. Clarify
- Attempt research for discoverable facts first (docs, public data, system logs).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when an answer can change the problem, goal, role, scope, cost, timing, or risk.
- Limit: ≤5 questions per session. Order by impact.
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）；送审前 dor_check 会硬检查收口与引用。

### 5. Generate
- Fill the template. Narrative gets sourced content; uncertain content goes in explicit registers (§6-§8).
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Completeness**: All sources represented? All roles identified? All constraints listed?
- **First-Principles**: Did I accidentally write a solution instead of a problem?
- **Source Fidelity**: Does each claim trace to a source statement?
- **Downstream Usability**: Can journey-and-stories pick this up without re-researching?
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Present: candidate summary, evidence summary (what sources support each claim), unknowns and their impact, required decisions, audit result, change summary.
**Only the business fact/goal owner may approve.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → update affected sections → re-run Audit → return to Human Gate.
- Later contradictions → re-enter this Skill from the beginning (not patched downstream).

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Accept "we need an app for X" as the problem statement | Ask "what observable outcome changes if we build this?" |
| List 20 goals without prioritization | Limit to 3-5 goals with measurable baselines and targets |
| Copy-paste BRD sections without classifying knowledge state | Tag every claim as FACT/DECISION/ASSUMPTION/etc. |
| Skip roles because "the BRD only mentions users" | Infer roles from workflow descriptions, tag as AI_INFERENCE |
| Write 3 pages of background for a 1-paragraph source | Scale output to input density |

## Example: Sufficient Input → Sufficient Output

**Input**: BRD with business context, current process, pain points, 5 goals, 4 roles, constraints.
**Output**: Full template with sourced narrative + explicit registers.

## Example: Sparse Input → Degraded Output

**Input**: Slack message "we need an event invitation system for VIP customers."
**Output**: Intake registers the source → Preflight returns L1 → Think identifies missing: who are the roles? what's the current process? what's the success metric? → Clarify generates 3 questions → stops at `needs_user_input`.

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/elicitation-techniques.md` | 需求采集技法（访谈/观察，材料稀疏时用） | 材料稀疏时 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |

## Completion

All requirement-bearing sources are represented or excluded with a reason; background, current state, problem, goal, and solution are distinct; material claims are traceable; blocking unknowns prevent confirmation; and an authorized human approves the baseline.
