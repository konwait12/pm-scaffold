# ID Contract · 产物与需求追溯编号

> 编号用于追溯和稳定引用，不表示优先级、实现顺序或业务真实性。业务语义必须由内容、来源和知识状态表达，不能由前缀推断。

## 两类编号

| 类别 | 用途 | 权威来源 | 示例 |
|---|---|---|---|
| Artifact ID | 标识一个 work item 产物版本；前缀来自 `workflow-registry.json.work_items[].artifact_prefix` | 注册表 | `US-001`、`FF-001`、`STATE-001` |
| Trace ID | 标识产物内可追溯的业务条目；前缀来自本契约 | 本文件 | `ST-001`、`FEA-001`、`FUN-001` |

Artifact ID 与 Trace ID 不可互换。注册表的 `US-`、`FL-`、`FF-`、`STATE-` 是文件级 artifact 前缀，不会改变已发布的条目引用 `ST-`、`FEA-`、`FUN-`、`STATE-`。

## 当前 Trace ID

| 业务对象 | 当前格式 | 关联 work item |
|---|---|---|
| 业务目标 | `G-001` | project-background-goal |
| 用户旅程 | `UJ-001` | user-journey |
| 用户故事 | `ST-001` | user-stories |
| 功能 | `FEA-001` | feature-list |
| 功能流程 | `FUN-001` | functional-flow |
| 页面 / 交互 / 规则 / 校验 | `PD-001` / `IX-001` / `BR-001` / `VL-001` | 对应 work item |
| 状态 / 异常 / 验收 | `STATE-001` / `EX-001` / `AC-001` | 对应 work item |
| 过程记录 | `ISS-001` / `Q-001` / `RR-001` / `SRC-001` | shared capabilities |

## 兼容性与校验边界

- 新条目使用对应前缀的递增编号，必须唯一且一经引用即稳定；编号空洞是删除、合并或拆分后的合法历史，不是内容缺失的证据。
- 已确认产物不得为填补空洞而重编号；废弃条目保留为 `superseded` / `retired` 或在变更记录说明，ID 永不复用。仅未送审草稿可在人工确认前整理编号。
- 读取型校验器兼容旧目标格式 `G1`，新产物写 `G-001`；旧状态条目 `SM-001` 可保留，新产物写 `STATE-001`。
- 不对已确认 artifact 做批量重编号。引用更新与内容变更一起走 reflow，并保留旧 ID 到新 ID 的映射说明。
- 新类型必须同步更新本契约、模板、校验器和正/负 fixture；不得仅靠新增正则前缀。
- 校验器检查 ID 的存在和显式上下游连接，但编号本身不是业务正确性的证明。每条主张仍需来源、知识状态、内容与人工确认。
