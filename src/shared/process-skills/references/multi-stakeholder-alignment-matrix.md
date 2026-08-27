# 多 Stakeholder 对齐矩阵（Multi-Stakeholder Alignment Matrix）

> 本文将相关实践转化为本项目的可选方法，不引入外部运行时依赖。
>
> **定位**：当 ≥2 stakeholder 描述同一事、但措辞/角度/优先级不一致时，本技法把"看似同一诉求"拆解成"对每类 stakeholder 的具体含义"，避免 AI 把"业务方说的 X"和"运营说的 X"混为同一条 RR-XXX。
>
> **触发**：Clarify 阶段出现以下信号——
> - 同一事实在 ≥2 stakeholder 描述中有措辞差异
> - 不同 stakeholder 给出的优先级冲突
> - 同一功能的成功判据在不同 stakeholder 间不一致
>
> **按需加载，不设全局闸门。**

---

## 1. 输入映射

| 外部信号 | pm-scaffold 对应产物 |
|---|---|
| ≥2 stakeholder 描述同一事 | RR-XXX 中多条重述行，每条链接到不同 SRC-* |
| 不同 stakeholder 的优先级冲突 | issue-record 的 DEC 类（待业务决策） |
| 成功判据不一致 | RR §4 stakeholder 自查反馈位 |

---

## 2. 对齐矩阵模板

对每个"看似一致"的诉求，构造 4 维矩阵：

| Stakeholder | 角色 / 利益点 | 原话 verbatim | 隐含假设 | 优先级 | 成功判据 |
|---|---|---|---|---|---|
| SH-001 业务负责人 | 业务增长 / 营收 | "我们要 X" | 假设 Y | P0 | K1 |
| SH-002 运营 | 客户满意度 / 流程效率 | "我觉得是 X" | 假设 Z | P1 | K2 |
| SH-003 客户 | 体验 / 价值 | "我想要 X" | 假设 W | P0 | K3 |
| SH-004 研发 | 技术可行性 / 维护成本 | "实现 X 用 A 方案" | 假设 V | P2 | — |

**关键判定**：
- 原话 verbatim 不同 → 不能合并为同一条 RR-XXX，必须每 stakeholder 一条
- 隐含假设冲突 → CONFLICT，路由 issue-record（CLS 类）
- 优先级不一致 → DEC 类，待业务负责人拍板
- 成功判据不可比 → 在 RR §4 stakeholder 自查反馈位记录差异，让 stakeholder 互相对齐

---

## 3. 应对 12 类典型追问

### 追问 1："业务方说要做 X，运营说要做 Y，到底做哪个？"
**答**：先确认 X 和 Y 是否同一诉求——若业务方的 X 是营收增长，运营的 Y 是流程效率，可能是同一目标的不同侧面。运行对齐矩阵：把"X"和"Y"还原成"为达成什么可观察结果"。若还原后是同一结果，则合并；若不同，则作为两个独立 RR-XXX。

### 追问 2："两个 stakeholder 都说 P0，但资源只够做 1 个，怎么选？"
**答**：用 RICE / MoSCoW 跑量化评分（参考 `feature-priority-quant.md`）。但量化只是沟通工具，最终决策权在业务负责人。

### 追问 3："客户说想要 X，但付费意愿显示他们实际想要 Y，咋办？"
**答**：标 W 诉求型（客户原话） + 标 AI_INFERENCE 推断（付费数据反推）。两者分别登记到 RR-XXX，让业务负责人裁决"按客户说的"还是"按数据说的"。

### 追问 4："研发说技术上做不到 X，业务方坚持要 X，怎么办？"
**答**：标 CLS 类冲突。研发评估的不是"做不到 X"，而是"用当前方案做不到 X"——追问"换个方案呢？"或"换个范围呢？"（参考 `feasibility-analysis`）。

### 追问 5："A stakeholder 沉默 / 没回复，怎么处理？"
**答**：标 INF 类（信息缺口）。A 的沉默可能是有意放弃、无暇顾及、或等待别人先表态——不假设。ISS-XXX target_close 设 7 天；7 天后未回复升级到 A 的上级。

### 追问 6："A stakeholder 一直改口，前天说 X，今天说 X'，怎么办？"
**答**：标 UNKNOWN → Q-XXX 提问 "昨天 X，今天 X'，哪个为准？"——把变更写进 issue-record 的 ChangeRecord。不静默接受最新版本。

### 追问 7："stakeholder 私下跟我说了 X，但没在群里说，要不要记？"
**答**：记——但标 "私人渠道"，来源标 `[私下交流]` 而不是 SRC-*。在 RR §4 stakeholder 自查反馈位记录，并请 stakeholder 在正式渠道确认。

### 追问 8："A stakeholder 跟 B stakeholder 直接对着干，怎么处理？"
**答**：标 CLS 类。AI 不调停——把两方原话 verbatim 写进 RR-XXX，路由给业务负责人或更高层裁决。

### 追问 9："业务方说'这个很简单，应该 1 周能上线'，但实际复杂，怎么办？"
**答**：标 ASSUMPTION（业务方假设）。追问"为什么是 1 周？基于什么？"——若基于历史经验，记为来源；若基于猜测，标 AI_INFERENCE。在 RR §时间窗/截止时间 章节记录。

### 追问 10："客户说'我想要 X'，但 X 在我们产品里已经有 80% 类似功能，怎么避免重复造轮子？"
**答**：标 "W 诉求型但事实已部分覆盖"。先看现有功能是否能满足；若能，跳过新建并标 "已在 X 中覆盖"；若不能，拆出"差什么"的子诉求。

### 追问 11："多个 stakeholder 都同意做 X，但其中 1 个沉默 3 天，怎么办？"
**答**：默认 沉默=不反对（社区惯例），但需在 RR §4 记录"X 在 2026-08-XX 通知 SH-NNN，未收到异议"——留审计痕迹。

### 追问 12："stakeholder 说'你看着办'，怎么办？"
**答**：这是灰名单信号（`confirmation-signal-technique.md`）。AI 不替业务方决策。追问 1-2 个具体选项：A 方案 vs B 方案 + 影响对比。让 stakeholder 二选一。

---

## 4. 与 RR 其他 references 的协作

- **fact-ledger.md**：W 诉求型 vs F 事实型——区分 stakeholder 真在讲事实还是在讲诉求
- **gap-checklist-14d.md**：stakeholder 角色覆盖度——是否漏了某类 stakeholder（合规/法务/数据 owner）
- **confirmation-signal-technique.md**：灰名单触发二次询问
- **scope-negotiation-scripts.md**：4 类范围谈判脚本
- **decision-reversibility.md**：评估 stakeholder 决策的可逆性

---

## 5. 错误示例

❌ **把"业务方说 X"和"客户说 X"合并为同一条 RR-XXX**：表面同，实则不同 stakeholder 隐含假设/优先级/成功判据都不同
✅ 拆为两条 RR-XXX，分别链接不同 stakeholder 的原话

❌ **AI 替 stakeholder 裁决优先级冲突**：当业务方说 P0，运营说 P1，AI 选 P0
✅ 标 DEC 类冲突，等业务负责人或更高层裁决

❌ **沉默 stakeholder 默认同意**：没人回话=全员通过
✅ 沉默 7 天以上升级；私底下没人同意≠正式同意；需要 explicit confirmation

❌ **把私下口头承诺当成正式决策**："昨天吃饭时客户口头答应了"
✅ 私下口头承诺标 ASSUMPTION 或 UNKNOWN，要求 stakeholder 在正式渠道（邮件/工单）确认

---

## 6. 质量自检清单

- [ ] 每个 ≥2 stakeholder 描述同一事的诉求都已构造对齐矩阵
- [ ] 矩阵中 4 维（原话/隐含假设/优先级/成功判据）每条都有值
- [ ] 原话 verbatim 保留，未做改写
- [ ] 优先级冲突 / 成功判据冲突都标 CLS / DEC 路由 issue-record
- [ ] 沉默 stakeholder 标 INF + target_close
- [ ] 改口 / 变更都进 ChangeRecord
- [ ] 私下口头承诺未当作正式决策
