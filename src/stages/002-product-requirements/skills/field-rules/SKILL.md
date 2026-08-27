---
name: field-rules
description: L2 only 主干。从 VL 拆出，**专门产出字段定义表 F-XXX（名称/类型/长度/必填/默认值/唯一性/来源/关联校验 VL）**。**PRD §8.2 字段清单** 的唯一上游——与 §8.3 字段校验（VL）分离。L1 不启用。
---

# 字段规则说明（Field Rules · L2 主干）

## 目的与边界

本 skill **专门产出字段定义表**——业务字段的结构化描述：

| 维度 | 说明 |
|---|---|
| F-XXX ID | 字段唯一标识 |
| 字段名 | 中文 + 英文 + 数据库字段名 |
| 类型 | string / int / float / bool / date / datetime / enum / array / object |
| 长度 / 范围 | 字符上限 / 数值区间 / 枚举值 |
| 必填 | 是 / 否 / 条件必填 |
| 默认值 | 默认值或生成规则（auto_increment / uuid / now()） |
| 唯一性 | 全局唯一 / 范围内唯一 / 不唯一 |
| 来源 | 业务方填写 / 系统生成 / 第三方同步 |
| 关联校验 VL | 引用校验规则 ID（VL-XXX）— 与 FIELDS 互引 |

**它不写校验规则**（那是 VL 的职责）——只写字段的结构化定义。校验规则由 VL 引用 F-XXX 反向绑定。

**L2 主干定位**：order=9（在 BR order=8 之后、VL order=10 之前）。L1 不启用（L1 不产字段定义表，VL 的"字段定义表"section 已删除）。

**PRD §8.2 字段清单 的唯一上游**——之前 §8.2 由 VL "§2 字段定义表"隐式提供，**现已分离**。VL 只产 §8.3 字段校验。

## 输入与输出

**输入**：上游已确认的 `feature-list` + `functional-flow` + `business-rules` + `page-design`（UI 收集了哪些字段）+ `interaction-rules`（哪些字段在哪个交互点填写）。

**输出**：单一 `field-rules.md`（`002-product-requirements/09-field-rules/field-rules.md`），使用 `src/templates/stage-2-product/field-rules.md` 模板。

产物标识：所有字段 ID 以 `F-` 前缀（如 `F-001`、`F-002`）；每个字段独占一行。

## 思考提示（按阶段）

按 8 步循环：**Preflight → Intake → Think → Clarify → Generate → Audit → Human Gate → Commit**。

### 1. Preflight（预检）
- "上游 feature-list / functional-flow / page-design / interaction-rules 是否已 confirmed？"
- "哪些 UI 表单 / API 入参需要字段定义？"
- "是否有字段已被废弃 / 改名？"

### 2. Intake（输入）
- 收集三类字段线索：
  - **来自 FE**：功能点对应的字段
  - **来自 FF**：流程中传递的数据
  - **来自 PD**：页面表单 / 列表字段
  - **来自 BR**：业务规则定义的派生字段

### 3. Think（思考；应用透镜）
- **First Principles**：本期 PRD 必须定义的字段是哪些？没有这些字段业务能否跑通？
- **Adversarial**：哪些看起来必要的字段其实是冗余 / 可派生？
- **Reverse Validation**：每个字段被什么校验 / 业务规则引用？被引用次数 = 0 的字段可考虑删除。

### 4. Clarify（澄清）
- 当字段定义有歧义时（"长度上限" / "必填规则"），停下询问业务方。
- ≤5 个问题/会话，按影响排序。

### 5. Generate（生成）
- **逐字段**：F-XXX / 名称 / 类型 / 长度 / 必填 / 默认 / 唯一性 / 来源 / 关联校验 VL
- 知识状态：每个字段标 F/D/A/AI/U
- **关联校验 VL 列**：指向 VL-XXX（VL 产物中校验规则 ID）；如尚未产出 VL，先留空 + 注明 "TBD-VL"

### 6. Audit（审计）
- **字段完整性**：每个 FE/FF 中提到的字段是否都有 F-XXX 行
- **类型一致性**：相同语义的字段是否类型一致（如 `user_id` 全局 int）
- **命名一致性**：英文字段名是否 snake_case 统一
- **未引用字段**：被引用次数 = 0 的字段标"删除候选"

### 7. Human Gate（人工关卡）
- 业务方拍板："这些字段就是本期全部字段？"
- 业务方确认："必填规则正确？"
- 业务方确认："默认值合理？"

### 8. Commit / Reflow（提交 / 回流）
- 只有 `pipeline.py review --decision approve` 才能写入 `confirmed`。
- 字段增删改 → 必须回流到本 skill 重做；VL 也要同步回流。

## 反模式

| ❌ 不要 | ✅ 要做 |
|---|---|
| 字段定义表写在 VL 末尾"顺手带一笔" | 字段定义表独立 work item，专门 §8.2 章节 |
| 字段名中文 + 英文混用，无统一规则 | 中文名 / 英文名 / DB 名 三列分明 |
| 字段类型模糊（"文本"/"数字"） | 类型用 string / int / float / bool / date / datetime / enum |
| 不标关联校验 VL | 每个字段必须指向 VL-XXX（或 TBD-VL） |
| 把校验规则写在字段定义行 | 字段行只写"关联校验 VL"列，校验在 VL 产物里 |

## 与下游关系

- `validation-rules` 引用本 skill 的 `F-XXX` 作为"校验对象"——VL-XXX 行指明"校验 F-XXX"
- `prd-assembly` 投影本 skill 到 prd.md §8.2 字段清单

## 与上游关系

- `feature-list` / `functional-flow` / `page-design` / `interaction-rules` / `business-rules` 是上游
- VL（校验规则）平行工作项，与 FIELDS 互相引用

## 加载参考文献

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/field-types.md` | 字段类型枚举 + 长度规范 | Intake / Generate 时 |
| `references/naming-conventions.md` | 命名规范（snake_case / camelCase / 中文名） | Generate 时 |

## 完成标准

每行字段必须有 F-XXX ID + 名称 + 类型 + 长度/范围 + 必填 + 默认值 + 唯一性 + 来源 + 关联校验 VL；上游 FE/FF/PD/IX 中提到的字段全部有 F-XXX 映射；命名统一（DB 字段 snake_case）；VL 反向引用完成。字段增删改回流机制写入 99-review 记录。

---

> 本 skill 在 `workflow-registry.json` 中 `id: field-rules`、`order: 9`、`tiers: ["L2"]`、`artifact_dir: 002-product-requirements/09-field-rules`。