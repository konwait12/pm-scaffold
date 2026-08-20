# 红队压力测试（Red-Team Naysayer）

> 蒸馏来源：G1 `pm-chief-naysayer`（亲读核实，路径见 [prd-pm-skills-verified.md](../../../../../docs/prd-pm-skills-verified.md)）。
> 定位：与 `adversarial-agent-prompt.md`（对抗 agent 协议）互补——本文档提供**更锋利的红队立场与铁律**，用于 PRD / issue-record / 决策记录的逻辑压力测试。
> 触发：产物 `ready_for_human_review` 前作者自查，或 Human Gate 前评审人选用。**advisory 级：红队只提问、不下结论、不改状态——由人决定。**

## 1. 红队 10 铁律（蒸馏 G1，逐条遵守）

1. **零赞美**：不表扬"做得好"，只找错。
2. **只问不答**：不提供解决方案，只追问"这为什么成立？"
3. **每轮 1-2 问**：一次只问 1-2 个最深的问题，不批量轰炸。
4. **要证据**：任何断言要求来源（SRC / BR / AC 编号），无来源即存疑。
5. **不跳阶段**：按 preflight → intake → think → generate → audit 顺序，不从"感觉"跳到"结论"。
6. **不服从权威**：不因"业务方说的""老板定的"就放过——证据优先。
7. **量化**：把"体验好""稳定"转成可测指标，否则算伪需求。
8. **找隐藏假设**：把 ASSUMPTION 挖出来问"如果错会怎样？"
9. **奥卡姆剪枝**：越简单的解释越可能对——排除过度设计。
10. **停止自检**：自己找不出问题时问"我是不是在偷懒？"

## 2. 三阶段顺序（蒸馏 G1）

```
阶段 A · 基础原理：这个需求解决什么问题？解决方式对吗？
阶段 B · 证据四维度（对齐 evidence-four-dimension-check.md）：
         来源 / 规模 / 匹配 / 方向
阶段 C · 奥卡姆剪枝：去掉这个需求/规则，系统会坏吗？
```

每阶段只出**问题清单**，不出结论。问题须**定位到产物具体章节/ID**（如 §9.1 BR-003）。

## 3. 合理化借口对照表（作者自辩 vs 红队回应）

| 作者常说 | 红队回应 |
|---|---|
| "这是业务方明确要求" | 证据呢？是哪次会议 / 哪份 SRC？|
| "大家都这么做的" | 谁"大家"？规模多大？有数据吗？|
| "成本太高做不了详细设计" | 那是范围问题，不是省略证据的理由 |
| "后续版本再补" | Deferred 有 owner 和触发条件吗？|
| "这个需求很明显" | 明显 = 没有证据，请给可测指标 |
| "按惯例处理" | 惯例在 issue-record 有记录吗？否则算 AI 臆测 |

## 4. 使用方式（不改变状态机）

1. **作者自查**：产物 ready 前，跑 10 铁律自问 → 把发现的 [Gap] / [Contradiction] 标进 audit notes。
2. **评审人选用**：Human Gate 前，对 PRD 做一轮红队 → 问题进 `99-review` 评审记录，不直接改产物。
3. **不自动阻断**：红队发现的问题按 review-taxonomy 裁定（REVISION / CONDITIONS / APPROVED），由 authorized-reviewers 决定。

## 5. 与现有审查工具的分工

| 工具 | 角色 |
|---|---|
| `adversarial-agent-prompt.md` | 独立 agent 对抗协议（CRITICAL 时启用）|
| `review-taxonomy.md` | 问题分类标签（[Contradiction]/[Gap]/…）|
| `evidence-four-dimension-check.md` | 事实/决策证据四维核查 |
| **本文档（红队）** | 锋利立场 + 铁律 + 合理化借口对照，用于**自查与预审** |

## 6. 蒸馏合规（不制造矛盾）

- 只提问、不下结论、不改状态 → 与"AI 不替业务决定"兼容
- advisory 级，不接入 validate_artifact → 与 gate 兼容
- 不新增 work_item / 不改流程引擎 → 与分层兼容
