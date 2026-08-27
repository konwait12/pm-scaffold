> superseded_by: `docs/tier-l0-l1-rebuild-plan.md`

> 历史状态：2026-08-20 起不再作为规范；保留用于追溯。失效范围：旧 L0 章节、累计评分、L1 数量与治理结论。

# 计划 v3 自我评判（PRD 章节重设 + Process Tier 工序档位）

> 评审对象：《完整计划 v3：PRD 章节重设 + Process Tier 工序档位 + 阶段分层》
> 评审方式：对照用户硬约束、workflow-registry 依赖图、既有校验器契约、REQ-001 已验证通路逐条自检
> 结论先行：**方向正确，不可直接实施**。存在 1 个违反用户硬约束的方案性错误（F1）、2 个破坏既有校验器的结构错误（F2/F3）、1 个依赖图计算错误（F4）、1 个推翻用户已拍板决策的开放项（F5）。需修订为 v3.1 后再动手。

---

## 1. 五维自评

| 维度 | 评分 | 说明 |
|---|---|---|
| 方向正确性 | 8/10 | 三层正交（阶段/章节/工序档位）与用户指示完全一致；问题清单出 PRD、UX 补齐独立成章均正确 |
| 用户约束符合度 | 6/10 | §4.2 上游产物合并直接违反"图中产物都要有"；开放项表推翻用户对可行性分析的明确选择 |
| 技术可实施性 | 5/10 | L1 产物数与前置依赖图矛盾；验收章删除会同时破坏 3 处机器契约 |
| 风险控制 | 4/10 | REQ-001 已 confirmed 产物兼容性完全未处理；13 步一次性交付无阶段隔离 |
| 完整性 | 6/10 | 方法论调研充分，但关键决策的落位字段多处缺失 |

**综合：不可直接实施，需修订。**

---

## 2. 做对了什么（保留项）

1. **三层正交设计**：阶段分层（已有 001/002/003，零修改）/ PRD 章节分层（文档呈现层）/ Process Tier（工序重量层）三者独立互不冲突——与用户"这个分层和阶段分层互不冲突"指示一致。
2. **项目用 vs PRD 用的区分**：可行性分析→99-review、问题清单→issue-record（默认不进 PRD）、需求重举→支持 skill 不是产物、校验器/收口表/hash 锚→流程用不占章节。这张"不进 PRD"清单是本计划最有价值的部分。
3. **UX 独立成章（§5 原型/UX）**：补上了之前 16 节结构里缺失的独立 UX 承载，与图中"原型/UX"产物对应。
4. **调研深度**：比较了轻量、中量和完整交付的模块结构；“默认按需”的判断被审慎吸收而非照搬，因为本项目有机器追溯链。
5. **AI 推荐 + 用户必选**：符合宪法"AI 不替业务决定"。

---

## 3. 关键缺陷（按严重度排序）

### F1【严重·违反硬约束】上游产物合并方案越权

- **原文**：§4.2 计划把 `validation-rules.md` / `state-machine.md` / `exception-handling.md` 模板"改为业务规则表的子类"。
- **为什么错**：用户硬约束是"**图中产物都要有，加入的其他产物也不影响**"。上游 13 产物是**流程层资产**（各有 artifact_dir / artifact_prefix / 校验器 / REQ-001 已 confirmed 的基线），PRD 章节是**呈现层编排**。合并上游产物会：
  - 违反"图中产物都要有"（图中交互规则、业务规则是独立产物）；
  - 破坏 `workflow-registry.json` 13 工作项注册（artifact_dir/file/prefix 均失配）；
  - 破坏 `traceability_check.py` 的 `STATE-` pattern 检查与 REQUIRED_EDGES；
  - 使 REQ-001 已 confirmed 的 VL-001/STATE-001/EX-001 基线与新模板失配。
- **修正**：**上游 13 产物零修改**。PRD 章节重排只动 `src/templates/stage-3-prd/prd.md` + prd-assembly 的 SKILL.md / output-contract.md / validate_artifact.py。VL/STATE/EX 在 PRD 中作为 §7 业务规则的 7.x 子节**逐字内嵌呈现**（呈现合并、产物独立）——这正是"内嵌不写指针"契约的正确用法。

### F2【严重·破坏校验器】章节映射一产物拆两章

- **原文**：§5 原型/UX ← PD-001 + IX-001，同时 §6 交互规则 ← IX-001。
- **为什么错**：IX-001 被同时映射到两章，装配时违反"逐字内嵌、不写指针"契约（同一上游全文无法在两章各嵌一遍而不产生重复漂移——正是 review-taxonomy 的 [Redundancy]）。
- **修正**：一一对应。§5 原型/UX ← PD-001（页面骨架/信息架构/原型）；§6 交互规则 ← IX-001（操作反馈/5 状态）。

### F3【严重·破坏追溯链】删除"验收依据"独立章

- **原文**：验收依据"并入 §8 PRD 汇总或 §7 业务规则末"。
- **为什么错**：AC 是追溯链的**终点锚**，三处机器契约同时依赖：
  - `prd-assembly/scripts/validate_artifact.py` 的 REQUIRED_HEADINGS 含"验收依据"；
  - `traceability_check.py` 核心链 G→ST→FEA→FUN→AC，`acceptance` pattern 必须命中；
  - RTM 必含 AC 列（列数 ≥6 校验）。
  验收不能因篇幅控制而省略；本项目存在机器追溯链，因此必须保留。
- **修正**：验收依据保留独立章（排在 §7 业务规则之后）。将"验收并入规则末"的判断**撤销**。

### F4【高·依赖图计算错误】L1"5 产物"不可达

- **原文**：L1 Standard = 5 个产物（BG/范围/US/BR/AC）。
- **为什么错**：按 `workflow-registry.json` 前置链：BR 的 predecessors=[functional-flow]，FF 的 predecessors=[feature-list]，FL 的 predecessors=[user-stories]，AC 的 predecessors=[exception-handling, interaction-rules]。按现有注册表走到 AC，前置链几乎要求全 12 项 confirmed。
- **修正**：L1 要真正可行，必须在 registry 为每个 work_item 增加 `tiers` 字段（如 `"tiers": ["L1","L2"]`）并在 pipeline gate 按 tier 过滤 predecessors（tier 豁免）。L1 最小集按依赖图重算：BG→US→FL→FF→BR→AC 至少 **6 项**（若按用户图的最小闭环），且 AC 的 EX/IX 前置需 tier 豁免。这是比原计划承认的**更深的结构性改动**，必须在计划里显式列出。

### F5【高·推翻用户决策】开放项重开已拍板答案

- **原文**：开放项表对"可行性分析"的"客观倾向"写"仅 99-review 不进 PRD"。
- **为什么错**：用户在 AskUserQuestion 中已明确选择"**进 PRD 为按需附录**"。开放项只能留**未决**问题，不能重开已决答案——用户决策优先于 AI 倾向。
- **修正**：可行性分析 = 按需附录 §5.5（已在 §2.2 正确写了"用户选项：可作为按需附录"，但开放项表自相矛盾，需删除该行）。

### F6【高·兼容性缺失】REQ-001 已 confirmed 产物未处理

- **问题**：REQ-001 的 prd.md（16 节旧结构、357KB）已 confirmed 且 hash 绑定。新模板（10 主干+4 按需+2 附录）上线后：
  - `validate_artifact.py` REQUIRED_HEADINGS 变更会让旧产物在新校验器下 FAIL；
  - `branch_validator.py` / `registry_contract_check.py`（模板↔校验器闭环 E3_drift）会报漂移；
  - 已 confirmed 产物按宪法不可变。
- **修正**：新模板配 `schema_version` 升版（7→8）；校验器按 REQ 的 schema_version 分叉（v7 走旧 headings、v8 走新 headings）；REQ-001 冻结在 v7 契约，仅新建 REQ 用 v8。

### F7【中·评分模型缺陷】6 维评分重复计分且无校准

- **问题**：维度 4"异常路径"2 分档含"含合规"，维度 5"合规/资金"又单列——同一信号双计；0-4/5-8/9-12 阈值无任何校准依据。
- **修正**：维度 4 只数异常路径条数（合规信号移出）；维度 5 独占合规/资金/PII。阈值标记为"初始值，首个真实 REQ 落地后校准"，不做硬承诺。

### F8【中·宪法冲突未声明】L0 裁掉治理底线的代价未声明

- **问题**：L0 跳过 hash-anchor / ReviewRecord / audit chain，与宪法"confirmed 产物 hash 绑定、不可篡改、禁止模拟批准"冲突。裁工序可以，但**治理底线**（谁批的、何时批的、批的什么版本）不能没有证据链。
- **修正**：L0 保留**轻量治理**——单签 ReviewRecord + hash 锚（一条记录），裁掉的是工序（preflight/七透镜/taxonomy 扫描/B3 收口表），不是证据链。在 mini-prd SKILL.md 里显式声明这一取舍。

### F9【中·落位缺失】"问题清单进不进 PRD"答复无存储字段

- **问题**：计划说"Intake 时问用户"，但答复存在哪（frontmatter？issue-record？intake-decision.md？）未定义，问完就丢。
- **修正**：REQ frontmatter 增加 `issue_in_prd: false`（默认），prd-assembly Generate 时读该字段决定是否落"附录 C：问题清单"。

### F10【中·图-框架差异未决】"项目范围"是否需要独立产物

- **问题**：图中"项目范围"是独立产物；我们框架里范围基线内嵌在 user-stories（US-001 §范围基线）。计划用"§2 项目范围 ← US-001"带过，没有正面回答图-框架映射差异。
- **修正**：两个选项留用户拍板——(a) US-001 承载（在图-产物映射表显式声明"图中项目范围 = US-001 范围基线章节"，不新建产物，**推荐**：避免范围与故事两处漂移）；(b) 新建独立 scope 产物（图严格对齐，但增加一个工作项 + In/Out 双写风险）。

### F11【中·交付节奏】13 步一次性交付无阶段隔离

- **问题**：PRD 章节重设（模板层、低风险）与 Process Tier（结构层、高风险）混在一个 A→M 序列，任何一步失败都牵连全链。
- **修正**：分两阶段，各自独立回归闸门：
  - **Phase 1（章节重设）**：模板 + prd-assembly 三件套 + schema_version 8 分叉 + 回归 → 单独验证 88/0；
  - **Phase 2（Process Tier）**：registry tiers 字段 + 000-minimal/mini-prd + intake 路由 + pipeline tier-aware → 独立回归。

### F12【低】耗时估计无依据

- 0.5-1pd / 3-5pd / 10-20pd 为拍脑袋数字，且与项目"避免无依据时间预测"的惯例相悖。删除或改为相对量级（轻/中/重）。

---

## 4. 修订后的计划骨架（v3.1 摘要）

```
Phase 1 · PRD 章节重设（模板层，上游产物零修改）
  ├─ P1.1 schema_version 7→8；校验器按 version 分叉（REQ-001 冻结 v7）
  ├─ P1.2 重写 prd.md 模板：10 主干 + 4 按需 + 2 附录
  │     §1 项目背景(←BG) §2 项目范围(←US 范围基线) §3 用户故事(←US)
  │     §4 用户旅程(←UJ) §5 原型/UX(←PD) §6 交互规则(←IX)
  │     §7 业务规则(←BR；7.x 子节逐字内嵌 VL/STATE/EX——呈现合并、产物独立)
  │     §8 验收依据(←AC，保留独立章=追溯链终点锚) §9 PRD 汇总
  │     按需：§5.1 竞品 §5.2 功能流程图(←FF) §5.3 字段规则 §5.4 埋点 §5.5 可行性(用户已拍板)
  │     附录A RTM / 附录B 自审 / 附录C 问题清单(仅 issue_in_prd=true)
  ├─ P1.3 同步 prd-assembly SKILL + output-contract + validate_artifact(HEADINGS)
  └─ P1.4 回归 run_tests_mac.sh → 88/0

Phase 2 · Process Tier（结构层，独立回归）
  ├─ P2.1 registry 每 work_item 加 tiers 字段；pipeline 按 tier 过滤 predecessors（L1 豁免链）
  ├─ P2.2 新建 000-minimal/mini-prd（历史六节草稿 + 轻量治理：单签 ReviewRecord + hash 锚）
  ├─ P2.3 intake-routing：6 维评分(去重计分) + 三档对比 + 用户必选 → frontmatter process_tier
  ├─ P2.4 REQ frontmatter：process_tier / issue_in_prd / schema_version
  └─ P2.5 回归 + mini-prd fixture 单测

台账：E2E-029（章节重设）/ E2E-030（Process Tier）登记
```

---

## 5. 遗留开放项（真正未决，需用户拍板）

| # | 项 | 候选 | 倾向 |
|---|---|---|---|
| 1 | 图中"项目范围"是否新建独立产物 | US-001 承载并显式声明映射 / 新建 scope 产物 | **US-001 承载**（避免 In/Out 双写漂移） |
| 2 | L1 tier 豁免的边界 | 仅豁免 predecessors / 同时豁免 RTM 列 | **仅豁免 predecessors**（RTM 按 L1 产物集缩列） |
| 3 | L0 mini-prd 是否入 audit chain | 轻量治理（单签+hash）/ 完全不入 | **轻量治理**（宪法底线） |
| 4 | 旧 REQ（v7 契约）遇到新校验器 | version 分叉豁免 / 强制迁移 | **version 分叉**（confirmed 不可变） |

---

## 6. 总判定

| 判定项 | 结论 |
|---|---|
| 三层正交架构 | ✅ 保留 |
| "不进 PRD"清单 | ✅ 保留（本计划最有价值部分） |
| §4.2 上游产物合并 | ❌ 撤销（违反"图中产物都要有"） |
| 验收章删除 | ❌ 撤销（追溯链终点锚，3 处机器契约依赖） |
| IX 一产物两章 | ❌ 修正为一一对应 |
| L1 5 产物 | ❌ 重算为 6+ 项 + tier 豁免机制 |
| 可行性分析去向 | ✅ 按需附录 §5.5（遵用户已拍板答案） |
| 一次性 A→M | ❌ 拆 Phase 1/2 独立回归 |

**结论：v3 是一份方向正确但工程细节多处失守的计划。按 v3.1 修订（上游零修改 + 验收保留 + 两阶段交付 + v7/v8 分叉）后方可实施。**
