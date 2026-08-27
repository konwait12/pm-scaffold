# 输出契约 · prd-assembly

## 状态机

`draft → needs_user_input → conditional_review → ready_for_human_review → confirmed → superseded`。

## 最终 PRD 的交付边界

`prd.md` 是面向业务、产品、设计与研发协作的需求规格，不是工作流审计包。它必须能独立说明：为什么做、做什么、不做什么、谁受影响、如何行为、何时失败、如何验收；它不得重新复制整个需求工作流。

正文保留：

1. 项目背景（问题、目标、约束、成功标准、立项依据 = 可行性分析摘要）
2. 项目范围（In / Out / Deferred / Conditional、业务假设和依赖）— **唯一上游：`project-scope`**
3. 用户与用户旅程
4. 用户故事与优先级
5. 功能清单
6. 功能流程
7. 页面与体验（实际适用时）
8. 交互规则（实际适用时）
9. 业务规则、字段清单、字段校验、状态与异常（各子节按实际适用性生成）
   - §9.1 计算与流程规则（来源：BR）
   - §9.2 字段清单（名称 / 类型 / 长度 / 必填 / 默认值 / 唯一性 / 来源）— **唯一上游：`field-rules`（L2 only）**
   - §9.3 字段校验（来源：VL；VL-XXX 行指向 `field-rules` 的 F-XXX）
   - §9.4 状态变化（来源：STATE）
   - §9.5 异常处理（来源：EX）
10. 验收标准
11. 依赖与待决业务问题（仅存在真实 Q-/UNK-/ISS-/DEC- 时）

正文中的业务声明必须保留其已有的 Trace ID 与知识状态标签。完整来源索引、选择器、文件哈希与内容哈希存入 `prd-assembly-manifest.json`；追溯报告、审查发现、问题收口、ReviewRecord、hash anchor 和 audit event 存入 `99-review/` 与 `.audit/`。

## 三档内容边界

| 档位 | 正文来源与深度 | 不得生成的内容 |
|---|---|---|
| L0 | 一个 confirmed mini-prd 的六类事实确定性投影；正文只保留变更、目标、范围、行为、边界、依赖和验收。 | 伪造页面、交互、字段校验、状态模型或上游链路；重复 mini-prd 全文。 |
| L1 | 9 个确认上游：可行性分析（FA）、背景（BG）、项目范围（SCOPE）、旅程（UJ）、故事（US）、功能（FE）、流程（FF）、业务规则（BR）、验收（AC）。页面、交互、字段、校验、状态、异常仅在 intake 有明确适用事实时出现。 | 用”本期不适用”大段正文替代产品内容；将 L2-only 规则或状态模型藏入业务规则。 |
| L2 | 15 个确认上游按章节职责整合：FA + BG + SCOPE + UJ + US + FE + FF + PD + IX + BR + FIELDS + VL + STATE + EX + AC。保留完整页面、交互、规则、字段、校验、状态、异常与验收。 | 15 份上游全文连续拼接；同一规则在摘要、全文和追溯表三次出现。 |

## 明确不在 `prd.md` 的内容

- Agent instruction、预检成熟度、产品质量增强记录、Clarifications 会话；
- FACT/DECISION/ASSUMPTION/UNKNOWN/CONFLICT 的全量登记册与 Constitution Compliance 自审表；
- Human Gate、ReviewRecord、B3 收口、评审 taxonomy、hash anchor、source hash、manifest 细节；
- 正向/反向追溯报告、完整 RTM、问题清单全文、下游交接过程、生成版本摘要；
- 任意上游产物的完整 source block 或原文镜像。

这些材料仍是项目治理事实，但属于项目侧证据，不是读者版 PRD 章节。

## 聚合规则

1. **确定性选择，不发明**：只选择已确认上游中的业务正文、规则、表格、流程、状态、异常和验收条目。源段落选择记录在 manifest；找不到必需事实就阻断并回流，不补写。
2. **按职责去重**：同一事实只在最合适的正文位置出现。流程章描述顺序，规则章描述约束，验收章描述判定条件。
3. **禁止两种极端**：禁止“详见 XX”替代正文，也禁止全文复制上游以规避总结取舍。
4. **适用性是输入，不是装配猜测**：`required`、`conditional`、`not_applicable` 必须来自持久化 intake 决策或确认上游。`not_applicable` 至少记录事实依据与来源；`conditional` 还需触发条件、当前判断和复审触发点。
5. **按需章节零占位**：没有已确认内容时不生成第 11 章或其子节；不得输出空表、`待确认` 伪内容或泛化 N/A。
6. **保留 ID，不保留冗余**：保留 G/ST/FEA/FUN/PD/IX/BR/VL/STATE/EX/AC 等业务 Trace ID；不要求将审计矩阵复制到正文。

## manifest 契约

v8 真实 REQ 的 `003-prd-output/prd-assembly-manifest.json` 必须包含：

- `schema_version: 2`、`process_tier`；
- 每个本档确认上游的 `work_item`、`artifact_id`、`path`、`status: confirmed`、`content_sha256`；
- 非空 `target_sections` 与 `selectors`，用于说明该来源被投影到哪些 PRD 章节；
- 不包含 source body，且不要求 `prd.md` 含 source block。

**`content_sha256` 算法（B3 明示）**：必须使用与校验器一致的**规范化哈希** `artifact_content_hash`（见 `src/scripts/workflow_registry.py`），而非原始文件的裸 SHA-256。规范化规则：将每行 `^(status|reviewer|reviewed_at|confirmed_at): ...` 替换为 `\1: <review-metadata>` 后，对规范化文本计算 SHA-256。示例（伪代码）：

```text
canonical = re.sub(r"(?m)^(status|reviewer|reviewed_at|confirmed_at):.*$",
                   r"\1: <review-metadata>", source_text)
content_sha256 = sha256(canonical.encode("utf-8")).hexdigest()
```

用原始 `shasum -a 256` 计算会与校验器不匹配，导致 `Assembly manifest failed: ... content_sha256 does not match source file`。

manifest 验证来源身份、路径边界、状态、哈希和档位；它不授权 assembly 创造业务内容。

## 兼容策略

- 缺少 `prd_structure_version: 8` 的 v7 存量 PRD 继续走旧 validator 契约，保持只读兼容。
- 新 v8 PRD 采用本契约；不要求 RTM、自审记录、source block 或 §11 空壳。
- 已 confirmed 的 PRD 不直接修改。模板/投影规则变化需通过 reflow 生成新 draft，人工批准后才成为新确认版本。
