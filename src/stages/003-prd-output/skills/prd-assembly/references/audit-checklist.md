# 审计清单 · prd-assembly

## 1. 结构闸门（Structural Gate）
- [ ] 12 required sections present (§0–§12)
- [ ] Frontmatter complete (10 fields + upstream_artifact_ids)
- [ ] §0 lists all 12 upstream artifacts with status=confirmed

## 2. 聚合闸门（Aggregation Gate）
- [ ] §1-§4 content matches upstream verbatim (no rewriting)
- [ ] All artifact and trace IDs preserved; new prose follows `id-contract.md` (`G-*` / `FUN-*` / `STATE-*`), confirmed historical IDs remain unchanged
- [ ] No new requirements introduced

## 3. 追溯闸门（Traceability Gate）
- [ ] §6 RTM covers all P0 G→ST→FEA→FUN→AC core chains; applicable BR/VL/STATE/EX evidence is linked without forcing a false linear chain
- [ ] §7 forward trace: no broken P0 links
- [ ] §8 backward trace: no orphan elements
- [ ] §9 inconsistency report generated (may be empty)

## 4. 边界闸门（Boundary Gate）
- [ ] §5.4 only aggregates upstream UNKNOWN items
- [ ] No new QuestionRecord issues generated (PRD stage exception)
- [ ] No content modified from upstream confirmed versions

## 5. 沟通闸门（Communication Gate）
- [ ] Can a new developer understand what to build?
- [ ] Can a tester write test cases from this PRD?
- [ ] Can a business stakeholder confirm "yes, this is what we asked for"?
- [ ] Are there sections that read like AI internal notes?

## 6. to B 审计项（advisory，吸收自 prd-review-design 双重逻辑校验）

### 6.1 逻辑准确性审查
- [ ] 需求目标与需求背景匹配性（目标解决背景所述问题）
- [ ] 业务逻辑合理性（排查矛盾点，无自相矛盾）
- [ ] 量化指标可行性（数值可达成，非凭空设定）
- [ ] 商业化逻辑合规性（付费提示清晰、无虚假宣传）

### 6.2 逻辑闭环审查
- [ ] 需求输入-处理-输出闭环（每功能有输入源→处理逻辑→输出产物）
- [ ] 异常场景闭环（付费失败 / 操作失误 / 权限不足 / 余额不足 / 超时均有恢复路径，追溯 EX-XXX）
- [ ] 商业化链路闭环（引流→转化→留存→复购无断裂，标 [CommercializationGap] 若断裂）

### 6.3 商业化合规四检查
- [ ] 付费流程合规（付费提示清晰、无虚假宣传、退款/对账路径完整）
- [ ] 数据收集合规（用户隐私保护、数据出境合规、授权链完整）
- [ ] 商业化链路完整性（引流-转化-留存-复购无断裂）
- [ ] 异常场景覆盖（付费失败、余额不足、权限不足等）

### 6.4 to B 结构性检查
- [ ] RBAC 权限矩阵（功能权限 + 数据权限双表）覆盖相关 FEA-XXX 与角色差异
- [ ] 状态生命周期（STATE-XXX）与字段状态枚举一致，无 CONFLICT
- [ ] to B 风险含权限 / 审计 / 数据出境披露
- [ ] 业务对象状态机有起止 [*] 与异常恢复路径

## 7. 新批次审计项（2026-08 第二轮吸收，advisory）

### 7.1 grill 对抗自检（来源 product-spec-generator）
- [ ] section-grill 四阶段跑完：静默重读 → 负载分级（🔴🟡🟢 风险挖掘）→ 逐项 grill → 判定 PASS / 待澄清 / 冲突
- [ ] 结构三维（结构完整性/一致性/幻觉）评分均有结论
- [ ] 发现的冲突已路由 issue-record 或人工裁决，无遗留未决 CONFLICT

### 7.2 评分矩阵（来源 pm888，0-40 分）
- [ ] 四维逐项评分：问题接地（是否真实问题）/ 需求可测（有判据）/ 指标严谨（有基线）/ 范围风险诚实（边界与风险显式）
- [ ] 总分 < 阈值（如 < 24）时，方案不应默认推进，须人工裁决

### 7.3 ADR 追溯与决策预注册（来源 pm888）
- [ ] 每个 DECISION 有内联 ADR：决策/替代方案/理由/后果/信心度/证伪器
- [ ] 决策按四象限（技能/方差/运气/学费）归属，事后可复盘归因
- [ ] 每条结论标 Sourcing 级（事实/输入/模型知识/推断/假设/禁编造），无"禁编造"项混入

### 7.4 下游交接三视角（来源 incremental-prd-collaboration）
- [ ] 以设计/研发/测试三视角各过一遍：先看什么/产出什么/缺什么
- [ ] 产品边界红线：未写 API 路径/HTTP 方法/异常码/DB 结构/字段类型（写了即 [Overreach]）

### 7.5 研发评审版硬标准（来源 pm-master-prosl，抽查）
- [ ] 13 项硬标准抽查：版本/目标/北极星+过程+反向指标/角色场景任务流/组件级需求/状态机/主路径+分支+异常+空状态+权限流程/埋点字段/异常降级安全边界/验收用例/结果交付路径
- [ ] 命中反模式 8 条（老板意见直写需求/只写功能不写价值/背景模糊/验收不可测/只写正常不写异常/优先级伪精确/指标只看增长/发布说明只写技术）即标 [AntiPattern]
