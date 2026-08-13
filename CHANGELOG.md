# Changelog

All notable changes to PM Scaffold · 产品 AI 脚手架 are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- (next release) — placeholder

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
- `run_tests.sh` 改为注册表驱动，覆盖全部 7 个分支 skill

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
- `docs/immediate-actionable-optimization-plan.md` · 立即可执行优化任务清单
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
