# 计划 v5：精华蒸馏融合（workbuddy Skill → pm-scaffold）

> 来源：[prd-pm-skills-verified.md](../prd-pm-skills-verified.md)（842 个 skill 中亲读过的 PRD/PM 高质量子集）
> 原则：蒸馏 → 融合 → 不制造项目自身矛盾。
> 与既有三套分层的关系：三套分层（阶段/章节/Tier）已稳，本计划**只补强文档级与轻量校验级**产物，不动流程引擎，不破既有回归。

## 0. 蒸馏红线（不制造项目自身矛盾）

| 红线 | 守则 |
|---|---|
| 流程引擎不动 | pipeline / orchestrator / dor_check / tier 过滤逻辑零改动 |
| 13 产物 + mini-prd 不增不减 | 仅给现有产物/技能**追加 references/** 蒸馏文档 |
| 校验器契约不冲突 | 新增蒸馏文档若被 validate_artifact 引用，必须先验证契约兼容 |
| 宪法底线不动 | confirmed 不可变 / AI 不替业务决定 / 来源可追溯 三大红线 |
| 回归红线 | 每个新增文件必须加至少 1 个回归用例；run_tests_mac.sh 必过 |
| 文档优先 | 蒸馏优先文档级（references/*.md），其次脚本级（validate_artifact.py），最后工作流级 |

## 1. 蒸馏清单（P0 = 文档级零风险，先做）

| P# | 来源 skill | 蒸馏内容 | 蒸馏目标 | 风险 | 验收 |
|---|---|---|---|---|---|
| P0-1 | A4 incremental-prd-collaboration | 高频遗漏检查清单（按钮文案、异常状态、阻断文案等）+ 产品边界（业务/规则/状态/文案/验收，不滑向 API/字段）| 新建 `src/stages/003-prd-output/skills/prd-assembly/references/incre-prd-checklist.md`，并在 [SKILL.md](file:///Users/edy/Desktop/workspace/01_项目仓库区/Project_001_产品AI脚手架/src/stages/003-prd-output/skills/prd-assembly/SKILL.md) §Audit 之前加 §Red-Review 步骤引用 | 零：纯 reference 文档 | 模板内出现高频遗漏案例覆盖度≥80% |
| P0-2 | F1 mermaid-diagram | 完整图类型选择表（流程/时序/状态/脑图/ER/时间线/用户旅程）+ 常见语法错误 | 新建 `src/shared/visualization/mermaid-style-guide.md`，所有 skill 的 `references/` 引此文档 | 零：纯文档 | 各 skill 引用一致 |
| P0-3 | B1 prd-reviewer | 10 分制 7 模块评分 + 3 大绝对红线 + 17 项快速检查清单 | 升级现有 [prd-scoring-rubric.md](file:///Users/edy/Desktop/workspace/01_项目仓库区/Project_001_产品AI脚手架/src/stages/003-prd-output/skills/prd-assembly/references/prd-scoring-rubric.md)，新增"研发评审版 PRD 硬标准"段 | 零：升级文档 | 含 3 红线 + 17 项 |
| P0-4 | A2 prd-development | "每个字段要描述其状态及状态间转变条件" — 与 BR/VL/STATE/EX 四个产物的契约一致 | 在 [prd-assembly/SKILL.md](file:///Users/edy/Desktop/workspace/01_项目仓库区/Project_001_产品AI脚手架/src/stages/003-prd-output/skills/prd-assembly/SKILL.md) §Generate 写一段"状态不变式提示"，引用现成业务规则与状态机产物 | 零：文档提示 | §Generate 含 1 行引用 |
| P0-5 | A4 高频遗漏精简版（5 条）| [mini-prd/SKILL.md](file:///Users/edy/Desktop/workspace/01_项目仓库区/Project_001_产品AI脚手架/src/stages/000-minimal/skills/mini-prd/SKILL.md) §Self-Audit 加 5 条 L0 自检 | 零：扩展既有自检 | §Self-Audit 5 条升级 |

## 2. 蒸馏清单（P1 = 轻量脚本级，零流程改动）

| P# | 来源 skill | 蒸馏内容 | 蒸馏目标 | 风险 | 验收 |
|---|---|---|---|---|---|
| P1-1 | A4 增量评审 rubric（与 P0-3 互补）| 把 P0-3 rubric 接入 prd-assembly 的 audit 阶段：在结构 validate PASS 之后、Human Gate 之前，新增一个 advisory 级 rubric 评分检查（不阻断，advisory）| 在 [validate_artifact.py](file:///Users/edy/Desktop/workspace/01_项目仓库区/Project_001_产品AI脚手架/src/stages/003-prd-output/skills/prd-assembly/scripts/validate_artifact.py) `validate()` 后段追加 advisory warnings（不升 errors） | 低：只增 advisory | 现有 95/0 仍绿 |
| P1-2 | H1 test-cases Happy/Edge/Error/StateTransition 四类覆盖 | 给 acceptance-criteria 产物加 `state_transition` 标签字段（非阻断）| 在 [acceptance-criteria/output-contract.md](file:///Users/edy/Desktop/workspace/01_项目仓库区/Project_001_产品AI脚手架/src/stages/002-product-requirements/skills/acceptance-criteria/references/output-contract.md) 加可选字段 | 低：可选字段 | fixture 通过 |

## 3. 不蒸馏清单（按用户红线"不制造项目自身矛盾"排除）

| 状态 | 对应 skill | 说明 |
|---|---|---|
| ✅ 已完成（P2-3，E2E-035）| G1 pm-chief-naysayer | 蒸馏为 advisory 红队指南 `src/shared/audit/red-team-naysayer.md`，只提问不改状态，不触发"独立审计改流程"矛盾 |
| ✅ 已完成（P2-2，E2E-035）| E2 prd-to-ddd-design | 蒸馏为 `prd-assembly/references/ddd-design-guide.md`，advisory 交接提示，**不新增 work_item**，规避"动流程引擎"矛盾 |
| ✅ 已完成（P2-1，E2E-035）| A3 pm-prd-workflow | 蒸馏为 `src/scripts/prd_to_docx.py`，本地离线 docx 导出，**不依赖 lark-cli/飞书**，规避"强依赖"矛盾 |
| 不蒸馏 | H2 testbuddy-skill | 强依赖外部 TAPD 平台 |
| 不蒸馏 | F2 hierarchy-visualizer | 与本项目"前端可视化=非必需"定位冲突 |
| 部分吸收 | G2 product-solution-evaluator | rubric 抽取部分已进 P0-3；其余不蒸馏（改 confirmed 风险）|
| 不蒸馏（需新增 work_item）| C1 req-clarifier / G3 pm-master | 需新增 work_item（动流程引擎），暂缓 |
| 不蒸馏（强依赖飞书）| E1 prd-to-design-doc | 强依赖 lark-cli / 飞书云文档 |

## 4. 实施顺序与完成状态

###Phase 1：P0 五项（预计 1-2 小时，零代码风险）

| 步骤 | 内容 | 依赖 |
|---|---|---|
| 1 | 写 `prd-assembly/references/incre-prd-checklist.md`（蒸馏 A4）| 无 |
| 2 | 写 `src/shared/visualization/mermaid-style-guide.md`（蒸馏 F1）| 无 |
| 3 | 升级 `prd-assembly/references/prd-scoring-rubric.md`（蒸馏 B1）| 无 |
| 4 | 在 `prd-assembly/SKILL.md` §Generate 加状态不变式提示（蒸馏 A2）| 1 写完 |
| 5 | 在 `mini-prd/SKILL.md` §Self-Audit 加 5 条（蒸馏 A4 精简版）| 无 |
| 6 | 跑 `run_tests_mac.sh` 验证回归仍 95/0 | — |
| 7 | 登记 E2E-033 | — |

###Phase 2：P1 二项（✅ 已完成，E2E-034）

P1-1 研发评审硬标准 advisory（`validate_artifact.py` `_rd_review_hard_stds`）；P1-2 验收状态转移覆盖（`acceptance-criteria.md` §1.5）。均为 advisory 级，不阻断现有 gate。

###Phase 3：P2 三项（✅ 已完成，E2E-035）

P2-1 docx 导出 `src/scripts/prd_to_docx.py`（A3 蒸馏）；P2-2 DDD 指南 `prd-assembly/references/ddd-design-guide.md`（E2 蒸馏）；P2-3 红队 `src/shared/audit/red-team-naysayer.md`（G1 蒸馏）。全量回归 97/0。

## 5. 蒸馏合规性自检

| 自检项 | Phase 1 后状态 |
|---|---|
| 流程引擎 0 改动 | ✅ |
| 13 产物 + mini-prd 不增不减 | ✅ |
| 宪法三红线（confirmed / AI 不决定 / 来源可追溯）| ✅（蒸馏文档是参考，不改契约）|
| 回归 95/0 → 仍绿 | ✅ |
| 每新增 ≥1 用例 | ⚠ Phase 1 文档级，加 manifest 引用测试即可 |