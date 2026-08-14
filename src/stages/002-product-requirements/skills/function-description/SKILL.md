---
name: function-description
description: Specify domain-level business rules, validation, permissions, state transitions, exceptions, and acceptance criteria for each confirmed feature. Interaction rules (IX) are owned by product-ux/interaction-rules — reference only.
---

# Function Description

## Purpose And Boundary

Define HOW every in-scope feature behaves — at a level business can understand, development can implement, and testing can verify. This Skill owns the feature inventory (FEA), functional flow, and domain rules (BR, VL, state, exceptions, AC). Interaction rules (IX) are owned by product-ux/interaction-rules — **reference them, do not redefine them**.

**Do not**: redesign UX, add untraceable features, write test cases, architecture, database schemas, or API contracts.

## Sub-Skills (execution order)

Each produces a section of the function-description artifact:
1. `feature-list` → §功能清单 (FEA table: confirmed in-scope feature inventory)
2. `functional-flow` → §功能流程 (per-FUN main/alternate/exception/failure paths)
3. `business-rules` → §业务规则 (BR table: domain constraints, calculations, policies)
4. `validation-rules` → §校验规则与字段定义 (VL table: field-level + cross-field checks, error messages + field definitions)
5. `state-machine` → §状态变化 (STATE table: states × events → target states)
6. `exception-handling` → §异常与失败处理 (EX table: failure modes + user-visible recovery)
7. `acceptance-criteria` → §验收依据 (AC table: Given/When/Then + quantified thresholds)

## Inputs And Outputs

**Input**: 上游功能清单 FEA（`feature-list` 子 skill 产出）+ confirmed `product-ux` (IX, pages) + confirmed business upstream (ST, scope baseline).
**Output**: 一个 `function-description.md`，由 7 个子 skill 依次产出 7 个章节：§功能清单 / §功能流程 / §业务规则 / §校验规则与字段定义 / §状态变化 / §异常与失败处理 / §验收依据。字段规则和埋点章节按需出现。

Load `references/thinking-framework.md` (→ `thinking-core.md` §1 mandatory + §2 check lenses) before analysis. Load `references/ears-syntax.md` before writing BR/VL rules (EARS 句式标准).

## Thinking Prompts (per stage)

### 1. Preflight
- "Are all upstream FEA confirmed? What's the total function count (P0/P1)?"
- Extract scope from product-ux: feature list, IX references, page/states, roles, dependencies.
- Flag: if a P0 FEA has no IX rules → warn (UX is under-specified for function design).

### 2. Intake
- Create one `FUN-XXX` block per P0 feature. Preserve `FEA-XXX` → `ST-XXX` links.
- **Before writing rules**: resolve any missing ownership or contradictory UX. If product-ux says "button does X" but user-journey says "button does Y", flag as CONFLICT.

### 3. Think (per function)
For each FUN, walk these paths systematically:
- **Main path**: happy-day flow from entry to success
- **Alternate paths**: user takes different valid route
- **Exception paths**: input errors, auth failures, state conflicts
- **Failure paths**: network timeout, system error, data inconsistency
- **Timeout paths**: idle timeout, session expiry
- **Permission paths**: role-based access control
- **Retry paths**: transient failures → retry with state preservation
- **Cancellation paths**: user aborts mid-flow
- **Rollback paths**: partial completion → cleanup

Each path → identify: what BR applies? what VL checks? what state change? what exception? what AC verifies?

### 4. Clarify
Batch questions that affect: user-visible behavior, business policy, permission rules, validation logic, state transitions, failure recovery, measurement thresholds.
Trigger `feasibility-analysis` (support skill) when material feasibility or multi-solution tradeoff exists.
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）；送审前 dor_check 会硬检查收口与引用。

### 5. Generate
Fill template (resolved by `src/templates/resolver.py function-description.md`). Each of the 7 sub-skills produces its corresponding section:
- `feature-list` → §功能清单 (FEA-*)
- `functional-flow` → §功能流程 (per-FUN flow)
- `business-rules` → §业务规则 (BR-*: domain constraints, calculations, state policies — one rule per row, linked to source BRD)
- `validation-rules` → §校验规则与字段定义 (VL-*: field-level checks with exact error message text + field definitions)
- `state-machine` → §状态变化 (STATE-*: all states × all events → target states, check completeness)
- `exception-handling` → §异常与失败处理 (EX-*: trigger → system behavior → user sees → recovery → associated BR)
- `acceptance-criteria` → §验收依据 (AC-*: Given/When/Then + quantified threshold (≤3s, >95%, etc.) + linked to G-X goal)

Rule density guard: each FUN must have ≥3 BR+VL+AC (validator will warn if under-specified).

### 6. Audit
- **Rule separation**: BR (domain), VL (format), AC (verification) are distinct categories. No BR that's actually a VL.
- **IX reference fidelity**: every IX referenced exists in product-ux with matching ID.
- **State completeness**: every state has defined entry/exit events. No orphan states.
- **Exception coverage**: every BR's exception branch has a defined recovery path.
- **AC measurability**: every AC has a quantified threshold or observable outcome.
Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors.
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Product owner confirms behavior + policy. Business owner confirms rule alignment with scope. Development reviews implementability. Testing reviews verifiability (AC completeness).

### 8. Commit / Reflow
After approval → hand FUN/BR/VL/AC IDs to PRD assembly.
Scope or feature changes → return to product-ux. Story/goal conflicts → return further upstream.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Write "system validates input" without specifying the rule | Write "VL-003: 手机号格式校验 1xx-xxxx-xxxx, 错误提示: '请使用+86手机号'" |
| Define BR that's actually a UI interaction | Reference IX from product-ux; BR = domain constraint |
| List states without transition events | Every state row: current → event → target → condition |
| Write AC as "系统应正常工作" | Given X, when Y, then Z — with threshold |
| Skip exception paths for "happy day" functions | Every function has at least: timeout, auth-failure, system-error |

## Example: Well-Specified Function Block

```markdown
### FUN-001: 活动预约提交
- **BR-001**: 活动已结束+已签到→"感谢出席"页; 已结束+未签到→"活动已结束"页 (B05)
- **VL-001**: 姓为空→红色提示"请输入您的姓氏" (F03)
- **ST-001**: 未预约→点场次选择器→选场次中 (I11)
- **EX-001**: 网络超时→弹窗"请重新提交"→点重试重新提交 (B19)
- **AC-001** (G2): Given 已登录客人填写完整信息, when 点即刻预约, then ≤3s内弹二次确认 (≤3s P95)
```

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/ears-syntax.md` | EARS 句式标准（BR/VL 规则表述） | 写 BR/VL 规则时 |
| `references/nfr-catalog.md` | NFR 分类目录（Volere 10-17） | 涉及非功能需求时 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |

## Completion

Every P0 feature has a complete functional block; IX and BR are distinct categories; permissions, validations, states, exceptions, and recovery are explicit; AC are measurable with quantified thresholds; and authorized humans approve the baseline.
