# Function Description Output Contract

交付物：**一个 `function-description.md`**，由 7 个子 skill 依次产出 7 个章节：

| 章节 | 产出子 skill | ID 前缀 |
|---|---|---|
| §功能清单 | `feature-list` | `FEA-` |
| §功能流程 | `functional-flow` | （描述每个 `FUN-XXX` 的流程，无独立 ID） |
| §业务规则 | `business-rules` | `BR-` |
| §校验规则与字段定义 | `validation-rules` | `VL-` |
| §状态变化 | `state-machine` | `STATE-` |
| §异常处理 | `exception-handling` | `EX-` |
| §验收依据 | `acceptance-criteria` | `AC-` |

ID 前缀语义：

- `FEA-XXX`: confirmed in-scope feature inventory（功能清单）。
- `BR-XXX`: domain policy, calculation, constraint or state rule（业务规则）。
- `VL-XXX`: input/data validation, field definitions, and user-visible error outcome（校验规则与字段定义）。
- `STATE-XXX`: entity state transitions — states × events → target states（状态变化）。
- `EX-XXX`: exception / failure / retry / rollback / recovery behavior（异常处理）。
- `AC-XXX`: measurable Given/When/Then acceptance basis（验收依据）。

每个 P0/P1 `FUN-XXX` 在 §功能流程 中描述其完整流程（主流程 / 备选 / 异常 / 失败 / 超时 / 权限 / 重试 / 取消 / 回滚路径），并引用其 `FEA-XXX` / `ST-XXX` / 前置条件 / 角色权限。字段规则（§校验规则与字段定义）与埋点章节按需出现。
