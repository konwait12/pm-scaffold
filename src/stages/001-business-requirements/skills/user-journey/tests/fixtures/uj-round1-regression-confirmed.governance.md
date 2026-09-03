---
artifact_id: UJ-TEST-001
main_artifact: uj-round1-regression-confirmed.md
main_version: v0.1
main_sha256: 759e1d24293001cae02e5044140ce1750e12ca4ee6b5d6721d4e5937557050e3
status: ready_for_human_review
board_artifact: ""
---

# 用户旅程治理伴随文件（脱敏回归 fixture）

> 本文件供 AI、校验器和后续集成读取。人读主文档中不放这些记录。

## 类型判断与输入充分度

- 输入成熟度：L2
- 类型：业务层 + 产品层
- 已确认角色：客户、FA
- 已知阶段：4 阶段（通知 / 查看 / 认领 / 反馈）
- 输入充分度：足以支撑 ready_for_human_review，但部分细节待 PM 确认（参见主文档「待确认与风险」段）

## 主张来源与知识状态

| 主张 | 知识状态 | 来源或依据 | 主文档落点 |
|---|---|---|---|
| 短信查看率 65% | FACT | SRC-002 | 情绪与可观察信号-通知 |
| 邮件打开率 42% | FACT | SRC-002 | 情绪与可观察信号-通知 |
| 详情页停留 8 秒 | ASSUMPTION | 行业经验（UNREGISTERED，未确认） | 情绪与可观察信号-查看 |
| 认领转化率 78% | FACT | SRC-001 | 情绪与可观察信号-认领 |
| NPS 8.2 | DECISION | 项目阶段性讨论（SRC-001） | 情绪与可观察信号-反馈 |
| 短信签名拦截率偏高 | UNKNOWN | 待运营商确认 | 触点痛点 UJ-001 |

## 澄清记录

| 问题 | AI 初步判断 | PM 答复 | 是否阻断 | 回写位置 |
|---|---|---|---|---|
| 站内信触达率？ | 未知，建议补埋点 | 待确认 | 否 | 旅程覆盖与边界 |
| 短信降级规则？ | 短信失败 → 邮件重试 | 待 PM 确认 | 否 | 待确认与风险 |
| FA 协助触发条件？ | 客户主动联系 | 与现有客服流程一致 | 否 | 角色旅程矩阵-FA |

## HTML 审阅板记录

- 本用例状态：未生成
- 触发判断：粒度含 product + 角色 ≥ 2 + 阶段 ≥ 4 + 路径 ≥ 2 → 触发条件命中
- 跳过原因：本 fixture 为回归用例，结构验证优先于视觉验证；如需视觉验证，按 SKILL.md §5 Generate 触发条件生成

## AI Audit

- 角色覆盖：✅ 客户、FA 两角色均已确认
- 阶段覆盖：✅ 4 阶段齐全
- 路径多样性：✅ normal / alternative / exception / failure 四类已覆盖
- 情绪与可观察信号：✅ 含 FACT / DECISION / ASSUMPTION / UNKNOWN 四态
- 来源追溯：✅ 主文档含 SRC-001/002/003；明细在 SOURCES.md
- 用户故事种子（P0-2）：✅ 含 ST-UJ-001/002/003 三种子子（短信 / 邮件 / 站内信同目的多入口拆分）
- 触点三层枚举协议（P1-1）：✅ 使用 SMS_3RD_PARTY / EMAIL_TRANS / INAPP_REMINDER_CENTER 等标准触点 + interaction-touchpoint 格式入口
- 审计结论：通过 advisory 层；产物可进入 ready_for_human_review

## PM 确认与变更

| 日期 | 确认人 | 决定 | 说明 |
|---|---|---|---|
| 待确认 | 待确认 | 待确认 | fixture 仅作结构验证，PM 评审后正式确认 |
