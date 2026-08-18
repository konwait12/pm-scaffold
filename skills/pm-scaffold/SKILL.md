---
name: pm-scaffold
description: PRD-only product manager AI scaffold. Convert raw requirements (BRDs, meeting notes, emails, PPTs) into structured, human-confirmed Chinese PRDs through a 3-stage registry-driven pipeline (13 work items + 3 branches + 1 resident + 2 capabilities).
version: 0.6.0
author: PM Scaffold
tags: [pm, prd, requirements, product-management, spec-driven, b2b]
---

# PM Scaffold · 产品 AI 脚手架

Convert raw requirement sources into a single, human-confirmed, traceable Chinese `prd.md` through a 3-stage, 13-work-item registry-driven pipeline (project-background-goal → user-journey → user-stories → feature-list → functional-flow → page-design → interaction-rules → business-rules → validation-rules → state-machine → exception-handling → acceptance-criteria → prd-assembly) with cryptographic confirmation invariants.

## Quick Start

```bash
# 1. Initialize a new requirement
python3 src/scripts/pipeline.py init REQ-005-my-feature

# 2. Add your source materials to requirements/REQ-005-my-feature/00-input/

# 3. Check status
python3 src/scripts/pipeline.py requirements/REQ-005-my-feature status

# 4. Work through each stage (AI follows SKILL.md for each Work Item)
#    Stage 1: project-background-goal → user-journey → user-stories
#    Stage 2: feature-list → functional-flow → page-design → interaction-rules
#             → business-rules → validation-rules → state-machine
#             → exception-handling → acceptance-criteria
#    Stage 3: prd-assembly

# 5. Run validators before human review
python3 src/scripts/pipeline.py requirements/REQ-005-my-feature gate --work-item project-background-goal
bash run_tests_mac.sh
```

## What It Does

- **13 Work Items** across 3 stages: business requirements → product requirements → PRD output
- **3 branch skills**: competitive-research（竞品调研）、feasibility-analysis（可行性分析）、tracking-plan（埋点计划）
- **1 resident skill**: issue-record（问题清单，跨阶段共享）
- **2 capability skills**: requirement-restate（需求复述）、brainstorming（发散收敛）
- **Shared thinking core**（`src/framework/thinking-core.md`）: §1 6 核心透镜必用 + §2 校验层透镜 + §3 发散决策层透镜 + §5 表达层技法注册
- **Non-bypassable human gates**: only `pipeline.py review --decision approve` with a real human reviewer can confirm artifacts
- **SHA-256 binding**: confirmed artifacts are cryptographically bound to their reviewer
- **Full traceability**: G→UJ→US→FEA→FL→PD→IX→BR→VL→SM→EX→AC forward and reverse traceability
- **84+ regression tests** with fixture-based validation, registry-contract gate (E3_drift) fail-loud first

## External Skill Essence Integration（2026-08, v0.6.0）

外部 PRD/PM skill 的精华按「A 思想层 / B 参考文档层 / C 审计层」注入既有 19 skill，不新增业务阶段、不触碰注册表/主干 8 步/模板 frontmatter/校验器：

- **A 档 · 思想层**（18 项）：thinking-core §2/§3/§5 新增透镜与技法登记（MRC 门禁、grill 对抗、反例扫描、预死亡分析、naysayer 三阶段、决策预注册、西瓜防御、溯源标注三级等）
- **B 档 · 参考文档层**（64 个技法文件）：各 skill `references/` 新增（14 维缺口扫描、7 维评分、RBAC 矩阵、UI 文案 5 原则 9 场景、研发评审 13 项、RICE 优先级、状态机完备性、埋点事件规范等），全部 ≥80 行且登记在 SKILL.md 加载表
- **C 档 · 审计层**（13 项）：review-taxonomy 12 标签（含 [CommercializationGap]/[HarddownRule]/[ScoreMatrix]/[AntiPattern] 等）+ 各 skill audit-checklist 追加

总注入点 95 个。实施依据：`docs/new-skills-integration-plan.md`（全量评估表 + 映射 + 里程碑）。

## Agent Entry Point

New AI agents: read `AGENTS.md` first for startup order, hard rules, and quick-start workflow.

**First contact with a new HUMAN user**: before explaining anything, open the cockpit for them (`open src/toolkit/visualization/scaffold-flow.html`) and point them to the 「📖 新手教程 · 从这里开始」 button in the left sidebar — that single self-contained HTML is the entire onboarding (flow diagram, 19-skill manual, command reference, file architecture, the two-round integration overview, and the 10-chapter human+agent collaboration tutorial). There is no external ecosystem; this file IS the front door.

## Key Files

| File | Purpose |
|---|---|
| `AGENTS.md` | AI agent runtime entry (startup order, hard rules) |
| `README.md` | Human-facing project overview |
| `src/framework/workflow-registry.json` | Single source of truth for all stages, skills, artifacts |
| `src/framework/thinking-core.md` | Shared thinking core（6 核心 + 校验层 + 发散决策层 + 表达层技法注册） |
| `src/framework/constitution.md` | 8 hard constitutional rules |
| `src/shared/audit/review-taxonomy.md` | 12-label PRD review classification |
| `docs/new-skills-integration-plan.md` | 外部 skill 评估表 + 95 注入点映射 + 里程碑 |

## Validation

```bash
bash run_tests_mac.sh                              # Full regression (84+ tests, registry contract first)
python3 src/scripts/consistency_check.py       # Cross-document drift check
python3 src/scripts/property_check.py <fd.md>  # Rule completeness properties
```

## Requirements

- Python 3.10+
- Git (for version control of artifacts)
- lark-cli (optional, for Feishu document integration)
