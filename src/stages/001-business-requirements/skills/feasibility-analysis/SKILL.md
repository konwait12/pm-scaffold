---
name: feasibility-analysis
description: L1/L2 主干立项首项。在业务需求阶段一开始，从市场空间 / 技术可行性 / 投入产出 / 风险评估 四个维度客观评估具体产品方案，输出 feasibility-report.md（带置信度 + 敏感度 + 多方案取舍）。**立项首项 — 必须先于 project-background-goal 完成**。AI 推荐；人类决策人拍板；本 skill 不会做出最终决策。
---

# 可行性分析（Feasibility Analysis · L1/L2 主干立项首项）

## 目的与边界

当技术、合规、资源或业务约束对某个具体产品级方案的可行性提出疑问时，本 skill 在四个维度上客观框定评估——**市场空间、技术可行性、投入产出、风险评估**——并给出带置信度的 做 / 不做 / 有条件做 推荐——但**绝不做出最终决策**。人类决策人拥有选择权。

当同一目标存在 ≥2 个实质不同的方案时（自研 vs 外购、不同路径、不同范围取舍），对比作为可行性报告内部的 **§多方案取舍** 章节处理，使用在打分前定义好的加权决策矩阵。它是报告的一章——不是独立的交付物。

**L1/L2 主干定位**：本 skill 在 001-business-requirements 阶段作为立项首项（order=1，详见 workflow-registry.json），位于 init 之后、`project-background-goal` 之前。`project-background-goal.predecessors` 含 `feasibility-analysis` —— 立项不通过即终止整个 REQ 流程，回流到需求池。

**L0 不启用**：L0 单点变更不需要立项评估；用 `mini-prd` 直接进入 §1 业务一句话。

**不要**做出最终决策、静默修改范围、设计架构，或评估只在实现细节上不同的方案（那些属于工程，不属于产品）。可行性评估要求一个具体的产品级方案已经存在。

## 输入与输出

**输入**：上游证据（background-goal / cost / constraint / compliance / market 数据）、一个具体的待评估产品级方案（来自已确认的 `feature-list` 或 `functional-flow`，或显式的可行性请求）、以及指定的 decision-owner。

**输出**：单一 `feasibility-report.md`（`001-business-requirements/00-feasibility-analysis/feasibility-report.md`），使用 `src/templates/stage-1-business/feasibility-report.md` 模板。

**§多方案取舍 章节**（若存在）使用 `src/templates/support/solution-comparison.md` 作为章节结构模板；嵌入在报告中，绝不作为独立产物产出。

产物标识：所有 ID 以 `FA-` 前缀（如 `FA-001`、`FA-MKT-001`）。

## 思考提示（按阶段）

按 8 步循环：**Preflight → Intake → Think → Clarify → Generate → Audit → Human Gate → Commit**。

### 1. Preflight（预检）
- "是否存在需要在市场 / 技术 / 投入产出 / 风险维度回答的可行性问题？是否存在具体的产品级方案？"
- "同一目标是否存在 ≥2 个真正不同的方案？如果是，适用 §多方案取舍 章节。"
- 识别 decision_owner。**如果不存在决策 owner，路由收据并 STOP 在 `needs_user_input`。**
- 评估成熟度：L0（无具体方案）→ L1（模糊想法）→ L2（存在产品级方案）→ L3（有成本/约束数据）→ L4（上游已确认）。

### 2. Intake（输入）
- "每个来源实际上是怎么说成本、约束、合规、依赖和风险的——而不是我假设的？"
- 收集四维度证据：市场空间 / 技术可行性 / 投入产出 / 风险评估。
- 按 `src/framework/contracts.md` 归类知识状态：FACT / DECISION / ASSUMPTION / AI_INFERENCE / UNKNOWN / CONFLICT。保留 SRC-ID。

### 3. Think（思考；应用 thinking-core.md §1 必用透镜）
- **First Principles**：要做的可观察决策是什么？哪些成本/风险是伪装成需求的假设？
- **Systems Thinking**：决策影响哪些上游/下游 work item、角色和依赖？
- **Adversarial**：明显的推荐会不会是陷阱？证据是否片面？
- **Reverse Validation**：从期望的结果倒推，每个方案要成功必须具备什么？

### 4. Clarify（澄清）
- 先调研可发现的客观事实（成本基准、公开定价、过往项目数据）。
- 批量整理剩余问题（≤5 个/会话，按影响排序）。
- **当答案会改变推荐、标准权重或重大成本/风险数字时，停止在 `needs_user_input`。**

### 5. Generate（生成）
- 主线四维度：市场空间 → 技术可行性 → 投入产出 → 风险评估 → 结论。
- **§多方案取舍 章节**（仅当 ≥2 实质方案时）：候选方案（等深）→ 权重在打分前定义 → 对比矩阵 → AI 推荐 + 置信度 → 敏感度分析 → 人工决策。
- 状态：使用 `draft` / `needs_user_input` / `conditional_review`——**绝不使用 `confirmed`**。

### 6. Audit（审计）
- **锚定检查**：标准是在打分前定义的吗？
- **对等检查**：每个候选是否以同等深度描述？
- **敏感度**：哪个标准若权重 ±1 会翻转推荐？
- **来源保真**：每条成本/风险数字是否追溯到来源？

### 7. Human Gate（人工关卡）
呈现：四维度证据摘要 + §多方案取舍 矩阵（若适用）+ 敏感度 + AI 推荐 + 审计结果。
**只有决策 owner 可以批准。** 人类选择被记录为 `DecisionRecord`（DEC-XXX）。

### 8. Commit / Reflow（提交 / 回流）
- 只有 `pipeline.py review --decision approve` 才能写入 `confirmed`。
- 立项不通过 → 整个 REQ 终止，不进入 BG。
- 立项有条件通过 → 把"条件"作为 BG 的前置约束记录。
- 已确认的 feasibility-report 被变更 → 重跑 Audit → 回到 Human Gate。

## 反模式

| ❌ 不要 | ✅ 要做 |
|---|---|
| 评估没有具体方案对象的"可行性" | 评估前要求具体的产品级方案 |
| AI 替业务方做最终决定 | AI 推荐 + 置信度；人拍板 |
| 打分后才定权重 | 权重先于打分定义 |
| 给偏爱的方案更多篇幅 | 每个候选等深描述 |
| 推荐不带置信度 | HIGH/MEDIUM/LOW 置信度 + 关键假设 |
| 跳过敏感度分析 | 识别哪个假设变化会翻转推荐 |
| 成本/风险估算当事实写死 | 标 `AI_INFERENCE`/`ASSUMPTION` + 责任人 + SRC-* |

## 与项目背景（BG）的关系

FA 是立项首项；BG 依赖 FA。当 FA 产出 `decision: go` 或 `decision: conditional_go`，BG 可以开始。当 FA 产出 `decision: no_go`，整个 REQ 终止，回报需求池。

FA 的 §1 结论会被 BG 引用作为"项目立项依据"；FA 自己的"建议结论"**永不**作为 BG 的事实事实，必须经人工评审 + 业务负责人签字后由 BG 引用。

## 加载参考文献

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/thinking-framework.md` | 思考透镜（Common Core + 评估领域 lens） | 任务开始（必读） |
| `references/output-contract.md` | 产物结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板 | Clarify 提问时 |
| `references/source-handling.md` | 来源处理规则 | Intake 时 |
| `references/anti-patterns.md` | AI 常见反模式（FA 特有） | Generate 时 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/reviewer-checklist.md` | 评审清单 | Human Gate 前 |
| `references/scoring-7d.md` | 7 维度 100 分制评分模型 | 打分阶段 |
| `references/idea-filtering.md` | Idea Filtering 市场重复性检查 | 新产品/自研方案评估前 |
| `references/rtm-and-market-sizing.md` | RTM + TAM/SAM/SOM 市场分析 | §市场空间 量化校验时 |

## 完成标准

四维度（市场 / 技术 / 投入产出 / 风险）都有证据支撑；当存在 ≥2 实质方案时，§多方案取舍 章节以等深方式记录每个方案；敏感度分析识别出翻转推荐的假设；结论是清晰的 做 / 不做 / 有条件做，条件具体可衡量；AI 推荐带显式置信度；人类决策者的选择被记录为 `DecisionRecord`。立项不通过时 REQ 终止，立项通过时 BG 可以开始。

---

> 本 skill 在 `workflow-registry.json` 中 `id: feasibility-analysis`、`order: 1`、`tiers: ["L1","L2"]`、`artifact_dir: 001-business-requirements/00-feasibility-analysis`。原 `src/support-skills/feasibility-analysis/` 作为历史归档保留（git blame / 旧 REQ 引用兼容）。
