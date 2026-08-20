# 领域映射提示（Domain Mapping Hint）

> 来源吸收：`prd-to-ddd-design__skillhub` 的 Phase 1 `PRD Text → Domain Model Extraction Rules` 映射表与 Rule Classification，仅取「PRD 信号 → 领域候选」这一张表，作为 prd-assembly 下游交接的可选提示能力。
> 定位：在 prd.md 定稿后给研发一个进入领域思考的入口——把 PRD 里的名词/动词/约束信号映射成领域候选（Entity / VO / Event / Command / Invariant / Enum），帮助研发更快开始 DDD 建模。
> 触发：Human Gate 通过、向下游研发交接时，研发明确要开始领域建模/技术设计时；或附录中希望给出领域思考起点时。**按需加载，不设全局闸门。仅作提示，不做完整 DDD 设计。**

## 1. 输入映射

| 外部 skill 输入 | pm-scaffold 对应产物 | 说明 |
|---|---|---|
| PRD 文本（名词/动词/约束/枚举） | prd.md 正文（功能清单/业务规则/校验规则/状态变化） | 提取信号做候选映射 |
| 业务规则（BR-XXX） | prd.md §8 业务规则 | 「Must」类约束 → Invariant 候选 |
| 状态流转（STATE-XXX，兼容历史 SM-XXX） | prd.md §10 状态变化 | 状态迁移 → 领域事件候选 |
| 校验规则（VL-XXX） | prd.md §9 校验规则 | 封闭取值集 → Enum 候选 |

## 2. 核心映射表：PRD 信号 → 领域候选

| PRD Signal（信号） | Domain Candidate（领域候选） | 说明 |
|---|---|---|
| Nouns with unique identity / lifecycle（有唯一身份/生命周期的名词） | **Entity** | 如「订单」「客户」——有身份、会变状态 |
| Nouns defined purely by attributes（纯属性定义的名词，无身份） | **Value Object** | 如「地址」「金额」——不可变、按值比较 |
| Verbs / state transitions（动词/状态迁移） | **Domain Event or Command** | 如「下单」「审核通过」 |
| "Must", "should", "cannot", "only if"（约束类表述） | **Domain Rule / Invariant** | 业务不变量，必须始终成立 |
| Calculations, formulas（计算/公式） | **Domain Logic (method)** | 如「积分 = 金额 × 系数」 |
| Closed set of named values（封闭的命名取值集） | **Enum** | 如「订单状态：待支付/已支付/已取消」 |

## 3. 规则分类（约束信号落到哪）

| Type | Definition | Where to Enforce |
|---|---|---|
| **Invariant** | Must always hold（必须始终成立） | Inside entity/aggregate |
| **Precondition** | Must hold before operation（操作前必须成立） | Method entry check |
| **Policy** | Business rule that may vary（可变业务规则） | Strategy pattern |

> 映射提示里只标「这类规则可能是 Invariant / Precondition / Policy」，具体的落位由研发在 DDD 设计阶段决定。

## 4. 使用方式：交接提示块

在 prd.md 附录或下游交接材料中输出如下「领域映射提示」块（**可选**，文本规则仍权威）：

```markdown
## 领域映射提示（研发可选用）
> 以下为从 PRD 信号到领域候选的提示性映射，帮助研发进入 DDD 思考；不是设计结论，落地以研发的 DDD 设计文档为准。

| PRD 原文信号（节/ID） | 信号类型 | 领域候选 | 备注 |
|---|---|---|---|
| §8 业务规则 BR-003「订单必须包含至少一个商品行」 | Must 约束 | Invariant | 订单聚合的不变量候选 |
| §6 页面「客户档案」（有唯一身份/生命周期） | Noun | Entity（Customer） | 身份候选 |
| §10 状态变化 STATE-001「待支付 → 已支付」 | 状态迁移 | Domain Event（OrderPaid） | 事件命名建议 |
| §9 校验规则 VL-002「订单状态 ∈ {待支付,已支付,已取消}」 | 封闭取值集 | Enum（OrderStatus） | 枚举候选 |
| §5 功能流程「积分 = 实付金额 × 系数」 | 计算公式 | Domain Logic | 方法候选 |
| §8 业务规则 BR-007「金额」（纯属性、无身份） | Noun | Value Object（Money） | 值对象候选 |
```

## 5. 提示规则（避免滑入 DDD 设计）

- 每个映射只给**候选**，不给定论：不指定聚合根、不画 ER、不建表。
- 每个映射必须带 PRD 原文位置（节/ID），让研发能回查。
- 命名建议仅作参考（如 `OrderPaid`），最终命名由研发按项目约定定。
- 只覆盖本次 PRD 显式提到的信号，不做未提及的领域扩展。
- 该块**可选**：研发不需要时可不产出；文本规则始终是权威。

## 6. 与脚手架产物的对应

| 脚手架产物 | 对应 DDD 信号来源 |
|---|---|
| FEA-XXX（功能清单） | 名词/动词候选的索引 |
| BR-XXX（业务规则） | Invariant / Precondition / Policy 候选 |
| VL-XXX（校验规则） | Enum / 边界校验候选 |
| STATE-XXX（状态变化；兼容历史 SM-XXX） | Domain Event 候选 |
| FUN-XXX（功能流程；artifact 可为 FL-XXX） | Command / 领域逻辑候选 |

## 7. 工作流程

1. 确认研发确实要开始领域建模，才产出本提示块（否则跳过）。
2. 扫描 prd.md 显式信号：名词、动词/状态迁移、Must 约束、计算式、封闭取值集。
3. 按映射表逐条给出领域候选，每条带原文位置与备注。
4. 按规则分类标注约束信号的候选类型（Invariant / Precondition / Policy）。
5. 将提示块放入交接材料（附录或 Handoff），并声明「文本规则仍权威」。
6. 提示块内容不写回 prd.md 正文，不改变任何基线内容。

## 8. 核心硬规则

1. 只做提示性映射，不做完整 DDD 设计（无聚合/无 ER/无表结构）。
2. 每个候选必须带 PRD 原文位置，可回查。
3. 只映射 PRD 显式信号，不扩展未提及的领域。
4. 约束类信号标注候选类型（Invariant/Precondition/Policy），落位交研发。
5. 提示块可选且不进 prd.md 正文，文本规则始终权威。
6. 不产出接口定义、表字段、跨层契约等实现细节（那些是 PRD 之后的另一层工作）。

## 9. 边界（Do Not）

1. 不做 Event Storming / Bounded Context / Aggregate 设计——那是研发的 DDD 流程。
2. 不产出 ER 图、数据库表、接口契约、领域服务签名。
3. 不替研发决定聚合边界、仓储接口或跨上下文映射。
4. 不因「可能是个 Entity」就改写 PRD 正文措辞。
5. 不为凑提示块而虚构信号——稀疏时宁可少映射几行。
6. 不在 prd-assembly 内展开完整 DDD 输出，本提示块是唯一的领域出口。

## 10. 质量自检清单

- [ ] 提示块仅在研发需开始领域建模时产出，未成为默认产物
- [ ] 每条映射带 PRD 原文位置（节/ID），可回查
- [ ] 覆盖了名词/动词/状态迁移/Must 约束/计算式/封闭取值集六类信号
- [ ] 约束类信号已标注候选类型（Invariant/Precondition/Policy）
- [ ] 未产出 ER / 表结构 / 接口契约 / 聚合设计
- [ ] 提示块在交接材料中，未写回 prd.md 正文
- [ ] 已声明「文本规则仍权威，映射仅作提示」
- [ ] 未虚构信号，稀疏输入时映射行数相应减少
