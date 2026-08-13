# Source Handling · user-journey-and-stories

This Skill primarily consumes one upstream artifact (confirmed project-background-goal). Source handling is therefore lighter than `project-background-goal`, but must still be rigorous.

## Primary Source

The confirmed `project-background-goal` artifact is the primary and authoritative source. Its §13 downstream handoff summary provides:
- `confirmed_roles`: → §2 journey map roles
- `known_lifecycle_clues`: → §1 lifecycle decomposition
- `goal_summary`: → §3 story priority hints
- `constraints_and_dependencies`: → boundary conditions for journey scope
- `source_ids`: → cross-referenced in §9

## Secondary Sources

When the upstream artifact references original materials (SRC-001, SRC-002, etc.), these may be consulted for additional context about roles and lifecycle, but only when the upstream artifact's summary is insufficient. Never override the confirmed artifact with raw source interpretation.

## Source Registration

Each claim in the journey map and story cards must reference either:
- The upstream artifact ID (for confirmed background facts)
- A specific SRC-* ID from the upstream artifact (for direct source evidence)
- An AI_INFERENCE or ASSUMPTION tag (for derived content)

## Conflict Handling

If a journey entry conflicts with the upstream background:
1. Flag as CONFLICT in §7.
2. Present both the journey-derived claim and the upstream background statement.
3. Request human resolution via Clarify.
4. Do not silently pick one side.

## Multi-Source Cross-Validation

When the upstream background has ≥ 3 sources, verify that:
- Role descriptions are consistent across sources
- Lifecycle stages are supported by ≥ 1 source
- Pain points in the journey map are traceable to upstream §4
