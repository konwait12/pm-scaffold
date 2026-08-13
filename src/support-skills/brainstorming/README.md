# Brainstorming Skill（需求发散收敛）

> **Support Skill** · 位于 `src/support-skills/brainstorming/`
> **一句话**：入口 L0（仅想法）或材料稀疏时，把一句话需求按 12 维度发散成候选、聚类去重、全部标 `AI_INFERENCE`，交人工以 include/exclude/defer/research 四值处置，仅 include 项写回 `project-background-goal` 输入包。

## 触发

- 入口路由判定 **L0**（`00-input` 无材料、仅一句话想法）→ 建议 brainstorming 发散收敛
- **材料稀疏**：有少量材料但角色 / 场景 / 生命周期 / 备选缺失
- 不适用：多源歧义（走 `requirement-restate`）；材料充分（直接进入 `project-background-goal`）

## 产物

`brainstorming-output.md`（写入 `99-review/support/`，结构见 `src/templates/others/brainstorming-output.md`）：

- `候选清单` — SCN-XXX 候选表（全部 `AI_INFERENCE`，每条含 Evidence / Impact）
- `人工处置表` — 8 列（Candidate ID / Role-Lifecycle / Candidate / Evidence / Impact / Human Disposition / Reason / Write-back Target），仅人工填处置四值
- `Include 项写回` + `收敛后输入包` — 仅 include 项综合为 ≥ 50 字输入包，交付 `project-background-goal`

产物状态机止步于 `ready_for_human_review`，本记录永不产 `confirmed`。

## 配套资源

- `agents/openai.yaml` · 路由元数据（interface + 触发示例）
- `references/` · 思考透镜（Common Core + 12 维度发散）/ 产物契约 / 审计与评审清单 / 提问模板 / 来源处理 / 反模式
- `scripts/validate_artifact.py` · 校验脚本
- 过程文档（只读参考）：`src/shared/brainstorming/` — README.md（diverge→cluster→disposition→converge 流程）、SCENARIO_EXPANSION.md（12 检查维度）、rediscovery-templates/scenario-disposition.md（处置表格式）
