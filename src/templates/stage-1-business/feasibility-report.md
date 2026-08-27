---
name: feasibility-report
work_item: feasibility-analysis
artifact_type: feasibility-report
process_tier: L1|L2
status: draft
created_at:
updated_at:
confirmed_at:
artifact_id: FA-DRAFT-001
---

# 可行性分析报告（Feasibility Analysis）

> 立项首项 · L1/L2 主干 · 必须在 `project-background-goal` 之前完成。
> AI 推荐 + 置信度；最终决策由人类决策人拍板；本 skill 不会自动做最终决策。
> 立项不通过 → 整个 REQ 终止，回流到需求池。

---

## §1 结论摘要

| 字段 | 值 |
|---|---|
| decision | ☐ go · ☐ no_go · ☐ conditional_go |
| ai_recommendation | ☐ go · ☐ no_go · ☐ conditional_go |
| ai_confidence | HIGH / MEDIUM / LOW |
| decision_owner | （决策人姓名 + 角色） |
| decision_date | （YYYY-MM-DD） |
| 关键假设列表 | 3-5 条命中假设（见 §6） |

> 立项决策三态：go / no_go / conditional_go。
> no_go → REQ 终止；conditional_go → 条件作为 BG 的前置约束。
> AI 永不伪造人工确认——decision_owner 由真实人填写。

---

## §2 市场空间（Market Sizing）

| 指标 | 数据 | 来源 / 知识状态 |
|---|---|---|
| target_users | （目标用户规模） | SRC-XXX（FACT/AI_INFERENCE） |
| market_size_estimate | TAM / SAM / SOM | SRC-XXX |
| source_refs | （公开报告 / 内部数据 / 二手研报） | （来源等级） |

> 每个数字必须可溯源：FACT（有可查来源）/ AI_INFERENCE（AI 估算）/ ASSUMPTION（业务方假设）/ UNKNOWN（未知）。

---

## §3 技术可行性（Technical Feasibility）

| 技术挑战 | 验证状态 | 验证方式 | 负责人 |
|---|---|---|---|
| （挑战 1） | 已验证 / 待验证 / 不可行 | （POC / Demo / 第三方 SDK / 内部能力） | （团队 / 角色） |
| （挑战 2） | | | |

> "不可行" 立即触发 no_go 决策；"待验证" 需在 conditional_go 中给出验证截止日。

---

## §4 投入产出（Cost & Revenue）

| 项目 | 金额 / 时间 | 说明 | 知识状态 |
|---|---|---|---|
| 研发成本 | （人月 / 元） | （拆解 / 区间） | AI_INFERENCE / ASSUMPTION |
| 运维成本 | （人月 / 元 / 年） | | |
| 预期收益 | （元 / 年） | （收益来源） | |
| 回本周期 | （月） | | |

> 投入产出数字必须标 AI_INFERENCE 或 ASSUMPTION + 责任人 + SRC-*。**绝不**当 FACT 写死。

---

## §5 风险评估（Risk Assessment）

| 风险 | 影响（高/中/低） | 概率（高/中/低） | 缓解措施 |
|---|---|---|---|
| 合规风险 | | | |
| 数据安全风险 | | | |
| 资金风险 | | | |
| 隐私风险 | | | |
| 技术风险 | | | |
| 市场风险 | | | |

> 风险姿态的四个轴（合规 / 数据安全 / 资金 / 隐私）必须每个填；强度传导到 `project-scope` §8 风险姿态。

---

## §6 多方案取舍（仅当存在 ≥2 个实质方案时启用）

> 触发条件：同一目标存在 ≥2 个**实质不同**的方案（自研 vs 外购、不同技术路径、不同范围取舍）。
> 不触发时整节删除；触发时使用 `src/templates/support/solution-comparison.md` 作为章节结构。

### §6.1 候选方案（等深）

| 维度 | 方案 A | 方案 B | 方案 C |
|---|---|---|---|
| 概述 | | | |
| 投入产出 | | | |
| 技术风险 | | | |
| 合规风险 | | | |
| 时间窗口 | | | |

### §6.2 加权决策矩阵（权重先于打分定义）

| 维度 | 权重（先定） | 方案 A 得分 | 方案 B 得分 | 方案 C 得分 |
|---|---|---|---|---|
| 合规 | 0.X | | | |
| 投入产出 | 0.X | | | |
| 时间窗口 | 0.X | | | |
| 长期演进 | 0.X | | | |
| **加权得分** | 1.0 | **Σ** | **Σ** | **Σ** |

> 锚定检查：权重必须在打分前定义。打分后才定权重 = 反模式 = 重做。

### §6.3 敏感度分析

| 假设变化 | 推荐是否翻转？ | 翻转条件 |
|---|---|---|
| 合规权重 ±0.1 | | |
| 投入产出权重 ±0.1 | | |
| 时间窗口权重 ±0.1 | | |

> 必须识别哪个假设变化会翻转推荐；不识别 = 反模式。

### §6.4 推荐与决策

**AI 推荐**：方案 X（加权得分最高 + 关键假设满足）  
**AI 置信度**：HIGH / MEDIUM / LOW  
**关键假设**：3-5 条命中假设  
**人类决策**：方案 ______（决策人填写）

---

## §7 附录：来源与未决项

### §7.1 来源登记

| SRC-ID | 来源 | 类型 | 知识状态 | 引用处 |
|---|---|---|---|---|
| SRC-001 | （文件名 / 链接） | 内部文档 / 外部报告 / 访谈纪要 | FACT / AI_INFERENCE | §X |

### §7.2 未决问题

| Q-ID | 问题 | 影响哪一节 | 阻塞？ |
|---|---|---|---|
| Q-001 | （待业务方澄清） | §X | 是 / 否 |

### §7.3 冲突日志

| 冲突项 | 说法 A | 说法 B | 处理 |
|---|---|---|---|
| （待澄清） | | | |

---

## §8 DecisionRecord

```yaml
- id: DEC-XXX
  decision: go | no_go | conditional_go
  decided_by: （决策人姓名 + 角色）
  decided_at: （YYYY-MM-DD）
  basis: §1 摘要 + §6 推荐 + 关键假设列表
  conditions: （conditional_go 时填）
  recorded_by: （记录人）
  evidence_refs: [SRC-XXX, ...]
```

> DecisionRecord 是事实记录，不是审批。**AI 永不写 DECISION 的 confirmed 字段**——只有 `pipeline.py review --decision approve`（真实人）才能生效。