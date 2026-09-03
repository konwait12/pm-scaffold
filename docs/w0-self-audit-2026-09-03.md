# W0 历史 commit 通用性自查（2026-09-03）

> 对照方案 W0「历史 commit 通用性审计」自查我之前推过的 commit，逐条问「这条规则是否形态无关」。

## 审查范围

- **UJ 仓库**：65895b4 之后的 5 个 commit
- **BG 仓库**：9713c38 之后的 3 个 commit

## 逐条审查

### UJ `076ff38` — P0-3 lite + P0-4 default board

- `templates/user-journey.md`：frontmatter 改"可选审阅板"→"默认审阅板"，指向 SKILL.md §5 触发条件
- `SKILL.md` §5 Generate：新增「HTML 审阅板触发条件」段——UJ 默认 / BG 按需
- 触发条件：「角色数 ≥ 2 / 阶段数 ≥ 3 / 路径类型 ≥ 2」——纯数量判断，无具体枚举

**形态无关判断**：✅ **保留**（无个案细节）。

### UJ `af1b1ca` — P1-1 三层枚举协议

- `references/touchpoint-catalog.md`：18 个标准触点（SMS_3RD_PARTY / EMAIL_TRANS / PUSH_OS / WE_COM_ROBOT / INAPP_RED_DOT / ...）
- `references/channel-catalog.md`：三维度分类（Side / Delivery / Latency）
- `references/interaction-catalog.md`：7 大类交互（reminder_ / share_ / login_ / payment_ / subscribe_ / favorite_ / review_ / confirm_）
- `references/touchpoint-coverage-matrix.md`：交互 × 触点组合矩阵

**形态无关判断**：⚠️ **有具体枚举值**，但属于行业标准技术枚举（非个案）：
- 触点 ID（SMS_3RD_PARTY 等）是技术通用名词，不是 CHANEL / DP / 微信等个案
- 交互 ID（reminder_appointment 等）是业务动作通用名
- 渠道维度（Side/Delivery/Latency）是方法论框架

**处置**：✅ **保留**——P1-1 协议的设计意图就是提供标准枚举清单，枚举是协议能力的一部分，不是写死的个案细节。若 PM 评审后要求改抽象化（如改成"外部/内部/社交"分类而非具体 ID），再调整。

### UJ `272b415` — P0-2 种子 + P0-1 tests/ skeleton

- `templates/user-journey.md` 产品层展开子块新增第 5 项「用户故事种子」
- `validate_artifact.py` 新增 advisory 检查 `uj.seed_missing` + `uj.seed_id_format`
- `tests/fixtures/SOURCES.md`：仅清单不存原文
- `tests/fixtures/uj-round1-regression-confirmed.md`：含 X-BRAND / 客户A / 系统X / TKU 等具体名称
- `tests/fixtures/uj-round1-regression-confirmed.governance.md`：治理伴随

**形态无关判断**：✅ **保留**：
- templates / validate / SOURCES.md 形态无关
- fixture 含 X-BRAND 等是合理的——fixture 本身需要具体数据来跑回归测试；DP 真实业务数据在飞书云盘，fixture 用脱敏占位（X-BRAND）作为占位，符合 P0-1 修订 1 的脱敏原则
- **注意**：fixture 是占位（待替换为真实 DP 脱敏版），已在 `uj-round1-regression-confirmed.md` frontmatter 的 governance 与 SOURCES.md 注明

### UJ `7bca482` — P1-2 入口对比视图 + 盲区 1+2+3

- `templates/user-journey.md` 产品层展开子块新增第 6 项「入口对比视图（按需生成）」
- `validate_artifact.py` 新增 advisory 检查 `uj.entry_catalog_missing` + `uj.comparison_view_suggested`
- `references/cross-cutting-conventions.md`（双 skill 共享）：版本协同 / 测试失败回收 / lite 链路传导

**形态无关判断**：✅ **保留**——触发条件是「清单中任一用户目的有 ≥ 2 个入口」，纯结构判断；references 是工程化约定不绑具体平台。

### UJ `0b3cc30` — anti-bloat

- `references/anti-bloat-conventions.md`：空骨架红线（密度 > 30%）/ 业务假设链 / 产物分级（仅规划）
- `validate_artifact.py` 新增 `uj.bloat_warning`

**形态无关判断**：✅ **保留**——纯结构密度判断，不涉及具体业务。

### BG `4889b0c` — P0-3 lite 注释化

- `templates/background-goal.md`：11 节用 HTML 注释标记「迭代」可裁剪
- `templates/background-goal.governance.md`：分级 + 下游依赖清单段
- `SKILL.md` 第 2 步加项目级会议基线（可选）说明

**形态无关判断**：✅ **保留**——按类型（重构 / 从 0 到 1 / 迭代）分支，不绑具体业务。

### BG `fae72aa` — 盲区 1+2+3

- `references/cross-cutting-conventions.md`（与 UJ 共享同一份内容）

**形态无关判断**：✅ **保留**——工程化约定。

### BG `ee9a4d3` — anti-bloat

- `references/anti-bloat-conventions.md`（与 UJ 共享）
- `validate_artifact.py` 新增 `bg.bloat_warning`

**形态无关判断**：✅ **保留**——纯结构密度判断。

## 自查总结

| 维度 | 命中情况 |
|---|---|
| 含具体枚举值的规则 | 1 处（P1-1 三层枚举协议）——但属于行业标准技术枚举，非个案细节，保留 |
| 含个案细节（CHANEL / DP / 微信等）写死进规则的 | 0 处 |
| 含具体客户/系统/平台名 | 0 处（fixture 中是脱敏占位 X-BRAND，符合规范） |
| tests fixture 含具体业务数据 | 1 处（`uj-round1-regression-confirmed.md`）—— 已脱敏 + frontmatter 标注占位状态 + SOURCES.md 注明待替换 |

**结论**：我之前推的 8 个 commit 全部通过 W0 自查——形态无关，无个案细节杂质。可作为后续 W1-W9 改动的基线。

**待跟进事项**（W6 入库时一并处理）：
1. `tests/fixtures/uj-round1-regression-confirmed.md` 当前为脱敏占位 fixture，W6 应替换为真实 DP 用例的脱敏副本（与 BG 实际产物对齐）；占位 fixture 可保留作为第二回归用例
2. fixture frontmatter 注明 `note: 占位 fixture，待 W6 替换或保留为第二回归用例`
