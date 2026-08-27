# 字段决策清单技法参考（Field Decision Checklist）

> 本文将相关实践转化为本项目的可选方法，不引入外部运行时依赖。
> 定位：validation-rules 产出的 VL-XXX 字段定义文本是权威；本文档提供"把字段中非用户明示的细节显式化为决策清单，交人工拍板"的技法，确保 AI 推断可被人工裁决。
> 触发：当字段涉及状态、权限、枚举、多租户归属等非用户明示细节时使用。**按需加载，不设全局闸门**。

## 1. 输入映射（pm-scaffold 语境）

| 外部 skill 输入 | pm-scaffold 对应产物 | 说明 |
|---|---|---|
| 字段定义 | validation-rules 的 VL-XXX | 决策清单条目来源 |
| 状态字段 | state-machine 的 STATE-XXX | 状态决策依据 |
| 权限 | business-rules 的 RBAC 矩阵 | 权限决策依据 |
| 业务规则 | business-rules 的 BR-XXX | 校验决策依据 |
| 核心字段 | functional-flow 五要素 | 字段所属功能 |

> **上游未 confirmed，不启动决策清单**：以 VL-XXX 已确认字段为准；缺失标 `待确认`。

## 2. 决策清单结构

| 字段 | 决策点 | 来源类型 | AI 推断值 | 待人工拍板 | 追溯 |
|---|---|---|---|---|---|
| status | 状态值序列 | AI_INFERENCE | 未处置→处置中→已完成 | 是 | STATE-XXX |
| owner_id | 归属租户 | AI_INFERENCE | 单租户隔离 | 是 | BR-XXX |
| role | 权限枚举 | AI_INFERENCE | admin/manager/staff | 是 | RBAC |
| amount | 金额精度 | AI_INFERENCE | DECIMAL(10,2) | 是 | BR-XXX |

### 来源类型标注（对齐 contracts.md 6 标签）

| 标签 | 含义 | 处置 |
|---|---|---|
| FACT | 用户明示 | 直接采用 |
| DECISION | 已记录人工决策 | 采用 |
| ASSUMPTION | 假设 | 须验证 |
| AI_INFERENCE | AI 推断 | **须经人工拍板** |
| UNKNOWN | 未知 | 标 `待确认` 阻断 |
| CONFLICT | 冲突 | 须裁决 |

仅 FACT 与 DECISION 视为已确认；AI_INFERENCE 须经人工拍板。

## 3. 核心字段示例（吸收自 prd-development 告警功能）

- 告警 ID：告警唯一标识（FACT）
- 告警名称：恶意软件家族（FACT）
- 影响资产：触发告警的资产 IP（FACT）
- 告警状态：**未处置 → 处置中 → 已完成**（AI_INFERENCE，由管理员手动切换，追溯 STATE-XXX，待人工拍板状态值序列）
- 处置人：处置告警的角色（AI_INFERENCE，待人工拍板是否限于管理员）

## 4. 拍板工作流程

1. **扫字段**：从 VL-XXX 提取所有字段，标记每个字段的非用户明示细节（状态/权限/枚举/归属/精度/必填默认值）。
2. **标来源类型**：按 §2 来源类型 6 标签归类；非用户明示一律标 `AI_INFERENCE`。
3. **列决策点 + AI 推断值**：每个 AI_INFERENCE 字段列出 AI 推断值与待拍板项。
4. **交人工拍板**：AI 推断不得直接当事实写入 VL-XXX；标 `待确认` 交人工，拍板后转为 DECISION。
5. **回写**：拍板后的 DECISION 回写 VL-XXX；未拍板的保持 `待确认` 阻断产物 confirmed。

## 5. 核心硬规则

1. **AI 推断显式化**：任何非用户明示的字段细节（状态值/权限枚举/租户归属/金额精度/必填默认值）必须标 `AI_INFERENCE`，不得静默当事实写入。
2. **拍板后才确认**：AI_INFERENCE 须经人工拍板转为 DECISION；未拍板的标 `待确认`，阻断产物 confirmed。
3. **占位不编造**：信息不足用 `[待确认]` 占位（对应 UNKNOWN），不编造字段值。
4. **to B 归属显式**：租户归属、权限层级必须显式决策，不默认单租户/最高权限；金额精度须拍板（不用 FLOAT）。
5. **状态值序列拍板**：状态字段的值序列若为 AI 推断，须人工拍板并与 STATE-XXX 对齐；不一致即 `CONFLICT`。

## 6. 边界（Do Not）

- 不替业务方决定字段值——AI 推断交人工拍板，不静默写入。
- 不替代 VL-XXX 文本——清单是决策视图，VL-XXX 是权威。
- 不设计数据库列/索引/外键（超出 PRD-only）。
- 不把 AI_INFERENCE 当 FACT（违反 contracts.md 知识状态）。

## 7. 质量自检清单

- [ ] 每个非用户明示字段细节标 AI_INFERENCE，未静默当事实
- [ ] AI 推断值与待拍板项成对列出
- [ ] 未拍板项标 `待确认`，不阻断流程绕过
- [ ] 租户归属/权限层级/金额精度显式决策（to B）
- [ ] 状态值序列拍板并与 STATE-XXX 对齐，无 CONFLICT
- [ ] 与 contracts.md 6 标签一致，无新发明标签
