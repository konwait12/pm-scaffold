---
name: prd-publish
description: Export a human-confirmed PRD to requested delivery formats without changing content, decisions, or confirmation state. Verify destination fidelity before declaring success.
---

# PRD Publish

## Purpose And Boundary

Take a **confirmed** PRD (SHA-256 verified) and export it to requested delivery channels (Feishu, PDF, HTML, Markdown). The published copy must be **byte-identical in content** to the confirmed baseline — only formatting may adapt to the target medium. The output is the `publish-record.md` artifact documenting source, destination, verifier, and timestamp.

**Do not** edit PRD content, resolve risks, create new confirmations, change knowledge states, or publish unconfirmed artifacts. If the PRD is not confirmed, stop and route back to prd-assembly. Content changes after publishing go through `change-management` / Reflow, never through silent edits during export.

## Inputs And Outputs

Inputs: a PRD with status `confirmed`, a valid ReviewRecord with SHA-256, the source file hash matching current content (tamper check), authorized reviewers in `00-input/authorized-reviewers.json`, and the requested target formats (Feishu / PDF / HTML / Markdown). If the PRD is not confirmed or the hash mismatches, STOP — do not publish.

Output: `publish-record.md` using the template at `src/support-skills/prd-publish/templates/publish-record.md`, placed in `99-review/support/`, plus the delivered channel copies.

Load `references/thinking-framework.md` (which references `src/framework/thinking-core.md` §1 mandatory lenses) before analysis. Load `references/source-handling.md` at Intake. Load `references/question-patterns.md` at Clarify. Load `references/output-contract.md` before drafting. Load `references/anti-patterns.md` at Generate. Load `references/audit-checklist.md` and `references/reviewer-checklist.md` before handoff. Run `scripts/validate_artifact.py <artifact> --json` before review.

## Thinking Prompts (per stage)

### 1. Preflight
- "Is this PRD confirmed? Does the current file hash match the confirmed SHA-256? Are all upstream artifacts confirmed?"
- Verify `authorized-reviewers.json` contains the publisher with the right role.
- **Stop if**: PRD not confirmed, hash mismatch, post-confirmation tampering detected, or any upstream artifact is not confirmed.

### 2. Intake
- "What exactly must be delivered, and to which channels?"
- Load: PRD artifact ID, version, SHA-256, confirmed reviewer, confirmed date, upstream artifact IDs.
- Determine target formats from the user request or project config. Register any channel evidence with SRC-IDs (e.g., the confirmed PRD path as SRC-001).

### 3. Think (apply thinking-core.md §1 mandatory lenses + publish domain lenses)
- **First Principles**: "What is the deliverable — exact content fidelity, nothing else? What must never change during export?"
- **Systems Thinking**: "Which downstream consumers (development, testing, business) depend on this published copy, and what do they each need intact?"
- **Adversarial**: "Could I be tempted to 'just fix a typo' or re-interpret for the medium? What guards against silent drift?"
- **Reverse Validation**: "From the stakeholder reading this copy backwards, what must be visible — headings, tables, diagrams, metadata?"
- Domain lens: Medium-Aptation Fidelity (formatting may adapt, content is immutable — see `references/thinking-framework.md`).

### 4. Clarify
- Confirm the channel list and any medium-specific constraints (Feishu doc vs PDF vs HTML).
- Batch remaining questions with: AI preliminary judgment, evidence, options, impact, owner, blocking flag.
- **Stop at `needs_user_input`** when a channel decision affects what gets delivered (e.g., which channels, whether Mermaid must render).
- Limit: ≤5 questions per session. Order by impact.

### 5. Generate
- Export each channel per its format rules (see `references/output-contract.md`):
  - Feishu Docx: verify headings, tables, Mermaid render correctly.
  - Feishu Markdown: Mermaid may not render — flag as limitation, use Docx + whiteboard where needed.
  - PDF: verify page breaks don't split tables; CJK fonts embedded.
  - HTML: self-contained (inline CSS/JS); all links absolute.
  - Markdown: relative paths adjusted for target location.
- Do not modify a single content character during export.

### 6. Audit
- **Destination Fidelity**: title matches; all headings present and ordered; tables intact; Mermaid/diagrams visible; traceability matrix intact; version + confirmation metadata visible; nothing added, removed, or reworded.
- **Tamper Check**: re-verify source hash still matches the confirmed SHA-256 after export.
- **Record Completeness**: publish-record contains source SHA-256, destination, verifier, timestamp, and any rendering limitations.
- Run `scripts/validate_artifact.py <artifact> --json`. Fix all errors. Warnings → document in audit notes.

### 7. Human Gate
Present: export summary (channels, links/paths), destination-fidelity verification results, rendering limitations, audit result.
**Only an authorized publisher may sign the publish record.** Approval creates a ReviewRecord with SHA-256. Never auto-mark the PRD as published.

### 8. Commit / Reflow
- Record the `PublishRecord` with source hash, destination, verifier, timestamp. Notify product owner, business owner, and downstream consumers with version, confirmation date, links, and known limitations.
- Any post-publish content change → route through `change-management` / Reflow; the published copy must not diverge silently.
- Later contradiction (a delivered copy diverges from source) → re-enter this Skill from Audit and re-verify.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| "Just fix a typo" during export | Export exactly the confirmed content — typo fixes go through change proposal |
| Publish unconfirmed PRD ("it's 99% done") | Stop — route back to prd-assembly Human Gate |
| Export and declare done without verifying | Verify every section rendered correctly at destination |
| Re-interpret content for the target medium | Only formatting adapts; content is immutable |
| AI marks the PRD as published | Only an authorized human signs the publish record |
| Let a delivered copy silently diverge from source | Tamper-check hashes; divergence → re-verify + change management |
| Skip recording rendering limitations | Note what couldn't render (e.g., Mermaid in Markdown) in the publish record |

## Example: Sufficient Input → Sufficient Output

**Input**: PRD `confirmed` at v1.0 with valid SHA-256, ReviewRecord present, all upstream artifacts confirmed, request "发布 PRD 到飞书和 PDF", publisher authorized in `authorized-reviewers.json`.
**Output**: Feishu Docx + PDF exported byte-identical in content; destination fidelity verified (all headings, tables, Mermaid, §7 traceability intact); `publish-record.md` filled with source hash, destinations, verifier, timestamp, and no rendering limitations → stakeholders notified.

## Example: Sparse Input → Degraded Output

**Input**: Slack message "把 PRD 发出去".
**Output**: Preflight finds the PRD's confirmation state is unknown → Intake registers SRC-001 (the PRD path) → Think identifies missing: is the PRD confirmed? which channels? who is the authorized publisher? → Clarify generates 3 questions (confirm status, channel list, publisher) → stops at `needs_user_input` — nothing is published.

## Load References

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（发布特有，写产物时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单（目的地保真核查） | Audit 前 |
| `references/output-contract.md` | 产物结构与 ID 契约（含各渠道格式规则） | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/source-handling.md` | 来源处理规则（SRC-* 登记与引用） | Intake/来源处理时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 发布领域 lens，必读） | 每次任务开始（必读） |

## Completion

PRD is exported to all requested channels; destination copies are verified byte-identical in content to the confirmed source; the publish record documents source SHA-256, destination, verifier, and timestamp; rendering limitations are recorded; stakeholders are notified; and no content, decision, or confirmation state was changed during export. The publish record itself is signed only by an authorized human.
