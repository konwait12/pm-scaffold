# 思考框架 · Requirement Restate（复述确认能力）

用这些透镜改进重述产物。不要把完整分析倾倒进产物——只记录会改变重述的发现。

## 公共核心（Common Core，必用 MANDATORY）

应用 `src/framework/thinking-core.md` §1 的 **6 个核心透镜**（第一性原理 First Principles、系统思维 Systems Thinking、对抗性审视 Adversarial Review、逆向验证 Reverse Validation、确认偏误防御 Confirmation Bias Defense、知识边界 Knowledge Boundary），以及 §2 中与本 work item 相关的检查层透镜（阶段收口前的 Pre-Mortem、Human Gate 前的 Fresh-Eyes、写作时的结论先行 Conclusion First + 读者视角 Reader Perspective）。只记录会改变候选产物的发现——不要逐字重复核心透镜分析。

---

## 需求复述 lens（RR-NNN）

### Source Fidelity（来源保真度）

如果重述产物不能忠实反映来源，它就是无价值的：

- 每条 RR-NNN 行是否都追溯到具体的 SRC-ID，精确到段落或时间戳？
- `original_phrase`（原始措辞）是否 verbatim 保留（方言、口语都保留）而不是被"清洗"过？
- 重述是否是来源的翻译，而不是在它之上叠加的解读？
- "重述 vs 原话"的差异是否正是重点——而不是被抹平？

### Atomicity（原子性）

- 有没有一行塞进了两个不同的诉求？
- 每行是否都能作为 stakeholder 可以回答"是/否"的单一主张被测试？
- 如果一行需要"并且还要…"才完整，就拆开它。

### No Solution Leak（无方案泄露）

- 有没有一行包含提议的方案、技术或设计（"做一个移动应用"、"用 QR 码"）？
- 来源中提到的方案是否记录为带 `solution_leak=true` 的 *hint*，而不是当作决策？
- 开发者读重述时，是否会在诉求确认之前就开始设计？

### Stakeholder Recognition（stakeholder 认可度）

- stakeholder 能否在每一行里认出他们自己的话？
- 措辞是 stakeholder 的，还是 AI 用自己词汇库做的转述？
- 这份产物能否原样发回给 stakeholder，并读起来是忠实的？

### Confirmation Bias Defense（确认偏误防御，重述特化）

AI 最可能悄悄把 stakeholder 的措辞"改进"或"对齐"成 AI 认为 stakeholder 想表达的意思：

1. 我是否改了他们的词让它更"干净"？（修复：保持 verbatim。）
2. 我是否把两个听起来相似但不同的诉求合并进一行？（修复：保持分开，注明重叠。）
3. 我是否通过选择更方便的措辞解决了一个矛盾？（修复：保留双方，标 CONFLICT。）

### Knowledge Boundary（知识边界，重述特化）

1. 我是否区分了"来源说 X"（FACT）、"我推断他们想表达的意思"（AI_INFERENCE）与"还没人知道"（UNKNOWN）？
2. 冲突是否保留双方措辞，而不是丢了一方？
3. 重述的边界（我们没能转写的、我们猜测的）是否可见？

---

## 稀疏降级（Sparse Degradation Mode）

**复述版**（单句无材料，见 `SKILL.md` § Preflight L1 gate）——lens 无法做有意义工作，切降级模式：

```text
low-density input → skip lens ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) input sufficiency assessment (char count, attachments, domain guess)
                      b) batched clarifying questions (each: AI preliminary judgment + options + impact + owner)
                   → status = needs_user_input
                   → wait for human to fill in, then re-enter Preflight in sufficient mode
```

降级触发条件（满足任一即可）：

- 输入长度 < 50 字符且无附件
- 无来源材料，只有记忆转述
- 用户只提到功能或实现，背后没有可验证的诉求（"做一个打卡功能"）

此模式不是失败状态。它产出一批干净的澄清问题，而不是一份塞满 `待确认` 的臃肿重述表——从无到有构建的重述只会是 AI 自己的猜测，却被当作 stakeholder 的话呈现。
