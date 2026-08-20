# brainstorming

发散收敛（头脑风暴）· 面向未定档的稀疏材料或方案发散，形成候选并交人工处置。材料成熟度不等于交付档位。

## 性质

这是**分析过程**，**不是 PRD 产物**。

它的输出是 `brainstorming-output.md`：稀疏材料被扩成候选（`SCN-XXX`，全 `AI_INFERENCE`），由业务负责人逐条处置（`include` / `exclude` / `defer` / `research`）。仅 `include` 候选可写回：L0 作为 `mini-prd` 第 1/2 节的输入线索，L1/L2 才进入 `project-background-goal` 输入包。

## 用途

- 未定档的一行想法或材料稀疏（`entry` 判定，无 SRC 来源）
- 材料稀疏到无法直接进入主干
- 方案/方向不清，需要先发散再收敛

## 不该用

- 有可追溯来源（L1-L4）需确认理解 → 用 `requirement-restate`（复述确认）
- 多来源冲突的裁决 → 那是复述 + issue-record 的职责
- 直接进入主线起草：L0 → `mini-prd`；L1/L2 → `project-background-goal`

## 发散原则

| 原则 | 原因 |
|---|---|
| **风险驱动扫描** | 12 个维度是检查透镜；不重要的维度标 `not_material` 并说明依据 |
| **聚类去重** | 一个独立想法一个 `SCN-XXX`，避免重复候选 |
| **全表 AI_INFERENCE** | 处置前不得把候选当事实 |
| **Evidence + Impact 必填** | 每个候选讲清"AI 为什么这么想"与"纳入的影响" |
| **人工唯一处置** | include/exclude/defer/research 只由 business_owner 判定 |
| **仅 include 写回** | excluded 不进入输入包；research 登记 issue-record 跟进 |

## 上下游衔接

- **上游**：未定档的原始想法 / 稀疏材料（若有材料按 `references/source-handling.md` 登记 SRC-*）
- **下游（成功路径）**：include 候选 → 复核 intake 决策 → L0 进入 `mini-prd` 输入线索，L1/L2 进入 `project-background-goal`
- **下游（失败/阻塞）**：处置不完整或出现实质新想法 → 从 Preflight 重新进入

## 验证

```bash
python3 scripts/validate_artifact.py <产物路径> --json
```

其中 `<产物路径>` 是生成的 `brainstorming-output.md`（如 `requirements/REQ-XXX/99-review/support/brainstorming-output.md`）；模板见 `src/templates/others/brainstorming-output.md`。

> 注：v0.5.1 拆分将原 `requirement-restate` 的「模式二·发散收敛」独立为本 skill。原 `src/shared/brainstorming/` 目录已删除，12 维度权威来源与处置表契约现统一收敛于本 skill 的 `references/output-contract.md` 与 `references/thinking-framework.md`。
