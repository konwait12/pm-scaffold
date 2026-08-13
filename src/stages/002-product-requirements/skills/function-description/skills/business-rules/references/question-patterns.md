# Question Patterns · business-rules

Eight canonical question templates for the one-question-at-a-time Clarify loop. Each entry gives:

- **When to use** — the trigger condition
- **Question shape** — the prompt structure
- **Three examples** — paraphrased real cases (desensitized, generic business scenarios)
- **Common traps** — typical AI mistakes when asking this kind of question

Use these as reference when generating a new question in a Clarify Session. See `SKILL.md` § Clarify for runtime rules.

---

## 1. 规则存在性与来源（Rule Existence / Source）

**When to use**: when a candidate BR has no source; or when the story/UX implies a rule but never states it; or when the same rule appears from two contradictory sources.

**Question shape**:

```
[为什么重要] 业务规则必须能追溯到已确认来源，否则无法验收也无法审计。
我识别出 [规则内容] 可能与 [功能/故事] 相关，但上游没有明确声明。
请确认: 这条规则 [存在 / 不存在 / 待补充来源]，来源是 [具体材料/决策人]?
```

**Examples**:

- "ST-002 只写「限制报名人数」，但没写数量与规则。请问配额是多少？按活动全局还是每人限报？"
- "邮件 SRC-002 §3 说 VIP 折扣 9 折，纪要 SRC-001 §2 说 8.5 折。哪一个是业务方最终确认的？"
- "这条「单笔订单超 ¥100k 需审批」我在上游找不到出处。是业务真实要求还是我的推断？"

**Common traps**:

- 把 AI 推断出的约束当作已确认事实
- 不问规则"存在与否"，直接编一个来源
- 两个来源冲突时静默选边而不是提交裁决

---

## 2. 计算口径（Calculation）

**When to use**: when a calculation rule lacks formula, unit, or rounding; or when the same quantity appears with different definitions.

**Question shape**:

```
[为什么重要] 计算口径不清会导致财务/统计口径错误，验收无法判定。
当前规则为 [计算内容]。请明确:
1. 公式是什么? 2. 单位/币种? 3. 舍入规则与精度? 4. 边界值(如满减临界点)如何处理?
```

**Examples**:

- "折扣按订单金额还是按单品价累加？满 ¥500 减 ¥100，是满额即减还是阶梯？」
- "「客单价」的分母是订单数还是客户数？统计窗口是自然月还是滚动 30 天？"
- "金额舍入保留几位小数？四舍五入还是银行家舍入？"

**Common traps**:

- 用「按规定计算」代替公式
- 不问币种/单位（分 vs 元）
- 忽略舍入与边界（9.99 折这种临界值）

---

## 3. 约束边界（Constraint Boundary）

**When to use**: when a constraint rule states a bound without boundary behavior; or when bounds contradict each other; or when the reject path is unspecified.

**Question shape**:

```
[为什么重要] 边界值决定规则的通过/拒绝判据，缺一个边界就缺一种行为。
规则为 [约束内容]。请明确上下界、开闭区间，以及 [边界值] 落入合法还是非法?
```

**Examples**:

- "配额上限是 100，那第 100 个和第 101 个分别如何处理？是拒绝、排队还是候补？"
- "「金额不能太大」——具体上限是多少？超上限是拒绝还是转人工审批？"
- "库存下限为 0 时还能下单吗？临界值为 0 是允许还是禁止？"

**Common traps**:

- 只写上限不写下限
- 边界值含糊（≥ vs >）
- 拒绝行为悬空（"超了怎么办"无人回答）

---

## 4. 触发条件（Trigger Condition）

**When to use**: when a rule's trigger is vague; or when a rule should fire but the trigger context is not specified.

**Question shape**:

```
[为什么重要] 触发条件不清，开发无法判断规则何时生效。
规则为 [规则内容]。请问: 在什么场景/时机下触发? 前置条件是什么? 一次性还是可重复触发?
```

**Examples**:

- "「报名截止后不可修改」——截止时间精确到分钟还是秒？时区是哪个？"
- "折扣在哪些条件下触发？仅新客，还是老客续费也触发？"
- "该规则是在提交时触发还是每次查询时触发？"

**Common traps**:

- 用「当……时」的空壳触发器
- 不问重复触发/一次性
- 时区、精度等参数缺失

---

## 5. 权限规则（Permission）

**When to use**: when a permission rule omits roles; or when who-may/who-may-not is unclear; or when data-scope limits are missing.

**Question shape**:

```
[为什么重要] 权限规则决定谁能操作、谁能看数据，漏一个角色就漏一个入口。
规则为 [权限内容]。请明确:
1. 谁能执行? 2. 谁不能? 3. 按什么数据范围(自己/本部门/全局)?
```

**Examples**:

- "「订单可修改」——谁能改？只有下单客服还是管理员也能？"
- "「报价可见」——销售看全部还是仅自己名下？"
- "审批流里第二级审批人是谁？超时未批由谁接手？"

**Common traps**:

- 只写谁可以，不写谁不可以
- 数据范围（行级权限）遗漏
- 审批升级/超时归属无人定义

---

## 6. 时序与依赖（Timing / Sequencing）

**When to use**: when a rule implies ordering; or when parallel/forbidden sequences are not covered; or when a dependency on another rule is unstated.

**Question shape**:

```
[为什么重要] 时序规则影响编排与状态机，漏一个顺序就漏一种状态流。
规则为 [时序内容]。请明确: 前后顺序? 是否可以并行? 哪些操作被禁止同时发生?
```

**Examples**:

- "取消订单和退款是同一动作还是两个先后动作？取消后还能改地址吗？"
- "核销与签到是否必须按顺序？跨场次签到是否允许？"
- "审核驳回后用户修改，是重新进入队列还是直接回到待审核？"

**Common traps**:

- 顺序不写（隐含假设）
- 不问互斥/并行
- 把时序规则写成 UI 步骤

---

## 7. 规则冲突（Conflict）

**When to use**: when two BRs contradict; or when a new rule conflicts with an existing confirmed rule.

**Question shape**:

```
[为什么重要] 冲突若不显式裁决，下游实现会各自选边，产生不一致行为。
我识别到 [规则A] 与 [规则B] 冲突: [冲突点描述]。
请裁决: 保留哪个? 或如何调和? 冲突的最终结论将登记为 CONFLICT-XXX。
```

**Examples**:

- "BR-002 允许取消，BR-007 说提交后不可修改——取消是否算修改？"
- "全球配额与单场配额同时生效时，取哪个上限？"
- "「全量推广」与「小范围试点」口径冲突，最终采用哪个？"

**Common traps**:

- 静默选边不记录 CONFLICT
- 不保留双方立场
- 裁决后不回流更新相关规则

---

## 8. 例外与拒绝行为（Exception / Reject Behavior）

**When to use**: when a rule lacks its exception branch; or when reject behavior is unspecified; or when the boundary between "rule violation" and "system error" is unclear.

**Question shape**:

```
[为什么重要] 例外与拒绝行为决定用户体验，缺一个分支就缺一种失败处理。
规则为 [规则内容]。请问: 违反时系统如何处理? 有无合法例外(白名单/管理员强制)? 与异常处理子技能的分界在哪?
```

**Examples**:

- "配额打满后用户点击报名，看到什么？直接拒绝还是进入候补队列？"
- "白名单客户是否豁免配额限制？由谁维护白名单？"
- "规则失败是业务拒绝（走 BR）还是系统故障（走 exception-handling）？"

**Common traps**:

- 只写正常路径，例外分支交给下游猜
- 白名单/豁免规则漏掉
- 把业务拒绝和系统异常混为一谈

---

## Cross-cutting tips

1. **排序原则**：Clarify 一次只问 1 个，按 Impact × Uncertainty 排序，先问阻断性高的。
2. **不要问 AI 能查的事实**：公司名、公开政策、行业报告，让 AI 自己查，不要让业务方回答。
3. **每问必带 AI 初步判断**：不要让业务方从零开始想问题。
4. **三选项常驻**：给 2-4 个互斥选项 + 「其他」兜底。
5. **跳过按钮**：非阻断项允许业务方打 ⚠️ 风险标签先跳过。
6. **回写位置必填**：每答一题必须能精确指向父文档 §业务规则 的哪条 BR。
