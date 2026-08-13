---
name: prd-assembly
description: Assemble all confirmed business and product baselines into one traceable PRD without introducing new requirements. Apply structured review taxonomy and traceability audit.
---

# PRD Assembly

## Purpose And Boundary

Produce the single final `prd.md` by organizing confirmed upstream content, validating cross-artifact consistency, applying structured review taxonomy, and making unresolved risks visible.

**Do not**: invent, silently resolve, summarize away, polish into changed meaning, or add any new requirement. PRD assembly is **aggregation + audit**, not design.

## Inputs And Outputs

**Inputs**: All four upstream work items confirmed (project-background-goal, user-journey-and-stories, product-ux, function-description).

**Outputs**:
- `prd.md` (standard, or `--variant executive|technical`)
- Traceability matrix (G→ST→FEA→FUN→AC/BR)
- Forward trace check (§8)
- Reverse trace check (§9)
- Inconsistency report (§10)
- Review taxonomy findings (§10, using labels from `src/shared/audit/review-taxonomy.md`)

Load `references/thinking-framework.md` (→ `thinking-core.md` §1 mandatory + §2 check + §3 pre-mortem) before assembly. Load `src/shared/audit/review-taxonomy.md` before audit. If upstream `product-ux` produced a clickable prototype, load `references/prototype-embedding.md` (§4 分功能详述 may embed iframe slices + version switcher; optional, text rules remain authoritative).

## Workflow

### 1. Preflight
- "Are ALL four upstream artifacts confirmed by valid human review records?"
- Verify: all predecessors `confirmed`, no simulated/superseded/blocked baselines.
- **Stop** if any baseline is missing or unconfirmed. Route back to earliest unconfirmed Work Item.

### 2. Intake
Load without changing knowledge state: source IDs, goals (G1-G5), roles, lifecycle stages, stories (ST-XXX), scope baseline, features (FEA-XXX), UX flows, pages, interaction rules (IX-XXX), functions (FUN-XXX), business rules (BR-XXX), validations (VL-XXX), state transitions, exceptions, acceptance criteria (AC-XXX), decisions (DEC-XXX), assumptions (AII-XXX), unknowns (UNK-XXX).

### 3. Think (cross-artifact analysis)
- **Forward trace**: G→ST→FEA→FUN→AC/BR. Every AC traces to a FUN→FEA→ST→G. No orphans.
- **Reverse trace**: AC→FUN→FEA→ST. No element without upstream reason to exist.
- **Consistency check**: Compare terminology, scope, priorities, constraints, roles, states, and dependencies across all four artifacts. Flag every mismatch.
- **Pre-Mortem** (thinking-core §2.7): "If this PRD fails 3 months after launch, what's the most likely cause?" → list 3-5 failure scenarios → check if PRD addresses them.

### 4. Clarify
- **Do not answer new business questions** in this Skill.
- Record inconsistencies with evidence. Route to earliest affected Work Item.
- Block final confirmation when material inconsistency exists.

### 5. Generate
Fill template (resolved by `src/templates/resolver.py prd.md` or `--variant`).
Sections: upstream register → background → journey/stories → UX/scope/flow/IX → functions/BR/VL/AC → architecture → NFR → trace matrix (§7) → forward check (§8) → reverse check (§9) → inconsistency report (§10) → facts/decisions → constitution compliance → version history.

### 6. Audit (apply review taxonomy)
Run in order:
1. `scripts/validate_artifact.py <prd> --json` → structural validation
2. `src/scripts/traceability_check.py <REQ-DIR> --json` → explicit edge audit
3. `src/scripts/branch_validator.py <REQ-DIR> --json` → shared records validation
4. **Review taxonomy pass** (apply `src/shared/audit/review-taxonomy.md`):
   - Scan for [Contradiction]: cross-section logical conflicts
   - Scan for [Gap]: missing critical information
   - Scan for [Fallacy]: incorrect premises
   - Scan for [Redundancy]: duplicated content
   - Scan for [Dangling]: broken references
   - Scan for [Overreach]: out-of-scope implementation details
   - Scan for [Unowned]: unassigned responsibilities
   - For each finding → verdict: APPROVED / CONDITIONS / REVISION
5. Adversarial review (thinking-core §1.3): "Can I construct a scenario where this PRD leads to the wrong product?"

Any broken relationship, unapproved addition, or REVISION-level finding → gate fails.

### 7. Human Gate
Present to authorized final approver:
- The PRD (standard + requested variant)
- Trace report (forward + reverse, edge counts, orphan detection)
- Inconsistency report (with [Contradiction]/[Gap]/etc. labels)
- Unresolved risks (UNK-XXX that became material)
- Upstream deltas (what changed since last assembly)
- Review taxonomy findings with verdicts

**Automatic and simulated approval are prohibited.** Only an authorized human reviewer from `00-input/authorized-reviewers.json` may approve.

### 8. Commit / Reflow
- On approval → `prd.md` becomes `confirmed` with SHA-256 binding.
- On rejection → write reflow record → return to earliest affected Work Item → rebuild PRD.
- On CONDITIONS → approve with condition list → downstream marked `conditional_review`.

## Review Taxonomy Quick Reference

From `src/shared/audit/review-taxonomy.md`:

| Label | What to look for in PRD |
|---|---|
| [Contradiction] | Two sections say opposite things |
| [Gap] | Missing info that blocks implementation |
| [Fallacy] | Claim based on wrong assumption |
| [Redundancy] | Same info in >1 place, may drift |
| [Dangling] | Reference to non-existent ST/FEA/BR |
| [Overreach] | PRD specifies implementation detail |
| [Unowned] | No human owner for a decision |

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Add a "nice to have" feature during assembly | Route the idea back to project-background-goal |
| Fix inconsistent terminology silently | Flag as [Redundancy] or [Contradiction] in §10 |
| Skip trace because "it's obvious" | Run traceability_check.py — it finds non-obvious orphans |
| Approve with unresolved CRITICAL [Gap] | Block with REVISION verdict |
| Generate PRD without running traceability_check | Always run the explicit edge audit |

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/prototype-embedding.md` | PRD 原型嵌入技法（上游有原型时用） | 上游有原型时 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 领域 lens，必读） | 每次任务开始（必读） |

## Completion

All upstream baselines are valid and confirmed; every required G→ST→FEA→FUN→AC/BR relationship is explicit; no new requirement was introduced; review taxonomy findings are documented with verdicts; risks and conflicts are visible; machine checks (validator + traceability + branch) pass; and the authorized human explicitly approves `prd.md`.
