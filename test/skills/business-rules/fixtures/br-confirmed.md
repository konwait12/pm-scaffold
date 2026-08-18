---
artifact_id: BR-HIRE-001
version: v0.1
status: ready_for_human_review
owner: PM-Office
business_fact_owner: VP of Talent
goal_decision_owner: VP of Talent
reviewer: VP of Talent
created_at: 2026-08-11
updated_at: 2026-08-11
confirmed_at: ""
upstream_artifact_id: "FEA-HIRE-001, FL-HIRE-001"
---

# 业务规则（BR）

> 22 条 BR-XXX 业务约束 · 4 类分组 · 每条 EARS 句式 + 挂接 FUN + 追溯上游

## 0. 预检输入充分度判定

- 输入：FEA-HIRE-001（18 个 FEA）+ FL-HIRE-001（10 个 FUN 流程）
- 判定：**充分模式** → 走 §1-§4 完整工作流

## 1. 业务规则表

| ID | 规则描述（EARS 句式） | 类型 | 触发条件 | 约束/逻辑 | 所属 FUN | 来源 |
|---|---|---|---|---|---|---|
| BR-001 | **Ubiquitous**：所有候选人邮箱必须唯一 | 约束条件 | 用户注册 | UNIQUE 约束 | FUN-008 | ST-HIRE-006 |
| BR-002 | **Event-driven**：当用户当日投递次数达 20 时，禁止再投递 | 约束条件 | 投递时 | count(today_applications) >= 20 → reject | FUN-003 | ST-HIRE-002 |
| BR-003 | **Ubiquitous**：所有用户密码必须 ≥ 8 位 + 含字母+数字 | 约束条件 | 注册/改密 | 长度 ≥ 8 且含字母数字 | FUN-008 | ST-HIRE-006 |
| BR-004 | **State-driven**：在简历状态为"待审"时，HR 可标记 | 状态约束 | HR 操作 | state == 'pending' → allow | FUN-006 | ST-HIRE-005 |
| BR-005 | **Event-driven**：当职位发布时间 > 30 天未投递，自动降权 | 策略规则 | 每日定时 | days_since_post > 30 → score *= 0.5 | FUN-001 | BG-HIRE-002 §3 |
| BR-006 | **Optional**：当用户启用"邮件推荐"时，按订阅条件每周一推送 | 策略规则 | 用户订阅 | weekly_send_enabled → push every Monday | FUN-005 | ST-HIRE-004 |
| BR-007 | **Ubiquitous**：所有 PII 字段必须加密存储（AES-256） | 约束条件 | 数据存储 | 字段含 PII 标记 → 加密 | FUN-008 | BG-HIRE-002 §约束 |
| BR-008 | **Ubiquitous**：PIPEDA 合规 — 候选人可申请删除账号（30 天内） | 约束条件 | 用户申请 | 30 天内必须执行删除 | FUN-008 | BG-HIRE-002 §约束 |
| BR-009 | **Event-driven**：当 HR 拒绝候选人时，必须填拒绝原因 | 约束条件 | HR 操作 | action == 'reject' → reason 必填 | FUN-006 | ST-HIRE-005 |
| BR-010 | **Ubiquitous**：招聘漏斗各阶段转换率必须 ≥ 基线 80% | 约束条件 | 数据看板 | baseline * 0.8 → 告警 | FUN-010 | G-004 |
| BR-011 | **Event-driven**：当简历上传 > 5MB 时，拒绝 | 约束条件 | 上传 | file_size > 5MB → reject | FUN-002 | F-002-1 |
| BR-012 | **Ubiquitous**：所有 API P99 延迟必须 < 800ms | 性能约束 | 每次请求 | P99 < 800ms | FUN-001 | G-002 |
| BR-013 | **Ubiquitous**：所有数据保留 7 年（合规） | 约束条件 | 数据存储 | retention_years = 7 | FUN-008 | PIPEDA |
| BR-014 | **State-driven**：在投递状态为"已撤回"时，不再计入漏斗 | 状态约束 | 撤回 | state == 'withdrawn' → exclude | FUN-003 | ST-HIRE-002 |
| BR-015 | **Event-driven**：当 HR 给候选人打"资深"标签时，自动推荐匹配的高级职位 | 策略规则 | 标签变更 | tag == 'senior' → push senior_jobs | FUN-007 | FEA-018 |
| BR-016 | **Ubiquitous**：薪酬展示必须包含最低 + 最高（不展示具体数） | 约束条件 | 职位展示 | show range, hide exact | FUN-011 | 加拿大劳动法 |
| BR-017 | **Event-driven**：当用户 90 天未登录时，发送召回邮件 | 策略规则 | 每日定时 | days_since_login > 90 → email | FUN-008 | DAU 维护 |
| BR-018 | **State-driven**：在账号被锁定时，禁用所有需要登录的功能 | 状态约束 | 锁定 | state == 'locked' → disable | FUN-008 | F-008-3 |
| BR-019 | **Optional**：当用户启用"勿扰模式"时，不发送任何通知（除安全） | 策略规则 | 用户设置 | dnd_enabled → skip non-security | FUN-008 | 用户体验 |
| BR-020 | **Event-driven**：当 PIN 邮件发送 3 次未达时，临时封禁邮箱 1h | 策略规则 | 重发 | attempts > 3 → block_email_1h | FUN-008 | F-008-2 |
| BR-021 | **Ubiquitous**：所有用户数据变更必须写入 audit log | 约束条件 | 数据变更 | any_update → audit_log | FUN-001 | 宪法第 8 条 |
| BR-022 | **Ubiquitous**：所有候选人可一键导出自己的全部数据（GDPR/PIPEDA） | 约束条件 | 用户请求 | export_user_data → 30 天内 | FUN-008 | PIPEDA |

## 2. 规则分类汇总

| 类别 | 数量 | 占比 |
|---|---|---|
| 约束条件（Ubiquitous） | 8 | 36% |
| 事件触发（Event-driven） | 7 | 32% |
| 状态约束（State-driven） | 4 | 18% |
| 策略规则（Optional） | 3 | 14% |

## 3. 异常与例外

| ID | 例外条件 | 处理 | 所属 FUN |
|---|---|---|---|
| BR-002 | 用户付费升级后（未来） | 限制放宽到 50/天 | FUN-003 |
| BR-005 | 客户付费 | 不降权 | FUN-001 |
| BR-006 | 用户标记"暂停接收" | 暂停推送 | FUN-005 |
| BR-019 | 安全告警 | 仍发送 | FUN-008 |

## 4. 与上游一致性

| 上游 | 引用方式 |
|---|---|
| BG-HIRE-002 | §目标 G1-G5 → BR-012/010/015/005/021 等 |
| ST-HIRE-001~010 | 每条 BR 标注"所属 ST"（如 BR-001 → ST-HIRE-006）|
| FEA-HIRE-001 | FEA-002/003/005/008/009/016 → 各 BR 引用 |
| FL-HIRE-001 | FUN-001~010 → 各 BR 标注"所属 FUN" |


## 5. 规则间依赖图

- BR-002 依赖 BR-021（audit log）：每日限制需读 audit_log 计数
- BR-005 依赖 BR-013（数据保留）：降权数据保留 7 年
- BR-007 依赖 BR-008（PIPEDA）：PII 加密后用户可申请导出
- BR-010 依赖 BR-021（看板告警写 audit log）
- BR-012 强制所有 API 实现 cache + 索引
- BR-014 影响 FUN-010（漏斗排除 withdrawn）
- BR-015 触发 FUN-005（推荐邮件）
- BR-021 依赖 .audit/events.jsonl（append-only 不可篡改）

## 6. 规则生命周期管理

### 6.1 新增 BR 流程
1. PM/业务方在 issue-record 提"新增 BR"需求（DEC 类）
2. 负责人审批（business_fact_owner + goal_decision_owner）
3. AI 起草 BR（EARS 句式 + 挂接 FUN + 追溯上游）
4. 校验：① BR ID 唯一 ② EARS 句式正确 ③ 挂接 FUN-XXX 存在 ④ 引用上游存在
5. 添加到 BR 表 + 更新追溯矩阵 + 触发下游重审

### 6.2 修订 BR 流程
1. PM 在 issue-record 提"修订 BR-XXX"（INF 类）
2. 评估影响：reflow 检测所有引用 BR-XXX 的下游（IX/VL/AC）
3. AI 修订 BR
4. 校验：① 保留 ID ② 更新版本号 ③ 触发 reflow
5. 下游 work_item 重新 confirmed

### 6.3 废弃 BR 流程
1. PM 在 issue-record 提"废弃 BR-XXX"（CLS 类）
2. 评估：是否仍有下游引用？如有，先替换再废弃
3. 标记 BR 为 deprecated（不删除，保留追溯）
4. 通知所有引用方
5. 30 天后归档（BR-013 7 年保留期的一部分）

## 7. BR 与宪法 8 条硬约束的对齐

| 宪法 | BR 体现 |
|---|---|
| §1 confirmed 只能人工 | BR-022 含 audit log 不可篡改 |
| §2 上游未 confirmed 下游不启动 | BR-018 locked 状态禁用 |
| §3 PRD 只聚合不发明 | BR-021 audit log 强制 |
| §4 知识状态标注 | BR-001/002/022 含 6 态标注 |
| §5 产物单点存放 | — |
| §6 变更使下游失效 | BR-010/021 → reflow |
| §7 注册表是真相源 | 所有 BR 挂接 FUN-XXX（注册表唯一）|
| §8 audit log 不可篡改 | BR-021 |

## 8. 业务方常见误解澄清

### 误解 1：「BR 是技术约束不是业务约束」
- 错。BR 表达业务意图（如 BR-002"每日 20 投递上限"是业务方对候选人行为的期待）
- 技术约束是 VL（VL-024 投递限制的执行）

### 误解 2：「BR 越多越好」
- 错。每条 BR 必须有 EARS 句式 + 触发条件 + 副作用 = 维护成本
- 22 条是合理边界（再增加需分版本）

### 误解 3：「BR 可以未来再补」
- 错。下游 IX/VL/AC 都引用 BR，新增 BR 会触发 reflow
- 应该在 first design 时就捕获大部分 BR

## 9. 附录：EARS 句式速查

| 句式 | 关键词 | 适用 | 例 |
|---|---|---|---|
| Ubiquitous | 陈述句 | 恒成立 | "所有邮箱必须唯一" |
| Event-driven | "当 X 时" | 触发事件 | "当投递数达 20 时拒绝" |
| State-driven | "在 X 状态时" | 状态窗口 | "在 locked 状态时禁用" |
| Optional | "当启用 X 时" | 用户可选 | "当启用邮件推荐时推送" |
| Unwanted | "永不" | 永久禁止 | "永不展示具体薪酬" |

## 10. BR → IX/VL/AC 引用矩阵

| BR | 规则主题 | 引用 IX | 引用 VL | 引用 AC | 所属 FUN |
|---|---|---|---|---|---|
| BR-001 | 邮箱唯一 | — | VL-001/002 | AC-010 | FUN-008 |
| BR-002 | 每日 20 投递上限 | — | — | AC-003 | FUN-003 |
| BR-003 | 密码强度 ≥ 8 位 | — | VL-003 | — | FUN-008 |
| BR-004 | 待审状态可标记 | IX-004 | — | AC-013 | FUN-006 |
| BR-005 | 超期自动降权 | — | — | — | FUN-001 |
| BR-006 | 邮件推荐推送 | IX-018 | — | AC-018 | FUN-005 |
| BR-007 | PII 加密存储 | — | VL-007~010 | — | FUN-008 |
| BR-008 | 30 天内删号 | — | VL-008 | AC-022/023 | FUN-008 |
| BR-009 | 拒绝必填原因 | — | VL-022 | AC-012 | FUN-006 |
| BR-010 | 漏斗转化率基线 | — | — | AC-015 | FUN-010 |
| BR-011 | 5MB 上传限制 | — | VL-009 | AC-006 | FUN-002 |
| BR-012 | API P99 < 800ms | IX-001/028/032 | — | AC-005/014 | FUN-001 |
| BR-013 | 数据保留 7 年 | — | — | — | FUN-008 |
| BR-014 | 撤回不计漏斗 | — | — | — | FUN-003 |
| BR-015 | 资深标签推职位 | — | — | — | FUN-007 |
| BR-016 | 薪酬区间展示 | — | — | — | FUN-011 |
| BR-017 | 90 天召回邮件 | — | — | — | FUN-008 |
| BR-018 | 锁定禁用功能 | IX-017 | — | AC-011 | FUN-008 |
| BR-019 | 勿扰模式 | — | — | — | FUN-008 |
| BR-020 | PIN 重发封禁 | — | — | — | FUN-008 |
| BR-021 | 变更写 audit | — | — | AC-022/023 | FUN-001 |
| BR-022 | 数据导出 | — | — | AC-022/023 | FUN-008 |

## 11. 知识状态标注

- 全部 22 条 BR 的规则语句均源于 BG-HIRE-002 §目标/§约束 与 ST-001~016 的明确表述 → **FACT**
- BR 的 EARS 句式选择与"全局 → 具体 FUN"挂接方式由 PM-Office 设计 → **DECISION**
- BR-017"90 天未登录召回"的召回窗口属增长运营假设 → **AI_INFERENCE**
- 加拿大各省劳动法对薪酬展示的具体条款差异待法务确认 → **UNKNOWN**
