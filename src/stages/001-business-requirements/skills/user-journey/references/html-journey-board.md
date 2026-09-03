# HTML 旅程审阅板

HTML 审阅板是 `user-journey.md` 的可视化阅读层。基于内置资产 `assets/user-journey-board.html`（Figma 风中性模板，约 700 行）复制后只替换顶部 `DATA` 对象即可——**不重写样式与交互层**，避免 HTML 与 skill 视觉规范漂移。

板只读、零外部网络依赖、不替代 Markdown、不是 page-design，不应引入未在来源中出现的页面、功能、文案或状态。设计风格与 skill 产物（`user-journey.md` 中嵌入的 HTML 产物、对比报告、UJ 治理文件）保持一致。

## 触发与输入

仅在以下任一条件满足时生成：角色×阶段矩阵较大、存在多个入口/分支需要现场审阅，或 PM 明确要求 HTML。输入只能来自当前 `user-journey.md` 及其治理文件已经记录的来源；若节点内容是 AI 推断或未知，板上必须显式显示该状态。

## 视觉风格（Figma 化 · 与 skill 产物一致）

- **顶部 sticky 工具条**（Figma 风格）：文件名 / 路径面包屑 / 角色·阶段·节点 chip
- **Frame 块**：每个视觉单元是一个 frame（border + 圆角 + shadow-sm），frame-head 含 ftag / ftitle / fsub
- **Figma 用户流**：水平时间线，2 角色 × 6 阶段 = 12 泳道格，每格水平排列节点；贝塞尔箭头连接；MOT 节点金色光晕（带右上角 ★）
- **Stage × Role Matrix**：同旅程的紧凑表视图，节点以 pill 嵌入并带左侧色条
- **Drawer**：底部抽屉，点节点查 5 字段（行为/触点/痛点/形态/证据）+ 证据 monospace 块
- **设计 token（CSS 变量）**：完整语义色板（accent/purple/gold/bad/good/warn）+ ink-1~5 + shadow-sm/md/lg
- **暗色模式**：`prefers-color-scheme: dark` 自动切换
- **打印模式**：`@media print` 隐藏过滤条与 drawer

## 数据契约（DATA 对象）

替换 `assets/user-journey-board.html` 脚本顶部 `DATA` 对象。字段与 skill 角色旅程矩阵同源：

```js
DATA = {
  meta:  { title, crumb, narrative, motIds: [] },
  stages:  [ { idx, code, name, trig } ... ],         // 6 阶段（顺序）
  roles:   [ { idx, code, who, goal } ... ],          // ≥1 角色
  nodes:   [ { id, r, s, title, behavior, touch, pain, path, ev, form?, cat? } ... ],
  edges:   [ [from, to] or [from, to, "back"] ... ],  // "back" 画虚线
  forms:   [ { id, cat:"ext|int", name, rule, nodes } ... ],  // 护栏 2（可选）
  categories: [ { dim, hbg, rtw } ... ],             // 护栏 1（可选）
  branches:   [ { dim, value, affects, given, status } ... ], // 护栏 3（可选）
  emptyStates: [ { state, list, entry, menu, status } ... ],  // 护栏 3（可选）
  states:     [ { id, name, type:"initial|normal|loopback|final", desc, trig } ... ],
  stateEdges: [ { from, to, label } ... ]
};
```

路径类型 path 取值：`normal | alternative | exception | failure | handoff | recovery`（与 skill 一致）。MOT 节点在 `meta.motIds` 列表声明（按节点 id 串）。

## 必备交互

- 按角色筛选（全部/仅客户/仅 FA，可扩展）；
- 按生命周期阶段筛选（在 Matrix 视图隐含；在 Flow 视图通过节点自动归位）；
- 按路径类型筛选：normal、alternative、exception、failure、handoff、recovery；
- 点节点 → drawer 查行为/触点/痛点/形态/证据；
- 显示路径类型图例，未知情绪以"证据不足"呈现；
- 支持 `?role=<id>&stage=<id>&path=<type>` 初始筛选（可扩展）和 `#<node-id>` 锚点，便于评审链接复用；
- 键盘可操作（Esc 关闭 drawer）、移动端可读（≤760px 切换单列布局）、筛选后无空白误导；所有节点都有稳定 ID。

## 视觉与安全边界

- 单文件 HTML，CSS/JS 内联，不加载 CDN、字体、图片或外部 API；
- 顶部 sticky 工具条使用 `backdrop-filter: blur(8px)` 但不依赖外部资源；
- 不把完整 PDF/截图当页面背景；复杂图片只有在原始材料本身承载旅程证据时才可作为缩略图，并保留来源位置；
- 不显示"当前页面/功能/API"等产品实现标签；不模拟页面跳转、不"点击按钮进入某页"的演示动作；
- HTML 只读浏览，不持久化业务数据，不发起网络请求；
- 风格与 skill 产物一致——Figma 化（克制几何、语义色、暗色模式），不堆营销式 hero / 渐变 / 装饰性大卡片。

## 生成前后检查

生成前先向 PM 报告角色、阶段、路径数量和缺口；不为填满矩阵补造节点。生成后检查：

1. 每个 Markdown 旅程节点在板上有对应稳定 ID；
2. 板上的角色、阶段、路径与 Markdown 一致；
3. 主路径和分支可以从视觉上区分（normal 实线蓝 / alternative 紫虚 / exception 红虚 / failure 红虚 / handoff 金实 / recovery 灰点），但不改变业务顺序；
4. 证据不足的情绪、痛点和机会不被渲染成确定结论（不显示形容词性"满意/焦虑"）；
5. 浏览器直接打开不白屏，窄屏不重叠，筛选和锚点可用。

HTML 的展示意见回写治理文件的澄清或变更记录，不能直接把视觉意见升级为业务事实。
