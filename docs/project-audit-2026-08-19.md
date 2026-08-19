# Project_001 全量审计与整改报告

> 日期：2026-08-19  
> 现行基线：`src/framework/workflow-registry.json`（schema v7）  
> 审计范围：所有非 `.git` 文件、未提交改动、需求实例、模板、Skill、脚本、测试与运行时残留。  
> 外部参考：WorkBuddy `skills-index.md` / `skills-index.csv`；GitHub `main` 与本地 HEAD 同为 `914c076`，无可合并的新上游实现。

## 1. 执行摘要

项目的强项是可验证的治理内核：注册表、前置依赖、人工确认、ReviewRecord 哈希绑定、追加式审计日志和投影缓存形成了闭环。整改前的主要风险集中在运行隔离、可移植性、旧复合结构残留和“测试看似通过”的偏差；本轮已完成对应 P0/P1 修复，并把活动内容收敛到 13 主干 work item 与 6 支持能力。

当前评分：

| 维度 | 权重 | 整改前 | 整改后 | 依据 |
|---|---:|---:|---:|---|
| 核心正确性与状态不变式 | 30% | 26 | 28 | 根目录隔离、投影失败阻断、审计链与 reflow 提交顺序 |
| 工作流与人工闸门完整性 | 20% | 15 | 18 | 13 项独立链路、授权评审、跨平台追溯 |
| PRD/产品方法质量 | 20% | 16 | 18 | 现行 PRD 模板分解为 registry v7 章节，证据/范围实践接入 |
| 可维护性与可测试性 | 15% | 9 | 13 | 删除 false-green 旧测试，补关键运行时回归 |
| 安全、隐私与可移植性 | 10% | 6 | 8 | 去除个人绝对路径，PATH/环境变量飞书检测 |
| 扩展与集成能力 | 5% | 4 | 4 | 保持可选适配器边界，不扩展隐式工作流 |
| 总分 | 100% | 76 | 89 | 可作为当前发布候选，剩余事项见第 8 节 |

## 2. 范围、证据与排除项

- 文件覆盖：执行 `find . -path './.git' -prune -o -type f -print`，覆盖 717 个非 Git 文件。源文件、文档、模板、测试、资产、需求实例、缓存和运行时产物均纳入分类检查。
- Git 内部对象不审计内容；`.DS_Store`、`__pycache__`、`.test-output`、`requirements/` 作为卫生与数据边界检查对象。
- 现有测试只作为一条证据线。独立证据包含临时目录初始化、飞书探测 mock、审计事件篡改、投影构建失败、reflow 提交和注册表闭包。
- WorkBuddy 索引的 840 条记录、729 个唯一名称及自动标注仅用于发现候选能力，不视为事实或直接依赖。

## 3. 文件覆盖与仓库卫生

| 类别 | 当前判断 | 整改状态 |
|---|---|---|
| 注册表、主干 Skill、核心模板 | 13 项均有独立路径、契约与校验器 | 已核验 |
| 支持能力 | competitive research、feasibility、restate、brainstorming、tracking、issue record | 已核验 |
| 旧复合模板与测试 | 不再有 resolver 入口或可执行测试 | 已删除 |
| 运行时需求实例 | 保留为历史数据；不作为现行模板或质量唯一依据 | 已隔离 |
| 缓存/系统文件 | 仍可能存在本地缓存，必须由 `.gitignore` 排除 | 持续治理 |

完整文件清单不在本文硬编码，以免再次成为过时快照。复核命令：

```bash
find . -path './.git' -prune -o -type f -print | sort
git status --short
```

## 4. 已修复问题

| ID | 严重度 | 证据位置 | 修复与验证 |
|---|---|---|---|
| F-001 | High | `src/scripts/pipeline.py` | `pipeline.py init <name> --root <dir>` 现在实际写入目标根目录；`test_init_root_isolated_from_repository` 覆盖。 |
| F-002 | High | `src/scripts/pipeline.py` | 删除 `/Users/...` 插件路径；只查 PATH 或 `PM_SCAFFOLD_LARK_PLUGIN_ROOT`。无配置和显式插件根目录均有回归测试。 |
| F-003 | High | `run_tests_win.ps1` | Windows 入口补齐与 macOS 同等的非 simulated PRD 追溯检查。 |
| F-004 | High | `src/scripts/branch_validator.py` | 审计链无效为 CRITICAL，投影构建失败为阻断 HIGH；legacy lookup 只作诊断。 |
| F-005 | High | `src/scripts/pipeline.py` | reflow 先收集计划、预写临时文件、追加事件，再原子替换产物；失败前不修改 live artifact。 |
| F-006 | Medium | `test/skills/*` | 删除旧复合 Skill 测试及其 `sys.exit(0)` 假绿包装；现行单测正常传播失败。 |
| F-007 | Medium | `src/templates/**`、`src/templates/resolver.py` | 删除旧复合模板和重复的 per-Skill 输出模板，所有 README 指向当前 core template。 |
| F-008 | Medium | `docs/ARCHITECTURE.md`、`README.md`、驾驶舱 | 活动说明改为 v0.6.1、13 主干/6 支持能力、动态测试数；历史仅在 CHANGELOG 保留。 |
| F-009 | Medium | `src/templates/stage-3-prd/prd.md`、PRD validator | PRD 模板和 validator 改为独立 user journey、stories、feature、flow、page、interaction、rules、state、exception、acceptance 章节。 |
| F-010 | Medium | 4 个现行 SKILL.md | WorkBuddy 启发的证据四维检查和范围谈判脚本已接入 project background、stories、feature list 与 PRD 汇总。 |

## 5. 架构与运行时结论

1. `workflow-registry.json` 是机器唯一真相。legacy artifact fields 仅供历史需求迁移探测，不能作为当前路径或模板入口。
2. `confirmed` 只允许授权人工的 `review --decision approve` 写入；确认内容、ReviewRecord、hash anchor 与事件链相互校验。
3. PRD assembly 只能聚合已确认上游内容。模板、validator 和 traceability check 不允许借汇总阶段新增需求。
4. 审计事件是事实源，projection 是可重建视图；投影异常不得降级为“成功”。
5. 飞书、研究、原型、文档导出均应保持可选适配器角色，不能改变主干依赖或人工闸门。

## 6. Skill 与模板评估

所有现行主干 work item 必须具备 `SKILL.md`、`agents/openai.yaml`、references、core template 和 validator。正向 fixture 证明有效产物，`*violation*` fixture 证明校验器会拒绝真实失败模式；不存在的旧复合能力不再伪装成测试覆盖。

新增的外部能力采用受控接入：

| 主题 | 结论 | 集成边界 |
|---|---|---|
| 证据质量 | 已有但补强 | 四维检查只审 FACT/DECISION 支撑，不替代人工判断 |
| 范围谈判 | 已有但补强 | 只在 stories/feature clarify 中记录取舍，不新增阶段 |
| 联网/竞品研究 | 已有按需能力 | 作为 candidate evidence，必须落来源与知识状态 |
| 原型与 Figma | 已有但受限 | 允许上游嵌入，不把视觉产物当业务事实 |
| 文档导出/企业协作 | 可选适配器 | 以 PATH、配置和脱敏为前提 |
| 自动多 Agent 编排 | 暂不引入 | 会扩大授权和状态机复杂度，优先保持当前审计边界 |

## 7. 验证结果

```text
bash run_tests_mac.sh
Result: 85 passed / 0 failed

python3 src/scripts/registry_contract_check.py
PASS registry contract: schema clean + template↔validator closure OK

python3 src/scripts/consistency_check.py
Result: 0 errors, 0 warnings
```

额外运行：`python3 test/scripts/test_workflow_runtime.py`，17 tests passed，覆盖临时 root、飞书检测、人工确认、投影/追溯和 reflow。

## 8. 剩余风险与路线图

| 优先级 | 项目 | 前置依赖 | 验收标准 |
|---|---|---|---|
| P1 | 以 PowerShell 原生命令替换 `Invoke-Expression` | Windows CI | Windows 执行路径无字符串拼接命令 |
| P1 | 将 `requirements/` 历史实例分级为 current/legacy | 迁移策略和人工确认 | legacy 实例不再被当作当前结构 fixture |
| P1 | 缓存与运行时清理自动化 | `.gitignore` 与 CI | 全新 clone 的测试不会产生可追踪残留 |
| P2 | 真实 Windows CI 验证 | Windows runner | 与 macOS 的注册表驱动检查结果一致 |
| P2 | 可选 research/prototype/export adapters | 授权、来源和脱敏契约 | 每项新适配器有超时、失败处理、fixture 与人工边界 |

## 9. 后续验收

- 任一新增 work item 必须同步 registry、template、validator、正负 fixture、README 和驾驶舱。
- 任一新增外部能力必须记录来源、许可证/授权边界、超时、脱敏与失败降级策略。
- 每次发布以实际 `run_tests_mac.sh` / Windows CI 结果更新，而不是手写通过数。
- 不以 GitHub 项目名或 WorkBuddy 自动标签替代源码证据和人工确认。
