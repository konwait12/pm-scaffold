# Question Patterns（Brainstorming）

Canonical question templates for the Clarify loop when divergence hits gaps. Each entry gives the trigger condition, the question shape, examples, and common traps. Batch ≤5 questions per session, order by impact, and register unresolved signals in issue-record per `SKILL.md` §4.

---

## 1. 想法意图（Intent）

**When to use**: when the raw idea states a feature ("做一个签到功能") with no business intent, or when "why now" is missing.

**Question shape**:

```
[为什么重要] 发散候选的锚点不清晰时，12 维扫描会空转。
当前原始想法是 [原文]。请确认: 这件事最终想改变什么 [业务结果]? 为什么是现在做?
```

**Examples**:
- "『做个签到功能』——签到的业务目的是什么？是统计到场人数、控制入场，还是会后回访依据？"
- "『客户邀约活动』——活动的业务目标是什么？答谢老客户、拉新、还是转化销售线索？"
- "这件事为什么必须这个季度做？有外部 deadline 还是内部节奏？"

**Common traps**:
- 把功能名当意图，直接按功能发散
- 不问"为什么是现在"
- 替业务方补一个"看起来很合理"的目标写进候选

---

## 2. 对象与范围（Scope / Audience）

**When to use**: when roles or the audience scope are undefined, or when the candidate set can't tell who the primary actor is.

**Question shape**:

```
[为什么重要] 角色不清则生命周期和权限维度无法发散。
请补充: 这件事涉及哪些 [角色]? 谁是 [发起人/执行人/受益者/受扰者]? 本期覆盖哪些 [对象范围]?
```

**Examples**:
- "『客户』指哪些客户？全部客户、VIP 客户，还是今年新签客户？"
- "谁发起这个活动？业务方谁对活动结果负责？"
- "现场接待这类角色本期是否需要进入候选？"

**Common traps**:
- 只发散"用户"不发散"运营/客服/法务"等支撑角色
- 不区分发起人与决策人
- 让候选在对象范围不明时"先发散着"

---

## 3. 生命周期（Lifecycle）

**When to use**: when the lifecycle dimension produced candidates with no stage boundary, or when the requestor can confirm a canonical stage order.

**Question shape**:

```
[为什么重要] 生命周期是所有后续场景的骨架。
当前候选生命周期是 [阶段列表]。请确认: 阶段划分是否符合业务实际? 有没有漏掉 [前置/后置] 阶段?
```

**Examples**:
- "邀约活动『名单准备→邀请→RSVP→签到→回访』五阶段，是否符合你们的实际流程？"
- "回访是否本期考虑？还是活动结束即止？"
- "名单准备里有没有『清洗/去重』这个内部阶段？"

**Common traps**:
- 用通用生命周期硬套业务（要问业务方认不认）
- 把"未来才做的阶段"提前进本期候选
- 阶段颗粒度忽粗忽细

---

## 4. 异常与失败（Exception / Failure）

**When to use**: when normal-path candidates exist but exception/failure/timeout candidates are missing, or when a failure candidate's impact is speculative.

**Question shape**:

```
[为什么重要] 异常场景决定成功判断的边界。
当前仅发散出正常路径。请补充: 真实业务里最常失败的 [环节] 是什么? 现在是怎么补救的?
```

**Examples**:
- "邀请发出后客户没收到/收到的是乱码，现在怎么补救？"
- "活动当天大量临时缺席，主办方接受吗？是否需要候补名单？"
- "名单里 10% 的联系方式失效，怎么处理？"

**Common traps**:
- 异常只发散"系统报错"，不发散"业务失败"
- 用通用异常清单代替问业务方
- 对失败频率乱猜数字

---

## 5. 处置标准（Disposition Criteria）

**When to use**: when the disposition table is about to be handed over and the requestor's priority/acceptance boundaries are unclear.

**Question shape**:

```
[为什么重要] 处置标准不清时，include 项可能偏离业务优先级。
请确认: 哪些候选 [必须本期有]? 哪些 [可接受后置]? 超出什么 [约束] 必须砍?
```

**Examples**:
- "预算上限是多少？超预算的候选是 defer 还是直接 exclude？"
- "如果时间只能覆盖三阶段，你最想保哪三阶段？"
- "『到场率 60%』是本期目标还是参考基线？"

**Common traps**:
- 把 AI 的优先级排序当成处置结果写进表
- 不区分"想要"与"必须"
- 处置表交给人工前不标注 deferral risk

---

## 6. 依赖与调研（Dependency / Research）

**When to use**: when a candidate is marked `research` (channel capability, vendor, existing system) and needs a follow-up owner.

**Question shape**:

```
[为什么重要] research 不落到 owner 就等于放弃。
候选 SCN-XXX 待调研项 [内容]: 谁来调研? 调研结论要回答什么 [问题]? 截止时间?
```

**Examples**:
- "短信/邮件发送渠道现状谁确认？供应商接口与配额是否支持 500 人量级？"
- "公司现有 CRM 里有没有客户名单？能不能导出？谁有权限？"
- "合规对『客户联系方式留存』有要求吗？谁负责确认？"

**Common traps**:
- research 候选不登记 issue-record，静默消失
- 让 AI 代替业务方去确认内部事实
- 调研问题提得无法回答（"看看怎么办"）

---

## Cross-cutting tips

1. 一次只问 1 个，按 Impact × Uncertainty 排序，先问阻断性高的。
2. 不要问 AI 能查的事实（公开渠道、行业报告），问业务方"内部才知道"的事。
3. 每问必带 AI 初步判断 + 候选 ID 引用，不让业务方从零想。
4. 给 2-4 个互斥选项 + 「其他」兜底。
5. 非阻断项允许业务方打 ⚠️ 风险标签先跳过。
6. 回写位置必填：每个答案必须能指向候选表/处置表的哪一行。
