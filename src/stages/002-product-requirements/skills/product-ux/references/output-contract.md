# Product UX Output Contract

Single artifact: **one `product-ux.md` containing two sections**. Both sections are produced by the `product-ux` sub-skills, which write directly into the same `product-ux.md` — each sub-skill is a section producer, not a separate artifact.

## One Artifact, Two Sections

| 章节 | 内容 | 产出方 | 在 product-ux.md 中的落位 |
|---|---|---|---|
| §页面设计 | 页面/步骤骨架：入口、前置条件、主要内容、操作、下一状态（非视觉设计） | `page-design` 子 skill | §页面设计（页面与步骤描述 + HTML 原型入口） |
| §交互规则 | IX-XXX 交互规则：触发条件 → 系统响应（正常/错误/空/加载/边界） | `interaction-rules` 子 skill | §交互规则 |

功能清单（feature-list）与功能流程（functional-flow）不在此产物内 —— 归 `function-description`。

## 各章节契约

### §页面设计（由 `page-design` 子 skill 产出）
- Page/step skeleton rows: entry trigger, preconditions, content areas, available actions, next state.
- Not visual design; no pixel positions.

### §交互规则（由 `interaction-rules` 子 skill 产出）
- `IX-XXX` rules: trigger → system response, covering normal + error + empty + loading + edge states.
- Belong to product-ux §交互规则 (UX layer).

## 产出顺序与所有权

- 顺序：委托 `page-design` 产 §页面设计（Phase A）→ 委托 `interaction-rules` 产 §交互规则（Phase B）。
- 两个子 skill 只写同一份 `product-ux.md` 的对应章节，各自不产独立产物。
- This artifact must not define `BR-XXX`, `VL-XXX`, or `AC-XXX`, nor feature lists (feature-list) or functional flows (functional-flow) — those belong to `function-description`.

## Required Sections (validator checked)

Required sections: input assessment, scope baseline, page/step/state descriptions (§页面设计), interaction rules (IX-XXX, §交互规则), knowledge registers, questions, sources, downstream handoff, audit compliance, and change summary.
