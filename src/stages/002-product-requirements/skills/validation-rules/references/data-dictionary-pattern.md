# 数据字典技法参考（Data Dictionary Pattern）

> 来源吸收：Trae `prd-generator` skill 的「数据字典模板 + 字段类型枚举 + 状态字段枚举」，作为 validation-rules 的可选落地能力。
> 定位：validation-rules 产出的 VL-XXX 字段定义文本是权威；本文档提供"把字段定义统一为数据字典格式"的技法，增强类型与状态枚举的一致性。
> 触发：当 VL-XXX 字段数量多、含状态枚举或需跨功能复用字段定义时使用。**按需加载，不设全局闸门**。

## 1. 输入映射（pm-scaffold 语境）

| 外部 skill 输入 | pm-scaffold 对应产物 | 说明 |
|---|---|---|
| 字段定义 | validation-rules 的 VL-XXX | 数据字典条目来源 |
| 状态字段 | state-machine 的 STATE-XXX | 状态枚举对齐 |
| 业务规则 | business-rules 的 BR-XXX | 字段校验规则来源 |
| 核心字段 | functional-flow 五要素 | 字段所属功能 |

> **上游未 confirmed，不启动字典编纂**：以 VL-XXX 已确认字段为准；缺失标 `待确认`。

## 2. 数据字典模板（吸收自 prd-generator）

| 字段名 | 字段中文名 | 数据类型 | 取值范围 | 是否必填 | 备注说明 |
|--------|------------|----------|----------|----------|----------|
| field_name | 字段中文名 | VARCHAR(100) | 任意字符串 | 是/否 | 字段说明（追溯 VL-XXX） |
| status | 状态 | ENUM | PENDING/PROCESSING/COMPLETED/ERROR | 是 | 状态流转（追溯 STATE-XXX） |
| amount | 金额 | DECIMAL(10,2) | 0.00-99999999.99 | 是 | 金额精度（to B） |

## 3. 字段类型枚举（吸收自 prd-generator）

- **STRING/VARCHAR**：字符串（VARCHAR(n) 标注最大长度）
- **INT/BIGINT**：整数
- **DECIMAL**：小数（金额须用 DECIMAL(p,s) 标注精度，不用 FLOAT）
- **BOOLEAN**：布尔
- **DATETIME**：日期时间
- **JSON**：对象/数组
- **UUID**：唯一标识
- **ENUM**：枚举（状态字段须列出所有枚举值）

## 4. 状态字段枚举（对齐 STATE-XXX，吸收自 prd-generator + to B 扩展）

| 枚举值 | 含义 | to B 场景 |
|---|---|---|
| PENDING | 待处理 | — |
| PROCESSING | 处理中 | — |
| COMPLETED | 已完成 | — |
| ERROR/FAILED | 错误/失败 | — |
| ACTIVE | 活跃 | 账户/权限状态 |
| INACTIVE | 未激活 | 账户/权限状态 |
| APPROVED | 已审批 | 审批流（to B） |
| REJECTED | 已驳回 | 审批流（to B） |
| ARCHIVED | 已归档 | 终态（to B） |

## 5. 工作流程

1. **汇总字段**：从所有 VL-XXX 提取字段，去重合并。
2. **定类型**：按 §3 类型枚举标注；to B 金额用 DECIMAL 标精度，权限状态用 ENUM。
3. **挂数举**：状态字段按 §4 列出值序列，与 state-machine 的 STATE-XXX 一致；不一致标 `CONFLICT`。
4. **挂校验**：每字段校验规则追溯 BR-XXX；缺失标 `待确认`。
5. **输出字典表**：在 validation-rules 产物附录呈现，跨功能复用。

## 6. 核心硬规则

1. **类型不臆断**：字段类型以 VL-XXX 为准；未定义类型标 `待确认`，不自行猜类型。
2. **状态枚举一致**：状态字段的值序列必须与 STATE-XXX 完全一致；不一致即 `CONFLICT` 交人工。
3. **校验不空挂**：每字段校验追溯 BR-XXX；无规则标 `待确认`。
4. **to B 金额精度**：金额字段必须用 DECIMAL 并标注精度（如 DECIMAL(10,2)），不用 FLOAT；涉及对账须标注精度一致。
5. **VARCHAR 标长度**：字符串字段标注 VARCHAR(n) 最大长度，不留无限长。
6. **枚举列全值**：ENUM 字段必须列出所有枚举值，不写"等"省略。

## 7. 边界（Do Not）

- 不设计数据库表结构/索引/外键（超出 PRD-only）。
- 不替代 VL-XXX 文本——字典是聚合视图，VL-XXX 是权威。
- 不替业务方决定状态值——以 STATE-XXX 为准。
- 不把字段塞入功能流程文本（属五要素）。

## 8. 质量自检清单

- [ ] 每字段类型对齐 §3 类型枚举，无臆断
- [ ] VARCHAR 标注最大长度
- [ ] 状态字段值序列与 STATE-XXX 一致（无 CONFLICT），枚举列全值
- [ ] 每字段校验追溯 BR-XXX
- [ ] 金额字段用 DECIMAL 并标注精度（to B）
- [ ] 字段去重，跨功能复用
- [ ] 无数据库表结构/索引/外键越界内容
