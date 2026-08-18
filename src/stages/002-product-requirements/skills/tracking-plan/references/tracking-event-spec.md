# 埋点事件设计规范（Tracking Event Specification）

> 来源吸收：`pm888` 的 0-40 评分「指标严谨」维度（每个指标有 baseline→target、集合覆盖 outcome 与 adoption、至少 1 个 guardrail）与 Reviewer 数据视角对抗检查（指标定义/归因逻辑/埋点完整性/数据口径）+ `pmaster` 的数据埋点模板（埋点位置/事件ID/触发条件/上报字段）与好指标 4 标准 + `product-spec-generator` 引用完整性检查（AC/BR/EX/FR 交叉引用无悬空），作为 tracking-plan 的可选事件层设计能力。
> 定位：把 EV-XXX 事件的「6 要素判定细则 + 命名规范 + 埋点↔指标↔验收闭环」做成可直接照做的规范，让事件表与属性字典一次写对、数据团队无需再澄清即可埋点。
> 触发：Generate 事件表与属性字典时（EV-XXX 命名、6 要素填写）、Audit 覆盖矩阵 / Naming Consistency / 闭环核对前。**按需加载，不设全局闸门**。

## 1. 输入映射（pm-scaffold 语境）

| 外部 skill 输入 | pm-scaffold 对应产物 | 说明 |
|---|---|---|
| 数据埋点模板（pmaster §9：埋点位置/事件ID/触发条件/上报字段） | tracking-plan 事件表 EV-XXX | 事件 6 要素的字段来源 |
| 好指标 4 标准（pmaster §14.2） | EV-XXX 的 metric 字段 | 过滤挂不上可行动指标的事件 |
| 指标严谨维度（pm888 §8.3） | tracking-plan 指标映射表 | baseline→target、outcome+adoption、guardrail |
| 数据视角对抗检查（pm888 §8.6） | Audit 指标闸门 | 指标定义/归因/埋点完整性/数据口径 |
| 引用完整性（product-spec-generator） | EV-XXX → FEA/IX/BR + G-X + AC | 埋点↔指标↔验收闭环无悬空 |
| 事件命名一致性（脚手架 audit-checklist） | event_name 合并与规范 | 禁缩写歧义、禁同名重复 |

> **上游未 confirmed，不写事件规格**：FEA/IX/BR 未确认时只登记候选事件，不编造触发时机与属性。

## 2. 事件 6 要素判定细则

对每个 EV-XXX 逐项过判定细则。六要素齐全且各自合格，事件才可入表。

### 2.1 要素判定表

| 要素 | 判定细则 | 不合格示例 | 合格示例 |
|---|---|---|---|
| **事件名** | snake_case verb_noun（或 verb_noun_result），全局唯一，无缩写歧义 | `click1`、`btn_ok`、`tj` | `approval_submit_success` |
| **属性** | 每个属性有 key/type/example/pii_flag/required；type 属允许集 | 只写"上报字段：userid"无类型无示例 | `submitter_role: string, example: "approver", required: yes` |
| **触发时机** | 写明触发条件（谁做了什么 → 何时触发），不与事件名矛盾 | "点击按钮时触发"（无哪个按钮/哪个角色） | "审批经理点击'通过'且工单非终态时触发" |
| **上报时机** | realtime / near_realtime / batch / on_session_end，且匹配指标时效 | 漏填，或实时类指标挂 batch | 转化漏斗事件 realtime；BI 统计 batch |
| **平台** | web / ios / android / miniprogram / server | 漏填或多平台合并混报 | 双端同事件时逐端列明 platform |
| **PII 标记** | 每属性必填 pii_flag 四档（false/quasi/true/sensitive）+ 保留期 | PII 属性未标记 | 手机号 `pii_flag: true, 保留期 90 天` |

### 2.2 事件类型允许集（判定用）

| event_type | 含义 | 典型示例 |
|---|---|---|
| page_view | 页面曝光 | 审批列表页曝光 |
| click | 点击（含 hover 等 UI 交互） | 通过按钮点击 |
| submit | 表单提交 | 审批提交 |
| exposure | 内容曝光 | 驳回原因字段曝光 |
| success | 业务成功结果 | 审批通过 |
| error | 失败/异常结果 | 审批提交失败 |
| custom | 自定义业务事件 | 审批超时 |

## 3. 事件命名规范（动词_对象_结果）

来源吸收：pm888 指标严谨的"可测、可归因"要求 + 脚手架 audit-checklist「Naming Consistency」（不允许 `click_btn` 与 `button_click` 并存）。

### 3.1 命名结构

```
{动词}_{对象}_{结果?}
   │     │       └─ 可选：区分结果（success/error/cancel/timeout）
   │     └─────────── 业务对象（submit/approval/coupon…），禁止歧义缩写
   └───────────────── 动作（submit/click/approve/reject/upload…），用标准动词表
```

### 3.2 好/坏命名对比表

| ❌ 坏命名 | 问题 | ✅ 好命名 |
|---|---|---|
| `click1` | 无含义 | `approval_approve_click` |
| `tj` | 拼音缩写，歧义 | `approval_submit_success` |
| `btn_ok` | 技术位置，非业务含义 | `approval_reject_click` |
| `submit` | 缺对象 | `order_submit_success` |
| `click_btn` + `button_click` | 同义重复未合并 | 合并为 `approval_submit_click` |

### 3.3 命名规则

1. 全局唯一；不同名称下含义重复的事件必须合并。
2. 禁止缩写歧义（`tj`、`scs`、`ok`）；对象名用完整业务词。
3. 结果后缀只用于同一动作需要区分结果时（如 `_success`/`_error`）；不区分则不后缀。
4. 同名事件不同平台 → 同一 EV 多 platform，不拆新事件。

## 4. 埋点 ↔ 指标 ↔ 验收闭环

来源吸收：pm888 指标严谨维度（指标有 baseline→target、覆盖 outcome+adoption、至少 1 个 guardrail）+ product-spec-generator 引用完整性（引用对象必须存在）。**每个事件必须能回答"支撑哪个指标、指标能否被 AC 验证"**。

### 4.1 闭环结构

```
EV-XXX（事件+属性）
  → 支撑 G-X（北极星/过程/反向指标）
    → 被 AC-XXX 验证（指标可测 → AC 可判定）
      → 回指 FEA-XXX（功能来源）
```

### 4.2 指标严谨 4 条（事件层落地，来源 pm888）

| # | 要求 | 事件层落地 |
|---|---|---|
| 1 | 每个指标有 baseline → target | 事件属性须含计算 baseline 所需字段（如提交数、通过数、耗时） |
| 2 | 指标集合覆盖 outcome 与 adoption | 既有结果事件（approval_submit_success）也有采纳/行为事件（approval_reject_click） |
| 3 | 至少 1 个 guardrail | 追通过率的同时埋超时/驳回/返工事件，防"赢了指标害了用户" |
| 4 | 指标与状态一致 | 事件结果与 ST-XXX 状态语义一致，不出现"状态已驳回但事件上报 success" |

### 4.3 闭环核对表

| 检查 | 方法 | 失败症状 |
|---|---|---|
| 事件→指标 | 每个 must_track 事件挂 G-X 与指标类型（north_star/funnel_step/counter/latency/conversion/retention） | 事件无指标（孤儿事件） |
| 指标→AC | 每个指标能写出验证它的 AC-XXX（可判定阈值） | 指标无 AC 验证，指标不可测 |
| 引用完整 | EV 的 FEA/IX/BR/G/AC 引用逐号存在 | 引用悬空（EV 引 G-999 不存在） |

### 4.4 数据视角对抗检查（来源 pm888 Reviewer 数据视角）

- **指标定义**：指标公式/时间窗/统计对象有口径吗？
- **归因逻辑**：多个事件归到同一指标时，去重/去噪规则说了吗？
- **埋点完整性**：指标要算的分母分子事件都埋了吗？（如通过率=通过/提交，两个事件都要有）
- **数据口径**：双端上报的同一属性口径一致吗？

## 5. 好指标 4 标准事件层落地

来源吸收：pmaster §14.2 好指标 4 标准（已在 `north-star-and-good-metric.md`，本文件补**事件层落地**含义）。

| 标准 | 事件层落地 | 反例 |
|---|---|---|
| **易理解** | 事件名与属性名业务人员一眼看懂，不用解释口径 | `tj_success_cnt`——拼音缩写 |
| **可比较** | 事件属性带可跨期比较的维度（版本/渠道/角色），时间戳标准化 | 事件无时间戳或本地时区 |
| **是比率** | 指标挂分子与分母事件，而非只埋绝对数 | 只埋"通过数"，不埋"提交数"→ 无法算通过率 |
| **能改变行为** | 事件必须能回答一个业务决策问题；挂不上可行动指标的事件删除或降级 nice_to_track | "全量点击"事件，无人据此行动 |

> 应用：候选事件先用 4 标准过滤——答不出"这个事件变多/变少代表什么、谁会据此做什么"的事件，不进入 must_track。

## 6. 反模式

| ❌ 反模式 | 说明 | ✅ 修正 |
|---|---|---|
| **只埋 PV/UV 不埋行为** | 页面曝光有事件，关键行为（提交/通过/驳回/超时）无事件，漏斗断节 | 为每个关键行为补 success/error/custom 事件 |
| **事件无版本** | 属性变更后旧数据无法区分口径 | 事件名或属性带版本（如 `_v2`）或在元数据登记版本号 |
| **PII 混入事件** | 手机号/身份证当普通属性上报 | 拆分到 PII 寄存器，标记四档 + 保留期 + 脱敏 |
| 自动记录每个点击 | 全量埋点，无指标指向 | 只保留能映射指标/目标的事件 |
| 多个动作塞进一个事件 | `submit` 同时表示提交成功与失败 | 按结果拆 `_success`/`_error` 或用 result 属性区分 |
| 忘掉 upload_timing | 数据团队不知道何时上报 | 明确 realtime/batch/session_end |
| 事件表里写 SQL/表结构 | 事件表定义"报什么"，实现交给数据团队 | 只留 6 要素字段 |

## 7. 完整示例：to B 审批流程埋点表

**上游**：FEA-008（工单审批）+ IX-007（审批操作页）+ BR-021（8 小时超时）+ G-003（审批时效：80% 工单 24 小时内完成）+ G-004（审批通过率 ≥ 95%）。

### 7.1 事件表（4 事件：提交 / 通过 / 驳回 / 超时）

| EV ID | event_name | event_type | FEA | IX | BR | trigger_condition | upload_timing | platform | metric | goal | priority |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-101 | approval_submit_success | submit | FEA-008 | IX-007 | BR-021 | 提交人点击提交且校验通过 | realtime | web/ios | funnel_step | G-004 | must_track |
| EV-102 | approval_approve_success | success | FEA-008 | IX-007 | BR-025 | 审批经理点击通过且备注 ≥10 字 | realtime | web/ios | conversion | G-004 | must_track |
| EV-103 | approval_reject_click | click | FEA-008 | IX-007 | BR-025 | 审批经理点击驳回 | realtime | web/ios | counter | G-004 | must_track |
| EV-104 | approval_timeout | custom | FEA-008 | — | BR-021 | 工单待审批超过 8 小时 | near_realtime | server | latency | G-003 | must_track |

### 7.2 属性字典（含 PII 标记）

| event_name | 属性 key | 类型 | example | pii_flag | required | 说明 |
|---|---|---|---|---|---|---|
| approval_submit_success | order_id | string | "WO-20260801-001" | false | yes | 工单号 |
| approval_submit_success | submitter_role | string | "requester" | false | yes | 提交人角色 |
| approval_submit_success | submit_ts | int | 1789000000000 | false | yes | 毫秒时间戳 |
| approval_approve_success | approver_role | string | "approver" | false | yes | 审批人角色 |
| approval_approve_success | handle_duration_min | int | 45 | false | yes | 处理耗时（分钟） |
| approval_approve_success | approver_phone | string | "138****0000" | true | no | 审批人手机号，脱敏后上报 |
| approval_reject_click | reject_reason_len | int | 12 | false | yes | 驳回备注字数 |
| approval_timeout | overdue_hours | int | 9 | false | yes | 超时时长 |

### 7.3 闭环核对

| 事件 | 回指指标 | 指标可被 AC 验证？ | guardrail | 归因逻辑 |
|---|---|---|---|---|
| EV-101 | G-004 提交数（分母） | ✅ AC-101 验证 | 通过率 guardrail | 同工单重复提交去重 |
| EV-102 | G-004 通过数（分子） | ✅ AC-101/104 验证 | — | 双审批并发以首次为准 |
| EV-103 | G-004 驳回率（guardrail） | ✅ AC-103 验证 | 防只追通过率 | 驳回原因分布 |
| EV-104 | G-003 超时占比（guardrail） | ✅ AC-102 验证 | 防拖延审批 | 系统侧 server 埋点，无 PII |

> 校验：6 要素齐全；命名 verb_noun_result 无缩写歧义；4 事件覆盖行为而非只埋曝光；每个事件回指 G-X 且指标有 AC 验证；PII（手机号）已标记脱敏并进 PII 寄存器；超时事件为反向护栏。

## 8. 工作流程

1. **枚举候选事件**：从 FEA/IX/BR 提取行为点，标知识状态（FACT/AI_INFERENCE/UNKNOWN）。
2. **好指标过滤**：用 4 标准筛掉挂不上可行动指标的事件。
3. **补 6 要素**：逐事件填事件名/属性/触发时机/上报时机/平台/PII 标记。
4. **命名规范**：verb_noun_result 命名，查重合并，禁缩写歧义。
5. **闭环核对**：事件→指标→AC 逐环核对，guardrail 与 outcome/adoption 覆盖检查。
6. **PII 收口**：PII 属性入寄存器（四档 + 保留期 + 脱敏规则）。
7. **Audit**：覆盖矩阵每个 P0 FEA ≥1 must_track；无孤儿事件；交 metric_owner 判定 must/nice。

## 9. 核心硬规则

1. **六要素缺一不可**：事件名/属性/触发时机/上报时机/平台/PII 标记任一缺失，事件不入表。
2. **命名规范**：snake_case verb_noun_result，全局唯一，禁缩写歧义；同义重复事件必须合并。
3. **每个事件必须闭环**：回指 G-X 指标，且指标能被 AC-XXX 验证——孤儿事件 = P0。
4. **行为优先于曝光**：关键行为（提交/通过/驳回/超时）必须有事件，只埋 PV/UV 属反模式。
5. **指标严谨 4 条**：baseline→target、outcome+adoption 覆盖、至少 1 个 guardrail、指标与状态一致。
6. **PII 零裸奔**：PII/敏感属性标记四档 + 保留期，脱敏后上报，绝不静默采集。
7. **事件带版本意识**：属性口径变更必须可区分版本，防新旧数据混算。
8. **指标不发明数值目标**：target 来自上游 G-X；本计划只映射，不设定具体目标值。

## 10. 边界（Do Not）

- 不写 SQL / 数仓表 / BI 看板（数据团队实现职责）。
- 不设定具体数值目标（background-goal 的 G-X 职责）。
- 不定 A/B 实验方法论。
- 不把 PII 属性静默埋入普通事件——必须走 PII 寄存器。
- 不因 4 标准过滤而删掉必要的 nice_to_track——分级由 metric_owner 定。
- 不把服务器内部实现细节（堆栈/表名）写进属性——属性只含业务可观察字段。

## 11. 质量自检清单

- [ ] 每个 must_track 事件 6 要素齐全（事件名/属性/触发时机/上报时机/平台/PII）
- [ ] event_name 符合 verb_noun_result，无缩写歧义，无同义重复
- [ ] 事件类型在允许集内（page_view/click/submit/exposure/success/error/custom）
- [ ] 每个事件回指 G-X 指标，且指标有可验证的 AC-XXX（闭环无悬空）
- [ ] 指标严谨 4 条通过：baseline→target、outcome+adoption、guardrail、状态一致
- [ ] 关键行为事件齐全，非只埋 PV/UV
- [ ] PII/敏感属性已标记四档 + 保留期 + 脱敏规则，已入 PII 寄存器
- [ ] 上报时机与平台已填且匹配指标时效
- [ ] 覆盖矩阵每个 P0 FEA ≥1 个 must_track
- [ ] 未写 SQL/数仓表/BI 看板，未设定具体数值目标
