# 思考框架 · Brainstorming（发散收敛 · 单模式）

用这些透镜把"L0 一行想法 / 稀疏材料"扩展成一组可被人工处置的候选。不要把完整分析倾倒进产物——只记录会变成 `SCN-XXX` 候选、会改变候选集或需人工补答的发现。

本 skill 是**发散器**：只负责把想法发散成候选、聚类收敛并交人工四值处置。它不做需求复述确认（那是 `requirement-restate` 的职责）、不做冲突路由（CONFLICT 是复述阶段的职责）、不做可行性判断。

---

## 公共核心（Common Core，必用 MANDATORY）

应用 `src/framework/thinking-core.md` §1 的 **6 个核心透镜**（第一性原理 First Principles、系统思维 Systems Thinking、对抗性审视 Adversarial Review、逆向验证 Reverse Validation、确认偏误防御 Confirmation Bias Defense、知识边界 Knowledge Boundary），以及 §2 中与本 work item 相关的检查层透镜（阶段收口前的 Pre-Mortem、Human Gate 前的 Fresh-Eyes、写作时的结论先行 Conclusion First + 读者视角 Reader Perspective），并可择用 §3 发散与决策层中同发散相关的载体（如 MECE 穷举、同理心视角）。

口径与 `requirement-restate` 的 Think 段保持一致，但**只记录会变成候选的发现**，不逐字重复核心透镜分析。发散专用透镜不代替 §1 必用透镜，二者叠加使用。

- **第一性原理（First Principles）**："这个想法想改变什么可观察结果？剥离所有提议方案后，它本身是什么？"——产出候选的「目标锚点」。
- **系统思维（Systems Thinking）**："这个想法隐含哪些正在推进的上游/下游系统？涉及哪些角色、数据、流程？"——产出跨系统影响的候选。
- **角色视角（Role Perspective）**："对每个可能角色，他们获得什么、失去什么、需要什么？"——产出角色动机类候选。
- **约束分析（Constraint Analysis）**："想法里嵌入的硬约束（时间/预算/技术/合规）是否不能静默忽略？"——产出约束类候选。
- **对抗性审视（Adversarial Review）**："最糟的展开方式是什么？候选是否防御了这种误读？"——见下文「发散特化」。
- **逆向验证（Reverse Validation）**："从想要的结果倒推，什么必须先成立？"——见下文「发散特化」。
- **确认偏误防御（Confirmation Bias Defense）**："我是不是顺着上游/用户的方案在发散，把 AI_INFERENCE 当成了 FACT？"——防止把候选写实。
- **知识边界认知（Knowledge Boundary）**："已知 / 未知 / 自以为知道，三者分清了没？"——见下文「发散特化」。

> 再次强调：本记录的每条发散候选在人工标记 `include` 之前都只是 `AI_INFERENCE`。没有任何发散内容是业务事实，除非它显式来自已登记的 `SRC-*` 材料。

---

## 发散领域 lens（Divergence Domain Lenses）

这是本 skill 的核心发散手段：按 **12 个场景维度**系统性地把"一行想法"扩展成候选。对每个维度问对应的问题并产出候选想法；一旦某个维度的候选开始重复（饱和），停止该维度。

| # | 维度 Dimension | 发散提问 |
|---|---|---|
| 1 | lifecycle 生命周期 | 这件事从开始到结束有哪些阶段？当前停留在哪个阶段？每个阶段会引出什么候选行为？ |
| 2 | roles 角色 | 谁会发起、执行、受益、受扰？每类角色的动机与顾虑？是否有被遗漏的间接角色？ |
| 3 | normal / alternate / exception / failure / timeout 正常·备选·异常·失败·超时 | 主路径是什么？备选路径？系统失败、异常与超时分别怎么处理？ |
| 4 | permission 权限 | 谁有权限做什么？不同角色看到的范围是否不同？权限边界在哪里？ |
| 5 | data condition 数据条件 | 哪些数据必须存在才能继续？数据缺失、脏数据、迟到的数据怎么办？ |
| 6 | handoff 交接 | 哪个节点从一个人/系统交接到另一个人/系统？交接时的信息是否完整？ |
| 7 | dependency 依赖 | 依赖哪些内部系统、外部供应商、审批或时间窗口？依赖不可用时怎么办？ |
| 8 | cancellation 取消 | 事情中途取消的触发条件与善后是什么？取消后的数据与通知怎么处理？ |
| 9 | retry 重试 | 哪些步骤需要重试？重试上限与策略？重试是否有副作用？ |
| 10 | rollback 回滚 | 已生效的结果能否回滚？回滚的代价与边界是什么？ |
| 11 | change-recovery 变更恢复 | 需求或方案变更后，如何恢复到一致状态？遗留的半完成状态怎么收尾？ |
| 12 | constraint 约束扫描 | 时间、预算、技术、合规四类约束各自会把想法展开成什么样？ |

> 12 维度列表与发散提问的权威来源：本文件的发散 lens 表。发散收敛流程的操作版见 `SKILL.md` §3 Think 与 §5 Generate。

---

## 聚类与去重（Clustering And Deduplication）

不聚类去重的发散只会产出几十条近似重复候选，无法交给人工一条条处置。规则：

- **合并重复措辞**：用不同措辞表达同一独立想法的候选合并，保留最清晰的措辞，把其余措辞作为 Evidence 里的同义表达记下。
- **跨维度交叉引用**：同时落在两个维度的候选留在它的**主维度**，在 Candidate 单元格中交叉引用另一个维度，不拆成两条。
- **饱和规则**：当一个维度**连续两轮产不出新的独立想法**时，停止该维度；全部十二维扫完后，若整体连续两轮无新增独立想法，散发收敛即告完成。
- **一个独立想法 = 一个 `SCN-XXX`**：去重后为每个独立想法分配稳定 ID（`SCN-001`、`SCN-002`…），ID 不随排序变化，便于人工处置与写回追踪。

---

## 发散特化的三个透镜

### Adversarial Review（对抗性审视，发散特化）

- 所述想法是否只是某个未明说问题的**症状**？把它写成症状背后的问题候选。
- 政策/流程改变能否在没有任何产品改动的情况下满足它？——这类候答应被提出但倾向 `defer` 或 `exclude`，不做可行性判断。
- 某个候选的证据是否只来自一个利益相关方？是否优化了一方而伤害另一方？
- 如果想法被反方向重写，哪个候选能存活下来？——用以剔除防御不了误读的候选。

### Reverse Validation（逆向验证，发散特化）

从预期结果出发，问"成功必须成立什么"；用结果揭示缺失的前提、依赖、基线数据与约束，把这些缺口作为**新候选**补进对应维度，而不是留在心里。

### Knowledge Boundary（知识边界，发散特化）

- 每个候选在人工标记 `include` 之前**一律是 `AI_INFERENCE`**；发散集合里没有任何东西是业务事实（除非显式来自已登记的 `SRC-*`）。
- Evidence 必须说明 *AI 为什么这么想*（来自原始想法、已登记来源或常识惯例）——**绝不要把推断当作观察呈现**，不得填占位符。
- `research` 处置意味着"现在无法判定"：登记到 issue-record / 一个 QuestionRecord 跟进，而不是让它静默搁置。

---

## 稀疏降级模式（Sparse Degradation Mode）

当输入只有一句话、没有业务领域/角色/时间锚点，且负责人不可得或首批问题未答时——发散仍可进行但输出降级：

```text
sparse input → diverge into candidate skeletons (short evidence: "AI 推断，无书面来源")
             → do not force complete Evidence/Impact
             → batch ≤5 clarifying questions (each: AI preliminary judgment + options + impact + owner)
             → status = needs_user_input
             → wait for human answers, then re-enter Generate in sufficient mode
```

降级触发条件（满足任一即可）：

- 输入长度 < 50 字符且无附件、无书面材料。
- 没有业务领域、没有角色提及、没有时间约束。
- 用户只提到功能或实现，背后没有可发散的具体情境（如"做一个邀约功能"）。

此模式不是失败状态。它产出一批干净的澄清问题，而不是一份塞满 `待确认` 的臃肿候选表——从无到有强凑的发散只会是 AI 自己的猜测，却被当作候选交付。