# Brainstorming 集成指南

> 用途：告诉产物型 SKILL（BG / mini-prd / FEA 等）**什么时候**、**怎么**路由到 brainstorming（发散收敛），以及 brainstorming 的产物（SCN-XXX + 4 值处置）**怎么**被消费。

---

## 一、brainstorming 是什么

`workflow-registry.json` 中 `brainstorming` 的 `output_kind: process`，`output_location: 99-review/support/`，**永远不进 PRD 正文**。

**它是发散器，不是收敛器**：当输入"只停留在一行想法 / 材料稀疏 / 需要方案发散"时，把"这想法到底是什么"扩展成可被人处置的候选。它**不做**：
- ❌ 需求复述确认（→ `requirement-restate`）
- ❌ 冲突路由（CONFLICT 是复述阶段的职责）
- ❌ 可行性判断（→ `feasibility-analysis`）
- ❌ 业务事实采集

---

## 二、5 个路由触发点

| 触发点 | 判定 | 路由动作 |
|---|---|---|
| **L0 仅一行想法** | 输入只有"想做 X"一句话，无任何书面材料 | → 必跑 brainstorming |
| **材料稀疏** | 材料 < 50 字 / 只有聊天消息 | → 必跑 brainstorming |
| **方案发散** | 已知目标但需要"还有什么方案" | → 必跑 brainstorming |
| **跨模块多系统多角色** | 目标存在但方案不明 | → 跑 brainstorming 的"全景发散"模式（12 维度全跑 + 分段呈现） |
| **轻量澄清（小范围）** | 单条方向明确、范围小 | → 跑 brainstorming 的"轻量澄清"模式（聚焦 1-2 维度） |

---

## 三、产物 SKILL 主体怎么引用 brainstorming（写法模板）

### mini-prd（000-minimal）的 Evaluate 阶段

```markdown
### 1. Evaluate（资格反查，必做）
- 在动手前读取 `00-input/intake-decision.md`，并按 intake-routing 的**资格矩阵与硬升级条件**复核 L0。
- **当材料成熟度 = L0（仅一行想法 / 无源）时**，加载 `src/shared/process-skills/brainstorming-integration.md`：
  1. 跑 brainstorming 生成 SCN-XXX 候选
  2. 人工作 `include / exclude / defer / research` 处置
  3. 仅 `include` 候选综合成 ≥50 字输入包
  4. 写回 mini-prd 的"目标与变更点"章节
- 命中任一硬升级条件或证据不足以证明上述边界时 → **STOP**，回到 intake-routing 重新选择 L1 或 L2。
```

### BG（project-background-goal）的 Preflight 阶段

```markdown
### 1. Preflight
- "我有哪些来源？谁拥有业务事实？信息密度如何？"
- **当成熟度判定为 L0 / 稀疏输入时**，加载 `src/shared/process-skills/brainstorming-integration.md`：
  - 先跑 brainstorming 生成 SCN-XXX 候选 + 4 值处置
  - 仅 `include` 候选综合为输入包
  - 然后再进 BG 的 Intake 阶段
- **成熟度 L2+（已有 BRD / 业务方案）时，跳过 brainstorming，直接进 BG Intake**。
```

### feature-list（002）的 Preflight 阶段

```markdown
### 1. Preflight
- "上游故事都已确认吗？范围基线是什么？"
- **当上游故事已确认但功能方案需要发散**（如"客户名单管理"有 N 种实现路径），加载 `src/shared/process-skills/brainstorming-integration.md`：
  - 跑 brainstorming 的"功能级发散"模式
  - 候选 → 4 值处置 → 仅 include 进 FEA 草案
```

---

## 四、brainstorming 核心 references 的强制加载点

| Reference | 加载时机 | 强制程度 |
|---|---|---|
| `references/thinking-framework.md` | 每次任务开始（必读，含 12 维度发散 lens） | **必读** |
| `references/output-contract.md` | 起草 SCN-XXX 候选表 + 8 列处置表前 | **必读** |
| `references/mode-dispatch.md` | Preflight 判断任务形态时（轻量/标准/全景三模式） | **必读**（按需） |
| `references/v1-boundary.md` | 候选收敛定范围时（V1 ≤3 个 + 三分类） | **必读**（按需） |
| `references/compliance-keywords.md` | SCN 候选涉及敏感关键词（位置/UGC/金融等） | **必读**（按需） |

---

## 五、错误示例

❌ **把 brainstorming 当产物**：把 SCN-XXX 写进 PRD 正文
✅ SCN-XXX 写入 `99-review/support/brainstorming-output.md`，PRD 只引用"经过 4 值处置的 include 候选"

❌ **AI 替人做处置**：SCN-001 标 `include` 不等人工
✅ SCN-XXX 全部 `AI_INFERENCE`，处置表就绪，等业务负责人人工处置

❌ **12 维度只跑一个**：只看 lifecycle 维度
✅ 扫全 12 维度（lifecycle/roles/normal-alternate-exception-failure-timeout/permission/data condition/handoff/dependency/cancellation/retry/rollback/change-recovery/constraint）

❌ **聚类不去重**：出 40 条近似重复候选
✅ 聚类去重；一个独立想法一个 SCN-XXX

❌ **让 brainstorming 静默跑完不显式 stop**：处置表未人工拍板就写回下游
✅ 呈现候选摘要后必须显式 `stop` 等人工处置，不边展示边写回（approval-gate 硬纪律）

❌ **把 excluded 候选也写回下游**：所有候选都进 BG
✅ 仅 `include` 候选进入输入包；`research` 成为 issue-record 条目；`exclude`/`defer` 不进下游

❌ **在 brainstorming 里解决 CONFLICT**：两个 stakeholder 说法不一，brainstorming 拍板
✅ 冲突是 `requirement-restate` 阶段的职责；brainstorming 不解决冲突，只发散本想法

---

## 六、与 requirement-restate 的区别

| 维度 | brainstorming | requirement-restate |
|---|---|---|
| 触发 | L0 / 稀疏 / 需要方案发散 | 多源歧义 / 新 stakeholder / 需要"我们同意了吗"检查位 |
| 目标 | 扩展"是什么"成候选 | 把已知内容 verbatim 重述确认 |
| 产物 | SCN-XXX 候选 + 4 值处置 | RR-XXX 复述清单 + CONFLICT/UNKNOWN 路由 |
| 知识状态 | 全部 AI_INFERENCE | 含 FACT/DECISION/ASSUMPTION/AI_INFERENCE/UNKNOWN/CONFLICT |
| 边界 | 不解决冲突 / 不做事实采集 | 不解决冲突（只标记） |

---

## 七、与 feasibility-analysis 的区别

| 维度 | brainstorming | feasibility-analysis |
|---|---|---|
| 触发 | 材料稀疏 / 方案发散 | 同一目标 ≥2 实质不同方案 |
| 目标 | 扩展候选 | 评估候选的可执行性 |
| 产物 | SCN-XXX + 4 值处置 | 可行性报告（4 维度 + 多方案取舍 + 置信度） |
| 谁拍板 | 人工 4 值处置 | AI 推荐 + 人类决策 owner |

> **三者协作**：brainstorming 出候选 → feasibility-analysis 评估候选可行性 → 人工选 1-2 个 → requirement-restate 重述对齐 → 进 BG / FEA。
