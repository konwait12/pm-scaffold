# Output Contract · prd-assembly

## Status Machine
Same 6 states as all Skills: draft → needs_user_input → conditional_review → ready_for_human_review → confirmed → superseded.

## Artifact Sections
1. **上游产物清单** (§0): All 4 upstream artifacts must be confirmed
2. **项目背景与目标** (§1): Verbatim from `project-background-goal`
3. **业务角色、用户旅程与用户故事** (§2): Verbatim from `user-journey-and-stories`
4. **UX：功能范围、功能流程与关键状态** (§3): Verbatim from `product-ux`
5. **分功能描述** (§4): Verbatim from `function-description`
6. **按需章节** (§5): Field rules, analytics, dependencies, unresolved items
7. **需求追溯矩阵** (§6): G→ST→FEA→FUN→AC→BR matrix
8. **正向追溯检查** (§7): Forward trace validation
9. **反向追溯检查** (§8): Backward trace validation
10. **不一致报告** (§9): Cross-artifact contradiction report
11. **事实与决定** (§10): Consolidated from all work items
12. **Constitution Compliance** (§11): 4-principle check
13. **验收依据与变更记录** (§12): Acceptance baseline + version history

## Aggregation Rules
- Copy verbatim from upstream, never paraphrase
- Preserve all IDs (SRC-*, ST-*, FEA-*, FUN-*, BR-*, AC-*)
- No new requirements in PRD
- No silent inconsistency resolution
- Conditional chapters (§5.1, §5.2) only if upstream has non-empty content

## RTM Format
| Goal (G) | Story (ST) | Feature (FEA) | Function (FUN) | Acceptance (AC) | Business Rule (BR) |
Each row = one complete trace chain. P0 items must have complete chains.
