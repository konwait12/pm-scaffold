# 模板库接口

本目录只定义未来业务场景模板包的元数据与接入边界。现行产物模板以 `src/framework/workflow-registry.json` 和 `src/templates/stage-1-business/`、`stage-2-product/`、`stage-3-prd/` 为准。

## 现行解析顺序

`src/templates/resolver.py` 依次查找：需求级 `.templates/` 覆盖、preset、已确认 extensions、核心模板。模板包不能改变 work item、前置依赖、frontmatter 或人工确认规则。

## 模板包约束

- `manifest.json` 必须符合 `manifest.schema.json`，状态为 `confirmed` 且完成脱敏后才可参与自动选择。
- `maps_to` 只能指向当前 resolver 的 artifact 文件名，例如 `user-journey.md`、`feature-list.md`、`prd.md`；不得使用已删除的复合模板名。
- 每个新增模板必须补充 registry 契约检查、validator、正向与负向 fixture，并在 README/CHANGELOG 记录来源和版本。
- 自动分类器只能提供候选，不得静默替换核心模板；无人确认时回退核心模板。

## 文件

| 文件 | 用途 |
|---|---|
| `manifest.schema.json` | 模板包清单 schema |
| `classifier-interface.md` | 未来分类器的输入、输出和回退契约 |
