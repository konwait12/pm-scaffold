# Thinking Framework · prd-assembly

Lenses for aggregating four confirmed artifacts into a single PRD with traceability verification.

This Skill differs from 前四个工作事项: it does NOT generate new content. It aggregates, verifies, and reports.


## Common Core (MANDATORY)

Apply the **6 core lenses** from `src/framework/thinking-core.md` §1 (First Principles, Systems Thinking, Adversarial Review, Reverse Validation, Confirmation Bias Defense, Knowledge Boundary) plus the check-layer lenses from §2 relevant to this work item (Pre-Mortem before phase close, Fresh-Eyes before Human Gate, Testability before acceptance criteria, Conclusion First + Reader Perspective when writing). Record only findings that change the candidate — do not repeat core-lens analysis verbatim.
## Lens 1: Aggregation Integrity

When pulling content from upstream artifacts into the PRD:

1. **Copy verbatim**, do not paraphrase. "润色" = unauthorized modification. The confirmed text has been reviewed by a human — you have no authority to change it.
2. **Preserve all source IDs**. Every SRC-*, ST-*, FEA-*, FUN-*, BR-*, AC-* must remain intact.
3. **If you find an error** in confirmed content: do NOT fix it silently. Record it in §9 不一致报告 and flag for human attention.

**Anti-pattern**: "This section from `project-background-goal` was a bit wordy, so I summarized it." — This is a violation of the aggregation contract.

## Lens 2: Forward Traceability

Walk the chain from goals to acceptance criteria:

```
G-X (background §5) → ST-XXX (journey §3) → FEA-XXX (UX §2.2) → FUN-XXX (function §1) → AC-XXX (function §2) → BR-XXX (function §2)
```

For each link, verify:
1. **G→ST**: Does every confirmed goal have ≥ 1 story that addresses it?
2. **ST→FEA**: Does every P0 story map to ≥ 1 feature?
3. **FEA→FUN**: Does every P0 feature map to ≥ 1 function?
4. **FUN→AC**: Does every P0 function have ≥ 1 acceptance criterion?
5. **AC→BR**: Does every AC with a business rule reference it?

Record broken links in §7 正向追溯检查.

## Lens 3: Backward Traceability

Walk the chain in reverse:

```
BR-XXX → AC-XXX → FUN-XXX → FEA-XXX → ST-XXX → G-X
```

For each element, verify:
1. **BR→AC**: Does every business rule have a corresponding AC that tests it?
2. **AC→FUN**: Does every acceptance criterion belong to a function?
3. **FUN→FEA**: Does every function trace to a feature?
4. **FEA→ST**: Does every feature trace to ≥ 1 story?
5. **No orphans**: Are there any elements with no upstream connection?

Record orphans in §8 反向追溯检查.

## Lens 4: Cross-Artifact Consistency

Scan for contradictions across artifacts:

| Check | What to Look For |
|---|---|
| **Role consistency** | Same role name, same description across all 4 artifacts |
| **Term consistency** | Same term means the same thing everywhere (e.g., "候选人状态" in `user-journey-and-stories` should match "候选人状态管理" in `function-description`) |
| **Constraint consistency** | Background §7 constraint still respected in `function-description` function descriptions? |
| **Scope consistency** | Background §8 non-goals → Are any of them accidentally included as features in `product-ux`? |
| **Priority consistency** | P0 story in `user-journey-and-stories` → P0 feature in `product-ux` → P0 function in `function-description`? No silent priority downgrades? |

**Anti-pattern**: Finding a contradiction and fixing it yourself. Record it in §9, let the human decide.

## Lens 5: Gap Detection

Identify what SHOULD be present but is missing:

1. **Uncovered goals**: A G-X with no downstream chain at all.
2. **Missing functions**: A P0 feature (FEA-XXX) with no function description (FUN-XXX).
3. **Untested acceptance criteria**: An AC-XXX with no measurable threshold.
4. **Missing NFR coverage**: A function that obviously needs NFR (e.g., handles personal data) but has no NFR section.

## Lens 6: RTM Construction

Build the Requirements Traceability Matrix (§6):

| G | ST | FEA | FUN | AC | BR |
|---|---|---|---|---|---|
| G1 | ST-001, ST-002 | FEA-001 | FUN-001, FUN-002 | AC-001, AC-002 | BR-001, BR-002 |

Rules:
- Each row represents one complete trace chain.
- A single G may span multiple rows (one per downstream branch).
- Empty cells are allowed for P2 elements, but must be noted.
- The RTM is built by reading all four artifacts, not by guessing.

## Lens 7: Completeness Final Review

Before submitting for human review, ask:

1. Can a new developer read this PRD and understand what to build without asking the PM?
2. Can a tester read this PRD and write test cases without ambiguity?
3. Can a business stakeholder read §1-§2 and confirm "yes, this is what we asked for"?
4. Are there any sections that read like internal AI notes rather than a deliverable document?

## Lens 8: Pre-Mortem (PRD 交付后失败预演)

The PRD is the contract handed to development. Before final approval, run a failure rehearsal:

1. What is the most likely way this PRD gets misread or misimplemented? (ambiguous term, buried constraint, contradictory rule)
2. What is the most likely scope creep after this PRD ships? (a near-IN feature the business will request, an assumption stated but not frozen)
3. What would the first 3 bug reports against this PRD look like? Are they covered by ACs?
4. What would a reviewer reject this PRD for? (missing acceptance basis, untraceable requirement, unclear ownership)

Record each failure mode in §9 不一致报告 / risk section with an owner — do not silently fix confirmed content.

---

## 表达层技法（可选加载）

当上游 product-ux 已产出可点击原型时，加载 `references/prototype-embedding.md`（吸收自 agile-pm-workflow），在 PRD §4 分功能详述区嵌入原型 iframe 切片（focus 沙盒锁定 + 版本切换器）。**文本规则仍是权威，切片是增强；原型缺失不静默跳过，在 §9 不一致报告标注。**
