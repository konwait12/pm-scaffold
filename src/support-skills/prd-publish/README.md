# PRD Publish · PRD 发布

> **Support Skill** · 位于 `src/support-skills/prd-publish/`
> **执行时机**：PRD 通过 Human Gate 之后、正式对外分发之前

## 用途

将已 `confirmed` 的 PRD 写入**正式发布记录**，包含 artifact ID、版本号、授权审阅人、生效时间、关联需求目录。`prd-publish` 是 PRD 流程的"封口"环节。

## 输入

- 已 `confirmed` 的 `prd.md`（由 `prd-assembly` 输出）
- `00-input/authorized-reviewers.json`（人工 review 授权记录）
- 关联的 `requirements/REQ-XXX/` 目录

## 输出

`publish-record.md` 模板（位于 `src/templates/others/publish-record.md`），含：

- artifact_id / version / status
- 授权审阅人列表（id + 角色）
- 生效时间窗（start / end）
- 关联需求目录
- 内容 sha256（用于后续比对是否被未授权修改）

## 触发判断

- 看到 "发布 PRD" / "PRD publish" / "正式上线" / "签发" → 触发
- 看到 "草稿" / "未确认" → **不触发**（必须先 confirmed）

## 关键约束

- **必须**有 `authorized-reviewers.json` 中的人工 reviewer 授权
- **必须**记录 `artifact_content_sha256`，下游校验（如 `branch_validator.py`）用其比对
- **绝不**由 AI 自动将 PRD 标记为 published
- 一旦发布，PRD 内容变更必须走 `change-management` 走 Reflow 流程

## 配套资源

- `agents/openai.yaml` · OpenAI / Anthropic Agent 路由元数据
- `references/` · 思考透镜 / 产物契约 / 审计与评审清单 / 提问模板 / 来源处理 / 反模式
- `src/templates/others/publish-record.md` · 发布记录模板
- `scripts/validate_artifact.py` · 校验脚本
