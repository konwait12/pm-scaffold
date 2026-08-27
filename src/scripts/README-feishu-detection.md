# 飞书能力扫描与启用询问 — pipeline.py init（v0.6.1）

> 仅在 `pipeline.py init` 流程内增量生效。不动其他 action（status / entry / gate /
> review / reflow / backfill）、不动校验器、不动注册表、不动模板。

## 1. 检测逻辑

`_detect_feishu_capability()`（pipeline.py 内部函数）按顺序扫描：

| 步骤 | 命令 / 路径 | 命中条件 |
|---|---|---|
| 1 | `which lark-cli` | macOS PATH 已注入宿主插件 bin 时返回 0 且 stdout 非空 |
| 2 | `PM_SCAFFOLD_LARK_PLUGIN_ROOT/<ver>/bin/lark-cli` | 仅当显式配置环境变量时扫描插件版本目录；不依赖任何个人绝对路径 |
| 3 | `lark-cli --version`（timeout=5s） | 捕获 stdout 作为 `version` 字段 |

**刻意不跑 `lark-cli auth status`**：宿主环境托管外部凭证注入下可能报
"Credential management is not supported" —— 用 `--version` 判断可执行性即可，
凭证可用性由宿主环境注入，auth 状态无法本地校验。

返回结构（与任务规格严格一致）：

```json
{"lark_cli": true, "lark_plugin": true, "version": "lark-cli version 1.0.68"}
```

`_lark_plugin_version_str()` 取配置的插件根目录下最大版本目录名（如 `1.0.3`），
作为 `feishu-enabled.json` 的 `lark_plugin_version` 字段落盘。

## 2. 询问触发条件

- **触发位置**：`init_requirement()` 末尾（创建骨架 + 写入 audit init 事件 + 打印成功消息之后）
  调用 `_prompt_feishu_integration(req_dir)`。
- **触发频率**：仅 init 一次。后续 status / entry / gate / review / reflow / backfill
  均不触发；其他 action 不读取 `feishu-enabled.json`。
- **触发条件**：`lark_cli=True` 或 `lark_plugin=True`。
  - TTY（`sys.stdin.isatty()` 为真）：主动询问 `[y/N]`，y→启用，N/空/其他→不启用。
  - 非 TTY（CI / 管道 `echo N | python3 ...`）：跳过询问，打印能力扫描结果，
    默认写 `enabled:false`。
- **未检测到飞书能力**：不询问，直接写 `{"enabled": false, "reason": "..."}`。

## 3. 启用决定落盘位置

文件：`requirements/<REQ-NNN-topic>/00-input/feishu-enabled.json`

启用（用户输入 y）：

```json
{
  "enabled": true,
  "detected_at": "2026-08-19",
  "lark_cli_version": "lark-cli version 1.0.68",
  "lark_plugin_version": "1.0.3"
}
```

不启用（用户输入 N / 默认 / 非 TTY）：

```json
{
  "enabled": false,
  "detected_at": "2026-08-19",
  "lark_cli_version": "lark-cli version 1.0.68",
  "lark_plugin_version": "1.0.3"
}
```

未检测到飞书能力：

```json
{
  "enabled": false,
  "reason": "lark-cli and lark plugin not detected"
}
```

落盘在 `00-input/`（与其他输入材料同级）是因为这是「项目的输入决定」，
不是审计事件本身 —— init 已写入 `.audit/events.jsonl` 的 `init` 事件，
飞书启用决定是项目级配置，由后续 lark-cli 集成步骤读取。

## 4. 后续 lark-cli 集成的启用前提

- **前提 1**：`feishu-enabled.json` 存在且 `enabled: true`。
- **前提 2**：lark-cli 在 PATH 中可执行（`which lark-cli` 命中）。
- **前提 3**：lark-cli 凭证由宿主环境注入（不依赖本地 `auth status`）。
- **后续步骤（不在本增量范围内）**：
  - `feishu_fetch.py`（已存在）按本配置读取飞书文档 → 落 `00-input/SRC-*.md`；
  - `prd_publish.py`（已存在）按本配置发布 `prd.md` 到飞书文档。

## 5. 自查清单

- ✅ 仅在 `init_requirement()` 末尾插入 1 行调用 + 3 个新增内部函数。
- ✅ 路径来源为 PATH 或 `PM_SCAFFOLD_LARK_PLUGIN_ROOT`，在 macOS、Windows 和 CI 中均可复现。
- ✅ 未触碰 status / entry / gate / review / reflow / backfill 任一 action。
- ✅ 未触碰 `machine_gate` / `review` / `audit_backfill` 等函数。
- ✅ 未触碰校验器（dor_check / branch_validator / property_check / traceability_check / registry_contract_check / issue-record validator）。
- ✅ 未触碰 `workflow-registry.json` 与 `work_items()` 注册表。
- ✅ 未触碰 `readme-skeleton.md` / `source-register-skeleton.md` 模板。
