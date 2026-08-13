# Function Description Audit Checklist

- [ ] Every P0/P1 feature has a `FUN-XXX` block and upstream links.
- [ ] Every P0 function has `IX`, `BR`, `VL`, state, exception/recovery and `AC` coverage.
- [ ] Interaction rules state user action and system response without hiding domain policy.
- [ ] Business rules state enforceable domain logic without vague UI wording.
- [ ] Permissions cover all relevant upstream roles.
- [ ] Alternate, failure, timeout, duplicate, retry, cancellation and rollback were considered.
- [ ] Acceptance criteria are measurable and traceable.
- [ ] Conditional fields/analytics are included only with a real trigger.
- [ ] No architecture, API, database schema or test-case implementation leaked in.
