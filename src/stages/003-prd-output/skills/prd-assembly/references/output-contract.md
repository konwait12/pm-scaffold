# 输出契约 · prd-assembly

## 状态机（Status Machine）
与所有 Skill 相同的 6 种状态：draft → needs_user_input → conditional_review → ready_for_human_review → confirmed → superseded。

## 产物章节（Artifact Sections）

L2 正文（10 节，干系人/研发/测试阅读；与图中 10 个主干产物一一对应）：
1. **项目背景** (§1): 来自 `project-background-goal` verbatim（现状/问题/目标 G-XXX/KPI/约束）
2. **项目范围** (§2): 来自 `user-stories` §项目范围基线 + `feature-list` 边界 verbatim（In/Out/Deferred/Conditional + 假设与依赖）
3. **用户旅程** (§3): 来自 `user-journey` verbatim（生命周期/旅程图/路径覆盖）
4. **用户故事** (§4): 来自 `user-stories` verbatim（故事卡 ST-XXX / MoSCoW / 覆盖矩阵）
5. **功能清单** (§5): 来自 `feature-list` verbatim（FEA-XXX 总账 + ST 追溯）
6. **功能流程** (§6): 来自 `functional-flow` verbatim（主/支/异常 Mermaid 整图）
7. **原型/UX** (§7): 来自 `page-design` verbatim（信息架构/页面结构/原型/交互标注/状态描述；纯服务端标「本期不适用」）
8. **交互规则** (§8): 来自 `interaction-rules` verbatim（IX-XXX 逐条 / 5 状态；纯服务端标「本期不适用」）
9. **业务规则** (§9): 呈现合并、产物独立——9.1 计算与流程规则 ← `business-rules` verbatim；9.2 校验规则 ← `validation-rules` verbatim；9.3 状态变化 ← `state-machine` verbatim；9.4 异常处理 ← `exception-handling` verbatim
10. **验收依据** (§10): 来自 `acceptance-criteria` verbatim（AC-XXX Given/When/Then + 量化阈值）

按需章节 (§11，上游有非空内容才落章，无内容标「本期不适用」)：
- 11.1 竞品分析 ← competitive-research；11.2 字段规则说明 ← validation-rules 字段表；11.3 埋点需求分析 ← tracking-plan；11.4 可行性分析 ← feasibility-analysis；11.5 术语表；11.6 团队职责

附录（评审/机器用，非正文）：
- **需求追溯矩阵**: G→ST→FEA→FUN→AC→BR matrix（traceability_check.py 读取此表）
- **自审记录（Constitution Compliance）**: AI 4-principle self-audit（dor_check audit_evidence 读取）
- **问题清单**（条件）: 仅 frontmatter `issue_in_prd: true` 时生成；默认问题清单只进 issue-record.md（Intake 时问用户）

**不在 PRD 内**（由机器在 gate 时产出、进 99-review 评审记录，或留在项目侧）：
- 上游产物清单 → frontmatter `upstream_artifact_ids`
- 正向/反向追溯检查 → `traceability_check.py` 输出
- 不一致报告 → 评审记录（review taxonomy [Contradiction]/[Gap]/… labels）
- 变更记录 → frontmatter version/updated_at + CHANGELOG
- 可行性分析（默认不进正文，仅 §11.4 按需）→ 项目侧 99-review/support/
- 问题清单（默认不进 PRD）→ issue-record.md
- 需求重举 / 流程校验器 / B3 收口表 / hash-anchor / ReviewRecord → 各自流程载体

## 兼容（v7 → v8）

- `prd_structure_version: 7`（缺省）＝存量 REQ 冻结旧 14 节结构契约（REQ-001 等），validate_artifact.py 走 `REQUIRED_HEADINGS_V7`。
- `prd_structure_version: 8` ＝ 新 REQ 按档位装配。`process_tier: L1` 仅装配 7 个确认上游与最终 PRD（共 8 个 work item），正文包含 §1-§6、§9.1、§10；§7、§8、§9.2-§9.4 必须省略，五项 L2-only 能力的不适用事实只记录在 `intake-decision.md` 与 assembly manifest，且不得声明 L2-only 上游。L1 的 §9.1 只可承载普通业务规则，不得写入状态枚举、状态转移、状态机，或含状态、触发事件及守卫/目标状态的转移表；出现这些设计信号即须升级 L2。`L2` 时 `REQUIRED_HEADINGS_V8_L2` 全 10 节。
- 存量 REQ 不迁移、不重跑（confirmed 不可变）。

## 聚合规则（Aggregation Rules）
- **内嵌完整内容，不写指针**：§1-§4 与 §6、§7 及其中的 BR/VL/STATE/EX/AC/字段表必须**逐字内嵌上游全文**（数据表整表搬运进 PRD），禁止用「详见 XX-XXX」「内容见 XX-XXX」一类的单行指针替代内容。下游消费方应能**只读 prd.md** 就拿到全部规则，无需再去翻上游文件。
- 逐字复制上游内容，绝不转述、不概括删减、不润色成改变含义。
- 保留全部 ID：artifact ID 依注册表（如 FL-*），正文 Trace ID 依 `src/framework/id-contract.md`（如 G-*、FUN-*、STATE-*）；兼容已确认的历史 SM-*，杜绝漂移。
- PRD 中无新需求。
- 不静默解决不一致。
- 条件章节（§5.1、§5.2）仅在上游有非空内容时才落章；上游无内容时标注「本期不适用」，**不得以「详见 XX-XXX」指针了事**。

## RTM 格式（RTM Format）
| Goal (G) | Story (ST) | Feature (FEA) | Function (FUN) | Acceptance (AC) | Applicable evidence |
每行 = 一条核心追溯链。P0 项必须有 G→ST→FEA→FUN→AC；BR/VL/STATE/EX/PD/IX 仅在适用时附入，不强制线性穿越。
