---
name: field-rules
work_item: field-rules
artifact_type: field-rules
process_tier: L2
status: draft
created_at:
updated_at:
confirmed_at:
artifact_id: FIELDS-DRAFT-001
---

# 字段规则说明（Field Rules）

> 本 skill 是 PRD §8.2 字段清单的唯一上游。
> 与 VL（§8.3 字段校验）分离：字段结构化定义在本表；校验规则在 VL。
> L1 不启用本 skill。

---

## §1 字段清单总览

| 字段 | 值 |
|---|---|
| 字段总数 | 0 |
| 必填字段数 | 0 |
| 可选字段数 | 0 |
| 系统生成字段数 | 0 |
| baseline_version | v0.1.0 |

> 字段增 / 删 / 改名 → baseline_version 必须升级。

---

## §2 字段定义表

| F-ID | 中文名 | 英文名 | DB 字段名 | 类型 | 长度/范围 | 必填 | 默认值 | 唯一性 | 来源 | 关联校验 VL |
|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | （示例：用户名） | username | user_name | string | 1-64 字符 | 是 | — | 范围内唯一 | 用户填写 | VL-001 |
| F-002 | （示例：邮箱） | email | email | string | ≤ 128 字符 / 正则 | 是 | — | 全局唯一 | 用户填写 | VL-002, VL-003 |
| F-003 | （示例：创建时间） | created_at | created_at | datetime | ISO 8601 | — | now() | — | 系统生成 | — |

### 字段类型枚举

- `string`：字符串
- `int`：整数
- `float`：浮点数
- `bool`：布尔
- `date`：日期（YYYY-MM-DD）
- `datetime`：日期时间（ISO 8601）
- `enum`：枚举（值在长度/范围列写明）
- `array`：数组（元素类型在长度/范围列写明）
- `object`：嵌套对象（schema 在长度/范围列写明）

### 必填规则三态

- `是`：任意场景必填
- `否`：可选
- `条件必填`：填写时必须有值（如选了"企业"则"企业名"必填）

### 唯一性三态

- `全局唯一`：全表唯一
- `范围内唯一`：在某字段值相同范围内唯一（如同一订单号下）
- `不唯一`：可重复

### 来源四态

- `用户填写`：业务方在 UI 上手动填写
- `系统生成`：代码层生成（如 uuid / now() / auto_increment）
- `第三方同步`：从外部数据源拉取
- `派生计算`：由其他字段派生（如总价 = 单价 × 数量）

---

## §3 字段来源说明

| F-ID | 业务含义 | 上游来源 skill | 引用证据 |
|---|---|---|---|
| F-001 | 用户登录账号 | page-design（注册表单） + interaction-rules（注册流程） | PD-XXX / IX-XXX |
| F-002 | 用户联系邮箱 | page-design（注册表单） | PD-XXX |
| F-003 | 记录创建时间 | feature-list（用户管理） | FE-XXX |

> 每个字段必须能从上游证据追溯；无上游证据的字段标"删除候选"。

---

## §4 字段与校验（VL）反向绑定

| VL-ID | 校验的字段 | 校验类型 | 失败提示 |
|---|---|---|---|
| VL-001 | F-001 | 长度 / 非空 | 用户名 1-64 字符 |
| VL-002 | F-002 | 正则 / 非空 | 请输入有效邮箱 |
| VL-003 | F-002 | 唯一性 | 该邮箱已注册 |
| | | | |

> 反向绑定：VL 行指明它校验哪些 F-XXX 字段。
> 当字段定义调整时（§2 改），VL 必须同步回流。

---

## 附录 A · 字段增删改回流日志

| 时间 | 变更类型 | 变更描述 | 触发 work item | baseline_version |
|---|---|---|---|---|
| | | | | |

> 任何字段调整触发本 skill 重做时，记录并升级 baseline_version。