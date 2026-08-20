# issue-record（跨阶段共享）

全局 PM/PRD 问题清单 · 任何阶段遇到"待确认" / UNKNOWN / CONFLICT 时，AI 自动登记带来源的 draft/open ISS-NNN。

## 用途

- 集中维护 BLK / RSK / DEC / INF / CLS / OUT 六类问题
- 跨阶段共享：一个需求从 background-goal 到 PRD 汇总，所有"未决"都在这里
- 给业务方一个权威的"还有什么没解决"清单
- 跟踪 owner、状态、目标关闭日期、缓解措施
- PRD 确认前必经的"问题清零"环节

## 不该用

- 想写需求 / 用户故事 / 设计（用对应 Skill）
- 仓库缺陷、测试失败、部署故障或研发实现任务（走工程维护，不进入 PM/PRD 问题清单）
- 业务方还没提出，自己推测的"风险"（不要 AI 主动写问题清单）

## 强制行为

**AI 必须自主登记**：当用户输入或源材料出现以下任一信号时：
- `待确认` / `我不确定` / `可能` / `也许` / `大概` / `之后再说` / `再看看`
- `?` / `TODO` / `TBD` / `[空]`
- 两个来源对同一事实给出不同表述
- 业务方口头表达但未签字
- 推导结果与某条 FACT 冲突
- 阶段产物生成后仍有 `UNKNOWN` 知识状态遗留

→ AI 必须在给出方案之前自动登记为带来源的 `ISS-NNN`，然后向用户展示：

> 我注意到 [引用具体源] 中存在 [BLK/RSK/DEC/INF/CLS/OUT] 信号：[具体描述]。
> 已登记 Issue Record（ISS-NNN）：[类别] / [具体描述] / [来源] / 建议 owner=[推荐 owner]。
> 请确认：1. 类别与 owner；2. 现在回答并回写 [目标产物 §X]；3. 是否由 [授权 owner] 接受风险或作出决策。

## 章节速查

| § | 标题 | 何时填写 |
|---|---|---|
| 1 | 项目元数据 | 起草时 |
| 2 | 总览（按类别与状态计数） | Generate 后 |
| 3 | Blocker（BLK） | 必有 |
| 4 | Risk（RSK） | 必有 |
| 5 | Decision-in-waiting（DEC） | 必有 |
| 6 | Information gap（INF） | 必有 |
| 7 | Clarification（CLS） | 必有 |
| 8 | Out-of-band（OUT） | 必有 |
| 9 | Closed Issues | 必有 |
| 10 | 来源追溯 | 必有 |
| 11 | 待确认问题 | 必有 |
| 12 | Constitution Compliance | 必有 |

## 与上下游的衔接

- **上游汇聚点**：所有产物（background-goal、user-journey、user-stories、feature-list、functional-flow、page-design、interaction-rules、business-rules、validation-rules、state-machine、exception-handling、acceptance-criteria、PRD）的"待确认"都应被提升为 ISS-NNN
- **下游关闸**：每次 `pipeline.py ... gate` 都校验 Issue Record 的存在、结构与 B3 收口；PRD 的人工确认仍由 `prd-assembly` work item 的 `pipeline.py review` 完成。Issue Record 不作为独立 work item 要求不可达的 `confirmed` 状态。
- **同级互补**：scope 定"做什么"，issue-record 列"卡点/风险/待决"
- **与 `clarify/issue-templates/question-record.md` 共存**：单条 QuestionRecord 提问模板 vs. 全局 PM/PRD 问题清单

## 审计硬约束

- 所有 open 状态必须有 owner
- BLK / DEC 必须有 target_close
- 30 天以上的 open 状态必须有 escalation 记录
- 与上游产物的"待确认"必须一一对应或有 documented 关闭理由
- 每条 AI 登记的问题必须有来源与知识状态；风险接受、业务 owner、关闭与确认必须经授权人工确认

## 验证

```bash
python3 scripts/validate_artifact.py <产物路径> --json
```

其中 `<产物路径>` 是生成的 `issue-record.md`（如 `requirements/REQ-XXX/99-review/support/issue-record.md`）；空模板见 Skill 目录下的 `assets/issue-record-template.md`。
