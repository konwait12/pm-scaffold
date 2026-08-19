# 高保真原型技法参考（High-Fidelity Prototype）

> 来源吸收：Trae `frontend-design` skill 的 BOLD aesthetic direction 设计哲学与硬规则（避 AI-slop、反 Inter/Arial、反纯紫渐变、可访问对比度等），以及 `web-artifacts-builder` / `interactive-demo-factory` 的单文件 HTML 落地技法，经适配后作为 page-design 的**可选附件**落地能力。
> 定位：page-design 的权威产物是页面与步骤描述表格（文本骨架）；高保真原型是该文本骨架的**可选高保真可视化附件**，用于在 ready_for_human_review 后向利益相关方做视觉/观感沟通——**互补，不替代**。区别于 `references/prototype-techniques.md`：后者产"逻辑 100% 忠于输入的可点击 demo"（中保真、状态机驱动）；本文档产"视觉方向鲜明、可指代品牌气质的高保真 mockup"（高保真、设计语言驱动）。
> 触发：①产物已进入 `ready_for_human_review` 状态、文本骨架与跳转表自审通过；②用户/PM 主动请求"出原型 / 做截图 / 给一版视觉"；③Agent 先自检能力——本地具备 `frontend-design` 或 `web-artifacts-builder` skill 或同类前端能力时才启用，否则**只交付文本骨架**，不硬出 HTML。

## 1. 输入映射（pm-scaffold 语境）

| 外部 skill 输入 | pm-scaffold 对应产物 | 说明 |
|---|---|---|
| 页面信息结构 | page-design 页面与步骤描述行（PG-XXX） | 每个 PG 一节 HTML，区块由"主要内容"列映射 |
| 页面导航关系 | page-design 跳转关系 / 下一状态列 | 超链接 / 按钮 onClick 目标 |
| 操作与文案 | page-design 操作列 + interaction-rules IX-XXX | 按钮文案与可点击元素 |
| 视觉调性 | feature-list / project-background 的产品定位 | 选定本文 §2 的设计方向 |
| 品牌 token | 项目设计系统（若有） | 覆盖默认色板/字体；无则用本文 §2 方向默认值 |

> **文本骨架未 ready_for_human_review 不出 HTML**：高保真原型是评审辅助，骨架未自审通过前不进入视觉阶段，避免"用视觉掩盖结构性缺陷"。无视觉请求时默认只交付文本骨架。

## 2. 设计方向（吸收 frontend-design BOLD aesthetic direction）

frontend-design 的核心是"承诺一个鲜明的概念方向，并精确执行"。以下给 3 种 PRD 高频场景的方向默认值；每个方向给色板 / 字体 / 留白 / 圆角 / 质感五项硬规则，**任一方向都不得退化成"白底紫渐变 + Inter 字体"的 AI-slop 默认皮**。

### 方向 A：Business Dashboard（To B 数据驾驶舱 / 后台管理）

- **色板**：深底优先（`#0B1220` 主底 / `#111827` 卡片底 / `#1F2937` 分隔）；强调色单一锐利（青绿 `#10E0C4` 或琥珀 `#F5A524`，二选一，不混用）；数据语义色仅 success/warn/danger 三类，不堆叠。
- **字体**：标题用具有几何特征的展示字（如 `Söhne` / `Geist Mono` / `IBM Plex Sans`，避免 Inter / Roboto / Arial）；正文用配套正文字；数字用等宽 tabular-nums。
- **留白**：信息密度高但有节奏：区块内 12px、区块间 24px、模块间 40px；不留无意义大空白，也不挤成一团。
- **圆角**：卡片 8px、按钮 6px、徽章 4px；不使用 24px+ 大圆角（那是消费类语汇）。
- **质感**：细网格底纹（opacity 0.04）、卡片 1px 边框 + 极淡阴影（`0 1px 0 rgba(255,255,255,0.04)`）；不堆模糊光晕。

### 方向 B：Consumer App Mobile（To C 移动端 / 面向消费者）

- **色板**：温暖底色（米白 `#FAF7F2` / 奶油 `#FFF8EE`）或单一品牌色作主色（饱和度 ≥ 70%）；强调色克制（最多 1 个辅助色）；禁纯白底 + 紫渐变。
- **字体**：展示字选有 character 的（如 `Fraunces` / `Recoleta` / `Tiempos`，避 Inter）；正文用人本可读的（如 `Söhne` / `Geist` / 系统中文 PingFang / Source Han Sans）。
- **留白**：呼吸量大——主内容左右各 20px、章节间 32px；首屏不要 4 列网格，单列优先。
- **圆角**：卡片 16–20px、按钮 999px（胶囊）/ 12px、图直角；混用而非全圆。
- **质感**：软阴影 `0 8px 24px rgba(0,0,0,0.06)`；可加极淡 grain overlay（opacity 0.02）增加纸质质感；禁大色块渐变背景。

### 方向 C：To B Console（开发者控制台 / 工程平台）

- **色板**：冷调中性（`#0D1117` 主底 / `#161B22` 面板 / `#30363D` 边线）；强调色用品牌色单一（如 `#58A6FF`），状态色饱和度统一。
- **字体**：等宽字优先（`JetBrains Mono` / `IBM Plex Mono` / `Geist Mono`）；标题用配套无衬线（避 Inter）；行高 1.5。
- **留白**：信息高密度，但行高、内边距严格统一（8/16/24 三档）；不留"装饰性"空白。
- **圆角**：4–6px 统一；按钮、卡片、徽章同档；不用大圆角。
- **质感**：1px hairline border 主导（`#30363D`），阴影几乎不用；图表用 1px stroke + 微 fill，不发光。

> 任一方向选定后，**在同一产物内不混用**——混用即丢失 BOLD 主张，回退到 AI-slop。若 PM 不能定方向，先出方向对比卡（三张小缩略图同屏），让授权人工选定后再进入 HTML 生成。

## 3. 反 AI-slop 硬规则（吸收 frontend-design NEVER 清单）

以下为禁项，违反任意一条都视为"AI-slop 默认皮"，应回炉重做：

1. **禁纯 Inter / Roboto / Arial / system-ui 单字族撑全场**：必须配一个有 character 的展示字。Space Grotesk 不得在多次生成中收敛复用（每次至少换一个展示字候选）。
2. **禁纯紫渐变 on 白底**：`linear-gradient(135deg, #667eea, #764ba2)` 这类 Tailwind/Stripe 默认皮禁止作为主背景或主按钮；如需渐变，用品牌色 + 同色系深浅过渡，且仅在 hero/CTA 等高焦点处局部使用。
3. **禁过度圆角**：全圆角（24px+）+ 全胶囊按钮的组合是 AI-slop 标志；圆角档位需匹配方向（见 §2 各方向圆角规则）。
4. **禁无障碍对比度不足**：正文与背景对比度 WCAG AA 起步（4.5:1；大字 3:1）；深底浅字或浅底深字都要核验；用 CSS 变量定义语义色，不在 inline style 写裸色。
5. **禁开发面板混入演示**：右侧 AI 规则面板、调试面板、路由表、资源说明卡不进入 demo 页（与 `prototype-techniques.md` §4 硬规则 4 一致）。
6. **禁 cookie-cutter 布局**：三列卡片 + 居中 hero + 底部 CTA 的"标准 SaaS 落地页"模板不得默认使用；布局须为内容服务，可不对称、可断网格、可留大呼吸量。

## 4. 落地方式

### 4.1 手写单文件 HTML（首选）

- 单一 `.html` 文件，内联 CSS + JS，无外部构建依赖，浏览器双击即可打开。
- 设计 token 用 `:root` CSS 变量定义（色板 / 字体 / 间距 / 圆角档位），便于一次性 rebrand。
- 字体走 Google Fonts CDN（或自托管 woff2）；不内嵌 base64 大字体文件。
- 交互只做必要的 hover/active/状态切换；不做无业务含义的视差/粒子等装饰动画。

### 4.2 占位渲染兜底（Agent 自检无 frontend-design 能力时）

- 用 Tailwind CSS CDN + 极简 HTML 结构，**仅作为占位**，明确告知 PM"这是低保真占位，建议由具备 frontend-design 能力的 Agent 或设计师重做"。
- 占位 HTML 仍遵守 §3 反 AI-slop 硬规则（即使用 Tailwind，也不用默认紫渐变 + Inter）。
- 占位交付后，文本骨架仍为权威产物，HTML 不替代表格。

### 4.3 落盘位置与命名

- 路径：`requirements/REQ-XXX/99-review/support/prototype/`（与 `prototype-techniques.md` §5 一致，避免分裂）。
- 命名：`[REQ-XXX-功能名]-高保真原型-v1.0.html`（与可点击 demo 的 `-交互原型-v1.0.html` 区分）。
- 同时落一份 `high-fi-direction.md` 简记：选定方向（A/B/C）、色板 token、字体、圆角档位、为什么选这个方向——便于后续 rebrand 与回溯。

## 5. 从 PG-XXX 文本骨架到 HTML 区块的工作流

把 page-design.md 的"页面与步骤描述"表格逐行映射为 HTML，**每个 PG 一节**，节内区块由"主要内容"列拆出。最小可用模板如下：

```text
PG-XXX: {页面名称}
├── <header>        ← 入口导航（来自"入口"列）
├── <main>
│   ├── 前置条件提示  ← "前置条件"列未满足时显示（如"请先登录"）
│   ├── 内容区块 A   ← "主要内容"列第 1 项
│   ├── 内容区块 B   ← "主要内容"列第 2 项
│   └── 操作区       ← "操作"列每条一个按钮/链接，onClick → 下一状态对应 PG
└── <footer>        ← 退出/帮助入口
```

**映射硬规则**：

1. **一行一节**：page-design 表格一行（一个 PG-XXX）对应 HTML 中一节 `<section data-pg="PG-XXX">`；不跨行合并、不拆行。
2. **主要内容→区块直译**："主要内容"列写的信息区块（如"场地卡片列表 + 筛选"）拆为 2 个 HTML 区块（卡片列表 / 筛选条），不发明表里没有的区块。
3. **操作→可点击元素**：每条操作 = 一个 button 或 link，`data-act="ACT-XXX"`（若有 ACT 编号），点击行为 = 切换到"下一状态"列对应的 PG 节（用 JS 切 section 显隐，或锚点跳转）。
4. **下一状态→目标**：下一状态若指向另一个 PG-XXX，链接/跳转目标即该 PG 节；若为"停留本页"，按钮 disabled 或弹 toast；若为"退出流程"，链接到外部首页占位。
5. **前置条件→门控**：前置条件未满足时（如未登录），整节用 `aria-hidden` + 遮罩，或直接渲染"前置未满足"占位卡片。
6. **AI_INFERENCE 标注**：表格中标 `AI_INFERENCE` 的内容区块，在 HTML 中加 `data-inference="true"` 属性并在视觉上以虚线边框 + 角标"推断"提示，交评审方优先核对。

## 6. 反模式

| ❌ 不要 | ✅ 要 |
|---|---|
| 用高保真 HTML 替代文本骨架表格 | 文本骨架是权威；HTML 是评审附件，二者同交付 |
| 在 ready_for_human_review 前就出 HTML | 先让骨架自审通过，再用视觉放大沟通 |
| 默认白底 + 紫渐变 + Inter | 选定 §2 一个方向，承诺 BOLD aesthetic direction |
| 三方向混用（Dashboard 底 + Consumer 圆角 + Console 字体） | 同一产物内只执行一个方向 |
| 把开发面板/路由表塞进 demo 页 | 演示页只放真实用户路径元素 |
| 占位 HTML 用 Tailwind 默认紫渐变 | 即使占位也守 §3 硬规则，或明确标注"低保真待重做" |
| 凭视觉方便新增表里没有的区块 | 区块严格来自"主要内容"列；新增区块回 page-design 补行 |

## 7. 与四份 references 联合使用

page-design 的 references 是一条流水线，建议联合使用、不要孤立读：

```text
information-architecture.md   ← §1 先画信息架构（Mermaid 层级 + 导航关系）
        ↓
（文本骨架）                  ← §2 出页面与步骤描述表格（PG-XXX，权威产物）
        ↓
high-fidelity-prototype.md    ← §3 可选：把文本骨架渲染为高保真 HTML 附件（本文档）
        ↓
ui-copywriting-rules.md       ← §4 收口：按钮 / 提示 / 空态文案说人话
        ↓
high-freq-missing-10.md      ← §5 自检：定稿前逐项核验 10 项高频遗漏
```

- **information-architecture.md**：先于本文档使用，确认信息层级；层级未定不进入高保真，否则 HTML 会掩盖结构问题。
- **prototype-techniques.md**：与本文档并列但场景不同——多入口/状态分支复杂时用可点击 demo（逻辑 100% 忠于输入）；视觉/品牌调性需沟通时用本文档高保真 mockup；两者可同交付（一个 `-交互原型-v1.0.html` + 一个 `-高保真原型-v1.0.html`）。
- **ui-copywriting-rules.md**：本文档产 HTML 后，按钮/提示/空态文案用该文档收口，避免 HTML 里塞机器话。
- **high-freq-missing-10.md**：定稿前用其 10 项清单核验，包括"标题/副标题、主次按钮文案、倒计时重试"等易漏点。

> **本文档接入不破坏回归**：纯文档层（B 档参考），不动 `workflow-registry.json`、不动 `templates/` frontmatter 契约、不动 `scripts/validate_artifact.py` 校验器；高保真 HTML 产物不进入任何 ID 契约或状态机，仅作为 `99-review/support/prototype/` 下的沟通附件存在。
