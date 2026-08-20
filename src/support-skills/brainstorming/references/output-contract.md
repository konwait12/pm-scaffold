# Output Contract · Brainstorming（发散收敛）

## 目的（Purpose）

本能力（`output_kind=process`）不是 PRD 产物：过程记录 `brainstorming-output.md` **永远不进 PRD 正文**。材料成熟度与 `process_tier` 正交；写回目标由持久化 intake 决策决定：L0 为 `mini-prd` 第 1/2 节输入线索，L1/L2 为 `project-background-goal` 输入包。

模板：`src/templates/others/brainstorming-output.md`。

## Artifact States（产物状态）

| 状态 | 含义 | 下游使用 |
|---|---|---|
| `draft` | 初始收集；Audit 未完成 | 否 |
| `needs_user_input` | 稀疏降级、答案会实质改变候选集或处置选项时阻断 | 否 |
| `conditional_review` | 已知晓非阻断未知，可审 | 否 |
| `ready_for_human_review` | 自审通过；待业务方/负责人工四值处置 | 否 |
| `confirmed` | **本记录禁止** | 否 |
| `superseded` | 被新版本取代 | 否 |

> 本记录**永不产 `confirmed`**：人工的 `include` 决策流入 `project-background-goal` 输入包，只有 `pipeline.py review --decision approve` 可确认下游工作项。过程记录最高只能停在 `ready_for_human_review`。

## 版本规则（Version Rules）

- 起 `v0.1`；人工要求修订时递增 minor（如 `v0.2`）。
- 本 skill 不产 confirmed，故**不存在** `v1.0` 概念；版本变更记录在 `## 版本变更摘要`。
- 跨阶段引用使用 `SCN-XXX` ID。

## Knowledge-State Labels（知识状态）

`FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`

- 发散候选表中，**唯一允许** `AI_INFERENCE`；未处置前不得升级为 `FACT`（仅在有 `SRC-*` 材料时可出现 `FACT`）。
- CONFLICT 在本 skill 中**不处理**：来源冲突是 `requirement-restate` 的职责，本 skill 只发散本想法。

---

## 候选表契约（Candidate Table · SCN-XXX）

材料稀疏时按风险相关维度发散。12 个维度是扫描透镜而非候选数量 KPI；无关维度标 `not_material` 并说明依据。聚类去重后每个独立想法一个稳定 ID `SCN-001`, `SCN-002`, …。

| 列 | 内容 | 规则 |
|---|---|---|
| Candidate ID | `SCN-XXX` | 单调递增，去重后编号，不随排序变化 |
| 发散维度 | 12 维度之一（lifecycle / roles / normal-alternate-exception-failure-timeout / permission / data condition / handoff / dependency / cancellation / retry / rollback / change-recovery / constraint） | 主维度 |
| Candidate | 候选内容一句话 | 单一诉求，不塞多条 |
| Evidence | 为什么 AI 这么想 | 引用原始想法原文 / SRC-* / 常识推断；**不得为空或占位** |
| Impact | 若纳入会产生什么影响 | 面向后续旅程/功能/范围的影响；**不得为空或占位** |
| 知识状态 | `AI_INFERENCE` | 全表统一；未处置前不得升级为 FACT |

> 12 维度列表与发散提问的权威来源：`references/thinking-framework.md` 的发散 lens 表。

## 人工处置表契约（Disposition Table · 8 列）

处置表有 **8 列**（`src/templates/records/scenario-disposition.md` 中约定的规范形态）：

| Candidate ID | Role-Lifecycle | Candidate | Evidence | Impact | Human Disposition | Reason | Write-back Target |
|---|---|---|---|---|---|---|---|
| `SCN-001` | 维度/阶段 | 候选内容 | 依据 | 影响 | include / exclude / defer / research | 原因 | 写回目标 |

Rules:

- **Human Disposition** 是四值之一：`include` / `exclude` / `defer` / `research`。AI 填其余所有列；**只有负责人工（business_owner）填这一列**。
- `include` → 候选进入正式写回；必须给非占位的 Write-back Target。L0 只可指向 `mini-prd` 第 1/2 节；L1/L2 才可指向 `project-background-goal` 输入包。
- `exclude` → 排除；Reason 必须说明排除原因。
- `defer` → 暂缓；Reason 给出触发条件或计划周期。
- `research` → 待调研；登记 issue-record / QuestionRecord，不静默搁置。

## 写回契约（Write-back Contract）

- 只有 `include` 候选被写回。L0 写为 `mini-prd` 第 1/2 节的来源线索；L1/L2 综合为 `project-background-goal` 输入包。
- 写回包必须是朴素的输入需求（"要探索什么"），而不是设计好的方案。
- `exclude` / `defer` / `research` 候选一律**不**写回输入包。
- 写回前必须复核或更新 `00-input/intake-decision.md`；回流 work item 由注册表 `resume_work_item_by_tier` 决定，不能由材料稀疏度猜测。

## YAGNI 削减契约（YAGNI Trim Contract）

在聚类去重后、写回前，候选经过一步**需求目标过滤**（AI 初判、人工拍板，方法见 `references/thinking-framework.md` §YAGNI 削减）。

Rules：

- AI **只给初判**，最终 `include/exclude/defer/research` 始终由 business_owner 人工填写在处置表的 `Human Disposition` 列。
- 被初判为 `exclude` / `defer` 的候选**不删除**，仍保留在候选表与处置表（供人工复核），只是更可能被排掉。
- 每条削减初判的理由必须落到处置表 `Reason` 列或候选 Evidence 中，禁止"想砍就砍"无凭据。
- 目的校准：`input_package` 只承接 **include** 候选，写入内容聚焦本需求目标，不把发散所有产物全量带下游。

## Human Responsibilities（人工责任）

- **business_owner（业务负责人）**：处置每个候选（`include` / `exclude` / `defer` / `research`），确认写回目标。
- **product_manager（产品经理）**：检查发散覆盖（12 维度）、证据质量、输入包对下游的可用性。

---

## Clarifications Session 契约

`## Clarifications` 一行一 session，≤5 sessions；`accepted_answer` 在 `ready_for_human_review` 前必填。每次 session：`CL-NNN` 单调编号；AI 初判 + 选项 + 影响 + owner + blocking；≤5 问题/轮；答案回写进候选表/处置表对应行。未知答案成为普通 QuestionRecord / issue-record 条目，不额外开分支。

## 下游交接（Downstream Handoff）

发散收敛通过后，仅 `include` 候选综合成的输入包进入 `project-background-goal` 输入包：

```text
mode                        # scn
trigger_signal              # L0 仅想法 / 材料稀疏 / 方案发散
version
scn_count                   # 候选总数
divergence_coverage         # 12 维度扫描摘要
included_candidates         # 仅 include 项
deferred_candidates         # defer 项 + 触发条件
research_items              # research 项 + issue-record 引用
input_package               # ≥50 字综合输入（交付 project-background-goal）
source_ids
```

## 内嵌于契约的反模式（Anti-Patterns Embedded In Contract）

- 出现"应该怎么设计"→ invalid，要求改写。
- 多候选塞一行 → 拆 `SCN-XXX`。
- 全表任何一条非 `AI_INFERENCE`（且无 SRC-* 支持）→ invalid。
- 过程记录状态到达 `confirmed` → invalid（止步 `ready_for_human_review`）。
- 处置表缺 Human Disposition、或 `include` 行缺非占位 Write-back Target → invalid。
- Evidence / Impact 任一为空或占位 → invalid。
