# Output Contract · Requirement Restate

## Purpose

Confirm a shared understanding of the ask **before** any design, journey, or PRD work begins. The artifact is a **shared-understanding checkpoint**, not a requirements document.

## Artifact States

| Status | Meaning | Downstream use |
|---|---|---|
| `draft` | 初始收集；Audit 未完成 | No |
| `needs_user_input` | CONFLICT / UNKNOWN 阻断 | No |
| `conditional_review` | 已知晓非阻断未知，可审 | No |
| `ready_for_human_review` | 自审通过；待 stakeholder 确认 | No |
| `confirmed` | 原 stakeholder（或其指定代理）显式确认 | Yes |
| `superseded` | 被新 confirmed 版本取代 | No |

## Version Rules

- 起 `v0.1`；人工要求修订时递增 minor。
- 首次 confirmed 为 `v1.0`。
- 跨阶段引用时使用 RR-XXX；版本变更记录在 `## 版本变更摘要`。

## Knowledge-State Labels

`FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`

## Required Sections

| § | 标题 | Required |
|---|---|---|
| 1 | 项目元数据 | Yes |
| 2 | 来源清单（SRC-IDs） | Yes |
| 3 | 重述需求清单（RR-XXX） | Yes |
| 4 | 冲突清单（CONFLICT → ISS-XXX） | Yes |
| 5 | 未知清单（UNKNOWN → Q-XXX） | Yes |
| 6 | stakeholder 自查反馈位 | Yes |
| 7 | 来源追溯 | Yes |
| 8 | 待确认问题 | Yes |
| 9 | Constitution Compliance | Yes |

空章节用 `待确认` 占位，不删除标题。

## Restate Row Schema

| 字段 | 必填 | 说明 |
|---|---|---|
| `RR-NNN` | Yes | 单调递增，本 artifact 内唯一 |
| `restated` | Yes | 用 stakeholder 的话重述（避免翻译损耗） |
| `original_phrase` | Yes | stakeholder 原始措辞（保留方言、口语） |
| `source` | Yes | SRC-ID（具体到段落/时间戳） |
| `knowledge_state` | Yes | 6 态之一 |
| `stakeholder` | Yes | 谁提出 |
| `confidence` | Yes | high / medium / low |
| `solution_leak` | Optional | 标记是否意外夹带方案（要求复审） |

## Anti-Patterns Embedded In Contract

- 出现"应该怎么设计"→ invalid，要求改写
- 多需求塞一行 → 拆 RR-NNN
- 解决方案混入 restate → 标记 `solution_leak=true`，需 stakeholder 重新确认

## Downstream Handoff

restate 通过后产出的合并体进入 issue-record 的 INF/CLS/CONFLICT 区：

```text
confirmed_version
rr_count
conflict_count
unknown_count
solution_leak_count
stakeholder_signed
source_ids
```

## Clarifications Session Contract

`## Clarifications` 一行一 session，≤5 sessions；`accepted_answer` 在 `ready_for_human_review` 前必填。
