# 触点 / 渠道 / 交互 三层覆盖矩阵（Coverage Matrix）

> 本目录给出常见业务场景下三层组合的典型用法，供 PM 在 Generate 时参考与选择。AI 在枚举交互、触点、渠道属性时，按本矩阵列出的「典型组合」作为候选清单；PM 可修改、删除、补充，AI 不强制要求完全匹配。

## 矩阵说明

- **行**：交互 ID（用户/系统要做的事）
- **列**：触点 ID（用什么接口）
- **单元格内容**：该组合的「典型渠道属性」（Side / Delivery / Latency）+ 适用场景 + 选型要点

单元格为 `—` 表示该组合不推荐或无意义；单元格为 `⚠️` 表示需特别谨慎（如合规约束、高成本）。

## 矩阵：提醒类交互 × 触点

| 交互 \ 触点 | SMS_3RD_PARTY | EMAIL_TRANS | PUSH_OS | INAPP_MODAL | INAPP_REMINDER_CENTER | MINI_PROGRAM_MSG |
|---|---|---|---|---|---|---|
| `reminder_appointment` | EXTERNAL/PUSH/INSTANT | EXTERNAL/PUSH/MINUTE | EXTERNAL/PUSH/INSTANT | INTERNAL/PUSH/INSTANT | INTERNAL/BOTH/MINUTE | HYBRID/PUSH/MINUTE |
| `reminder_birthday` | EXTERNAL/PUSH/INSTANT | EXTERNAL/PUSH/HOUR | EXTERNAL/PUSH/INSTANT | — | INTERNAL/BOTH/HOUR | HYBRID/PUSH/HOUR |
| `reminder_event` | EXTERNAL/PUSH/MINUTE | EXTERNAL/PUSH/HOUR | EXTERNAL/PUSH/MINUTE | ⚠️ 仅重要活动 | INTERNAL/BOTH/MINUTE | HYBRID/PUSH/MINUTE |
| `reminder_payment_due` | EXTERNAL/PUSH/MINUTE | EXTERNAL/PUSH/HOUR | EXTERNAL/PUSH/MINUTE | ⚠️ 高频催收易打扰 | INTERNAL/BOTH/MINUTE | HYBRID/PUSH/MINUTE |
| `reminder_expiry` | EXTERNAL/PUSH/HOUR | EXTERNAL/PUSH/DAY | EXTERNAL/PUSH/HOUR | — | INTERNAL/BOTH/HOUR | HYBRID/PUSH/HOUR |
| `reminder_status_change` | — | EXTERNAL/PUSH/MINUTE | EXTERNAL/PUSH/INSTANT | ⚠️ 仅关键节点 | INTERNAL/BOTH/MINUTE | HYBRID/PUSH/MINUTE |

## 矩阵：分享类交互 × 触点

| 交互 \ 触点 | WECHAT_SHARE | WEIBO_SHARE | COPY_LINK | INAPP_TOAST | EMAIL_TRANS |
|---|---|---|---|---|---|
| `share_content` | HYBRID/PULL/INSTANT | HYBRID/PULL/INSTANT | INTERNAL/PULL/INSTANT | INTERNAL/PUSH/INSTANT（确认反馈） | EXTERNAL/PUSH/HOUR |
| `share_invitation` | HYBRID/PULL/INSTANT | — | INTERNAL/PULL/INSTANT | INTERNAL/PUSH/INSTANT | EXTERNAL/PUSH/HOUR |
| `share_promotion` | HYBRID/PULL/INSTANT | HYBRID/PULL/INSTANT | INTERNAL/PULL/INSTANT | INTERNAL/PUSH/INSTANT | EXTERNAL/PUSH/HOUR |
| `share_result` | HYBRID/PULL/INSTANT | HYBRID/PULL/INSTANT | INTERNAL/PULL/INSTANT | INTERNAL/PUSH/INSTANT | — |

## 矩阵：登录类交互 × 触点

| 交互 \ 触点 | SMS_3RD_PARTY | EMAIL_TRANS | 系统级 OAuth | INAPP_MODAL | PUSH_OS |
|---|---|---|---|---|---|
| `login_phone` | EXTERNAL/PUSH/INSTANT（验证码下发） | — | — | — | — |
| `login_email` | — | EXTERNAL/PUSH/MINUTE（验证链接） | — | — | — |
| `login_wechat` | — | — | HYBRID/PULL/INSTANT | INTERNAL/PUSH/INSTANT（OAuth 回调） | — |
| `login_qr` | — | — | — | INTERNAL/PUSH/INSTANT（显示二维码） | — |
| `login_biometric` | — | — | 系统级 / 设备能力 | INTERNAL/PUSH/INSTANT | — |

## 矩阵：支付类交互 × 触点

| 交互 \ 触点 | INAPP_MODAL | 外部支付 SDK | EMAIL_TRANS | INAPP_REMINDER_CENTER |
|---|---|---|---|---|
| `payment_order` | INTERNAL/PUSH/INSTANT（支付弹窗） | EXTERNAL/PULL/INSTANT | EXTERNAL/PUSH/MINUTE（订单确认） | — |
| `payment_deposit` | INTERNAL/PUSH/INSTANT | EXTERNAL/PULL/INSTANT | EXTERNAL/PUSH/MINUTE | — |
| `payment_refund` | ⚠️ 仅大额退款 | — | EXTERNAL/PUSH/MINUTE（合规披露） | INTERNAL/BOTH/MINUTE（退款进度） |
| `payment_settlement` | — | — | EXTERNAL/PUSH/HOUR（B 端） | INTERNAL/BOTH/HOUR（B 端） |

## 矩阵：订阅类 / 收藏类 / 评价类 / 确认类 × 触点

| 交互 \ 触点 | INAPP_RED_DOT | INAPP_TOAST | INAPP_MODAL | INAPP_REMINDER_CENTER | PUSH_OS | MINI_PROGRAM_MSG | EMAIL_TRANS |
|---|---|---|---|---|---|---|---|
| `subscribe_content` | INTERNAL/PUSH/INSTANT | — | — | INTERNAL/BOTH/MINUTE | — | — | — |
| `subscribe_notification` | — | INTERNAL/PUSH/INSTANT | — | — | EXTERNAL/PUSH/INSTANT（授权提示） | HYBRID/PUSH/MINUTE | — |
| `subscribe_marketing` | — | — | INTERNAL/PUSH/INSTANT（订阅弹窗） | — | — | — | EXTERNAL/PUSH/HOUR |
| `favorite_product` | INTERNAL/PUSH/INSTANT | INTERNAL/PUSH/INSTANT | — | INTERNAL/BOTH/MINUTE | — | — | — |
| `favorite_content` | INTERNAL/PUSH/INSTANT | INTERNAL/PUSH/INSTANT | — | INTERNAL/BOTH/MINUTE | — | — | — |
| `review_service` | — | — | INTERNAL/PUSH/MINUTE | INTERNAL/BOTH/MINUTE（待评价列表） | — | — | — |
| `review_product` | — | — | — | INTERNAL/BOTH/DAY | — | — | EXTERNAL/PUSH/DAY |
| `confirm_arrival` | INTERNAL/PUSH/INSTANT | — | INTERNAL/PUSH/INSTANT | — | — | — | — |
| `confirm_event` | INTERNAL/PUSH/INSTANT | — | INTERNAL/PUSH/HOUR | — | EXTERNAL/PUSH/HOUR | HYBRID/PUSH/HOUR | — |
| `confirm_signature` | — | — | INTERNAL/PUSH/INSTANT | — | — | — | — |

## 选型决策树（PM 视角）

```
1. 用户当前在应用内？
   是 → INAPP_* 系列；否 → 外部/混合渠道
2. 需要用户立即看到？
   是 → INSTANT 触达：SMS / PUSH_OS / INAPP_MODAL
   否 → MINUTE/HOUR/DAY：EMAIL_TRANS / INAPP_REMINDER_CENTER / PUSH_OS
3. 用户需主动操作（如点击）？
   是 → 必须是 PUSH（系统主动推）
   否 → 用户主动查看可考虑 PULL（如消息中心）
4. 合规约束？
   营销 → 必须有退订（EMAIL_MARKETING）
   支付 → 必须有合规披露（payment_refund 必须配 EMAIL_TRANS）
   登录 → 验证码必须有上行通道（SMS_3RD_PARTY）
5. 成本敏感？
   高频推送 → INAPP 系列（边际成本低）
   低频重要 → SMS_3RD_PARTY / CALL_VOICE_AI（成本高但触达强）
```

## 矩阵的扩展

本矩阵随 PM 用例回归定期补全。新增条目时：

1. 确认触点已在 `touchpoint-catalog.md` 登记；
2. 确认交互已在 `interaction-catalog.md` 登记；
3. 在矩阵对应单元格补一行典型组合；
4. 若涉及新交互类别（如 `report_*`、`apply_*`），先在 interaction-catalog.md 加新分类，再回本矩阵补行。

## 矩阵与 governance 的衔接

PM 选定组合后，落 governance 治理伴随文件时使用 `<interaction>-<touchpoint>` 唯一标识，例如：

```yaml
chosen_touchpoints:
  - id: reminder_appointment-sms_3rd_party
    interaction: reminder_appointment
    touchpoint: sms_3rd_party
    channel_attrs:
      side: external
      delivery: push
      latency: instant
    source_material: "src/原始材料/会议纪要-2026-08-15.md#触达方式"
    pm_confirmed: true
  - id: reminder_appointment-push_os
    interaction: reminder_appointment
    touchpoint: push_os
    channel_attrs:
      side: external
      delivery: push
      latency: instant
    source_material: "src/原始材料/PPT-PM评审-2026-08.pptx#通知方式"
    pm_confirmed: true
```

每个被选组合必须有 `pm_confirmed: true` 字段，否则校验器发 `uj.touchpoint_unconfirmed` 警告。
