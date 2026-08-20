# 输出契约 · 问题清单（Issue Record · 跨阶段共享）

## 产物状态（Artifact States）

| 状态 | 含义 | 下游使用 |
|---|---|---|
| `draft` | 初始收集；Audit 未完成 | No |
| `needs_user_input` | 阻断 / 待决；需要先回答 | No |
| `conditional_review` | 已知晓非阻断未知，可审 | No |
| `ready_for_human_review` | 自审通过；待授权审 | No |
| `confirmed` | 仅为历史兼容保留；Issue Record 不作为独立 work item 确认 | No |
| `superseded` | 被后续版本取代 | No |

## 版本规则（Version Rules）

- 起 `v0.1`，人工要求修订时递增 minor。
- Issue Record 随主线工作项持续更新；其结构和 B3 收口通过每次 `pipeline.py ... gate` 校验。最终 PRD 的确认由 `prd-assembly` 处理。
- 新问题随时可加；状态变更走 Audit。

## 知识状态标签（Knowledge-State Labels）

`FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`

## 必需章节（Required Sections）

| § | 标题 | Required |
|---|---|---|
| 1 | 项目元数据 | Yes |
| 2 | 总览（按类别与状态计数） | Yes |
| 3 | Blocker（BLK） | Yes |
| 4 | Risk（RSK） | Yes |
| 5 | Decision-in-waiting（DEC） | Yes |
| 6 | Information gap（INF） | Yes |
| 7 | Clarification（CLS） | Yes |
| 8 | Out-of-band（OUT） | Yes |
| 9 | Closed Issues（accepted / resolved / escalated） | Yes |
| 10 | 来源追溯 | Yes |
| 11 | 待确认问题 | Yes |
| 12 | Constitution Compliance | Yes |
| 13 | 阶段收口表（B3） | Yes，L1/L2 only |

空章节用明确的“无”声明，不删除标题。L0 不创建 issue-record；L1/L2 的
`§13 阶段收口表` 是由 `00-input/intake-decision.md` 的持久化
`process_tier` 与 workflow registry 派生的治理账本，不能手工沿用另一档位的行。

## 问题结构（Issue Schema）

| 字段 | 必填 | 说明 |
|---|---|---|
| `ISS-NNN` | Yes | 单调递增，限定本 artifact |
| `category` | Yes | `BLK` / `RSK` / `DEC` / `INF` / `CLS` / `OUT` |
| `state` | Yes | `open` / `in_progress` / `blocked` / `accepted` / `resolved` / `escalated` |
| `title` | Yes | 一句话、具体 |
| `description` | Yes | 上下文 / 影响 / "完成" 的定义 |
| `owner` | Yes | 个人或角色 |
| `knowledge_state` | Yes | 6 态之一 |
| `source` | Yes | SRC-ID |
| `affected_artifact` | Optional | 来自哪个上游产物 |
| `raised_at` | Yes | 提单日期 |
| `target_close` | Required for BLK/DEC | 目标解决日期 |
| `mitigation` | Required for RSK | 缓解措施 |
| `resolution` | Required for resolved | 解决内容与引用变更 |
| `escalated_to` | Required for escalated | 新 Owner 或机构 |
| `notes` | Optional | 边缘情况 / 依赖 |

## 审计钩子（Audit Hooks）

- 上游产物每个"待确认"必须有 ISS-NNN 引用或 `closed_at_intake` 理由
- 每个 open 都有 Owner
- BLK / DEC 都有 target_close
- 30 天以上 open 都有 escalation 记录
- B3 收口表的 `(阶段, Work Item)` 必须与当前档位 work item 集合精确相等：
  L1 为 7 个上游加 `prd-assembly`（8 行），L2 为 13 行；缺行、重复行、
  跨档行或错误阶段均为结构错误。
- 每次送审时，当前 work item 的 B3 行必须已收口；其余行可以保持 `open`，
  但不得伪造不属于当前档位的“0 问题”记录。

## 人类职责（Human Responsibilities）

- 决策 Owner：接受 `accepted` 状态，签发 closed-out 列表
- 问题 Owner：维护状态、Owner、target_close
- 最终 Reviewer：授权 issue list 用于 PRD 确认

## 下游移交（Downstream Handoff）

```text
confirmed_version
open_count
in_progress_count
blocked_count
accepted_count
resolved_count
escalated_count
open_blk_ids
open_dec_ids
critical_top5
source_ids
```

## 澄清会话契约（Clarifications Session Contract）

`## Clarifications` 一行一 session，≤5 sessions，`accepted_answer` 在 `ready_for_human_review` 前必填。
