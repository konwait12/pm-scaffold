# Question Patterns · PRD Publish

Eight canonical question templates for the one-question-at-a-time Clarify loop. Each entry gives:

- **When to use** — the trigger condition
- **Question shape** — the prompt structure
- **Three examples** — paraphrased real cases (desensitized)
- **Common traps** — typical AI mistakes when asking this kind of question

Use these as reference when generating a new question in a Clarify Session. See `SKILL.md` § Thinking Prompts → Clarify for runtime rules.

---

## 1. 确认状态（Confirmation State）

**When to use**: when the PRD's confirmation state is unknown, unverifiable, or when the hash does not match.

**Question shape**:

```
[为什么重要] 发布未确认或已被篡改的 PRD 是流程级缺陷。
当前 PRD 状态是 [已知/未知]，hash [一致/不一致]。请确认:
1. PRD 是否已由授权 reviewer 确认?
2. 若 hash 不一致，是否发生过确认后修改?是否需要先走 change-management?
```

**Examples**:

- "PRD 当前状态我无法确认是否为 confirmed。能否提供确认记录（reviewer + 日期 + SHA-256）？"
- "文件 hash 与确认 hash 不一致——确认后是否有人改过？需要先处理再发布。"
- "上游还有一个 Work Item 未 confirmed。按规则不能发布，是否先完成上游确认？"

**Common traps**:

- 看到"99% done"就当确认
- hash 不匹配仍强行发布
- 忽略上游未 confirmed 的级联约束

---

## 2. 渠道选择（Channel Selection）

**When to use**: when the delivery channel list is missing or ambiguous.

**Question shape**:

```
[为什么重要] 渠道决定导出方式与验证项。
请明确发布渠道: [飞书 Docx / 飞书 Markdown / PDF / HTML / Markdown 文件] 中要哪些?
是否同时需要多渠道，还是单一渠道即可?
```

**Examples**:

- "发布到飞书 Docx 还是 PDF？还是两个都要？"
- "研发希望要 Markdown 方便 diff，业务看飞书 Docx。是否各出一份？"
- "只需要内部分发（飞书），不需要对外 HTML？"

**Common traps**:

- 默认全渠道发布，增加维护负担
- 不区分内部/外部受众
- 渠道选择不询问就直接导

---

## 3. 格式与渲染约束（Format / Render Constraints）

**When to use**: when a target medium has known rendering constraints (e.g., Mermaid in Markdown), or when content may not survive the conversion.

**Question shape**:

```
[为什么重要] 渲染问题会造成发布副本与源不一致。
[渠道] 不支持 [内容]（如飞书 Markdown 的 Mermaid）。
可接受的处理:
1. 记录为已知限制并照发?
2. 改用支持该内容的渠道（如飞书 Docx + 白板）?
```

**Examples**:

- "飞书 Markdown 不渲染 Mermaid 流程图。是接受该限制，还是改用 Docx + 白板？"
- "PDF 里表格跨页会断行。是否需要调整分页设置，还是接受现状？"
- "HTML 需要内联样式自包含。生成后链接是否绝对路径？需要检查。"

**Common traps**:

- 不告知限制直接发布残缺内容
- 因渲染问题擅自改写内容
- 信任工具默认设置不核查

---

## 4. 授权发布人（Authorized Publisher）

**When to use**: when no authorized publisher is identified, or the requester is not authorized to sign the publish record.

**Question shape**:

```
[为什么重要] 发布记录必须由授权人签收，否则无效。
谁有权签收本次发布?是否已在 authorized-reviewers.json 中登记?
若无，请登记 [id/姓名/角色]，或指定有权者操作。
```

**Examples**:

- "谁签收这份发布？产品负责人还是业务负责人？请确认其已在授权清单中。"
- "你（请求者）不在 authorized-reviewers.json 中。是否有授权人代签？"
- "发布人角色是 business_owner 还是 product_owner？两者权限不同。"

**Common traps**:

- AI 自己"宣布发布"
- 请求者无权却要求发布
- 发布人角色不符授权清单

---

## 5. 通知对象（Notification Recipients）

**When to use**: when notification recipients or channels are unspecified, or downstream consumers are unknown.

**Question shape**:

```
[为什么重要] 发布的意义在于让需要的人拿到正确版本。
请确认通知对象: [产品负责人 / 业务方 / 研发 / 测试] 哪些需要?
通知方式: 飞书消息 / 邮件 / 群文档 @?
```

**Examples**:

- "研发和测试是否需要在本版本发布时被通知？还是只通知产品与业务？"
- "通知是飞书消息还是群文档 @所有人？"
- "是否需要在发布群里附上发布记录链接供追溯？"

**Common traps**:

- 只通知提需求的人，漏掉下游消费者
- 通知里不带版本号/确认日期/链接
- 把"已发消息"当"已送达已读"

---

## 6. 时间与生效（Timing）

**When to use**: when the publish timing is asserted without evidence, or when a specific effective time matters (e.g., sync with a release window).

**Question shape**:

```
[为什么重要] 发布时间影响通知与下游排期。
本次发布在 [立即 / 指定时间] 生效?
是否需要与 [发布窗口/会议/版本冻结] 对齐?
```

**Examples**:

- "现在就发布，还是等版本冻结后再发布？"
- "PDF 版本是否要在上线日再生成，避免提前泄露新功能？"
- "发布记录的时间戳按实际发布时刻填，还是按计划生效时间填？"

**Common traps**:

- 时间戳填计划时间而非实际时间
- 忽略与版本冻结/上线窗口的同步
- 发布时间影响保密需求时未询问

---

## 7. 内容变更边界（Content Change Boundary）

**When to use**: when the requester asks to "顺手改一下" during publish, or when content drift is suspected.

**Question shape**:

```
[为什么重要] 发布即冻结。任何内容变更都使副本不再是确认版本。
你提到 [改动内容]。这属于 [错别字 / 数字更正 / 范围变更]。
处理方式:
1. 本次照原样发布，变更走 change-management?
2. 先走变更流程更新确认版本，再发布新版本?
```

**Examples**:

- "发布时发现一个错别字。本次照原样发布，还是先走变更流程改确认版本？"
- "业务方要求发布前把上线日期改一下。这改变了确认内容——是否先走 Reflow？"
- "只允许格式调整。任何内容改动都需要你明确批准并登记 ChangeRecord。"

**Common traps**:

- "顺手改个 typo"静默改内容
- 把变更混进发布操作
- 变更后不更新 hash，副本与源失联

---

## 8. 验证范围（Verification Scope）

**When to use**: when the fidelity check depth is unclear, or when only partial verification is requested.

**Question shape**:

```
[为什么重要] 验证深度决定"发布成功"的可信度。
本次验证范围:
1. 仅结构（标题/章节存在）?
2. 完整保真（标题+章节顺序+表格+图+追溯矩阵+元数据+无内容漂移）?
```

**Examples**:

- "只检查标题是否齐全，还是逐节核对表格与图是否完整渲染？"
- "§7 追溯矩阵是否需要逐行核对？"
- "若已知一处渲染问题，本次是否整体停发，还是记录后照发？"

**Common traps**:

- 结构检查通过就当内容保真
- 不检查目的地只检查源文件
- 已知渲染缺陷仍宣称"发布成功"

---

## Cross-cutting tips

1. **排序原则**：Clarify 一次只问 1 个，按 Impact × Uncertainty 排序，先问阻断性高的。
2. **不要问 AI 能查的事实**：PRD 确认记录、authorized-reviewers.json、hash 值，让 AI 自己查。
3. **每问必带 AI 初步判断**：不要让业务方从零开始想问题。
4. **三选项常驻**：给 2-4 个互斥选项 + 「其他」兜底。
5. **跳过按钮**：非阻断项允许业务方打 ⚠️ 风险标签先跳过。
6. **回写位置必填**：每答一题必须能精确指向发布记录产物的哪个章节。
