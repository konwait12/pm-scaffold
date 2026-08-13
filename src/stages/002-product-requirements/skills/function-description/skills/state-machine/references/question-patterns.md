# Question Patterns · state-machine

Eight canonical question templates for the one-question-at-a-time Clarify loop. Each entry gives:

- **When to use** — the trigger condition
- **Question shape** — the prompt structure
- **Three examples** — paraphrased real cases (desensitized, generic business scenarios)
- **Common traps** — typical AI mistakes when asking this kind of question

Use these as reference when generating a new question in a Clarify Session. See `SKILL.md` § Clarify for runtime rules.

---

## 1. 状态集合完整性（State Enumeration）

**When to use**: when a source mentions states but lists none; or when the state set looks incomplete (no cancel/timeout/terminal); or when two "states" may actually be one view.

**Question shape**:

```
[为什么重要] 状态集合不全，转移表就无法覆盖真实业务。
我为 [实体] 识别的状态为 [已列状态]。请确认:
1. 还有没有漏的状态(取消/超时/驳回后重提/冻结)? 2. 有没有其实是 UI 视图、不是真状态的项?
```

**Examples**:

- "订单状态我列了 待支付/已支付/已取消/已发货/已完成，还有退款中、售后中这种状态吗？"
- "「审核中」和「待审核」是两个状态，还是同一个状态的不同称呼？"
- "「已结束」之后还能恢复成进行中吗？如果不能，它是终态。"

**Common traps**:

- 只写成功路径状态
- 把 UI 视图（如"列表页""详情页"）当状态
- 终态/取消态/超时态漏掉

---

## 2. 触发事件定义（Trigger Event）

**When to use**: when a transition lacks a named event; or when the same event has different meanings in different states; or when who-triggers is unclear.

**Question shape**:

```
[为什么重要] 事件定义不清，开发不知道"什么动作"驱动这条转移。
从 [状态A] 到 [状态B] 的触发事件是什么? 由谁触发(用户/系统定时/管理员)? 事件在 [其他状态] 下含义是否不同?
```

**Examples**:

- "从 待支付 到 已支付 的触发事件是「支付成功回调」，对吗？超时未支付的事件叫什么？"
- "「取消」事件在 待支付 和 已发货 下分别是用户取消和客服取消，去向一样吗？"
- "「审核通过」是人工点击还是系统自动判定？"

**Common traps**:

- 事件无名（"……就变……"）
- 不区分触发者（用户/系统/管理员）
- 同一事件跨状态含义不澄清

---

## 3. 目标状态与悬空转移（Target State / Dangling）

**When to use**: when a state × event combination has no defined target; or when a transition table has holes; or when a terminal state accidentally has outbound edges.

**Question shape**:

```
[为什么重要] 悬空转移会让实现方凭空猜测状态去向。
[状态] 遇到 [事件] 时目标状态是什么? 该组合是合法、被禁止(不允许)还是业务上不可能发生?
```

**Examples**:

- "已取消 状态下收到「再次支付」事件，目标是什么？不允许，还是回到 待支付？"
- "已完成 状态下还有哪些合法事件？退款、重开各去向哪里？"
- "从 待审核 到 审核中 的边是否存在？还是这两个其实是同一状态？"

**Common traps**:

- 组合留空不定义
- 终态意外有出边（"取消后还能回进行中"）
- 把"业务上不可能"与"被禁止"混为一谈

---

## 4. 守卫条件（Guard Condition）

**When to use**: when a guard is vague; or when the same transition fires under different conditions with different targets; or when the guard can't be expressed as a BR-checkable rule.

**Question shape**:

```
[为什么重要] 守卫条件必须可判真伪，否则无法写进 BR 校验。
从 [状态A] 到 [状态B] 的守卫条件是? 是否可写成可判定表达式(时间/数值/角色/状态)?
条件不满足时停留原状态，还是走别的分支?
```

**Examples**:

- "「订单异常时自动驳回」——异常的具体判定是什么？超时 30 分钟？还是校验失败？"
- "从 待支付 到 已取消：条件是超时 30 分钟，还是用户主动取消？两个条件去向相同吗？"
- "审批通过的条件是余额充足，对吗？余额不足时走哪个分支？"

**Common traps**:

- 用形容词当条件（"当订单异常时"）
- 条件不满足时去向不定义
- 同一转移多条件不同去向未拆分

---

## 5. 副作用（Side Effects）

**When to use**: when a transition's side effects are unstated or vague ("通知相关人员"); or when related-entity updates/audit/rollback are missing; or when no-effect transitions need explicit confirmation.

**Question shape**:

```
[为什么重要] 副作用不点名，下游无法接线通知、联动与回滚。
从 [状态A] 到 [状态B] 的副作用是什么?
1. 发通知给谁、什么渠道、何时? 2. 联动更新哪些相关实体/状态? 3. 有无埋点/审计/回滚动作? 无副作用写「无」。
```

**Examples**:

- "从 已支付 到 已发货，是否通知用户发货？短信还是站内信？"
- "取消订单是否联动更新库存、释放优惠券？"
- "驳回是否记审计日志？回滚已扣的款项吗？"

**Common traps**:

- 写"通知相关人员"不点名
- 联动更新遗漏
- 无副作用不写「无」，让实现方自行发挥

---

## 6. 非法转移（Forbidden Transition）

**When to use**: when a transition should be forbidden but is unstated; or when the reject behavior is unclear; or when security/permission gating on a transition is missing.

**Question shape**:

```
[为什么重要] 被禁止的转移若不显式标注，实现方会按"默认允许"处理。
从 [状态A] 到 [状态B] 是否被禁止? 为什么? 尝试该转移时系统如何响应(拒绝并提示/忽略/记录)?
```

**Examples**:

- "已取消 的订单能重新发货吗？若不能，标注「不允许」。"
- "未授权的角色尝试推进审批状态，系统如何拒绝？"
- "从 已支付 回退到 待支付 是否被禁止？回退会导致重复扣款吗？"

**Common traps**:

- 非法转移留空（等于默认允许）
- 拒绝行为（提示/忽略/记录）不定义
- 权限越权转移未排除

---

## 7. 终态与取消语义（Terminal / Cancel Semantics）

**When to use**: when terminal states are not identified; or when cancel/terminate semantics are ambiguous; or when a "cancel" path doesn't reach a true terminal state.

**Question shape**:

```
[为什么重要] 终态语义决定生命周期是否闭环，语义矛盾会误导实现。
请确认: 哪些是终态? 终态之后能否重开(如取消后重新报名)? 取消与终止是否等价?
```

**Examples**:

- "「已取消」是终态吗？用户还能重新报名、走新的流程吗？"
- "「已完成」与「已归档」是否等价？归档后还能退款吗？"
- "取消订单后优惠券是否返还？返还后状态机是否需要新状态？"

**Common traps**:

- 不识别终态
- 取消后还能回到进行中（语义矛盾）
- 终态后重开路径未定义

---

## 8. 超时/并发/重复事件（Timeout / Concurrency / Duplicate）

**When to use**: when implicit transitions (timeout auto-cancel, session expiry) are missing; or when duplicate/concurrent triggers are unhandled; or when the same event arrives twice.

**Question shape**:

```
[为什么重要] 超时与重复事件是线上最常见的问题，漏掉会在生产中产生脏状态。
请确认: [状态] 的超时事件(如支付超时自动取消)规则? 重复事件(重复点击/重复回调)如何处理? 并发触发时以哪个为准?
```

**Examples**:

- "待支付 超时多久自动取消？定时任务还是事件驱动？"
- "支付回调重复到达（同一订单两次成功回调）如何保证幂等？"
- "并发下管理员驳回与用户取消同时发生，以哪个状态为准？"

**Common traps**:

- 不定义超时转移
- 重复事件/幂等不处理
- 并发竞态不澄清归属

---

## Cross-cutting tips

1. **排序原则**：Clarify 一次只问 1 个，按 Impact × Uncertainty 排序，先问阻断性高的。
2. **不要问 AI 能查的事实**：既有系统状态机、流程文档、审计日志，让 AI 自己查，不要让业务方回答。
3. **每问必带 AI 初步判断**：不要让业务方从零开始想问题。
4. **三选项常驻**：给 2-4 个互斥选项 + 「其他」兜底。
5. **跳过按钮**：非阻断项允许业务方打 ⚠️ 风险标签先跳过。
6. **回写位置必填**：每答一题必须能精确指向父文档 §状态变化 的哪条 STATE。
