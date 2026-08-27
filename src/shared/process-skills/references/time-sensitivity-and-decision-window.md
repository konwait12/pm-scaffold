# 时效性与决策时间窗（Time Sensitivity & Decision Window）

> 本文将相关实践转化为本项目的可选方法，不引入外部运行时依赖。
>
> **定位**：很多诉求暗含"何时做 / 何时作废 / 何时必须决策"的时间维度——AI 经常忽略，结果 PRD 写的是"做 X"，但 stakeholder 心里想的是"3 周内必须做完 / 这个优惠月底失效 / 决策截止周五"。本技法把这些隐性时间维度显式化。
>
> **触发**：RR Intake 时遇到以下信号——
> - 业务方提到"尽快 / 紧急 / 截止 / 月底前 / 季度内"
> - 诉求有强时间窗口（优惠 / 季节性 / 法定时限）
> - 决策需要快速推进（老板催 / 客户逼 / 监管 deadline）
>
> **按需加载，不设全局闸门。**

---

## 1. 输入映射

| 外部信号 | pm-scaffold 对应产物 |
|---|---|
| 时间窗类诉求 | RR-XXX 的 `valid_until` / `effective_window` 字段 |
| 决策时限 | issue-record 的 DEC 类 + target_close |
| 时效性失效 | issue-record 的 BLK / RSK 类（业务影响） |

---

## 2. 时间维度 5 类

### 类型 1：决策时间窗（Decision Window）

**什么时候必须做决策**：业务方 / 老板 / 客户的"什么时候必须拍板"。

例：
- "老板说周五必须上线"
- "客户合同里写的是 Q3 完成"
- "法务说 9 月 1 日新法生效前必须合规"

**处理**：
- 写到 RR-XXX 的 `decision_deadline` 字段
- 标 issue-record 的 DEC 类 + target_close
- 加载 `confirmation-signal-technique.md` MRC 门禁：G4 业务约束显式（含时间约束）

### 类型 2：有效时间窗（Effective Window）

**诉求本身什么时候有效 / 失效**：优惠 / 季节 / 法规 / 设备生命周期。

例：
- "618 大促期间（6/1-6/18）"
- "新法规生效前用旧版，之后必须切新版本"
- "iOS 18 适配必须在 9 月发布前完成"

**处理**：
- 写到 RR-XXX 的 `effective_window: <start> ~ <end>` 字段
- 超过 effective_window 的 RR-XXX 标 `superseded`
- 在 BG §约束章节明确登记

### 类型 3：执行时间窗（Execution Window）

**什么时候必须做完**：上线时间 / 验收窗口 / 发布日。

例：
- "10 月 1 日上线"
- "双 11 前必须完成"
- "客户 12 月验收"

**处理**：
- 写到 FEA-XXX 的 `release_target` 字段
- 关联到 AC-XXX 的时间判据
- 反推所需功能粒度（P0 必做 / P1 视情况 / P2 砍掉）

### 类型 4：响应时间窗（Response Window）

**系统响应用户操作的时间要求**：登录响应 < 2s / 报表生成 < 30s / 工单响应 < 1h。

例：
- "下单必须 3 秒内成功"
- "客户来电 30 秒内接听"
- "故障 5 分钟内告警"

**处理**：
- 写到 BR-XXX（非功能性业务规则）
- 关联到 AC-XXX 的量化阈值
- 触发 NFR（性能 / 可用性）章节

### 类型 5：变更时间窗（Change Window）

**什么时候可以变更 / 不能变更**：发布冻结 / 维护窗口 / 业务低峰期。

例：
- "周五 18:00 - 周日 18:00 不能发布"
- "双 11 当天不能改价格"
- "新版本灰度 1 周后才能切全量"

**处理**：
- 写到 state-machine 的转移条件
- 关联到 BR 的时间约束
- 标 RR 的"变更窗约束"字段

---

## 3. 应对 12 类典型追问

### 追问 1："业务方说'尽快'，到底多快？"
**答**：这是灰名单信号。追问 "尽快" 的具体含义——是今天 / 本周 / 本月 / 本季度？把模糊时间窗转成具体日期。写进 RR-XXX 的 `decision_deadline` 字段。

### 追问 2："时间窗过了但业务还在做，怎么办？"
**答**：标 `superseded` 旧 RR-XXX，跑新的 RR 重述对齐新时间窗。issue-record 记录变更。

### 追问 3："客户说'月底前必须交付'，但研发说做不到，怎么办？"
**答**：标 DEC 类。让业务方决策——是砍范围、还是延期、还是加班。AI 不替业务方决定（`contracts.md`）。

### 追问 4："时间窗很短，能不能跳过一些阶段直接做？"
**答**：不能跳过——但可调整深度。L0 mini-prd 适用于"单点可定位改动"；L1/L2 适用于完整 PRD。看时间窗紧迫度选档位。

### 追问 5："业务方说'先做着看，时间再说'，怎么办？"
**答**：追问 "做着看" 是哪段时间——若真没时间窗，标 ASSUMPTION；若隐含"下个版本前"，写进 RR `effective_window` 字段。

### 追问 6："RR-001 的 `valid_until` 是月底，但下游 FEA-001 没标，怎么办？"
**答**：FEA-001 必须反向追溯 RR-001 的时间窗——这是 `evidence-four-dimension-check.md` 的"匹配"维度问题。

### 追问 7："多个诉求时间窗冲突，怎么办？"
**答**：标 CLS 类。让业务方排优先级——A 在 6 月必须 / B 在 8 月必须，哪个优先？或并行？

### 追问 8："时间窗到了，但还没做完，怎么办？"
**答**：标 BLK 类（阻断交付）。issue-record 触发 7 天提示 → 14 天升级。业务方决策：延期 / 砍范围 / 加班。

### 追问 9："客户说'5 月内上线'，但合同写的是 6 月，怎么办？"
**答**：以合同为准（FACT）。客户口头承诺标 ASSUMPTION。两个时间窗分别记录到 RR-XXX。

### 追问 10："iOS 17 / 18 / 19 各要适配，时间窗不同，怎么办？"
**答**：每个版本一条 RR-XXX，分别带 `effective_window`。状态机中"已适配 iOS 17" / "iOS 18 待适配"等。

### 追问 11："优惠活动 7 天，PRD 还没定，怎么办？"
**答**：标 BLK 阻断。决策路径——
1. 立刻跑 mini-prd（L0）写"必须做的最小集"
2. 其余细节后置（Deferred）
3. 活动结束后再补 L1/L2

### 追问 12："时间窗和决策可逆性怎么平衡？"
**答**：不可逆决策（合规 / 资金）即使时间窗紧迫也必须验证。可逆决策（UI 文案）即使时间窗宽松也要标 ASSUMPTION（参考 `decision-reversibility.md`）。

---

## 4. 与 RR 其他 references 的协作

- **assumption-stress-test.md**：时间窗假设常需证伪
- **decision-reversibility.md**：时间窗紧迫性 vs 决策可逆性
- **value-cost-risk-triangle.md**：时间窗影响成本（赶工加班 vs 延期罚款）
- **multi-stakeholder-alignment-matrix.md**：不同 stakeholder 的时间窗可能不同

---

## 5. 错误示例

❌ **忽略时间窗**：RR-001 写"做优惠活动"，没标 valid_until
✅ RR-001 `effective_window: 2026-06-01 ~ 2026-06-18`，过期自动 superseded

❌ **把"尽快"当时间窗**："业务方说尽快"——没有具体日期
✅ 追问"尽快"的具体含义，写 `decision_deadline: 2026-08-25`

❌ **时间窗到了还继续做**：超期不标 superseded，悄悄延期
✅ 超期标 superseded，issue-record 记录延期决策

❌ **混淆决策窗 vs 有效窗**：决策窗是 stakeholder 决策时间；有效窗是诉求本身有效期
✅ 分别记录到 RR-XXX 的 `decision_deadline` 和 `effective_window` 字段

❌ **跳过 MRC 门禁 G4 业务约束**："时间紧迫来不及登记业务约束"
✅ G4 门禁硬规则——MRC 不全则不送审（见 `confirmation-signal-technique.md`）

---

## 6. 质量自检清单

- [ ] 每个 RR-XXX 都有 `decision_deadline` 字段（或显式标"无截止"）
- [ ] 每个有强时间窗的 RR-XXX 都有 `effective_window` 字段
- [ ] 时间窗过期的 RR-XXX 自动 superseded
- [ ] 时间窗冲突标 CLS 类 + 路由 issue-record
- [ ] 时间窗紧迫场景优先 mini-prd（L0）做最小集
- [ ] 不可逆决策即使紧迫也必须验证
- [ ] 客户口头承诺 vs 合同时间分别记录
- [ ] MRC 门禁 G4 业务约束显式登记
