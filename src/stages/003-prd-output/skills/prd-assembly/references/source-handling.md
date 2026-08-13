# Source Handling · prd-assembly

This Skill is unique: it consumes ALL four confirmed upstream artifacts and produces zero new content — only aggregation, verification, and reporting.

## Primary Sources (All Four)

The PRD assembly step requires all four upstream artifacts to be `status: confirmed`:

| Work Item | Artifact ID Prefix | Provides |
|---|---|---|
| 1 | BG-XXX | §1 项目背景与目标 (goals, constraints, roles, unknowns) |
| 2 | JS-XXX | §2 用户旅程与用户故事 (journey map, story cards, path coverage) |
| 3 | UX-XXX | §3 UX (scope baseline, feature list, flows, pages, states) |
| 4 | FD-XXX | §4 功能描述 (functions, interaction rules, business rules, validation, permissions, states, exceptions/recovery, AC) |

## Aggregation Rules

1. **Copy, don't rewrite**: Content from upstream artifacts must be reproduced verbatim. No summarization, no "improved wording", no restructuring.
2. **Preserve all IDs**: Every SRC-*, ST-*, FEA-*, FUN-*, BR-*, AC-*, IX-*, G-X must appear in the PRD exactly as in the source.
3. **Section mapping**: PRD §1 ← BG, PRD §2 ← JS, PRD §3 ← UX, PRD §4 ← FD. Do not rearrange content across sections.
4. **Conditional chapters** (§5.1 字段规则, §5.2 埋点需求): Only include if the upstream FD artifact has non-empty §4 or §5. Otherwise note "本期不适用".

## What NOT to Do

- **Do NOT introduce new requirements**. If you think something is missing, record it in §9 不一致报告.
- **Do NOT resolve inconsistencies**. Record them, let the human decide.
- **Do NOT modify confirmed text**. Even if you find a typo — record it, don't fix it.
- **Do NOT add content to fill gaps**. An empty RTM cell is better than a fabricated trace link.
- **Do NOT generate new QuestionRecord issues**. Per `01-三阶段主流程与工作事项.md` §6.1, PRD stage does not independently produce new QuestionRecord. Existing unresolved items go into §5.4 未决问题与风险 as "待澄清事实".

## Traceability Verification

The RTM (§6), forward traceability check (§7), and backward traceability check (§8) are built by:

1. Parsing all four upstream artifacts for stable IDs (G-X, ST-XXX, FEA-XXX, FUN-XXX, AC-XXX, BR-XXX).
2. Following the explicit references in each artifact (e.g., §2.2 feature list says "来源故事: ST-001, ST-002").
3. Constructing the matrix mechanically — no inference, no guessing.

## Inconsistency Reporting

When a gap or contradiction is found, the §9 report must include:
- **Type**: broken_link / orphan / contradiction / priority_downgrade / missing_nfr / other
- **Elements**: Which IDs are involved, in which artifacts
- **Description**: What is the specific problem
- **Suggested resolution**: AI's recommendation (for human decision, not autonomous action)
- **Severity**: CRITICAL (blocks PRD confirmation) / HIGH (should fix) / MEDIUM (document and accept) / LOW (cosmetic)

## Conflict Handling

The PRD assembly step must not override any confirmed upstream content. If two artifacts disagree:
1. Record both versions in §9.
2. Flag the contradiction as CRITICAL or HIGH severity.
3. The human reviewer decides which version prevails and whether to trigger upstream reflow.
