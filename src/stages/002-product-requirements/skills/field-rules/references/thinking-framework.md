# 思考框架（Thinking Framework · field-rules）

用这些透镜改进字段定义表候选产物。不要把完整分析倾倒进产物。

## 公共核心（Common Core，必用 MANDATORY）

应用 `src/framework/thinking-core.md` §1 的 **6 个核心透镜**（第一性原理、系统思维、对抗性审视、逆向验证、确认偏误防御、知识边界），以及 §2 中与本 work item 相关的检查层透镜（Human Gate 前的 Fresh-Eyes、写作时的结论先行 + 读者视角）。只记录会改变字段定义的发现。

## 第一性原理（First Principles）

- 本期 PRD 必须定义的字段是哪些？没有这些字段，业务能否跑通？
- 哪些字段其实是派生字段（可从其他字段计算得出），不必单独定义？

## 对抗性审视（Adversarial Review）

- 哪些看起来必要的字段其实是冗余 / 可派生？
- 字段类型是否在模糊（"文本" vs 精确的 string/enum）？
- 被引用次数 = 0 的字段是否应标"删除候选"？

## 逆向验证（Reverse Validation）

- 每个字段被什么校验（VL-XXX）或业务规则（BR-XXX）引用？
- 没有被任何下游引用的字段，其存在理由是什么？

## 系统思维（Systems Thinking）

- 相同语义的字段是否类型一致（如 user_id 全局 int）？
- 字段增删改如何级联到 validation-rules（校验对象跟着变）？

## 知识边界（Knowledge Boundary）

- 每个字段的来源（业务方填写 / 系统生成 / 第三方同步）是否明确？
- 类型、长度、必填、默认值这些是 FACT 还是 AI 推断？

## 低密度降级模式（Low-Density Degradation Mode）

当上游 FE/FF/PD/IX 未提供足够字段线索、无法画出字段定义表时（触发：无任何表单/入参字段线索）：

```text
low-density input → skip field-table ideation
                   → do not enter Generate / Audit
                   → output only:
                      a) 字段线索充分度评估（来自 FE/FF/PD/IX 的字段数）
                      b) 批量澄清问题（字段类型 / 长度 / 必填 / 默认值 / 来源）
                   → status = needs_user_input
```

此模式不是失败状态。它是信息不足时的正确反应——产出干净的澄清问题，而不是一份塞满"待确认"的空字段表。
