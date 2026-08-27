# L0/L1 产品能力质量矩阵

## 结论

本矩阵把经过评估的产品能力落到本项目的产物和校验规则中：证据分层、用户研究合成、范围谈判、方案评估、反向质疑、失败恢复与可判定验收。矩阵描述的是能力要求，不是外部工具依赖。

| 对标方向 | 索引候选 | 当前项目原有基础 | 本次落点 | 档位 |
|---|---|---|---|---|
| PRD 深度与增量协作 | `prd-generator`、`prd-writer`、`incremental-prd-collaboration` | canonical PRD、mini-prd、Clarifications | 统一质量增强记录、替代方案、停止条件和证据来源 | L0 必须，L1 结构化 |
| 反向质疑 | `prd-reviewer`、`pm-chief-naysayer` | reviewer checklist、anti-patterns | 可证伪条件/停止条件，禁止只给通过结论 | L0 必须，L1 评审 |
| 用户研究与合成 | `user-research`、`research-synthesis` | user-journey 的角色/阶段/痛点/机会 | 事实账本、痛点→机会→故事覆盖，未知不补写 | L1 |
| 竞品与方案评估 | `competitive-analysis`、`product-analysis-zh` | competitive-research 按需分支 | 采用方案/被排除替代及价值-成本-风险记录 | L0/L1 按需 |
| 原型与 UX | `prd-to-prototype`、`ui-ux-pro-max` | page-design、interaction-rules | 仅在存在页面/交互事实时触发，不能用 UI 代替需求证据 | L1→L2 |
| 工程可执行 PRD | `prd-development` | functional-flow、business-rules、AC | 每项功能都要有边界、异常、来源和可测试验收 | L1 |

## 验收

1. 新 L0 产物必须有真实证据、用户影响、替代方案、失败边界、回退、可证伪条件和验收。
2. 新 L1 产物必须在事实/决定/假设账本中记录取舍，并使旅程→故事→功能→流程→规则→验收链可逆追溯。
3. 缺少依据时进入 `needs_user_input` 或升级，不以空泛文字通过。
