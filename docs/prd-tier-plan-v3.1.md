> superseded_by: `docs/tier-l0-l1-rebuild-plan.md`

> 历史状态：2026-08-20 起不再作为规范；保留用于追溯。失效范围：旧 L0 章节、累计评分、L1 数量与治理结论。

# 完整计划 v3.1：PRD 章节重设 + Process Tier 工序档位

> 版本：v3.1（取代 v3；修正自评文档 `prd-tier-plan-self-review.md` F1-F12 全部缺陷）
> 硬约束来源：用户图（10 主干产物 + 4 按需产物）+ 三轮 AskUserQuestion 拍板结论
> 总原则：**呈现层重排、产物层零修改、两阶段独立交付**

---

## 0. 用户已拍板决策（本计划不可重开）

| # | 决策 | 来源 |
|---|---|---|
| D1 | 档位 = 工序裁剪（Process Tier），产物集按档位路由 | 拍板 1 |
| D2 | 档位 = L0 / L1 / L2 三档 | 拍板 2 |
| D3 | AI 6 维评分给推荐 + 用户必选（改档无需理由） | 拍板 3 |
| D4 | 档位在 Intake 入口一次性决定，写入 REQ frontmatter | 拍板 4 |
| D5 | 一套 src 多档位，不复制 src-lite/mid/full | 拍板 5 |
| D6 | L0 = 一个 skill 一气呵成（紧凑工作流） | 拍板 6 |
| D7 | 图中产物都要有；加入的其他产物不影响 | 图指示 |
| D8 | 可行性分析 **进 PRD 为按需附录** | 拍板 7 |
| D9 | 问题清单（ISS-NNN）**默认不进 PRD**，进 issue-record.md；Intake 问用户 | 拍板 7 |
| D10 | 需求重举是支持 skill（功能），不是产物 | 图指示 |
| D11 | 分层与阶段分层（001/002/003）互不冲突，阶段分层零修改 | 拍板 8 |

## 0.1 修正对照（v3 → v3.1）

| 缺陷 | v3 错误方案 | v3.1 修正 |
|---|---|---|
| F1 违反"图中产物都要有" | 把 VL/STATE/EX 模板改为业务规则子类 | **上游 13 产物零修改**；PRD §9 业务规则用 9.x 子节**逐字内嵌** VL/STATE/EX（呈现合并、产物独立） |
| F2 一产物两章 | IX-001 同时映射 §5 原型/UX 和 §6 交互规则 | 一一对应：§7 原型/UX ← PD-001；§8 交互规则 ← IX-001 |
| F3 破坏追溯链 | 删除"验收依据"独立章 | **保留独立章**（G→ST→FEA→FUN→AC 终点锚；REQUIRED_HEADINGS / traceability / RTM 三处机器契约依赖） |
| F4 依赖图错误 | L1 = 5 产物 | L1 = **7 产物**（BG→UJ→US→FL→FF→BR→AC，按 registry 前置链重算）+ tier 豁免机制 |
| F5 推翻用户决策 | 开放项表写"可行性分析仅 99-review" | 按需附录 §11.4（遵 D8） |
| F6 兼容缺失 | 无 schema 版本处理 | `schema_version` 7→8 分叉；REQ-001 冻结 v7 契约 |
| F7 评分重复计分 | 维度 4 含合规信号 | 维度 4 只数异常路径条数；合规独立在维度 5 |
| F8 治理底线 | L0 无任何治理 | L0 保留轻量治理：单签 ReviewRecord + hash 锚 |
| F9 落位缺失 | "问用户"无存储 | frontmatter `issue_in_prd: false` 默认 |
| F10 图-框架差异 | 未回答"项目范围"承载 | 明确 US-001 范围基线承载（映射显式声明），开放项 1 仍可改 |
| F11 交付节奏 | A→M 一条线 | Phase 1 / Phase 2 两阶段，各自独立回归闸门 |
| F12 耗时拍脑袋 | 0.5-1pd 等数字 | 删除绝对耗时，改相对量级 |

---

## 1. 三层正交架构（总览）

| 层 | 回答的问题 | 载体 | 本计划改动 |
|---|---|---|---|
| **阶段分层**（已有） | 流程上"什么时候做" | `001/002/003` 三阶段目录 + 13 work_items | **零修改**（D11） |
| **PRD 章节分层**（Phase 1） | 文档上"PRD 长什么样" | `prd.md` 模板 + prd-assembly 三件套 | 重写模板为 10 主干 + 按需 + 3 附录 |
| **Process Tier**（Phase 2） | 工序上"做多重" | registry `tiers` 字段 + intake 路由 + pipeline 过滤 | 新增 L0/L1/L2 三档 |

三套各自独立 frontmatter 字段：`phase`（隐含于目录）、`process_tier`、PRD 结构由 `prd_structure_version` 决定。互不覆盖、互不冲突。

### 1.1 三档与阶段的关系

```
L0 Light      → 000-minimal（新 stage，1 个 work_item：mini-prd）
L1 Standard   → 001/002 现有目录，7 个 work_item（tier 过滤）+ prd-assembly（L1 模式）
L2 Complete   → 001/002/003 现有目录，13 个 work_item（现状，零修改）
```

---

## 2. Phase 1：PRD 章节重设（模板层）

> 范围：只动 `src/templates/stage-3-prd/prd.md` + `prd-assembly` 的 SKILL.md / output-contract.md / validate_artifact.py + schema_version。
> **上游 13 个产物模板、校验器、registry 全部零修改**（F1 修正）。

### 2.1 新 PRD 章节结构（10 主干 + 按需 + 3 附录）

| 章节 | 章节名 | 内嵌上游（一一对应） | 进入条件 |
|---|---|---|---|
| §1 | 项目背景 | BG-001（含 G-/DEC-/ASS/UNK 全量） | 必含 |
| §2 | 项目范围 | US-001 §范围基线（In/Out/Deferred/Conditional）+ FL-001 边界 | 必含 |
| §3 | 用户旅程 | UJ-001（生命周期表/旅程图 verbatim） | 必含 |
| §4 | 用户故事 | US-001（ST-XXX 卡片/MoSCoW/覆盖矩阵） | 必含 |
| §5 | 功能清单 | FL-001（FEA-XXX 总账 + ST 追溯） | 必含 |
| §6 | 功能流程 | FF-001（主/支/异常 Mermaid） | 必含（structure-9q 第 4/5 问） |
| §7 | 原型/UX | PD-001（信息架构/页面结构/导航/原型/交互标注/状态描述） | 必含（纯服务端需求标"本期不适用"） |
| §8 | 交互规则 | IX-001（操作反馈/跳转/弹窗/表单交互 + 5 状态） | 必含（纯服务端需求标"本期不适用"） |
| §9 | 业务规则 | **9.1 计算与流程规则** ← BR-001；**9.2 校验规则** ← VL-001；**9.3 状态变化** ← STATE-001；**9.4 异常处理** ← EX-001 | 必含（9.2/9.3/9.4 子节按需，无内容标"本期不适用"） |
| §10 | 验收依据 | AC-001（AC-XXX Given/When/Then + 量化阈值） | **必含**（F3 修正：追溯链终点锚） |
| §11 | 按需章节 | 11.1 竞品分析 ← competitive-research；11.2 字段规则说明 ← VL-001 字段表；11.3 埋点需求分析 ← tracking-plan；**11.4 可行性分析** ← feasibility-analysis（D8）；11.5 术语表；11.6 团队职责 | 按需（上游无内容标"本期不适用"） |
| 附录A | 需求追溯矩阵 | RTM（G→ST→FEA→FUN→AC→BR + 适用证据列） | 必含（机器可读） |
| 附录B | 自审记录 | Constitution Compliance 四原则 | 必含（AI 自证） |
| 附录C | 问题清单 | issue-record ISS-NNN 汇总表 | **仅 `issue_in_prd: true` 时生成**（D9/F9） |

### 2.2 不进 PRD 的项（项目用 / 流程用）

| 项 | 性质 | 去向 |
|---|---|---|
| 需求重举 | 支持 skill | 贯穿流程调用，不占章节（D10） |
| 校验器/追溯器/branch_validator | 流程用 | `src/scripts/`，gate 时运行 |
| B3 收口表 | 流程用 | issue-record.md §13 |
| hash-anchor / ReviewRecord / audit chain | 流程用 | `.audit/` + `99-review/` |
| 来源处理表 SRC-* | 流程用 | 各上游产物 §来源追溯 |
| issue-record.md（默认） | 流程用 | `99-review/support/`，仅 issue_in_prd=true 时摘录进附录C |
| Process Tier 决策记录 | 流程用 | REQ frontmatter + `00-input/intake-decision.md` |
| 六态知识标注 | 写法约束 | 内嵌上游时随原文保留，不单独成章 |

### 2.3 图-产物映射表（显式声明，回应 D7/F10）

| 图中产物 | 本框架对应 | 进 PRD 章节 | 备注 |
|---|---|---|---|
| 项目背景 | project-background-goal（BG-） | §1 | 直映 |
| 可行性分析 | feasibility-analysis（支持产物） | §11.4 按需 | D8 |
| 问题清单 | issue-record（IR-） | 附录C 条件 | D9 |
| 项目范围 | user-stories §范围基线（US-） | §2 | **映射声明**：图"项目范围"=US 范围基线章节，不新建产物（开放项 1） |
| 需求重举 | requirement-restate（skill） | — | D10 |
| 用户故事 | user-stories（US-/ST-） | §4 | 直映 |
| 用户旅程 | user-journey（UJ-） | §3 | 直映 |
| 原型/UX | page-design（PD-） | §7 | 直映（信息架构/页面/原型/标注全承载） |
| 交互规则 | interaction-rules（IX-） | §8 | 直映 |
| 业务规则 | business-rules（BR-）+ validation-rules（VL-）+ state-machine（STATE-）+ exception-handling（EX-） | §9（9.1-9.4） | **呈现合并、产物独立**（F1） |
| PRD 汇总 | prd-assembly（PRD-） | 全文本身 | 直映 |
| 竞品分析 | competitive-research（支持产物） | §11.1 按需 | 图按需 |
| 功能流程图 | functional-flow（FF-） | §6 | 图按需，本框架主干（9 问必需） |
| 字段规则说明 | validation-rules 字段表 | §11.2 按需 | 图按需 |
| 埋点需求分析 | tracking-plan（支持产物） | §11.3 按需 | 图按需 |
| （框架自有）feature-list | feature-list（FL-） | §5 | "加入的其他产物不影响"（D7） |
| （框架自有）acceptance-criteria | acceptance-criteria（AC-） | §10 | 同上；追溯链终点锚 |

图中产物 **100% 覆盖**，框架自有产物（FL/AC）作为新增不影响。

### 2.4 结构版本兼容（F6 修正 · 实际实现说明）

> **实现修正**：原计划写「registry `schema_version` 7→8」，落地时改为**产物级 `prd_structure_version` frontmatter 字段**（registry `schema_version` 保持 7——`workflow_registry.load_registry` 版本白名单只认 3-7，且 registry 版本与产物结构本就该解耦）。下文以实际实现为准。

- registry `schema_version`：保持 **7**（不动，避免 load_registry 白名单拒绝）
- PRD 结构版本走产物 frontmatter `prd_structure_version`：**"7"（缺省）= 存量 v7 契约**（REQ-001 冻结）；**"8" = 新 10 主干 + 按需 + 附录**
- `prd-assembly/scripts/validate_artifact.py` 按 `prd_structure_version` + `process_tier` 分叉 headings
  - **v7**（REQ-001 等存量 REQ）：走旧 14 headings（REQ-001 冻结 v7 契约，已 confirmed 不可变）
  - **v8 + L2**（新 REQ）：`REQUIRED_HEADINGS_V8_L2`（10 主干 + 附录A/B）
  - **v8 + L1**（新 REQ 标准档）：`REQUIRED_HEADINGS_V8_L1`（8 主干，§7/§8 省略或标「本期不适用」）+ 不得声明 L2-only 上游（Q6 双查）
- `registry_contract_check.py`（E3_drift 闭环）同步分叉校验
- 存量 REQ 不迁移、不重跑（宪法：confirmed 不可变）

### 2.5 validate_artifact.py 改动明细

```python
# 新增：按 schema_version 与 process_tier 分叉的 headings
REQUIRED_HEADINGS_V8_L2 = [  # 10 主干 + 附录
    "项目背景", "项目范围", "用户旅程", "用户故事", "功能清单",
    "功能流程", "原型/UX", "交互规则", "业务规则", "验收依据",
    "需求追溯矩阵", "自审记录",
]
REQUIRED_HEADINGS_V8_L1 = [  # L1 模式：无原型/UX 与交互规则（上游无产物）
    "项目背景", "项目范围", "用户旅程", "用户故事", "功能清单",
    "功能流程", "业务规则", "验收依据",
    "需求追溯矩阵", "自审记录",
]
# forward_chain_ids 保持现有 13 槽位（FUN 接受 FUN|FL|FEA，E2E-028 口径）
# D5.2 upstream 检查按 tier 分叉（L1 只查 7 个）
# 内容密度闸门（禁止"详见 XX-XXX"指针）保持不变
```

### 2.6 模板改动明细（`src/templates/stage-3-prd/prd.md`）

- 顶层骨架改为 §1-§10 + §11 按需 + 附录A/B/C
- frontmatter 新增字段：`prd_structure_version: "8"`、`process_tier: "L2"`、`issue_in_prd: false`
- 每节注释保留"逐字内嵌上游全文、不写指针"指令
- 原 §12"按需章节"（5.1-5.6）整合为新 §11（11.1-11.6，新增 11.4 可行性分析）
- 原 §13"事实与决定"独立章**删除**——六态标注随各上游内嵌原文保留，不顶层重复
- 原 §14"验收依据"保留为 §10（F3）

---

## 3. Phase 2：Process Tier 工序档位（结构层）

### 3.1 三档定义

| 维度 | L0 Light | L1 Standard | L2 Complete |
|---|---|---|---|
| 适用 | 单点改动/文案/配置/Bug 修复 | 单模块新功能/单一主流程/风险可控 | 多角色/合规/状态机/多端 |
| work_items | **1**（mini-prd） | **7**（BG→UJ→US→FL→FF→BR→AC + prd-assembly L1 模式） | **13**（现状） |
| PRD 交付 | mini-prd.md（历史六节草稿） | prd.md（L1 模式，8 主干章） | prd.md（完整 10 主干章） |
| 治理 | 轻量：单签 ReviewRecord + hash 锚（F8） | 完整：ReviewRecord + hash + audit chain | 完整（现状） |
| 校验器 | mini-prd 校验器（新，轻量） | 现有各产物校验器 + prd-assembly L1 headings | 现有全部（零修改） |
| traceability_check | 不跑 | 跑（tier 集内边审计） | 跑（现状） |
| branch_validator | 跑（audit chain 基础） | 跑 | 跑 |
| issue-record | 不建库（mini-prd 内嵌"开口问题"节） | 按需建库 | 强制建库 |
| B3 收口表 | 不适用 | L1 集内落行 | 13 行全落 |
| 耗时量级 | 轻 | 中 | 重（无绝对数字，F12） |

### 3.2 L0 · mini-prd skill（新建 `src/stages/000-minimal/skills/mini-prd/`）

**章节（历史六节草稿，D6）**：
1. 改什么（改动点：文件/页面/字段/文案 + 一句话目标）
2. 为什么（触发来源 + 一句话证据）
3. 影响范围（模块/角色/入口 + 回滚方式）
4. 行为需求与验收（可观察结果 + Given/When/Then 精简）
5. 异常与边界（失败路径 ≤3 条 + 兜底）
6. 依赖与开口问题（外部依赖 + 未决项 ≤3）

**文件清单**：
- `SKILL.md`：六节工作流（Intake→Think(6 维评分反查)→Generate→Self-audit(错误清单)→Human Gate→Commit）
- `assets/mini-prd-template.md`：模板骨架
- `references/output-contract.md`：6 节契约 + 升档触发线
- `scripts/validate_artifact.py`：frontmatter + 6 节 + 验收 + 回滚四项硬检查
- `README.md`、`agents/openai.yaml`：对齐现有 skill 风格

**升档触发线（防 L0 误吞）**：Evaluate 阶段反向跑 6 维评分，任一维度 ≥1 分 → 停止生成，返回 intake-routing 推荐升 L1。

**轻量治理（F8）**：`pipeline.py review --work-item mini-prd --decision approve` 仍走 ReviewRecord + hash 锚（单签），不入 audit chain 全链。

### 3.3 L1 · tier 过滤与前置豁免（F4 修正）

**registry 每个 work_item 增加 `tiers` 字段**：

```json
{ "id": "user-journey", ..., "tiers": ["L1", "L2"] }
{ "id": "page-design", ..., "tiers": ["L2"] }
{ "id": "mini-prd", ..., "tiers": ["L0"] }
```

**tier → work_item 映射**：

| work_item | L0 | L1 | L2 |
|---|---|---|---|
| mini-prd | ✅ | — | — |
| project-background-goal | — | ✅ | ✅ |
| user-journey | — | ✅ | ✅ |
| user-stories | — | ✅ | ✅ |
| feature-list | — | ✅ | ✅ |
| functional-flow | — | ✅ | ✅ |
| page-design | — | — | ✅ |
| interaction-rules | — | — | ✅ |
| business-rules | — | ✅ | ✅ |
| validation-rules | — | — | ✅ |
| state-machine | — | — | ✅ |
| exception-handling | — | — | ✅ |
| acceptance-criteria | — | ✅ | ✅ |
| prd-assembly | — | ✅（L1 模式） | ✅ |

**L1 前置豁免**：AC 的 predecessors=[exception-handling, interaction-rules]，两者 L1 不启用 → pipeline gate 按「tier 集合 ∩ predecessors」判前置（交集为空即放行）。L1 集内链：BG→UJ→US→FL→FF→BR→AC→prd-assembly(L1)。

**L1 的 PRD**：prd-assembly L1 模式——模板同 v8 但 §7 原型/UX、§8 交互规则标"本期不适用"（上游无产物），校验器用 `REQUIRED_HEADINGS_V8_L1`；RTM 列缩为 G→ST→FEA→AC→BR。

### 3.4 6 维评分（F7 去重版）

| # | 维度 | 0 分 | 1 分 | 2 分 |
|---|---|---|---|---|
| 1 | 影响模块数 | ≤1 模块 | 2-3 模块同端 | 多端/多服务 |
| 2 | 角色数 | 单一 | 2 类 | ≥3 或含外部 |
| 3 | 状态复杂度 | 无/单翻转 | 2-3 状态 | ≥4 状态或状态机必备 |
| 4 | **异常路径条数** | 0 | 1-2 条 | ≥3 条 |
| 5 | **合规/资金/PII** | 无 | 数据合规 | 资金/跨境/PII |
| 6 | 改动体量 | ≤1 文件或 ≤10 行 | 数文件 | ≥1 模块 |

映射：**0-4 → L0；5-8 → L1；9-12 → L2**（初始值，首个真实 REQ 落地后校准并记录进 intake-decision.md）。

### 3.5 Intake 决策流（`src/shared/intake-routing/` 扩展）

```
登记 SRC → 评估材料成熟度 L0-L4（现有，正交保留）
  → 6 维评分 → AI 推荐档位
  → 呈现：6 维明细表 + 三档对比表（产物集/工序/校验器/治理/量级）
  → 用户必选（推荐高亮，改档无需理由）
  → 写入 REQ frontmatter：process_tier / issue_in_prd / prd_structure_version
  → 写入 00-input/intake-decision.md（评分明细 + 用户选择 + 时间）
```

新增文件：
- `references/process-tier-routing.md`：评分表 + 三档对比 + 决策流 + 升档触发线
- README.md 增补档位路由段（与现有 L0-L4 成熟度段落并列，声明正交）

### 3.6 pipeline.py 改动

- `work_items()` 增加 tier 过滤参数（默认 L2 = 现状，向后兼容）
- gate 的 predecessors 判定改为「tier 集 ∩ predecessors」
- `confirmed_count == len(work_items(tier))`（E2E-026 动态口径延伸到 tier）
- status 输出增加 `process_tier` 字段
- `--process-tier` CLI 参数（覆盖 frontmatter，用于人工纠偏）

### 3.7 REQ frontmatter 新字段

| 字段 | 取值 | 默认 | 用途 |
|---|---|---|---|
| `process_tier` | L0/L1/L2 | L2 | 工序档位（D4） |
| `issue_in_prd` | true/false | false | 问题清单是否进 PRD 附录C（D9/F9） |
| `prd_structure_version` | "7"/"8" | "8"（新 REQ） | PRD 结构版本分叉（F6） |

---

## 4. 实施步骤（两阶段，各自独立回归闸门）

### Phase 1 · PRD 章节重设（模板层，上游零修改）

| 步骤 | 内容 | 验证 |
|---|---|---|
| P1.1 | 存量 REQ 零改动（不写 schema_version）；新 REQ 产物 frontmatter 用 `prd_structure_version` 分叉（registry schema_version 保持 7） | `registry_contract_check.py` PASS |
| P1.2 | 重写 `src/templates/stage-3-prd/prd.md`（§1-§10 + §11 + 附录A/B/C） | 模板 lint |
| P1.3 | 更新 prd-assembly `SKILL.md` + `output-contract.md`（新章节契约 + 图-产物映射表 + "不进 PRD"清单） | 人工对照图 |
| P1.4 | 更新 prd-assembly `validate_artifact.py`（v7/v8 分叉 + L1/L2 headings 分叉） | 单测 fixture：v7 旧产物 PASS、v8 新产物 PASS、缺章 FAIL |
| P1.5 | `run_tests_mac.sh` 全量回归 | **88/0**（REQ-001 冻结 v7 不受影响） |

### Phase 2 · Process Tier（结构层）

| 步骤 | 内容 | 验证 |
|---|---|---|
| P2.1 | registry 每 work_item 加 `tiers` 字段 + 新 stage `000-minimal` + work_item `mini-prd` 注册 | `registry_contract_check.py` PASS |
| P2.2 | 新建 `src/stages/000-minimal/skills/mini-prd/` 全套（SKILL/模板/契约/校验器/README） | mini-prd 校验器单测（正/负 fixture） |
| P2.3 | 扩 `intake-routing`：`process-tier-routing.md` + README 增补 + `intake-decision.md` 模板 | 6 维评分表 lint |
| P2.4 | `pipeline.py`：tier 过滤 + 前置豁免 + tier-aware confirmed + `--process-tier` | `test_workflow_runtime.py` 扩 tier 用例 |
| P2.5 | REQ frontmatter 模板（`readme-skeleton.md`）加三字段 | 模板 lint |
| P2.6 | `run_tests_mac.sh` 全量回归 + mini-prd 新增单测 | 全绿 |
| P2.7 | 端到端演练：造一个 L0 测试 REQ（单点文案改动）走 mini-prd 全流程 | pipeline status complete=True |

### 台账收尾

| 动作 | 位置 |
|---|---|
| 登记 E2E-029（PRD 章节重设：上游零修改 + 呈现合并） | `99-review/support/e2e-issues.md` |
| 登记 E2E-030（Process Tier 三档 + tier 豁免） | 同上 |
| issue-record §13 版本变更摘要 v1.9 | REQ-001 issue-record.md |

---

## 5. 风险与回退

| 风险 | 概率 | 缓解 | 回退 |
|---|---|---|---|
| 新模板破坏 REQ-001（已 confirmed） | 低 | v7/v8 分叉，REQ-001 冻结 v7 | 回滚 P1.4 校验器 |
| tier 豁免放过越级（L1 跳过 EX 直接 AC） | 中 | AC 产物自身校验器仍要求异常路径覆盖（P0 AC 必含异常） | 收紧豁免白名单 |
| L0 误吞本该 L1 的需求 | 中 | mini-prd Evaluate 反向 6 维评分，任一维 ≥1 分强制升档 | 无需回退（自动路由） |
| L1 缺 PD/IX 导致研发无 UI 依据 | 低 | L1 定位"单模块/主流程"，含 UI 的需求评分维度 1/6 自然 ≥L2 | 用户改档（无需理由） |
| prd-assembly L1 模式校验器复杂化 | 中 | headings 分叉仅两套常量，逻辑集中一处 | L1 暂用 L2 模板 + 空章标"不适用" |
| registry tiers 字段破坏旧工具读取 | 低 | 字段可选缺省=L2（向后兼容）；`registry_contract_check.py` 全量回归 | 删字段恢复现状 |
| 评分阈值不准 | 中 | 标记初始值 + 首个 REQ 校准 | 调表不改架构 |

**Checkpoint 策略**：P1.5 与 P2.6 两个回归闸门各自独立通过才进下一 Phase；任一闸门红 → 停止推进、回滚该 Phase 全部改动、登记 e2e 台账。

---

## 6. 验收标准（DoD）

1. **Phase 1 DoD**：新模板 + 校验器分叉落地；`run_tests_mac.sh` 88/0；REQ-001 v7 冻结产物在新校验器下仍 PASS；新 REQ（v8）缺任一主干章 FAIL。
2. **Phase 2 DoD**：三档端到端可走通（L0 演练 REQ + L1/L2 依赖链正确）；tier 过滤不影响 L2 现状回归；6 维评分 + 用户必选 + frontmatter 落位闭环。
3. **总 DoD**：图中 15 项产物 100% 映射；上游 13 产物零修改（git diff 可证）；两 Phase 回归全绿。

---

## 7. 开放项（真正未决，需拍板）

| # | 项 | 候选 | 倾向 |
|---|---|---|---|
| 1 | 图"项目范围"承载方式 | US-001 范围基线承载（映射声明，不新建产物） / 新建独立 scope 产物 | **US-001 承载**（避免 In/Out 双写漂移；§2 已按此设计，改则另立项） |
| 2 | L1 的 RTM 列 | 缩为 G→ST→FEA→AC→BR / 保持全列空值 | **缩列**（空列是噪音） |
| 3 | L0 mini-prd 的 reviewer 角色 | business_owner 单签 / product_owner 单签 | **business_owner**（L0 体量最轻） |
| 4 | 首个 L1 演练需求来源 | 待用户指定真实需求 / 造测试 REQ | **真实需求**（同时校准评分阈值） |
