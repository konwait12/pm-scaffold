# Traceability

Maintain explicit `TraceabilityLink` records from goals to stories, features, functions, acceptance criteria and business rules. A relationship must be visible on a traceability row or statement; the presence of IDs in separate documents is not sufficient.

追溯链（v2）：`BG → UJ → US → ST → FEA → FUN → PD → IX → BR → VL → SM → EX → AC`

- `BG` = background-goal
- `UJ` = user-journey，`US` = user-stories
- `ST` = story tag（FEA/FUN 追溯用），`FEA` = feature-list，`FUN` = functional-flow
- `PD` = page-design，`IX` = interaction-rules
- `BR` = business-rules，`VL` = validation-rules，`SM` = state-machine，`EX` = exception-handling，`AC` = acceptance-criteria

PRD assembly validates forward and reverse relationships. Broken or orphan links block final confirmation and route to the earliest affected work item.
