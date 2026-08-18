# 输出契约 · prd-assembly

## 状态机（Status Machine）
与所有 Skill 相同的 6 种状态：draft → needs_user_input → conditional_review → ready_for_human_review → confirmed → superseded。

## 产物章节（Artifact Sections）

正文（7 节，干系人/研发/测试阅读）：
1. **项目背景与目标** (§1): 来自 `project-background-goal` verbatim
2. **用户旅程与用户故事** (§2): 来自 `user-journey` / `user-stories` verbatim
3. **功能流程与页面设计** (§3): 来自 `functional-flow` / `page-design` / `interaction-rules` / `state-machine` verbatim
4. **分功能描述** (§4): 来自 `feature-list` / `functional-flow` / `business-rules` / `interaction-rules` / `validation-rules` / `exception-handling` / `acceptance-criteria` verbatim
5. **按需章节** (§5): 字段规则、埋点、依赖、未决项
6. **事实与决定** (§6): 汇总的关键事实与人工决策
7. **验收依据** (§7): 验收基线

附录（2 节，评审/机器用，非正文）：
- **需求追溯矩阵**: G→ST→FEA→FL→AC→BR matrix（traceability_check.py 读取此表）
- **自审记录（Constitution Compliance）**: AI 4-principle self-audit（dor_check audit_evidence 读取）

**不在 PRD 内**（由机器在 gate 时产出、进 99-review 评审记录）：
- 上游产物清单 → frontmatter `upstream_artifact_ids`
- 正向/反向追溯检查 → `traceability_check.py` 输出
- 不一致报告 → 评审记录（review taxonomy [Contradiction]/[Gap]/… labels）
- 变更记录 → frontmatter version/updated_at + CHANGELOG

## 聚合规则（Aggregation Rules）
- **内嵌完整内容，不写指针**：§1-§4 与 §6、§7 及其中的 BR/VL/SM/EX/AC/字段表必须**逐字内嵌上游全文**（数据表整表搬运进 PRD），禁止用「详见 XX-XXX」「内容见 XX-XXX」一类的单行指针替代内容。下游消费方应能**只读 prd.md** 就拿到全部规则，无需再去翻上游文件。
- 逐字复制上游内容，绝不转述、不概括删减、不润色成改变含义。
- 保留全部 ID（SRC-*、BG-*、UJ-*、US-*、ST-*、FEA-*、FL-*、PD-*、IX-*、BR-*、VL-*、SM-*、EX-*、AC-*），杜绝漂移。
- PRD 中无新需求。
- 不静默解决不一致。
- 条件章节（§5.1、§5.2）仅在上游有非空内容时才落章；上游无内容时标注「本期不适用」，**不得以「详见 XX-XXX」指针了事**。

## RTM 格式（RTM Format）
| Goal (G) | Story (ST) | Feature (FEA) | Function (FL) | Acceptance (AC) | Business Rule (BR) |
每行 = 一条完整追溯链。P0 项必须有完整链。
