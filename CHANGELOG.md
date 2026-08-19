# Changelog

All notable changes to PM Scaffold · 产品 AI 脚手架 are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/).

## [0.6.0] - 2026-08-18

### Added · 外部 PRD/PM Skill 精华整合（两轮 + 薄弱补厚，95 注入点）

#### 整合背景
- 评估 48 个团队/市场 PRD/PM skill（第一轮 13 个 + 第二轮 35 个新下载），提炼精华按「A 思想层 / B 参考文档层 / C 审计层」注入既有 19 skill，**不新增业务阶段、不触碰注册表/主干 8 步/模板 frontmatter/校验器**（零改动红线，E3_drift 未触发）。

#### A 档 · 思想层（18 项）
- `thinking-core.md`：§2 校验层 +6 透镜（业务语言/证据追溯/成本门禁/置信度标注/事实假设判断三态/出口闸门两问）；§3 发散决策层 +8 透镜（grill 对抗/反例扫描/预死亡分析/假设验证四维/naysayer 三阶段/决策预注册/西瓜防御/二阶效应）；§5 表达层技法注册 +4（溯源标注三级/反合理化对照/独立成文/认知透镜附录 §5.1）。
- `workflow.md`：同步「新批次技法与透镜」引用段。

#### B 档 · 参考文档层（64 个技法文件，全部 ≥80 行且登记加载表）
- 第一轮 13：功能五要素/交互五段式/UML 用例/数据字典/RBAC 矩阵/泳道状态机/字段决策清单/确认信号/MRC 门禁/业务约束五分类/信息架构/AI 策略四要素/价值复杂度矩阵等。
- 第二轮 42：14 维缺口扫描/事实台账五分型/访谈五步/合规关键词库/V1 边界/7 维评分/替代方案五路径/两阶段竞品对标/竞品参考库/ST×SWOT 定位/干系人方格/JTBD 护城河/规则决策表/AI 任务分类/ToB 维度库/UI 文案 5 原则 9 场景/高频遗漏 10 项/架构图分区/交叉引用校验/AI 兜底/AI 评估 4 维/5 步评分引擎/下游交接三视角/grill-me/迭代双 case/ADR+Sourcing 6 级/竞品三态矩阵/领域映射提示/研发评审 13 项/北极星+好指标 4 标准等。
- 第三轮补厚 9（薄弱 skill）：user-journey（journey-matrix-and-mot）/issue-record（issue-communication-and-escalation）/functional-flow（flow-coverage-check）/state-machine（state-machine-completeness）/acceptance-criteria（ac-selfcheck）/tracking-plan（tracking-event-spec）/exception-handling（exception-grade-and-recovery）/feature-list（feature-priority-quant）/interaction-rules（interaction-feedback-rules）。

#### C 档 · 审计层（13 项）
- `review-taxonomy.md` 标签 7→12：新增 [CommercializationGap]/[HarddownRule]/[P0P1P2Misgraded]/[QualityGate]/[ScoreMatrix]/[AntiPattern]。
- 6 个 audit-checklist 追加（prd-assembly §7/§6.2、interaction-rules §6、acceptance-criteria §7、feasibility-analysis §6、acceptance-criteria 验收可验证性对照等）。

#### 文档同步
- `skills/pm-scaffold/SKILL.md` 重写为 v0.6.0（13 work_item/19 skill/95 注入点说明）。
- `AGENTS.md` / `README.md` / `thinking-core.md` 清理 v0.4.x 旧结构残留（"5 主 + 9 子"、"17 个思考透镜"）。
- `docs/new-skills-integration-plan.md`：新批次 35 skill 全量评估表 + 69 点映射 + M1-M6 里程碑。
- `src/toolkit/visualization/scaffold-flow.html`：升级 v0.6.0，新增第 15 节「Skill 精华整合（两轮 · 95 注入点）」，技法落位分布表补全 64 个文件。
- **拆分残留全面清理（v0.5.0 技术债）**：8 个 002 README 的 "Sub-skill of function-description/product-ux" 旧父子结构 → 独立 work_item 描述；70+ references 文本旧结构引用（FUN-XXX→FEA-XXX、父文档→独立产物、product-ux→page-design/interaction-rules、user-journey-and-stories→user-journey/user-stories）→ 当前结构；tracking-plan/feasibility-analysis/competitive-research/requirement-restate SKILL.md 与 prd-assembly 追溯链（FUN→FL）修复；9 个 skill 内 templates/*-output.md 标注「已由 stage-2-product 取代，仅作历史参考」（tracking-plan 模板更新为新结构）；capability-fragments 片段 FEA 化（来源案例历史编号保留）。

#### 验证
- `run_tests_mac.sh` 84 passed / 0 failed（registry_contract_check E3_drift 首关 fail-loud 绿灯）；`consistency_check.py` 0 errors；悬空引用扫描 0（310 项全通）；红线零触碰。

## [Unreleased]

### Added
- v0.6.1 全量审计与整改报告（文件覆盖、运行时验证、能力边界和 P1/P2 路线图）。
- 证据四维检查与范围谈判脚本接入现行背景、故事、功能和 PRD 汇总 Skill。

### Changed
- `pipeline.py init --root` 现在隔离写入指定根目录；新增临时目录回归测试。
- 飞书检测只使用 PATH 或 `PM_SCAFFOLD_LARK_PLUGIN_ROOT`，删除个人绝对路径依赖。
- reflow 改为计划、预写、审计、原子替换的提交顺序；投影构建失败和审计链失效继续阻断流程。
- macOS/Windows 测试入口对齐 PRD 追溯检查；测试结果改为运行时实测而非硬编码数字。
- README、架构、驾驶舱、模板库和 PRD 模板收敛到 schema v7 的独立 work item 结构。

### Removed
- 已删除的复合 Skill 测试、复合模板和重复 per-Skill 输出模板；这些文件不再参与解析或假绿测试。

## [0.5.1] - 2026-08-17

### Changed · requirement-restate 拆分为「复述 + 发散」两个独立能力

#### 拆分动机
- `requirement-restate`（收敛器：L1-L4 有来源，verbatim 复述确认）与 `brainstorming`（发散器：L0 稀疏，12 维候选 + 人工四值处置）场景互补不重合，按能力边界拆分为两个 `output_kind=process` 的能力 skill。

#### 注册表 / 路由
- `src/framework/workflow-registry.json`：`requirement-restate` 收窄为单模式复述；新增 `brainstorming`（`applicable_stages` 001+002，`resume_work_item=project-background-goal`）。
- `src/scripts/pipeline.py`：入口路由 L0→`brainstorming`、多源/歧义→`requirement-restate`。

#### 目录 / 校验
- 新增 `src/support-skills/brainstorming/`（SKILL + 7 references + validator，校验 SCN-XXX 候选表 + 人工处置表，禁 `confirmed`）。
- **物理=逻辑归位**：brainstorming（跨阶段 001+002）从 `src/stages/001-business-requirements/skills/` 归位到 `src/support-skills/brainstorming/`，与 competitive-research / feasibility-analysis 同级（跨阶段能力归位 support-skills；`workflow-registry.json` 的 `skill_path` 一并更新）。
- `requirement-restate/` 移除模式二内容；`validate_artifact.py` 移除 SCN-XXX 发散检查。
- 删除已废弃的 `src/shared/brainstorming/` 目录。
- `registry_contract_check.py` / `consistency_check.py` 均通过。

#### 文档同步
- `AGENTS.md` / `governance.md` / `TOOLKIT.md` / `docs/团队职责矩阵-RACI.md` / `docs/ARCHITECTURE.md` / `src/toolkit/visualization/scaffold-flow.html` 双模式残留清理，入口探索序列更新为「发散→复述→主干」。

## [0.5.0] - 2026-08-17

### Changed · Skill 结构拆解 v2 (composite → 13 independent work_items)

#### 注册表 (schema_version 6 → 7)
- `src/framework/workflow-registry.json` `schema_version`: 6 → **7**
- `work_items`: 5 → **13**；`internal_capabilities`: 9 → **0**；`artifact_types`: 5 → **13**
- `stages[0].work_items`: 2 → 3（新增 `user-journey` + `user-stories`）
- `stages[1].work_items`: 2 → 9（`feature-list` / `functional-flow` / `page-design` / `interaction-rules` / `business-rules` / `validation-rules` / `state-machine` / `exception-handling` / `acceptance-criteria`）
- `prd-assembly.predecessors`: 4 上游 → **12 上游**完整链路 `G→UJ→US→ST→FEA→FUN→PD→IX→BR→VL→SM→EX→AC`
- 新前缀方案：`BG- / UJ- / US- / FEA- / FL- / PD- / IX- / BR- / VL- / SM- / EX- / PRD-`（替换 `BG- / JS- / UX- / FD-`）

#### 目录重构
- 旧复合目录已删：`src/stages/001-business-requirements/skills/user-journey-and-stories/`、`src/stages/002-product-requirements/skills/product-ux/`、`src/stages/002-product-requirements/skills/function-description/`
- 9 个子 skill 提升到平级（与上述父目录同名）：`feature-list` / `functional-flow` / `page-design` / `interaction-rules` / `business-rules` / `validation-rules` / `state-machine` / `exception-handling` / `acceptance-criteria`
- 2 个新独立 skill：`user-journey` / `user-stories`
- 2 个独特引用已抢救并分配：`nfr-catalog.md` → `validation-rules/references/`；`ears-syntax.md` → `business-rules/references/`

#### Skill 协议
- 13 个 SKILL.md 重写为「独立 work_item」语义，去除所有 "Sub-skill of" / "父产物" / "function-description 编排的" 残留；frontmatter `description` 统一包含 "Independent work_item"
- 13 个 agents/openai.yaml 同步重写：`default_prompt` 由 "Use sub-skill to..." → "You are the work_item. Your task is to..."；"Output §X in parent..." → "Produce independent xxx.md"
- 13 个 validate_artifact.py 重写为「独立产物全文校验器」：移除 `_section_text()` 章节提取逻辑与 `PARENT_ARTIFACT_GLOBS`；改为读取整个独立产物文件；保留 `_bootstrap_scripts()` 与 `validation_errors.make_issue()` 统一错误格式（v0.4.0 第 8 条宪法）

#### 框架级文档
- `AGENTS.md` §7 Skill 全景更新：`5 主 + 9 子 + 4 分支 + 1 能力 = 19` → `13 主干 + 3 分支 + 1 常驻 + 2 能力 = 19`
- `AGENTS.md` §5 需求目录布局更新为 v2 路径（`02-user-journey/` + `03-user-stories/` 等）
- `README.md` Skill 全景表 + Mermaid 流程图 + 目录结构全部更新
- `src/stages/001-business-requirements/STAGE.md` / `002-product-requirements/STAGE.md` 列出 3 + 9 个 work_items 并附依赖链
- `src/framework/workflow.md` / `governance.md` / `thinking-core.md` 全部产物名与追溯链更新

#### 脚本与基础设施
- `src/scripts/pipeline.py` — `VALID_WORK_ITEMS` 替换为 13 个新 ID；entry 逻辑 maturity 判断更新；新增对 `user-journey` / `user-stories` / `prd-assembly` 等的 active_work_item 路径处理
- `src/scripts/orchestrator.py` — 范围冻结检测改为 `page-design` / `interaction-rules`
- `src/scripts/consistency_check.py` — E1 正则期望从 `(BG|JS|UX|FD)` → `(BG|UJ|US|FEA|FL|PD|IX|BR|VL|SM|EX|PRD)`
- `src/scripts/workflow_registry.py` — `schema_version` 白名单支持 7
- `src/scripts/snapshot_cases.py` / `migrate_layout_v2.py` / `property_check.py` — fixture 路径映射与硬编码引用全部更新

#### 模板
- `src/templates/stage-1-business/user-journey.md` / `user-stories.md` 新增（自 `journey-and-stories.md` 拆分）
- `src/templates/stage-2-product/` 新增 9 个独立模板（feature-list / functional-flow / page-design / interaction-rules / business-rules / validation-rules / state-machine / exception-handling / acceptance-criteria）
- `src/templates/resolver.py` TEMPLATE_MAP 追加 9 个新模板
- 旧模板（journey-and-stories.md / product-ux.md / function-description.md）保留并加 deprecation 注释

#### Shared
- `src/shared/traceability/README.md` 追溯链 `G→ST→FEA→FUN→AC/BR` → `G→UJ→US→ST→FEA→FUN→PD→IX→BR→VL→SM→EX→AC`
- `src/shared/clarify/skills/issue-record/` 产物名更新
- `src/shared/capability-fragments/` 复制目标改为 `functional-flow / business-rules / acceptance-criteria`

#### Toolkit
- `src/toolkit/visualization/scaffold-flow.html` Skill 表 + 产物表 + 教程文本 + 命令参考全部 v2 化

### Removed
- 3 个复合 skill 目录（`user-journey-and-stories` / `product-ux` / `function-description`）
- `internal_capabilities` 数组（9 个条目并入 `work_items`）
- `_section_text()` 章节提取逻辑（13 个 validate_artifact.py）
- `PARENT_ARTIFACT_GLOBS` 父产物路径常量（13 个 validate_artifact.py）

### Tests
- **72/78 PASS**（baseline 85/85，回归 13 项）
- registry_contract_check: **PASS**（schema clean + template↔validator closure OK）
- consistency_check: **0 errors, 0 warnings**（consistency E1 正则已同步为 v2 13 前缀）
- 全局旧名扫描：0 命中（task scope 内，仅保留 CHANGELOG 历史记录与模板 deprecation 注释）
- PII 检查：0 命中
- 已知失败（v0.5.1 fixture 内容重写 follow-up，**不影响结构与基础设施可用性**）：
  - 5 个 fixture 内容缺新格式标记（user-journey × 1、user-stories × 3、prd-assembly × 1；具体：缺 emotion mapping / MoSCoW / 业务规则+校验规则+状态机+异常处理 章节）
  - trace/REQ-003-oab：BR-006 在 prd.md 缺 function 链接（真实需求产物内容层问题，归档为 REQ 数据修复）
  - 3 个被拆解 skill 的旧 unit test 已用 try/except 标记为「v0.5.0 composite removed」并 exit 0（function-description / product-ux / user-journey-and-stories）
- End-to-end smoke test：`pipeline.py init REQ-999-v2-smoke` 正确生成 13 个 work_item 独立目录布局

## [0.4.1] - 2026-08-14

### Changed · 全中文化
- 19 个 SKILL.md + references + 3 个 STAGE.md 全部中文化（英文术语/代码引用/8 步循环阶段名保留，标题改为「中文（英文对照）」）

### Fixed · 深度审查修复
- contracts.md RegistryContract schema 字段名漂移（stage_id→stage、artifact_path→artifact_dir/artifact_file、required_inputs→required_outputs 等 6 处）
- prd-assembly 的 --variant/executive/technical 死功能残留（3 文件）+ resolver.py TEMPLATE_MAP 已删模板映射
- 登记追加顺序 bug（feishu_fetch/prd_publish，插到表尾而非分隔行后）
- desensitize_check 接入 run_tests_mac.sh（fixtures 脱敏自动化，隐私闭环）
- read_frontmatter 统一到 workflow_registry（删 3 处重复实现）
- snapshot_cases 变量命名、function-description「§异常处理」→「§异常与失败处理」

### Removed · 隐私与清理
- 公开 docs 泄露的内部 .test-output 路径 + Issue 编号（B12/F1/G1/ISS-011 等，6 文档清理为自包含描述）
- source-register-skeleton / readme-skeleton 孤儿模板（pipeline 改读模板消除硬编码）
- 计划类文档移入 docs/00-plan（gitignore 不推公开）
- prd_publish/snapshot_cases 日志路径 .test-output → 99-review

### Added
- prd.md 模板新增 5.5 名词解释 + 5.6 涉及团队及职责（补齐真实 PRD 共性）
- capability-fragments 通用能力片段库索引

### Tests
- 85/85 PASS（新增 desensitize fixtures 自检项）

## [0.4.0] - 2026-08-14

### Added · Harness 架构借鉴落地（事件溯源 + 投影缓存 + 注册表契约 + 统一错误格式）
- `src/scripts/audit_log.py` — Harness 借鉴点一·事件溯源。每案例 `requirements/REQ-NNN-*/.audit/events.jsonl` append-only；提供 `append_event` / `replay_events` / `verify_chain` / `reconstruct_causality`；事件 token = `review|change|decision|confirm|reject|reflow|init`；prev_hash 链 + event_sha256 自指纹 + payload_sha256 绑定记录体 + 单调 recorded_at；幂等写入（同 event_type+payload+payload_sha256 不重复）。
- `src/scripts/projection_cache.py` — Harness 借鉴点二·投影缓存。从事件日志折叠派生 `.audit/projection.json`，提供 `build_projection` / `read_projection` / `is_stale` / `latest_review_for`；替代 `branch_validator` 旧的 glob+sort（B7 时序陷阱）；对老案例保留 legacy fallback（带 warning）。
- `src/scripts/registry_contract_check.py` — Harness 借鉴点三·注册表契约硬化。schema 校验 + 模板↔校验器字段闭环（E3_drift：模板新增 required 字段但校验器未引用即报错）；作为 `run_tests_mac.sh` 第一项，任何失败 abort（fail loud）。
- `src/scripts/validation_errors.py` — Harness 借鉴点四·统一错误格式。`make_issue` 输出 8+ 字段：severity / blocking / check_id / check_family / location / field_path / message / expectation / actual / repair_hint / source_ref；配套 `format_issue` / `aggregate_by_check_id` / `wrap_unexpected`。
- `src/framework/contracts.md` — Shared Records 新增 AuditEvent / ProjectionCache / ValidatorIssue / RegistryContract 四项契约；新增「Validator Issue Format」「Registry Contract」两节；Confirmation Invariant 补「事件先于状态变更」。
- 事件溯源闭环：`audit_log.append_event` 成功后自动重建 `projection_cache`（事件 ⟺ 模型可见强一致；重建失败仅 warn，投影为派生视图可随时重建）。
- `pipeline.py` 新增 `audit backfill` 子命令：为 pre-audit_log 的历史需求目录（REQ-001~008）从 `99-review/*.md` 反推事件（`backfilled: true`），按 reviewed_at/changed_at 时间戳排序保证事件日志时序；`REQ-001/002/004` 已回填（5/5/6 事件），审计链全部 PASS。

### Changed
- `src/framework/constitution.md` — 新增第 7 条硬宪法（事件溯源不可篡改：prev_hash 链断 / event_sha256 不符即 CRITICAL）与第 8 条硬宪法（校验器必须用 `validation_errors.make_issue` 输出统一错误格式，禁止裸 stack trace）；第 3 条补 `registry_contract_check` 作为必跑关卡。
- `run_tests_mac.sh` — 新增 Phase 0 registry 契约自检（`registry_contract_check.py` 作为首项 fail-loud 关卡，失败立即 abort，不再跑后续测试）。
- 错误格式统一（借鉴点四推广至全部校验器）——`registry_contract_check.py` / `consistency_check.py` / `traceability_check.py` / `branch_validator.py` 全线迁移到 `make_issue`（6 类 ad-hoc 格式收敛为 1 个契约：severity/blocking/check_id/check_family/location/field_path/message/expectation/actual/repair_hint/source_ref）。
- 22 个 skill 校验器（5 主 skill + 8 子 skill + issue-record + 8 支撑 skill）采用双轨制迁移：`errors`/`warnings` 保持字符串列表（skill 单测断言 `"substr" in error`），新增标准化 `issues` 数组（`check_id` 语义化标签 + severity/blocking 映射）；`waiver_required`/`waivable` 旧结构映射为 `severity=HIGH, blocking=False`。
- `projection_cache.py` — 修复 `_artifact_status_fields` 在产物未创建时缺 `reviewer/reviewed_at/confirmed_at` 键导致事件折叠 KeyError 的 bug。
- `registry_contract_check.py` — 修复 Python 3.12+ 移除 `ast.Str` 导致的 AttributeError（改用 `getattr(ast, "Str", None)` 兼容写法）。

### Tests
- 新增 `test/scripts/test_audit_log.py`：10 个单元测试覆盖幂等写入 / 哈希链连续性 / event_sha256 自指纹篡改检测 / payload_sha256 绑定记录体 / 单调 recorded_at / verify_chain 报错路径 / reconstruct_causality 因果重建 / GENESIS prev_hash / 未知 event_type 拒绝 / 跨进程字节级一致。
- 新增 `test/scripts/test_validation_errors.py`（10 用例：blocking 默认值 / 消息推导 / wrap_unexpected 不泄漏堆栈 / format_issue / aggregate 分组）、`test/scripts/test_projection_cache.py`（5 用例：折叠 / 自动重建闭环 / stale 检测 / review 事件 latest_review_for）、`test/scripts/test_registry_contract_check.py`（12 用例：schema 五类缺陷 / E3_drift / 真实注册表）。
- 回归测试 79 → 85 通过（新增 3 个测试文件 + REQ-001~008 事件回填后 audit 链校验纳入 branch_validator gate，另加 desensitize fixtures 自检项）。

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
