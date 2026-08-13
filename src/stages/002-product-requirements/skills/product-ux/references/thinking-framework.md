# Product UX Thinking Framework

## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Testability before acceptance criteria, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.

1. **Scope lens**: in, out, assumptions, dependencies, system ownership, and release boundary.
2. **Story-to-feature lens**: group by user capability and business outcome, not CRUD screens.
3. **System lens**: modules, external systems, handoffs, and ownership gaps.
4. **Flow lens**: entry, steps, decisions, main/alternate/failure paths, cancellation and recovery.
5. **State lens**: empty, loading, partial, success, failure, timeout, permission mismatch, and stale data.
6. **Role/channel lens**: role-specific access paths and material desktop/mobile/channel differences.
7. **First-principles lens**: remove functions that do not contribute to a confirmed story or goal.
8. **Adversarial/reverse lens**: try to break the flow, then verify each feature backward to a story.

Stop at the structural product model. Detailed feedback, validation, permissions, business policy and acceptance belong downstream.
