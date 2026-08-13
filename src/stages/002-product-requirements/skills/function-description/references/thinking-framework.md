# Function Description Thinking Framework

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Testability before acceptance criteria, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

For each function examine:

1. purpose and upstream value;
2. actor, permission and precondition;
3. user action and system response (`IX`);
4. domain policy, calculation and state constraint (`BR`);
5. input, cross-field and cross-system validation (`VL`);
6. normal, alternate, exception, failure, timeout, duplicate, cancellation, retry, rollback and recovery paths;
7. state transitions and side effects;
8. measurable acceptance (`AC`);
9. security, performance, availability, accessibility and compliance only when relevant;
10. reverse trace to feature, story and goal.

Interaction and business rules coexist in the function block but must never be merged into an ambiguous sentence.
