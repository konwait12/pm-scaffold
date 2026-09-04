---
artifact_id: BG-CHANEL-001
main_artifact: BG-CHANEL-001.md
main_version: v0.2
main_sha256: c48602d066c87103303e97bc22935374eb05f247789f186ca608d9394b9fb10a
status: needs_user_input
---

# 项目背景与目标治理伴随文件

> 本文件供 AI、校验器和后续集成读取。人读主文档中不放这些记录。
> 执行说明：盲测轮次 2 产物（v0.1 → v0.2）。原始材料仅两份（见主文档「参考资料」对应的 raw 文件）；PM 于 2026-09-02 就项目类型三选一作出答复（从 0 到 1），本版本据此回写；其余 PM 环节（量化基线、成功指标口径、关键日期）仍未答复，AI 未代替 PM 做任何确认。

## 类型判断与 PM 选择

- AI 判断：从 0 到 1。
- 判断证据与信心（信心中高）：
  1. 目标业务能力是"微信生态内的 DP 客户服务能力"（客户端访问 DP、FA 创建 DP、本地数据追踪），材料将微信生态 DP 定位为"全新时刻"，且方案需新建本地 DP 服务/后端与本地 BI（it-intake 方案概览与架构假设页）；
  2. 按 skill 规则，已有小程序（FSN MP/SA）、账号体系或渠道不改变"从 0 到 1"判断；
  3. 材料呈现章程级 MVP 范围与完整项目时间线（kick off → 设计开发测试 → UAT → go live），不是局部新增或调整。
- 可能误判点：若把全球 DP 服务（2021 年起运行）视为"已有系统"，把中国上线视为其本地化扩展，可判为迭代/扩展；OAB/ORT、InCHANEL 登录等既有能力也可能被视作"已有能力"。
- PM 选择：从 0 到 1（2026-09-02 三选一答复，与 AI 判断一致）。
- PM 覆盖 AI 判断的理由：不适用（PM 选择与 AI 判断一致，无覆盖）。
- 佐证（AI 解读，不构成 CHANEL 业务事实来源）：001 会议基线上俞明宏对 DP 案例的评述为"他其实就想从 0 到 1，在中国弄一个 DP 这样的东西""国外有这样的服务，我们没有"，与 PM 的三选一结论一致（详见「001 会议基线读取记录」四类拆分）。

## 001 会议基线读取记录

- 原文：2026-08-27「PM Scaffold 阶段性成果讨论」会议文字记录（飞书文档 MDVkds3yJocDvGxSYCGceULBn8f）。
- 读取命令：`lark-cli docs +fetch --doc MDVkds3yJocDvGxSYCGceULBn8f --doc-format markdown --scope full --format pretty`（lark-cli：~/.workbuddy/binaries/node/cli-connector-packages/bin/lark-cli）。
- 检索日期：2026-09-02。
- 使用位置：BG-CHANEL-001 / UJ-CHANEL-001 治理伴随文件（`-001` artifact 会议基线段）；记录本产物所属 001 项目的方法论基线，不向主文档注入业务事实。
- 四类拆分（分别记录，不混写）：
  1. 会议明确决定：验证有效性是核心红线——AI 必须以原始业务材料（PPT/口述/几步流程）为输入跑通并产出需求文档，禁止把成品需求文档喂给 AI 改写出文档（俞明宏原意：把最终需求文档给 AI 让 AI 填出一个需求文档"没有意义"）；先单点打磨每个 skill「管用」，再 AI 串联 workflow；交付节奏每周 1–2 个可用 skill，双人 review 定「可用」。
  2. 会议业务示例：以 DP（Digital Passport）项目为例——原始材料即 Client Journey PDF（用户旅程）与系统方案/IT 方案 PDF，最终要输出的是需求文档；俞明宏评述 DP 案例"从 0 到 1，在中国弄一个 DP""国外有这样的服务，我们没有"。
  3. 会议讨论或建议：脚手架流程分业务需求/产品需求两阶段、每阶段设 AI 审批与人工审批；暗区由系统判断哪些必区、哪些暗区；头脑风暴等功能性能力在适当时机调用而非预设为独立阶段；校验规则/状态/异常处理不输出进 PRD，用于校验整个项目、让产出更稳定、减少幻觉；建议先做复杂档（第三档/L2）再做扎实，简单/中等档基于复杂档简化。
  4. AI 解读：本轮 CHANEL 盲测（两份原始 PDF → BG/UJ 两个产物）即上述「先单点验证 skill 是否管用」红线在 BG/UJ 两个 skill 上的执行；会议对 DP 案例「从 0 到 1」的解读与 PM 于 2026-09-02 对项目类型的三选一确认一致，作旁证记录。

## 主张来源与知识状态

> 来源写法：材料文件 + 章节/页。client-journey = raw/client-journey.txt；it-intake = raw/it-intake.txt。六态：FACT / DECISION / ASSUMPTION / AI_INFERENCE / UNKNOWN / CONFLICT。PM 已确认项以 DECISION 登记并标注确认日期。

| 主张 | 知识状态 | 来源或依据 | 主文档落点 |
| --- | --- | --- | --- |
| CHANEL & moi 为每件作品提供持久关注，通过全产品线护理维修服务体现 | FACT | it-intake"Context and business value"Why/How embodied today | 项目背景 |
| 两大目标：深化客户关系、通过护理维修承诺品质 | DECISION | it-intake"2 Main OBJECTIVES" | 项目背景、目标与成功判断 |
| DP 是全产品线数字产品信息查询工具并直达服务；全球 2021 年 4 月启动；HBG&WOC 自 2021-04-01；RTW 2024 年 11 月底；SLG 2025 TBC | FACT | it-intake"DIGITAL PASSPORT: WHAT IS THIS?" | 项目背景、当前现状 |
| 微信生态 DP 创造客户端连接新时刻、强化 CHANEL & moi 中国落地、量化采用（如 DP 注册率） | DECISION | it-intake"Business value" | 项目背景、目标与成功判断 |
| 项目类型三选一 = 从 0 到 1 | DECISION | PM 2026-09-02 三选一答复（与 AI 初判一致）；旁证：001 会议基线上对 DP 案例"从 0 到 1"的评述 | frontmatter、摘要注、当前现状首行、待确认第 1 条 |
| 微信生态中此前没有 DP 能力 | AI_INFERENCE | 由"全新时刻/强化在中国落地/需建本地 DP 服务与后端"推导，材料未直接陈述"中国当前无 DP"；与 PM 确认类型一致 | 当前现状、核心问题二 |
| 为什么是现在：2024-09 已进入设计开发测试阶段、RTW 全球 2024-11 加入、近期节点 9/11、9/18、9/30 | FACT（时间线索）+AI_INFERENCE（"窗口期"归纳） | it-intake"High-level PROJECT timeline""Next steps" | 项目背景 |
| ICON 约 95% 销售、CORE 100% 交易（含换货、员工购买等边缘情况） | FACT | it-intake"MVP guideline for FA journey"注* | 当前现状 |
| FA 在销售仪式中介绍 DP、检查数字账户、协助结账（含远程销售）、按场景创建 DP（整单/选定产品/不创建） | FACT | client-journey"Macro journey"；it-intake"DP business requirement – FA journey" | 当前现状（流程 1-2） |
| DP 创建与支付后通知应即时；DP 实时进入 FSN 小程序账户；POS/ICON/CORE 实时同步 | DECISION | client-journey FA 旅程注*；it-intake 客户/FA 旅程需求 | 当前现状（流程 3）、目标（候选指标） |
| 通知渠道与降级规则（模板可用：SA 消息+EDM+MP 提醒，未关注 SA 者 SMS；不可用：SMS+EDM+MP 提醒） | DECISION | client-journey"DP related notifications rules"；it-intake 客户旅程需求 | 约束与依赖 |
| 腾讯严格管控服务号新消息模板（风险） | FACT | client-journey 风险标注 | 核心问题四、待确认第 4 条 |
| 仅数字账户客户可持有 DP；仅国内购买可加入（legal 与 PCN 约束）；Gifting 等全球方案、海外等 PCN 方案 | DECISION | 两份材料"MVP guideline for client journey" | 约束与依赖、边界与非目标 |
| MVP 品类：HBG&WOC 与 RTW；SLG 目标 2025 Q2（全球计划） | DECISION | it-intake"MVP guideline for FA journey" | 约束与依赖 |
| 退换货时 DP 与客户解除关联、精品店可立即转售、换货符合条件时 FA 重新激活 | DECISION | client-journey"Specific scenarios (Return & Exchange)"；it-intake 客户旅程需求 | 当前现状（流程 5） |
| 分享 DP 时须去除 SN、购买与保修信息；仅登录客户可见 DP | DECISION | client-journey PDP–share DP 及业务规则标注 | 当前现状（流程 4，概要级） |
| 数据追踪目的、两个 epic、六个分析维度、BI 呈现 | FACT | it-intake"MVP guideline for data tracking""Key epics""Dimension Explanation" | 目标与成功判断（交付结果 4） |
| 数据权限：精品店指标对店管理团队开放、店内按角色授权、概览仅 Fashion office | DECISION | it-intake 数据追踪 MVP 指南 | 边界与非目标 |
| BI 数据来自 We-analyze、CN DP、CRM 三源；依赖 SN360/YEXT/LION/PIONEER 等；ORT H5 与搜索筛选待方案 | ASSUMPTION | it-intake"solution & architecture assumption"（材料自标为假设） | 约束与依赖 |
| 候选成功指标（DP 注册率、通知到达时延、同步时延、访问转化、售后入口使用）及口径 | ASSUMPTION | 按 background-4elements"SLA 候选值推导"框架由 AI 推导，未经 PM 确认 | 目标与成功判断（候选指标表） |
| 观测窗口 30/90 天 | ASSUMPTION | AI 推导建议 | 目标与成功判断（承诺与观测段） |
| go live 约 2025 年 4–6 月区间 | AI_INFERENCE | it-intake 高层时间线横轴读取 | 目标与成功判断（时间窗口） |
| 中国 DP 注册率、通知触达、售后耗时等基线 | UNKNOWN | 两份材料均未给出；已列取数路径（全球/EU 仪表板、We-analyze/CRM、售后记录、抽样、负责人估算） | 待确认第 2 条 |
| 中国客户当前获取保修信息与售后的做法 | UNKNOWN | 材料未描述 | 当前现状、待确认第 8 条 |
| 远程销售的客户旅程 | UNKNOWN | client-journey"Next step"明确列为待办（FA 侧含远程销售为 DECISION） | 边界与非目标、待确认第 6 条 |
| go live 具体日期、与 InCHANEL 联动、试点范围与精品店选择 | UNKNOWN | it-intake 时间线未给具体日期；"Pilot targeted in 2025"未展开 | 待确认第 6 条 |
| HBG 差异化护理内容 TBC、质保条款待 Legal、字段缺失场景原型待全球提供 | FACT（待办性质） | client-journey 相关页注 | 待确认第 5 条 |
| DP 启动日期两说：2021-04-01（品类资格）vs 2021-04-08（服务启动） | CONFLICT | it-intake 同一页两处表述，材料未说明二者区别 | 待确认第 7 条 |
| Gifting 位置：9 月版 MVP 范围图含"Automation & Gifting"于 MVP 框，但指南注明等待全球方案 | CONFLICT（轻微） | client-journey 6 月版该格为"Automation"；it-intake 9 月版为"Automation & Gifting" | 待确认第 7 条 |

## 澄清记录

> 盲测执行：以下为本轮 AI 提出的高影响问题（每轮不超过 5 个）。2026-09-02 PM 已答复「项目类型」一题并确认产物配置；其余 PM 环节待答复。阻断性问题未获答复前，状态保持 needs_user_input。

| 问题 | AI 初步判断 | PM 答复 | 是否阻断 | 回写位置 |
| --- | --- | --- | --- | --- |
| 项目类型三选一：重构 / 从 0 到 1 / 迭代？ | 从 0 到 1（证据见"类型判断与 PM 选择"）；若以全球 DP 为既有系统可判迭代/扩展 | 从 0 到 1（2026-09-02 答复） | 已答复，解除阻断 | 治理文件类型段、主文档 frontmatter、待确认第 1 条 |
| 中国 DP 注册率等基线能否取到？（全球 SN 仪表板是否含中国数据；We-analyze/CRM 有无现有口径） | 全球仪表板存在但中国本地 BI 待建，判断"部分可取、需拼接"；取不到时降级抽样/负责人估算 | 待答复 | 是（影响目标可验证性） | 目标与成功判断（基线段）、待确认第 2 条 |
| 成功指标选哪个/哪些？口径与目标值如何定（注册率分母按产品/交易/客户？时延阈值？） | 推荐 DP 注册率 + 通知到达时延为首批（材料分别给出"量化采用"与"即时"要求） | 待答复 | 是 | 目标与成功判断（候选指标表） |
| go live 具体日期与 InCHANEL 小程序上线联动方式？试点（Pilot targeted in 2025）范围与精品店？ | 时间线仅到月，判断需 PM 依 InCHANEL 排期确认 | 待答复 | 否（不阻断背景目标，但影响时间约束） | 待确认第 6 条 |
| 远程销售的客户旅程是否纳入本次范围？ | FA 侧已含远程销售（DECISION），客户侧旅程材料明确待定义，建议列为后续工作 | 待答复 | 否 | 边界与非目标 |

## AI Audit

以项目组成员视角重读主文档（v0.2），逐项核对 audit-checklist：

- 能否一两句话说清项目是什么、为什么现在做、要改变什么：能。摘要与背景直接回答"在微信生态首次建立 DP 能力、深化客户关系、让 CHANEL & moi 在中国可见可感"；"为什么是现在"标注为 AI_INFERENCE 并给了材料时间线索。
- 是否先还原高层业务事件而非罗列功能页面：是。"当前现状与已有做法"还原了五步业务流程与已有做法；页面级细节（PDP 字段、搜索条件、红点规则）均已排除。
- 当前做法与问题是否来自原始材料：是。四处问题均标注材料出处；两处材料未支持的（中国无 DP 痛点、当前售后做法）分别标 AI_INFERENCE 与 UNKNOWN，未补造。
- 输入以方案/旅程为主时是否区分了范围证据、AI 高层理解、无法得出的背景与目标：是。MVP 指南/旅程作为范围与规则证据登记为 FACT/DECISION；业务动机中材料仅设问处标 AI_INFERENCE；量化基线列 UNKNOWN 并给取数路径。
- 类型写法是否符合（从 0 到 1 写线下/已有步骤与要建立的结果）：符合。项目类型已由 PM 拍板（2026-09-02），类型写法与 frontmatter 同步；已有做法五条 + 首个完整业务流程五步 + 要建立的业务结果四条。
- 角色、约束、依赖、边界、非目标是否遗漏：已覆盖材料中全部角色（客户/FA/精品店/Fashion office/IT/全球/法务/腾讯）与约束（合规/范围/通知降级/组织/技术数据/时间）；非目标含 Gifting、海外购买、未来阶段功能、SLG、FA 侧详细旅程。
- 目标能否判断成败；不能量化的是否明确待确认：候选指标表给出指标名+口径+数据来源，全部标 ASSUMPTION 并注明"PM 确认口径后才升 DECISION"；基线 UNKNOWN 已附取数路径。
- 是否把功能、页面、字段、接口或架构误写成业务事实：否。技术与架构内容仅出现在"约束与依赖"，且标注为材料自述的"方案假设"（ASSUMPTION）。
- 是否保留来源冲突和未知而不是静默选边：是。CONFLICT 两条（DP 启动日期、Gifting 位置）保留在待确认第 7 条；UNKNOWN 四类均未擅自补全。
- Audit 结论：通过（自评）。v0.2 相对 v0.1 的实质变化：项目类型从"AI 判断待确认"升级为"PM 拍板从 0 到 1"（治理文件 DECISION 登记 + 主文档回写），其余内容未引入新业务事实。主要风险：材料为方案/旅程型输入，业务问题与紧迫性证据偏定性，已按规范以 AI_INFERENCE/UNKNOWN 显式标注并给取数路径，待 PM 补充量化基线与确认成功指标口径。

## PM 确认与变更

| 日期 | 确认人 | 决定 | 说明 |
| --- | --- | --- | --- |
| 2026-09-02 | PM（工作台对话方） | 项目类型三选一 = 从 0 到 1 | 盲测轮次 2 产物配置确认：产物落点 blind-test-round2-chanel/products、项目类型从 0 到 1、UJ 粒度 business+product、深版 v0.2（吸收盲测对比报告 P0/P1）。本产物升级 v0.2 回写该决定；不影响 confirmed 语义（AI 永不设 confirmed） |
| 待确认 | 待确认 | 待确认 | 剩余 PM 环节：量化基线可获取性、成功指标口径与目标值、关键日期；确认前状态保持 needs_user_input，确认后方可在宿主流程中推进 |
