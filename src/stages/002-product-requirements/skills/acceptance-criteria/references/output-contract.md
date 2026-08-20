# Output Contract · acceptance-criteria

## Position In Artifact

Produces the `## 1. 验收标准` section of the standalone `acceptance-criteria.md`, with each `AC-XXX` row referencing a `FEA-XXX`.
Output format must match the table in `src/templates/stage-2-product/acceptance-criteria.md`。

## AC-XXX Row Contract

| 列 | 要求 |
|---|---|
| ID | `AC-XXX`，全局唯一、稳定且不可复用；允许历史编号空洞，引用适用的 `FEA/FUN` 或显式 `GLOBAL`，不与 BR-/VL-/ST-/EX-/IX- 混淆 |
| 验收标准 | Given（前置条件）→ when（动作/事件）→ then（可观测结果）三段式，缺一不可 |
| 量化阈值 | 可量化的结果必须有具体阈值（≤ 2 秒 / ≥ 99.9% / 0 元），可回溯 `G-XXX` |
| 来源目标 | Stage 1 目标 `G-XXX` ID；无对应目标标 `待确认` 或 `UNKNOWN` |
| 优先级 | 与该 FEA 优先级一致（P0 高优），无 P0 全部低优、P1 反而高优的错位 |

## ID And Prefix Rules

- 保持 `AC-` 前缀；不与 `BR-` / `VL-` / `ST-` / `EX-` / `IX-` 混淆。
- 每条 `AC-XXX` 引用适用的 `FEA-XXX` / `FUN-XXX`；跨功能或平台级验收写 `GLOBAL` 并保留来源。ID 全局唯一且不可复用。
- 一条 AC = 一个行为（原子）；多个 when/then 拆成多条，让失败时能精准定位到是哪一步不满足。

## 状态转移覆盖（可选 · 蒸馏自 H1 test-cases StateTransition）

当本期需求**涉及状态变更**时，模板 `## 1.5 状态转移覆盖` 表**应当填写**（非强制，校验器不阻断）：
- 起始状态 / 触发事件 / 守卫 / 终止状态：必须**与 `state-machine` 产物中的转移表一一对应**
- 关联 AC：每条 ST-XX 至少挂一条 AC-XX 验证"触发 → 终止"路径
- 仅展示只读页面（无状态变更）的需求：标 `本期不适用` + 注明"无状态实体"

不适用场景举例：纯文案修正、纯配置开关、纯一次性回滚操作（无状态机）。

## Knowledge-State Labels

| Label | Meaning (AC domain) |
|---|---|
| `FACT` | 来自已确认业务目标/决策的阈值 |
| `DECISION` | 业务方对成功定义/阈值的明确决定 |
| `ASSUMPTION` | 暂定接受的验收前提 |
| `AI_INFERENCE` | AI 推断补充的阈值，未经业务确认 |
| `UNKNOWN` | 缺失的成功定义 / 阈值 / 目标关联 |
| `CONFLICT` | AC 与上游 BR/VL/EX 在触发条件或预期结果上矛盾 |

## Version / Status / Placeholder Rules

- 状态机：`draft → needs_user_input / conditional_review → ready_for_human_review → confirmed`；`confirmed` 只能由 `pipeline.py review --decision approve` 产生，AI 不得设置。
- 起始候选 `v0.1`；人工要求修订则 `v0.2`、`v0.3`；首个确认基线 `v1.0`。
- 无确认内容写 `待确认` 并链接到问题/未知 ID，不删除列。
- 无法量化的验收降级为 `UNKNOWN` 并登记到 acceptance-criteria.md「待确认问题」，不静默编造阈值。

## Downstream Handoff

按功能输出紧凑 handoff：

```text
confirmed_function_ids
ac_id_list
main_flow_acs
exception_acs
threshold_sources          # 每个阈值的 G-XXX 或待确认
open_unknowns              # 未确认的成功定义 / 阈值
source_ids
```

## Human Responsibilities

- 产品 owner：确认完成定义（成功/失败标准）与优先级。
- 业务 owner：确认量化阈值与 `G-XXX` 目标一致。
- 测试/研发：确认每条 AC 都能构造通过/失败的验证输入，可无歧义消费。
- 最终评审人：授权验收基线进入下游。一人可兼任多角色，但决策权必须明确。
