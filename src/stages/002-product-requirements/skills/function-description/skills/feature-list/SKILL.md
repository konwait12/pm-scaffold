---
name: feature-list
description: 功能清单——从已确认的用户故事（ST-XXX）分解出功能清单（FEA-XXX），每个功能可追溯、边界清晰不重叠、带 P0/P1 优先级。function-description 编排的第一个子 skill。
---

# Feature List · 功能清单

## Purpose And Boundary

把已确认的用户故事（ST-XXX）分解为产品必须交付的完整功能清单（FEA-XXX）——这是下游所有 function-description 子 skill 消费的唯一功能总账。每个 FEA-XXX 必须追溯 ≥1 个已确认的 ST-XXX，必须有清晰、互不重叠的功能边界，必须标注 P0/P1 优先级。

**Do not** 设计 UX 流程（→ `product-ux`/`ux-flow`）、交互规则（→ `product-ux`/`interaction-rules`）、页面骨架或原型（→ `product-ux`/`page-design`）、领域业务规则（→ `business-rules`）、字段校验（→ `validation-rules`）、状态机（→ `state-machine`）、异常与失败处理（→ `exception-handling`）、验收依据（→ `acceptance-criteria`）。功能清单只命名「做什么（WHAT）」；行为细节由其他子 skill 定义。

## Inputs And Outputs

**Input**: 已确认的 `user-journey-and-stories` 故事（ST-XXX）与范围基线，以及影响范围的已确认 `project-background-goal` 事实与目标。**Output**: 父产物 `function-description.md` 的 §功能清单 章节（registry `output_section`: 功能清单），模板由 `src/templates/resolver.py function-description.md` 解析。

分析前加载 `references/thinking-framework.md`（引用 `src/framework/thinking-core.md` §1 必用透镜 + §2 检查透镜）。草拟前加载 `references/output-contract.md`。送审前加载 `references/audit-checklist.md` 与 `references/reviewer-checklist.md`。评审前运行 `scripts/validate_artifact.py <父产物> --json`。

## Thinking Prompts (per stage)

### 1. Preflight
- "Are all upstream stories confirmed? What's the scope baseline (in/out)?"
- 枚举已确认的 ST-XXX、角色与生命周期阶段；发现缺失归属或矛盾故事时，先标 `CONFLICT` 再写任何 FEA。
- **If no confirmed story exists**, return a routing receipt and STOP — do not proceed to Intake.

### 2. Intake
- "What does each confirmed story actually require the system to do — not what I think it means?"
- 把每个已确认故事映射到 ≥1 个 FEA；有故事无功能 → 覆盖缺口，有功能无故事 → 范围越权。
- 每个候选都保留 `ST-XXX` 链接；不静默合并不同故事的诉求为一个功能。

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "What observable outcome must the feature enable? Which features are disguised assumptions?"
- **Systems Thinking**: "Which features depend on each other? What data or upstream capability does each feature need?"
- **Role Perspective**: "For each role — which features serve them, and what do they lose if a feature is cut?"
- **Constraint Analysis**: "What hard constraints (scope, legal, platform, timeline) bound the feature set?"
- **Adversarial**: "Could two features overlap so a user is confused about where to go? Which feature is actually redundant?"
- **Reverse Validation**: "From the confirmed stories backwards, what features must exist for every story to be satisfiable?"

### 4. Clarify
- Research discoverable facts first (existing product specs, competitor screens, public data).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when a feature boundary or scope decision changes what must be built.
- Limit: ≤5 questions per session. Order by impact.
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）；送审前 dor_check 会硬检查收口与引用。

### 5. Generate
- 填 §功能清单 表。一行一个功能，强制列：ID / 功能名称 / 所属故事 ST / 优先级 / 一句话描述 / 来源。
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.

### 6. Audit
- **Traceability**: 每个 FEA-XXX 链接 ≥1 个 ST-XXX；反向检查每个 P0 ST-XXX 有 ≥1 个 FEA。
- **Non-overlap**: 没有两个 FEA 目的相同或边界含糊；每项动作只能归属一个功能。
- **Priority**: 每个 FEA 有 P0/P1/P2 及理由；P0 = 缺它就无法满足某个已确认故事。
- **Consumability**: 每个 FEA 的一句话描述足以让 `functional-flow` / `business-rules` 直接消费，无需回头重研故事。
- Run `scripts/validate_artifact.py <父产物> --json`. Fix all errors. Warnings → document in audit notes.
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Present candidate §功能清单, evidence summary (which story supports each feature), unknowns and their impact, required decisions, audit result, change summary.
**Only the product owner / business owner may approve.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → update affected FEA rows → re-run Audit → return to Human Gate.
- Story/scope contradictions discovered later → re-enter this Skill from the beginning (not patched downstream).

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| 一个故事拆成 5 个无新增信息量的微功能 | 一个 FEA 对应一个内聚能力；粒度与故事匹配 |
| 写 "FEA-002: 客户管理" 无边界 | 写 "FEA-002: 客户名单导入" 并明示 in/out |
| 无 ST 链接凭空造功能 | 每个 FEA 追溯 ≥1 个已确认故事 |
| 功能互相重叠（活动创建 vs 活动编辑 vs 活动发布混在一起） | 画清边界，重叠则合并或拆分至互斥 |
| 全部标 P0 | 用 MoSCoW：P0 = 缺它旅程无法完成 |
| 把 UX 文案、页面布局抄进清单 | 清单只写 WHAT；UX/IX/页面属于 product-ux |
| 为 1 行故事写 5 页描述 | 产出密度与输入密度匹配，稀疏时降级 |

## Example: Sufficient Input → Sufficient Output

**Input**: confirmed `user-journey-and-stories`，ST-001..ST-006（客户邀约活动：名单导入、活动创建、邀约发放、客户接受/拒绝、二次催办、效果看板）。
**Output**: §功能清单 FEA-001..FEA-006 —— 每项追溯 ST-XXX、P0/P1 优先级带理由、边界互不重叠、来源可查。

## Example: Sparse Input → Degraded Output

**Input**: confirmed 一行 "给 VIP 客户发邀请"，无名单来源、无活动配置、无响应流程。
**Output**: Preflight 判定 L1 → Intake 登记单一候选为 `UNKNOWN` → Think 识别缺失：名单从哪来? 邀约如何发放? 客户如何响应? → Clarify 生成 3 个问题 → 停在 `needs_user_input`。不为凑表格而编造 FEA。

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |

## Completion

Every confirmed story is represented by ≥1 FEA-XXX; every FEA traces to ≥1 confirmed ST-XXX; feature boundaries are clear and non-overlapping; P0/P1 priorities are stated with rationale; no UX/rule content leaks in; feature density matches input density; blocking unknowns prevent confirmation; and an authorized product/business owner approves the §功能清单 baseline.
