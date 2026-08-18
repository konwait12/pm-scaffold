# 可视化伴随 · Brainstorming（可选 Viz Companion）

本文件定义发散收敛阶段**可选**的可视化呈现方法。它是**纯增强、不阻塞主流程**：viz 只帮助人理解候选结构与处置关系，viz 缺席不影响发散、收敛、写回任何一步的正常完成。

## 何时使用（When）

| 场景 | 是否建议 |
|---|---|
| **全景发散**（跨模块 / 多系统 / 多角色，候选量大） | 建议——分模块/系统/角色的发散难以用一张表装下 |
| **Human Gate 呈现**（向 business_owner 展示候选与处置） | 建议——可视化辅助处置判断 |
| 标准发散、候选量小 | 可选/不必 |
| 轻量澄清 | 不必要 |

判定规则：**只有偏"全景发散"或"处置呈现"时才选用**；SKILL.md 的 Load References 表已标注该用法的可选属性。

## 怎么做（How）

- 用**自包含 HTML/SVG**（`data-dynamic-ui-widget`），不依赖外部库；若无展示环境则退化为 markdown 表，结果保持一致。
- 只呈现两者之一或两者：**发散全景图**（12 维度 → 候选 SCN-XXX 的分布）、**处置视图**（include/exclude/defer/research 四簇 + 写回目标）。

### 建议载体

- **发散全景图**：12 维度作为分组（lifecycle / roles / … / constraint），每个 `SCN-XXX` 作为该组下的小卡片；标出 Evidence 强弱或影响提示。
- **处置视图**：按 `include / exclude / defer / research` 四列分栏，候选落入对应栏；`include` 项标注 Write-back Target。
- 颜色仅作辅助区分，不承担唯一语义；弱视亦可见（文字+图标双通道）。

## 纪律（Discipline）

- **不阻塞**：viz 失败/缺失 → 退化为 markdown 表继续，绝不因 viz block 主流程。
- **不引入新事实**：viz 只复刻已在 `brainstorming-output.md` 中的候选/处置/证据，不新增或改判候选。
- **不写回**：viz 产物是呈现层，不进入 `brainstorming-output.md`、不入 PRD、不参与哈希绑定。
- **处置仍靠人工**：viz 只漂亮地展示，Human Gate 的 `stop and wait` 纪律不变。