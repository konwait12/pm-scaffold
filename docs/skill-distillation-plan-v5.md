# 计划 v5：产品能力蒸馏融合

> 公开版说明：本历史计划保留能力取舍与实施记录；具体调研样本、内部文件名和本地索引已移除。
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

| P# | 能力主题 | 蒸馏内容 | 蒸馏目标 | 风险 | 验收 |
|---|---|---|---|---|---|
| P0-1 | 增量评审 | 高频遗漏检查清单（按钮文案、异常状态、阻断文案等）+ 产品边界（业务/规则/状态/文案/验收，不滑向 API/字段）| 新建 `src/stages/003-prd-output/skills/prd-assembly/references/incre-prd-checklist.md`，并在 [SKILL.md](src/stages/003-prd-output/skills/prd-assembly/SKILL.md) §Audit 之前加 §Red-Review 步骤引用 | 零：纯参考文档 | 模板内出现高频遗漏案例覆盖度≥80% |
| P0-2 | 图表表达 | 完整图类型选择表（流程/时序/状态/脑图/ER/时间线/用户旅程）+ 常见语法错误 | 新建 `src/shared/visualization/mermaid-style-guide.md`，所有 skill 的 `references/` 引此文档 | 零：纯文档 | 各 skill 引用一致 |
| P0-3 | PRD 评审 | 10 分制 7 模块评分 + 3 大绝对红线 + 17 项快速检查清单 | 升级现有 [prd-scoring-rubric.md](src/stages/003-prd-output/skills/prd-assembly/references/prd-scoring-rubric.md)，新增"研发评审版 PRD 硬标准"段 | 零：升级文档 | 含 3 红线 + 17 项 |
| P0-4 | 状态生命周期 | "每个字段要描述其状态及状态间转变条件"，与 BR/VL/STATE/EX 四个产物的契约一致 | 在 [prd-assembly/SKILL.md](src/stages/003-prd-output/skills/prd-assembly/SKILL.md) §Generate 写一段"状态不变式提示"，引用现成业务规则与状态机产物 | 零：文档提示 | §Generate 含 1 行引用 |
| P0-5 | L0 自检 | [mini-prd/SKILL.md](src/stages/000-minimal/skills/mini-prd/SKILL.md) §Self-Audit 加 5 条 L0 自检 | 零：扩展既有自检 | §Self-Audit 5 条升级 |

## 2. 蒸馏清单（P1 = 轻量脚本级，零流程改动）

| P# | 能力主题 | 蒸馏内容 | 蒸馏目标 | 风险 | 验收 |
|---|---|---|---|---|---|
| P1-1 | 增量评审评分 | 把 P0-3 rubric 接入 prd-assembly 的 audit 阶段：在结构 validate PASS 之后、Human Gate 之前，新增一个 advisory 级 rubric 评分检查（不阻断，advisory）| 在 [validate_artifact.py](src/stages/003-prd-output/skills/prd-assembly/scripts/validate_artifact.py) `validate()` 后段追加 advisory warnings（不升 errors） | 低：只增 advisory | 现有回归仍绿 |
| P1-2 | 验收场景覆盖 | 给 acceptance-criteria 产物加 `state_transition` 标签字段（非阻断）| 在 [acceptance-criteria/output-contract.md](src/stages/002-product-requirements/skills/acceptance-criteria/references/output-contract.md) 加可选字段 | 低：可选字段 | fixture 通过 |

## 3. 不蒸馏清单（按用户红线"不制造项目自身矛盾"排除）

| 状态 | 对应 skill | 说明 |
|---|---|---|
| ✅ 已完成（P2-3，E2E-035）| 红队质疑 | 蒸馏为 advisory 红队指南 `src/shared/audit/red-team-naysayer.md`，只提问不改状态，不触发"独立审计改流程"矛盾 |
| ✅ 已完成（P2-2，E2E-035）| 领域交接 | 蒸馏为 `prd-assembly/references/ddd-design-guide.md`，advisory 交接提示，**不新增 work_item**，规避"动流程引擎"矛盾 |
| ✅ 已完成（P2-1，E2E-035）| 离线文档导出 | 蒸馏为 `src/scripts/prd_to_docx.py`，本地离线 docx 导出，不引入强制云服务依赖 |
| 不蒸馏 | 外部测试平台依赖 | 强依赖特定第三方平台 |
| 不蒸馏 | 层级可视化 | 与本项目"前端可视化=非必需"定位冲突 |
| 部分吸收 | 方案评估 | rubric 抽取部分已进 P0-3；其余不蒸馏（改 confirmed 风险）|
| 不蒸馏（需新增 work_item）| 深度澄清/主控能力 | 需新增 work_item（动流程引擎），暂缓 |
| 不蒸馏（强依赖云文档）| 云端设计交接 | 强依赖外部云文档服务 |

## 4. 实施顺序与完成状态

###Phase 1：P0 五项（预计 1-2 小时，零代码风险）

| 步骤 | 内容 | 依赖 |
|---|---|---|
| 1 | 写 `prd-assembly/references/incre-prd-checklist.md`（蒸馏 A4）| 无 |
| 2 | 写 `src/shared/visualization/mermaid-style-guide.md`（蒸馏 F1）| 无 |
| 3 | 升级 `prd-assembly/references/prd-scoring-rubric.md`（蒸馏 B1）| 无 |
| 4 | 在 `prd-assembly/SKILL.md` §Generate 加状态不变式提示（蒸馏 A2）| 1 写完 |
| 5 | 在 `mini-prd/SKILL.md` §Self-Audit 加 5 条（蒸馏 A4 精简版）| 无 |
| 6 | 跑 `run_tests_mac.sh` 验证全部回归通过 | — |
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
| 回归脚本 | ✅（以脚本实测为准） |
| 每新增 ≥1 用例 | ⚠ Phase 1 文档级，加 manifest 引用测试即可 |
