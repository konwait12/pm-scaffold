# Nova：AI 产品经理 Agent 新项目计划（Agent 化大改造）

> 版本：v0.1（2026-08-14）
> 项目代号：**Nova**（AI 产品经理 Agent）
> 定位：**独立新项目**，与现有 PM Scaffold 脚手架不冲突。复用脚手架的产物规范、校验器、术语表，但引入 agent 运行时能力。
> 参考基准：DeepSeek Harness（dsh）、OpenAI Codex、Anthropic Claude Code 三家架构的深度搬运与参考。
> 调研日期：2026-08-14（dsh 于 2026-08-13 开源，MIT 协议）

---

## 0. 为什么做 Agent 化

现有 PM Scaffold 是「文档流水线 + 校验器」：AI 按固定阶段生成产物，每步有 gate 把关。它解决了「产物质量」问题，但没有解决「AI 如何自主工作」的问题——上下文管理、多轮澄清、子代理协作、权限门控、会话恢复都靠人工/外部环境。

Agent 化的目标：把脚手架变成**一个真正自主工作的 AI 产品经理**——它能自己澄清需求、自己调研、自己写 PRD、自己评审、自己迭代，全程可追溯、可审批、可恢复。

三家的核心启示：

| 来源 | 核心启示 |
|---|---|
| **dsh** | 一切皆插件（能力可组合可替换）；每次运行可追溯（append-only session log + "模型可见 ⟺ 已记录" 不变式） |
| **Codex** | 沙箱与审批分离（技术边界 vs 决策边界）；主线程纯净（子代理返回摘要防 context pollution）；指令分层（AGENTS.md 规则 vs Memories 记忆） |
| **Claude Code** | 模型自由决策 + 确定性 harness 强制（1.6% AI / 98.4% 基础设施）；5 层渐进压缩流水线；渐进信任谱系（permission modes）；hooks 确定性门控 |

---

## 1. 总体架构

```
┌─────────────────────────────────────────────────────────┐
│                    AI 产品经理 Agent                      │
│                                                         │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐            │
│  │ 需求澄清器 │  │  PRD 生成器 │  │  PRD 评审器 │  ← 子代理  │
│  │ Clarifier │  │  Writer   │  │ Reviewer  │            │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘            │
│        │              │              │                  │
│  ┌─────▼──────────────▼──────────────▼─────┐            │
│  │            Agent Loop（主循环）            │            │
│  │  gather → think → act → verify → repeat  │            │
│  └─────┬───────────────────────────┬────────┘            │
│        │                           │                     │
│  ┌─────▼─────┐              ┌──────▼──────┐             │
│  │ 上下文管理 │              │  权限门控     │             │
│  │ Compaction│              │ Permission  │             │
│  └─────┬─────┘              └──────┬──────┘             │
│        │                           │                     │
│  ┌─────▼───────────────────────────▼────────┐            │
│  │           Session Log（append-only）       │            │
│  │   模型可见 ⟺ 已记录（硬不变式）              │            │
│  └───────────────────────────────────────────┘            │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  复用 PM Scaffold：产物规范 / 校验器 / 术语表 / RACI │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**核心设计决策（搬运自三家）**：
1. **模型自由决策 + 确定性 harness 强制**（Claude Code）：需求澄清、PRD 生成、评审交给模型自由发挥；流程状态机、文档模板校验、权限门控、上下文管理用确定性代码实现。
2. **一切皆插件**（dsh）：模型适配器、工具、技能、会话、存储、子代理、UI 都是插件，可组合可替换。
3. **每次运行可追溯**（dsh）：append-only session log，模型看到的一切必须能从日志重建。
4. **主线程纯净**（Codex/Claude Code）：子代理返回摘要而非原始输出，防 context pollution/rot。

---

## 2. 核心子系统设计（逐项搬运）

### 2.1 Agent Loop（主循环）

**参考**：Claude Code 三阶段循环（gather context → take action → verify results → repeat）+ Codex Agent SDK 的 Runner 循环。

**PM Agent 的每轮流水线**（仿 Claude Code 9 步流水线）：

```
1. Settings resolution（解析配置：模型/权限/项目规范）
2. State init（加载会话状态、checkpoint）
3. Context assembly（组装上下文：项目规范 + 需求材料 + 历史决策 + 术语表）
4. Pre-model shaping（5 个上下文整形器，见 §2.2）
5. Model call（调用模型）
6. Tool dispatch（工具路由）
7. Permission gate（权限门控，见 §2.5）
8. Tool execution（执行工具）
9. Stop condition（停止条件：无工具调用 / 达到最大轮数 / 上下文溢出 / hook 干预 / 显式中止）
```

**PM 场景的停止条件**：
- 需求澄清完成（无更多待确认问题）
- PRD 生成完成且通过校验
- 评审通过（ReviewRecord 已写）
- 用户中断

### 2.2 上下文管理（PM 场景最值得抄的部分）

**参考**：Claude Code 5 层渐进压缩流水线 + Codex 的 ContextualUserFragment 约束。

**5 层渐进压缩**（按最便宜优先）：

| 层级 | 策略 | PM 场景对应 |
|---|---|---|
| Budget Reduction | 每条消息大小上限裁剪 | 长需求材料裁剪 |
| Snip | 裁剪较旧历史片段 | 早期澄清对话裁剪 |
| Microcompact | 缓存感知细粒度压缩 | 高频重复内容压缩 |
| Context Collapse | 读取时虚拟投影（非破坏性） | 大表格/长文档投影 |
| Auto-Compact | 全量模型生成摘要（最后手段） | 生成「需求决策摘要」保留关键约束 |

**硬约束（搬运 Codex AGENTS.md）**：
- 上下文必须增量构建，禁止重写历史
- 所有注入片段必须有界、有硬上限（单条 ≤ 10K tokens）
- 新增单条 >1K tokens 的项需额外审查
- 所有注入片段定义为 struct，实现统一接口

**PM 专用上下文片段**（ContextualUserFragment 的 PM 版）：
- 用户画像（Persona）
- 竞品摘要（CompetitorSummary）
- 历史决策（DecisionHistory）
- 术语表（Glossary）
- 需求材料（RequirementSource，按 SRC-* 引用）

### 2.3 记忆机制

**参考**：Codex Memories（脱敏、后台异步、rate-limit 感知）+ Claude Code Auto Memory（文件式、无向量库、可审计）。

**PM Agent 记忆内容**：
- 用户偏好（语言、风格、详略偏好）
- 产品线惯例（各业务线命名、术语、评审偏好）
- 历史 PRD 风格（作为生成参考）
- 已知坑（历史踩过的坑）

**设计决策**：
- 文件式存储（`~/.pm-agent/memory/`），无向量库、无 embedding，LLM 按头部扫描取回——完全可审计、可编辑、可版本控制（Claude Code 方案）
- 自动脱敏 secrets（Codex 方案）
- 后台异步更新，等线程空闲才总结（Codex 方案）
- **规则唯一来源是入库文档（AGENTS.md/CLAUDE.md），记忆只是 recall 层**（Codex 明确边界）

### 2.4 子代理系统（评审流程核心）

**参考**：Claude Code 内置 6 类子代理 + Sidechain transcripts 隔离 + Codex 自定义 agent 文件。

**PM Agent 内置角色子代理**：

| 子代理 | 职责 | 模型 | 工具 | 隔离 |
|---|---|---|---|---|
| `clarifier` | 需求澄清员：读材料、识别待确认信号、提问 | 旗舰 | 读文件、提问 | in-process |
| `researcher` | 竞品/行业研究员：联网调研 | mini | 读文件、web | worktree |
| `writer` | PRD 生成员：按模板写产物 | 旗舰 | 读文件、写文件 | in-process |
| `reviewer` | PRD 评审员：对照清单评审 | high reasoning | 读文件、跑校验器 | in-process |
| `verifier` | 验收标准验证员：逐条勾选 | mini | 读文件、跑校验器 | in-process |

**关键设计（搬运）**：
- **Sidechain transcripts**：每个子代理写独立 JSONL，**只有摘要返回父代理**，完整历史永不进入父上下文（Claude Code）
- **SkillTool vs AgentTool**：轻量规则（PRD 格式规范）用 Skill 注入当前上下文（便宜）；重量任务（深度竞品调研）用子代理隔离执行（贵，约 7 倍 token，但防上下文爆炸）
- **显式触发原则**（Codex）：默认单线程澄清，仅在用户要求或任务明确可并行时才派发子代理
- **自定义 agent 文件**（Codex）：`name / description / developer_instructions / model / reasoning_effort / sandbox_mode` 字段齐全

### 2.5 权限与审批（渐进信任谱系）

**参考**：Claude Code 7 种 permission modes + Codex 沙箱与审批分离 + 三层审批模型。

**PM Agent 的渐进信任谱系**（映射 Claude Code 的 Shift+Tab 模式）：

| 模式 | 行为 | 信任级别 | PM 场景 |
|---|---|---|---|
| `plan` | 只读，先出计划供审批 | 最低 | 需求澄清问题清单 / PRD 大纲 |
| `clarify` | 可提问、可读材料 | 低 | 需求澄清阶段 |
| `write` | 可写 PRD 文档 | 中 | PRD 生成阶段 |
| `review` | 可调用评审子代理 | 高 | 评审阶段 |
| `publish` | 可提交/推送/发飞书 | 最高 | 发布阶段 |

**审批策略（搬运 Codex 三层）**：
- 技术边界（沙箱：能做什么）与决策边界（审批：何时问人）分离
- `untrusted`：只自动运行已知安全操作，其余全问
- `on-request`：沙箱内自主，越界时询问（默认推荐）
- `never`：从不询问（CI/批量场景）

**PM 场景的高风险动作（必须审批）**：
- 修改已 confirmed 产物
- 删除需求/范围
- 发送给干系人（邮件/飞书）
- 修改已确认范围
- 调用外部 API（JIRA/飞书）

### 2.6 会话与状态（可追溯性核心）

**参考**：Claude Code append-only JSONL + Codex JSONL 会话 + dsh session log。

**三条通道（搬运 Claude Code）**：

| 通道 | 格式 | 用途 |
|---|---|---|
| Session transcripts | append-only JSONL | 完整对话，压缩边界用 chain-patching 修补 |
| Global prompt history | history.jsonl | 跨会话提示词召回 |
| Subagent sidechains | 每个子代理独立 JSONL | 隔离的子代理历史 |

**硬不变式（搬运 dsh）**：**模型可见 ⟺ 已记录**。任何到达模型请求的内容必须能从 session log 重建；新增模型可见输入必须新增 session event。

**Checkpoint（搬运 Claude Code）**：
- 每次 PRD 编辑前自动快照受影响文件
- 支持「回退到上一版需求」
- 会话级权限不恢复（resume 后需重新审批）

### 2.7 配置系统（分层 + 可组合）

**参考**：Claude Code 4 级作用域 + Codex profile + dsh profile/bundle 分层。

**PM Agent 配置层级**：

| 层级 | 位置 | 影响 | 团队共享 |
|---|---|---|---|
| Managed（企业） | `/etc/pm-agent/settings.json` | 全机器所有用户 | 是 |
| User | `~/.pm-agent/settings.json` | 个人所有项目 | 否 |
| Project | `.pm-agent/settings.json` | 仓库协作者 | 是（提交 git） |
| Local | `.pm-agent/settings.local.json` | 仅本仓库个人 | 否（gitignore） |

**指令文件层级（PM_AGENTS.md / CLAUDE.md 的 PM 版）**：
- Managed（公司产品规范）
- User（个人偏好）
- Project（项目 PRD 规范、术语表）
- Local（个人草稿）
- 支持 `paths` frontmatter 做路径级规则（只对某模块需求生效）

**Profile（搬运 Codex/dsh）**：
- `pm-clarify`（澄清预设）
- `pm-write`（生成预设）
- `pm-review`（评审预设）
- `pm-publish`（发布预设）

### 2.8 确定性门控（Hooks）

**参考**：Claude Code hooks（确定性，注册后必然执行）+ Codex 生命周期钩子。

**PM Agent hooks**：

| 事件 | 触发时机 | PM 场景 |
|---|---|---|
| `PreToolUse` | 工具调用前 | 拦截对 confirmed 产物的写入、敏感文件保护 |
| `PostToolUse` | 工具调用后 | 自动格式化、命令日志 |
| `PreCompact` | 压缩前 | 保存压缩前快照 |
| `PostCompact` | 压缩后 | 记录压缩摘要 |
| `SubagentStart/Stop` | 子代理启停 | 记录子代理调度 |
| `Stop` | 会话结束 | 生成会话总结 |

**关键设计**：流程规则从「提示词建议」升级为「确定性强制」——如「PRD 必须包含验收标准，否则 PostToolUse hook 阻断」「发布前必须过评审子代理」。

### 2.9 验证闭环（最被低估的一条）

**参考**：Claude Code「给 agent 验证自己工作的方式」是最高杠杆 + 现有 PM Scaffold 校验器。

**PM Agent 内置验证器**：
- PRD 对照需求清单逐条勾选（traceability）
- LLM-as-judge 评审（reviewer 子代理）
- 结构化 schema 校验文档完整性（复用现有 validate_artifact.py）
- 术语表合规检查（引用已定义术语）
- RACI 合规检查（产物 frontmatter 角色字段合法）

**原则（搬运 Claude Code）**：定义规则 → 说明哪条规则失败及原因，优于模糊反馈。

---

## 3. 复用现有 PM Scaffold 的部分

| 现有资产 | 复用方式 |
|---|---|
| 产物规范（background-goal / journey / UX / function-description / PRD） | 直接复用为 PM Agent 的产物模板 |
| 17 个 `validate_artifact.py` 校验器 | 直接复用为 PM Agent 的验证器 |
| 术语表 `docs/术语表-glossary.md` | 注入 PM Agent 上下文 |
| 团队职责矩阵 `docs/团队职责矩阵-RACI.md` | 作为权限门控依据 |
| 变更管理机制 `docs/变更管理机制-change-management.md` | 作为 confirmed 不可变 + change-record 依据 |
| issue-record skill | 作为需求澄清的问题清单载体 |
| workflow-registry.json | 作为产物/阶段注册表 |
| 飞书工具（feishu_fetch / prd_publish） | 作为 PM Agent 的飞书工具插件 |

---

## 4. 技术选型建议

| 组件 | 建议 | 理由 |
|---|---|---|
| 语言/运行时 | TypeScript + Node（或 Python） | dsh/Claude Code 用 TS，Codex 用 Rust；PM 场景 TS 生态成熟 |
| Agent 框架 | 自研轻量 loop（参考三家）或基于现有 SDK | 不引入重框架，保持可控 |
| 会话存储 | append-only JSONL + SQLite 索引 | Claude Code 方案，可审计可重建 |
| 插件系统 | 自研（参考 Cordis 理念）或轻量 DI | 一切皆插件，但 PM 场景不需要完整 Cordis |
| 校验器 | 复用现有 Python 校验器（子进程调用） | 资产复用，不重写 |
| 飞书集成 | 复用现有 lark-cli 工具 | 资产复用 |
| 记忆 | 文件式 markdown（无向量库） | Claude Code 方案，透明可审计 |

---

## 5. 实施路线图

### Phase 0：地基（1-2 周）
- 项目初始化（monorepo，TS + Python 混合）
- 复用 PM Scaffold 资产（产物规范、校验器、术语表、RACI）
- 定义 PM Agent 的 9 步流水线骨架

### Phase 1：核心循环（2-3 周）
- Agent Loop 实现（gather → think → act → verify）
- 上下文管理（5 层渐进压缩 + 有界片段）
- Session Log（append-only JSONL + 硬不变式）
- 权限门控（5 级渐进信任谱系）

### Phase 2：子代理与评审（2-3 周）
- 5 个角色子代理（clarifier / researcher / writer / reviewer / verifier）
- Sidechain transcripts 隔离
- 评审流程（reviewer 子代理 + 校验器 + LLM-as-judge）

### Phase 3：记忆与配置（1-2 周）
- 文件式记忆（自动脱敏、后台异步）
- 4 级配置层级 + Profile
- PM_AGENTS.md 指令链

### Phase 4：确定性门控与发布（1-2 周）
- Hooks（PreToolUse / PostToolUse / PreCompact / Stop）
- 发布流程（publish 模式 + 飞书集成）
- Checkpoint / resume / fork

### Phase 5：验证闭环与打磨（持续）
- 验证器（traceability / schema / LLM-as-judge）
- 快照回归（keyless snapshot replay）
- 可观测性（hooks 埋点、审计日志）

---

## 6. 验收标准

1. **自主性**：给定一个飞书需求文档，PM Agent 能自主完成 澄清 → 生成 → 评审 → 确认 全流程，无需人工干预（除审批点）。
2. **可追溯**：任何产物都能回答「从哪来、为什么长这样」——session log 可重建全部模型输入。
3. **质量**：所有产物通过现有校验器（复用 PM Scaffold 的 79 项回归 + 新增用例）。
4. **可审批**：高风险动作（改 confirmed、发干系人）必须经过审批门控。
5. **可恢复**：会话中断后可 resume / fork / replay。
6. **不简化不敷衍**：空文件/缺章节/缺字段被 gate 拒绝，与现有脚手架一致。

---

## 7. 风险与对策

| 风险 | 对策 |
|---|---|
| 上下文爆炸（长需求会话） | 5 层渐进压缩 + 子代理摘要回收 |
| 模型幻觉（编造需求） | 硬不变式「模型可见 ⟺ 已记录」+ 校验器 + LLM-as-judge |
| 权限失控（误改 confirmed） | 5 级信任谱系 + hooks 拦截 + 审批门控 |
| 与现有脚手架冲突 | 独立新项目，复用资产不侵入 |
| 过度工程 | 先做 Phase 0-1 最小闭环，再逐步加子代理/记忆 |

---

## 8. 参考来源

| 来源 | 链接 |
|---|---|
| DeepSeek Harness 官网 | https://www.deepseek.com/harness/en/ |
| DeepSeek Harness GitHub | https://github.com/deepseek-ai/deepseek-harness |
| dsh 架构文档 | https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md |
| dsh AGENTS.md | https://github.com/deepseek-ai/deepseek-harness/blob/master/AGENTS.md |
| Codex 官方总览 | https://developers.openai.com/codex/ |
| Codex 沙箱与审批 | https://developers.openai.com/codex/agent-approvals-security |
| Codex 配置参考 | https://developers.openai.com/codex/config-reference |
| Codex 子代理 | https://developers.openai.com/codex/subagents |
| Codex Memories | https://developers.openai.com/codex/memories |
| Codex AGENTS.md 指南 | https://developers.openai.com/codex/guides/agents-md |
| Claude Code 工作原理 | https://code.claude.com/docs/en/how-claude-code-works |
| Claude Code 权限模式 | https://docs.anthropic.com/en/docs/claude-code/permission-modes |
| Claude Code 记忆 | https://docs.anthropic.com/en/docs/claude-code/memory |
| Claude Code 子代理 | https://docs.anthropic.com/en/docs/claude-code/sub-agents |
| Claude Code Hooks | https://docs.anthropic.com/en/docs/claude-code/hooks-guide |
| Claude Code 沙箱 | https://docs.anthropic.com/en/docs/claude-code/sandboxing |
| Dive into Claude Code（论文） | https://arxiv.org/abs/2604.14228 |
| Anthropic 工具设计 | https://www.anthropic.com/engineering/writing-tools-for-agents |
