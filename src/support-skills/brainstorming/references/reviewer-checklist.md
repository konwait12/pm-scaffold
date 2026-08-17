# 人类审查清单 · Brainstorming（发散收敛）

> 本清单给 **business_owner（业务负责人）** 在审查 `brainstorming-output.md` 时使用——你看到的是 AI 对某个 L0 想法的发散候选，你要判断它发散得够不够、是否值得收敛进需求。
> 不是给 AI 看的（AI 看 `audit-checklist.md`）。
> 每条 = "是 / 否 / 不适用"，有"否"则可要求 AI 修订并发散补充。

## 覆盖（Coverage）
- [ ] 12 维度是否都扫过或显式说明跳过了（lifecycle / roles / normal-alternate-exception-failure-timeout / permission / data condition / handoff / dependency / cancellation / retry / rollback / change-recovery / constraint）？
- [ ] 有没有明显重要的候选被漏掉？例如你知道某个关键角色、某条硬约束或某个善后场景，清单里却看不到。
- [ ] 有没有候选跨了两个维度却只标了主维度的？——那没关系，但要能交叉引用。

## 质量（Quality）
- [ ] 每条候选是不是**独立**的想法？有没有两条其实在说同一件事（近似重复）没有合并？
- [ ] 有没有候选把 AI 的推断写成"事实"了？——发散候选应全是 `AI_INFERENCE`，除非它来自你提供的书面材料。
- [ ] 每条的 Evidence（AI 为什么这么想）与 Impact（纳入后会怎样）是否说清楚了，有没有空着或"待确认"？

## 处置（Disposition）
- [ ] 你是否清楚每个候选的 **include / exclude / defer / research** 含义？
- [ ] 对 `defer` 的候选，你是否接受它的触发条件或计划周期？（deferral risks）
- [ ] 对 `research` 的候选，它是否被登记进了 issue-record / QuestionRecord 会被跟进，而不是就被搁置了？

## 收敛（Convergence）
- [ ] `include` 的候选足够支撑进入 `project-background-goal` 输入包吗？被纳入的内容是否足以让下游"不需要重新调研就能开始"？
- [ ] 只有 `include` 的选进了输入包，exclude / defer / research 没有被混入吗？
- [ ] 输入包综合是否 ≥ 50 字、表达了"要探索什么"而不是一个做好的方案？

## 最终判断
请直接回答：
1. **这份发散结果我如何处置？** 全部认可进入下一步，还是先让 AI 补充某个维度？
2. **哪些 include？** 在处置表里标记你想要的候选为 `include`（及其写回目标）。
3. **哪些研究？** 把需要确认的候选标为 `research`，交 issue-record 跟进。
4. 处置完成后，确认 `include` 项综合成的输入包可以交付 `project-background-goal`。