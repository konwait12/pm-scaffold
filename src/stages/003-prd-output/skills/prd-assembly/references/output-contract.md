# Output Contract · prd-assembly

## Status Machine
Same 6 states as all Skills: draft → needs_user_input → conditional_review → ready_for_human_review → confirmed → superseded.

## Artifact Sections

正文（7 节，干系人/研发/测试阅读）：
1. **项目背景与目标** (§1): Verbatim from `project-background-goal`
2. **业务角色、用户旅程与用户故事** (§2): Verbatim from `user-journey-and-stories`
3. **UX：功能范围、功能流程与关键状态** (§3): Verbatim from `product-ux`
4. **分功能描述** (§4): Verbatim from `function-description`
5. **按需章节** (§5): Field rules, analytics, dependencies, unresolved items
6. **事实与决定** (§6): Consolidated key facts and human decisions
7. **验收依据** (§7): Acceptance baseline

附录（2 节，评审/机器用，非正文）：
- **需求追溯矩阵**: G→ST→FEA→FUN→AC→BR matrix（traceability_check.py 读取此表）
- **自审记录（Constitution Compliance）**: AI 4-principle self-audit（dor_check audit_evidence 读取）

**不在 PRD 内**（由机器在 gate 时产出、进 99-review 评审记录）：
- 上游产物清单 → frontmatter `upstream_artifact_ids`
- 正向/反向追溯检查 → `traceability_check.py` 输出
- 不一致报告 → 评审记录（review taxonomy [Contradiction]/[Gap]/… labels）
- 变更记录 → frontmatter version/updated_at + CHANGELOG

## Aggregation Rules
- Copy verbatim from upstream, never paraphrase
- Preserve all IDs (SRC-*, ST-*, FEA-*, FUN-*, BR-*, AC-*)
- No new requirements in PRD
- No silent inconsistency resolution
- Conditional chapters (§5.1, §5.2) only if upstream has non-empty content

## RTM Format
| Goal (G) | Story (ST) | Feature (FEA) | Function (FUN) | Acceptance (AC) | Business Rule (BR) |
Each row = one complete trace chain. P0 items must have complete chains.
