# 来源处理 · prd-assembly

## 输入范围

PRD assembly 只消费持久化档位允许且状态为 `confirmed` 的上游：

| 档位 | 上游 work item |
|---|---|
| L0 | mini-prd |
| L1 | project-background-goal、user-journey、user-stories、feature-list、functional-flow、business-rules、acceptance-criteria |
| L2 | L1 的 7 项，加 page-design、interaction-rules、validation-rules、state-machine、exception-handling |

## 选择与落位

来源不是“全文复制许可证”。装配器必须为每个来源记录：来源 artifact、哈希、选取器以及落入的目标章节；只选取下列可交付信息：

- 背景、目标、范围、角色、用户价值；
- 功能、流程、关键分支、跨系统交接；
- 页面、交互、业务规则、字段校验、状态、异常与恢复；
- 验收标准、真实业务依赖与待决问题。

以下内容不得进入最终 PRD：frontmatter、技能说明、预检、质量增强记录、全量事实/决定/未知登记、Clarifications、来源追溯表、Constitution Compliance、版本摘要、审计报告、ReviewRecord、hash anchor、source block。

## 不变式

1. 不新增业务事实、不静默解决冲突、不替业务确认阈值或取舍。
2. 不使用 `详见 XX` 取代必要产品内容。
3. 不将同一来源全文、摘要和追溯表重复塞进正文。
4. 每个正文业务条目保留已有 Trace ID；无 Trace ID 的事实保留来源 artifact ID。
5. 任何来源缺失、未确认、越档或哈希漂移都阻断装配。
6. 选择器无法找到原始事实时，路由回最早受影响 work item；不得由 assembly 编写“合理摘要”。

## 追溯与审查

完整 G→ST→FEA→FUN→AC 及横向 BR/VL/STATE/EX/PD/IX 关系由 `traceability_check.py` 从项目侧来源和 manifest 生成。正向/反向报告、审查 taxonomy、问题清单、证据质量检查与人工评审记录进入 `99-review/`；它们可以随 Human Gate 展示，但不属于 `prd.md` 的正文。
