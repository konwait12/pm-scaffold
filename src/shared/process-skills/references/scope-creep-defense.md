# 范围蠕变防御（Scope Creep Defense）

> 本文将相关实践转化为本项目的可选方法，不引入外部运行时依赖。
>
> **定位**：stakeholder 提的诉求常常是"原始诉求 + 衍生意图 + 隐性扩展"——AI 经常把衍生意图当原始诉求处理，结果 PRD 越写越大。本技法把三层拆开，逼 stakeholder 区分"必须做"vs"顺手做"vs"以后做"。
>
> **触发**：RR Intake 时遇到以下信号——
> - 业务方说"做 X"但 X 含多个独立子诉求
> - 业务方说"顺便也做 Y"——但 Y 与 X 无逻辑关系
> - 业务方说"以后会用到 Z"——但 Z 当前无明确场景
> - PRD 范围膨胀，超出 STAGE.md / intake-decision 原始范围
>
> **按需加载，不设全局闸门。**

---

## 1. 输入映射

| 外部信号 | pm-scaffold 对应产物 |
|---|---|
| 原始诉求（O） | RR-XXX 的核心重述 |
| 衍生意图（D） | RR-XXX 的衍生标记 + 独立 RR |
| 隐性扩展（E） | scope-negotiation 谈判 → DEC 类或 excluded |

---

## 2. 3 层范围拆解

### 层 1：原始诉求（Original Intent）

**stakeholder 真正想达成什么**——可观察结果 / 业务目标。

例：
- "我想让客户更快下单"（原始诉求 = 提升下单速度）
- "我担心客户流失"（原始诉求 = 减少流失）
- "老板要我们这个季度有亮点"（原始诉求 = 季度亮点功能）

**判定方法**：追问"为什么想要 X" → 剥到不可剥为止。原始诉求通常对应业务目标。

### 层 2：衍生意图（Derived Intent）

**stakeholder 想到的具体方案 / 功能**——可能是多个。

例：
- "想要一键下单"（原始 = 提速；衍生方案 1）
- "想要预填信息"（原始 = 提速；衍生方案 2）
- "想要扫码下单"（原始 = 提速；衍生方案 3）

**判定方法**：列出 stakeholder 提到的所有"X 应该有 / X 应该支持 / X 必须做"，每个都是独立衍生方案。

### 层 3：隐性扩展（Implicit Extension）

**stakeholder 没明说但默认包括的扩展**——常被忽略。

例：
- "做一键下单" + 默认含"已登录用户才看到"（隐性权限）
- "做报表" + 默认含"导出 Excel"（隐性导出）
- "做通知" + 默认含"短信 + 邮件 + 站内信"三通道（隐性多通道）

**判定方法**：追问"X 还有其他要求吗？" / "类似的 Y 之前怎么做？"——挖掘 stakeholder 没明说的扩展。

---

## 3. 范围三态处置

### O 态（Original）：必做

原始诉求必须做——这是 PRD 范围的核心。

**处理**：
- 写到 BG-XXX 的目标章节
- 拆解到 ST-XXX 用户故事
- 关联到 FEA-XXX 功能

### D 态（Derived）：可选

衍生意图可选——做不做、做什么，由业务方决策。

**处理**：
- 每个衍生意图写独立 RR-XXX
- 业务方决策 include / exclude / defer
- 决策结果落到 feature-list 的 In/Out/Deferred/Conditional

### E 态（Implicit）：默认做但要登记

隐性扩展默认做——但要登记到 issue-record，让 stakeholder 知会。

**处理**：
- 标 issue-record（DEC 类，target_close 7 天）
- stakeholder 知会后决策 include / exclude
- 若 7 天无回复 → 升级到 stakeholder 上级

---

## 4. 应对 12 类典型追问

### 追问 1："业务方说'做 X'，X 含 5 个子诉求，怎么拆？"
**答**：拆 5 个 RR-XXX，每条对应一个子诉求。每个追问"为什么想要这个子诉求？"——可能 3 个是衍生意图，1 个是原始诉求，1 个是隐性扩展。

### 追问 2："业务方说'顺便也做 Y'，但 Y 与 X 无关，怎么办？"
**答**：Y 是独立衍生诉求——标 D 态。追问"Y 的原始诉求是什么？"——可能 Y 是另一个真实问题，跑独立 RR 链。

### 追问 3："业务方说'以后会用到 Z'，要不要做？"
**答**：Z 标 `deferred`，不写进本期 PRD。但要追问"什么时候用到？"——若有明确时间窗，标 `conditional`；若模糊，标 `out_of_scope` 进 backlog。

### 追问 4："PRD 写到一半发现范围超出 STAGE.md，怎么办？"
**答**：标 CLS 类，路由 issue-record。让业务方决策：扩大范围（升档 L2 / 新建 REQ）/ 砍回原范围 / 拆需求（部分本期 + 部分 deferred）。

### 追问 5："业务方说'都做完就好了'，但资源只够做 60%，怎么办？"
**答**：用 `scope-negotiation-scripts.md` 脚本二（must-have 谈判）——"必须做完"压到 80% 价值的最小区间，剩下的标 deferred 或 out_of_scope。

### 追问 6："业务方说'这个是标配，所有竞品都有'，怎么办？"
**答**：用 `scope-negotiation-scripts.md` 脚本三（竞品谈判）——找 win/loss 证据 + 客户访谈，确认是否为真实决策驱动。若是，进本期；若否，标观察项。

### 追问 7："业务方说'加上这个功能，研发只多花 1 周'，但评估是 1 个月，怎么办？"
**答**：研发评估是 F 事实（FACT）。业务方评估是 ASSUMPTION（基于猜测）。以研发为准——追问"为什么是 1 周？"让业务方拿出具体证据。

### 追问 8："隐性扩展太多，每个都要 stakeholder 知会，效率低，怎么办？"
**答**：批量登记 issue-record（一次 5-10 个 ISS-XXX），让 stakeholder 一次性决策。stakeholder 不回复 → 14 天升级。

### 追问 9："业务方说'我不管范围，反正上线就好'，怎么办？"
**答**：典型责任规避。让业务方书面签字接受"范围未明确导致的后果"——AI 不替决策。

### 追问 10："PRD 写到 30 个 FEA，怎么砍？"
**答**：用 RICE 评分（参考 `feature-priority-quant.md`）。P0 必做（缺它功能无法运转）；P1 视情况（本期或下期）；P2 砍掉或延后。

### 追问 11："业务方加的需求是'顺手做'，但做完发现它让其他功能变复杂，怎么办？"
**答**：标 DEC 类。问"加之前没想到的复杂度，怎么办？"——业务方决策：保留加（接受复杂度）/ 回退加（接受不完整）/ 重构其他功能（高成本）。

### 追问 12："衍生诉求 D 跟原始诉求 O 矛盾，怎么办？"
**答**：标 CLS 类。让 stakeholder 选——保 O 砍 D，或保 D 改 O，或两者都改（重新跑 RR）。

---

## 5. 与 RR 其他 references 的协作

- **multi-stakeholder-alignment-matrix.md**：不同 stakeholder 对 O/D/E 划分不同
- **time-sensitivity-and-decision-window.md**：D 态可标 deferred + 触发时间窗
- **value-cost-risk-triangle.md**：D 态需三角评估决定 include / exclude
- **scope-negotiation-scripts.md**：4 类谈判脚本处理范围争议
- **fact-ledger.md**：W 诉求型常是 D 态；F 事实型常是 O 态

---

## 6. 错误示例

❌ **把衍生意图当原始诉求**："业务方说做一键下单 → FEA-XXX 一键下单"——原始诉求是提速，衍生是一键下单
✅ 原始诉求 = 提速 → 评估多个方案（一键下单 / 预填 / 扫码） → 让 stakeholder 决策

❌ **隐性扩展没登记**："做通知"默认含"短信 + 邮件 + 站内信"——没问 stakeholder
✅ 显式追问 + 登记 issue-record DEC 类 + 7 天决策窗

❌ **业务方说"以后会用到"就做**："以后会用到 AI 推荐" → 立即做 AI 推荐
✅ 标 deferred + 追问"什么时候用到？"——若无明确时间，进 backlog

❌ **PRD 范围膨胀不警报**：从 8 个 FEA 写到 30 个 FEA，没人 flag
✅ 写到 15+ FEA 时触发 issue-record CLS 类，路由业务方决策

❌ **"都做完"压垮资源**："业务方说都做完，AI 默默接受"
✅ 用 must-have 谈判压到 80% 价值，其余标 deferred/out_of_scope

❌ **隐性扩展默认做不登记**：报表"默认含导出 Excel"——没人说过
✅ 显式追问"还有哪些要求？" + 登记 issue-record

---

## 7. 质量自检清单

- [ ] 每个 stakeholder 诉求都已拆 O/D/E 三层
- [ ] 原始诉求写到 BG-XXX 目标章节
- [ ] 衍生意图每个独立 RR-XXX + 业务方决策
- [ ] 隐性扩展批量登记 issue-record DEC 类 + 7 天决策窗
- [ ] PRD FEA 数控制在 15 以内（超过触发 CLS）
- [ ] 范围争议走 4 类谈判脚本（加 X / must-have / 竞品 / 全 P1）
- [ ] "以后会用到"标 deferred 或 out_of_scope
- [ ] 衍生诉求 D 与原始诉求 O 矛盾标 CLS
- [ ] 隐性扩展默认做必须登记 + stakeholder 知会
- [ ] 业务方"都做完"压到 80% 价值最小区间
