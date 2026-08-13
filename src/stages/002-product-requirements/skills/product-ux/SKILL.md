---
name: product-ux
description: Define product scope, UX flows, interaction rules, and page skeletons from confirmed journey and stories. Separate WHAT (UX/IX) from HOW (BR/VL/AC owned by function-description).
---

# Product UX

## Purpose And Boundary

Translate confirmed business needs into product scope (FEA), functional structure, UX flows (Mermaid), interaction rules (IX), and page skeletons — at a level business can review and function-description can use without re-interpreting.

This Skill owns the **Scope → Structural → Framework** three-layer model. Interaction rules (IX) belong here (§3.3, produced by interaction-rules sub-skill). Business rules (BR), validations (VL), and acceptance criteria (AC) belong to function-description — **do not leak them here**.

**Do not**: design visual UI (colors/fonts), write business rules, define acceptance criteria, invent features not traced to confirmed stories, or use prototype as substitute for written rules.

## Three-Layer Model

```
Scope (§2)      → FEA-XXX: WHAT features exist, in/out boundaries, priorities
Structural (§3)  → IX-XXX + Mermaid flows: HOW users interact, what the system does
Framework (§4)   → Page skeletons: WHERE content lives, entry→content→actions→next-state
```

This mirrors how senior PMs sequence product definition: scope first, then rules, then page layout.

## PM-Specific Deliverables

- **Feature-to-story mapping**: every FEA traces to ≥1 confirmed ST → no orphan features
- **Priority framework**: P0 (core value, no workaround) / P1 (important, workaround exists) / P2 (nice to have)
- **IX rules**: trigger → system response, covering normal + error + empty + loading + edge states
- **Page skeletons**: entry trigger + preconditions + content areas + available actions + next-state — not visual design
- **Prototype as communication aid**: clickable HTML can accompany the spec but never replaces written rules

## Inputs And Outputs

**Input**: confirmed `user-journey-and-stories` (stories, scope baseline, roles, lifecycle).
**Output**: single `product-ux.md` with feature list (FEA), functional structure, Mermaid flows, IX rules (§3.3), page skeletons (§4).

Load `references/thinking-framework.md` (→ `thinking-core.md` §1 mandatory) before analysis.

## Thinking Prompts (per stage)

### 1. Preflight
- "Are all stories confirmed? What's the scope baseline (in/out)?"
- Verify upstream. Extract: confirmed stories (ST-XXX), scope baseline, roles, lifecycle stages, open non-blockers.
- Flag if scope baseline is missing → return upstream.

### 2. Intake
- "Which stories become features? Which are out of scope?"
- Map each confirmed story to ≥1 feature (FEA-XXX). Stories without features → gap. Features without stories → overreach.
- Classify each FEA: P0 (MVP must-have) / P1 (should-have) / P2 (could-have).
- Priority rationale: why is this P0/P1/P2? (MoSCoW: Is there a workaround? How many users affected? What's the business impact of deferring?)

### 3. Think

**Phase A — Scope (FEA definition)**
- "What are the system boundaries? What does each feature include and explicitly exclude?"
- Define in/out for each FEA. No feature should be a black box.

**Phase B — Structural (IX + flows)**
For each P0 FEA, design:
- Main flow: happy-day path from entry to success
- Alternate flows: different valid routes
- Error states: what the user sees on failure
- Empty states: what shows when there's no data
- Loading states: what shows while waiting
- Edge cases: boundary conditions

**Phase C — Framework (pages)**
- "What pages exist? What can the user do on each? What happens next?"
- Page skeleton: entry → preconditions → content → actions → next-state. Not visual design.

### 4. Clarify
- Batch questions about: feature boundaries, interaction behavior, state transitions visible to users.
- Do not ask about business rules (belongs to function-description).
- Trigger `competitive-research` if feature design lacks reference.
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）；送审前 dor_check 会硬检查收口与引用。

### 5. Generate
Fill template in 3 ordered phases (A→B→C):
- A: §2 FEA list + functional structure + in/out boundaries
- B: §3 Mermaid flows + IX rules (delegate to ux-flow + interaction-rules sub-skills)
- C: §4 page skeletons (delegate to page-design sub-skill)

Prototype (HTML) can accompany the spec as communication aid, but written rules remain authoritative. If generating prototype, reference `skills/pm-scaffold/` toolkit integration manifest for prototype skill pipeline.

### 6. Audit
- **FEA↔ST coverage**: every P0 story has ≥1 FEA; every FEA traces to ≥1 ST.
- **IX density**: ≥3 IX rules when P0 FEA exist (validator will warn if under-specified).
- **State completeness**: every page accounts for normal + error + empty + loading + edge.
- **No BR/VL/AC leakage**: scan for business-rule keywords (format/regex/formula/permission/only-admin-can).
- Run validator. Fix all errors.
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Present: feature list (FEA) with priority rationale, Mermaid flows, IX rules, page skeletons, coverage gaps.
**Product owner confirms** scope and behavior. Business owner confirms alignment with scope baseline.

### 8. Commit / Reflow
After approval → confirmed baseline. Hand off: FEA list, IX rules, page skeletons, flows, open non-blockers to `function-description`.
Scope changes → return to user-journey-and-stories. Feature changes → re-enter this Skill.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Define BR ("field must be ≤30 chars") in UX spec | Route BR to function-description; UX only defines IX |
| Skip error/empty/loading states ("the developer will figure it out") | Define every state — these are where PMs add the most value |
| Prioritize everything as P0 | Use MoSCoW: P0 = journey cannot complete without it |
| Use prototype as the spec | Written IX + page skeletons are authoritative; prototype is communication aid |
| Design pages as visual layouts | Page skeleton = entry/preconditions/content/actions/next-state — not pixel positions |

## Example: Well-Formed Interaction Rule

```markdown
| IX-011 | I11 | 用户点场次选择器 | 进入日期+时间选择页；默认选中最近可用日期；名额满的置灰 | 无可用场次→提示"所有场次已满" | BRD I11 |
```

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式 | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约 (IX 属于 §3.3) | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板 | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单 | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则 | Intake 时 |
| `references/thinking-framework.md` | 思考透镜 (Common Core + 领域 lens) | 每次任务开始 |

## Completion

All confirmed stories are represented by ≥1 FEA with explicit P0/P1/P2 rationale; every P0 FEA has Mermaid flow + ≥3 IX rules + error/empty/loading/edge states; page skeletons cover all interaction touchpoints; no BR/VL/AC leakage; prototype (if generated) is communication aid not substitute for rules; and authorized humans approve the baseline.
