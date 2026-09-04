---
artifact_id: UJ-CHANEL-001
main_artifact: UJ-CHANEL-001.md
main_version: v0.2.0
main_sha256: ee8a2d295c6f0851027bf273bbb15ffc62afd88d9e09965d7e0006462ec2d3d8
status: needs_user_input
board_artifact: UJ-CHANEL-001.board.html
---

# UJ-CHANEL-001 治理伴随文件（Chanel & moi Digital Passport 用户旅程）

## 类型判断与输入充分度

- 旅程类型：业务事件生命周期旅程（Digital Passport 从购买到解绑/删除的完整生命周期）。
- 粒度：`business+product`。AI 判断与证据：材料同时包含业务层宏观旅程（SRC-001·L120-151；SRC-002·L186-215）与 FSN 小程序内产品层交互流程（SRC-001·L219-1014），故按「业务层为主 + 产品层展开（角色旅程矩阵内子表分开）」产出；**Q-GR-001 已闭环**：PM 于 2026-09-02 三选一答复为 C（business+product），frontmatter `granularity` 与主文档组织均已回写。
- 材料成熟度：L3（角色、阶段、触点和部分分支清楚；情绪证据缺失）。
- 材料隔离测试模式：**启用**。事实输入仅限 PM 本轮指定的 SRC-001、SRC-002 两份原始文件；上游 BG 产物、reference、搜索结果与模型记忆仅作方法背景，未补充、未纠正、未暗示任何旅程事实。主文档每条事实均可回到指定原始材料的行号位置。
- 上游产物：BG-CHANEL-001（v0.2）为候选基线（status=needs_user_input），主文档全部内容为**候选**，等待授权人类确认。
- 起点/终点判断（AI_INFERENCE）：起点=销售仪式开始（客户购买）；终点=客户长期重新访问 DP（Re-access）或 DP 解绑/删除。依据：SRC-001·L120-151 宏观旅程首尾节点；终点不视为已确认。
- v0.2 变更范围（2026-09-02）：吸收盲测对比报告 P0/P1 改进（A-1～A-6 修复、P1 空态/身份骨架、A-7 占位符登记），见主文档「预检与摘要 · v0.2 变更摘要」；节点库存（2 角色 × 28 节点）与六阶段保持不变，变更集中在产品层展开与覆盖/边界章节，未新增未经材料证实的事实。

### 已加载 reference 清单

| reference | 状态 | 跳过理由 |
|---|---|---|
| references/thinking-framework.md | 已加载 | — |
| references/source-handling.md | 已加载 | — |
| references/output-contract.md | 已加载 | — |
| references/audit-checklist.md | 已加载 | — |
| references/anti-patterns.md | 已加载 | — |
| references/journey-matrix-and-mot.md | 已加载 | — |
| references/journey-error-recovery-and-metrics.md | 已加载 | — |
| references/journey-behavior-vs-feature-jtbd.md | 已加载 | — |
| references/html-journey-board.md | 已加载 | — |
| references/reviewer-checklist.md | **跳过** | 本次盲测执行未进入人工评审环节，PM 未发起评审，无评审前检查对象 |

条件必选触发说明：journey-matrix-and-mot（角色数 2 ≥ 2 且阶段数 6 ≥ 3）；journey-error-recovery-and-metrics（材料含"错误通知/创建失败/退换/删除/待定方案"等异常信号）；journey-behavior-vs-feature-jtbd（材料含大量页面/按钮/字段等实现层描述，用于防功能泄漏）；html-journey-board（PM 明确要求 HTML 可视化画板）。产物中可追溯的方法落点：旅程矩阵与网格（journey-matrix-and-mot §2）、MOT 三判据（§3）、触点矩阵（§4）、E1-E6 异常表与旅程指标（journey-error-recovery-and-metrics §4/§5）、行为层改写与一句话叙事（journey-behavior-vs-feature-jtbd §1/§2）、画板契约（html-journey-board 全文）。

## 001 会议基线读取记录

- 原文：2026-08-27「PM Scaffold 阶段性成果讨论」会议文字记录（飞书文档 MDVkds3yJocDvGxSYCGceULBn8f）。
- 读取命令：`lark-cli docs +fetch --doc MDVkds3yJocDvGxSYCGceULBn8f --doc-format markdown --scope full --format pretty`（lark-cli：~/.workbuddy/binaries/node/cli-connector-packages/bin/lark-cli）。
- 检索日期：2026-09-02。
- 使用位置：BG-CHANEL-001 / UJ-CHANEL-001 治理伴随文件（`-001` artifact 会议基线段）；记录本产物所属 001 项目的方法论基线，不向主文档注入业务事实。
- 四类拆分（分别记录，不混写）：
  1. 会议明确决定：验证有效性是核心红线——AI 必须以原始业务材料（PPT/口述/几步流程）为输入跑通并产出需求文档，禁止把成品需求文档喂给 AI 改写出文档（= 拿成品改成品，无价值）；先单点打磨每个 skill「管用」，再 AI 串联 workflow；交付节奏每周 1–2 个可用 skill，双人 review 定「可用」。
  2. 会议业务示例：以 DP（Digital Passport）项目为例——原始材料即 Client Journey PDF（用户旅程）与系统方案/IT 方案 PDF，最终要输出的是需求文档；会上评述 DP 案例「从 0 到 1，在中国弄一个 DP 这样的东西」「国外有这样的服务，我们没有」。
  3. 会议讨论或建议：脚手架流程分业务需求/产品需求两阶段、每阶段设 AI 审批与人工审批；暗区由系统判断；头脑风暴等功能性能力在适当时机调用而非预设为独立阶段；校验规则/状态/异常处理不输出进 PRD，用于稳定产出、防幻觉；先做复杂档再简化出简单/中等档。
  4. AI 解读：本轮 CHANEL 盲测（两份原始 PDF → BG/UJ 两个产物）即「先单点验证 skill 是否管用」红线在 BG/UJ 两个 skill 上的执行；v0.2 的「品类强制分列 / 形态枚举 / 空态与身份骨架」改进即本轮对 skill 质量缺陷的修复闭环，与会议「单点打磨 skill 质量」的节奏一致。

## 主张来源与知识状态

### 来源登记

| 字段 | SRC-001 | SRC-002 |
|---|---|---|
| title_or_description | Client journey（Digital Passport 客户旅程 PDF 文本） | IT intake（业务需求简报 + 方案与架构假设） |
| format | PDF 转文本（PPT 页序保留，含图片占位文字） | PDF 转文本（同左） |
| author_or_speaker | Digital Service Innovation & Client Experience · Client experience & retail innovation · FASHION MAINLAND CHINA | 同左 |
| provided_by | PM（盲测任务指定） | PM（盲测任务指定） |
| created_at | 2024-06 | 2024-09 |
| retrieved_at | 2026-09-01 | 2026-09-01 |
| authority_scope | 内部材料（Internal use）：客户旅程 MVP 设计与场景细节 | 内部材料：业务需求简报、FA 旅程需求、数据追踪与方案假设 |
| location_or_link | 05_临时缓存回收站/blind-test-round2-chanel/raw/client-journey.txt | 05_临时缓存回收站/blind-test-round2-chanel/raw/it-intake.txt |
| notes | 含多处 TBC/pending/assumption 标注；版式转文本后个别标注（如 Today's focus）位置无法精确定位 | 时效性晚于 SRC-001 三个月；两材料宏观旅程一致，SRC-002 版补充"含远程销售"并以 CHANEL & moi 与 DP 表述 |

### 知识状态汇总

- FACT：旅程结构（2 角色、6 阶段）、28 个节点的行为/触点/路径类型、通知渠道与降级规则、入口与登录规则、**MP 内三提醒形态（红点/New/Reminder 弹窗）**、**HBG/RTW 品类字段与入口差异**、**EDM 三模板图示**、退换解绑规则、FA 工具创建与状态同步、数据追踪口径（均可定位到 SRC 行号）。
- DECISION：1 条已确认——粒度 Q-GR-001 = C（business+product，PM 2026-09-02 答复）。材料中的 MVP 指引按 FACT 登记为"材料明确陈述"；流程内的人工确认尚未发生，等待授权人类确认。
- ASSUMPTION：1 条——删除最后一件 DP 的场景（SRC-001·L706 材料自标 Assumption，主文档 C-15/E6/R5）。
- AI_INFERENCE：SA 指代解读（C-1）、Today's focus 位置解读、起点/终点判断、MOT 结构性判断、身份×登录×资产状态影响面结论、画板顺畅度推导。
- UNKNOWN：全部节点情绪、Reminder 触发频率与文案（Q-UJ-005）、EDM 模板选择规则（R8）、通知即时性阈值、指标目标值、技术方案细节（搜索/筛选/视图/分享/ORT H5）、短信/EDM 占位符口径（R7）、E4/E6 的 Test、空态去向。
- CONFLICT：1 条（CONFLICT-001，见下）。

### 冲突登记 CONFLICT-001（保留双方陈述，未选边）

- 陈述 A（SRC-001·L1003，退换场景 FA 行）：「There is no action needed by FA」（FA Tool）。
- 陈述 B（SRC-001·L1009，同场景）：「FA needs to reactivate the DP if the products are eligible」（FA Tool；标注 to be shared in the FA journey session）。
- 可能解读（AI_INFERENCE，仅供裁决参考）：A 对应退货、B 对应换货（换得的新品符合条件时需重新激活）；但文本版式无法证实归属。
- 影响：FA-12 节点行为与 S6 路径类型；裁决人：业务负责人（待指认）；状态：未裁决。已关联澄清问题 Q-UJ-001。

## 澄清记录

| 字段 | 内容 |
|---|---|
| question_id | Q-GR-001 |
| 问题 | 本旅程按哪种粒度产出？ |
| AI 初步判断及证据 | C（业务层为主+产品层展开）。证据：材料含宏观旅程（SRC-001·L120-151）与小程序交互流程（SRC-001·L219-1014）。 |
| A/B/C 选项 | A 只做业务层；B 只做产品层（前提：业务层已确认）；C 都要（业务层为主，产品层作业务阶段展开） |
| PM 答复 | **C（business+product）——2026-09-02 已答复** |
| 负责人 | PM |
| 影响 | 主文档结构、产品层子表去留、下游输入（user-stories vs page-design） |
| 是否阻断 | 已答复，解除阻断 |
| 回写位置 | frontmatter granularity + 角色旅程矩阵产品层子表 |
| 回写后的 Audit 结果 | 通过（主文档按 C 组织，产品层展开含形态清单/品类对照/占位符登记） |

| 字段 | 内容 |
|---|---|
| question_id | Q-UJ-001 |
| 问题 | 退换场景中 FA 是否需要行动（CONFLICT-001）？ |
| AI 初步判断及证据 | 无法判定，保留冲突。证据：SRC-001·L999-1010 同时出现两种表述。 |
| A/B/C 选项 | A 退货无需 FA 操作、换货符合条件需重新激活；B 两者均无需操作；C 其他（自由回答） |
| PM 答复 | 待确认 |
| 负责人 | 业务负责人（待指认） |
| 影响 | FA-12 节点行为与 S6 路径覆盖 |
| 是否阻断 | 否（已按 CONFLICT 标注，未静默选边） |
| 回写位置 | FA-12 节点、路径覆盖表 |
| 回写后的 Audit 结果 | 待回写 |

| 字段 | 内容 |
|---|---|
| question_id | Q-UJ-002 |
| 问题 | 材料无任何情绪证据，如何处理情绪层？ |
| AI 初步判断及证据 | 全部标 UNKNOWN，画板仅用路径类型推导顺畅度并显式标注 AI_INFERENCE。证据：两份材料全文无客服/流失/满意度类陈述。 |
| A/B/C 选项 | A 接受路径类型推导（AI_INFERENCE 标注）；B 补充客服/调研/流失材料；C 情绪层留空 UNKNOWN |
| PM 答复 | 待确认 |
| 负责人 | PM/业务负责人（待指认） |
| 影响 | 痛点优先级、机会评分、MOT 情绪判据 |
| 是否阻断 | 否（当前按最保守处理） |
| 回写位置 | 路径与情绪章节、画板情绪曲线 |
| 回写后的 Audit 结果 | 待回写 |

| 字段 | 内容 |
|---|---|
| question_id | Q-UJ-003 |
| 问题 | 宏观旅程 "Follow SA and register the FSN MP" 中 SA 指代？ |
| AI 初步判断及证据 | 更可能指 FSN 服务号（材料中 FSN SA 均指 Service Account）。证据：SRC-001·L142、SRC-002·L206-208。 |
| A/B/C 选项 | A FSN 服务号；B 销售助理；C 其他（自由回答） |
| PM 答复 | 待确认 |
| 负责人 | 业务负责人（待指认） |
| 影响 | C-1 行为表述准确性 |
| 是否阻断 | 否 |
| 回写位置 | C-1 节点行为 |
| 回写后的 Audit 结果 | 待回写 |

| 字段 | 内容 |
|---|---|
| question_id | Q-UJ-004 |
| 问题 | 旅程范围：客户为主 FA 为辅（当前），还是仅客户侧 / 完整 FA 旅程另做？ |
| AI 初步判断及证据 | 客户为主 FA 为辅。证据：任务重点为"客户旅程"，但宏观旅程含 FA 行（SRC-001·L120-151），IT intake 含 FA 旅程需求（SRC-002·L265-343），静默丢弃即违反反模式 AP4。 |
| A/B/C 选项 | A 客户为主 FA 为辅（当前）；B 仅客户侧（FA 行移出）；C 完整 FA 旅程另行产出 |
| PM 答复 | 待确认 |
| 负责人 | PM |
| 影响 | 矩阵行列、画板角色泳道 |
| 是否阻断 | 否 |
| 回写位置 | 角色旅程矩阵、画板 |
| 回写后的 Audit 结果 | 待回写 |

| 字段 | 内容 |
|---|---|
| question_id | Q-UJ-005（v0.2 新增，对应盲测 A-3 修复追问） |
| 问题 | Reminder 弹窗（MP 内第三提醒形态）的触发频率/出现条件/文案规则？材料仅在各路径流程图中给出「Receive a reminder」节点，未给规则。 |
| AI 初步判断及证据 | 红点（进列表前持续）与 New 标签（开 PDP 前/最长 3 个月）均有规则，Reminder 无；推断为「打开 MP 进入列表前出现、与本次新 DP 相关」，但不可证，故追问。 |
| A/B/C 选项 | A 每次进入列表前出现；B 仅新 DP 创建后首次进入出现；C 其他（自由回答） |
| PM 答复 | 待确认 |
| 负责人 | 产品负责人（待指认） |
| 影响 | S4 提醒体验、提醒形态清单第 6 行、E 表可验收性 |
| 是否阻断 | 否（已按 UNKNOWN 登记，未并入红点/New 形态） |
| 回写位置 | 主文档形态清单 Reminder 行、Q-UJ-005 |
| 回写后的 Audit 结果 | 待回写 |

## HTML 审阅板记录

- 板文件：`UJ-CHANEL-001.board.html`（单文件、零外部网络依赖、只读；基于 skill `assets/journey-map-studio.html` 模板复制后仅替换 DATA 数据块与说明文字，渲染逻辑未改动）。
- 生成前报告（按 html-journey-board.md「生成前先向 PM 报告角色、阶段、路径数量和缺口」）：角色 2（客户、FA）、阶段 6、节点 28（客户 16 + FA 12）；FA 在 S3/S4 无节点，按 skill 规则如实留空，未虚构行为填充；路径六态全覆盖，failure 客户侧与客户侧上下文保留为已声明缺口。
- 节点覆盖核对（硬约束）：主文档角色旅程矩阵节点 C-1～C-16、FA-1～FA-12 共 28 个，与画板 `roles[].nodes` 逐节点核对一致（2 角色 × 28 节点，一个不缺）；泳道图 lanes=2、swim nodes=28，覆盖全部角色泳道；旅程地图视图支持角色切换（综合视角 + 每角色独立旅程，角色无节点的阶段不出现，不压缩为混合旅程）。
- v0.2 同步说明：v0.2 深版新增内容（通知/提醒形态清单、HBG/RTW 品类对照、分支骨架与空态矩阵、占位符登记）属**文档级结构化表达**，画板按节点契约同步受影响的节点文本（C-4 通知形态、C-11 品类分列、C-14 ORT 适用范围）与触点/痛点行；不新增画板节点（节点库存与泳道/边结构不变，保持与主文档矩阵一一对应）。产物级一致性：主文档矩阵 ↔ 画板 `roles[].nodes` ↔ `swim.nodes` 仍一一对应。
- 一致性检查：板上角色、阶段、路径类型、知识状态徽标（FACT/AI_INFERENCE/UNKNOWN/ASSUMPTION/CONFLICT 经徽标色区分）与主文档一致；情绪分值为路径类型推导并显式标注 AI_INFERENCE；证据不足项未渲染成确定结论。
- 已知限制：材料无情绪证据 → 板上情绪/顺畅度曲线为推导值；"Today's focus"位置、SA 指代等未知项见澄清记录；Reminder 触发规则、EDM 模板选择、身份/空态去向等 TBC/假设项，板上仅以节点+标注呈现，不新增内容。
- 展示意见回流：如评审对板提出修改意见，将回写本文件澄清/变更记录，不直接升级为业务事实。

## AI Audit

```text
status_recommendation: needs_user_input
passed_checks:
  - 结构闸门：模板全部必需标题齐备；frontmatter 12 个必需字段齐备（未知值写待确认，未伪造确认结果）；主文档无治理表残留（ReviewRecord/SHA-256/SRC-001 | 模式均未出现）
  - 来源覆盖闸门：两份指定材料均已登记并给出行号定位；直接陈述与 AI 解读可区分；冲突保持可见
  - 语义闸门：每个阶段有触发/行为/触点/结果/路径类型；路径六态覆盖且缺口显式；情绪无证据不编造
  - v0.2 P0 修复核查：①HBG/RTW 字段/功能入口/信息入口/ORT 适用范围已分列（品类对照表，A-1/A-2/A-5）；②Reminder 弹窗已识别为独立第三形态并生成 Q-UJ-005 追问，未并入红点/New（A-3）；③EDM 三模板已逐一枚举（A-4）；④通知/提醒六形态清单齐备（A-3 修复）
  - v0.2 P1 修复核查：⑤身份×登录×资产状态分支骨架含影响面清单（A-6）；⑥资产空态矩阵覆盖列表与入口去向（P1）；均以材料行号为限，TBC 处如实标注
  - v0.2 P2 轻度：⑦短信/EDM 动态占位符登记（R7，供下游认领）
  - 行为层防功能泄漏：业务层主语为角色；「进入某页面/点击按钮」类表述隔离在产品层展开（granularity 已声明）
  - 反模式自查：AP1（功能≠目标）、AP2（无外部结论）、AP3（机会量化标待确认）、AP4（材料信息未静默丢弃，含 FA 行/退换/InCHANEL TBC/品类差异）、AP5（冲突未选边）、AP6（情绪/未知不编造）、AP7（无方案建议）、AP8（每条不确定项有负责人+处理方式）
  - 可视化一致性：画板 2 角色 × 28 节点与主文档矩阵一一对应（v0.2 仅文本级同步）
failed_checks: 无阻断失败项；非阻断：Q-GR-001 已闭环；Q-UJ-001～005、R1-R8 仍待确认（已登记负责人与处理方式）
repairs_applied:
  - 将「进入列表页/点击链接」类功能表述改写为业务行为，原文交互流程保留在产品层子表
  - 情绪全部改标 UNKNOWN，画板顺畅度改用路径类型推导并显式标注 AI_INFERENCE
  - CONFLICT-001 保留双方陈述，未静默选边
  - 综合视角情绪分值改为按各阶段最保守路径分推导（min），避免拔高
  - v0.2：品类信息由合并表述改为 HBG/RTW 分列（C-11/C-14/品类对照表）；Reminder 由并入红点/New 改为独立形态 + 澄清问题；EDM 由一笔带过改为三模板枚举；新增空态与身份×登录分支骨架（材料 TBC 处不补全）
blocking_questions: 无（候选产出）；对基线确认而言，Q-UJ-001～005 与上游 BG 整体确认是前置
nonblocking_unknowns: R1-R8、全部节点情绪 UNKNOWN、指标目标值、身份/空态 TBC 去向
decisions_required: Q-UJ-001（CONFLICT-001 裁决）、Q-UJ-004（范围）、Q-UJ-005（Reminder 规则）、R7/R8（占位符与模板选择口径）
traceability_gaps: E4/E6 Test 待确认；failure 路径客户侧闭环缺口；错误后上下文保留未描述；空态去向裁决依赖 R5 假设验证
downstream_risks: 下游 user-stories/feature-list 须待旅程确认后消费；搜索/筛选/分享等待技术方案影响排期；ORT H5 性能影响 O3；品类差异若在下游合并表述将重演 A-1/A-2/A-5（v0.2 已显式继承）
```

- 校验器运行结果：`python3 scripts/validate_artifact.py`（详见下方回填记录）。

### 校验器运行记录

- 第 1 次运行（v0.1.0）：PASS（0 errors；对应 v0.1 版校验器口径）。
- 第 2 次运行（v0.2.0 终版，2026-09-02）：PASS（0 errors，0 warnings）。校验按 v0.1 同款「规范名暂存目录」方式执行：将主文档与治理文件以规范名（user-journey.md / user-journey.governance.md）复制到暂存目录后运行 `python3 scripts/validate_artifact.py`；校验器对伴随文件的定位依赖规范名，交付目录沿用产物命名（UJ-CHANEL-001.md / UJ-CHANEL-001.governance.md）。

## PM 确认与变更

- 已确认：Q-GR-001 粒度 = business+product（选项 C，2026-09-02）；产物配置四件套（落点 blind-test-round2-chanel/products、项目类型从 0 到 1、UJ 粒度 C、深版 v0.2 吸收 P0/P1）。
- 待 PM 确认清单：Q-UJ-001～Q-UJ-005 的答复；R1-R8 负责人指认；状态推进（needs_user_input → 后续状态由授权人类决定）。
- 人工闸门：机器校验只产出候选与校验结果，`confirmed` 永远不能由 AI 设置；需授权业务/产品负责人在宿主流程中批准。
- 变更记录：v0.1.0（2026-09-01）初始产出（盲测轮次 2）；v0.2.0（2026-09-02）深版升级——吸收盲测对比报告 A-1～A-7 修复（品类分列/Reminder/EDM 三模板/形态清单/分支骨架/空态矩阵/占位符登记），粒度闭环为 C；无已确认内容被变更（全程无 confirmed 内容）。
- 回流约定：已确认内容发生变化时，记录变更与下游影响，重新生成 Markdown/HTML、重跑 Audit，再回到人工评审；不在下游 skill 中静默修补上游旅程。
- 治理哈希：主文档 v0.2.0 的 SHA-256 摘要记录于本文件 frontmatter `main_sha256`（校验器已核验一致）。
