---
name: interaction-rules
description: 定义页面级交互规则 IX-XXX——用户操作 → 系统响应，覆盖正常/错误/空态/加载/边界行为。Independent work_item, produces interaction-rules.md.
---

# Interaction Rules · 交互规则

## 目的与边界

为已确认 `page-design.md` 中每个页面的可交互元素，定义精确的「用户操作 → 系统响应」对子：用户做什么、系统可见地回应什么，含状态变化、反馈时机、弹窗/对话框行为与导航触发。每条规则都要写得让开发者能直接实现、测试者能仅凭这一条规则复现。

**不得** 编写数据校验逻辑（→ `validation-rules` `VL-XXX`）、业务计算（→ `business-rules` `BR-XXX`）、权限规则（→ `business-rules`）或验收标准（→ `acceptance-criteria` `AC-XXX`）。交互规则描述用户在页面层*看到与做*的事；系统的领域判断属于下游。

## 输入与输出

输入：来自 `page-design.md` 的已确认页面骨架、来自 `functional-flow.md` 的已确认功能流程（主流程 / 分支流程 / 异常流程），以及来自 `feature-list.md` 的 `FEA-XXX`。输出：独立的 `interaction-rules.md`，使用 `src/templates/resolver.py interaction-rules.md` 解析出的模板。

分析前加载 `references/thinking-framework.md`（其引用 `src/framework/thinking-core.md` §1 强制透镜）。Draft 前加载 `references/output-contract.md`。写任何规则前加载 `references/rule-writing-format.md`。交接前加载 `references/audit-checklist.md` 与 `references/reviewer-checklist.md`。Review 前运行 `scripts/validate_artifact.py <artifact> --json`。

## 思考提示（按阶段）

### 1. Preflight
- "哪些页面与可交互元素已确认？每条规则追溯哪个 FEA 与流程步骤？"
- 从 `page-design.md` 枚举页面；在每个页面上，从操作列列出可点击/可触碰的元素。
- **若页面骨架缺失或未确认**，返回 routing receipt 并 STOP——规则不能挂在凭空发明的页面上。

### 2. Intake
- "每个已确认操作实际触发什么——而不是通用模式应该触发什么？"
- 逐字从页面操作（page-design）与功能流程分支（functional-flow）中摘取：操作、其前置条件与预期结果。
- 按 `src/framework/contracts.md` 将每条规则声明归类为 `FACT` / `DECISION` / `ASSUMPTION` / `AI_INFERENCE` / `UNKNOWN` / `CONFLICT`。
- 我为补全而发明的响应必须标记 `AI_INFERENCE`。

### 3. Think (apply thinking-core.md §1 mandatory lenses)
- **First Principles**: "用户在此操作后必须得到什么可观察的反馈？哪些反馈被暗示但未明说？"
- **Systems Thinking**: "该响应是否依赖必须表示为状态的下游系统结果（异步、支付、通知）？"
- **Adversarial**: "双击、超时、断网或页面陈旧时会发生什么？错误响应是否已定义？"
- **Reverse Validation**: "从期望的用户体验反向推导，每个操作必须存在哪些响应？"

### 4. Clarify
- 先尝试自行消解可发现的缺口（复查页面操作、流程分支、平台惯例）。
- 剩余问题批量提交：AI 初步判断、依据、选项、影响、owner、阻断标志。
- 当答案改变某 P0 页面的交互或反馈行为时，**停在 `needs_user_input`**。
- Limit: 每轮 ≤5 个问题。不问业务规则（→ `business-rules`）或视觉样式。
- 遇到「待确认 / 冲突 / 信息缺口」信号：主动询问是否登记 issue-record（问题清单，见 `src/shared/clarify/skills/issue-record`）；送审前 dor_check 会硬检查收口与引用。

### 5. Generate
- 每个可交互元素或行为一条规则，按 `rule-writing-format.md` 格式以表格形式或段落形式书写。
- 顺序分配唯一 `IX-XXX` ID；每条规则引用其适用页面与 `FEA-XXX`。
- Status: 用 `draft`、`needs_user_input` 或 `conditional_review`——**永不 `confirmed`**。

### 6. Audit
- **Completeness**: 每个 P0 页面的可交互元素都有规则；无没有页面依托的孤儿规则。
- **State Coverage**: 在适用处覆盖每条的 loading/空态/错误/禁用/超时。
- **Boundary**: 扫描校验/计算/权限关键词 → 路由到 `validation-rules` / `business-rules`。
- **Implementability**: 无「合理提示」/ 「适当反馈」式含糊；每个响应都是具体动作或状态。
- 运行 `scripts/validate_artifact.py <artifact> --json`。修复所有 error；warning 在审计记录中说明。
- **B3 收口**：确认 issue-record 的 §13 阶段收口表已更新本 work item 行（问题数 / 收口日期 / 状态；空阶段也落行）。

### 7. Human Gate
Present: 按层分组的 IX 规则清单（入口/身份、核心操作、反馈/异常）、每条规则的触发→响应，以及任何标 `AI_INFERENCE` 的规则。
**产品负责人确认交互行为；业务负责人确认反馈/错误处理。** 批准产生 ReviewRecord（SHA-256）。

### 8. Commit / Reflow
- 只有 `pipeline.py review --decision approve` 可写入 `confirmed`。
- 变更时：记录 delta → 更新受影响规则 → 重跑 Audit → 返回 Human Gate。
- 页面操作（来自 page-design）的改变会使挂在其上的规则失效 → 回到受影响的规则，而非下游打补丁。

## 反模式

| ❌ 不要 | ✅ 要 |
|---|---|
| 只写功能句不写系统响应（"点击进入下一步"） | 每个触发都配上可观察的系统响应 |
| 只写系统动作、丢了触发上下文（"系统打开弹窗"） | 说明是什么用户操作导致该响应 |
| 只描述成功路径 | 为每个元素覆盖 loading、空态、错误、禁用、超时 |
| 写"给出合理提示" / "适当反馈" | 给出具体响应：明确的消息、页面或状态 |
| 写"密码必须 8 位" / "仅 VIP 可操作" / "库存不足禁止下单" | 把校验/计算/权限路由到 validation-rules / business-rules |
| 创建不挂在页面上的孤儿规则 | 每条 IX 引用一个适用页面 + FEA-XXX |

## 示例：充分输入 → 充分输出

**输入**: "场地预约" FEA-001 的已确认页面（场地列表页、详情页、填写页、结果页），含来自 page-design 的操作与下一状态。
**输出**: IX 规则——例如 IX-001 场地卡片点击→进入详情页; IX-002 提交按钮 loading→成功跳结果页/失败驻留表单+错误提示; IX-003 未登录点击预约→跳登录页、登录后回跳; IX-004 名额满的场地置灰不可点; 每条都含触发→响应、适用页面、来源，且无 BR/VL 泄漏。

## 示例：稀疏输入 → 降级输出

**输入**: "给预约流程加些交互规则吧"，没有任何已确认的页面或操作。
**输出**: Preflight 返回 L1（无页面骨架）→ Intake 记录无规则材料 → Think 列出缺失（哪些可交互元素? 触发与响应? 异常反馈?）→ Clarify 批量生成 ≤5 个问题 → 停在 `needs_user_input`。不为不存在的页面发明任何 IX 规则。

## 加载参考

| 文件 | 用途 | 何时加载 |
|---|---|---|
| `references/anti-patterns.md` | AI 常见反模式（写规则时对照规避） | Generate 时对照 |
| `references/audit-checklist.md` | Audit 自审清单 | Audit 前 |
| `references/output-contract.md` | 产出结构与 ID 契约 | Draft 前 |
| `references/question-patterns.md` | Clarify 提问模板（8 类句式） | Clarify 提问时 |
| `references/reviewer-checklist.md` | 人工评审清单（Human Gate 用） | Human Gate 前 |
| `references/rule-writing-format.md` | 交互规则书写格式（段落式，必读） | 写任何规则前 |
| `references/source-handling.md` | 上游追溯规则（FEA-/PG-/SRC- 引用） | Intake/追溯时 |
| `references/thinking-framework.md` | 思考透镜（Common Core + 交互规则领域 lens，必读） | 每次任务开始（必读） |
| `references/flow-five-stage.md` | 交互流程五段式技法（触发/执行中/成功/失败/边界条件） | Generate 交互流程时（按需） |
| `../page-design/references/ui-copywriting-rules.md` | 复用 UI 文案规范技法（5 原则 + 9 场景检查清单） | 写交互反馈/提示文案时（按需，跨 skill 复用） |
| `../page-design/references/high-freq-missing-10.md` | 复用高频遗漏 10 项技法（评审前逐项核验缺项） | 交互规则定稿/评审前（按需，跨 skill 复用） |
| `references/interaction-feedback-rules.md` | 交互反馈规范技法（四态反馈 + 防重复提交 + 破坏性两档确认 + 权限不足三问 + 表单 5 态示例） | Generate 反馈类 IX 规则 / Audit 前核对反馈完备性时（按需） |

## 完成标准

每个 P0 页面的可交互元素都有带 触发 → 系统响应 的 `IX-XXX` 规则；在适用处覆盖状态（loading/空态/错误/禁用/超时）；每条规则引用其适用页面与 FEA；无数据校验、计算或权限逻辑泄漏进 IX；规则写得让开发者可实现、测试者可复现；规则表与页面/流程清单一致；在 `business-rules` 启动前，授权人工已批准这些交互规则。
