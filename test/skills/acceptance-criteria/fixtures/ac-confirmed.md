---
artifact_id: AC-HIRE-001
version: v0.1
status: ready_for_human_review
quality_contract_version: "1"
owner: PM-Office
business_fact_owner: VP of Talent
goal_decision_owner: VP of Talent
reviewer: VP of Talent
created_at: 2026-08-11
updated_at: 2026-08-11
confirmed_at: ""
upstream_artifact_id: "FEA-HIRE-001, BR-HIRE-001, EX-HIRE-001"
---

# 验收标准（AC）

> 45 条 AC-XXX 验收标准 · Given/When/Then + 量化阈值 · 可测可自动化

## 0. 预检输入充分度判定

- 输入：FEA-HIRE-001（18 FEA）+ BR-HIRE-001（22 BR）+ EX-HIRE-001（20 EX）
- 判定：**充分模式** → 走 §1-§3 完整工作流

## 1. AC 表

| ID | 验收标准 | 量化阈值 | 来源 G | 所属 FUN | P | 可测 |
|---|---|---|---|---|---|---|
| AC-001 | Given 候选人已登录 + 简历已上传, when 投递职位, then 3s 内提示成功 | P99 ≤ 3s | G-002 | FUN-003 | P0 | E2E |
| AC-002 | Given 简历未上传, when 点投递, then 按钮禁用 + 提示"请先上传简历" | ≤ 100ms | G-002 | FUN-003 | P0 | 单测 |
| AC-003 | Given 当日已投 20 个, when 再投递, then 拒绝 + "已达上限" | ≤ 200ms | G-002 | FUN-003 | P0 | 单测 |
| AC-004 | Given 网络断开, when 搜索, then 顶部黄条 + 缓存显示 | ≤ 500ms | G-002 | FUN-001 | P0 | E2E |
| AC-005 | Given 搜索 P99 > 800ms, when 任意用户搜索, then 不报错 + 仍显示结果 | P99 ≤ 800ms | G-002 | FUN-001 | P0 | 压测 |
| AC-006 | Given 简历 > 5MB, when 上传, then 拒绝 + "文件过大" | ≤ 200ms | G-002 | FUN-002 | P0 | 单测 |
| AC-007 | Given 文件非 PDF/DOC, when 上传, then 拒绝 + "格式不支持" | ≤ 200ms | G-002 | FUN-002 | P0 | 单测 |
| AC-008 | Given 简历解析 confidence < 0.7, when 上传完成, then 标"待补全" | ≤ 10s | G-002 | FUN-002 | P0 | E2E |
| AC-009 | Given 候选人 90 天未登录, when 定时任务, then 发召回邮件 | T+1 天 | G-002 | FUN-008 | P1 | E2E |
| AC-010 | Given 邮箱格式错, when 注册, then 拒绝 + "请输入有效邮箱" | ≤ 200ms | G-002 | FUN-008 | P0 | 单测 |
| AC-011 | Given PIN 错 3 次, when 第 4 次, then 锁定 24h | ≤ 500ms | G-002 | FUN-008 | P0 | E2E |
| AC-012 | Given HR 拒绝无 reason, when 点拒绝, then 拒绝 + 提示"必填理由" | ≤ 200ms | G-005 | FUN-006 | P0 | 单测 |
| AC-013 | Given HR 看候选人, when 状态变更, then 1s 内看板更新 | ≤ 1s | G-005 | FUN-006 | P0 | E2E |
| AC-014 | Given 数据看板加载, when 任意时间范围, then P99 < 3s | P99 ≤ 3s | G-005 | FUN-010 | P0 | 压测 |
| AC-015 | Given 漏斗某阶段转化率 < 基线 80%, when 数据刷新, then 告警 | ≤ 1s | G-005 | FUN-010 | P1 | E2E |
| AC-016 | Given LinkedIn 登录, when 网络异常, then 回退到邮箱登录 | ≤ 2s | G-002 | FUN-008 | P1 | E2E |
| AC-017 | Given 收藏职位, when 用户取消, then 列表立即更新 | ≤ 300ms | G-003 | FUN-004 | P1 | 单测 |
| AC-018 | Given 邮件推荐订阅, when 周一 09:00, then 自动推送 | T+0 | G-003 | FUN-005 | P1 | E2E |
| AC-019 | Given 投递撤回, when 24h 内, then 成功撤回 + 通知 HR | ≤ 500ms | G-002 | FUN-003 | P0 | E2E |
| AC-020 | Given 搜索无结果, when 显示, then "暂无匹配" + 调整建议 | ≤ 100ms | G-002 | FUN-001 | P0 | 单测 |
| AC-021 | Given 职位已关闭, when 候选人访问, then 显示"已关闭" + 相似 | ≤ 500ms | G-002 | FUN-001 | P0 | E2E |
| AC-022 | Given 用户申请数据导出, when 提交, then 30 天内生成 ZIP | T+30 | G-005 | FUN-008 | P0 | E2E |
| AC-023 | Given 用户申请账号删除, when 提交, then 30 天内彻底删除 | T+30 | G-005 | FUN-008 | P0 | E2E |
| AC-024 | Given HR 安排面试, when 操作, then 候选人收到邮件 + 日历 | ≤ 5s | G-005 | FUN-006 | P0 | E2E |
| AC-025 | Given 数据看板打开, when 用户下钻, then 维度切换 ≤ 1s | ≤ 1s | G-005 | FUN-010 | P1 | E2E |
| AC-026 | Given 用户修改简历, when 保存, then ≤ 500ms + 更新列表 | ≤ 500ms | G-002 | FUN-009 | P0 | 单测 |
| AC-027 | Given 邮件订阅, when 用户取消, then 立即停推 + 保留历史 | ≤ 200ms | G-003 | FUN-005 | P1 | 单测 |
| AC-028 | Given 简历 OCR 解析, when 任意输入, then 5s 内完成 | P95 ≤ 5s | G-002 | FUN-002 | P0 | 压测 |
| AC-029 | Given HR 导出数据, when 点击, then 1 分钟内生成 CSV | ≤ 60s | G-005 | FUN-010 | P1 | E2E |
| AC-030 | Given 用户切换语言, when 任意页面, then 全部文案切换 | ≤ 200ms | G-002 | 全局 | P2 | E2E |

## 2. 追溯矩阵

| AC | 所属 FUN | 关联 FEA | 关联 ST | 关联 G | 优先级 |
|---|---|---|---|---|---|
| AC-001~003 | FUN-003 | FEA-002/003 | ST-002 | G-002 | P0 |
| AC-004~005 | FUN-001 | FEA-001 | ST-001 | G-002 | P0 |
| AC-006~008 | FUN-002 | FEA-002/009 | ST-002/007 | G-002 | P0 |
| AC-009~011 | FUN-008 | FEA-008 | ST-006 | G-002 | P0 |
| AC-012~013 | FUN-006 | FEA-006 | ST-005 | G-005 | P0 |
| AC-014~015 | FUN-010 | FEA-012 | ST-010 | G-005 | P0/P1 |
| AC-016 | FUN-008 | FEA-016 | ST-014 | G-002 | P1 |
| AC-017 | FUN-004 | FEA-004 | ST-003 | G-003 | P1 |
| AC-018 | FUN-005 | FEA-005 | ST-004 | G-003 | P1 |
| AC-019 | FUN-003 | FEA-003 | ST-002 | G-002 | P0 |
| AC-020~021 | FUN-001 | FEA-001 | ST-001 | G-002 | P0 |
| AC-022~023 | FUN-008 | FEA-008 | ST-006 | G-005 | P0 |
| AC-024 | FUN-006 | FEA-006 | ST-005 | G-005 | P0 |
| AC-025 | FUN-010 | FEA-012 | ST-010 | G-005 | P1 |
| AC-026 | FUN-009 | FEA-009 | ST-007 | G-002 | P0 |
| AC-027 | FUN-005 | FEA-005 | ST-004 | G-003 | P1 |
| AC-028 | FUN-002 | FEA-002 | ST-002 | G-002 | P0 |
| AC-029 | FUN-010 | FEA-012 | ST-010 | G-005 | P1 |
| AC-030 | 全局 | FEA-015 | ST-013 | G-002 | P2 |

## 3. 优先级分布

| 优先级 | 数量 | 占比 |
|---|---|---|
| P0 | 18 | 60% |
| P1 | 9 | 30% |
| P2 | 3 | 10% |

## 4. 自动化可行性

- **E2E**（Playwright/Cypress）：22 条 — 用户流程类
- **单测**（pytest）：7 条 — 字段校验/状态约束类
- **压测**（k6/Locust）：3 条 — 性能类
- **手动**（UAT）：0 条（**所有 AC 必须可自动化**）

## 5. 法规合规 AC

| ID | 验收标准 | 量化阈值 | 来源 | P | 可测 |
|---|---|---|---|---|---|
| AC-031 | Given 用户不同意隐私政策, when 提交注册, then 拒绝注册 | 立即拒绝 ≤ 200ms | PIPEDA | P0 | 单测 |
| AC-032 | Given 用户申请数据导出, when 提交, then 30 天内生成下载链接 | 30 天完成率 100% | PIPEDA | P0 | 人工+日志 |
| AC-033 | Given 用户申请账号删除, when 提交, then 30 天内彻底删除所有数据 | 30 天完成率 100% | PIPEDA | P0 | 人工+日志 |
| AC-034 | Given 雇主填薪资低于省最低, when 保存职位, then 提示低于法定最低并拒绝保存 | ≤ 500ms | 各省劳工法 | P0 | 单测 |
| AC-035 | Given 职位要求含年龄限制, when 保存, then 提示平等就业法禁止年龄限制并拒绝保存 | ≤ 500ms | Ontario HR Code | P0 | 单测 |

## 6. 可访问性 AC

| ID | 验收标准 | 量化阈值 | P | 可测 |
|---|---|---|---|---|
| AC-036 | Given 键盘用户, when Tab 导航, then 所有可点击元素都能被聚焦 | 覆盖率 100% | P0 | axe-core 自动化 |
| AC-037 | Given 屏幕阅读器, when 浏览页面, then 所有图标都有 aria-label | 覆盖率 100% | P0 | axe-core |
| AC-038 | Given 对比度检查, when 任意页面, then 所有文字对比度 ≥ 4.5:1 | 通过率 100% | P0 | axe-core |
| AC-039 | Given 触摸设备, when 点击按钮, then 所有按钮可点击区域 ≥ 44×44px | 覆盖率 100% | P1 | 视觉检查 |
| AC-040 | Given 用户缩放 200%, when 浏览页面, then 不出现横向滚动条 | 所有页面通过 | P1 | 手动 |

## 7. 性能 AC 补充

| ID | 验收标准 | 量化阈值 | P |
|---|---|---|---|
| AC-041 | 首屏加载（空缓存）| LCP ≤ 2.5s（移动 3G）| P0 |
| AC-042 | 首屏加载（3G 慢速）| LCP ≤ 4s | P0 |
| AC-043 | HTML 大小 | ≤ 200KB gzipped | P1 |
| AC-044 | JavaScript 总大小 | ≤ 1MB gzipped | P1 |
| AC-045 | 第三方脚本阻塞 | 不阻塞首屏渲染（async/defer）| P1 |

## 8. AC 写作原则

好的 AC 必须满足：
1. **Given/When/Then 三段式** → 清晰前置条件/触发动作/预期结果
2. **必须量化** → 不说"很快"要说"P99 ≤ 3s"
3. **必须可测试** → 不能说"用户体验好"，要说"所有操作响应 ≤ 500ms"
4. **必须关联来源** → 每一条 AC 追溯到对应的 FEA/BR/G
5. **必须指定优先级** → P0 必须过；P1 可以延期；P2 可以砍

### 反例
- "系统运行流畅" → 不可测，不量化
- "搜索要快" → 什么叫快？
- "界面美观" → 主观，无法验收
- "支持加拿大劳动法" → 太笼统，不具体

### 正例
- "Given 搜索关键词, when 用户提交, then P99 返回结果 ≤ 800ms"
- "Given 用户申请删除, when 提交, then 30 天内彻底删除所有数据"

## 9. 测试分层映射

| AC 类型 | E2E | 单测 | 压测 | 手动 |
|---|---|---|---|---|
| 用户流程 | Y | — | — | — |
| 字段校验 | — | Y | — | — |
| 性能阈值 | — | — | Y | — |
| 合规法规 | Y | Y | — | 人工签字 |
| 可访问性 | axe 自动 | — | — | — |
| 视觉设计 | — | — | — | Y |

## 10. 就绪标准（DoR）对 AC 的要求

AC 进入 ready_for_human_review 必须满足：
- 所有 P0 FEA 都有至少 3 条 AC
- 所有 BR 都有对应 AC（BR 是业务规则 → AC 验证这个规则确实实现了）
- 所有 EX 都有对应 AC（异常场景也要验收）
- 所有 AC 都符合 G/W/T 格式
- 所有 AC 都量化，没有主观描述
- 优先级清晰（P0/P1/P2）

## 11. 知识状态标注

| 内容 | 状态 | 说明 |
|---|---|---|
| 30 天导出/删除 | FACT | PIPEDA 法定要求 |
| 可访问性标准 | FACT | WCAG 2.1 AA 国际标准 |
| G/W/T 格式 | FACT | BDD 最佳实践 |
| 性能阈值 | DECISION | 加拿大主流 4G/5G 覆盖下的用户期望 |
| 优先级分布 | DECISION | v1.0 优先保障核心流程 |

## 12. 完整追溯矩阵（扩展）

| AC 范围 | P0 | P1 | P2 | 总计 |
|---|---|---|---|---|
| 候选人核心流程 | 11 | 3 | 1 | 15 |
| 雇主后台 | 6 | 4 | 0 | 10 |
| 合规法规 | 5 | 0 | 0 | 5 |
| 可访问性 | 3 | 2 | 0 | 5 |
| 性能 | 2 | 3 | 0 | 5 |
| 全局 | 0 | 0 | 1 | 1 |
| **合计** | **27** | **12** | **2** | **41** |
## 产品质量增强记录

| 项目 | 结论 | 知识状态 | 来源/位置 | 判断人 | 复核触发 |
|---|---|---|---|---|---|
| 受影响角色与结果 | 验收覆盖候选人主流程和异常重试 | FACT | FEA-001 §功能 | PM | 功能变化 |
| 采用方案与被排除替代 | 采用 Given/When/Then，不用“体验好”判定 | DECISION | AC-001 §标准 | PM | 验收方式变化 |
| 价值-成本-风险 | 阈值来自目标，成本与风险待测试确认 | UNKNOWN | G-001 §目标 | PM | 指标变化 |
| 失败边界与回退 | 异常验收失败则回退到草稿 | FACT | EX-001 §恢复 | PM | 恢复策略变化 |
| 可证伪条件/停止条件 | 阈值无来源时不得进入确认 | DECISION | AC-001 §来源 | 业务负责人 | 目标变化 |
