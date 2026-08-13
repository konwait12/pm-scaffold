# Product UX Output Contract

Single artifact: **one `product-ux.md` containing four sections**. The `product-ux` main skill produces §功能清单 itself (no sub-skill); the other three sections are produced by its sub-skills, which write directly into the same `product-ux.md` — each sub-skill is a section producer, not a separate artifact.

## One Artifact, Four Sections

| 章节 | 内容 | 产出方 | 在 product-ux.md 中的落位 |
|---|---|---|---|
| §功能清单 | FEA-XXX 功能清单（名称、目的、所属模块、来源 ST-XXX、优先级、知识状态）+ 功能结构与 in/out 边界 | **product-ux 主 skill 自身产出（无子 skill）** | §2 功能结构（含 §2.2 功能清单） |
| §UX 流程 | 每个 P0 FEA 的 Mermaid 主流程 + 分支与状态（正常/备选/失败/空/加载/边界） | `ux-flow` 子 skill | §3.1 主流程 + §3.2 分支与状态 |
| §交互规则 | IX-XXX 交互规则：触发条件 → 系统响应（正常/错误/空/加载/边界） | `interaction-rules` 子 skill | §3.3 交互规则 |
| §页面设计 | 页面/步骤骨架：入口、前置条件、主要内容、操作、下一状态（非视觉设计） | `page-design` 子 skill | §4 页面与原型（§4.1 页面与步骤描述 + §4.2 HTML 原型） |

## 各章节契约

### §功能清单（由 product-ux 主 skill 自产，无子 skill）
- Every `FEA-XXX` includes name, purpose, module, source `ST-XXX`, priority, and knowledge state.
- Scope baseline with in/out boundaries; every feature traces to ≥1 confirmed `ST-XXX` — no orphan features.

### §UX 流程（由 `ux-flow` 子 skill 产出）
- Every P0 flow includes entry, steps/pages, decisions, main/alternate/failure paths, error/empty/loading variants, and resulting states.

### §交互规则（由 `interaction-rules` 子 skill 产出）
- `IX-XXX` rules: trigger → system response, covering normal + error + empty + loading + edge states.
- Belong to product-ux §3.3 (Structural layer).

### §页面设计（由 `page-design` 子 skill 产出）
- Page/step skeleton rows: entry trigger, preconditions, content areas, available actions, next state.

## 产出顺序与所有权

- 顺序：主 skill 先自产 §功能清单（Phase A）→ 委托 `ux-flow` 产 §UX 流程（Phase B-1）→ 委托 `interaction-rules` 产 §交互规则（Phase B-2）→ 委托 `page-design` 产 §页面设计（Phase C）。
- 三个子 skill 只写同一份 `product-ux.md` 的对应章节，各自不产独立产物。
- This artifact must not define `BR-XXX`, `VL-XXX`, or `AC-XXX` — those belong to `function-description`.

## Required Sections (validator checked)

Required sections: input assessment, scope baseline (FEA-XXX), UX flows (Mermaid), interaction rules (IX-XXX, §3.3), page/step/state descriptions (§4 Framework layer), knowledge registers, questions, sources, downstream handoff, audit compliance, and change summary.
