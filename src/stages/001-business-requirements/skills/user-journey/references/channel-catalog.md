# 渠道目录（Channel Catalog）

> 渠道是触点的载体分类属性，不是独立触点。本目录定义三类维度，描述触点的「在哪一侧」「谁来推」「何时达」。每次 Generate 枚举触点后，必须用本目录对每个触点标注渠道属性；落 governance 时渠道属性作为元数据写入。

## 三维度定义

### 1. 载体侧（Side）

触点传递发生在用户与系统哪一侧。

| ID | 名称 | 含义 | 典型触点 |
|---|---|---|---|
| `EXTERNAL` | 外部渠道 | 用户离开自家应用，通过第三方通道接收 | SMS_3RD_PARTY、EMAIL_TRANS、PUSH_OS、CALL_VOICE_AI、WECHAT_SHARE |
| `INTERNAL` | 内部渠道 | 用户在自己应用内接收 | INAPP_RED_DOT、INAPP_BANNER、INAPP_MODAL、INAPP_REMINDER_CENTER |
| `HYBRID` | 混合渠道 | 触发或接收跨内外 | MINI_PROGRAM_MSG（小程序内订阅、系统外触达）、WE_COM_ROBOT（内部员工接收、外部用户触发） |

### 2. 推送方式（Delivery）

谁发起这次触达。

| ID | 名称 | 含义 | 触达即时性约束 |
|---|---|---|---|
| `PUSH` | 主动推送 | 系统主动发起，无需用户当前操作 | 取决于触点；系统侧可控制时延 |
| `PULL` | 被动拉取 | 用户主动查看，系统不主动通知 | 用户触发即达 |
| `BOTH` | 双向 | 同一触点两种模式皆可（如 INAPP_REMINDER_CENTER 可主动推、也可用户主动看） | 两种模式各自有时效 |

### 3. 触达时效（Latency）

从触达触发到用户实际接收的时间窗口。

| ID | 名称 | 含义 | 典型场景 |
|---|---|---|---|
| `INSTANT` | 即时（秒级） | ≤5 秒 | 操作反馈、即时通知 |
| `MINUTE` | 分钟级 | 5 秒 - 10 分钟 | 订单进度、支付确认 |
| `HOUR` | 小时级 | 10 分钟 - 数小时 | 营销通知、活动预告 |
| `DAY` | 天级 | > 数小时 | 行程前一天、订阅日报 |
| `SCHEDULED` | 定时 | 特定时刻或规则触发 | 生日祝福、活动前 N 天 |

## 渠道属性的标注规则

每个触点在旅程节点中应至少标注 `Side` 与 `Delivery` 两维；`Latency` 用于补充说明。例如：

```
节点：客人收到预约提醒
触点：SMS_3RD_PARTY
渠道属性：Side=EXTERNAL, Delivery=PUSH, Latency=INSTANT
```

在 governance 治理伴随文件的「主张来源与知识状态」段登记时，渠道属性作为元数据一并写入；不强制主文档显示。

## 渠道属性 vs 触点 ID 的关系

触点 ID（如 `SMS_3RD_PARTY`）是枚举单位，渠道属性是它的分类标签。一个触点可以对应一组固定渠道属性（如 `SMS_3RD_PARTY` 永远是 EXTERNAL/PUSH），但部分触点属性可变（如 `INAPP_REMINDER_CENTER` 可能是 PUSH 或 PULL）。当材料描述与默认属性冲突时：

1. 优先材料原文；
2. 若材料未明说，按触点的「典型渠道属性」（见下表）落默认值；
3. 在 governance 登记时标注「默认渠道属性」便于审计。

### 触点默认渠道属性速查

| 触点 ID | Side | Delivery | Latency |
|---|---|---|---|
| SMS_3RD_PARTY | EXTERNAL | PUSH | INSTANT |
| EMAIL_TRANS | EXTERNAL | PUSH | MINUTE |
| EMAIL_MARKETING | EXTERNAL | PUSH | HOUR |
| PUSH_OS | EXTERNAL | PUSH | INSTANT |
| WE_COM_ROBOT | HYBRID | PUSH | MINUTE |
| WE_COM_APP | INTERNAL | PUSH | MINUTE |
| CALL_VOICE_AI | EXTERNAL | PUSH | INSTANT |
| CALL_VOICE_HUMAN | EXTERNAL | PUSH | INSTANT |
| INAPP_RED_DOT | INTERNAL | PUSH | INSTANT |
| INAPP_BANNER | INTERNAL | PUSH | INSTANT |
| INAPP_MODAL | INTERNAL | PUSH | INSTANT |
| INAPP_DRAWER | INTERNAL | PUSH | INSTANT |
| INAPP_TOAST | INTERNAL | PUSH | INSTANT |
| INAPP_REMINDER_CENTER | INTERNAL | BOTH | MINUTE |
| MINI_PROGRAM_MSG | HYBRID | PUSH | MINUTE |
| WECHAT_SHARE | HYBRID | PULL | INSTANT |
| WEIBO_SHARE | HYBRID | PULL | INSTANT |
| COPY_LINK | INTERNAL | PULL | INSTANT |

## 模板外的渠道属性

本目录的渠道 ID 是固定的（不随业务增长）。如果材料描述触达特性不能用本目录维度表达（如「跨账号推送」「离线消息」），在 governance 登记并提示 PM，由 PM 在旅程注释中说明——本目录本身不扩展。
