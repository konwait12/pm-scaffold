# L0/L1 分档重建与产物契约优化计划

> 状态：2026-08-20 权威计划。本文定义当前运行时、产物和验收契约；旧计划仅用于历史追溯。

## 统一 PRD 章节契约（首要规则）

L0、L1、L2 的最终 PRD 均使用现有 L2/v8 模板的同一组 canonical 章节：§1 项目背景、§2 项目范围、§3 用户旅程、§4 用户故事、§5 功能清单、§6 功能流程、§7 原型/UX、§8 交互规则、§9（含 §9.1-§9.4 业务规则子节）、§10 验收依据、§11 按需章节，以及统一的追溯矩阵和自审记录。档位只改变工作项数量、证据深度、治理强度和装配路径，不改变章节编号、标题或含义。

每个主章节及 §9.1-§9.4 必须声明 `required`、`conditional` 或 `not_applicable`。`not_applicable` 必须包含事实依据、来源引用、判断人和判断时间；`conditional` 必须包含触发条件、当前判断和复审触发点。禁止删除章节、泛化 N/A 或用“本期不做”替代决策。L0 的 `mini-prd` 只是紧凑事实采集/起草工件，在一次人工确认中必须确定性映射到完整 canonical PRD。

入口先选择需求难度：低难度不触发档位建议；中/高难度触发 L1/L2 建议。建议只作只读提示，最终档位由人工确认并持久化到 `intake-decision.md`，不允许自动切档。

## 产物清单

| 产物 | 最终调整 | 验收结果 |
|---|---|---|
| `docs/tier-l0-l1-rebuild-plan.md` | 唯一权威计划，定义 L0/L1/L2 边界、治理、迁移和验收 | 不与旧 v3.1/v4 规则冲突 |
| `00-input/intake-decision.md` 与模板 | 每个 REQ 的持久化档位事实源，含 owner、证据、资格矩阵、L2-only 适用性和升级理由 | 所有命令从同一事实源解析档位 |
| `src/shared/intake-routing/references/process-tier-routing.md` | 资格矩阵与硬升级条件，评分仅作建议 | 无累计评分矛盾 |
| `pipeline.py`、`orchestrator.py`、`dor_check.py`、`workflow_registry.py` | 初始化、状态、闸门、评审、回流统一执行持久档位，跨档 fail-loud | 不可通过临时参数切档 |
| REQ 初始化模板与目录 | `init` 必须显式选择 L0/L1/L2，只创建公共目录和当前档位 work item | README/目录投影与档位一致 |
| `src/stages/000-minimal/skills/mini-prd/` | 单产物 L0，六个核心章节，条件化记录风险/质量/发布/指标/术语 | 快速交付但不丢边界、验收、回退和未决项 |
| mini-PRD validator、fixtures、E2E | 校验真实内容、来源、可观察验收、回退依据、开放问题 owner 和升档信号 | 不以标题或空泛 N/A 冒充质量 |
| L1 registry 与 PRD assembly contract | 7 个上游 + `prd-assembly`，共 8 个 work item | 文档、状态和测试统一 |
| PRD assembly manifest/hash 链 | 记录 confirmed 来源、相对路径、内容哈希、目标章节；装配后验证源和来源块未被改写 | 最终 PRD 只能聚合已确认内容 |
| L1 适用性决策 | PD/IX/VL/STATE/EX 逐项记录不适用事实；任一适用即升级 L2 | 不把缺失工程细节伪装为完整 |
| README、AGENTS、框架文档、`scaffold-flow.html` | 同步真实运行时、档位目录、8 项 L1、L0 治理和当前测试口径 | 文档可直接操作 |
| 历史计划 | 保留并添加 `superseded_by`、日期和失效范围 | 可追溯但不会误导执行 |
| 回归与验收测试 | 覆盖三档初始化、跨档阻断、L0 审计、L1 manifest 篡改和 L2 兼容 | 以行为验收，不固定测试数量 |

## 当前判断

已保留的基础改动包括注册表 tier 字段、L1 集内前置豁免、L0 单产物目录、持久化 intake 决策、跨档阻断和 L0 的 ReviewRecord/hash anchor/audit event。旧 v4 中 L0 扩为 12 个强制章节、累计评分、不可核验的逐字移植、L1 写成 7 项（遗漏 PRD assembly）及固定测试数量均不再有效。

## 权威交付定义

### L0

适用于单一可定位变更、单角色、无持久状态、无敏感/资金/合规影响、无数据迁移且只有简单回退的需求。保留六类事实采集 `mini-prd.md`，但它不是最终 PRD；一次人工确认中映射到完整 canonical 章节并完成适用性判断。L0 不要求完整上游链或 issue-record，但保留一次真实人工确认、ReviewRecord、hash anchor 和 audit event。

### L1

适用于标准、受限场景。七个上游为 `project-background-goal`、`user-journey`、`user-stories`、`feature-list`、`functional-flow`、`business-rules`、`acceptance-criteria`，加 `prd-assembly` 共 8 个 work item。PD、IX、VL、STATE、EX 进入适用性矩阵；只有事实化依据才能标记 `not_applicable`，任一项实际适用或依据不足即升级 L2。最终 PRD 仍保留完整 canonical 章节。

### L2

有状态、交互、验证、异常、合规、多角色、多系统或数据迁移需求的默认完整路径。既有无 intake 的 REQ 按 L2 兼容运行，并输出迁移提示；不得降低既有 v7/v8 产物语义。

## 实施规则

1. 新建 REQ 必须执行 `pipeline.py init REQ-NNN-topic --process-tier L0|L1|L2`。`intake-decision.md` 是唯一持久事实源，README 仅为投影。
2. `status` 可用 `--process-tier` 展示预览差异；`gate`、`review`、`reflow`、发布和装配只能使用持久档位，跨档 work item 在任何写操作前失败且不产生审计副作用。
3. 路由采用资格矩阵和硬升级条件。评分（若显示）不能覆盖硬条件。
4. L1/L2 assembly manifest 必须列出允许上游的 artifact ID、相对路径、`confirmed` 状态、内容 SHA-256 和目标章节。装配器按确定性映射嵌入源正文并写入来源块标记；源文件或来源块被改动必须失败。
5. 外部参考只可沉淀为可独立验证的抽象原则；没有可复核原文件和授权时，不声称逐字复制。

## 迁移与文档

既有 REQ 优先读取已有 intake；缺失时按 L2 兼容并提示补录。README、AGENTS、`src/framework/{workflow,governance,contracts}.md`、注册表说明和 `scaffold-flow.html` 必须展示当前档位命令、L0 六类事实采集到 canonical PRD 的投影、L1 八项及真实审计语义。历史计划保留，不删除用户工作区内容。

## 验收矩阵

- 三档临时 REQ 的目录、README 当前项、intake、status、gate、review、audit event 和 hash anchor 行为正确。
- L0 合法单点需求通过；多模块、PII、持久状态、多角色或复杂异常在 init/gate 时指向 L1/L2。
- L1 七个上游和 PRD assembly 共八项顺序完成；缺少五项不适用依据、声明 L2-only 上游或发现适用能力时升级 L2。
- 未确认来源、伪造 artifact ID、源文件装配后修改、PRD 来源块手改均失败；合法 L1 与冻结 L2 fixture 继续通过。
- `bash run_tests_mac.sh`、registry/consistency 检查和 `git diff --check` 通过。测试数量随实现变化，不写固定 93/95 承诺。

## 默认决策

不执行 12 节强制 L0，不新增不可验证的 `industry` frontmatter，不在 L1 PRD 填泛化 N/A，不删除历史计划，不复制来源不明的文本；保留 L0 审批留痕并将其写成正式治理契约。
