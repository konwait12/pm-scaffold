# 治理与质量闸门

## 质量顺序

每个工作项依次执行结构校验、语义与领域审计、沟通检查和人工评审；PRD 汇总还要执行跨产物关系与记录校验。

事件溯源层（`audit_log` 与 `projection_cache`）是评审和变更生命周期的唯一事实源。校验器读取 `.audit/projection.json`，而不是按文件名 glob 后排序；每次状态变更都先向 `.audit/events.jsonl` 追加 `AuditEvent`，再写入产物 frontmatter，因此日志始终可以重放。

## 工序档位

每个新 REQ 的持久化档位只以 `00-input/intake-decision.md` 为准。L0 省略跨产物工作流，但不省略审批证据：真实人工评审、`ReviewRecord`、哈希锚点和审计事件均为必需。L1 包含 7 个上游产物和 PRD 汇总，共 8 个工作项；只有 intake 对 PD/IX/VL/STATE/EX 分别记载了可核验的不适用理由时，才可省略它们。任一能力实际适用时默认进入完整 L2。针对持久化档位外工作项的命令，必须在写入产物、评审记录、锚点或事件前失败。

## 确认规则

`confirmed` 要求评审人已列入需求的 `00-input/authorized-reviewers.json`，其角色还必须出现在该工作项注册表的 `reviewer_roles` 中。`ReviewRecord` 绑定时间、稳定评审人 ID、角色和被审产物的版本与哈希。`ready_for_human_review`、`conditional_review`、`simulated` 和 `needs_user_input` 都不代表完成；人工驳回或任何阻断性机器闸门都会使命令失败。

每次 review、change、confirm 和 reflow 都通过 `audit_log.append_event` 向 `.audit/events.jsonl` 追加 `AuditEvent`；`projection_cache` 将最新状态折叠到 `.audit/projection.json`。哈希链由 `prev_hash`、`event_sha256` 自指纹和 `payload_sha256` 记录体绑定组成，`audit_log.verify_chain` 能检测篡改。

## 质量维度

检查完整性、正确性、清晰度、追溯性、一致性、可验证性、角色与场景覆盖以及下游可用性。只出现关键词不能证明满足产物契约。

## 在制约束

每个需求同一时刻只能有一个活跃工作项。被阻断的工作项必须保留负责人、影响和回流目标；同一问题反复修改时触发升级与方向复审。

## 变更控制

产品 UX 被确认后范围冻结。新增功能必须有上游用户故事，或先发起明确的上游回流。已确认产物改变时，受影响的下游确认必须失效并重跑。

## 人机协作询问契约

本脚手架不是“一份 PRD 适配所有需求”的生成器。每个分支和产物都有默认行为及询问闸门，人工可以明确覆盖默认选择。

### 何时询问

任一 Skill 在下列情况出现时必须发起结构化询问：

1. 产出可能写入 `prd.md`，但并非必填正文，例如范围基线、埋点计划、问题清单风险摘要或复述来源。
2. 输入包含“待确认、 不确定、可能、也许、?、TODO、TBD、再看看、之后再说”等决策信号。
3. 多个来源对同一事实表达冲突。
4. 准备进入可选能力分支，例如可行性分析、竞品调研或需求复述。

### 询问模板

> 当前处于 [分支 / 产物 X]，默认行为是 [Y]。
> 请选择：
> 1. 保持默认行为（Y）
> 2. 将 [产物 X] 纳入或排除出 `prd.md` §N
> 3. 延后到下一阶段决定
> 4. 取消该分支

### 主干与分支

| 分类 | 定义 | PRD 处理 |
|---|---|---|
| **主干** | 当前档位启用的主链工作项；L2 为 13 项完整链 | 必填；写入对应的确定性 PRD 章节，无需询问 |
| **分支 / 可选能力** | 共享机制及按需支持能力，如澄清、变更管理、决策记录、入口路由、人工闸门、审计、追溯、竞品、可行性、埋点、复述、头脑风暴 | 进入时询问；按产物默认归宿与人工选择处理 |

> `issue-record` 是 L1/L2 的常驻治理产物，不走可选询问；L0 不创建独立清单，未决事项写入 mini-PRD §6。它只能记录 PM/PRD 过程中的澄清、冲突、风险、待决和范围问题，不记录仓库缺陷、测试失败、部署问题或工程实施任务。

### 默认归宿

| 产物或机制 | 默认 PRD 归宿 | 询问 / 处理 |
|---|---|---|
| 当前档位主干产物 | 对应固定章节 | 必填，无需询问 |
| `tracking-plan` | 可选 §5.2 埋点 | Skill 入口与 PRD 汇总时询问；接受后保留原事件表 |
| `requirement-restate` | 默认不进正文 | 入口询问；可在 §0 附 RR-XXX 来源说明 |
| `brainstorming` | 默认不进正文 | 入口询问；仅 `include` 候选汇总到输入包 |
| `issue-record` | 默认不进正文 | L1/L2 强制生成；仅作为治理与沟通记录 |
| `competitive-research`、`feasibility-analysis` | 可选支持证据 | 入口询问；可附在 §0 或附录 |
| `clarify`、`change-management`、`intake-routing`、`project-init`、`human-gate` | 不作为 PRD 产物 | 分别服务澄清、回流、路由、初始化或治理 |
| `decision-log` | 可选 §11 决定说明 | 入口询问；可汇总 DEC-XXX |
| `audit`、`traceability` | 运行时质量证据 | 审计产出 §10 一致性发现；追溯约束 PRD 对应章节 |

> “审计”有两个不可混淆的含义：共享审计机制由 `consistency_check`、`dor_check`、`traceability_check` 检查实时产物并输出发现；`audit_log` 与 `projection_cache` 则是记录 review、change、confirm、reflow 事件的基础设施。

## L1/L2 问题清单与阶段收口

`issue-record` 是 L1/L2 与业务方沟通和澄清需求的正式载体。每个 L1/L2 案例都必须创建 `99-review/support/issue-record.md`，即使没有开放问题；空清单本身也是审计证据。其格式必须符合 `src/shared/clarify/skills/issue-record/assets/issue-record-template.md`。`pipeline` 的机器闸门会验证此文件；缺失或校验失败即阻断送审。AI 发现 BLK、RSK、DEC、INF、CLS 或 OUT 时应即时登记，送审前确保 §13 阶段收口表包含当前工作项。

## 入口业务探索

进入当前档位首个主干工作项之前，由 `pipeline.py entry` 输出以下机器信号：

1. 检查 `00-input/` 中的问题陈述、受影响角色、约束、产品级方案、功能清单、业务规则六类信号，评估材料成熟度 L0-L4；材料不足时输出 `entry_blocked`。
2. 仅一行想法或材料稀疏时，使用 `brainstorming` 生成候选，由人工作 `include/exclude/defer/research` 处置；只有 `include` 候选进入输入包。
3. 多源材料或存在歧义时，使用 `requirement-restate`；冲突路由到问题清单，未知项保留问题 ID 与负责人。
4. L1/L2 从 `project-background-goal` 开始，且其送审前必须至少有一项 SRC 来源材料；L0 从 `mini-prd` 开始。

## B3 阶段收口

L1/L2 每个工作项进入 `ready_for_human_review` 前，`99-review/support/issue-record.md` 必须通过结构校验，且 §13 收口表必须包含该工作项的一行；即使问题数为 0 也必须记录。正文所有“待确认”表述必须在同一行给出 Q-/ISS-/DEC-/SRC- 引用。L0 不要求问题清单或 B3，但仍要求 mini-PRD、一次真实人工确认、`ReviewRecord`、哈希锚点和审计事件。

伴随信号不会自动改变状态：同一项连续 3 次变更提示熔断；开放问题 7 天提示、14 天升级；页面设计或交互规则确认后，上游重审提示进入变更管理。
