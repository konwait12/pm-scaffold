# Question Patterns · 异常与失败处理

Eight canonical question templates for the one-question-at-a-time Clarify loop. Each entry gives:

- **When to use** — the trigger condition
- **Question shape** — the prompt structure
- **Three examples** — paraphrased real cases (desensitized)
- **Common traps** — typical AI mistakes when asking this kind of question

Use these as reference when generating a new question in a Clarify Session. See `SKILL.md` § Clarify for runtime rules（一次一问、≤5 问、按 Impact × Uncertainty 排序）。

---

## 1. 来源（Source）

**When to use**: when a failure scenario or recovery policy has no authoritative source; or when sources conflict on how a failure should be handled.

**Question shape**:

```
[为什么重要] 失败场景必须可追溯，恢复策略必须有人拍板。
当前 [功能/EX] 的 [失败内容] 来自 [来源 A] 而非 [来源 B]，请确认 [是 / 否 / 待补充]?
```

**Examples**:

- "FUN-001 的「余额不足」失败来自 BR-007,但纪要 SRC-002 提到还有「账户冻结」。哪一种失败是本期必须接住的?"
- "「重试 3 次」是业务方决定的,还是 AI 推断的?如果是推断,应该标 AI_INFERENCE 并请业务确认。"
- "线上监控 SRC-003 显示网络超时 P99=8s,但产品没有定义超时策略。能否请业务补一句恢复策略作为 DECISION?"

**Common traps**:

- 接受口头描述的失败不登记 SRC-*
- 把监控数据（FACT 观察）当成业务策略（需要 DECISION）
- 不同来源对同一失败处理说法矛盾时静默选边

---

## 2. 失败源（Failure Source）

**When to use**: when a function's failure branches are absent or only list the most obvious one; or when the six failure-source classes were not walked.

**Question shape**:

```
[为什么重要] 失败源枚举不全 = 下游无法差异化恢复。
FUN-XXX 目前只写了 [已有失败]。请确认: [校验 / 权限 / 资源 / 业务 / 冲突 / 网络] 中哪些在本函数真实可能发生?哪些明确不适用?
```

**Examples**:

- "FUN-003（库存扣减）只写了网络超时。库存并发超卖、SKU 失效、数量不足这些业务/冲突失败是否真实存在?"
- "FUN-001 提到权限失败,但对应角色矩阵里所有角色都允许提交。是否应该标「不适用」而不是留空?"
- "客服工单 SRC-004 提到用户会重复点提交导致重复扣款。这是否应该补一条幂等/并发冲突的失败?"

**Common traps**:

- 所有函数套用同一组失败源,不按函数真实风险排查
- 把「不适用」写成留空,让下游误以为未覆盖
- 漏掉高频的用户错误（重复提交、误操作）

---

## 3. 系统行为（System Behavior）

**When to use**: when a failure row's system behavior is blank; or when behavior is described only as "系统处理失败".

**Question shape**:

```
[为什么重要] 系统行为决定失败后发生了什么,不能留白。
FUN-XXX 的 [失败场景] 发生后,系统应该 [拦截 / 降级 / 回滚 / 阻断] 哪一步?具体做什么?
```

**Examples**:

- "EX-001 网络超时发生后,系统是保留草稿、自动重试,还是直接失败?行为要落到可观测。"
- "「活动已结束」驳回时,系统只是拒绝提交,还是要回滚已选场次的状态?"
- "并发版本冲突时,系统是提示用户刷新,还是强制覆盖?这影响数据安全,需要业务决定。"

**Common traps**:

- 系统行为留空或写「提示用户」
- 把「回滚」写得很含糊,不说明回滚到哪个状态
- 对金钱/库存类失败不写补偿行为

---

## 4. 恢复策略（Recovery Policy）

**When to use**: when a recovery path lacks a boundary (count, interval, idempotency); or when retry/rollback is asserted without a policy.

**Question shape**:

```
[为什么重要] 恢复策略决定用户能不能自己恢复。
FUN-XXX 的 [失败场景] 恢复方式写的是 [重试 / 手动 / 自动 / 终止],请明确: 重试几次?间隔多久?是否幂等?需不需要人工介入?
```

**Examples**:

- "EX-002 写「重试」,但没说几次、间隔多久。是 3 次 × 30s 还是无限重试?幂等吗?"
- "扣款失败后自动重试,如果网络抖动恢复,会不会重复扣款?需要幂等键还是改为手动重试?"
- "不可恢复的失败（如账号被冻结）是终止并引导客服,还是让用户无限点重试?"

**Common traps**:

- 写「重试」不写边界（次数/间隔/幂等）
- 可恢复与不可恢复用同一条恢复路径
- 不区分用户可自助恢复与必须人工介入

---

## 5. 用户提示（User Prompt）

**When to use**: when the user prompt is an error code, "请联系管理员", or inconsistent with the recovery path.

**Question shape**:

```
[为什么重要] 用户提示决定用户能否自助恢复,必须与恢复策略一致。
FUN-XXX 的 [失败场景] 用户提示文案是 [已有文案],能否改为说明「哪里失败 + 用户能怎么办」的中文?
```

**Examples**:

- "EX-003 用户提示是「ERROR-500」,用户不知道发生了什么。能否改为「提交失败,请检查网络后重试」?"
- "提示文案说「请重试」,但恢复策略是「终止并人工处理」,两者矛盾。以哪个为准?"
- "提示「请联系管理员」但对不可恢复失败确实需要人工,这句提示是否可保留但补充处理时效?"

**Common traps**:

- 用户提示用内部错误码
- 提示与恢复路径语义矛盾（提示重试但系统不重试）
- 可恢复与不可恢复共用一句提示

---

## 6. 补偿（Compensation）

**When to use**: when a money/inventory/data-affecting failure has no rollback or compensation; or when compensation is asserted without scope.

**Question shape**:

```
[为什么重要] 涉及金钱/库存/数据的失败必须有补偿,否则资损与数据不一致。
FUN-XXX 的 [失败场景] 影响 [金钱/库存/数据],补偿方式是 [回滚 / 冲正 / 人工处理]?回写哪些字段?是否幂等?
```

**Examples**:

- "扣款成功但下单失败,是否自动原路退回?退回到哪一步状态?"
- "库存预占成功但支付超时,释放库存的时机是什么?超时多久释放?"
- "补偿操作失败怎么办?是否需要告警 + 人工对账,补偿路径本身要不要定义失败分支?"

**Common traps**:

- 对金钱/库存失败不写补偿
- 补偿写「自动回滚」却不说明回滚范围与触发时机
- 忽略补偿自身失败的兜底

---

## 7. 优先级（Priority）

**When to use**: when which failure branches must be handled this release is unclear; or when scope creep from rare edge cases is high.

**Question shape**:

```
[为什么重要] 失败处理也要排优先级,不是所有边角失败都本期做。
请圈定: [候选项] 中哪些失败本期必须接住,哪些可以标注「后续版本」?
```

**Examples**:

- "磁盘满、机房宕机这类系统级失败,本期是否只做降级提示,不做完整恢复?"
- "账号冻结影响极少数用户,但处理复杂。能否本期只终止提示,恢复流程下一期?"
- "网络超时重试本期必做,那重试导致的重复提交防护是否也在本期?"

**Common traps**:

- 把全部失败都塞进本期,不做优先级
- 遗漏「本期不做但相邻」的失败处理,不写非目标
- 优先级与该函数 P0/P1 不一致

---

## 8. 边界（Boundary）

**When to use**: when a proposed EX row actually belongs to validation-rules, state-machine, interaction-rules, or implementation.

**Question shape**:

```
[为什么重要] 异常处理只接「失败如何恢复」,不接「是否拒绝输入」「状态如何流转」「UI 如何提示」。
FUN-XXX 的 [内容] 更接近 [校验规则 / 状态机 / 交互 / 实现细节],是否应移交给对应子技能?请确认落位。
```

**Examples**:

- "「手机号格式校验」是字段校验规则,应交给 validation-rules,不在 EX 表重复定义。"
- "「重试时状态从未提交流转到重试中」是状态机内容,交给 state-machine。"
- "表里出现 try-catch、超时毫秒数,这些是实现细节,异常表只保留产品级行为。"

**Common traps**:

- 把校验/状态/交互内容写进异常表
- 把实现细节（异常类型、MQ、幂等键）混入产品语义
- 与上游子技能重复定义同一失败处理

---

## Cross-cutting tips

1. **排序原则**：Clarify 一次只问 1 个，按 Impact × Uncertainty 排序，先问阻断性高的。
2. **不要问 AI 能查的事实**：监控数据、缺陷记录、客服工单能确认失败发生，让 AI 自己查，不要让业务方从零想。
3. **每问必带 AI 初步判断**：先给出你的推断（如「据 BR-007 推断需补偿回滚」），让业务方确认而非从零回答。
4. **三选项常驻**：给 2-4 个互斥选项 + 「其他」兜底。
5. **跳过按钮**：非阻断项允许业务方打 ⚠️ 风险标签先跳过。
6. **回写位置必填**：每答一题必须能精确指向父文档的哪个 FUN-XXX / 哪个 EX-XXX。
