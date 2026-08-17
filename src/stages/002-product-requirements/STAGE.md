# 002 产品需求（Product Requirements）

## 目标（Goal）

把已确认的业务需求转化为产品范围、功能、用户流程和可实现的功能行为。

## 核心问题（Core Questions）

- 什么在范围内、什么在范围外、每个系统拥有什么？
- 哪些功能满足每条已确认的故事？
- 每个功能在正常、替代、失败和恢复路径上如何表现？

## 进入条件（Entry）

Stage 001 已确认，且 `user-stories` work_item 已 confirmed。

## 工作项（Work Items）

1. `feature-list`
2. `functional-flow`
3. `page-design`
4. `interaction-rules`
5. `business-rules`
6. `validation-rules`
7. `state-machine`
8. `exception-handling`
9. `acceptance-criteria`

## 必需输出（Required Outputs）

产品范围、功能清单、功能流程、页面布局、交互规则，以及包含业务、权限、校验、状态、异常和验收规则的逐功能描述。

## 执行顺序依赖链（Dependency Chain）

```
feature-list → functional-flow → page-design → interaction-rules
                         ↓              ↓
                  business-rules   validation-rules
                         ↓              ↓
                  state-machine → exception-handling
                                            ↓
                                    acceptance-criteria
```

## 条件支持（Conditional Support）

当触发条件存在时，进行功能模式的竞品调研、方案评估、字段规则、埋点需求和原型。

## 不做（Do Not）

不要发明不可追溯的功能、用原型替代规则，或编写技术架构和测试用例。

## 人类负责人与退出（Human Owners And Exit）

产品确认方案；业务确认范围一致性；开发与测试在需要时审查可实现性与可验证性。
