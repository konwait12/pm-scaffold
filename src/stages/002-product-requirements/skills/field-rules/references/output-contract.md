# Output Contract · 字段规则产物

## 产物标识

- **文件路径**：`002-product-requirements/09-field-rules/field-rules.md`
- **ID 前缀**：`F-`（字段 ID，如 `F-001`、`F-002`）
- **状态**：`draft` / `needs_user_input` / `conditional_review` / `ready_for_human_review`（**绝不 `confirmed`**）

## 主干章节契约

```yaml
required_sections:
  - id: §1
    title: 字段清单总览
    must_contain: [field_count, required_count, optional_count, system_generated_count, baseline_version]
  - id: §2
    title: 字段定义表
    must_contain: [F-XXX, field_name_cn, field_name_en, db_field_name, type, length_or_range, required, default, uniqueness, source, related_vl]
  - id: §3
    title: 字段来源说明
    must_contain: [F-XXX, business_meaning, upstream_skill, source_skill]
  - id: §4
    title: 字段与校验（VL）反向绑定
    must_contain: [VL-XXX, validates_fields, validation_type, error_message]

validation:
  - §2 每个字段必须有 F-XXX ID + 全部 10 列内容
  - §4 每个 VL-XXX 必须指向至少一个 F-XXX 字段（反向绑定）
  - 字段增 / 删 / 改名 → §1 baseline_version 必须升级
  - VL-XXX 不存在时 §2 关联校验 VL 列填 "TBD-VL" + 在 §4 留 placeholder
```

## 与下游关系

- `validation-rules` 引用本 skill 的 F-XXX 作为校验对象——VL 行的 `validates_fields` 字段指向 `F-XXX`
- `prd-assembly` 投影本 skill 全部到 prd.md §8.2 字段清单

## 与上游关系

- `feature-list` / `functional-flow` / `page-design` / `interaction-rules` / `business-rules` 是上游
- 字段必须能从上游证据追溯；不可凭空增加

## 与 PRD 章节映射

`artifact_types` 中 `field-rules.prd_destination` 是「§8.2 字段清单（名称 / 类型 / 长度 / 必填 / 默认值 / 唯一性 / 来源 / 关联校验 VL）」——这是 prd.md §8.2 的唯一上游。

`artifact_types` 中 `validation-rules.prd_destination` 由 "§8.2 字段定义表 + §8.3 字段校验" 改为 "§8.3 字段校验"（已与 §8.2 分离）。

## 字段增删改回流机制

1. 上游 / 下游任一 work item 发现字段需调整 → 在 `99-review/support/reflow.md` 记录
2. 本 skill 重做 → §1 baseline_version 升级
3. validation-rules 同步回流（因为字段改了校验对象也跟着改）
4. 全部下游 rebi