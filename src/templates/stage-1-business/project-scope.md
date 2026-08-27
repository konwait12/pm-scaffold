---
name: project-scope
work_item: project-scope
artifact_type: project-scope
process_tier: L1|L2
status: draft
created_at:
updated_at:
confirmed_at:
artifact_id: SCOPE-DRAFT-001
---

# 项目范围（Project Scope）

> 本 skill 是 PRD §2 项目范围的唯一上游。
> 输入：可行性分析（FA）+ 业务背景与目标（BG）。
> 输出：四态范围基线 + 假设 + 依赖 + 风险姿态。

---

## §1 结论摘要

| 字段 | 值 |
|---|---|
| scope_baseline_version | v0.1.0 |
| In 项数 | 0 |
| Out 项数 | 0 |
| Deferred 项数 | 0 |
| Conditional 项数 | 0 |
| baseline_owner | （待业务负责人拍板） |
| baseline_date | （YYYY-MM-DD） |

> 任何 In/Out/Deferred/Conditional 增删后，scope_baseline_version 必须升级。

---

## §2 In Scope（本期做）

| scope_id | 名称 | 描述 | 成功标志 | 优先级 |
|---|---|---|---|---|
| SCOPE-IN-001 | （示例：核心下单流程） | （可被本期 PRD 验证实现的业务能力） | （可观测的完成信号） | P0/P1/P2 |

> §2 是本期 PRD 的**必含范围**。每行必须有 scope_id；改 / 增 / 删 → 回流本 skill 重做。

---

## §3 Out of Scope（本期不做）

| scope_id | 名称 | 不做的理由 | 预计再评估时机 |
|---|---|---|---|
| SCOPE-OUT-001 | （示例：跨境支付） | （合规/资源/依赖等具体原因） | （下一版本窗口或触发条件） |

> §3 是本期 PRD 的**显式排除**。每行必须有理由；"AI 漏掉"不是理由。

---

## §4 Deferred（暂缓）

| scope_id | 名称 | 暂缓理由 | 扩展点设计 |
|---|---|---|---|
| SCOPE-DEF-001 | （示例：会员体系二期） | （本期不实现的合理原因） | （代码层 / 数据层留口） |

> §4 是本期不实现但**保留扩展点**的能力。

---

## §5 Conditional（条件性）

| scope_id | 名称 | 触发条件 | Owner | 升级规则 |
|---|---|---|---|---|
| SCOPE-COND-001 | （示例：医保对接） | （用户量达标 / 合规要求变化 / 依赖上线） | （部门 / 角色） | （满足后回流 SCOPE 改 In 或 Out） |

> §5 是**当条件满足时纳入**的能力。无任何条件项时显式声明"本期无 Conditional 项"。

---

## §6 假设清单

| 假设 ID | 内容 | 知识状态 | 可证伪测试 | Owner |
|---|---|---|---|---|
| SCOPE-ASM-001 | （示例：日活 ≥ X 才上 C 方案） | AI_INFERENCE | （测什么能推翻它） | （部门 / 角色） |

> 知识状态标签：`FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`。
> 每条假设必须能被反驳 / 确认——可证伪性是底线。

---

## §7 依赖清单

| 依赖 ID | 名称 | 类型 | Owner | 计划落地日期 | 单点依赖 |
|---|---|---|---|---|---|
| SCOPE-DEP-001 | （示例：支付通道 X） | 外部 / 内部 / 跨产品线 | （部门 / 角色） | （YYYY-MM-DD） | ✅/❌ |

> 任何**关键依赖**必须有 Owner + 计划落地日期 + 单点标识。单点依赖需在 §8 风险姿态对应轴标 HIGH。

---

## §8 风险姿态

| 风险轴 | 强度 | 理由 | 缓解措施 |
|---|---|---|---|
| 合规 | HIGH/MEDIUM/LOW | （具体合规要求） | （本期如何管控） |
| 数据安全 | HIGH/MEDIUM/LOW | （数据敏感度） | （脱敏 / 加密 / 审计） |
| 资金 | HIGH/MEDIUM/LOW | （是否涉及资金流） | （对账 / 风控 / 限额） |
| 隐私 | HIGH/MEDIUM/LOW | （是否处理个人信息） | （最小化 / 同意 / 撤回） |

> 强度来源于上游 FA 的"风险姿态"章节；本 skill 在 §2 In / §7 依赖 与之对齐。

---

## 附录 A · 范围变更回流日志

| 时间 | 变更类型 | 变更描述 | 触发 work item | scope_baseline_version |
|---|---|---|---|---|
| | | | | |

> 任何后续 work item 触发范围调整时，必须在本表记录并升级 scope_baseline_version。