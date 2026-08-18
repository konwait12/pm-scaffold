# 价值复杂度矩阵技法参考（Value Complexity Matrix）

> 来源吸收：Trae `prd-writing-expert` skill 的「问题陈述 + 用户故事 + MoSCoW 优先级 + 价值复杂度矩阵 + 北极星指标 + Key Results」，作为 project-background-goal 的可选落地能力。
> 定位：project-background-goal 产出的 BG-XXX 目标文本是权威；本文档提供"用价值×复杂度四象限辅助需求优先级 + 定义北极星指标体系"的技法，增强目标与范围的关联。
> 触发：当需对功能/故事排优先级、或需定义北极星指标与 Key Results 时使用。**按需加载，不设全局闸门**。

## 1. 输入映射（pm-scaffold 语境）

| 外部 skill 输入 | pm-scaffold 对应产物 | 说明 |
|---|---|---|
| 目标 | project-background-goal 的 BG-XXX | 北极星指标依据 |
| 故事 | user-stories 的 ST-XXX | 矩阵条目 |
| 功能 | feature-list 的 FEA-XXX | 矩阵条目 |
| 范围基线 | user-stories 的 In/Out/Deferred | 优先级判定 |
| 痛点 | user-journey 的 UJ-XXX | 价值评估依据 |

## 2. 优先级方法：MoSCoW（吸收自 prd-writing-expert）

| 优先级 | 含义 | 范围基线 |
|---|---|---|
| Must | 必须有，无则产品不成立 | In |
| Should | 应该有，重要但非阻断 | In |
| Could | 可以有，时间/资源允许时 | Deferred（Conditional） |
| Won't | 本期不做 | Out |

## 3. 价值复杂度四象限（吸收自 prd-writing-expert）

|  | 低复杂度 | 高复杂度 |
|---|---|---|
| **高价值** | Quick Win（先做，Must） | Big Bet（重点投入/分阶段，Must/Should） |
| **低价值** | Maybe Later（Could/Deferred） | Time Sink（Won't/Out） |

每条 ST-XXX / FEA-XXX 落入一象限，附判定理由（追溯 BG-XXX 痛点/目标）。

## 4. 北极星指标体系（吸收自 prd-writing-expert）

| 要素 | 内容 | to B 示例 |
|---|---|---|
| 北极星指标 | 唯一核心指标 | 核心流程完成率 / 审批时效 |
| Key Results | 量化 KR（2-4 条） | 审批时效从 48h 降至 4h；流程完成率 ≥95% |
| 监控指标 | 过程监控指标 | 各环节停留时长、异常率 |

北极星指标必须可量化、可追溯 BG-XXX 目标；只定一个，多个并列须人工裁决取一。

## 5. 工作流程

1. **定北极星**：从 BG-XXX 目标推导唯一北极星指标 + 2-4 条量化 KR。
2. **评价值/复杂度**：对每 ST-XXX/FEA-XXX 评价值（对北极星贡献）与复杂度（实现/依赖成本）。
3. **落象限**：每条落入 §3 四象限，附理由；Quick Win 先做，Time Sink Out。
4. **标 MoSCoW**：按 §2 标 Must/Should/Could/Won't，关联 In/Out/Deferred。
5. **挂范围**：象限+MoSCoW 结果关联范围基线。

## 6. 核心硬规则

1. **北极星唯一**：只定一个核心指标，不列一堆并列指标；多个并列须人工裁决取一。
2. **量化必填**：北极星与 KR 必须有具体数值（如 48h→4h、≥95%）；无数值标 `待确认`，不模糊表述。
3. **象限有理由**：每条落象限附判定理由，追溯 BG-XXX/ST-XXX 痛点。
4. **to B 价值维度**：价值评估须含业务效率/合规风险/成本节约，不只看用户量；to B 北极星常为效率/时效/合规类指标。
5. **MoSCoW 与范围一致**：Must=In、Won't=Out、Could=Deferred，不矛盾；矛盾标 `CONFLICT`。

## 7. 边界（Do Not）

- 不替业务方定北极星——AI 推断交人工裁决，标 `AI_INFERENCE`。
- 不替代 BG-XXX/user-stories 文本——矩阵是辅助视图。
- 不展开运营推广/用户增长活动（超出 PRD-only）。
- 不列多个并列北极星。

## 8. 质量自检清单

- [ ] 北极星唯一且有具体数值
- [ ] KR 2-4 条且可量化，追溯 BG-XXX
- [ ] 每条 ST-XXX/FEA-XXX 落象限并附理由
- [ ] MoSCoW 与范围基线一致（Must=In/Won't=Out/Could=Deferred）
- [ ] 价值评估含业务效率/合规/成本（to B）
- [ ] 无运营推广越界内容
