---
name: mini-prd
description: 面向 L0 档单点变更的单产物 PRD：修复、文案或配置调整；一个技能、一个产物、一次人工签核。边界复杂时升级至 L1/L2。
---

# 轻量 PRD（Mini PRD · L0 档）

## 目的与边界（Purpose And Boundary）

为**单点、低风险**需求产出**一个**自包含的 `mini-prd.md`（workbuddy 流派：一个 skill 一气呵成），不拆分 12 个上游产物、不跑 preflight/七透镜/taxonomy 扫描/B3 收口表等重型工序。产出即最终交付，供研发/测试直接取用。

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

**输出**：`mini-prd.md`（模板见 `assets/mini-prd-template.md`；L0 产物独立于主模板链，不经过 resolver）。

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

### 6.1 高频遗漏精简参考
单点改动也要保证文案、按钮、阻断/降级说明；详见 `src/stages/003-prd-output/skills/prd-assembly/references/incre-prd-checklist.md`（蒸馏源 A4）。

### 7. Human Gate
呈现 mini-prd + 自检结果 + 未决项。**business_owner 单签**。L0 仍写入 ReviewRecord、hash anchor 和 audit event；省略的是跨产物追溯、独立 issue-record 与 B3 阶段收口，而不是确认留痕。

### 8. Commit
只有 `pipeline.py review --work-item mini-prd --decision approve` 可写入 `confirmed`（前置：registry tiers 含 L0）。

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

6 节全部有真实内容；无指针引用；validate_artifact.py PASS；资格矩阵全部满足且无硬升级条件；business_owner 显式批准；frontmatter `process_tier: L0` 与 `status: confirmed`；ReviewRecord、hash anchor 与 audit event 均已写入。
