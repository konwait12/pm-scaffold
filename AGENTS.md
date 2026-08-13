# PM Scaffold · 产品 AI 脚手架 — Agent 唯一入口

> 任何 AI 执行体（Claude Code / Codex / Cursor / Copilot / 其他）进入本项目的**第一份必读文件**。
> 读完本文件后，按「启动顺序」依次读框架文件，再开始工作。不要跳过、不要先读别的。

---

## 1. 定位与边界

这是 **PRD-only 产品经理 AI 脚手架**：把原始需求材料（BRD、会议纪要、邮件、PPT、图片）逐步转化为一份**经真实人工确认、可沟通、可实现、可核验的中文 `prd.md`**。

- ✅ 我做：需求采集 → 业务需求 → 产品需求 → PRD 汇总 → 人工确认。
- ❌ 我不做：研发任务拆分、技术架构设计、测试用例、用户手册、API 合约。唯一交付物是 `prd.md`。

三条硬哲学：**业务真相由人类拥有**、**证据与不确定性必须可见**、**AI 不得伪造人工确认**。

---

## 2. 启动顺序（严格按序，共 5 个文件）

| 顺序 | 文件 | 作用 |
|---|---|---|
| 1 | `src/framework/workflow-registry.json` | 阶段 / Skill / 产物的**唯一机器真相源**，一切路径以此为准，不要硬编码 |
| 2 | `src/framework/constitution.md` | 6 条硬宪法，违反任何一条 = 缺陷 |
| 3 | `src/framework/workflow.md` | 每个 Work Item 必走的 8 步循环 |
| 4 | `src/framework/thinking-core.md` | 17 个思考透镜，§1 的 6 个核心透镜每次必用 |
| 5 | `src/framework/contracts.md` | 知识状态标注 + 确认不变式 |

之后读当前需求的 `STAGE.md` 和对应 Skill 的 `SKILL.md`。

---

## 3. 硬红线（违反即缺陷）

1. **`confirmed` 永远不能由 AI 设置**——只有 `pipeline.py review --decision approve`（带真实人名 + 授权清单匹配）才能产生。`--yes` 只能跑机器检查。
2. **上游未 confirmed，下游不启动**——`orchestrator` 会检测越级并阻止。
3. **PRD assembly 只聚合、不发明**——发现缺口路由回最早的 Work Item 重来。
4. **知识状态必须标注**——每条声明标 `FACT / DECISION / ASSUMPTION / AI_INFERENCE / UNKNOWN / CONFLICT`，不得把推断当事实、忽略冲突、漏掉未知。
5. **产物单点存放**——一个 artifact 一个位置，版本演进用 v0.* 快照，不在别处复制。
6. **变更已确认内容使下游失效**——回归到最早受影响的 Work Item 重跑。
7. **注册表是唯一真相源**——不要硬编码路径 / 阶段名 / Skill 名。

---

## 4. 执行循环（每个 Work Item 必走一遍）

```text
Preflight → Intake → Think → Clarify → Generate → Audit → Human Gate → Commit / Reflow
```

- **Clarify**（提问澄清）、**Reflow**（回流重做）是当前 Work Item 内部状态，不是独立主干。
- **Human Gate 不可绕过**：机器检查只能产出 `ready_for_human_review`，永远不能产出 `confirmed`。
- 产物状态机：`draft → needs_user_input / conditional_review / ready_for_human_review → confirmed`（`superseded` / `simulated` 为特殊态）。

---

## 5. 需求目录布局

```text
requirements/REQ-NNN-topic/
├── README.md
├── 00-input/                      # 原始材料 + authorized-reviewers.json
├── 001-business-requirements/
│   ├── 01-background-goal/
│   └── 02-user-journey-stories/
├── 002-product-requirements/
│   ├── 01-product-ux/
│   └── 02-function-description/
├── 003-prd-output/prd.md          # 唯一最终交付物
└── 99-review/                     # 评审记录 + 支持产物
```

一个 artifact 原地演进；快照与评审/变更记录保存历史，不创建竞争的「最终版」副本。

---

## 6. 常用命令

```bash
# 1. 创建新需求骨架
python3 src/scripts/pipeline.py init REQ-005-topic-name

# 2. 把输入材料放进 requirements/REQ-005-topic-name/00-input/

# 3. 查状态（active_work_item / next_work_item / 越级检测）
python3 src/scripts/pipeline.py requirements/REQ-005-topic-name status

# 4. 跑机器闸门（不改状态，只校验）
python3 src/scripts/pipeline.py requirements/REQ-005-topic-name gate \
  --work-item project-background-goal

# 5. 人工确认（只有人，带真实姓名 + 角色；--reviewer-id 需与 00-input/authorized-reviewers.json 一致）
python3 src/scripts/pipeline.py requirements/REQ-005-topic-name review \
  --work-item project-background-goal --decision approve \
  --reviewer "评审人姓名" --reviewer-id "飞书或组织稳定用户ID" \
  --reviewer-role "business_owner"

# 6. 变更回流预览 / 应用级联失效
python3 src/scripts/pipeline.py requirements/REQ-005-topic-name reflow --work-item project-background-goal
python3 src/scripts/pipeline.py requirements/REQ-005-topic-name reflow --work-item project-background-goal --apply

# 7. 全量自检
bash run_tests.sh
python3 src/scripts/consistency_check.py
```

人工批准前需在 `00-input/authorized-reviewers.json` 登记 reviewer 的 id、姓名与允许角色；本地校验不替代未来的飞书/SSO 身份认证。

---

## 7. Skill 全景（5 主 + 8 子 + 7 分支 = 20）

**主 skill（5，主干必做，永不询问）**
`project-background-goal` → `user-journey-and-stories` → `product-ux` → `function-description` → `prd-assembly`

**子 skill（8，挂到父 skill 的产物章节）**
`product-ux` 内：`ux-flow` / `page-design` / `interaction-rules`
`function-description` 内：`business-rules` / `validation-rules` / `state-machine` / `exception-handling` / `acceptance-criteria`

**分支/条件 skill（7，触发才跑）**
`competitive-research`（方向不清）、`solution-assessment`（方案取舍）、`prd-publish`（PRD 已确认）、`project-scope`（范围基线）、`requirement-restate`（需求复述）、`tracking-plan`（埋点计划）、`issue-record`（跨阶段澄清）

每个 skill 的权威行为见各自的 `SKILL.md`（含 8 步 Thinking Prompts、Anti-Patterns、示例、Load References、Completion 清单）。

---

## 8. 需要停下来问人（不要自己猜）

- 信息不足无法合理判断 → 标 `needs_user_input`，列出缺失信息。
- 两个来源说法矛盾 → 标 `CONFLICT`，列出冲突点。
- 业务决策（非技术选择）→ 标 `DECISION`，给出选项与推荐。
- 不确定声明是事实还是假设 → 标 `AI_INFERENCE`。

---

## 9. 关键目录地图

```text
src/framework/       宪法、契约、思考核心、注册表（先读这里）
src/stages/          3 阶段 × 5 主 skill + 8 子 skill
src/shared/          9 个共享机制（审计/澄清/变更/闸门/追溯等）
src/support-skills/  7 个分支/条件 skill
src/scripts/         pipeline / orchestrator / 校验器
src/templates/       22 个产物模板 + resolver
src/toolkit/         工具使用指南（Figma / Mermaid / lark-cli）
test/                回归测试（fixtures + 单元/集成测试）
requirements/        需求实例（运行时生成，gitignore）
```

更多：人类视角读 `README.md`；打包安装读 `skills/pm-scaffold/SKILL.md`。
