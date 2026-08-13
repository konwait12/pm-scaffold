# Output Contract · ux-flow

本子 Skill 产出父级 `product-ux.md` 的 **§3.1 主流程（P0）+ §3.2 分支与状态**（隶属 `## 3. UX 流程与交互规则（Structural 层）`）。不产出独立产物；所有内容直接写入父产物对应章节。

## ID 契约

| ID 类型 | 格式 | 规则 |
|---|---|---|
| 功能 | `FEA-XXX` | 每个流程图必须归属一个父产物 §2 已登记的 FEA；不得引入 §2 之外的孤儿功能 |
| 故事 | `ST-XXX` | 每张图的步骤必须可回溯到已确认的用户故事；无法回溯的步骤标 `AI_INFERENCE` |
| 步骤 | `FL-XXX`（图内节点） | 图内步骤/状态节点可编号，命名与 §4 页面清单、故事原文一致，不自造术语 |
| 冲突 | `CONFLICT-XXX` | 上游范围与图面表达矛盾时显式保留，交人工裁决 |

## Artifact States

| Status | Meaning | Downstream use |
|---|---|---|
| `draft` | 初始候选；Audit 未完成 | No |
| `needs_user_input` | 某入口/步骤/分支/状态的事实或决定阻断确认 | No |
| `conditional_review` | 结构可评审，剩余未知非阻断且有责任人 | No |
| `ready_for_human_review` | 自审通过，等待授权评审 | No |
| `confirmed` | 授权人工明确批准此版本 | Yes |
| `superseded` | 更新的已确认基线替代本版本 | No |

## Version Rules

- 起始候选 `v0.1`；人工要求修订递增小版本 `v0.2`、`v0.3`。
- 首次确认基线用 `v1.0`；已确认基线变更按影响递增 patch/minor。
- 保留人工可见版本之间的简明变更摘要，不保留每次内部自审迭代。

## Knowledge-State Labels

| Label | Definition |
|---|---|
| `FACT` | 上游故事/已确认范围中的显式步骤或分支 |
| `DECISION` | 授权人工关于入口/分支/出口的明确决定 |
| `ASSUMPTION` | 为画图接受但未确认的临时条件 |
| `AI_INFERENCE` | AI 为使图完整而补的结构推断（有证据但非业务事实） |
| `UNKNOWN` | 缺失信息（如空态/超时行为尚未确认） |
| `CONFLICT` | 上游来源与图面表达不一致，需人工裁决 |

## Required Section Content

父产物 `## 3. UX 流程与交互规则` 下：

- `### 3.1 主流程（P0）`：每个 P0 FEA ≥1 张 Mermaid 图，覆盖入口 → 步骤 → 决策 → 出口。
- `### 3.2 分支与状态`：以文本/表列出分支条件、error/empty/loading/timeout/cancel/recovery 状态与回退目标。

若某 FEA 无确认流程内容，写 `待确认` 并关联问题/未知 ID；**不删除标题、不跳过 FEA**。

## Downstream Handoff

向 page-design 与 interaction-rules 传递：

```text
confirmed_version
per_fea_flow_summary      # 每 FEA：入口、步骤、分支、出口
branch_conditions         # 每条分支的判定条件（供 IX 引用）
state_inventory           # error/empty/loading/timeout 状态清单
handoff_points            # 跨系统交接与失败回退
ai_inferred_steps         # 所有 AI_INFERENCE 步骤清单
open_nonblocking_unknowns
source_ids                # ST-XXX / FEA-XXX / SRC-*
```

不要在本 Handoff 中创建页面骨架或交互规则。

## Clarifications Session Contract

沿用父产物 `## Clarifications` 表，一行一个 Session（`CL-NNN`），字段与父级一致。`reflow_target` 必须指向本子 Skill 影响的章节（`§3.1` / `§3.2`）。`audit_recheck` 为最后填写字段；若 `fail`，状态回退 `needs_user_input` 并开新一轮 Session。
