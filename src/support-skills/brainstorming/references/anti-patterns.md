# AI 常见反模式 · Brainstorming（发散收敛）

> 这些是 AI 在本 Skill 中最容易犯的错误。产物审查遇到以下模式时，应直接进入 Revision 修改或要求人工重新处置。
>
> 注：示例统一用通用业务场景，避免与 `test/skills/` 下的测试夹具业务域同域。

## AP1：把一行想法当事实
- **表现**：L0 输入"想做会员积分活动"，AI 直接写成"平台将为会员开放积分兑换"，把它当成已确认的需求事实。
- **为什么有害**：发散候选的正确知识状态是 `AI_INFERENCE`；一旦被写成事实，下游不再核，误读被固化。
- **修复**：全表保持 `AI_INFERENCE`，直到人工逐条处置；能来自已登记 `SRC-*` 的才可能有 FACT，否则一律推断。

## AP2：只在一个维度发散
- **表现**：只顺着 roles（用户/运营/管理员）展开，忽略了 lifecycle、cancellation、rollback 等其他维度，候选全集中在角色视角。
- **为什么有害**：发散覆盖不全，收敛后输入包漏掉大量可被下游利用的方向，等于没发散过。
- **修复**：扫全 12 维度（lifecycle / roles / normal-alternate-exception-failure-timeout / permission / data condition / handoff / dependency / cancellation / retry / rollback / change-recovery / constraint）；某个维度该跳也要显式注明"为何跳过"。

## AP3：出大量近似重复候选
- **表现**："用户可取消""用户可以退""用户能终止"写成三条候选，意思其实是同一件事。
- **为什么有害**：没有聚类去重的候选表让业务方逐条处置近 40 条重复项，消耗人工且稀释真实信号。
- **修复**：聚类去重；一个独立想法一个 `SCN-XXX`，重复措辞合并进 Evidence 作同义表达，跨维度交叉引用而非拆条。

## AP4：替人工决定 include / exclude / defer / research
- **表现**：AI 在 Human Disposition 列擅自填了"include"或"exclude"。
- **为什么有害**：处置是业务决策，涉及取舍与风险承担；AI 代填等于伪造人工确认（宪法红线）。
- **修复**：AI 填其余所有列，**只有负责人工（business_owner）填处置列**；AI 可以给"推荐处置"，但最终列由人填。

## AP5：research 静默搁置
- **表现**：某个候选"外部供应商是否支持批量接口"无法判定，AI 就没再跟进，也没登记。
- **为什么有害**：`research` 处置本意是"现在无法判定"，静默搁置会让它从记录里消失，问题从不被解决。
- **修复**：`research` 处置登记 issue-record / QuestionRecord 并跟进，明确由谁、何时复核。

## AP6：把 excluded 候选也写回
- **表现**：人工把 `SCN-004` 标为 exclude，AI 仍把它综合进输入包。
- **为什么有害**：写回契约规定只有 `include` 候选进输入包；把被排除项写回会污染下游背景，让 `project-background-goal` 基于已否决的方向展开。
- **修复**：仅 `include` 候选综合成 ≥50 字输入包写入 `project-background-goal`；exclude / defer / research 一律不写回。

## AP7：让过程记录 confirmed
- **表现**：AI 在 `brainstorming-output.md` 的状态字段填了 `confirmed`。
- **为什么有害**：本记录永不产 `confirmed`；过程记录不该有"定稿"感，否则下游误以为候选已全部确认。
- **修复**：记录最高停在 `ready_for_human_review`；只有 `pipeline.py review --decision approve` 可确认下游工作项。

## AP8：在本 skill 解决来源冲突
- **表现**：邮件说"仅老会员可参与"，纪要又说"全员可参与"，AI 直接选一边写进候选并隐藏另一边。
- **为什么有害**：冲突是 `requirement-restate`（复述）阶段的职责；本 skill 只发散本想法，擅自裁决会让业务方不知道存在分歧。
- **修复**：这里是发散阶段；若必须标记，保留双方措辞并注明冲突交由复述阶段处理，本 skill 不做裁决。

## AP9：Evidence / Impact 填占位
- **表现**：候选表里 Evidence 写"待确认"，Impact 空着。
- **为什么有害**：没有依据、没有影响的候选无法被人工处置——它既不知道 AI 为什么这么想，也看不到纳入后果。
- **修复**：Evidence 说明 AI 为什么这么想（原始想法 / SRC-* / 常识推断），Impact 说明对后续旅程/功能/范围的影响；两者都不得为空或占位。