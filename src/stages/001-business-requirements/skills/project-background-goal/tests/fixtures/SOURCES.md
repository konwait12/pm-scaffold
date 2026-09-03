# 原始材料来源清单（SOURCES）

> 本目录只放**原始材料清单**和**脱敏摘要**，不嵌入任何真实业务材料原文。
>
> 仓库公开可见；原文材料（PPT / 会议纪要 / 口述录音 / PDF 等）受控存放，**不进仓库**。
>
> 跑回归测试时，由执行人按清单获取原文喂入；CI 不直接拉取原文。

## 用例 1：uj-round1-regression（ready_for_human_review）

### 用途

P0-1 标准回归用例：DP（Digital Passport）触达场景的脱敏摘要。验证 UJ skill 端到端跑通后产物结构合规，并通过校验器（仅 advisory warning，不阻断）。

### 原始材料清单（执行人按需获取，不在本仓库）

| ID | 标题 | 类型 | 持有方 | 检索方式 | 日期 |
|---|---|---|---|---|---|
| SRC-001 | 项目阶段性成果讨论（脱敏版本） | 飞书 docx | PM 本地 | `lark-cli docs +fetch --doc <PM-指定 doc-id> --doc-format markdown --scope full --format pretty` | 2026-08-15 |
| SRC-002 | DP 通知方案评审 PPT（脱敏版本） | PPTX | PM 本地 | 受控访问，PM 转交 | 2026-08-22 |
| SRC-003 | 短信模板与发送规则（脱敏版本） | PDF | PM 本地 | 受控访问 | 2026-08-25 |

> 全部原始材料含客户名、订单数据、内部代号，**不得直接进入仓库**。脱敏版由 PM 维护。

### 脱敏规则

- 公司名 / 品牌名 → `<X-BRAND>` 或具体脱敏代号
- 真实客户名 → `<客户-A>` `<客户-B>` ...
- 内部系统代号 → `<系统-X>`
- 订单 / 金额 / 时间 → 保留结构骨架，去掉具体数值
- 短信模板文案 → 保留格式与变量占位，不写具体业务字符串

### 跑测流程

```bash
# 1. 获取原文（执行人手动）
lark-cli docs +fetch --doc <PM-指定 doc-id> --doc-format markdown --scope full --format pretty > /tmp/uj-test-raw.md

# 2. 喂入 UJ skill（按 SKILL.md 流程）
# 输出 user-journey.md + user-journey.governance.md 至 /tmp/uj-test/

# 3. 与本仓库 fixture 对照预期要点清单（TODO: P0-1 后续补 fixtures 期望清单）
# 当前为骨架版，仅验证产物结构合规

# 4. 跑校验器（结构合规 + advisory warning 不阻断）
python3 src/stages/001-business-requirements/skills/user-journey/scripts/validate_artifact.py \
  /tmp/uj-test/user-journey.md --json
```

### 期望要点清单（placeholder）

P0-1 后续维护：每个用例需配「预期产物要点清单」（必含 / 可选 / 不得出现），跑测时逐项核对。当前为骨架版，要点清单留待 PM 评审后补齐。

## 用例 2（待补）

下一轮盲测材料落地后，按同样模板新增「用例 2」段。
