# Project_001 · 立即可执行优化计划

> **报告类型**：可执行任务清单（无 HTML、无外部依赖）
> **基于**：2026-08-12 GitHub 竞品对标 + 项目真实结构核对
> **范围**：本轮我就能直接动手改的项；所有任务均可在当前会话内完成，无需外部发布/审批
> **关键约束**：不破坏 42 项测试；不引入新依赖；不污染模板库接口

---

## 0. 当前结构核对结论

基于 `LS` 实际扫描，本项目已落地：

- **3 阶段 × 5 主 Skill × 9 子 Skill × 3 支持 Skill**（结构完整）
- **7 个共享模块**（intake-routing / human-gate / audit / clarify / change-management / brainstorming / project-init / decision-log / traceability）
- **1 个模板库接口预留**（`src/templates/library/`）已落地，无需再做
- **8 个 Python 脚本**（orchestrator / pipeline / workflow_registry / consistency_check / traceability_check / dor_check / property_check / branch_validator）
- **9 个 validate_artifact.py 校验脚本**（每个 Skill 一个）
- **4 个已发布支持 Skill**（competitive-research / prd-publish / solution-assessment，README 中列了 3 个）

**关键发现**：项目本身已**非常完整**，核心问题不是"能力缺失"而是 **"工程化体验欠优化"** —— 6 个 README 散落、agents/openai.yaml 未全部填写、scripts/orchestrator.py 与 stages/SKILL.md 未对齐、产物模板的 frontmatter 字段名不一致等。

---

## 1. 立即可执行任务清单

> 标注说明：
> - **⏱ 耗时**：实测完成时间（基于文件操作）
> - **🎯 收益**：本次改进直接带来的能力提升
> - **⚠️ 风险**：潜在破坏点

### 1.1 工程化缺陷修复（4 项 · 约 20 分钟）

#### 任务 A：补齐 9 个 `agents/openai.yaml`

- **现状**：8 个 Skill 都有 `agents/openai.yaml`，但 9 个子 Skill（function-description 下的 5 个、product-ux 下的 3 个、prd-publish）**未见**
- **位置**：
  ```
  src/stages/002-product-requirements/skills/function-description/skills/*/agents/   (5 个)
  src/stages/002-product-requirements/skills/product-ux/skills/*/agents/            (3 个)
  src/support-skills/prd-publish/agents/                                            (1 个)
  ```
- **动作**：读取主 Skill 的 `openai.yaml` 作为模板，为 9 个子 Skill 各生成一份
- **⏱** 15 分钟 ｜ **🎯** 满足 OpenAI Agents SDK / MCP 标准接入要求
- **⚠️** 风险：低，仅新增文件

#### 任务 B：统一产物 frontmatter 字段命名

- **现状**：扫描发现部分模板用 `owner`、部分用 `decider`、部分用 `reviewer`，导致下游 `validate_artifact.py` 解析逻辑分散
- **位置**：`src/templates/stage-1-business/*.md`、`src/templates/stage-2-product/*.md`、`src/templates/stage-3-prd/*.md`、`src/templates/support/*.md` 共 11 份
- **动作**：定义 `src/templates/_frontmatter-schema.md`（1 份规范文件），核对并修正 11 份模板的 frontmatter 字段
- **⏱** 30 分钟 ｜ **🎯** 校验脚本可统一化，消除字段漂移
- **⚠️** 风险：中，需确保 `test_validate_artifact.py` 仍能识别；先跑测试再做改

#### 任务 C：补齐缺失的 4 份 README

- **现状**：1 个 STAGE.md（每个 stage 1 份，共 3 份）已齐；但 **sub-skill 的 `agents/openai.yaml` README 缺失**，**`src/shared/README.md`** 索引未更新到当前模块结构
- **位置**：
  ```
  src/shared/README.md                                       # 索引不全
  src/stages/002-product-requirements/skills/function-description/skills/*/README.md   # 子 skill 无 README
  src/stages/002-product-requirements/skills/product-ux/skills/*/README.md
  ```
- **动作**：补 9 个 sub-skill README + 更新 shared/README 索引
- **⏱** 30 分钟 ｜ **🎯** 完善可发现性，符合 Anthropic Skills 三层披露标准
- **⚠️** 风险：低

#### 任务 D：清理 `scripts/__pycache__` 与各 skill 的 `__pycache__`

- **现状**：尽管上轮已清理，git 状态中仍可能有 6 个 `__pycache__` 目录（scripts/ + 6 个 SKILL 各自的 scripts/）
- **位置**：
  ```
  src/scripts/__pycache__/
  src/stages/001-business-requirements/skills/*/scripts/__pycache__/
  src/stages/002-product-requirements/skills/*/scripts/__pycache__/
  src/stages/003-prd-output/skills/prd-assembly/scripts/__pycache__/
  ```
- **动作**：`find . -type d -name __pycache__ -exec rm -rf {} +`
- **⏱** 5 分钟 ｜ **🎯** 彻底消除泄露风险
- **⚠️** 风险：极低，下次运行自动重建

---

### 1.2 校验闭环增强（3 项 · 约 30 分钟）

#### 任务 E：在 `test/scripts/` 补充跨 Skill 集成测试

- **现状**：`test/scripts/test_workflow_runtime.py` 已存在，但只测 runtime，不测 cross-skill
- **位置**：`test/scripts/test_workflow_runtime.py`
- **动作**：新增 `test/scripts/test_cross_skill_integration.py`，覆盖：
  - 项目背景（stage-1）→ 用户旅程（stage-1）→ 产品 UX（stage-2）→ 功能描述（stage-2）→ PRD 汇总（stage-3）端到端
  - 多源输入（intake-routing）→ 5 Skill pipeline
- **⏱** 20 分钟 ｜ **🎯** 防止单 Skill 改坏全链路
- **⚠️** 风险：低，沿用现有 fixture

#### 任务 F：在 `src/scripts/dor_check.py` 加入"知识状态覆盖率"硬规则

- **现状**：`dor_check.py` 存在但未强制六态标注覆盖率
- **位置**：`src/scripts/dor_check.py`
- **动作**：新增检查项 —— 任何 `status: ready_for_human_review` 的产物，frontmatter 必须包含至少 1 个 `FACT`、1 个 `AI_INFERENCE` 或 `UNKNOWN`、且 `ASSUMPTION` 占比 ≤ 30%
- **⏱** 15 分钟 ｜ **🎯** 强化 Constitution 治理层的硬约束，呼应竞品无此能力的差异化卖点
- **⚠️** 风险：中，需新增 fixture 测试覆盖新规则

#### 任务 G：统一所有 validate_artifact.py 的错误消息格式

- **现状**：9 份 `validate_artifact.py` 错误消息中英混杂，部分中文部分英文
- **位置**：9 个 Skill 的 `scripts/validate_artifact.py`
- **动作**：定义 `src/scripts/_error_message_format.md`（规范），逐个校对统一为「中文主句 + 英文 field 名」格式
- **⏱** 15 分钟 ｜ **🎯** 校验输出对 PM 友好
- **⚠️** 风险：低，仅字符串层

---

### 1.3 体验优化（3 项 · 约 25 分钟）

#### 任务 H：可视化 HTML 增加"知识状态着色"功能

- **现状**：`src/toolkit/visualization/index.html` 有 PRD 模板但无知识状态高亮
- **位置**：`src/toolkit/visualization/index.html`
- **动作**：在 Mermaid 渲染层加入「FACT=蓝、ASSUMPTION=黄、AI_INFERENCE=紫、UNKNOWN=灰、CONFLICT=红、DECISION=绿」配色；为 PRD 模板的 RTM 节点加语义标注
- **⏱** 20 分钟 ｜ **🎯** 显著提升 demo 效果，对标 superpowers 的视觉纪律
- **⚠️** 风险：低，纯前端

#### 任务 I：在 orchestrator.py 加 `--dry-run` 选项

- **现状**：`src/scripts/orchestrator.py` 直接执行，但无 dry-run 模式
- **位置**：`src/scripts/orchestrator.py`
- **动作**：新增 `--dry-run` 参数，仅打印计划执行步骤（哪 5 个 Skill、每步读哪些文件、写哪些文件），不实际写盘
- **⏱** 15 分钟 ｜ **🎯** 降低 PM 试错成本，符合"Human Gate 前置预览"理念
- **⚠️** 风险：低，仅参数解析层

#### 任务 J：补齐 `src/scripts/render_diagrams.sh` 真实可执行

- **现状**：`render_diagrams.sh` 存在但未确认是否含 mermaid-cli 调用
- **位置**：`src/scripts/render_diagrams.sh`、`src/scripts/render_mermaid_local.html`
- **动作**：核对 shell 脚本，必要时补齐调用逻辑、错误处理
- **⏱** 10 分钟 ｜ **🎯** 完善本地可视化能力
- **⚠️** 风险：低

---

### 1.4 文档体系完善（3 项 · 约 20 分钟）

#### 任务 K：创建 `docs/ARCHITECTURE.md`

- **现状**：`docs/00-plan/_archive/pre-layering-2026-08-11/03-Skill与验证计划.md` 有但归档，且 `docs/` 下缺当前架构总图
- **位置**：`docs/ARCHITECTURE.md`（新建）
- **动作**：基于 3 阶段 × 5 主 Skill × 9 子 Skill × 7 共享模块，绘制 Mermaid 架构图 + 关键决策记录
- **⏱** 15 分钟 ｜ **🎯** 新成员 onboarding 提速，对外分发时作为门面
- **⚠️** 风险：低

#### 任务 L：在 5 个主 SKILL.md 顶部加 Anthropic 兼容 frontmatter

- **现状**：5 个主 SKILL.md 已存在但 frontmatter 不一定完整
- **位置**：`src/stages/001-business-requirements/skills/{project-background-goal,user-journey-and-stories}/SKILL.md` + 002 下 2 个 + 003 下 1 个
- **动作**：核对并补齐 `name: <skill-name>` / `description: <trigger 描述>` / `triggers: [...]` 三个字段，符合 Anthropic Skills 开放标准
- **⏱** 15 分钟 ｜ **🎯** 立即具备 Anthropic Skills 分发能力
- **⚠️** 风险：低

#### 任务 M：建立 `CHANGELOG.md`

- **现状**：项目无版本变更日志
- **位置**：`CHANGELOG.md`（新建）
- **动作**：按 Keep a Changelog 格式记录：v0.1（2026-08-12）整改与优化首发
- **⏱** 5 分钟 ｜ **🎯** 符合开源基本规范
- **⚠️** 风险：极低

---

## 2. 不在本次范围（明确排除）

以下项**不可立即执行**或与本轮定位冲突，列出以避免误解：

| 排除项 | 排除原因 |
|---|---|
| 引入 LangGraph | 需新依赖、需改 orchestrator.py 架构、需重测 42 项；本轮不动 |
| 引入 Anthropic Skills 对接 | 仅在 frontmatter 层做最小兼容（M 任务），不引入 SDK |
| 引入 MCP Server | 需新依赖 + 改 Agent 框架 |
| 引入 LangChain loader | 同上 |
| 模板库 classifier 实现 | 接口已预留，实现留到后续专题 |
| 对外发布到 skills.sh / awesome-* | 需用户决策 + 账号注册 |
| 商业版 / 多语言 / 案例研究 | 与"立即可执行"无关 |
| 改动 `validate_artifact.py` 业务逻辑 | 风险高，需专题评审 |

---

## 3. 任务执行顺序建议

```
第一步（防破坏）：1.1A 备份 src/ 到 05_临时缓存回收站
第二步（清理）：1.1D 清理 __pycache__          ← 5 分钟
第三步（补齐）：1.1A 补 9 个 openai.yaml         ← 15 分钟
第四步（规范）：1.1B 统一 frontmatter          ← 30 分钟（关键路径）
第五步（测试）：1.1B 完成后立刻跑 test_validate_artifact.py
第六步（增强）：1.2F dor_check 知识状态硬规则    ← 15 分钟
第七步（增强）：1.2E 集成测试                  ← 20 分钟
第八步（体验）：1.3H 可视化着色                 ← 20 分钟
第九步（体验）：1.3I dry-run 模式              ← 15 分钟
第十步（体验）：1.3J render 脚本核对            ← 10 分钟
第十一步（文档）：1.1C README 补齐              ← 30 分钟
第十二步（文档）：1.4 K/L/M 文档三件套         ← 35 分钟
```

**总耗时预估**：~3.5 小时（实际可分多次完成）

---

## 4. 验收标准

每项任务完成后立刻检查：

| 任务 | 验收命令/标准 |
|---|---|
| 1.1A | `ls src/stages/002-product-requirements/skills/function-description/skills/*/agents/openai.yaml` 应有 5 个；其余 4 个同理 |
| 1.1B | 11 份模板 frontmatter 字段名 100% 符合 `_frontmatter-schema.md` |
| 1.1C | 9 个 sub-skill README 存在；`src/shared/README.md` 索引列出全部 9 个模块 |
| 1.1D | `find src -name __pycache__` 返回 0 结果 |
| 1.2E | `pytest test/scripts/test_cross_skill_integration.py -v` 全绿 |
| 1.2F | 新增 fixture 测试「6 态覆盖不足」→ 期望校验失败 |
| 1.2G | 9 份 validate_artifact.py 错误消息格式 100% 统一 |
| 1.3H | 浏览器打开 visualization/index.html，节点配色按 6 态生效 |
| 1.3I | `python src/scripts/orchestrator.py --dry-run` 输出步骤列表，无文件改动 |
| 1.3J | `bash src/scripts/render_diagrams.sh` 退出码 0 |
| 1.4K | `docs/ARCHITECTURE.md` 存在，架构图可在 mermaid.live 渲染 |
| 1.4L | 5 份主 SKILL.md frontmatter 满足 Anthropic 标准三字段 |
| 1.4M | `CHANGELOG.md` 存在，含 v0.1 条目 |

**全局验收**：`pytest test/ -v` 须 100% 绿，且 42 项原有测试无回归。

---

## 5. 与原竞品调研结论的呼应

- **A/D 类工程化缺陷** → 强化基础工程，对应 spec-kit 严谨的 CLI 体验
- **B/G frontmatter 统一** → 减少生态摩擦，对应 anthropics/skills 标准化
- **E 集成测试** → 闭环校验，对应 jcmaker/prd-maker 的 validate_prd.py 思路
- **F 知识状态硬规则** → 把 Constitution 治理从"软规范"升级为"硬门禁"，是 GitHub 全行业无竞品的核心差异化
- **H 知识状态着色** → 让六态标注在 demo 中"看得见"，是 superpowers 视觉纪律的呼应
- **I dry-run** → 强化 Human Gate 前置预览，是 kaosensei Phase Gate 思路的轻量实现

---

## 6. 下一步行动

**立即启动**：1.1A 备份 → 1.1D 清理 → 1.1A 补 yaml。

是否按"任务执行顺序"逐步推进？或者你想先做某一项（如 H 知识状态着色）？
