# UX Flow · UX 流程

> **Sub-skill of** [`product-ux`](../SKILL.md)
> **输出章节**：父级 `product-ux.md` §3.1 主流程（P0）+ §3.2 分支与状态
> **执行顺序**：1 / 3（首先生成流程骨架）

## 用途

为每个 P0 功能画出**端到端 UX 流程**：入口、页面/步骤、决策点、主支线、异常回退。是后续 §Page（页面设计）和 §IX（交互规则）的骨架。

## 输入

- `user-journey-and-stories` 的 confirmed artifact（含 ST-XXX 用户故事、范围基线）
- 父级 `product-ux` §2 功能清单（FEA-XXX 与 P0/P1/P2）

## 产物

`§3.1 + §3.2` 区块：

- **Mermaid flowchart**（必出）：入口 → 主路径 → 分支 → 终止状态；异常回退路径（用虚线或红色标注）
- **分支与状态**（补充说明）：分支条件、error/empty/loading/timeout/cancel 状态与回退目标

## 触发判断

- 看到 "用户流程" / "UX 流程" / "页面跳转" / "用户路径" / "流程图" → 触发
- 看到 "页面设计" / "组件" → **不触发**（走 `page-design`）
- 看到 "交互规则" / "输入约束" → **不触发**（走 `interaction-rules`）

## 关键约束

- 每个流程图必须包含：入口、≥1 主路径、≥1 异常回退、终止状态
- 每条分支必须有条件标签；每个 P0 FEA ≥1 张图，且每张图 ≥1 个 error/empty/loading 状态
- 每个步骤可回溯 `ST-XXX` / `FEA-XXX`；AI 补的步骤标 `AI_INFERENCE`
- 不画视觉细节、不写交互规则、不写业务规则

## 执行循环

Preflight → Intake → Think → Clarify → Generate → Audit → Human Gate → Commit / Reflow（详见 `SKILL.md`）。**永远不产 `confirmed`**；只有 `pipeline.py review --decision approve` 能写入。

## 配套资源

- `agents/openai.yaml` · OpenAI / Anthropic Agent 路由元数据
- `references/anti-patterns.md` · AI 常见反模式
- `references/audit-checklist.md` · 审计清单
- `references/output-contract.md` · §3.1/§3.2 输出契约
- `references/question-patterns.md` · Clarify 提问模板
- `references/reviewer-checklist.md` · 人工评审清单
- `references/source-handling.md` · 上游追溯规则
- `references/thinking-framework.md` · 思考框架（必读）
- `scripts/validate_artifact.py` · 产物校验
- `templates/ux-flow-output.md` · 输出模板
