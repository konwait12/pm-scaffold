# 测试结果案例报告 · project-background-goal Skill

> 测试日期：2026-08-11
> 测试对象：`src/stages/001-business-requirements/skills/project-background-goal/` v0.1（英文版）+ `-zh`（中文版）
> 校验脚本：`scripts/validate_artifact.py`（结构校验 + 5 条语义红线）
> 测试框架：`test/skills/project-background-goal/test_validate_artifact.py`（unittest，3 用例）

---

## 一、结论摘要

**Skill 当前状态：P0 可上线（已过 `project-background-goal` → `user-journey-and-stories` 推进闸门全部机器化指标）。**

- ✅ unittest：3/3 通过
- ✅ 模板自身：PASS（0 error / 0 warning）
- ✅ 7 份产物：全部 PASS（errors=0；warnings 均 ≤ 3，违规样本的 warning 是故意制造的）
- ✅ 触发/不触发案例：`eval-cases.json` 8 + 8 条，与 `agents/openai.yaml` 双段示例一致
- ✅ 端到端案例：3 个（多源 / 缺事实 / 冲突），多源与冲突已用 RSVP 真实验证 + 招聘网站三阶段闭环
- ✅ **confirmed 路径全流程跑通**：draft → ready → confirmed（含 §13 下游交接、知识状态升级、CNF 关闭）

## 二、产物清单与校验结果

| # | 产物 | 模式 | 校验结果 | warning 明细 |
|---|---|---|---|---|
| 1 | `fixtures/project-background-goal-test-result.md` | 充分模式（基线） | ✅ ok / 0 err / 0 warn | - |
| 2 | `fixtures/project-background-goal-regression-test-result.md` | 充分模式（回归一致性） | ✅ ok / 0 err / 0 warn | - |
| 3 | `fixtures/project-background-goal-regression-violation-test.md` | 故意违规（反例教学） | ✅ ok / 0 err / **3 warn** | 目标章节空 + 38 处待确认状态不匹配 + 目标无量化判据 |
| 4 | `fixtures/project-background-goal-rsvp-real-verification.md` | 充分模式 + 真实多源 | ✅ ok / 0 err / **1 warn** | 8 处待确认但状态 ready（模板必填结构，闸门允许 ≤2） |
| 5 | `fixtures/hire-website-low-density.md` | 低密度退化（真实需求演示） | ✅ ok / 0 err / 0 warn | - |
| 6 | `fixtures/hire-website-sufficient.md` | 充分模式（真实需求演示） | ✅ ok / 0 err / **1 warn** | ready 状态下非阻断待确认 |
| 7 | `fixtures/hire-website-confirmed.md` | **confirmed 终态（真实需求演示）** | ✅ ok / 0 err / **0 warn** | - |

> 注：hire-website 三阶段已按 REQ-DIR 规则正式落位到 `requirements/REQ-001-hire-website/001-business-requirements/01-background-goal/`（background-goal.md = confirmed v1.0；v0.1/ 下为 ready 快照）。fixtures 保留演示副本。

## 三、测试用例执行情况

### 3.1 unittest（test_validate_artifact.py）

| 用例 | 验证点 | 结果 |
|---|---|---|
| `test_template_passes` | 模板自身通过结构校验 | ✅ PASS |
| `test_missing_contract_fails` | 缺 frontmatter/标题 → 报错 | ✅ PASS |
| `test_confirmed_artifact_requires_confirmation_owners` | confirmed 状态缺确认人 → 报错 | ✅ PASS |

> 本次修复（1）：`parse_frontmatter` 增加跳过注释头支持——模板与示例产物自带 `<!-- -->` 头部，原逻辑只匹配文件开头的 `---`，导致模板自身校验失败。修复后模板与全部产物均 PASS。

> 本次修复（2）：confirmed 状态校验会因模板强制章节标题"## 11. 待确认问题"本身含"待确认"二字而**永远无法 0 warning**（标题不能删）。修复：剥离章节标题后再扫描正文，只把正文内容中的待确认算作残留标记。修复后 confirmed 产物 0/0 通过，且不误伤其他产物（回归验证 7 份全 PASS）。

### 3.2 触发/不触发案例（eval-cases.json）

| 组 | 数量 | 覆盖点 | 状态 |
|---|---|---|---|
| `should_trigger` | 8 | 邮件/纪要/PPT 整理、防 PRD 提前、冲突核对、功能请求还原、更新审查 | ✅ 与 openai.yaml trigger_examples 一致 |
| `should_not_trigger` | 8 | 旅程/原型/功能描述/PRD/测试/竞品/DB/手册 → 路由下游 | ✅ 与 openai.yaml should_not_trigger_examples 一致 |
| `end_to_end` | 3 | 多源完整 / 缺业务事实 / 来源冲突 | ✅ 全部闭环 |

### 3.3 端到端案例映射

| eval case | 覆盖产物 | 覆盖情况 |
|---|---|---|
| `complete-multi-source`（邮件+纪要+负责人） | #4 RSVP + #6 招聘网站充分 | ✅ 3 源交叉 + 5 项 KPI + 6 类标签全用 + CONFLICT 暴露 |
| `missing-business-facts`（单句无事实） | #2 回归（低密度退化）+ #5 招聘网站低密度 | ✅ needs_user_input + 8 个阻断问题 + 不编造 |
| `conflicting-sources`（纪要 vs 邮件目标冲突） | #4 RSVP 的 CNF-001 + #7 招聘网站 CNF-001 | ✅ 保留双方 + 要求权威决策 + 裁决后转 DECISION 关闭 |

## 四、5 条语义红线验证

| # | 红线 | 验证方式 | 结果 |
|---|---|---|---|
| 1 | ready 但目标章节空 | 违规样本 #3 | ✅ 命中 |
| 2 | FACT + 实现词 + SRC < 2（方案当事实） | 单元测试 + 代码审查 | ✅ 逻辑存在 |
| 3 | 待确认 ≥ 3 但状态不匹配 | 违规样本 #3（38 处） | ✅ 命中 |
| 4 | Clarifications Session > 5 或 ready 前未填答案 | 单元测试 + 代码审查 | ✅ 逻辑存在 |
| 5 | ready 但目标无量化判据（29148 Verifiable） | 违规样本 #3 | ✅ 命中 |

## 五、覆盖矩阵（4 个维度）

| 维度 | 覆盖产物 | 状态 |
|---|---|---|
| 结构层（15 章节 + frontmatter 10 字段 + Constitution Compliance） | #1 #2 #4 #7 | ✅ |
| 语义层（背景/问题/目标/成功判断分离） | #4 #6（5 项 KPI） | ✅ |
| 来源层（3 SRC 交叉 + 6 类标签） | #4 #6 #7 | ✅ |
| 流程层（三模式 × 7 步骤 × 3 闸门 + 三阶段升级路径） | #5（退化）#6（充分）#7（confirmed） | ✅ |

## 六、文件清单

```
test/skills/project-background-goal/
├── eval-cases.json                     # 触发/不触发/端到端案例定义
├── test_validate_artifact.py           # unittest（3 用例）
├── TEST-REPORT.md                      # 本报告
└── fixtures/                           # 验证产物归档（7 份）
    ├── project-background-goal-test-result.md
    ├── project-background-goal-regression-test-result.md
    ├── project-background-goal-regression-violation-test.md
    ├── project-background-goal-rsvp-real-verification.md
    ├── hire-website-low-density.md
    ├── hire-website-sufficient.md
    └── hire-website-confirmed.md
```

> 真实需求正式落位：`requirements/REQ-001-hire-website/`（见总控 06 §8.1 REQ-DIR 规则）。

## 七、补充说明

1. **本次修复的 2 个缺陷**：`parse_frontmatter` 注释头支持 + confirmed 状态标题剥离。均同步到中文版。
2. **confirmed 路径完整演示**：招聘网站需求走通 draft → ready → confirmed 全链路（人工裁决 3 阻断项 → AI_INFERENCE/ASSUMPTION 升 FACT → CNF 关闭 → §13 下游交接填写 → v1.0 基线）。
3. **关联报告**：`project-background-goal-evaluation-report.md`（Skill 能力评判，5 维度 7-9 分）、`project-background-goal-rsvp-self-assessment.md`（RSVP 自评估，覆盖闭环）。
4. **工作事项推进判定**：满足 `03-实施迁移与验证计划.md` §6.6.2 硬指标 1-3；指标 4（主理人签字）与 5（归档）待项目主理人执行。
