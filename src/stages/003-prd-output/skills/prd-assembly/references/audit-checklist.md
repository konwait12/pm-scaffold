# Audit Checklist · prd-assembly

## 1. Structural Gate
- [ ] 12 required sections present (§0–§12)
- [ ] Frontmatter complete (10 fields + upstream_artifact_ids)
- [ ] §0 lists all 4 upstream artifacts with status=confirmed

## 2. Aggregation Gate
- [ ] §1-§4 content matches upstream verbatim (no rewriting)
- [ ] All stable IDs preserved (SRC-*, ST-*, FEA-*, FUN-*, BR-*, AC-*)
- [ ] No new requirements introduced

## 3. Traceability Gate
- [ ] §6 RTM covers all P0 G→ST→FEA→FUN→AC→BR chains
- [ ] §7 forward trace: no broken P0 links
- [ ] §8 backward trace: no orphan elements
- [ ] §9 inconsistency report generated (may be empty)

## 4. Boundary Gate
- [ ] §5.4 only aggregates upstream UNKNOWN items
- [ ] No new QuestionRecord issues generated (PRD stage exception)
- [ ] No content modified from upstream confirmed versions

## 5. Communication Gate
- [ ] Can a new developer understand what to build?
- [ ] Can a tester write test cases from this PRD?
- [ ] Can a business stakeholder confirm "yes, this is what we asked for"?
- [ ] Are there sections that read like AI internal notes?
