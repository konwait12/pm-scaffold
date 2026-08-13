# Question Patterns · Requirement Restate

Eight canonical question templates for the one-question-at-a-time Clarify loop. Each entry gives:

- **When to use** — the trigger condition
- **Question shape** — the prompt structure
- **Three examples** — paraphrased real cases (desensitized)
- **Common traps** — typical AI mistakes when asking this kind of question

Use these as reference when generating a new question in a Clarify Session. See `SKILL.md` § Clarify for runtime rules (≤5 sessions, ordered by impact, every question carries an AI preliminary judgment).

---

## 1. 措辞确认（Wording）

**When to use**: when a restated row is likely to drift from the stakeholder's original words.

**Question shape**:

```
[为什么重要] 重述的价值在"你原话"与"我们的理解"之间的差异。
RR-NNN 我重述为「[重述文本]」。你的原话是「[原始措辞]」。这样对吗?还是要改回你的说法?
```

**Examples**:

- "你说'尽快处理'，我重述为'在提交后 24 小时内处理'。24 小时是你的意思吗?"
- "RR-003 我用了'审批通过后自动通知'，你原话是'批了就发个消息'。要不要改回更接近原话?"
- "你原话里的'VIP'，在部门里指的是年消费 10 万以上的客户吗?还是另一个定义?"

**Common traps**:

- 用 AI 更"规范"的词替换 stakeholder 的原词
- 不展示原话，只展示重述
- 把"你是不是这个意思"问成引导性封闭题

---

## 2. 来源权威（Source Authority）

**When to use**: when multiple sources give the same ask differently, or the authoritative source is unclear.

**Question shape**:

```
[为什么重要] 归属错误的来源会让回流找不到真源头。
「[具体诉求]」在 [SRC-001（纪要）] 和 [SRC-002（邮件）] 里措辞不同。哪一份是权威?还是以你此刻确认为准?
```

**Examples**:

- "会议纪要写'全渠道触达'，邮件写'仅微信渠道'。以哪个为准?"
- "这条需求最早来自销售总监的口头，没有书面材料。能否补一封邮件作为 SRC-003?"
- "两个版本的时间点不同。后续邮件是否显式取代了先前邮件?"

**Common traps**:

- 默认时间最近的来源权威（权威需按决策权评估，不只按时点）
- 不标记口头来源（口头信息也要登记 SRC-*）
- 把不同来源张冠李戴

---

## 3. 诉求边界（Ask Boundary）

**When to use**: when a restated row bundles multiple asks, or the boundary of the ask is unclear.

**Question shape**:

```
[为什么重要] 一行一个诉求才可逐条确认。
RR-NNN 现在同时包含 [诉求 A] 和 [诉求 B]。它们是两个独立的诉求吗?要不要拆成两行?
```

**Examples**:

- "'支持批量导入且支持去重' 是两个诉求还是一个?能否拆开确认?"
- "这条诉求的范围是'下单'还是'下单+核销'?"
- "你提到'通知用户'，通知的方式（短信/推送）算不算诉求本身?"

**Common traps**:

- 把"相关"当成"同一个"合并进一行
- 不拆行直接跳过确认
- 让 stakeholder 一次确认多个隐含诉求

---

## 4. 冲突路由（Conflict Routing）

**When to use**: when two phrasings contradict and the conflict must be resolved by the stakeholder.

**Question shape**:

```
[为什么重要] 重述阶段只标记冲突、不解决；解决权在 stakeholder。
「[诉求 X]」在 A 处说 [表述 A]，在 B 处说 [表述 B]。请选择: [A / B / 合并为… / 其他]?这会改变 [下游影响]。
```

**Examples**:

- "会议说'所有角色可见'，邮件说'仅经理可见'。请选择生效口径。"
- "工单说'自动退款'，会议纪要却说'需人工审核后退款'。以哪个为准?"
- "两个来源都支持'客户可自助'，但自助的范围（全部/部分字段）没说清。请圈定。"

**Common traps**:

- 替 stakeholder 选边
- 只留一个表述、丢掉另一个
- 不说明冲突对下游的影响

---

## 5. 未知补全（Unknown Fill）

**When to use**: when a restated row depends on missing information (deadline, metric, scope).

**Question shape**:

```
[为什么重要] 未知不补齐，重述无法进入下游。
RR-NNN 缺少 [deadline / 成功指标 / 角色范围]。请补: [具体问题]?建议初判: [AI 建议]，选项: [A / B / C]。
```

**Examples**:

- "这条需求的期望上线时间是?是 8 月底还是可以到 Q4?"
- "'提升效率'的量化判据是什么?任务时长从 3 天降到 1 天?"
- "你指的'运营人员'包含一线客服吗?还是仅指运营经理?"

**Common traps**:

- 用模板字段倒推未知内容
- 让 stakeholder 从零想，不给选项
- 把未知当已知写进 FACT

---

## 6. 方案泄露检查（Solution Leak）

**When to use**: when a source mentions a solution ("做一个 dashboard") that should be recorded as a hint, not a decision.

**Question shape**:

```
[为什么重要] 方案混入重述会让下游直接按方案设计，跳过真实诉求。
源材料提到「[方案]」。请确认: 这是[你真正要的东西],还是[达成某个目标的手段]?如果是手段,背后想解决的业务问题是?
```

**Examples**:

- "'做个 dashboard'——dashboard 是你想要的，还是想看某个数据的手段?想看什么数据?"
- "'加个按钮'——按钮是诉求，还是某个流程缺少入口的症状?缺的流程是什么?"
- "'接入 AI 客服'——要的是 AI 客服，还是'降低响应时长'?两者下游完全不同。"

**Common traps**:

- 把方案当诉求记进 RR-NNN
- 不标 `solution_leak=true`
- 追问方案细节而非背后的诉求

---

## 7. 术语统一（Term Unification）

**When to use**: when different sources use different terms for the same thing.

**Question shape**:

```
[为什么重要] 术语不一致会在下游产生两套定义。
[SRC-001] 称「[术语 A]」,[SRC-002] 称「[术语 B]」。它们是同一件事吗?以哪个为统一术语?是否要建立同义词映射?
```

**Examples**:

- "一处叫'客户'，另一处叫'会员'。是同一个对象吗?统一叫什么?"
- "'核销''销核''消费确认'指同一动作吗?重述里统一用哪个?"
- "术语差异是否隐含范围差异（如'客户'含匿名访客，'会员'仅含注册用户）?"

**Common traps**:

- 静默统一术语，不告知 stakeholder
- 忽略术语差异背后的范围/对象差异
- 只记一个术语，丢掉另一个

---

## 8. 承认检查（Acknowledgment）

**When to use**: right before Human Gate, to give the stakeholder the yes/no acknowledgment checkpoint.

**Question shape**:

```
[为什么重要] 这是"我们真的同意了吗"的检查位。
请阅读整份重述清单。请回答: 是的,这就是我说的 / 部分不是(请注明哪几条) / 不是,请重新理解(请描述真实意图)。
```

**Examples**:

- "RR-001 到 RR-007 是否都忠实?有哪几条需要修订?"
- "你可以现在签收这份重述吗?还是需要先和部门内对一次?"
- "修订后请确认最终版，签收将记录 ReviewRecord 与 SHA-256。"

**Common traps**:

- 让 AI 代签收（只有 stakeholder 能确认）
- 不给"部分不是"的选项，逼成二选一
- 确认后仍偷偷改词

---

## Cross-cutting tips

1. **排序原则**: Clarify 一次只问 1 个,按 Impact × Uncertainty 排序,先问阻断性高的。
2. **展示原话**: 每个问题都同时给出"你的原话"与"我们的重述"，让差异可见。
3. **每问必带 AI 初步判断**: 不要让 stakeholder 从零开始想问题。
4. **三选项常驻**: 给 2-4 个互斥选项 + 「其他」兜底。
5. **回写位置必填**: 每答一题必须能精确指向 requirement-restate.md 的哪一行。
6. **冲突不解决**: 重述阶段只确认与标记，冲突解决路由 issue-record。
