## 分功能详述

### FUN-001: 测试功能

| AC-001 | Given/When/Then | 量化阈值 | 关联目标 | 关联故事 |
|---|---|---|---|---|
| AC-001 | Given 用户已登录, when 提交, then 成功 | ≤3s | G2 | ST-001 |
| AC-002 | Given 网络异常, when 提交, then 重试提示 | — | G2 | ST-001 |
| AC-003 | Given 字段为空, when 提交, then 校验错误 | — | G2 | ST-001 |
