# 思考框架（Thinking Framework · project-scope）

用这些透镜改进范围基线候选产物。不要把完整分析倾倒进产物。

## 公共核心（Common Core，必用 MANDATORY）

应用 `src/framework/thinking-core.md` §1 的 **6 个核心透镜**（第一性原理、系统思维、对抗性审视、逆向验证、确认偏误防御、知识边界），以及 §2 中与本 work item 相关的检查层透镜（阶段收口前的 Pre-Mortem、Human Gate 前的 Fresh-Eyes、写作时的结论先行 + 读者视角）。只记录会改变范围基线的发现。

## 第一性原理（First Principles）

- 本期 PRD 真正必须解决的 1 件事是什么？
- 去掉某个 In 项后，目标仍然成立吗？
- 哪些"In"其实是实现细节，而非范围？

## 对抗性审视（Adversarial Review）

- 哪些看起来 In 的功能其实是 Out（业务方没要求，AI 想当然加进去）？
- 哪些 Out 会引起业务方反弹？如果会，是否应改为 Conditional？
- 范围是否在优化一个角色的同时损害另一个？

## 逆向验证（Reverse Validation）

- 从"本期就做这些 In"出发，成功交付必须成立的前提是什么？
- 每个 In 项是否都有明确的 success_signal？没有信号的范围项 = 不可验收。

## 系统思维（Systems Thinking）

- 范围变化如何影响下游 UJ / US / FE 的触点、故事与功能点？
- 一个 In 项是否依赖某个 Out 项才能成立（隐性耦合）？

## 知识边界（Knowledge Boundary）

- 每条假设标了 F/D/A/AI/U/C 吗？假设可被什么证据推翻？
- 依赖是否有 Owner + 计划落地日期，还是含糊的"待定"？

## 低密度降级模式（Low-Density Degradation Mode）

当 BG/FA 未提供足够范围线索、无法画出四态基线时（触发：无任何 In/Out 草稿、无风险姿态输入）：

```text
low-density input → skip four-state ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) 范围线索充分度评估（来自 BG/FA 的 In/Out 草稿数）
                      b) 批量澄清问题（In 边界 / Out 边界 / Conditional 触发 / 依赖 Owner）
                   → status = needs_user_input
```

此模式不是失败状态。它是信息不足时的正确反应——产出干净的澄清问题，而不是一份塞满"待确认"的空范围基线。
