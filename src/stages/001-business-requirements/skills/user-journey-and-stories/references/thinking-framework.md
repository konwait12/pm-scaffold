# Thinking Framework · user-journey-and-stories

Lenses for decomposing business lifecycle and deriving story cards from a confirmed project background.


## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Testability before acceptance criteria, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.
## Lens 1: Lifecycle Decomposition

Break the business domain into sequential stages from the user's perspective, not the system's:

1. Identify the natural start and end of the lifecycle from the background.
2. List all stages a user passes through (awareness → engagement → transaction → fulfillment → offboarding).
3. For each stage, ask: who acts? who is affected? what triggers entry? what triggers exit?
4. Flag stages not mentioned in the background but logically implied.

**Anti-pattern**: Decomposing by system module or page instead of by business event.

## Lens 2: Role-Based Perspective

For each confirmed role from upstream §6:

1. Walk through the lifecycle stage by stage as that role.
2. What does this role see, do, need, and fear at each stage?
3. Where does this role interact with other roles?
4. What information does this role need from or pass to others?

**Anti-pattern**: Focusing only on the primary user and ignoring supporting roles.

## Lens 3: Path Type Expansion

For each journey entry, explicitly consider all 6 path types:

| Type | Question |
|---|---|
| Normal | What happens when everything goes right? |
| Alternative | What other valid way could this role achieve the same goal? |
| Exception | What business rule violations can occur? |
| Failure | What system or external failures can block this? |
| Handoff | Where does responsibility transfer between roles? |
| Recovery | How does the user recover from a failure or mistake? |

**Anti-pattern**: Only mapping the happy path and calling it done.

## Lens 4: Story Completeness

For each story card, verify:

1. Is the scene described clearly enough that a developer could estimate it?
2. Is the goal stated as an outcome, not a feature?
3. Can the story be traced back to a specific journey entry?
4. Does the story's path type match the journey entry?

**Anti-pattern**: Writing stories as feature requests ("As a user, I want a dashboard") without context.

## Lens 5: Adversarial Review

1. If I were the business owner, what lifecycle stage would I say is missing?
2. If I were a developer, what story would I say is too vague to implement?
3. If I were a tester, what failure path would I say is uncovered?
4. If I were the user, what handoff or recovery scenario would I say is ignored?

## Lens 6: Role Immersion

For EACH confirmed role from the upstream background, explicitly role-play before deriving story cards:

1. **Become this role**: What do I care about? What am I responsible for? What frustrates me today?
2. **Walk through the lifecycle as this role**: At each stage, what do I see? What do I need? What could go wrong for me specifically?
3. **What would I ask for?**: If I were this role in a stakeholder meeting, what feature or scenario would I demand that isn't in the source materials?
4. **What am I afraid of?**: What change or new system would threaten my workflow or responsibilities?

Output: For each role, produce 2-3 "immersed scenarios" that go beyond what the source materials explicitly state. Mark these as **AI_INFERENCE** — they are discovered, not confirmed.

**Anti-pattern**: Listing roles from the background without actually thinking from their perspective. "内容编辑需要查看稿件" is role-listing. "内容编辑每天收到 30 篇投稿邮件，最怕漏掉高质量作者的首发投递——所以需要统一收件箱和筛选标记" is role-immersion.


## Lens 7: MECE Scenario Enumeration (B2 场景发散)

Before the work item closes, enumerate candidate scenarios exhaustively using a **matrix**, not a list:

1. **Cut 1 — Role**: every confirmed role × every lifecycle stage. Empty cells = candidate missing scenarios.
2. **Cut 2 — Path type**: every (stage × role) cell × the 6 path types (normal/alt/exception/failure/handoff/recovery). Uncovered types = candidate exception/failure/handoff scenarios.
3. **Cut 3 — Business event**: for each cell, ask "what event enters/exits this cell?" and "what event would business say is missing?"
4. Only after the matrix is fully filled, mark: covered cells (ST-XXX), B2 candidate questions, explicitly out-of-scope cells (with reason).

**Anti-pattern**: Brainstorming a flat list without the matrix — this always misses gaps in the least obvious cells. Ask the business only about cells that are uncovered, logically implied, or require a scope decision.


## Degraded Mode

When the upstream background has fewer than 2 confirmed roles or unclear lifecycle clues:

1. Extract whatever roles and lifecycle hints exist.
2. Build a minimal journey with `UNKNOWN` markers for missing stages.
3. Derive only the stories that are directly supported.
4. Flag all gaps explicitly in §7 and §8.
5. Set `needs_user_input` for any blocking gap.


## Lens 8: 旅程体验验证技法（Journey Experience Validation）

Specs 测功能，Journeys 测体验——旅程在拆成 story 卡之前，先对关键旅程做三重体验验证：

1. **Persona 快照（Persona Snapshot）**：每个关键旅程先写该角色进入旅程时的心智快照——是谁、带什么目标/情绪/前置状态（首次/回访/管理员、已登录/购物车有货/弱网）。同一旅程在不同前置状态下体验完全不同，快照决定后续步骤与成功标准是否成立。
2. **情感曲线（Emotion Curve）**：沿旅程步骤标注情绪高/低点（沮丧、困惑、惊喜、满足）。高点 = 体验峰值要保住；低点 = 摩擦点必须给出缓解（骨架屏、进度提示、明确下一步）。只列步骤不标情绪的旅程等于没验证。
3. **错误恢复路径验证（Error Recovery Validation）**：对每一步追问「用户会在这里出错吗？出错后如何回到正轨？」。关键旅程至少写 1-2 个错误场景：触发原因 / 用户看到什么 / 恢复路径 / 如何验证恢复有效。只画 happy path 的旅程是反模式。

产出标注：persona 快照与情绪解读是体验推断，标 **AI_INFERENCE**；错误恢复路径若出自背景材料为 FACT，出自推断为 AI_INFERENCE，均不得写成 confirmed。验证结果随 journey 产物交 Human Gate 人工确认。

**Anti-pattern**: 把旅程写成 specs 列表（步骤 + 系统响应），缺前置状态、缺情绪标注、缺错误恢复路径。
