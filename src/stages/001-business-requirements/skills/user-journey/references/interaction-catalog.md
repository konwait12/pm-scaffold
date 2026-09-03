# 交互目录（Interaction Catalog）

> 交互是触点承载的动作类型，回答「用户/系统在触点上做什么」。每次 Generate 涉及触达行为时，必须先枚举交互（用户要做什么），再选触点（用什么接口）。交互 ID 与触点 ID 解耦，组合出 `<interaction>-<touchpoint>` 唯一标识。

## 交互 ID 命名规范

`<动词>_<名词>`，小写下划线分隔。例如 `reminder_appointment`、`share_invitation`、`login_phone`。

## 交互清单（按业务领域）

### 提醒类（reminder_*）

用户因某事件被动接收通知，不需主动操作。

| ID | 含义 | 典型场景 | 用户后续动作 |
|---|---|---|---|
| `reminder_appointment` | 预约提醒 | 预约前 N 小时通知客户 | 查看详情 / 取消 / 改约 |
| `reminder_birthday` | 生日祝福 | 客户生日前后通知 | 领取福利 / 跳转活动 |
| `reminder_event` | 活动通知 | 活动前 N 天 / N 小时通知 | 报名 / 查看详情 |
| `reminder_payment_due` | 付款到期提醒 | 账单到期前 N 天通知 | 立即支付 / 查看账单 |
| `reminder_expiry` | 过期预警 | 优惠/会员到期前通知 | 续费 / 查看权益 |
| `reminder_status_change` | 状态变更通知 | 订单/工单状态变更 | 查看详情 |

### 分享类（share_*）

用户主动将内容分享给他人或平台。

| ID | 含义 | 典型场景 | 触点特征 |
|---|---|---|---|
| `share_content` | 内容分享 | 文章/卡片/海报分享 | 被动拉取，需用户主动选 |
| `share_invitation` | 邀请分享 | 邀请好友注册/参与活动 | 触发注册链路 |
| `share_promotion` | 促销分享 | 优惠券/拼团链接分享 | 关联转化追踪 |
| `share_result` | 结果分享 | 打卡/测试/成绩分享 | 社交属性强 |

### 登录类（login_*）

用户身份验证。

| ID | 含义 | 触点 | 备注 |
|---|---|---|---|
| `login_phone` | 手机号登录 | SMS_3RD_PARTY（验证码） | 国内主流 |
| `login_email` | 邮箱登录 | EMAIL_TRANS（验证链接） | 海外/特定行业 |
| `login_wechat` | 微信登录 | 微信 OAuth | 第三方授权 |
| `login_qr` | 扫码登录 | INAPP_MODAL / 外部扫码 | 跨端登录 |
| `login_biometric` | 生物识别登录 | 系统级（Face ID、指纹） | 设备能力依赖 |

### 支付类（payment_*）

资金流相关——包含金额、退款、合规链路。

| ID | 含义 | 触点 | 备注 |
|---|---|---|---|
| `payment_order` | 订单支付 | INAPP_MODAL / 外部 SDK | 主流场景 |
| `payment_deposit` | 押金支付 | INAPP_MODAL | 业务场景 |
| `payment_refund` | 退款通知 | EMAIL_TRANS / INAPP_REMINDER_CENTER | 含合规披露 |
| `payment_settlement` | 结算通知 | EMAIL_TRANS | B 端场景 |

### 订阅类（subscribe_*）

用户对持续性内容的订阅。

| ID | 含义 | 触点 | 备注 |
|---|---|---|---|
| `subscribe_content` | 内容订阅 | INAPP_REMINDER_CENTER | 关注作者/专栏 |
| `subscribe_notification` | 通知订阅 | MINI_PROGRAM_MSG / PUSH_OS | 系统级推送授权 |
| `subscribe_marketing` | 营销订阅 | EMAIL_MARKETING | 含退订机制 |

### 收藏类（favorite_*）

用户对内容或商品的标记。

| ID | 含义 | 触点 | 备注 |
|---|---|---|---|
| `favorite_product` | 商品收藏 | INAPP_RED_DOT（收藏成功提示） | 需配合 INAPP_REMINDER_CENTER 持久化 |
| `favorite_content` | 内容收藏 | INAPP_RED_DOT | 同上 |

### 评价类（review_*）

用户对服务或商品的反馈。

| ID | 含义 | 触点 | 备注 |
|---|---|---|---|
| `review_service` | 服务评价 | INAPP_MODAL（弹出评价） | 需在合理时机（如服务完成后 24 小时内）触发 |
| `review_product` | 商品评价 | INAPP_REMINDER_CENTER（待评价列表） | 与订单关联 |

### 确认类（confirm_*）

用户对某状态的确认或签收。

| ID | 含义 | 触点 | 备注 |
|---|---|---|---|
| `confirm_arrival` | 到店确认 | INAPP_RED_DOT + GEO | 地理围栏触发 |
| `confirm_event` | 活动确认 | INAPP_MODAL | 活动前确认出席 |
| `confirm_signature` | 电子签收 | INAPP_MODAL | 含法律效力 |

## 选择交互的判断要点

- **触发主体**：系统主动 → reminder_* / confirm_*；用户主动 → share_* / favorite_*；双方 → login_* / payment_*
- **用户角色**：B 端 → payment_settlement / 关注结算；C 端 → reminder_* / favorite_*
- **时机敏感性**：高（实时反馈）→ INAPP 系列；低（异步通知）→ EMAIL_TRANS / PUSH_OS
- **合规约束**：支付 → 必有 refund 配套；登录 → 必有验证；评价 → 不可强制好评

## 模板外的交互处理

若材料中出现本目录未列的交互（如 `report_complaint`、`apply_voucher`）：

1. AI 不得自创，必须先在 governance 登记；
2. 按命名规范 `<动词>_<名词>` 提议新 ID；
3. 提示 PM：「检测到新交互 `<X>`，未在标准目录内。是否纳入？纳入后建议加入本目录。」
4. PM 确认后纳入。

## 交互与触点的组合落地

governance 登记触点时使用 `<interaction>-<touchpoint>` 唯一标识。例如：

```
reminder_appointment-sms_3rd_party     // 预约提醒 via 第三方短信
reminder_appointment-push_os          // 预约提醒 via 系统推送
reminder_appointment-inapp_modal      // 预约提醒 via 应用内弹窗
share_invitation-wechat_share         // 邀请分享 via 微信分享
```

组合覆盖关系参见 `touchpoint-coverage-matrix.md`。
