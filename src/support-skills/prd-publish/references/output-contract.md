# Output Contract · PRD Publish

## Artifact States

| Status | Meaning | Downstream use |
|---|---|---|
| `draft` | Initial candidate; Audit not complete | No |
| `needs_user_input` | Confirmation state, channel list, or publisher unresolved | No |
| `conditional_review` | Structurally reviewable with explicit non-blocking unknowns (e.g., a known rendering limitation) | No |
| `ready_for_human_review` | Self-audit passed; waiting for authorized publisher to sign | No |
| `confirmed` | Authorized human signed the publish record | Yes |
| `superseded` | A newer confirmed publish record replaces this version | No |

## Version Rules

- Start candidates at `v0.1`.
- Increment the minor candidate version for each human-requested revision: `v0.2`, `v0.3`.
- Use `v1.0` for the first signed publish record unless the host project defines another policy.
- The published PRD version must match the confirmed PRD version exactly — publishing is not a version change.

## Knowledge-State Labels

| Label | Definition |
|---|---|
| `FACT` | Confirmed source PRD statement (baseline), verified at destination |
| `DECISION` | Authorized human decision (the confirmed PRD, the publish sign-off) |
| `ASSUMPTION` | Provisional condition accepted for analysis but not confirmed |
| `AI_INFERENCE` | AI-derived interpretation (e.g., "Feishu received the doc" inferred from a tool response) |
| `UNKNOWN` | Missing information |
| `CONFLICT` | Incompatible statements (e.g., source hash vs current file content) |

The default posture of a publish record: **the content was FACT/confirmed at source, and the only question is whether the destination copy matches it.** Mark unverified delivery claims as `AI_INFERENCE` until confirmed.

## Required Sections

Use all headings from the template at `src/templates/others/publish-record.md`:

- `## 发布前检查` — PRD confirmed, hash verified, all 5 Work Items confirmed, DoD passed, no open REVISION-level issues
- `## 发布渠道` — each channel (飞书 Docx / PDF / HTML / Markdown) with status and link/path
- `## 通知` — recipients, notification method, and status

If a section has no confirmed content, write `待确认` and link it to a question or unknown ID; do not delete the heading.

## Format-Specific Rules

| Format | Tool | Key Checks |
|---|---|---|
| Feishu Docx | `lark-cli drive +import --type docx` | Headings, tables, Mermaid diagrams render correctly |
| Feishu Markdown | `lark-cli markdown +create` | Mermaid may not render — record limitation, use Docx + whiteboard where needed |
| PDF | Pandoc or browser print | Page breaks don't split tables; CJK fonts embedded |
| HTML | Direct copy or template render | Self-contained (inline CSS/JS); all links absolute |
| Markdown | Direct copy | Relative paths adjusted for target location |

## Human Responsibilities

- Authorized publisher: verifies confirmation state, signs the publish record, owns the delivery claim.
- PM: verifies destination fidelity against the source and records rendering limitations.
- Final reviewer: confirms the publish record is complete before sign-off. One person may hold multiple roles, but the decision rights must be explicit.

## Downstream Handoff

Emit a compact handoff containing:

```text
publish_version
confirmed_source_sha256
destination_links (per channel)
verification_result (fidelity checks)
rendering_limitations
notification_status
```

Do not create new requirements, risk resolutions, or confirmation records in this handoff.

## Clarifications Session Contract

Each Clarify Session is logged as a structured row inside the artifact's `## Clarifications` section (placed after `## 通知` and before the version-change summary). One row per Session, ordered by session id:

| Field | Meaning | Example |
|---|---|---|
| `session_id` | Monotonic `CL-NNN`, zero-padded | `CL-001` |
| `category` | One of 6 Impact × Uncertainty categories (scope / data-model / UX / non-functional / integration / compliance) | `integration` |
| `question` | The single question asked this turn, paraphrased | "发布到哪些渠道?需要飞书 Docx 吗,还是只 PDF?" |
| `ai_preliminary_judgment` | The AI's preliminary answer with evidence | "Inferred from SRC-001: 历史项目默认飞书 Docx + PDF; need confirmation" |
| `options` | 2–5 mutually exclusive options (or "free-form short answer") | A) 飞书 Docx B) PDF C) 飞书 Docx + PDF D) other |
| `decision_owner` | The authorized publisher who answers | 产品负责人 |
| `blocking` | yes / no | `yes` |
| `deferral_risk` | What breaks if we defer | "渠道未定则无法导出与验证" |
| `accepted_answer` | The chosen option after human reply | `C (飞书 Docx + PDF)` |
| `reflow_target` | The artifact section that gets updated | `## 发布渠道` |
| `integrated_at` | ISO timestamp when answer was written back | `2026-08-11T10:30:00Z` |
| `integrated_by` | AI or human actor | `AI` |
| `audit_recheck` | Result of the re-Audit after integration (`pass` / `fail` / `n/a`) | `pass` |

Rules:

- One row per Session. Never merge multiple Q+A rounds into a single row.
- `accepted_answer` MUST be filled in before the artifact reaches `ready_for_human_review`.
- `reflow_target` MUST reference an existing section heading.
- `audit_recheck` MUST be the last field filled; if `fail`, switch status back to `needs_user_input` and run another Session.
