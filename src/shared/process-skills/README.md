# 过程型能力中心（Process Skills Hub）

> 本目录是**所有过程型能力（process capabilities）的统一入口**，供任何产物型 SKILL 在"输入 → 输出 → 治理"环节遇到跨阶段问题时显式路由。
>
> **背景**：本脚手架的产物型 skill 是"做一份什么"（BG / UJ / US / FEA / FUN / BR / VL / STATE / EX / AC / PRD），而过程型 skill 是"以什么方式做"——事实台账 / 14 维缺口 / 访谈提炼 / 复述确认 / 问题清单 / 头脑风暴 / 范围谈判。
>
> 历史问题：过程型能力 references 之前散落在各自 SKILL 表格里，被 81% 的产物型 skill 列为"按需加载"，但 SKILL 主体从未引用——AI 跑产物时**根本不会主动加载**这些能力。本目录的存在就是为了**强制路由**：每个产物 SKILL 在 §4 Clarify 和 §6 Audit 阶段必须主动检查"是否需要路由到本目录的某个能力"。

---

## 一、能力矩阵（4 类过程能力 × 3 类应用场景）

| 能力 | 触发场景 | 调用入口 | 产物形态 |
|---|---|---|---|
| **事实台账 / fact-ledger** | 多源素材 / 冲突仲裁 / 任何要标 `FACT` 的主张 | `references/fact-ledger.md` | F/D/A/W/O 五分型 + 来源可信度仲裁 |
| **14 维缺口扫描 / gap-checklist** | Intake 后 / Generate 前 / Audit 前 | `references/gap-checklist-14d.md` | 14 维度（角色/流程/规则/状态/数据/集成/界面/异常/性能/合规/迁移/灰度/度量/可测试性）扫描清单 |
| **访谈五步 / interview-synthesis** | 大量口语化原话 / 聊天记录 / 会议纪要 | `references/interview-synthesis.md` | 目标/角色/场景/规则/风险五步提炼 |
| **MRC 门禁 / confirmation-signal** | Clarify 阶段完整度阈值 / 用户回复是否真正确认 | `src/shared/clarify/references/confirmation-signal-technique.md` | 白/灰/黑信号识别 + 6 项门禁判定 |
| **需求复述 / requirement-restate** | 多源歧义 / 需要"我们真的同意了吗"检查位 / 新 stakeholder 锚定 | `src/stages/001-business-requirements/skills/requirement-restate/SKILL.md` | RR-XXX 复述清单 + CONFLICT/UNKNOWN 路由 |
| **头脑风暴 / brainstorming** | L0 一行想法 / 材料稀疏 / 方案发散 | `src/support-skills/brainstorming/SKILL.md` | SCN-XXX 候选 + 4 值处置（include/exclude/defer/research） |
| **问题清单 / issue-record** | 任何阶段出现 BLK/RSK/DEC/INF/CLS/OUT 信号 | `src/shared/clarify/skills/issue-record/SKILL.md` | ISS-NNN 六类问题 + B3 阶段收口 |
| **范围谈判 / scope-negotiation** | Clarify 阶段范围扩张/压测/竞品对标/优先级摊平 | `src/shared/clarify/references/scope-negotiation-scripts.md` | 4 类脚本（加 X / must-have / 竞品 / 全 P1） |
| **证据四维 / evidence-four-dimension** | 任何标 `FACT` / Human Gate / 对抗审查 | `src/shared/audit/evidence-four-dimension-check.md` | 来源/规模/匹配/方向四维核验 |
| **红队压力测试 / red-team-naysayer** | ready_for_human_review 前作者自查 / Human Gate 前评审 | `src/shared/audit/red-team-naysayer.md` | 10 铁律 + 3 阶段红队问题清单 |

---

## 二、产物 SKILL 强制路由点（每个 SKILL 必须检查的 4 个时点）

| 时点 | 检查问题 | 路由到 |
|---|---|---|
| **§1 Preflight** | "输入材料有多源歧义吗？是否有 W 诉求型需要拆出？是否 L0 稀疏？" | → fact-ledger / interview-synthesis / brainstorming |
| **§2 Intake** | "逐字提取的素材是否要做 14 维结构性遗漏扫描？是否要识别 MRC 信号？" | → gap-checklist-14d / confirmation-signal |
| **§4 Clarify** | "出现了 CONFLICT / UNKNOWN / 范围争议 / 多源不一致？" | → issue-record / scope-negotiation / requirement-restate |
| **§6 Audit** | "标 `FACT` 的主张过四维证据了吗？是否需要红队压力测试？" | → evidence-four-dimension / red-team-naysayer |

> **硬规则**：每个产物 SKILL 的 §4 Clarify 必须显式提及"过程型能力中心"（引用本 README），否则视为治理缺陷。

---

## 三、与 `workflow-registry.json` 的关系

`workflow-registry.json` 的 `support_capabilities[]` 已声明 4 个 process 类型：
- `requirement-restate`（output_kind=process）
- `brainstorming`（output_kind=process）
- `issue-record`（output_kind=artifact）
- `competitive-research` / `feasibility-analysis`（output_kind=artifact）

本目录不新增注册条目，**只做索引与路由**——让 14 个产物 skill 在治理上不漏掉这 4 类能力。

---

## 四、为什么这个目录之前不存在

读历史：原架构里这些能力 references 散落在各自 SKILL.md 的"加载参考文档"表格里，但 SKILL 主体从未引用。结果 81% 的 references 是孤岛——AI 跑产物时按字面理解 SKILL，不会加载它们。

修复路径：每个 SKILL.md 主体必须显式引用本 README，并在 4 个时点（Preflight / Intake / Clarify / Audit）检查路由。

---

## 五、详细 integration 文档

- `requirement-restate-integration.md` —— RR 怎么被 BG/UJ/US 调用
- `brainstorming-integration.md` —— 怎么被 BG 调用（L0 降级）
- `issue-record-integration.md` —— 怎么被任何 SKILL 调用（B3 收口）
- `references/` —— RR 缺失的 7 个能力 references

