---
name: product-ux
description: Define page skeletons and interaction rules (IX) from confirmed journey and stories. Pure UX — page design (§页面设计) + interaction rules (§交互规则). Feature lists and functional flows belong to function-description.
---

# Product UX

## Purpose And Boundary

Translate confirmed journey and stories into page skeletons (WHERE content lives) and interaction rules (IX, HOW users interact) — at a level business can review and function-description can use without re-interpreting.

This Skill owns the **UX layer** only: page skeletons (§页面设计, produced by `page-design`) and interaction rules (§交互规则, produced by `interaction-rules`). **Do not do 功能清单 (feature lists) or 功能流程 (functional flows)** — those belong to `function-description`. Business rules (BR), validations (VL), and acceptance criteria (AC) also belong to function-description — **do not leak them here**.

**Do not**: design visual UI (colors/fonts), write business rules, define acceptance criteria, produce feature lists or functional flows, invent pages not traced to confirmed stories, or use prototype as substitute for written rules.

## UX Layer Model

```
页面设计 (§页面设计)  → Page skeletons: WHERE content lives, entry→content→actions→next-state
交互规则 (§交互规则)  → IX-XXX: HOW users interact, trigger → system response (normal/error/empty/loading/edge)
```

This mirrors how senior PMs sequence UX definition: pages first (structure/layout of content), then the interaction rules that govern each page.

## PM-Specific Deliverables

- **Page skeletons**: entry trigger + preconditions + content areas + available actions + next-state — not visual design
- **IX rules**: trigger → system response, covering normal + error + empty + loading + edge states
- **Story traceability**: every page and rule traces to ≥1 confirmed ST → no orphan pages/rules
- **Prototype as communication aid**: clickable HTML can accompany the spec but never replaces written rules

## Inputs And Outputs

**Input**: confirmed `user-journey-and-stories` (stories, scope baseline, roles, lifecycle).
**Output**: single `product-ux.md` with **two sections** — §页面设计 (page skeletons, `page-design` sub-skill), §交互规则 (IX rules, `interaction-rules` sub-skill).

Load `references/thinking-framework.md` (→ `thinking-core.md` §1 mandatory) before analysis.

## Thinking Prompts (per stage)

### 1. Preflight
- "Are all stories confirmed? What's the scope baseline (in/out)?"
- Verify upstream. Extract: confirmed stories (ST-XXX), scope baseline, roles, lifecycle stages, open non-blockers.
- Flag if scope baseline is missing → return upstream.

### 2. Intake
- "Which pages do the confirmed stories imply? Which interactive elements need rules?"
- Derive candidate pages from confirmed stories. Stories without pages → gap. Pages without story trace → overreach.

### 3. Think

**Phase A — 页面设计 (page skeletons)**
- "What pages exist? What can the user do on each? What happens next?"
- Page skeleton: entry → preconditions → content → actions → next-state. Not visual design.

**Phase B — 交互规则 (IX)**
For each page's interactive elements, design:
- Normal: happy-day trigger → response
- Alternate flows: different valid routes
- Error states: what the user sees on failure
- Empty states: what shows when there's no data
- Loading states: what shows while waiting
- Edge cases: boundary conditions

### 4. Clarify
- Batch questions about: page boundaries, interaction behavior, state transitions visible to users.
- Do not ask about business rules (belongs to function-description).
- Trigger `competitive-research` if page/interaction design lacks reference.
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）；送审前 dor_check 会硬检查收口与引用。

### 5. Generate
Fill template in 2 ordered phases (A→B). One artifact `product-ux.md` with two sections, both delegated to sub-skills, which write their section into the same file:
- §页面设计 —— 委托 `page-design` 子 skill 产出（页面骨架：入口/前置条件/内容/操作/下一状态）
- §交互规则 —— 委托 `interaction-rules` 子 skill 产出（IX-XXX 规则表）

功能清单（feature-list）与功能流程（functional-flow）不在此产出，归 `function-description`。

Prototype (HTML) can accompany the spec as communication aid, but written rules remain authoritative. If generating prototype, reference `skills/pm-scaffold/` toolkit integration manifest for prototype skill pipeline.

### 6. Audit
- **IX density**: ≥3 IX rules when interactive elements exist (validator will warn if under-specified).
- **State completeness**: every page accounts for normal + error + empty + loading + edge.
- **Story traceability**: every page and rule traces to ≥1 confirmed ST.
- **No BR/VL/AC leakage**: scan for business-rule keywords (format/regex/formula/permission/only-admin-can).
- **No feature-list/flow leakage**: 功能清单与功能流程归 function-description，不在 product-ux 产出。
- Run validator. Fix all errors.
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Present: page skeletons, IX rules, coverage gaps.
**Product owner confirms** scope and interaction behavior. Business owner confirms alignment with scope baseline.

### 8. Commit / Reflow
After approval → confirmed baseline. Hand off: page skeletons, IX rules, open non-blockers to `function-description`.
Scope changes → return to user-journey-and-stories. Page/rule changes → re-enter this Skill.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Produce 功能清单/功能流程 in product-ux | Route them to function-description; UX only covers pages + IX rules |
| Define BR ("field must be ≤30 chars") in UX spec | Route BR to function-description; UX only defines IX |
| Skip error/empty/loading states ("the developer will figure it out") | Define every state — these are where PMs add the most value |
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
| `references/output-contract.md` | 产物结构与 ID 契约（一个产物 2 章节：§页面设计→`page-design`，§交互规则→`interaction-rules`） | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板 | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单 | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则 | Intake 时 |
| `references/thinking-framework.md` | 思考透镜 (Common Core + 领域 lens) | 每次任务开始 |

## Completion

All confirmed stories are represented by ≥1 page skeleton and IX rules covering every interactive element; every P0 page has ≥3 IX rules + error/empty/loading/edge states; page skeletons cover all interaction touchpoints; no feature-list/flow/BR/VL/AC leakage; prototype (if generated) is communication aid not substitute for rules; and authorized humans approve the baseline.
