---
name: prd-assembly
description: Assemble confirmed business facts into a concise, traceable, reader-facing PRD without introducing requirements or copying workflow governance into the deliverable.
---

# PRD 汇总（PRD Assembly）

## 目的与边界

产出唯一的最终 `prd.md`：面向业务、产品、设计与研发协作的可读需求规格，不是上游工件档案或审计报告。

Assembly 只做三件事：

1. 从本档位已确认上游选择业务事实；
2. 按读者需要重排、去重，保留稳定 Trace ID；
3. 将来源、选择器、哈希、追溯和审查证据写入项目侧载体。

禁止发明需求、静默解决矛盾、替业务确认阈值，或以全文复制逃避取舍。缺少必要事实时停止并回流到最早受影响的 work item。

## 输入与输出

- L0：一个 confirmed `mini-prd`，六类事实确定性投影到最终 PRD。
- L1：7 个 confirmed 上游：背景、旅程、故事、功能、流程、业务规则、验收。
- L2：L1 上游加页面、交互、校验、状态、异常，共 12 个。
- 适用性判断来自持久化 `00-input/intake-decision.md`；不能在装配时猜测。
- 输出：精简 `prd.md` + `prd-assembly-manifest.json`。追溯、审查、问题收口、ReviewRecord、hash anchor 和 audit event 进入 `99-review/` 与 `.audit/`。

## 三档生成规则

### L0

保留变更、目标、范围、行为、边界、依赖和验收。页面、交互、字段校验、持久状态、异常等没有事实时不生成伪规则，也不附加 mini-prd 全文。

### L1

保留 7 个上游的产品事实。页面、交互、字段校验、状态和异常仅在 intake 有明确适用事实时生成；实际适用时应升级 L2，不把 L2-only 规则藏入业务规则。

### L2

保留完整页面、交互、业务规则、校验、状态、异常和验收，但按章节职责整合；禁止将 12 份上游全文连续复制，禁止同一规则在摘要、全文和追溯表重复出现。

## 最终 PRD 允许的内容

1. 项目背景
2. 项目范围
3. 用户与用户旅程
4. 用户故事与优先级
5. 功能清单
6. 功能流程
7. 页面与体验（实际适用时）
8. 交互规则（实际适用时）
9. 业务规则、校验、状态与异常（按适用性生成）
10. 验收标准
11. 依赖与待决业务问题（仅存在真实 Q-/UNK-/ISS-/DEC- 时）

业务声明保留既有 Trace ID 和知识状态；完整来源索引、选择器和哈希放在 manifest。

## 不得进入 `prd.md`

Agent instruction、预检成熟度、质量增强记录、Clarifications、全量事实/决定/未知登记册、Constitution Compliance、自审记录、Human Gate、ReviewRecord、B3 收口、评审 taxonomy、hash anchor、source hash、manifest 细节、正反向追溯报告、完整 RTM、问题清单全文、下游交接过程、版本摘要、任意 source block 或上游原文镜像。

## 聚合不变式

1. 只选择已确认上游事实；选择不到必需事实就阻断并回流，不补写。
2. 不用 `详见 XX` 替代必要产品内容，也不全文复制上游。
3. 同一事实只在最合适正文位置出现：流程讲顺序，规则讲约束，验收讲判定。
4. `required`、`conditional`、`not_applicable` 来自 intake；`not_applicable` 有事实依据和来源，`conditional` 有触发条件、当前判断和复审点。
5. 无已确认内容时不生成空的按需章节、空表、泛化 N/A 或 `待确认` 占位。
6. 不新增业务事实、不静默解决冲突、不改写已确认语义。

## 机器证据

manifest v2 记录每个本档来源的 `work_item`、`artifact_id`、安全相对路径、confirmed 状态、源文件哈希、`target_sections` 和 `selectors`，不包含 source body。`traceability_check.py`、`branch_validator.py`、审查 taxonomy 和人工评审继续读取项目侧记录。

## Human Gate / Reflow

已 confirmed 的 PRD 不直接修改。模板或投影规则变化通过 reflow 生成新 draft，机器闸门通过后由授权人工 `pipeline.py review --decision approve` 确认；旧版本保留为历史/`superseded`。v7 存量产物保持只读兼容，新 v8 使用本契约。

## 完成标准

正文可独立阅读、无治理泄漏、无完整上游复制、无指针代替实质内容；范围、行为、规则、失败边界、验收和 Trace ID 完整；manifest/hash/审查证据可重建；授权人工明确批准。

## 参考资料

| 文件 | 用途 | 触发时机 |
|---|---|---|
| `references/output-contract.md` | reader-facing 最终 PRD 契约：三档边界、章节职责、manifest v2 要求 | 装配与校验时（强制） |
| `references/source-handling.md` | 上游正文与过程治理内容的边界：禁止 source body 全文镜像 | 装配时（强制） |
| `references/prd-structure-reference.md` | v8 章节结构与适用性元数据定义 | 装配时（强制） |
| `references/prd-scoring-rubric.md` | 评审评分与 R&D-review-v1 硬标准（advisory） | 人工评审时 |
| `references/ddd-design-guide.md` | DDD 设计 7 阶段交接提示（事件风暴→行为建模，含贫血模型检查，advisory） | 研发开始 DDD 设计时（按需） |
| `references/prototype-embedding.md` | 原型/UX 内容嵌入边界 | L2 页面/体验章节装配时 |
| `references/incre-prd-checklist.md` | 增量 PRD 协作检查清单 | 增量迭代时 |
| `references/anti-patterns.md` | 装配反模式清单 | 自检时 |
| `references/audit-checklist.md` | 装配审计检查清单 | 审计时 |
| `references/reviewer-checklist.md` | 人工评审检查清单 | 人工评审时 |
| `references/downstream-handoff.md` | 下游交接说明（仅评审载体，不进入 PRD 正文） | 交接时 |
| `references/structure-9q.md` / `references/question-patterns.md` / `references/grill-me.md` / `references/iteration-pattern.md` / `references/domain-mapping-hint.md` / `references/adr-and-sourcing.md` / `references/competitor-three-state.md` / `references/review-engine-5step.md` / `references/thinking-framework.md` | 需求澄清、结构追问与评审方法论（advisory） | 澄清/评审时 |
| `src/shared/audit/red-team-naysayer.md` | 红队质疑清单（10 铁律、三阶段、只提问、advisory，永不改状态） | 装配与评审自检时 |
