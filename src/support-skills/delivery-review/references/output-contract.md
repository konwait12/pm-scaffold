# 输出契约：交付评审包

文件：`99-review/support/delivery-review.md`。这是过程记录，不进入最终 PRD 正文。

## Frontmatter

```yaml
artifact_id: DR-001
version: v0.1
status: ready_for_human_review
owner: 产品经理
reviewer: 业务负责人
source_ids: SRC-001, FEA-001
created_at: 2026-08-20
updated_at: 2026-08-20
```

`status` 只能是 `draft`、`needs_user_input`、`ready_for_human_review` 或 `superseded`；本记录禁止 `confirmed`。

## 必须章节

1. **交付结论**：当前是否具备人工评审条件，以及不具备时的阻断原因。
2. **需求拆解**：每行一个命题，包含范围内、范围外、知识状态和来源。
3. **行为验收**：每个命题至少一个可复现的 Given/When/Then、输入输出或命令断言。
4. **证据索引**：列出来源 ID、文件路径、命令和运行结果；不可验证的内容标 `UNKNOWN`。
5. **失败边界与回退**：至少一个异常/边界场景，说明影响和回退依据；确实无需回退时写理由。
6. **未决项与责任人**：问题、owner、阻断性、下一步和期限；无未决项须写“无未决项（已核对）”。
7. **人工决定**：保留给授权人填写的 approve / revise / reject、姓名、时间和意见。

## 语义红线

- 没有来源的业务事实只能写 `AI_INFERENCE` 或 `UNKNOWN`。
- “完成”“稳定”“体验好”等不可观察形容词不能单独作为验收判据。
- 评审包不能新增上游没有确认的范围、数字、阈值或验收结论。
- 未完成人工决定时，不得写 `confirmed`，也不得把评审包当成 PRD 来源。
