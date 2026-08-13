# Question Patterns · Project Scope

Eight canonical question templates for the one-question-at-a-time Clarify loop. Each entry gives:

- **When to use** — the trigger condition
- **Question shape** — the prompt structure
- **Three examples** — paraphrased real cases (desensitized)
- **Common traps** — typical AI mistakes when asking this kind of question

Use these as reference when generating a new question in a Clarify Session. See `SKILL.md` § Clarify for runtime rules (≤5 sessions, ordered by impact, every question carries an AI preliminary judgment).

---

## 1. 边界归属（Classification）

**When to use**: when a candidate item's In/Out/Deferred/Conditional category is unclear or contested.

**Question shape**:

```
[为什么重要] 归类决定这条是否进入本期交付。
当前候选 [具体项] 落在 [已有归类]。请确认: 它是 [In / Out / Deferred / Conditional]?依据是 [证据/约束/决议]?
```

**Examples**:

- "积分机制在邮件 SRC-002 里提到,但业务方口头说下一版本做。应归 Deferred 还是 Out?"
- "数据迁移是本期 In 还是 Conditional?旧系统数据量多大、有没有迁移工具?"
- "该候选项同时被客服团队和技术团队声称归自己管。谁拥有这条的裁决权?"

**Common traps**:

- 替决策者悄悄选边
- 把"还没想好"当成 Out（应归 Conditional 或 UNKNOWN）
- 只问"是/否"不给选项

---

## 2. Out 项原因（Out Reason）

**When to use**: when an Out item has no explicit reason, or the reason is vague ("不做这个").

**Question shape**:

```
[为什么重要] Out 必须有原因,否则下游可能悄悄把它做回来。
当前 Out 项 [具体项] 没有理由。请确认它是: [硬约束 / 业务决议 / 未来工作 / 暂不明确]?
```

**Examples**:

- "自定义工作流引擎 Out 的原因是厂商内置能力够用,还是团队没有人力?"
- "移动端 Out 是因为 Phase 2 排期,还是因为当前没有移动战略?"
- "该 Out 项如果被法务/合规再次提出,是否要升级为 Conditional?"

**Common traps**:

- 用"不做"当理由
- 把强约束和软偏好混为一谈
- 不记录 Out 项的历史来源,导致重复讨论

---

## 3. Deferred 触发（Deferred Trigger）

**When to use**: when a Deferred item has no trigger condition or planned phase.

**Question shape**:

```
[为什么重要] 暂缓项必须有触发条件,否则"以后做"永远不会兑现。
Deferred 项 [具体项] 的触发条件是什么?[用户量达到 N / 下个版本 / 预算到位 / 外部依赖就绪]?
```

**Examples**:

- "高级分析 Deferred 的触发条件是用户量过 10 万,还是直接排 V2?"
- "该 Deferred 项依赖的数据源目前不存在。它是等数据源,还是有替代方案?"
- "Deferred 项需要谁在什么时点重新评估?"

**Common traps**:

- 写"以后再说"当触发条件
- 不标注重估 owner
- 把 Deferred 当 Out 写进文档后就遗忘

---

## 4. Conditional 条件（Condition）

**When to use**: when a Conditional item's condition is vague ("if budget allows").

**Question shape**:

```
[为什么重要] 条件必须可判真,否则 Conditional 无法裁决。
Conditional 项 [具体项] 的条件要具体到可判断: 预算阈值?审批时点?由谁判断条件是否成立?
```

**Examples**:

- "预算通过则加 Salesforce 同步"——预算阈值是多少、哪个阶段的预算?
- "法务签字则放开跨境数据"——法务 review 的预计周期?签字人是谁?
- "技术就绪则接入实时推送"——就绪的验收标准是什么?"

**Common traps**:

- 条件写得太模糊,无法裁决
- 不指定判断条件的 owner 和时点
- 把 Conditional 和 In 混排

---

## 5. 重叠边界（Overlap / Seam）

**When to use**: when two teams or two projects claim the same work, or a seam is undefined.

**Question shape**:

```
[为什么重要] 范围重叠是返工和甩锅的源头。
[具体项] 同时出现在 [本项目 / 相邻项目 X / 团队 Y]。谁拥有它?交接点在哪?
```

**Examples**:

- "用户登录模块同时在本项目和单点登录项目里。谁负责?以哪个为准?"
- "该报表数据由数据团队产出,但页面在我们这边。数据口径谁定?"
- "相邻项目正在重构同一条链路。我们的范围是否需要排除它以对齐?"

**Common traps**:

- 假设重叠会自然消失
- 不记录交接 owner
- 把重叠项悄悄并进本项目

---

## 6. 验收依据（Acceptance Criterion）

**When to use**: when an In item has no verifiable acceptance criterion.

**Question shape**:

```
[为什么重要] 验收依据决定"做到什么程度算完成"。
In 项 [具体项] 的验收标准是什么?[具体行为 + 数量/时长/通过条件 + 谁验收]?
```

**Examples**:

- "SSO 接入的验收标准是:'使用企业账号可登录全部 3 个系统'吗?"
- "数据迁移的验收是迁移成功率 ≥ 99.9%?谁确认?验证方式?"
- "培训材料的验收是材料交付,还是学员通过考核?"

**Common traps**:

- 用形容词当验收（"体验好"）
- 不指定验收人
- 把实现细节当成验收标准

---

## 7. 优先级取舍（Priority Trade-off）

**When to use**: when the In list exceeds the feasible budget/timeline and items must compete.

**Question shape**:

```
[为什么重要] 范围超载会延期或降质。
当前 In 项 [数量] 超出 [时间/预算]。请按成功判据排序: 哪些是必须保留的 must-have?哪些可降到 Deferred?
```

**Examples**:

- "按 Q4 上线倒排,只能保留 5 个 In 项。你优先保留哪 5 个?"
- "并行运行 30 天是硬要求,还是可缩减为 7 天?"
- "如果必须砍一项,砍哪个对目标伤害最小?"

**Common traps**:

- 让 AI 替业务方砍项
- 不基于成功判据排序,而基于个人偏好
- 回避取舍,默认全保留

---

## 8. 决策权威（Decision Authority）

**When to use**: when it is unclear who owns a boundary decision, or when stakeholders disagree.

**Question shape**:

```
[为什么重要] 边界裁决必须有明确 owner,否则争议无法收敛。
[具体争议项] 的裁决权属于谁?[goal_decision_owner / business_sponsor / 项目 PMO / 其他]?
```

**Examples**:

- "In/Out 清单由谁最终签字?是业务负责人还是 PMO?"
- "法务相关的边界项,是否需要法务负责人加入审批链?"
- "该争议项已僵持两周。是否需要升级到更高权威?"

**Common traps**:

- 默认 PM 或 AI 拥有裁决权
- 争议项没有 owner 就一直挂着
- 不记录裁决时点和结果

---

## Cross-cutting tips

1. **排序原则**: Clarify 一次只问 1 个,按 Impact × Uncertainty 排序,先问阻断性高的。
2. **不要问 AI 能查的事实**: 公开范围口径、历史迭代范围,让 AI 自己查。
3. **每问必带 AI 初步判断**: 不要让业务方从零开始想问题。
4. **三选项常驻**: 给 2-4 个互斥选项 + 「其他」兜底。
5. **回写位置必填**: 每答一题必须能精确指向 project-scope.md 的哪个章节。
6. **争议必路由**: 不能收敛的争议项登记 issue-record（DEC/CLS）并标注裁决 owner。
