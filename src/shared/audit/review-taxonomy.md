# PRD 审查分类法 · Review Taxonomy

> 借鉴社区 PRD 审查最佳实践，用于 PRD 审查时统一问题标签和裁决标准。
> 本文件是 `prd-assembly` Human Gate 阶段的审查语言，与 `audit-checklist.md` 互补。
> audit-checklist 管"检查什么"，本文件管"发现问题后怎么分类和裁决"。

## 一、问题标签（7 类）

每发现一个 PRD 缺陷，必须附加以下标签之一：

| 标签 | 英文 | 定义 | 示例 |
|---|---|---|---|
| `[Contradiction]` | 矛盾 | 两处或多处陈述在逻辑上不可同时成立 | §3.1 说"不限制携伴人数"但 §4.2 BR-104 说"最多1位" |
| `[Gap]` | 缺口 | 关键信息缺失，影响可实现性或可测试性 | 主流程描述到"提交预约"结束，未说明提交失败怎么办 |
| `[Fallacy]` | 谬误 | 基于错误前提或不成立假设的推断 | "所有客人都会使用微信"—但可能有国际客人用WhatsApp |
| `[Redundancy]` | 冗余 | 同一信息在多处重复且不一致风险高 | BR-005 和 IX-014 描述了相同的二次确认逻辑但文案不同 |
| `[Dangling]` | 悬空 | 引用了不存在或未定义的对象 | AC-003 引用了 ST-008 (P1) 但 ST-008 不在 MVP 范围 |
| `[Overreach]` | 越界 | 超出 PRD 范围，定义了应由下游决定的实现细节 | 指定了具体的数据库表结构或 API endpoint 命名 |
| `[Unowned]` | 无主 | 缺少明确的负责人、审批人或决策者 | "性能应满足要求"—没有量化阈值也没有负责人确认 |
| `[CommercializationGap]` | 商业化缺口 | to B 商业化链路（引流→转化→留存→复购）断裂或合规缺口 | 付费流程未覆盖退款/对账；数据收集未获合规授权 |
| `[HarddownRule]` | 硬性降级 | 触发 9 条硬性降级项之一（合规红线/依赖不可控/成本倒挂/AI 为了 AI 等），方案不应推进 | 涉及跨境数据但无合规授权路径；依赖供应商无替代且关键路径 |
| `[P0P1P2Misgraded]` | 优先级定级错误 | P0/P1/P2 优先级标注与"是否可定义/是否阻断"不符 | P0 功能无法定义验收或非核心路径；P1 实际为 P0 核心 |
| `[QualityGate]` | 质量门缺失 | 未通过启动/执行/交付任一质量门（Q-Gate）即推进下游 | 需求未确认即进入研发；交付无验收证据 |
| `[ScoreMatrix]` | 评分矩阵不达标 | 0-40 评分 4 维（问题接地/需求可测/指标严谨/范围风险诚实）任一分项低于阈值 | 需求不可测（无判据）；指标不严谨（无基线） |
| `[AntiPattern]` | 反模式 | 命中已知反模式（老板意见直写需求/只写功能不写用户价值/背景模糊/验收不可测/只写正常不写异常/优先级伪精确/指标只看增长/发布说明只写技术等） | PRD 只描述功能清单，未说明用户价值与异常场景 |

## 二、裁决级别（3 级）

审查完成后，每条发现必须有裁决：

| 裁决 | 含义 | 后续动作 |
|---|---|---|
| **APPROVED** | 无阻断性问题，可以确认 | 产物状态可变为 `confirmed` |
| **CONDITIONS** | 有非阻断性问题，需在指定时间内修复但不阻止确认 | 列出 conditions 清单 + 修复期限；确认后可推进但条件未满足前下游标记 `conditional_review` |
| **REVISION** | 有阻断性问题，必须修改后重新审查 | 产物打回 `draft` → 修改 → 重新 Audit → 重新 Human Gate |

## 三、裁决绑定

每条裁决必须记录：

```yaml
- tag: "[Gap]"
  location: "§5 FL-001 主流程"
  description: "未描述网络超时场景的恢复路径"
  severity: CRITICAL  # CRITICAL / HIGH / MEDIUM / LOW
  verdict: REVISION
  reviewer: "评审人姓名"
  reviewed_at: "YYYY-MM-DD"
  deadline: "2026-08-14"  # CONDITIONS 时必填
```

## 四、裁决流程图

```text
发现问题 → 贴标签 → 判断严重程度
  ├── CRITICAL → 必须 REVISION（阻断确认）
  ├── HIGH → 通常 REVISION（除非 reviewer 显式 waiver）
  ├── MEDIUM → CONDITIONS 或 REVISION（reviewer 判断）
  └── LOW → CONDITIONS（记录但不阻断）

全部 REVISION 类问题解决后 → 重新 Audit → Human Gate
全部 CONDITIONS 类问题记录后 → APPROVED（附条件清单）
无问题 → APPROVED
```

## 五、与现有闸门的集成

- `prd-assembly/references/audit-checklist.md` → 检查项分类引用本分类法的标签
- `prd-assembly/scripts/validate_artifact.py` → 检查审查记录中是否包含分类法标签
- `pipeline.py review` → 当 verdict 为 REVISION 时返回 nonzero；CONDITIONS 时输出条件清单
- `src/shared/human-gate/` → 三次连续 REVISION → 方向评审；十次累计 → 升级
