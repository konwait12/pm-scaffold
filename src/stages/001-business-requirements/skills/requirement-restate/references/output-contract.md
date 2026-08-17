# Output Contract · Requirement Restate（复述确认能力）

## 目的（Purpose）

本 skill 是**能力（`output_kind=process`）**：产物是过程记录，**不进 PRD 正文**。本 skill **只做需求复述**（`requirement-restate.md` —— 共享理解检查点 shared-understanding checkpoint），非需求文档，也非候选发散产物。发散收敛已拆出为独立的 `brainstorming` skill。

## Artifact States

| 状态 | 含义 | 下游使用 |
|---|---|---|
| `draft` | 初始收集；Audit 未完成 | 否 |
| `needs_user_input` | CONFLICT / UNKNOWN 阻断 | 否 |
| `conditional_review` | 已知晓非阻断未知，可审 | 否 |
| `ready_for_human_review` | 自审通过；待 stakeholder 确认 | 否 |
| `confirmed` | 原 stakeholder 显式确认 | 是 |
| `superseded` | 被新 confirmed 版本取代 | 否 |

> 只有 `pipeline.py review --decision approve` 可确认下游工作项；过程记录本身最高 `ready_for_human_review`。

## 版本规则（Version Rules）

- 起 `v0.1`；人工要求修订时递增 minor。
- 首次 confirmed 为 `v1.0`。
- 跨阶段引用时使用 RR-XXX；版本变更记录在 `## 版本变更摘要`。

## Knowledge-State Labels

`FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`

- 每条重述标 6 态之一；无来源支持的内容标 `AI_INFERENCE` 或 `UNKNOWN`，不得混入 FACT。

---

## 需求复述行契约（RR-NNN）

### 必需章节（Required Sections）

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

### 重述行 Schema（Restate Row Schema）

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

### 内嵌于契约的反模式（Anti-Patterns Embedded In Contract）

- 出现"应该怎么设计"→ invalid，要求改写
- 多需求塞一行 → 拆 RR-NNN
- 解决方案混入 restate → 标记 `solution_leak=true`，需 stakeholder 重新确认

---

## 契约共用段

### Clarifications Session 契约（Clarifications Session Contract）

`## Clarifications` 一行一 session，≤5 sessions；`accepted_answer` 在 `ready_for_human_review` 前必填。每次 session：`CL-NNN` 单调编号；AI 初判 + 选项 + 影响 + owner + blocking；≤5 问题/轮；答案回写进重述清单对应行。未知答案成为普通 QuestionRecord / issue-record 条目，不额外开分支。

### 下游交接（Downstream Handoff）

复述通过后产出的合并体进入 issue-record 的 INF/CLS/CONFLICT 区：

```text
mode                        # rr
trigger_signal              # 多源歧义 / 单源歧义
confirmed_version
rr_count
conflict_count
unknown_count
solution_leak_count
stakeholder_signed
source_ids
```

### Anti-Patterns Embedded In Contract

- 出现"应该怎么设计"→ invalid，要求改写
- 多需求塞一行 → 拆 RR-NNN
- 解决方案混入 restate → 标记 `solution_leak=true`，需 stakeholder 重新确认
- 过程记录状态到达 `confirmed`（未经 `pipeline.py review --decision approve`）→ invalid（记录止步 `ready_for_human_review`）
