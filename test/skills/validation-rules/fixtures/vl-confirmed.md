---
artifact_id: VL-HIRE-001
version: v0.1
status: ready_for_human_review
owner: PM-Office
business_fact_owner: VP of Talent
goal_decision_owner: VP of Talent
reviewer: VP of Talent
created_at: 2026-08-11
updated_at: 2026-08-11
confirmed_at: ""
upstream_artifact_id: "FEA-HIRE-001, BR-HIRE-001"
---

# 字段校验（VL）

> 38 条 VL-XXX 字段校验 + 字段定义表 + 跨字段约束 + 法规合规

## 0. 预检输入充分度判定

- 输入：FEA-HIRE-001（18 个 FEA）+ BR-HIRE-001（22 条 BR）
- 判定：**充分模式** → 走 §1-§4 完整工作流

## 1. 字段定义表

| 字段 | 类型 | 长度 | 必填 | 默认 | PII | 来源 FEA | 备注 |
|---|---|---|---|---|---|---|---|
| email | string | 5-100 | 是 | — | 是 | FEA-008 | RFC 5322 |
| password | string | 8-64 | 是 | — | 是 | FEA-008 | ≥8 位含字母+数字 |
| full_name | string | 2-50 | 是 | — | 是 | FEA-008 | — |
| phone | string | 10-15 | 否 | — | 是 | FEA-001 | E.164 格式 |
| city | enum | — | 是 | — | 否 | FEA-001 | 多伦多/温哥华/蒙特利尔 等 |
| industry | enum | — | 是 | — | 否 | FEA-001 | Tech/Finance/Healthcare 等 |
| experience_years | int | 0-50 | 是 | 0 | 否 | FEA-001 | — |
| resume_file | file | ≤5MB | 是 | — | 是 | FEA-002 | PDF/DOC |
| cover_letter | text | 0-2000 | 否 | — | 否 | FEA-003 | 0=使用默认模板 |
| job_id | string | — | 是 | — | 否 | FEA-001 | UUID |
| company_name | string | 2-100 | 是 | — | 否 | FEA-011 | — |
| job_title | string | 2-100 | 是 | — | 否 | FEA-011 | — |
| salary_min | int | 0-1000000 | 否 | — | 否 | FEA-011 | CAD |
| salary_max | int | 0-1000000 | 否 | — | 否 | FEA-011 | CAD, ≥ salary_min |
| pin_code | string | 6 | 是 | — | 否 | FEA-008 | 数字 |
| tag_name | string | 2-20 | 是 | — | 否 | FEA-007 | — |
| status | enum | — | 是 | 'pending' | 否 | FEA-006 | pending/interview/offer/rejected |

## 2. 系统校验

| ID | 校验内容 | 校验规则 | 错误提示 | 关联字段 | 所属 FUN | 来源 BR |
|---|---|---|---|---|---|---|
| VL-001 | 邮箱格式 | RFC 5322 严格校验 | "请输入有效邮箱地址" | email | FUN-008 | BR-001 |
| VL-002 | 邮箱唯一 | DB UNIQUE 约束 | "该邮箱已注册，请直接登录" | email | FUN-008 | BR-001 |
| VL-003 | 密码强度 | ≥8 位 + 含字母+数字 | "密码需 ≥8 位且含字母和数字" | password | FUN-008 | BR-003 |
| VL-004 | 手机格式 | E.164 格式 (+1...) | "请输入有效的国际手机号" | phone | FUN-001 | — |
| VL-005 | 城市枚举 | 必须在白名单 | "请选择支持的城市" | city | FUN-001 | — |
| VL-006 | 行业枚举 | 必须在白名单 | "请选择支持的行业" | industry | FUN-001 | — |
| VL-007 | 经验年数 | 0 ≤ x ≤ 50 | "经验年数需在 0-50 之间" | experience_years | FUN-001 | — |
| VL-008 | 简历文件类型 | PDF/DOC | "仅支持 PDF 和 DOC 格式" | resume_file | FUN-002 | — |
| VL-009 | 简历文件大小 | ≤ 5MB | "文件不能超过 5MB" | resume_file | FUN-002 | BR-011 |
| VL-010 | 求职信长度 | 0-2000 字 | "求职信需在 2000 字以内" | cover_letter | FUN-003 | — |
| VL-011 | 职位 ID 存在 | DB 存在 | "职位不存在或已下架" | job_id | FUN-001 | — |
| VL-012 | 职位未关闭 | state == 'open' | "该职位已关闭" | job_id | FUN-003 | — |
| VL-013 | 公司名长度 | 2-100 字 | "公司名需在 2-100 字" | company_name | FUN-011 | — |
| VL-014 | 职位名长度 | 2-100 字 | "职位名需在 2-100 字" | job_title | FUN-011 | — |
| VL-015 | 薪酬范围 | salary_max ≥ salary_min | "薪酬上限必须 ≥ 下限" | salary_min/max | FUN-011 | — |
| VL-016 | 薪酬合理性 | 0 ≤ x ≤ 1000000 CAD | "薪酬超出合理范围" | salary_min/max | FUN-011 | — |
| VL-017 | PIN 格式 | 6 位数字 | "请输入 6 位数字 PIN" | pin_code | FUN-008 | — |
| VL-018 | PIN 错误次数 | ≤ 3 次/24h | "PIN 错误次数过多，账号已锁定" | pin_code | FUN-008 | BR-018 |
| VL-019 | 标签名长度 | 2-20 字 | "标签名需在 2-20 字" | tag_name | FUN-007 | — |
| VL-020 | 标签去重 | DB UNIQUE | "标签已存在" | tag_name | FUN-007 | — |
| VL-021 | 状态枚举 | pending/interview/offer/rejected | "无效状态" | status | FUN-006 | — |
| VL-022 | 拒绝原因必填 | reason 长度 ≥ 10 | "请填写 ≥10 字的拒绝原因" | status, reason | FUN-006 | BR-009 |
| VL-023 | 搜索关键词长度 | 1-50 字 | "搜索词需在 1-50 字" | (搜索表单) | FUN-001 | — |
| VL-024 | 搜索条件至少 1 | 城市或关键词必填一项 | "请至少输入城市或关键词" | (搜索表单) | FUN-001 | — |
| VL-025 | 邮箱未验证 | state == 'verified' | "请先验证邮箱" | email | FUN-008 | BR-008 |

## 3. 跨字段约束

| ID | 涉及字段 | 规则 |
|---|---|---|
| VL-CC-01 | salary_min, salary_max | salary_max ≥ salary_min |
| VL-CC-02 | start_date, end_date | 任何日期范围：end_date > start_date |
| VL-CC-03 | email, password | 邮箱与密码不同时为空（登录时） |
| VL-CC-04 | resume_file, cover_letter | 至少 resume_file 非空 |
| VL-CC-05 | job_id, user_id | 不能同时投递相同 job_id（去重） |

## 4. 错误信息规范

所有 VL 错误必须含**行动指引**（不能只说"错误"）：

- ✅ 正确："请输入有效的邮箱地址"（含"请"）
- ✅ 正确："文件不能超过 5MB，请压缩后再上传"（含行动）
- ❌ 错误："邮箱格式错误"（无行动）
- ❌ 错误："系统异常"（无行动）

## 5. 加拿大招聘法规特殊校验

### 5.1 平等就业机会（EEO）合规

| ID | 校验内容 | 规则 | 说明 | 所属 FUN |
|---|---|---|---|---|
| VL-026 | 禁止年龄问题 | 简历/申请不得要求填写出生日期 | Ontario Human Rights Code 要求 | FUN-003 |
| VL-027 | 禁止婚姻状况 | 不得询问婚姻/家庭状况 | 联邦人权法要求（FEA-003） | FUN-003 |
| VL-028 | 禁止宗教问题 | 不得强制披露宗教信仰 | 平等就业要求 | FUN-003 |
| VL-029 | 残障便利请求 | 用户可勾选需要面试便利 → 必须记录 | AODA 要求（FEA-008） | FUN-008 |

### 5.2 省级最低工资合规

| ID | 校验内容 | 规则 | 所属 FUN |
|---|---|---|---|
| VL-030 | 时薪 ≥ 各省最低 | Ontario $16.55, BC $16.75, QC $14.25 (2026) | FUN-011 |
| VL-031 | 年薪换算时薪 | 若标年薪需保证换算后不低于该省最低（FEA-011） | FUN-011 |
| VL-032 | 零薪资标记 | 志愿者职位必须明确标注"无薪" | FUN-011 |

### 5.3 语言要求合法性

- **VL-033**：英法双语要求必须与工作内容相关 → 不能歧视只会一种官方语言的申请人（魁北克特殊）
- **VL-034**：魁北克职位必须有法语选项（OQLF 要求）

## 6. PIPEDA 隐私合规校验

| ID | 校验内容 | 规则 | 来源 | 所属 FUN |
|---|---|---|---|---|
| VL-035 | 同意必须明确 | 不能默认勾选"同意隐私政策" | PIPEDA 原则（FEA-008） | FUN-008 |
| VL-036 | 数据最小化 | 只收集必要信息，不强制非必需 | PIPEDA | FUN-008 |
| VL-037 | 导出申请必须允许 | 用户申请导出后 30 天内必须提供 | 数据可携权（FEA-008） | FUN-008 |
| VL-038 | 删除申请必须允许 | 用户申请删除后 30 天内必须删除 | 被遗忘权 | FUN-008 |

## 7. 校验时机分层

### 前端即时校验（Instant）
- 格式类（邮箱、密码、长度）→ 输入时即校验
- 枚举类（城市、行业）→ 选择框天然保证
- 响应：红框提示，不阻止输入，但阻止提交

### 提交前预校验（Pre-submit）
- 必填项检查 → 一次报出所有缺失，不报一个让用户改一个
- 跨字段约束检查 → 指出冲突字段位置
- 业务规则检查（每日上限、重复投递）

### 后端最终校验（Final）
- 唯一性检查（邮箱、标签名）→ DB 事务保证
- 权限检查（用户是否登录、是否有权操作）
- 防注入检查（SQLi / XSS）
- 文件病毒扫描
- 落库前最终一致性检查

**为什么三层？**
- 前端快：给用户即时反馈
- 前端不可信：最终必须后端校验（防篡改绕过）
- 预校验减少 round trip：提升体验

## 8. 错误文案风格指南

所有 VL 错误文案必须：
1. **用"请"开头** → 礼貌引导，不是命令指责
2. **包含具体修复建议** → "请压缩至 5MB 以内"不是"文件过大"
3. **不使用技术术语** → "请输入有效的邮箱地址"不是"格式不匹配 RFC 5322"
4. **中文标点全角** → 保持阅读一致性
5. **长度控制在 10-30 字** → 太长用户不读

反例：
- "格式错误" → 缺修复建议
- "参数异常" → 用户看不懂
- "Validation failed: Email is invalid" → 中英文混，术语

正例：
- "请输入有效的邮箱地址"
- "文件不能超过 5MB，请压缩后再上传"
- "薪酬上限不能低于下限，请调整数值"

## 9. 知识状态与合规声明

| 规则类别 | 状态 | 来源 |
|---|---|---|
| 基础字段校验 | FACT | 产品常识 |
| 加拿大 EEO 规则 | FACT | Ontario Human Rights Code + AODA |
| PIPEDA 隐私规则 | FACT | 联邦隐私法要求 |
| 三层校验时机 | AI_INFERENCE | 前端架构最佳实践 |
| 错误文案风格 | DECISION | UX 团队统一规范 |

## 10. 追溯矩阵

| VL | 关联 BR | 关联 FEA | 关联 FUN |
|---|---|---|---|
| VL-001~003 | BR-001~003 | FEA-008 | FUN-008 |
| VL-004~006 | — | FEA-001 | FUN-001 |
| VL-026~029 | BR-019~020 | FEA-008 | FUN-003/008 |
| VL-030~032 | BR-016 | FEA-011 | FUN-011 |
| VL-035~038 | BR-007~008 | FEA-008 | FUN-008 |
