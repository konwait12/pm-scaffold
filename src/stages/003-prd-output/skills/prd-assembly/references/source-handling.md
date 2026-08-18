# 来源处理 · prd-assembly

本 Skill 很特殊：它消费**全部 12 个已确认的上游产物**，产出的新内容为零——只有聚合、核验与报告。

## 主来源（Primary Sources，全部 12 个）

PRD 汇总步骤要求全部 12 个上游产物 `status: confirmed`：

| 产物 | ID 前缀 | 提供 |
|---|---|---|
| background-goal.md | BG-XXX | §1 项目背景与目标（目标、约束、角色、未知） |
| user-journey.md | UJ-XXX | §2 用户旅程（旅程图、路径覆盖） |
| user-stories.md | US-XXX | §3 用户故事与范围基线（故事卡 ST-XXX） |
| feature-list.md | FEA-XXX | §4 功能清单（P0/P1/P2） |
| functional-flow.md | FL-XXX | §5 功能流程（主流程/分支/异常、跨系统交接点） |
| page-design.md | PD-XXX | §6 页面设计（页面骨架、字段） |
| interaction-rules.md | IX-XXX | §7 交互规则 |
| business-rules.md | BR-XXX | §8 业务规则 |
| validation-rules.md | VL-XXX | §9 校验规则 |
| state-machine.md | SM-XXX | §10 状态变化 |
| exception-handling.md | EX-XXX | §11 异常与失败处理 |
| acceptance-criteria.md | AC-XXX | §12 验收依据 |

## 聚合规则（Aggregation Rules）

1. **复制，不改写（Copy, don't rewrite）**：来自上游产物的内容必须 verbatim 复现。不概括、不"润色措辞"、不重构。
2. **保留全部 ID**：每个 SRC-*、BG-*、UJ-*、US-*、ST-*、FEA-*、FL-*、PD-*、IX-*、BR-*、VL-*、SM-*、EX-*、AC-*、G-X 都必须与来源完全一致地出现在 PRD 中。
3. **章节映射**：按上表「提供」列一一对应，不要跨章节重排内容。
4. **条件章节**（§5 按需：字段规则、埋点需求、依赖、未决项）：仅当上游相关产物有非空内容时才纳入。否则注明「本期不适用」。

## 不要做什么（What NOT to Do）

- **不要引入新需求**。如果你认为有缺失，在 §9 不一致报告中记录。
- **不要解决不一致**。记录它们，让人类决定。
- **不要修改已确认文本**。即使你发现错别字——记录下来，不要修。
- **不要添加内容来填补缺口**。空的 RTM 单元格好于一条编造的追溯链接。
- **不要生成新的 QuestionRecord 问题**。按 `01-三阶段主流程与工作事项.md` §6.1，PRD 阶段不独立产出新的 QuestionRecord。已存在的未决项作为"待澄清事实"进入 §5.4 未决问题与风险。

## 追溯核验（Traceability Verification）

RTM（§6）、正向追溯检查（§7）与反向追溯检查（§8）通过以下方式构建：

1. 解析全部 12 个上游产物中的稳定 ID（G-X、ST-XXX、FEA-XXX、FL-XXX、AC-XXX、BR-XXX）。
2. 跟随每个产物中的显式引用（例如 `feature-list` 功能清单说"来源故事：ST-001、ST-002"）。
3. 机械地构建矩阵——无推断、无猜测。

## 不一致报告（Inconsistency Reporting）

发现缺口或矛盾时，§9 报告必须包含：
- **类型（Type）**：broken_link / orphan / contradiction / priority_downgrade / missing_nfr / other
- **元素（Elements）**：涉及哪些 ID，在哪些产物中
- **描述（Description）**：具体问题是什么
- **建议解决方案（Suggested resolution）**：AI 的建议（供人工决策，不是自主行动）
- **严重度（Severity）**：CRITICAL（阻断 PRD 确认）/ HIGH（应修复）/ MEDIUM（记录并接受）/ LOW（外观性）

## 冲突处理（Conflict Handling）

PRD 汇总步骤不得覆盖任何已确认的上游内容。如果两个产物不一致：
1. 在 §9 中记录双方版本。
2. 把矛盾标记为 CRITICAL 或 HIGH 严重度。
3. 人工评审人决定哪个版本生效，以及是否触发上游 reflow。
