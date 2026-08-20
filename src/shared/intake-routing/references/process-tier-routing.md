# Process Tier 路由（PRD 工序档位决策）

> 工序档位与材料成熟度 L0-L4 正交：前者决定交付和治理强度，后者只说明输入材料的完整程度。`00-input/intake-decision.md` 是唯一档位事实源；README 仅为投影。

## 1. 交付定义

| 档位 | 适用边界 | work item | 治理 | 不适用内容 |
|---|---|---:|---|---|
| L0 | 单一可定位改动、单角色、无持久状态/敏感数据/合规/迁移、单一简单回退 | 1：`mini-prd` | 一次 `business_owner` 审批、ReviewRecord、hash anchor、audit event | 跨产物追溯、issue-record、阶段收口 |
| L1 | 受限场景下可实施的标准交付；五项 L2-only 能力均有事实化“不适用”依据 | 8：7 个上游 + `prd-assembly` | 完整确认、审计和集内追溯 | `page-design`、`interaction-rules`、`validation-rules`、`state-machine`、`exception-handling` 本身 |
| L2 | 有状态、交互、验证、异常、合规、多系统或多角色协作的完整路径 | 13 | 完整治理与追溯 | 无 |

L1 的 7 个上游为 `project-background-goal` → `user-journey` → `user-stories` → `feature-list` → `functional-flow` → `business-rules` → `acceptance-criteria`；加最终 `prd-assembly` 共 8 个 work item。

## 2. 资格矩阵与硬升级条件

评分可以作为沟通提示，但不得覆盖硬条件，也不得单独决定档位。决策人必须在 intake 决策中记录每一项事实依据。

| 维度 | L0 必须同时满足 | L1 可以满足 | 命中后必须 L2 |
|---|---|---|---|
| 范围 | 单一点、可定位变更 | 单模块主流程 | 多模块/多系统/数据迁移 |
| 角色与状态 | 单角色、无持久状态设计 | 单角色或受限协作，且无状态机 | 多角色协作、状态机或生命周期 |
| 风险 | 无 PII、资金、合规或安全影响 | 有明确不适用事实 | PII、资金、合规、安全或权限模型变更 |
| 交互与规则 | 仅简单既有界面/配置 | 五项 L2-only 均明确不适用 | 需页面、交互、字段校验、状态或异常规则 |
| 回退 | 单一简单回退 | 有可实施回退边界 | 多个独立恢复路径或不可逆操作 |

五项 L2-only 能力为 PD（页面/原型）、IX（交互规则）、VL（校验规则）、STATE（状态机）、EX（异常处理）。L1 对其中任一项只要“适用”，必须升级 L2；不得用空泛的“本期不适用”代替事实依据。

## 3. 创建与迁移

1. 新 REQ 必须执行 `pipeline.py init REQ-NNN-topic --process-tier L0|L1|L2`。
2. 初始化写入 `00-input/intake-decision.md`，并只创建公共目录及本档位 work item 目录。
3. `status`/`entry` 的 `--process-tier` 仅用于预览差异；`gate`、`review`、`reflow` 和发布均使用持久化档位，并拒绝跨档 work item。
4. 既有 REQ 若无 intake 决策，按 L2 兼容读取。迁移时应创建 intake 决策，不能只改 README。
5. 已确认产物不得通过降档规避治理。改档前必须留存升级/降档原因，并对受影响下游执行 reflow。

## 4. 复审触发

范围、角色、状态、数据、合规、权限、异常恢复或回退策略发生变化时，必须回到本路由重评；命中任一硬升级条件后，停止当前低档位产物的确认并升级。
