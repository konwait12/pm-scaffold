# Issue-Record 集成指南

> 用途：告诉产物型 SKILL **什么时候**、**怎么**登记 ISS-NNN，以及 B3 阶段收口的硬性检查点。

---

## 一、issue-record 是什么

`workflow-registry.json` 中 `issue-record` 的 `output_kind: artifact`，但**默认不进 PRD 正文**——它是**问题清单**，不是需求清单。

**6 类问题**：

| 类别 | 含义 | 例子 |
|---|---|---|
| **BLK**（blocking） | 阻断性问题 | "上线范围待决，缺业务负责人签字" |
| **RSK**（risk） | 已识别风险 | "跨境数据合规风险，缺法务 review" |
| **DEC**（decision） | 待业务决策 | "VIP 阈值 10 万 vs 50 万，待 VP 拍板" |
| **INF**（information） | 信息缺口 | "缺客户分级数据，待数据团队提供" |
| **CLS**（conflict） | 歧义 / 来源冲突 | "所有角色 vs 仅经理，两份材料说法不一" |
| **OUT**（out of scope） | 范围外路由 | "积分机制已确认不进本期，路由下一版本" |

---

## 二、AI 硬约束（必须遵守）

`issue-record/SKILL.md` 第 14 行明确：

> **AI 行为硬约束**：当用户输入或源材料出现"待确认 / 不明确 / 没说过 / 模糊 / 矛盾"等信号时，AI 必须在给出方案之前将其**自动登记**为带来源的 ISS-NNN（默认 `draft` / `open`），并向用户展示类别、影响、建议 owner 与待答 Q-NNN；不得默默继续。

AI **不能**：
- ❌ 默默跳过"待确认"信号
- ❌ 自行设为 `accepted` / `resolved` / `confirmed`
- ❌ 替业务方确定 owner 或业务决策
- ❌ 发明不存在的 ISS-NNN

AI **可以**：
- ✅ 登记 `draft` / `open` / `needs_user_input`
- ✅ 标注 AI 初判（类别 / 影响 / 建议 owner）
- ✅ 触发 issue-record 的 B3 阶段收口检查

---

## 三、每个产物 SKILL 的强制登记点

每个 SKILL.md 的 §4 Clarify 阶段都必须显式提及 issue-record。具体模板：

```markdown
### 4. Clarify
- ...（原有内容）
- **遇到「待确认 / 冲突 / 信息缺口 / 风险 / 待决 / 范围外」信号时，加载 `src/shared/clarify/skills/issue-record/SKILL.md` 登记 ISS-NNN**：
  - 类别归属（BLK / RSK / DEC / INF / CLS / OUT）
  - 知识状态（FACT / DECISION / ASSUMPTION / AI_INFERENCE / UNKNOWN / CONFLICT）
  - 来源（SRC-* 或上游产物 ID）
  - 影响范围（affected_artifact）
  - 建议 owner（由人工确认）
- **AI 不得自行设为 `accepted` / `resolved` / `confirmed`；这些状态只能由授权人工设置。**
- 加载 `src/shared/clarify/references/confirmation-signal-technique.md` 识别用户回复是否为真确认（白/灰/黑信号）。
```

---

## 四、B3 阶段收口（每个产物 SKILL 送审前必做）

`governance.md` 第 93 行明确：

> 伴随信号不会自动改变状态：同一项连续 3 次变更提示熔断；开放问题 7 天提示、14 天升级；页面设计或交互规则确认后，上游重审提示进入变更管理。

**B3 阶段收口表的硬规则**：

每个产物 SKILL 送审 `ready_for_human_review` 前，必须更新 `99-review/support/issue-record.md` 的 §13 阶段收口表，对应当前 work item 的一行：
- 问题数（即使是 0 也要落行）
- 收口日期
- 状态（`open` / `closed` / `waived`）

**L0 mini-prd 不要求 issue-record**，但 mini-prd §6 必须包含未决项清单。

---

## 五、与 requirement-restate 的关系

| 触发 | RR 输出 | issue-record 输出 |
|---|---|---|
| 多源说法冲突 | 标 CONFLICT | 路由 ISS-XXX（CLS 类别） |
| 信息缺失 | 标 UNKNOWN → Q-XXX | 路由 ISS-XXX（INF 类别） |
| 待业务决策 | （RR 不决策） | 写 ISS-XXX（DEC 类别），target_close |
| 已识别风险 | （RR 不评估风险） | 写 ISS-XXX（RSK 类别），mitigation |

**RR 是"识别"过程，issue-record 是"登记"过程**——RR 标记 → issue-record 路由 → 业务负责人处置 → 关闭或转 DECISION。

---

## 六、与 confirmation-signal 的关系

当 AI 在 Clarify 阶段向用户提问后，用户的回复按白/灰/黑信号处理：

| 信号 | 类别 | 动作 |
|---|---|---|
| **白名单**（确认 / OK / 可以 / 没问题） | → DECISION | 转 ISS-XXX（DEC）→ 关闭 |
| **灰名单**（看起来不错 / 应该可以 / 嗯） | → 二次询问 | 仍标 UNKNOWN，触发 ISS-XXX（INF） |
| **黑名单**（修改 / 不对 / 等等） | → CONFLICT | 转 ISS-XXX（CLS）→ 路由回上游 work item |

`confirmation-signal-technique.md` 解决"用户答了什么、算不算确认"；`issue-record` 解决"确认后怎么登记"。

---

## 七、与 scope-negotiation 的关系

4 类范围谈判（加 X / must-have / 竞品 / 全 P1）输出：
- "加 X" → ISS-XXX（DEC：交换项 / backlog 项）
- "must-have" → ISS-XXX（DEC：缩小方案 / 缺项清单）
- "竞品" → ISS-XXX（DEC：进本期 / 观察项）
- "全 P1" → ISS-XXX（DEC：强制排序结果）

每次谈判结束，结果必须落到 issue-record 或 feature-list / user-stories，不留在对话里。

---

## 八、错误示例

❌ **默默跳过"待确认"**：业务方说"这个之后再看吧"，AI 继续写 PRD
✅ 登记 ISS-XXX（DEC 或 CLS），等业务方处置

❌ **AI 自行 accepted**：AI 把 RSK 标 accepted
✅ accepted 只能由决策 owner 设，AI 只能登记 `draft` / `open`

❌ **B3 收口表空着**：送审前 issue-record.md §13 没更新
✅ dor_check 会硬阻断，校验器返回 CRITICAL

❌ **问题散落在多个产物里**：每个 skill 自己登记，不集中
✅ 所有问题集中在 `99-review/support/issue-record.md` 一份

❌ **把 issue-record 当需求清单**：把 ISS-XXX 当成"要做的事"
✅ issue-record 是"未决"，不是"要做"——方案交给后续 skill

❌ **长期 open 无 owner**：30 天以上 open 没有 escalation
✅ 7 天提示、14 天升级；30 天必须有 escalation 记录
