# project-scope

独立项目范围产物 · In/Out/Deferred/Conditional 边界定义。

## 用途

- 当项目边界不清、多个团队可能有重叠、scope creep 风险高时使用
- 当需要"明确写出我们不做什么"时使用
- 当需要在签约/预算/资源决策前形成正式 scope 文件时使用

## 不该用

- 项目边界已经清楚（"修这一个 bug"）
- 已经存在 confirmed 的 scope 文件
- 应该用 user-journey-and-stories（用户旅程）或 product-ux（UX）的场景

## 章节速查

| § | 标题 | 何时填写 |
|---|---|---|
| 1 | 项目元数据 | 起草时 |
| 2 | 范围总览 | Generate 后 |
| 3 | In-Scope | 必有 |
| 4 | Out-of-Scope | 必有（必须有"不做"项的理由） |
| 5 | Deferred | 必有 |
| 6 | Conditional | 必有（"如果预算通过则..."这类） |
| 7 | 来源追溯 | 必有 |
| 8 | 待确认问题 | 必有 |
| 9 | Constitution Compliance | 必有 |

## 与上下游的衔接

- 上游：可参考 background-goal.md（不强制）
- 下游：scope 锁定后，user-journey-and-stories 才能开展
- 同级：与 issue-record 互补 —— scope 定"做什么"，issue-record 列"卡点/风险/待决"

## 验证

```bash
python3 scripts/validate_artifact.py <产物路径> --json
```

其中 `<产物路径>` 是生成的 `project-scope.md`（如 `requirements/REQ-XXX/99-review/support/project-scope.md`）；空模板见 Skill 目录下的 `assets/project-scope-template.md`。
