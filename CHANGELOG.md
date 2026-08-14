# Changelog

All notable changes to PM Scaffold · 产品 AI 脚手架 are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- (next release) — placeholder

## [0.3.1] - 2026-08-13

### Fixed · 运行时崩溃
- orchestrator.py 恰好 1 个 active work item 时 `active_sorted` 未定义抛 UnboundLocalError（正常流程每次只激活一个，核心路径崩溃）

### Fixed · 校验器与模板一致性（功能/UX 分离收尾）
- prd.md §3 标题「UX：功能范围、功能流程与关键状态」→「UX：页面设计与交互规则」（模板+校验器+output-contract+fixtures）
- prd-assembly 删除对已移出正文章节（上游产物清单/不一致报告）的检查（此前每次送审误报「不一致报告缺失」）
- prd-assembly D5.2 上游完整性检查改读 frontmatter `upstream_artifact_ids`（不依赖已删章节）
- function-description 删除错误要求 IX 交互规则的检查（IX 归 product-ux，出现才警告越界）
- product-ux/page-design 校验器死代码「页面与原型」→「页面设计」；registry `output_section` 同步
- tracking-plan `SECTION_NAME`「埋点需求」→「埋点需求分析」（对齐模板与 fixture）

### Fixed · 逻辑 bug
- property_check 状态机检查全文误匹配 + 6 列表只取 3 列 → 章节限定 + 正确列（63 states → 真实 3 states）；VL↔AC 配对改按「所属 FUN」关联
- find_artifact 的 v0 快照排除 `startswith("v0.")` 匹配不到 `xxx-v0.1.md` → `re.search(r"v0\.\d+")`

### Removed · 死代码与孤儿文件
- pipeline.py waiver 死代码（读错路径永不生效）+ `--variant`/`--preset`/`--waive` 死参数
- 7 个孤儿模板：field-rules / functional-structure / analytics-requirements / prd-executive / prd-technical / publish-record / analytics.md（埋点已由 tracking-plan 分支 skill 取代）
- `src/shared/brainstorming/` 残留目录（发散收敛能力已并入 requirement-restate 模式二）
- 3 个 bg 测试残留 fixture（历史测试结果记录，非有效产物）
- `.gitignore` 新增 `.backup*/`

### Changed
- 12 处文档过时引用修正：feature-list 的 ux-flow、DIAGRAMS/TOOLKIT/LOCAL_DIAGRAM_TOOLS 的功能结构树/UX 流程图、readme-skeleton 的 product-ux 描述、interaction-rules-output 的「UX 流程」标题等

### Tests
- 新增 orchestrator 单活跃项回归测试（test_orchestrator_single_active_item_does_not_crash）
- 53/53 PASS（删 3 个残留 fixture 后 56→53）

## [0.3.0] - 2026-08-13

### Changed · 产物清单对齐老版 + 一产物一 Skill
- 正式产物 10 → 5：一个主 work item 一个产物（journey 3 产物、product-ux 4 产物折叠为单产物 + 内部章节）
- **功能 / UX 严格分离**：功能清单（feature-list）与功能流程（functional-flow，原 ux-flow 误归 UX）移出 product-ux → function-description；product-ux 纯 UX（page-design + interaction-rules 2 子）；function-description 7 子
- 子 skill 8 → 9；skill 总数 21 → 19（5 主 + 9 子 + 4 分支产物 + 1 能力）
- 分支 skill 收编：brainstorming 并入「需求重举能力」、prd-publish 降级为发布复核动作（SHA-256 在 branch_validator）、project-scope 并入 journey 范围基线、solution-assessment 改名 feasibility-analysis（多方案降为章节）
- 补「字段规则说明」并入 validation-rules（字段定义表）
- registry schema v5 → v6

### Changed · PRD 结构瘦身（校验章节移出正文）
- prd.md 13 → 9 节：7 正文（背景/旅程/UX/分功能/按需/事实决定/验收）+ 需求追溯矩阵附录 + 自审记录附录
- 移出正文（由机器在 gate 产出、进 99-review 评审记录）：上游产物清单、正向/反向追溯检查、不一致报告

### Added · 入口探索阶段 + 一闸门两分支机器化
- entry 内容六信号 L0-L4 判定 + entry_blocked（L0/L1 材料不足）+ 分支信号
- bg DoR 硬检查「00-input ≥1 SRC」（无源即停机器版）
- B3 每阶段强制收口：dor_check stage_closeup（issue-record §13 收口表 + 待确认引用）+ 13 个 SKILL.md Clarify/Audit 接线
- B1 熔断（连续 3 轮 changes）/ B3 老化（7/14 天）/ 范围冻结信号（orchestrator loop_signals）
- 六态行内标注检测（FACT：…/。DECISION：… 自然写法不再误拦）
- 负例测试机制：violation fixture 反向断言（必须被校验器拒绝）

### Added · 驾驶舱（项目门面 + 教程）
- 单文件自包含驾驶舱 HTML：程序流程图（每线带条件）、命令全集、Skill/产物/脚本/共享机制/模板说明书、全景节点图（31 节点可展开收起）、文件完整架构
- 左侧导航（锚点 + 滚动高亮）+ 新手教程弹窗（10 章人机协作手册，目录跳转）
- AGENTS.md §0 首次接触协议：AI 见新人先开驾驶舱

### Added · 外部 skill 技法吸收
- pm-phase-4.5-prototype → page-design 原型两步流程；prd/prd-writer → prd-assembly 结构参考（只聚合边界）；requirements-gathering → bg 采集技法；user-journeys → journey 体验验证；doc-coauthoring → B1 修改循环；image2html → 参考图还原；webapp-testing → 原型自测

## [0.2.0] - 2026-08-13

### Changed · 入口收敛
- 四份入口（README/AGENTS/CLAUDE/AI）收敛为唯一 `AGENTS.md`（中文运行时入口），删除 `AI.md` 与 `CLAUDE.md`（CLAUDE.md 加入 .gitignore，防止个人 Agent 配置误入仓库），`README.md` 重写为开源门面（快速开始 + 架构图 + 能力说明）

### Added · Loop 引擎（机器闭环）
- `pipeline.py init <REQ-NNN-topic>` 从注册表生成需求骨架（目录 + authorized-reviewers.json + source-register + README）
- `pipeline.py reflow --apply` 真正级联失效：下游 confirmed/ready 翻为 superseded + 写 ChangeRecord
- `machine_gate` 对 function-description 增加 `property_check`（状态机穷尽/异常恢复/VL↔AC 配对/规则密度）
- `consistency_check` 覆盖 `requirements/` 内容（关闭空目录盲区）
- `traceability_check` 增加反向追溯（上游 ID 必须被下游消费）
- `entry` action 输出机器可检测的分支 skill 信号（prd-publish 确定性触发）

### Changed · Registry v5
- `support_capabilities` 3→7：新增注册 `project-scope` / `requirement-restate` / `tracking-plan` / `issue-record` 为分支 skill
- `tracking-plan` 从 function-description/skills/ 归位到 002 顶层（与 product-ux/function-description 同级）
- schema_version 4 → 5

### Added · Skill 同等丰富化（15 个 skill）
- 8 子 skill + 3 支持 skill + 4 分支 skill 全部补齐到主 skill 标准：10 节 SKILL.md + 7 类 references + thinking-framework 接线 thinking-core + agents/openai.yaml + README
- 修复：exception-handling validator ID 正则（EX-）、state-machine 前缀（STATE-）、solution-assessment 模板路径漂移、_norm 中文序号剥离
- `run_tests_mac.sh` 改为注册表驱动，覆盖全部 7 个分支 skill

### Added · 开源准备
- `LICENSE`（MIT）、`CONTRIBUTING.md`；确认无隐私数据残留

## [0.1.0] - 2026-08-12

### Added · 工程化补齐
- 9 个 sub-skill `agents/openai.yaml` 元数据（business-rules / validation-rules / state-machine / exception-handling / acceptance-criteria / ux-flow / page-design / interaction-rules / prd-publish）
- `src/templates/_frontmatter-schema.md` · 产物 frontmatter 统一规范文档
- 5 份跨 Skill 集成测试（`test/scripts/test_cross_skill_integration.py`）
  - orchestrator 序列匹配注册表
  - 主 Skill 模板/校验脚本存在性
  - 5 主模板覆盖 6 态知识标注
  - dor_check 知识状态硬规则触发
  - orchestrator --dry-run 报告正确

### Added · 治理强化
- `dor_check.py` 知识状态硬规则（`ready_for_human_review` 状态必须覆盖 FACT/DECISION/ASSUMPTION/AI_INFERENCE/UNKNOWN/CONFLICT 六态，ASSUMPTION 占比 ≤ 30%）
- `orchestrator.py --dry-run` 预览模式（PM/AI 在 Human Gate 前可看到下一步将触碰哪些文件）

### Added · 可视化增强
- `src/toolkit/visualization/index.html` 新增六态配色（CSS 变量 + 知识状态流模板 + Mermaid themeVariables）
- 六态图例（侧边栏）

### Added · 文档
- `docs/ARCHITECTURE.md` · 整体架构说明
- 9 份 sub-skill README（sub-skill/README.md）
- `docs/immediate-actionable-optimization-plan.md` · 立即可执行优化任务清单（已于 v0.2.0 起移出仓库）
- `src/templates/library/` · 模板库接口预留（README / manifest.schema.json / classifier-interface.md）

### Changed
- `test/skills/project-background-goal/fixtures/hire-website-confirmed.md` · §10 补全六态历史记录（UNK-002 / ASM-002 / AII-003/AII-004 / CNF-002/CNF-003）
- `src/shared/README.md` · 新增 9 大子 Skill 索引 + 3 支持 Skill 索引 + 全局变更日志

### Cleanup
- 清理 6 个 `__pycache__` 目录（27 个 `.pyc` 文件）

### Tests
- 测试套件：43/43 PASS（42 原有 + 5 新增跨 Skill 集成 - 4 新增单测集成，1 个 unit 文件含多 case）

## [0.0.x] - 2026-08-11 and earlier

历史版本见 git log。
