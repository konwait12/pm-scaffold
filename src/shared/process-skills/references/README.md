# Process Skills References · 应对追问的能力 references

> 本目录收纳过程型能力（RR / brainstorming / issue-record / shared/clarify）的核心 references，按"用户/AI 的典型追问"维度组织——目的是让任何产物 SKILL 在面对追问时能直接加载对应的 reference 应对。

---

## 一、references 矩阵

| Reference | 应对的追问类型 | 强制程度 | 加载时机 |
|---|---|---|---|
| `fact-ledger.md` | "这条信息是 F 事实 / D 决议 / A 假设 / W 诉求 / O 意见哪一型？" | **必读** | 多源素材 / 冲突仲裁 / 任何标 `FACT` 的主张 |
| `gap-checklist-14d.md` | "PRD 有没有结构性遗漏（合规 / 数据迁移 / 灰度 / 度量）？" | **必读** | Intake 后 / Generate 前 / Audit 前 |
| `interview-synthesis.md` | "大量访谈原话怎么提炼成结构化需求？" | **必读** | 大量口语化原话 / 聊天记录 / 会议纪要 |
| `confirmation-signal-technique.md` | "用户说'差不多就行'，算不算真确认？" | **必读** | Clarify 阶段识别用户回复 |
| `multi-stakeholder-alignment-matrix.md` | "A stakeholder 说 X，B stakeholder 说 X'，到底是 X 还是 X'？" | 按需 | ≥2 stakeholder 描述同一事 |
| `assumption-stress-test.md` | "这个假设显然对吧，还需要验证吗？" | 按需 | ASSUMPTION 类主张 ≥3 条 |
| `time-sensitivity-and-decision-window.md` | "业务方说'尽快'，到底多快？" | 按需 | 强时间窗诉求 / 决策时限 |
| `value-cost-risk-triangle.md` | "业务方说 X 价值很大，成本呢？" | 按需 | 优先级定级 / 范围扩张 |
| `latent-pain-signal.md` | "stakeholder 说'想要 X'，但 X 不像痛点，怎么办？" | 按需 | O 意见型多 / stakeholder 沉默 |
| `decision-reversibility.md` | "这事不可逆，老板说'赶紧做'，怎么办？" | 按需 | 含合规/资金/PII/法律告知/数据迁移 |
| `scope-creep-defense.md` | "业务方说'顺便也做 Y'，怎么办？" | 按需 | PRD 范围膨胀 / 衍生诉求多 |

---

## 二、追问应对 12 类总表

每个 reference 都内置了 12 类典型追问 + 应对话术（见各文件 §4）。汇总：

| 追问类型 | 主应对 reference | 辅 reference |
|---|---|---|
| "W 诉求型当事实" | fact-ledger.md | — |
| "多 stakeholder 说法不一" | multi-stakeholder-alignment-matrix.md | fact-ledger / confirmation-signal |
| "假设太显然还需要验证吗" | assumption-stress-test.md | — |
| "时间窗模糊" | time-sensitivity-and-decision-window.md | decision-reversibility |
| "高价值低成本零风险（不存在）" | value-cost-risk-triangle.md | — |
| "stakeholder 沉默 / 情绪 / 迂回" | latent-pain-signal.md | confirmation-signal |
| "不可逆决策被时间压" | decision-reversibility.md | time-sensitivity |
| "范围膨胀" | scope-creep-defense.md | scope-negotiation-scripts |
| "结构性遗漏" | gap-checklist-14d.md | — |
| "访谈口语化" | interview-synthesis.md | fact-ledger |
| "用户确认算不算数" | confirmation-signal-technique.md | — |
| "老板 vs 业务方互推责任" | multi-stakeholder-alignment-matrix.md | issue-record |

---

## 三、使用流程

```
遇到追问 / 信号
  ↓
查 §二 总表，找到主应对 reference
  ↓
读 reference 的 §3 应对 12 类典型追问
  ↓
按话术处理；若标 CLS / DEC / INF 类，路由 issue-record
  ↓
登记到 RR-XXX 或 issue-record.md
```

---

## 四、为什么这 11 个 references 是必备的

之前 RR 只有 5 个 references（fact-ledger / gap-checklist-14d / interview-synthesis / question-patterns / confirmation-signal）。本目录新增 6 个：
- multi-stakeholder-alignment-matrix（多 stakeholder 冲突）
- assumption-stress-test（假设可证伪）
- time-sensitivity-and-decision-window（时间窗）
- value-cost-risk-triangle（价值 / 成本 / 风险三角）
- latent-pain-signal（隐性痛点）
- decision-reversibility（决策可逆性）
- scope-creep-defense（范围蠕变防御）

理由：你的追问"需求重举是不是太敷衍、考虑够不够多、能不能应付用户追问"——这 11 个 references 就是应对追问的完整装备。
