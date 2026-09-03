# 跨 Skill 通用约定（Cross-cutting Conventions）

> 本目录收容两个 skill（project-background-goal / user-journey）共享的工程化约定，避免在每个 SKILL.md 重复维护。任何新规则先在本目录沉淀，半年后无争议的再考虑下沉到具体 SKILL.md。

## 1. 跨 skill 版本协同（盲区 1）

### 现状

两个 skill 各自独立版本号：UJ 当前 v1.8、BG 当前 v1.3。两个 skill 的衔接点（P0-2 用户故事种子、P1-4 上游主张回链、跨 skill lite 传导）共享上下文——若版本不匹配，下游可能因上游字段缺失而推断暴涨。

### 规则

- **minor 版本必须配对演进**：UJ `v1.x` ↔ BG `v1.x`，pipeline 启动时校验 `user-journey.md` 的 `upstream_artifact_id` 与 `BG-XXX` 主文档 `artifact_id` 同版本（minor 一致）
- **major 版本独立**：skill 重大重构（API/模板结构变更）允许 major 跨版本，但必须在 CHANGELOG 写明与上游的兼容矩阵
- **跨 skill 校验器（advisory）**：UJ validator 增加 `uj.upstream_version_sync` 检查，BG validator 增加 `bg.downstream_aware` 检查，校验上游/下游主文档版本号一致；不匹配发 advisory warning，不阻断

### 落地步骤

1. 当前 BG/UJ 各自 v1.x，校验器默认值匹配（无需立刻校验）
2. 下一轮任何一边的 minor 升版（v1.4 / v1.9）必须同步另一边
3. 引入 CHANGELOG.md（每个 skill 一份），记录 minor 升版的兼容性

## 2. 测试用例失败回收策略（盲区 2）

### 三级分类

| 类别 | 触发条件 | 处理 |
|---|---|---|
| **校验类（CRITICAL）** | `validate_artifact.py` 报错（`uj.*_missing` / `uj.*_mismatch` 等结构性失败） | **阻断交付**：必须修复后重跑 |
| **内容类（MEDIUM/advisory）** | fixture 对照预期要点清单缺失；ST-ID 格式不规范；入口对比视图未生成等 | **告警 + 标注差异**，不阻断：CI 输出 advisory warning，记录到 `tests/results/<date>-advisory.log` |
| **性能类（MEDIUM/advisory）** | 产物行数 / 表格密度 / 章节分布等回归 | **告警 + 趋势图**：连续 3 次同向偏离则升级为内容类告警 |

### 阈值（建议初始值，可调整）

- **内容类**缺失占比 > 20% → 升级为校验类（阻断）
- **性能类**产物行数偏离基线 ±30% → 告警
- **性能类**产物行数偏离基线 ±50% → 升级为内容类

### 落地步骤

1. 在 SKILL.md §5 Generate 末尾加本节摘要（指向本 reference）
2. `tests/results/` 目录预留为 advisory 输出位置（不强制实现）
3. 第一次跑测即建立基线（基线本身作为 advisory 校对基准）

## 3. lite 模式与下游链路的传导（盲区 3）

### 现状

BG 的 lite 模式裁剪了大量节（项目背景 / 角色与干系人 / 约束与依赖 / 边界与非目标）。下游 skill（UJ / user-stories / page-design / business-rules / interaction-rules / validation-rules / feasibility-analysis / feature-list）的必填字段可能因上游字段缺失而出现「未知」或「待确认」暴涨——尤其当 PM 选 lite 后未在主文档登记裁剪理由时。

### 规则

- **BG governance 强制 lite 出口检查**：BG validator 在主文档 `status == ready_for_human_review` 时检查 governance 的「下游依赖清单」段是否填写；未填写则发 advisory warning（`bg.lite_export_unfilled`）
- **下游 skill 优先走澄清**：UJ / user-stories 等下游 skill 在 Generate 阶段，若检测到上游 BG 是 lite 模式 + 必填字段缺失，先在「澄清记录」段登记缺失项并向 PM 提问，**不允许默认推断**
- **下游校验器新增（advisory）**：UJ validator 检查 governance 的「上游依赖说明」段是否登记 BG lite 裁剪影响；未登记发 `uj.upstream_lite_aware` advisory

### 落地步骤

1. BG governance 模板已预留「下游依赖清单」段（P0-3 已落地），本约定仅作为执行规范说明
2. 下次 UJ validator 增加 lite-aware 检查时引用本节
3. 真正实现时再做一轮回归，确认 lite 模式产物能正常被下游 UJ / user-stories 消费

## 4. 三约定的执行优先级

```
冲突时优先级：
1. 「AI 不得伪造人工确认」(skill 架构红线) — 最高
2. 「只认本次原始材料」(skill 边界) — 次高
3. 本目录三条约定 — 普通
```

普通规则不应与红线和边界冲突；若发现冲突，立即反馈给 skill owner。

## 5. 维护

- 本目录由两个 skill owner 共同维护；任何新增约定需评审后才入库
- 半年无争议的约定考虑下沉到具体 SKILL.md
- 反之，争议多的约定在本目录留更长时间以便讨论
