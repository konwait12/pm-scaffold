---
name: project-scope
description: L1/L2 主干立项次项。在业务需求阶段 BG 之后、UJ 之前，**显式定义 PRD §2 项目范围**——In/Out/Deferred/Conditional 四态范围基线 + 假设 + 依赖 + 风险姿态。**这是 PRD §2 的唯一上游**（之前 §2 由 BG + US 隐式拼凑）。产物 project-scope.md 作为范围变更回流的事实源。
---

# 项目范围（Project Scope · L1/L2 主干）

## 目的与边界

本 skill 是 **PRD §2 项目范围** 的唯一上游。**它不收集需求**（那是 BG 的职责）、**不写用户故事**（那是 US 的职责）——它的唯一职责是**显式画出范围基线**：

- **In Scope（本期做）**：本期 PRD 必须包含的功能/能力/章节
- **Out of Scope（本期不做）**：明确不做，避免业务方误以为遗漏
- **Deferred（暂缓）**：未来版本考虑，本期不实现但保留扩展点
- **Conditional（条件性）**：当某种触发条件满足时纳入（用户量达标、合规要求变化、依赖上线等）

同时记录：
- **Assumptions（假设）**：当前决策基于的、可被推翻的事实陈述
- **Dependencies（依赖）**：跨团队 / 跨系统 / 跨产品线依赖
- **Risk Posture（风险姿态）**：本项目对哪类风险有强约束（合规 / 数据安全 / 资金 / 隐私）

**L1/L2 主干定位**：order=3（在 feasibility-analysis=1、BG=2 之后；user-journey=4 之前）。L0 不启用——L0 单点变更的范围在 `mini-prd` §1 业务一句话中表达。

## 输入与输出

**输入**：上游已确认的 `feasibility-report`（立项决策）+ `background-goal`（项目背景与目标）。下游：被 `user-journey` / `user-stories` / `feature-list` 引用作为范围基线。

**输出**：单一 `project-scope.md`（`001-business-requirements/02-project-scope/project-scope.md`），使用 `src/templates/stage-1-business/project-scope.md` 模板。

产物标识：所有 ID 以 `SCOPE-` 前缀（如 `SCOPE-001`）。

## 思考提示（按阶段）

### 1. Preflight（预检）
- "立项是否已通过（FA 决策 = go 或 conditional_go）？"
- "BG 是否已确认（predecessors: feasibility-analysis 满足）？"
- "是否已经有任何 In/Out/Deferred/Conditional 的草稿（来自 BG、邮件、纪要）？"

### 2. Intake（输入）
- 收集三类范围线索：
  - **来自 BG**：明确提到的"In"和"Out"
  - **来自 FA**：风险姿态（合规/资金/隐私约束）
  - **来自历史 REQ**：相似项目的范围基线作为参考

### 3. Think（思考；应用透镜）
- **First Principles**：本期 PRD 真正必须解决的 1 件事是什么？
- **Adversarial**：哪些看起来 In 的功能其实是 Out？
- **Reversibility**：本期 Out 是否会引起业务方反弹？如果会，是否应改为 Conditional？

### 4. Clarify（澄清）
- 当 In/Out 边界模糊（"算不算？"）时，停下来询问业务方。
- ≤5 个问题/会话，按影响排序。

### 5. Generate（生成）
- 四态范围基线表（In / Out / Deferred / Conditional）
- 假设清单（每条假设标 F/D/A/AI/U 知识状态）
- 依赖清单（跨团队 / 跨系统 / 跨产品线）
- 风险姿态（合规 / 数据安全 / 资金 / 隐私 四个轴的强度）

### 6. Audit（审计）
- **范围完整性**：四态每态至少 1 行（除非显式声明"无 Conditional 项"）
- **假设可证伪**：每条假设都必须能被反驳/确认
- **依赖单点**：任何关键依赖必须有 Owner + 计划落地日期

### 7. Human Gate（人工关卡）
- 业务方拍板："本期是否就做这些？"（In 列表）
- 业务方确认："这些确实不做？"（Out 列表）
- 业务方确认："这些等条件满足再做？"（Conditional 列表）
- **范围变更 → 回流**：后续 UJ/US/FE 中任一项说"实际需要 §X 范围外能力"时，必须先回流到本 skill 改范围基线。

### 8. Commit / Reflow（提交 / 回流）
- 只有 `pipeline.py review --decision approve` 才能写入 `confirmed`。
- 范围变化（In/Out/Deferred/Conditional 任一调整）→ 回流到本 skill 重做。

## 反模式

| ❌ 不要 | ✅ 要做 |
|---|---|
| 把范围写在 BG 末尾"顺手带一笔" | 范围独立 work item，专门 §2 章节 |
| 只列 In 不列 Out（让 Out 变成"AI 漏掉"） | In / Out / Deferred / Conditional 四态齐全 |
| 把"将来可能做"放进 In | 用 Deferred 或 Conditional 标记 |
| 假设不标知识状态 | 每条假设标 F/D/A/AI/U/C |
| 依赖只写"待定" | 依赖必须有 Owner + 计划落地日期 |

## 与下游关系

- `user-journey` 引用 `project-scope.In` 作为旅程触点边界
- `user-stories` 引用 `project-scope.In` 作为故事范围，引用 `Out` 作为非故事依据
- `feature-list` 引用 `project-scope.In + Conditional` 作为功能点来源
- `prd-assembly` 投影 `project-scope` 到 prd.md §2 项目范围

## 与上游关系

- `project-background-goal.predecessors` 含本 skill
- `feasibility-analysis` 的"风险姿态"章节是本 skill 输入

## 加载参考文献

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/scope-decision-matrix.md` | 四态范围决策矩阵 | Clarify 时 |
| `references/assumption-catalog.md` | 假设清单模板（含知识状态标注） | Intake / Generate 时 |

## 完成标准

四态范围基线（In / Out / Deferred / Conditional）每态至少 1 行；假设清单标 F/D/A/AI/U/C；依赖清单含 Owner + 落地日期；风险姿态在四轴上各给出强度（HIGH/MEDIUM/LOW）。范围变更回流机制写入 99-review 记录。

---

> 本 skill 在 `workflow-registry.json` 中 `id: project-scope`、`order: 3`、`tiers: ["L1","L2"]`、`artifact_dir: 001-business-requirements/02-project-scope`。
