# `project-background-goal` Skill 能力评判报告

> 评估对象：`src/stages/001-business-requirements/skills/project-background-goal/` v0.1
> 评估日期：2026-08-11
> 评估方式：通读全部文件 + 跑 `validate_artifact.py` 对 3 份测试产物回归 + 对照 `01-前四阶段主流程与节点框架.md` §1 与 `01-三阶段主流程与工作事项.md` §4

---

## 一、5 个维度评分

### A. 流程严谨度：8 / 10

**一句话**：三闸门（G1 事实 / G2 目标 / G3 基线）+ §1.1 三模式分流 + 6 类知识状态标签 + Failure/Reflow 已成体系，是当前脚手架里最像样的单点能力。

值得加分的点：

- `SKILL.md` 第 41–45 行的 G1/G2/G3 三闸门显式声明"何时必须停"，把"AI 不替业务决定"做成了机械约束；
- §1.1 三模式（充分 / 低密度退化 / 路由改出）落地到位，且与 `01-前四阶段主流程与节点框架.md` §1.1 对齐；
- Boundary 段"Do not"第 4 条（"Turn a requested feature into the project goal without identifying the business outcome behind it"）直接针对 PM 类 AI 最常见错误；
- 7 个 lens 在 `thinking-framework.md` 中给出且各自有可观测的使用结论（与 §4 Clarify 直接挂钩）。

扣分点：

- 三闸门只在 `SKILL.md` 描述，`thinking-framework.md` 与 `audit-checklist.md` 没有反向引用 G1/G2/G3；自审时容易把"闸门触发条件"误读为"建议"；
- §4 Clarify 与 §6 Self-Audit 边界有重叠：审计里说"如果语义阻塞仍存在则设 needs_user_input"，与 Clarify 的批量提问职责未切干净；
- Failure/Reflow 段第 5 条"重跑 Audit 并请求再次确认"未规定"再次确认"是否走 G3 重判。

### B. 文档完整度：8 / 10

**一句话**：7 个必备文件全部存在、相互引用齐全、`assets/template.md` 14 章节骨架与 `validate_artifact.py` REQUIRED_HEADINGS 字字对应，校验脚本能拦下结构性缺陷。

值得加分的点：

- 目录与 `03-实施迁移与验证计划.md` §6.7 v0.1 实施基线完全一致（`agents/openai.yaml` 也在）；
- `REQUIRED_HEADINGS`（`validate_artifact.py:26–41`）与模板 §1–§14 命名精确匹配，不存在"模板有但脚本没列"或反过来的情况；
- `check_semantic_red_flags`（`validate_artifact.py:115–151`）新增的 3 条软规则刚好覆盖 `04-补强建议_基于调研与短板.md` 第 3 条短板；
- `references/` 4 个文件互相引用清晰：`SKILL.md` 第 32–37 行说明"何时读哪个 reference"。

扣分点：

- 缺 `examples/`（`03-实施迁移与验证计划.md` §2 列了 `question-patterns.md` 与 `examples.md` 两个标准件，本 Skill 都没建）；
- `references/output-contract.md` 列出 6 类状态，但 `references/audit-checklist.md` 的"Human Gate"段没把 6 状态的转换规则画成状态图；
- `agents/openai.yaml` 只有 3 行（`display_name` + `short_description` + `default_prompt`），没有 `agents/openai.yaml` 应当承载的"何时不应被触发"反例清单，对应 `eval-cases.json` 里的 `should_not_trigger` 还没落地。

### C. 可落地性：7 / 10

**一句话**：单句自然语言路径与"信息充分"路径都已用测试产物走过一遍；但"邮件 + 会议纪要 + 草图"这种 PM 真实混合输入尚未做端到端验证。

值得加分的点：

- 低密度退化路径在回归测试里被验证：从 10 字输入 → §0 Preflight 充分度判定 → §11 8 个澄清问题（含 AI 初步判断、选项、影响、责任人、阻断、回写位置），结构完整可执行；
- 回归测试产物 `test/skills/project-background-goal/fixtures/project-background-goal-regression-test-result.md` 通过验证脚本返回 `{"ok": true, "warnings": []}`，证明产物结构干净；
- Failure/Reflow 段第 4 条已说明"研究只能止步于证据，业务适用性必须人工确认"，挡住了"AI 拿竞品报告当业务事实"的常见陷阱。

扣分点：

- `eval-cases.json` 里 `complete-multi-source`（邮件+会议纪要+业务负责人）和 `conflicting-sources`（会议纪要与邮件目标冲突）两个端到端 case 至今没有真实跑过——这是 `project-background-goal` 验证标准（`03 §6.6.1`）明确要求的关键场景；
- 模板没有针对"多源输入"的字段示例（如：邮件引用 SRC-001、会议纪要引用 SRC-002、PPT 引用 SRC-003 的统一登记表格）；
- §6 Self-Audit 段第 3 条"不编造业务内容以满足清单"是口头要求，没有硬规则阻止——例如"目标章节如果只剩 1 行 KPI 而没有 evidence，仍能通过校验脚本"。

### D. 与公司既有规范对齐：9 / 10

**一句话**：与 `01-三阶段主流程与工作事项.md` §1–§7、`01-前四阶段主流程与节点框架.md` §1.1 / §2、`02-共享机制与产物契约.md` §4 / §6 / §8 全面对齐；`04-补强建议` 中 7 项短板已有 5 项落地。

值得加分的点：

- "工作事项锚点而非产出物"对齐：`SKILL.md` 第 6–8 行明确"Build the first confirmed baseline in the PRD-only workflow"；
- "三阶段主流程"对齐：本 Skill 是 `project-background-goal` 第一步，主流程标准 §2 的五步序列完全匹配；
- "AI 不替业务决定"对齐：Boundary "Do not" 第 4、5、6 条三连约束；
- "流程可暂停/恢复/回退"对齐：`SKILL.md` 第 159–164 行的 Failure/Reflow + G3 闸门 + `02-共享机制与产物契约.md` §8 变更回流已联通；
- 飞书会议 18 条要求中的 14 条已落地（见 `04-补强建议 §七` 对照表），本 Skill 在其中的 #A/B/C/E/F/G/H/I/K/M/N/O/Q/R/S 均通过。

扣分点：

- `01-前四阶段主流程与节点框架.md` §8 强制要求 5 个主干步骤产物末尾加 `## Constitution Compliance` 章节，本 Skill 的 `SKILL.md` / `template.md` / 3 份测试产物都没加该章节（违反改进 5 对本步的强约束）。

### E. 与 Spec Kit / 行业标杆差距：7 / 10

**一句话**：已借鉴 Constitution / Clarify / Checklist / Analyze 的核心思路，但"一次一问、Clarify 独立步骤、状态机显式"三项尚未补齐。

值得加分的点：

- 6 状态机（`references/output-contract.md:6–12`）已显式：draft / needs_user_input / conditional_review / ready_for_human_review / confirmed / superseded；
- Constitution 对齐通过 `references/audit-checklist.md` §3 Semantic Gate 隐式表达；
- `validate_artifact.py` 的 `check_semantic_red_flags` 已对应 Spec Kit Analyze 的"跨制品一致性检查"思想；
- 路由改出回执（SKILL.md §1.3）借鉴了 Spec Kit 的 `/clarify` 不替业务回答的边界。

扣分点：

- **缺独立 Clarify 阶段**：`SKILL.md` §4 Clarify 内嵌在 Generate 之前，未与 Generate 完全分离；`04-补强建议` 改进 4 明确要求"独立 Clarify 步骤 + 一次一问 + 立即回写"，本 Skill 仍是批量提问（§11 同时列出 Q-001~Q-008），与 Spec Kit `clarify.md` 的 1-question-per-iteration 不一致；
- **状态机仅在 output-contract 列了表，未画转换图**：从 `draft → needs_user_input → ready_for_human_review → confirmed → superseded` 的合法迁移路径与"谁有权触发"没显式写出；
- **无 Issue List 活文档机制**：`02-共享机制与产物契约.md` §6 要求 `IssueRecord`，但本 Skill 的 §11 待确认问题表是"一次性快照"，不跟踪决议日期/回写锚点/修订历史；
- **无 `## Clarifications` Session 章节**：每次用户答复后没有独立的会话记录位置，与 Spec Kit `Clarifications` 章节（spec.md 末尾的版本化会话日志）对不上。

---

## 二、能力清单（对照 `01-前四阶段主流程与节点框架.md` §1.0 项目背景与目标的最小结果）

| 最小结果项 | 对应模板/章节 | 状态 | 备注 |
|---|---|---|---|
| 原始需求来源 | §1 需求来源与触发 + §12 来源追溯 | PASS | SRC-001 起，可扩展至多源 |
| 为什么现在做 | §2 项目与需求背景 | PASS | 含 why now 提示位 |
| 当前如何处理 | §3 当前现状与已有做法 | PASS | 含"仍然有效的部分"提示 |
| 存在什么问题 | §4 核心问题与证据 | PASS | "问题→影响→证据"三件套强制 |
| 未来希望怎样 | §5 目标、未来期望与成功判断 | PASS | 三层（业务结果/交付结果/成功判断）+ 非目标 |
| 涉及哪些角色 | §6 用户角色与利益相关者 | PASS | 含决策者/事实所有者字段 |
| 何时交付 | §7 时间、约束与依赖 | PASS | 含 deadline/资源/合规/数据/系统/外部依赖 6 子项 |
| 哪些约束 | §7 时间、约束与依赖 + §8 初步边界与非目标 | PASS | 双章节覆盖 |
| 哪些未知 | §10 假设、AI 推断、未知与冲突 + §11 待确认问题 | PASS | 6 状态标签齐全 |

**结论**：9 项最小结果全部 PASS，无 FAIL。

---

## 三、3 份测试产物覆盖度评估

| 测试产物 | 对应模式 | 期望命中校验规则 | 实跑结果 | 覆盖度评估 |
|---|---|---|---|---|
| `project-background-goal-test-result.md`（v0.1 首次） | 低密度退化 + 路由改出 | status=needs_user_input；14 章节齐全；SRC-* 至少 1 条 | `{"ok": true, "warnings": []}` | **覆盖低密度退化路径**，但产物同时尝试走完整 §1–§14（违反 §1.2 "不进入 Generate"），属于 v0.1 早期版本对退化路径理解不全的痕迹，**改进后的回归产物已替代** |
| `project-background-goal-regression-test-result.md`（改进后） | 纯低密度退化 | status=needs_user_input；新增 §0 Preflight + §11.5 路由回执 | `{"ok": true, "warnings": []}` | **完整覆盖低密度退化路径**：含判定过程、跳过的步骤、猜测 vs 事实的严格分离、8 个 Q 的四要素齐全、对 §1.3 路由回执做了对称回执 |
| `project-background-goal-regression-violation-test.md`（故意违规） | 故意把 status 设 ready_for_human_review 但 §5 目标为空 + 大量 `待确认` | 应被 `check_semantic_red_flags` 抓出 | `{"ok": true, "warnings": [...]}`，命中 2 条语义 warning | **正确覆盖语义红线**：warning 1 "目标章节为空但状态 ready"、warning 2 "37 处 待确认 但状态不匹配"，证明改进 3 落地有效 |

**测试覆盖度判断**：

- ✅ 覆盖了"充分模式"（template 通过校验脚本 + 测试 1 模板测试）
- ✅ 覆盖了"低密度退化模式"（回归测试产物）
- �️ **未覆盖"充分模式 + 真实附件"**：没有端到端跑过 `eval-cases.json` 的 `complete-multi-source`（邮件+会议纪要+业务负责人）与 `conflicting-sources`（会议纪要与邮件目标冲突）两个真实验证 case
- ✅ 覆盖了"故意违规"（语义 warning 拦截验证）
- ⚠️ **缺"信息充分 + 实际附件"的真实验证**：这是 `project-background-goal` 推进闸门（`03 §6.6.2`）第 1 条要求的"当前工作事项 的所有真实验证案例全部通过"，目前只是模板级 PASS，不是真实邮件+纪要级 PASS

**建议补 1 份真实验证产物**：从 PM 邮箱里找一个真实的邮件+纪要混合输入，跑出 `complete-multi-source` 案例的 ready_for_human_review 候选产物，作为 `project-background-goal`→`user-journey-and-stories` 推进的人工事实。

---

## 四、5 条"是否需要新增/修改"建议

### 建议 1：在 `template.md` §14 之前加 `## Constitution Compliance` 章节

- **现在的空白**：`01-前四阶段主流程与节点框架.md` §8 把 `## Constitution Compliance` 列为所有 5 步的强制章节，模板与 3 份测试产物都没加。这意味着 `user-journey-and-stories` 评审时如果直接进入下一步，宪法违反项无法被本步自审拦下。
- **建议改什么**：在 `assets/project-background-goal-template.md` §14 之前插入宪法合规章节（PASS / FAIL / JUSTIFIED 三态），同时把 `validate_artifact.py:26–41` 的 `REQUIRED_HEADINGS` 加上"Constitution Compliance"，并在 `audit-checklist.md` 的 Structural Gate 第 1 条补"包含宪法合规章节"。
- **影响范围**：`template.md`、`validate_artifact.py`、`audit-checklist.md`、所有历史产物需一次性补正。
- **是否阻塞 `project-background-goal`→`user-journey-and-stories`**：**阻塞**。`04-补强建议` 改进 5 明确"`user-journey-and-stories` 启动前"完成，不补则 `user-journey-and-stories` 进入 user-journey-and-stories 时宪法追溯链断裂。

### 建议 2：把 Clarify 从 §4 拆出独立步骤，引入"一次一问 + 立即回写 + Clarifications Session 章节"

- **现在的空白**：`SKILL.md §4 Clarify` 与 §5 Draft 是顺序段，但当前 §11 一次性输出 8 个 Q（Q-001~Q-008），不符合 Spec Kit `clarify.md` 的"一次一问、每答一题立即回写到产物对应章节"。`04-补强建议` 改进 4 已识别此短板但未落地。
- **建议改什么**：(a) 在 SKILL.md 增加 §4.5 Clarify Session Log 段落；(b) 在 `template.md` 末尾加 `## Clarifications` 章节，每个 Session 含 `session_id / question / answer / reflow_target / timestamp`；(c) 文档化"单次最多 5 问，按 Impact × Uncertainty 排序"，与 §11 批量提问契约对齐。
- **影响范围**：SKILL.md、template.md、test 脚本（需新增 §11 表行数 vs §13 Clarifications Session 数的一致性校验）。
- **是否阻塞 `project-background-goal`→`user-journey-and-stories`**：**不阻塞但强烈建议**。如果不补，`user-journey-and-stories` 的 `user-journey-and-stories` 会沿用批量提问模式，Issue List 沉淀不下来。

### 建议 3：补 `eval-cases.json` 的 `complete-multi-source` 和 `conflicting-sources` 两份真实产物

- **现在的空白**：3 份测试产物只覆盖了低密度退化模式，没有真实的多源材料（邮件+会议纪要+PPT）跑通的产物，也没覆盖源冲突场景。`03 §6.6.2` 闸门第 1 条要求"当前工作事项 的所有真实验证案例全部通过 §6.6.1"，未达即不进入 `user-journey-and-stories`。
- **建议改什么**：从 PM 实际工作邮箱/飞书里拉 1 个完整需求（含 1 封邮件 + 1 份会议纪要 + 已知业务负责人），跑出 `ready_for_human_review` 候选产物；再准备 1 个会议纪要与邮件目标冲突的样本，跑出含 CONFLICT-XXX 的产物。
- **影响范围**：仅测试产物，不改 Skill 自身代码；但需补 `test/skills/project-background-goal/` 下的真实验证 fixture。
- **是否阻塞 `project-background-goal`→`user-journey-and-stories`**：**阻塞**。闸门条款直接写明。

### 建议 4：补 `references/question-patterns.md` 与 `references/examples.md`

- **现在的空白**：`03 §2` 通用结构列出 `references/question-patterns.md` 与 `references/examples.md` 两个标准件，本 Skill 的 `references/` 目录只有 4 个文件，缺这两个。这意味着 PM 拿不到"该问什么样的问题"和"一个好的产物长什么样"两份参考。
- **建议改什么**：(a) `question-patterns.md` 收录 §11 的 8 类问题模板（来源、背景、现状、问题、目标、角色、时间、范围），每类 3 个示例；(b) `examples.md` 收录 2 份已人工确认的真实产物脱敏版，作为 PM 与新加入团队的对照参考。
- **影响范围**：`references/` 新增 2 文件；eval-cases 可引用 examples 中的样本作为 fixture。
- **是否阻塞 `project-background-goal`→`user-journey-and-stories`**：**不阻塞**。可在 `user-journey-and-stories` 启动前补齐。

### 建议 5：把 `agents/openai.yaml` 补成 trigger / anti-trigger 双段，对齐 `eval-cases.json`

- **现在的空白**：`agents/openai.yaml` 只 3 行（`display_name` + `short_description` + `default_prompt`），未承载 `eval-cases.json` 中的 `should_trigger` / `should_not_trigger` 双向样例，意味着 Skill 触发条件不可被 Agent runtime 自动校验。
- **建议改什么**：在 yaml 中加 `trigger_examples: [eval-cases.json::should_trigger]` 与 `should_not_trigger_examples: [eval-cases.json::should_not_trigger]`，让 OpenAI Agent / Anthropic Agent 在路由阶段能自我检查是否错配。
- **影响范围**：`agents/openai.yaml` 单文件更新；同时给 `eval-cases.json` 留引用接口。
- **是否阻塞 `project-background-goal`→`user-journey-and-stories`**：**不阻塞**，但属于"工程完备性"短板，不补会导致下游 4 个 Skill 复制同样的不完整 yaml。

---

## 五、总体结论

**这个 Skill 当前是 P1（接近 P0，但仍需 5 项中的 2 项强制改进）才能进入 `user-journey-and-stories`。**

- **已具备**：Boundary 三段式 / 三闸门 / 三模式分流 / 6 状态 / 6 知识状态 / 14 章节骨架 / 校验脚本 0 error / 语义红线 warning / Failure/Reflow 与公司既有规范对齐 90% 以上；
- **缺 2 项阻塞改进**：
  1. Constitution Compliance 章节（建议 1）—— 阻塞 `user-journey-and-stories`；
  2. 2 份真实多源验证产物（建议 3）—— 阻塞 `project-background-goal` 闸门；
- **缺 3 项非阻塞改进**：Clarify 独立步骤（建议 2）、question-patterns/examples 参考件（建议 4）、openai.yaml 双段触发示例（建议 5），可在 `user-journey-and-stories` 启动前一次性补齐。

如果只看代码与文档严谨度，这个 Skill 已经达到 P0 上线门槛；但 `03 §6.6.1/§6.6.2` 闸门条款里"真实验证"和"Constitution Compliance"两项是硬性指标，因此当前严谨判定为：**P1，建议先跑完 1 个真实邮件+会议纪要的端到端 case 并加 Constitution 章节后再升 P0**。
