---
name: validation-rules
description: Define system validation rules VL-XXX — format, range, length, required, uniqueness, cross-field constraints — each with the user-visible error message. Second rule sub-skill of function-description orchestration.
---

# Validation Rules · 系统校验

## Purpose And Boundary

Define exactly what data the system accepts and rejects at the field level, and what the user sees when validation fails. Every VL must be decidable (a developer can implement the check and a tester can construct a pass/fail case) and must carry a user-facing Chinese error message.

**Do not** define business calculations or domain policy (→ business-rules `BR-XXX`), describe how the error is displayed (→ interaction-rules `IX-XXX`), model state changes (→ state-machine), or write acceptance tests (→ acceptance-criteria `AC-XXX`).

## Inputs And Outputs

**Input**: confirmed §业务规则 (`BR-XXX`) for the function set, confirmed `product-ux` field definitions (F-XXX), and the confirmed scope baseline. **Output**: the §系统校验 section of the parent `function-description.md` (registry `output_section`: 系统校验), using the template resolved by `src/templates/resolver.py function-description.md`.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses + §2 check lenses) before analysis. Load `references/output-contract.md` before drafting. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <artifact> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "Are the §业务规则 and field definitions confirmed? Which FUN-XXX blocks have user input?"
- Enumerate every function with user-facing input fields. Flag any P0 function whose inputs are under-specified before writing VLs.
- **If no confirmed field definitions exist**, return a routing receipt and STOP — do not proceed to Intake.

### 2. Intake
- "What does the confirmed UX actually define as the input surface — not what I assume the form has?"
- List every input path: form fields, search/filter params, uploaded files, query params, batch-pasted data, and hidden inputs (URL params, defaults the user can overwrite).
- Tag each VL candidate's knowledge state: `FACT` / `DECISION` / `AI_INFERENCE` / `UNKNOWN` per `src/framework/contracts.md`. Keep the BR-XXX / FEA-XXX source on every candidate.

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "What is the minimal set of checks the system truly needs to accept this input safely? Which checks are invented decoration?"
- **Systems Thinking**: "Which other fields, BR rules, or downstream steps does this field's validity affect?"
- **Role Perspective**: "Who types this input? What would a real user mistakenly enter? What would a malicious user try?"
- **Constraint Analysis**: "What are the hard limits (length, charset, business domain values) the check must enforce?"
- **Adversarial**: "Could a value pass every check and still break downstream? Could a legitimate value be wrongly rejected (over-validation)?"
- **Reverse Validation**: "From 'valid data enters the system', what must be true about each field's format, range, and cross-field relations?"

### 4. Clarify
- Research discoverable facts first (existing formats, codebooks, system logs).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when a validation boundary or error-message wording changes data acceptance, cost, or risk.
- Limit: ≤5 questions per session. Order by impact.
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）；送审前 dor_check 会硬检查收口与引用。

### 5. Generate
- Fill the §系统校验 table. One check per row: field, check type (必填/格式/范围/长度/枚举/跨字段/唯一性), rule expression, trigger, error message, source.
- Every VL carries a user-facing Chinese error message stating "what is wrong + how to fix it" — no internal error codes.
- Status: use `draft`, `needs_user_input`, or `conditional_review` — **never `confirmed`**.
- 按需产出字段定义表（并入老版字段规则说明：字段名称、类型、长度、校验规则、来源），字段须引用来源（上游 IX/FUN）与关联校验 VL-XXX。

### 6. Audit
- **Decidability**: every VL has an executable value domain; no "校验手机号格式" without the format.
- **Error message**: every VL has a user-facing message; none are English/internal codes.
- **Coverage**: every user input field has ≥1 VL; no invisible-input gaps; no validation on read-only/system fields (never-trigger rules).
- **Cross-field**: A-required-when-B-selected dependencies match the referenced BR/UX.
- **字段定义表（按需）**：如产出，表头含「字段名/类型」，每个 F-XXX 有来源引用与关联 VL；缺失仅记 warning，记入审计说明。
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Present candidate §系统校验, evidence summary (which field/BR supports each VL), unknowns and impact, required decisions, audit result, change summary.
**Only the product owner / business owner may approve.** Approval creates a ReviewRecord with SHA-256.

### 8. Commit / Reflow
- Only `pipeline.py review --decision approve` may write `confirmed`.
- On changes: record delta → update affected VLs → re-run Audit → return to Human Gate.
- Field or BR changes upstream → re-enter this Skill from the beginning (not patched downstream).

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Write "系统应校验手机号格式" | Write "VL-003: 手机号格式 ^1[3-9]\d{9}$, 错误提示: '请输入有效的 11 位手机号'" |
| Error message "Invalid input" / code E002 | User-facing Chinese: "邮箱格式不正确，示例: name@domain.com" |
| Invent "密码必须 8 位" with no source | State the source (BR / security policy); else mark UNKNOWN and ask |
| Validate only visible form boxes | Enumerate hidden inputs too (URL params, default-overridable fields) |
| One generic message for every failure | Distinguish 必填缺失 / 格式错误 / 超出范围 / 已存在冲突 |
| Validate fields the system auto-generates | Skip read-only/system fields — rules that never fire are noise |

## Example: Sufficient Input → Sufficient Output

**Input**: confirmed FEA-003 (注册) with BR-005 (密码策略) and field definitions (手机号、邮箱、密码、确认密码).
**Output**: §系统校验 with VL-001..VL-005 — phone format, email format, password length + charset, password-confirm match (cross-field), each with a Chinese error message and traceable source.

## Example: Sparse Input → Degraded Output

**Input**: one confirmed line "注册要校验手机号和密码" with no formats, no lengths, no rules.
**Output**: Preflight returns L1 → Intake enumerates the two fields as `UNKNOWN` → Think identifies missing: phone charset/country? password length? confirm-password behavior? → Clarify generates 3 questions → stops at `needs_user_input`. No VL is fabricated with guessed values.

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

Every user-input field in every P0 FUN-XXX has ≥1 decidable VL-XXX with a user-facing Chinese error message; every VL is traceable to a BR-XXX / FEA-XXX / field definition; no invisible-input gaps and no never-trigger rules; cross-field constraints match upstream; blocking unknowns prevent confirmation; and an authorized human approves the §系统校验 baseline.
