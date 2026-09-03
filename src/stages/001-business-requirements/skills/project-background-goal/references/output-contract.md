# 输出契约

## 文件

- `background-goal.md`：人和 AI 都能读的自然语言主文档。
- `background-goal.governance.md`：AI、校验器和集成读取的治理伴随文件。

两份文件必须同目录、同 artifact_id 和版本。主文档不放知识状态表、来源矩阵、审计表或哈希。

## 主文档必备内容

一句话摘要、项目背景、当前现状与已有做法、核心问题与证据、目标与成功判断、角色与干系人、约束与依赖、边界与非目标、待确认与风险、参考资料。

## 三种类型

- 重构：现状、问题证据、before -> after。
- 从 0 到 1：线下/人工过程、关键步骤、要建立的业务结果。
- 迭代：为什么加/改、加/改后要获得什么结果，保持简短。

## 状态

`draft`、`needs_user_input`、`ready_for_human_review`、`confirmed`、`superseded`。

`confirmed` 只能由 PM/业务事实负责人确认，AI 不得代写确认。
