# 测试资产与差异归因规则（tests/）

> 本目录是 skill 仓库的回归测试资产：原材料引用、产物副本或占位 fixture、BRD 对比结论、验收记录。`tests/README.md` 是测试流程的总入口，固化差异归因规则——避免每次评审重复越界归因。

## 1. 差异归因五步决策树

测试流程中，对比发现的任何**缺失**（skill 产物 vs BRD vs 实际预期），必须先按以下五步归因：

```
① 缺失属于本 skill 的 output-contract（references/output-contract.md）？
   ├─ 是 → 本 skill 缺陷，登记到缺陷清单
   └─ 否 ↓
② 缺失属于下游 skill 的 output-contract？
   ├─ 是 → 下游缺陷，回执下游 owner；本轮不修
   └─ 否 ↓
③ 缺失属于流程外（PM 决策 / BRD 范围 / 实施期变更 / 项目管理 / 跨团队协调）？
   ├─ 是 → 流程外，回执对应 owner；本轮不修
   └─ 否 ↓
④ 产物是否已把该缺失正确登记为 TBC / 澄清问题（材料不足时的标准登记）？
   ├─ 是 → 【非缺陷，是 skill 的正确行为】——登记为「已识别并正确登记」观察项
   └─ 否 ↓
⑤ 全不属于？
   └─ 测试观察，待 PM 评审，不计缺陷
```

### 第④步的两轮实测依据

- background-goal 轮曾把 3 项下游职责（CN DP Services 15 条服务能力清单 / User Story 编号体系 / BRD 范围一致性核对）误记为 skill 缺陷；按①②③归因后撤回。
- user-journey 轮的 RSVP 实测中，「后台取消预约后主客侧无通知」「D-7 行程单改版后去留」等材料未定义项，产物按 TBC + 澄清问题登记——第④步验证为正确行为，非缺陷。
- 第④步避免了「材料不足 + 登记正确 = 误判为缺陷」的误归因。

### 决策树的不可绕过性

- 对比发现任何缺失 → 必须先过决策树 → 不能跳过①②③直接计入缺陷清单
- 归因不清的记「测试观察」→ 不计缺陷 → 不写进「缺陷清单」
- 评审收到的外部意见也必须过这张表 → 否则可能把「顺手做了吧」的建议吸收成巨石模板（方案 scope 守卫的硬哲学）

## 2. DP 用例（第一回归基线）

### 用途

DP（Digital Passport）案例是 user-journey 与 background-goal 两个 skill 的首轮实测基准：原始材料两份（Client journey PPT 45 页 + IT Intake PPT 32 页），跑通 skill 全部 8 步流程，产出主文档 + 治理伴随文件，与 DP BRD 对应章节对标。

### 资产位置

| 资产 | 位置 | 备注 |
|---|---|---|
| **原材料** | 飞书云盘「产品组项目资料汇总」表内 | Client journey + IT Intake 各一份 |
| **产物主文档 + 治理**（BG / UJ） | 飞书云盘（链接见方案 W6） | 不在本仓库——飞书云盘版本管控与本地 skill 演进独立 |
| **本地占位 fixture** | `fixtures/uj-round1-regression-confirmed.md` + `.governance.md` | 脱敏占位（X-BRAND / 客户A / 系统X 等），仅用于结构验证；待替换为真实 DP 用例副本 |
| **BRD 对标基准** | 飞书 docx（方案 W6 链接） | DP BRD |
| **验收记录** | 飞书方案 W6 节 + UJ-DP-001 治理文件「AI Audit」段 | 含校验器跑通记录、advisory 警告、缺失归因结论 |

### 跑测流程

```bash
# 1. 获取原文（执行人按 tests/fixtures/SOURCES.md 清单）
lark-cli docs +fetch --doc <doc-id> --doc-format markdown --scope full --format pretty > /tmp/uj-test-raw.md

# 2. 喂入 skill（按 SKILL.md §1-§8 流程）
# 输出 user-journey.md + user-journey.governance.md 至 /tmp/uj-test/

# 3. 跑校验器
python3 scripts/validate_artifact.py /tmp/uj-test/user-journey.md --json

# 4. 与 BRD 对应章节对标，按差异归因决策树走完 5 步
#    任何缺失先过决策树再计入缺陷清单
```

## 3. RSVP 用例（第二回归基线，9/3 已实测）

### 用途

RSVP（CHANEL FSN 线下活动邀约）案例是 user-journey 与 background-goal 的第二轮实测基准：形态刻意与 DP 不同（数据表 / 文档 / 议题表，非 PPT），项目类型为重构（vs DP 的从 0 到 1）。

### 资产位置

| 资产 | 位置 | 备注 |
|---|---|---|
| **原材料** | 飞书云盘「产品组项目资料汇总」表内 | 25K Event RSVP Recap（Sheets）+ FSN RSVP 运营文档（docx）+ RSVP AS-IS 梳理（docx）+ RSVP H5→MP Impact Issues（Sheets） |
| **产物主文档 + 治理**（BG / UJ） | 飞书云盘（链接见方案 W6） | BG-RSVP-001 + UJ-RSVP-001 + 各自治理文件 |
| **W7 测试报告** | 飞书云盘 | 含 11 条 skill 缺陷 + 5 类归因 + 五步决策树验证 |
| **BRD 对标基准** | 飞书 docx RSVP BRD V1.8（9 个 User Story + 8 轮变更日志） | 含服务号推送规则、入口生命周期变更 |
| **验收记录** | 飞书方案第 7 节 + W7 测试报告 | 含校验器跑通记录（零 CRITICAL）、11 条缺陷归入 W9 |

### 跑测结论（已固化）

- 11 条 skill 本体缺陷 → 全部归入 W9（护栏体系扩展 ⑥-⑬）
- 1 条材料冲突（TKU 推送规则 BRD vs 运营文档） → 回执 BRD owner（W8）
- 2 条材料缺口 → 第④步验证为正确行为，非缺陷
- 5 条符合现状 → 不计缺陷
- 五条既有护栏无一被「PPT 专属假设」推翻——通用化方向在数据表 / 文档 / 议题表形态上成立

## 4. 维护

- 新用例：先写「原材料 + 产物引用 + BRD 对标 + 验收」四件套 → 按五步决策树归因 → 入本 README
- 失败用例：登记到缺陷清单，按 W1-W9 工作单分布实施修复
- 跨用例规律：通用规则沉淀到护栏（`references/journey-extraction-guardrails.md` / `references/audit-checklist.md` / `references/source-handling.md`），用例特有细节不写进规则
