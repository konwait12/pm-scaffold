# Audit Checklist · user-journey-and-stories

Self-audit before every human handoff. Run the deterministic validator first, then apply this checklist.

## 1. Structural Gate

- [ ] Frontmatter: all 11 fields present (10 standard + `upstream_artifact_id`)
- [ ] All 12 required sections present (§0–§12)
- [ ] Upstream artifact ID is a valid confirmed background-goal artifact
- [ ] Status is one of the 6 valid states
- [ ] At least one SRC-* reference in §9 that maps to an upstream source
- [ ] If status is `confirmed`, all confirmation fields are filled

## 2. Upstream Traceability Gate

- [ ] §0 verifies the upstream artifact exists and is confirmed
- [ ] §1 lifecycle stages are traceable to upstream §13 lifecycle clues
- [ ] §2 journey roles match upstream §6 confirmed roles
- [ ] §2 pain points reference upstream §4 core problems
- [ ] §6 facts cite upstream source IDs
- [ ] §9 source table maps to upstream §12 source traceability

## 3. Journey Map Quality Gate

- [ ] Journey is organized by lifecycle stage (rows) × role (columns), NOT by page/screen
- [ ] Every (stage × role) cell with content has: trigger, actions, touchpoints, pain points, expected outcome, path type, source, knowledge state
- [ ] Lifecycle stages not implied by the background but logically necessary are flagged as UNKNOWN
- [ ] At least one role appears in the journey map
- [ ] No invented roles without upstream evidence — tag as AI_INFERENCE if derived

## 4. Story Card Quality Gate

- [ ] Every story card uses the canonical format: `在〈前提/场景〉下，作为〈角色〉，我希望〈动作〉，以便〈目标/价值〉`
- [ ] Every story card has a source journey entry reference
- [ ] Story cards are grouped by role or epic theme
- [ ] Priority hints are informed by upstream §5 goals
- [ ] Story IDs are sequential (ST-001, ST-002, ...) and unique

## 5. Coverage Gate

- [ ] §4 coverage matrix maps every non-empty journey entry to ≥ 1 story card
- [ ] §5 path type coverage checks all 6 types (normal/alt/exception/failure/handoff/recovery)
- [ ] Unexplained gaps are marked with a reason
- [ ] Orphan story cards (no source journey entry) are tagged and justified

## 6. Knowledge State Gate

- [ ] §6 FACT entries have source evidence
- [ ] §7 ASSUMPTION entries have a basis and an owner
- [ ] §7 AI_INFERENCE entries are labeled as such (not passed off as FACT)
- [ ] §7 CONFLICT entries preserve both sides — no silent resolution
- [ ] §7 UNKNOWN entries have an assigned owner and impact assessment

## 7. Semantic Red Flags (same spirit as `project-background-goal`)

Check for:

1. Ready for review but journey map has < 2 lifecycle stages → likely insufficient decomposition
2. Story cards present but no journey entries → missing upstream traceability
3. Journey map mentions roles NOT in upstream §6 → invented content
4. All stories are normal-path only → missing exception/failure/recovery coverage
5. Story cards describe UI interactions ("click button", "open page") → premature UX design
6. Coverage matrix shows gaps without reasons → incomplete audit

## 8. Human Gate

- [ ] All blocking Clarify sessions have accepted answers
- [ ] No more than 5 Clarify sessions; if 6+, `needs_user_input`
- [ ] All `待确认` in body content are intentional non-blocking items
- [ ] Constitution Compliance §11 has all 4 principles assessed (not `待确认`)
- [ ] Downstream handoff summary (§10) is complete enough for product-ux to consume

## 9. Regression Gate

- [ ] `python3 scripts/validate_artifact.py <artifact.md> --json` returns `"ok": true`
- [ ] Template itself passes the validator
- [ ] At least one fixture covers sufficient mode
- [ ] At least one fixture covers degraded mode
