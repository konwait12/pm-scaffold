---
name: mini-prd
description: 面向 L0 档单点变更的紧凑事实采集与起草工件；一个技能、一个主工作项、一次人工签核。发布前映射为统一 canonical PRD，边界复杂时升级至 L1/L2。
---

# 轻量 PRD（Mini PRD · L0 档）

## 目的与边界（Purpose And Boundary）

为**单点、低风险**需求产出**一个**自包含的 `mini-prd.md`，不拆分 12 个上游产物、不跑 preflight/七透镜/taxonomy 扫描/B3 收口表等重型工序。mini-prd 是紧凑事实采集与起草工件，不是最终 PRD 章节契约；确认后由确定性映射生成与 L1/L2 相同章节集合的 canonical `prd.md`。

**适用**：bug 修复（单文件/单字段/单文案）、配置开关改动、一处状态文案调整、无需多角色/多模块/合规的简单变更。

**不适用**（命中任一即升档 L1/L2，返回 intake-routing 重新决策）：
- 影响多个模块，或跨端/多服务
- 涉及多个角色或外部角色
- 需要状态机、生命周期、状态副作用或恢复策略
- 存在多个独立恢复路径、不可逆操作，或无法证明可简单回退
- 含合规 / 资金 / PII / 跨境
- 改动体量 ≥1 个完整模块

**不要**：不设计旅程/状态机/页面骨架；不引入新需求；不写「详见 XX-XXX」指针；不伪造验收阈值。

## 输入与输出（Inputs And Outputs）

**输入**：一个来源（含改动点位置：文件/页面/字段/文案）+ 一句话目标 + 一句话验收 + 回滚方式。材料成熟度 L0-L4 判定沿用 intake-routing（正交，不冲突）。

**输出**：`mini-prd.md`（模板见 `assets/mini-prd-template.md`；L0 主工作项独立于上游主链）。发布前的 `003-prd-output/prd.md` 使用 `src/templates/stage-3-prd/prd.md` 的 canonical 章节，不得把六节 mini-prd 直接当成最终 PRD。

## 工作流（Workflow）

### 1. Evaluate（资格反查，必做）
在动手前读取 `00-input/intake-decision.md`，并按 intake-routing 的**资格矩阵与硬升级条件**复核 L0：
- 仅限单一可定位变更、单角色、无持久状态设计、无敏感/资金/合规影响、无数据迁移，且存在单一简单回退。
- 命中任一硬升级条件或证据不足以证明上述边界时 → **STOP**，回到 intake-routing 重新选择 L1 或 L2。
- 评分如被使用，只能帮助沟通风险；不能推翻硬升级条件，也不是 L0 的通过条件。

### 2. Intake
逐字提取来源中的改动点陈述（保留来源 ID）。登记到 frontmatter `upstream_artifact_ids`（如 SRC-XXX / BG-XXX）。

### 3. Think（轻量）
只做三问：改了什么可观察结果 / 影响哪些入口 / 失败怎么兜底。不做七透镜。

### 4. Clarify
至多 3 个澄清问题，批量呈现，附带 AI 初步判断。答案可能改变影响面/验收口径时停在 `needs_user_input`。问题记录进 mini-prd §6 依赖与开口问题（不单独建 issue-record 库）。

### 5. Generate
填充 6 节模板。每节都要有真实内容，禁止 `待确认` 占位遗留（frontmatter 除外）。状态使用 `draft` / `needs_user_input` / `conditional_review`——绝不用 `confirmed`。

### 6. Self-Audit（作者自检，不机器扫描）
对照以下 5 条错误清单自检（蒸馏 A4 incremental-prd-collaboration 高频遗漏精简版）：
1. 改动点是否精确（文件/字段/文案可定位）？
2. 影响范围是否穷举（入口/角色/回滚）？
3. 验收是否可观察可判定（Given/When/Then 精简版）？
4. §5 是否说明实际适用的边界与回退依据；若不改变既有失败语义，是否写明依据？
5. 是否无指针引用（详见 XX-XXX）？

补充自检（仅 L0 适用，蒸馏自 PRD §2.1-2.5）：
- 按钮文案是否明确（避免"确定"这种语义模糊）？
- 阻断 / 降级文案是否已写？
- 时间窗 / 倒计时的取值依据是否记录？

运行 `scripts/validate_artifact.py <mini-prd.md> --json`。修复所有 errors；warnings 记录进 audit notes。

### 6.1 产品质量增强记录

在送审前必须填写模板中的“产品质量增强记录”。它把用户研究合成、方案替代、价值-成本-风险、反向质疑和失败恢复压缩为五行证据，不要求 L0 伪造完整研究或竞品报告：

- 受影响角色与可观察结果：不能只写“用户体验”；写角色、入口、行为和不受影响边界。
- 采用方案与被排除替代：至少记录一个真实考虑过的替代方案及排除理由；没有替代方案时说明为何单点修复无需方案比较。
- 价值-成本-风险：分别写证据或 `UNKNOWN`，不把 AI 推断当事实，不写“风险可控”这类空话。
- 失败边界与回退：写真实失败路径、回退动作和触发条件；若无需新增回退，写事实依据。
- 可证伪条件/停止条件：写什么证据会让本次方案停止、改范围或升级档位。

缺少事实时停在 `needs_user_input`，而不是用 `N/A` 填满。完整规则见 `src/shared/process-skills/references/l0-l1-product-quality-contract.md`。

### 6.2 高频遗漏精简参考
单点改动也要保证文案、按钮、阻断/降级说明；详见 `src/stages/003-prd-output/skills/prd-assembly/references/incre-prd-checklist.md`（蒸馏源 A4）。

### 7. Human Gate
呈现 mini-prd + 自检结果 + 未决项。**business_owner 单签**。L0 仍写入 ReviewRecord、hash anchor 和 audit event；省略的是跨产物追溯、独立 issue-record 与 B3 阶段收口，而不是确认留痕。

### 8. Commit
只有 `pipeline.py review --work-item mini-prd --decision approve` 可写入 `confirmed`（前置：registry tiers 含 L0）。批准事务同时确定性生成 `003-prd-output/prd.md`：六类事实按固定映射填入 canonical 章节，并为每个章节写入适用性状态；映射失败时整次确认失败，不生成伪造章节或新业务事实。

## mini-prd 到 canonical PRD 的固定映射

| mini-prd 事实 | canonical PRD 章节 | 规则 |
|---|---|---|
| §1 改什么 | §2 项目范围、§5 功能清单、§6 功能流程 | 原文嵌入对应章节；无法定位范围或行为时阻断 |
| §2 为什么 | §1 项目背景、§4 用户故事 | 只承接来源与目标，不补写用户价值 |
| §3 影响范围 | §2 项目范围、§3 用户旅程、§7 原型/UX、§8 交互规则 | 仅根据明确入口/角色/界面事实判断适用性 |
| §4 行为需求与验收 | §6 功能流程、§9.1 计算与流程规则、§10 验收依据 | 保留 Given/When/Then 和原验收，不新增阈值 |
| §5 异常与边界 | §9.4 异常处理 | 无新增失败语义时写事实化 `not_applicable` |
| §6 依赖与开口问题 | §11 按需章节、需求追溯矩阵、自审记录 | 保留 owner、影响与未决状态 |

L0 的 §7、§8、§9.2、§9.3 不能默认为不适用；必须由 `intake-decision.md` 的 canonical 章节矩阵给出事实化判断。任何页面、交互、字段校验、状态或新异常信号都会触发补证据或升级 L2。

## 反模式（Anti-Patterns）

| ❌ 不要 | ✅ 要做 |
|---|---|
| 用累计评分或“低风险”直觉绕过硬升级条件 | 以资格矩阵和可定位证据决定是否升档 |
| 写「详见 BR-XXX」指针 | 把规则内嵌写进 §4 行为需求与验收 |
| 伪造验收阈值 | 验收必须可观察或可量化，并说明判定方式 |
| 为满足格式编造异常 | §5 只写实际适用边界；可说明既有失败语义不变及其依据 |
| 引出一堆新需求 | 新需求路由回 intake-routing 立项 |

## 加载参考文档（Load References）

| 文件 | 用途 |
|---|---|
| `assets/mini-prd-template.md` | 6 节模板骨架（Generate 用） |
| `references/output-contract.md` | 6 节契约 + 升档触发线（Draft 前） |
| `src/shared/intake-routing/references/process-tier-routing.md` | 资格矩阵、硬升级条件与档位对比（Evaluate 时必读） |

## 完成标准（Completion）

6 节和产品质量增强记录全部有真实内容；无指针引用；validate_artifact.py PASS；资格矩阵全部满足且无硬升级条件；business_owner 显式批准；frontmatter `process_tier: L0` 与 `status: confirmed`；ReviewRecord、hash anchor 与 audit event 均已写入。
