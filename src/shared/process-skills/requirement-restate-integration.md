# Requirement-Restate 集成指南

> 用途：告诉产物型 SKILL（BG / UJ / US / FEA / FUN / BR / VL / STATE / EX / AC）**怎么**、**什么时候**、**在哪个阶段**路由到 requirement-restate（RR），以及 RR 的产物（RR-XXX / CONFLICT / UNKNOWN）**怎么**被消费。

---

## 一、RR 不是产物，是过程型能力

`workflow-registry.json` 中 `requirement-restate` 的 `output_kind: process`，`output_location: 99-review/support/`，**永远不进 PRD 正文**。

**这是最重要的边界**：RR 的产物（RR-XXX 重述清单 / CONFLICT → ISS-XXX / UNKNOWN → Q-XXX）是"对齐检查点"，只喂给后续 work item 的 Intake 阶段。

---

## 二、5 个路由触发点（每个产物 SKILL 必须检查）

| 触发点 | 判定 | 路由动作 |
|---|---|---|
| **新增 stakeholder** | intake 时 stakeholder 列表发生新增 | → 重新跑 RR，把新 stakeholder 原话 verbatim 追加进 RR-XXX |
| **多源术语不一致** | 同一事实在两个 SRC 中措辞冲突 | → RR §Intake 阶段登记 SRC-001/SRC-002 双方原话 → Clarify 阶段生成 CLS 类 ISS-NNN |
| **下游产物出现 CONFLICT** | BR / VL / STATE 自相矛盾 | → 回流到 RR 重述：哪条 stakeholder 原话被误解了？ |
| **新源材料进来** | 新会议纪要 / 邮件 / 工单评论入库 | → RR 跑一遍，把新诉求加进 RR-XXX；旧的 RR-XXX 标 `superseded` |
| **合规/法律/昂贵构建场景** | 误读代价高 | → RR 必跑（即使只有单源）；强制 stakeholder 复述确认 |

---

## 三、产物 SKILL 主体怎么引用 RR（写法模板）

### BG（project-background-goal）的 Intake 阶段

```markdown
### 2. Intake
- "每个来源实际说了什么——而不是我认为它是什么意思？"
- 在解读之前先逐字提取来源陈述。按 `src/framework/contracts.md` 将每条分类为 `FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` 或 `CONFLICT`。
- **当出现 ≥2 源材料或多 stakeholder 说法时**，加载 `src/shared/process-skills/README.md` 路由到 `requirement-restate`：用 stakeholder 原话 verbatim 重述，CONFLICT 路由 issue-record，UNKNOWN 写 Q-XXX。**BG 自己的 Intake 不解决冲突**——只登记来源并按 `fact-ledger.md` 的 F/D/A/W/O 五分型标注。
```

### UJ（user-journey）的 Intake 阶段

```markdown
### 2. Intake
- 从 BG 已确认的角色、目标、痛点中提取旅程元素。
- **当旅程中出现多角色对同一行为描述不一致**（如运营与客户对"下单成功"的定义不同），加载 `src/shared/process-skills/README.md` 路由到 `requirement-restate`。
- 按 `src/framework/contracts.md` 6 态标注每条主张；不静默合并不同角色的旅程。
```

### US（user-stories）的 Intake 阶段

```markdown
### 2. Intake
- "每个机会真正需要系统做什么——而不是我认为故事应该是什么格式？"
- 从旅程的痛点/机会逐字提取故事候选。
- **当业务方提的"想要 X"是诉求（W 型）而非事实（F 型）**时，加载 `src/shared/process-skills/references/fact-ledger.md` 追问"为什么"，并路由到 `requirement-restate` 复述 stakeholder 原话。
```

### BR / VL / STATE / EX / AC（002 阶段）的 Intake / Clarify 阶段

```markdown
### X. Intake / Clarify
- 当上游素材出现以下任一情况，加载 `src/shared/process-skills/README.md` 路由到对应能力：
  1. **W 诉求型当事实写** → `fact-ledger.md` 重新标注 W → A，再追问 stakeholder
  2. **多源对同一规则冲突** → `requirement-restate` 重述对齐
  3. **CONFLICT / UNKNOWN 信号** → `issue-record` 登记 ISS-NNN
  4. **范围扩张/压测/竞品对标/优先级摊平** → `scope-negotiation-scripts.md` 4 类脚本
- **BR 永远不能从 W 诉求型直接抄进产物**——必须有 stakeholder 原话背书（FACT/DECISION）。
```

---

## 四、RR 核心 references 的强制加载点

| Reference | 加载时机 | 强制程度 |
|---|---|---|
| `fact-ledger.md` | 任何产物 Intake 阶段遇到多源素材 / W 诉求 / 冲突仲裁 | **必读** |
| `gap-checklist-14d.md` | Intake 后 / Generate 前 / Audit 前，对 14 维度做结构性遗漏扫描 | **必读**（按需） |
| `interview-synthesis.md` | 大量口语化原话 / 聊天记录 / 会议纪要 | **必读**（按需） |
| `confirmation-signal-technique.md` | Clarify 阶段识别用户回复是否为真确认 | **必读** |
| `multi-stakeholder-alignment-matrix.md` | ≥2 stakeholder 描述同一事时 | **按需** |
| `assumption-stress-test.md` | ASSUMPTION / AI_INFERENCE 类主张 ≥3 条时 | **按需** |
| `time-sensitivity-and-decision-window.md` | 含时间敏感 / 截止时间 / 决策时窗的诉求 | **按需** |
| `value-cost-risk-triangle.md` | 优先级冲突 / 多方案取舍 | **按需** |
| `latent-pain-signal.md` | O 意见型多 / stakeholder 沉默信号 | **按需** |
| `decision-reversibility.md` | 含不可逆操作 / 决策前需评估可逆性 | **按需** |
| `scope-creep-defense.md` | 范围扩张信号 / 衍生意图 vs 原始诉求剥离 | **按需** |

---

## 五、错误示例（AI 经常犯的）

❌ **把 RR 当产物**：把 RR-XXX 写进 PRD 正文
✅ RR-XXX 写入 `99-review/support/requirement-restate.md`，PRD 只引用 RR-XXX ID

❌ **跳过 RR 直接抄 W 诉求**：业务方说"要做 X"，AI 直接抄进 FEA-XXX
✅ 加载 `fact-ledger.md` 标 W → 追问 stakeholder "为什么" → 写进 RR-XXX → RR 跑通后写进 BG / FEA

❌ **用 AI 推断代替 stakeholder 原话**：RR-001 写成"系统应支持 X"（AI 改写）
✅ RR-001 严格保留 stakeholder 原话 verbatim，写"我想要 X，这样 Y"（stakeholder 自己的话）

❌ **CONFLICT 在 RR 里解决**：两个 stakeholder 说法不一，AI 拍板选一边
✅ 标 CONFLICT → 路由 issue-record ISS-NNN（CLS 类），等 stakeholder 自己裁决

❌ **隐藏来源**：RR-001 写"业务方说要…"无具体段落/时间戳
✅ RR-001 写"业务方说要…[SRC-001 §3.2, 2026-08-15 邮件]"——始终引用 SRC-ID

❌ **让 RR 跑完直接 confirmed**：RR 过程记录本身最高 `ready_for_human_review`
✅ RR 永远不能 `confirmed`，只有 `pipeline.py review --decision approve` 可确认下游工作项

---

## 六、与 issue-record 的关系

RR 把：
- **CONFLICT**（多 stakeholder 说法不一） → 路由到 `issue-record.md` 的 ISS-XXX（CLS 类别）
- **UNKNOWN**（信息缺口） → 写 `Q-XXX` 提问，并路由到 ISS-XXX（INF 类别）
- **FACT / DECISION** → 直接进入下游 BG / UJ / FEA 等产物

issue-record 是**问题清单**，RR 是**复述确认能力**——两者互补不重叠。
