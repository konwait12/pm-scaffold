---
name: pm-scaffold
description: 面向产品经理的 PRD 工作流脚手架。将 BRD、会议纪要、邮件、PPT 等原始需求，通过注册表驱动的三阶段流程转为结构化、经人工确认、可追溯的中文 PRD。
version: 0.6.1
author: PM Scaffold
tags: [pm, prd, requirements, product-management, spec-driven, b2b]
---

# PM Scaffold · 产品 AI 脚手架

将原始需求来源转化为一份经人工确认且可追溯的中文 `prd.md`。流程按 `workflow-registry.json` 运行：L0 只有一个 mini-PRD，L1 有 7 个上游产物与最终 PRD 共 8 项，L2 执行 13 项完整链。所有确认都由哈希、评审记录和审计事件绑定。

## 快速开始

```bash
# 1. 创建需求并明确工序档位
python3 src/scripts/pipeline.py init REQ-005-my-feature --process-tier L2

# 2. 将原始材料放到 requirements/REQ-005-my-feature/00-input/

# 3. 查看当前档位和进度
python3 src/scripts/pipeline.py requirements/REQ-005-my-feature status

# 4. 按当前档位依次完成工作项；每项都遵循对应 SKILL.md

# 5. 人工评审前运行机器闸门与回归
python3 src/scripts/pipeline.py requirements/REQ-005-my-feature gate --work-item project-background-goal
bash run_tests_mac.sh
```

## 能力范围

- **分档主干**：L0 为 `mini-prd`；L1 为 8 项；L2 为业务需求、产品需求和 PRD 输出三阶段的 13 项完整链。
- **按需分支**：`competitive-research`（竞品调研）、`feasibility-analysis`（可行性分析）、`tracking-plan`（埋点计划）。
- **常驻治理**：L1/L2 使用 `issue-record` 记录 PM/PRD 过程中的澄清、冲突、风险、待决与范围问题；L0 的未决项写入 mini-PRD。
- **过程能力**：`requirement-restate`（需求复述）与 `brainstorming`（发散收敛）仅生成过程记录或输入包，默认不进入 PRD 正文。
- **共享思考核心**：`src/framework/thinking-core.md` 定义必须使用的核心透镜、校验层、发散决策层和表达技法。
- **不可绕过的人工闸门**：只有授权人工通过 `pipeline.py review --decision approve` 才能确认产物。
- **哈希绑定与可追溯**：确认版本与评审人绑定，L2 支持 G→UJ→US→FEA→FL→PD→IX→BR→VL→SM→EX→AC 正反向追溯。
- **注册表驱动回归**：fixture 校验与注册表契约闸门优先失败；测试数量以当前执行结果为准。

## 外部方法的定制化吸收

外部 PRD/PM 方法以三类形式纳入项目：思考透镜、按需参考文件、审计清单。它们不得新增业务阶段、改变注册表主干、破坏模板 frontmatter 或替代人工决定。每项引用的来源与适用范围应以当前仓库和注册表为准，历史汇总数字不构成运行时承诺。

本项目额外定制了“交付复核”能力：将验收先行、验证证据、业务评审包、人工闸门和并行交叉审计纳入 PM 语境；它不把代码代理、Git worktree 或研发代码审查流程直接写入 PRD 主干。

## Agent 入口

新的 AI Agent 应先阅读 `AGENTS.md`，了解启动顺序、硬规则与分档工作流。首次面向使用者时，先打开驾驶舱：`open src/toolkit/visualization/scaffold-flow.html`，并引导其从左侧“新手教程 · 从这里开始”进入。该单文件驾驶舱包含流程图、Skill 手册、命令参考、目录结构和人机协作教程。

## 关键文件

| 文件 | 用途 |
|---|---|
| `AGENTS.md` | AI Agent 的启动顺序、硬规则与协作约定 |
| `README.md` | 面向使用者的项目总览 |
| `src/framework/workflow-registry.json` | 阶段、Skill 与产物的机器事实源 |
| `src/framework/thinking-core.md` | 共享思考核心与技法登记 |
| `src/framework/constitution.md` | 宪法级硬规则 |
| `src/framework/governance.md` | 人工闸门、档位和治理规则 |
| `src/support-skills/delivery-review/` | 定制化交付复核能力 |

## 验证

```bash
bash run_tests_mac.sh
python3 src/scripts/consistency_check.py
python3 src/scripts/property_check.py <fd.md>
```

## 运行要求

- Python 3.10+
- Git（用于产物版本控制）
- lark-cli（可选，用于飞书文档集成）
