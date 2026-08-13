---
name: user-journey-and-stories
description: Build a lifecycle-by-role user journey with emotional mapping, derive traceable user story cards, and establish scope baseline from a confirmed background and goal baseline.
---

# User Journey And Stories

## Purpose And Boundary

Explain how the business event develops across roles — capturing not just actions but emotions, pain points, and opportunities at each touchpoint. Turn selected journey needs into user stories with clear priorities (MoSCoW). Produce a scope baseline that product-ux can use directly.

**Do not**: organize the journey by pages, design UX/UI, define functions or rules (BR/VL/AC), or confirm brainstormed candidates without business selection.

## PM-Specific Deliverables

This is the most authentically PM deliverable in Stage 1. It produces:
- **Lifecycle-by-role journey** — not page-based, not feature-based. Shows HOW the business event flows across people and systems.
- **Emotional mapping** — at each stage, what does each role feel? (frustrated, confused, confident, delighted) — this is what turns a functional spec into a human-centered product.
- **Pain points → Opportunities** — for every pain point, identify a concrete opportunity. This is the bridge from "current state is broken" to "here's what we can improve."
- **Story cards** — using the canonical Chinese format `在〈前提/场景〉下，作为〈角色〉，我希望〈动作〉，以便〈目标/价值〉`
- **Scope baseline** — explicit in/out decisions that downstream work items cannot silently expand.

## Persona Quick-Profiling

Before building the journey, create lightweight persona cards for each role identified in background-goal:

| Dimension | What to capture |
|---|---|
| Role name | e.g., FA (时尚顾问), 客人(主客), 客人(携伴) |
| Primary goal | What outcome do they need from this system? |
| Current pain | What's broken in their current workflow? |
| Context | When/where/how often do they interact? |
| Tech comfort | Novice / comfortable / expert (affects interaction complexity) |
| Decision power | Can they approve, or only suggest? |

## Inputs And Outputs

**Input**: confirmed `project-background-goal` (goals G1-G5, roles, constraints, sources).
**Output**: single `journey-and-stories.md` with lifecycle model, role matrix with personas, journey map (with emotions + pain points + opportunities), story cards (MoSCoW prioritized), journey-to-story coverage matrix, scope baseline.

Load `references/thinking-framework.md` (→ `thinking-core.md` §1 mandatory + §2 MECE scenario enumeration) before analysis.

## Thinking Prompts (per stage)

### 1. Preflight
- "Are all goals and roles confirmed? What lifecycle clues exist in the background?"
- Verify upstream confirmation. Extract goals (G1-G5), roles, lifecycle clues, constraints, sources.
- Return upstream if background is not confirmed.

### 2. Intake
- "What does each source say about how the business event unfolds across roles?"
- Separate confirmed role/scene facts from assumptions and unknowns.
- Register every lifecycle clue, stakeholder handoff, and emotional signal before expansion.
- Build lightweight persona cards for each role.

### 3. Think

**Phase A — Lifecycle First (业务生命周期)**
- "What's the business event lifecycle — independent of any product?"
- Stages must be named as business events, not product features. Example: "活动创建" not "后台表单页面"; "客人接收邀请" not "H5过渡页".

**Phase B — Role Matrix (角色矩阵)**
For each lifecycle stage × each role:
- Actor: who's doing the action?
- Observer: who needs to know?
- Approver: who decides?
- Collaborator: who helps?
- Support: what system/tool assists?

**Phase C — Emotional Mapping (情感旅程)** 🔑 NEW
- At each touchpoint, what is the role feeling? (😤 frustrated / 😰 anxious / 😐 neutral / 🙂 satisfied / 😍 delighted)
- What's the emotional arc across the entire journey? (Does it end better than it started?)
- Where's the lowest emotional point? → This is usually where the product needs to intervene most.

**Phase D — Pain Points → Opportunities**
- For every pain point: "What would make this better?" → concrete opportunity
- Opportunities are the raw material for user stories
- Tag AI-generated opportunities as `AI_INFERENCE`

**Phase E — Path Diversity (路径类型覆盖)**
Walk all 11 path types for each lifecycle stage where applicable: normal, alternative, exception, failure, timeout, permission-mismatch, handoff, cancellation, retry, rollback, recovery.

### 4. Clarify
- Create journey skeleton first. Batch questions that materially affect: role ownership, lifecycle boundaries, required events, business scope, candidate selection.
- Keep AI-added scenes as `AI_INFERENCE` until business owner selects them.
- Limit: ≤5 questions per session. Order by journey impact.
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）；送审前 dor_check 会硬检查收口与引用。

### 5. Generate

**Story Card Format** (canonical Chinese):
```
在〈前提/场景〉下，作为〈角色〉，我希望〈动作〉，以便〈目标/价值〉
```

**Prioritization** (MoSCoW):
- **P0 (Must have)**: Without this, the journey cannot complete. Core value delivery.
- **P1 (Should have)**: Important but workaround exists. Include if feasible.
- **P2 (Could have)**: Nice to have. Defer unless trivial.
- **P3 (Won't have this time)**: Explicitly excluded with reason.

Build the lifecycle-by-role journey with emotional annotations → derive story cards from selected entries → build coverage matrix → establish scope baseline.

A Mermaid view may accompany the authoritative matrix when useful, but no separate diagram gate is required.

### 6. Audit
- **Role coverage**: Every confirmed role appears in at least one journey stage.
- **Lifecycle coverage**: Every stage has at least one role acting.
- **Path diversity**: Normal + at least 2 other path types present.
- **Emotional completeness**: Every role has emotional annotations at key touchpoints.
- **Story-card quality**: Every story uses canonical format + MoSCoW priority + knowledge state.
- **Bidirectional links**: Every story references a journey entry; uncovered entries have a reason.
Run validator. Repair non-business defects.
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Present: journey map (with emotions + pain points), persona cards, story cards (with MoSCoW priorities), coverage gaps, unselected candidates (excluded evidence, not requirements).
**Only business owner may confirm** — journey boundaries, role ownership, priority decisions.

### 8. Commit / Reflow
After approval → confirmed baseline. Hand off: roles, selected stories, lifecycle structure, scope baseline, dependencies, open non-blockers to `product-ux`.
Later journey gaps → re-enter this Skill.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Organize journey by pages ("首页→详情页→提交页") | Organize by business lifecycle stages ("活动创建→邀请发送→客人接收") |
| Skip emotional mapping ("emotions are subjective") | Capture emotional states — they reveal where the product must intervene |
| Assign P0 to everything | Use MoSCoW: if everything is P0, nothing is |
| Write stories as "系统应支持X功能" | Use canonical format: 在〈场景〉下，作为〈角色〉，我希望〈动作〉，以便〈价值〉 |
| Confirm AI-generated journey entries without review | Mark as AI_INFERENCE until business owner selects |

## Example: Well-Formed Journey Entry

| 阶段 | FA (时尚顾问) | 客人 (主客) | 情感 (FA) | 情感 (客人) | 痛点 | 机会 |
|---|---|---|---|---|---|---|
| 4.活动预约 | — | 选择场次→确认信息→点"即刻预约"→二次确认→提交 | — | 😐→🙂 (选好场次) → 😰 (担心填错) → 😍 (预约成功) | 信息填写多，需授权手机号；网络异常时信息可能丢失 | 已注册用户自动填充；异常时信息保留+重试 |

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式 | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板 | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单 | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则 | Intake 时 |
| `references/thinking-framework.md` | 思考透镜 (Common Core + MECE scenario enumeration) | 每次任务开始 |

## Completion

All confirmed roles and lifecycle stages are represented; emotional mapping reveals where the product must intervene; pain points have corresponding opportunities; story cards use canonical format with MoSCoW priorities; bidirectional journey↔story links are complete; no candidate is silently confirmed; scope baseline is explicit; and an authorized human approves both required outputs.
