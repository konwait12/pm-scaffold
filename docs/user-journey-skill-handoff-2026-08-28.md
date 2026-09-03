# User Journey Skill 交接记录

日期：2026-08-28  
项目：001 产品 AI 脚手架  
交接对象：下一位继续审阅和优化本 skill 的 AI

## 本轮目标

只修改 `user-journey` skill 及其直接模板、校验器、测试和 HTML 资产。目标是让 AI 从确认的上游背景和本轮原始旅程材料中，生成可追溯的角色×生命周期旅程；主文档供人和 AI 阅读，治理信息独立保存，HTML 只作为审阅板。

本轮不是脱离会议的通用重构：`project-background-goal` 与 `user-journey` 都以 2026-08-27 项目会议原文为直接基线。会议链接：[飞书会议文档](https://ccegroup.feishu.cn/docx/MDVkds3yJocDvGxSYCGceULBn8f?from=from_copylink)。继续优化时应先用飞书 CLI 读取原文，再判断哪些是会议决定、哪些是讨论建议、哪些只是 AI 解读；不要把本报告或任何 reference 当成会议原文。

## 已完成的改动

### 本轮继续修正：会议链接是执行基线

- 重新通过 `lark-cli docs +fetch --doc MDVkds3yJocDvGxSYCGceULBn8f --doc-format markdown --scope full --format pretty` 读取了 2026-08-27 会议原文。
- `project-background-goal` 和 `user-journey` 启动时都必须读取完整会议原文；读取失败或只有摘要时必须停在 `needs_user_input`。
- 两个 skill 都要求把会议内容分成“明确决定 / 会议业务示例 / 讨论或建议 / AI 解读”。DP、SVP 等会议演示只有在 PM 本轮明确指定时才是业务输入，不能成为默认测试夹具。
- 将会议中的实际工作顺序写入两个 skill：先澄清业务本质、方向/框架和起点终点，再逐步完善和实现；每个 skill 单点输入/输出，使用原始材料与人工期望或独立参照比对验证。
- 两个治理模板新增“001 会议基线读取记录”；对应校验器对 `BG-001`/`UJ-001` 缺少文档 ID、`lark-cli` 命令或四类拆分记录时直接报错。
- `user-journey` 的触发元数据改为允许在上游未确认时生成明确标注的候选旅程，但禁止把候选当成事实。

- 重写 `src/stages/001-business-requirements/skills/user-journey/SKILL.md`：
  - 明确 001 项目会议是本轮重建的直接方法与背景基线；
  - 明确原始材料边界，禁止联网、行业常识、模型记忆、其他项目、历史案例和旧夹具补充事实；
  - 新增“材料隔离测试模式”，测试时只允许使用本轮指定原始文件和 PM 本轮说明；
  - 保留第一性原理、系统思维、同理心、对抗性审视、逆向验证和知识边界，但只记录会改变产物的发现；
  - 要求 AI 先判断再用 A/B/C 三选项提问；
  - 分离 `user-journey.md`、`user-journey.governance.md` 和可选 HTML 审阅板；
  - 明确旅程不下沉到页面、功能、字段、接口、业务规则或实现。
- 重写 `src/templates/stage-1-business/user-journey.md`，使其只保留人和 AI 可读的旅程正文。
- 新增 `src/templates/stage-1-business/user-journey.governance.md`，承载来源、知识状态、澄清、Audit、HTML 一致性、PM 确认和哈希。
- 新增 `src/stages/001-business-requirements/skills/user-journey/assets/user-journey-board.html`：
  - 单文件、零网络依赖、只读；
  - 角色/阶段/路径筛选；URL 查询参数和 `#stage-*` 锚点；
  - 节点详情、来源和 UNKNOWN/CONFLICT/AI_INFERENCE 状态；
  - 增加证据状态图例、键盘焦点样式和无效筛选降级；
  - 只呈现旅程节点，不模拟页面或功能。
- 更新 user-journey references，将具体业务示例改为结构化占位内容，并保留矩阵、关键时刻、行为与功能边界、异常恢复和指标等可选方法。
- 更新 `scripts/validate_artifact.py`，支持主文档/治理伴随文件、哈希、状态和治理边界校验；AI 不能写 `confirmed`。
- 删除 `test/skills/user-journey/fixtures/` 中旧业务夹具，测试改为中性角色和业务词。
- 更新 `agents/openai.yaml`，说明治理伴随文件和 HTML 审阅板。
- 修正 `references/audit-checklist.md` 中仍指向旧 `Constitution Compliance`/版本摘要结构的要求，使其与新版旅程契约一致。

## HTML 取舍依据

参考了本地 `flow2demo` 与 `interactive-demo-factory` 的可复用方向：单文件、零依赖、可点击筛选、可复用 URL 路由、窄屏可读和审阅优先。但没有引入它们的页面原型、手机壳、状态模拟、调试面板、截图背景或产品功能演示，因为这些会越过 user-journey 的行为层边界。当前 HTML 是“阅读/筛选/展开证据”的审阅板，不是 demo。

## 已验证

- 直接执行 5 个 user-journey 校验测试：全部通过；
- `python3 src/scripts/registry_contract_check.py`：通过；
- Python 编译检查：通过；
- Node `--check` HTML 脚本语法检查：通过；
- `git diff --check`：通过；
- 注册表已指向 `src/stages/001-business-requirements/skills/user-journey` 和 `03-user-journey`，无需修改。

## 环境限制

- `skill-creator` 官方 `quick_validate.py` 未能运行：环境缺少 `PyYAML`（`ModuleNotFoundError: No module named 'yaml'`）。
- 当前环境没有 Playwright、Puppeteer 或 Chromium，因此只做了 HTML 脚本语法检查，尚未完成真实浏览器截图和交互冒烟。
- `unittest discover` 不会发现现有 pytest 风格函数；本轮改用直接调用测试函数验证。

## 下一位 AI 应优先检查

1. 重新阅读本 skill 与所有引用，确认通用 reference 的方法说明不会覆盖“材料隔离测试模式”。
2. 在有浏览器环境时打开 `assets/user-journey-board.html`，用实际节点数据做筛选、锚点、窄屏和证据状态冒烟测试。
3. 评估是否需要将治理伴随文件的哈希/状态检查接入更上层 pipeline；本轮只保证本地校验器行为。
4. 如需清理其他 skill 的旧业务夹具，先逐目录确认其测试依赖，再单独处理；本轮只清理了 user-journey 目录，没有回滚或删除其他 skill 的用户内容。
5. 不要把本交接记录、reference 示例或测试中性词当作 001 项目的业务事实。
