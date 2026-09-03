from __future__ import annotations

import hashlib
import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "src/stages/001-business-requirements/skills/user-journey/scripts/validate_artifact.py"
SPEC = importlib.util.spec_from_file_location("journey_validator", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def main_doc(status: str = "draft", artifact_id: str = "UJ-TEST") -> str:
    return f'''---
artifact_id: {artifact_id}
version: v0.1
status: {status}
owner: PM
business_fact_owner: PM
goal_decision_owner: PM
reviewer: PM
created_at: 2026-08-28
updated_at: 2026-08-28
confirmed_at: ""
upstream_artifact_id: BG-TEST
---

# 用户旅程

## 预检与摘要
输入成熟度：L3；角色：角色一、角色二；生命周期：阶段一、阶段二。

## 一句话旅程叙事
角色一希望完成业务目标并获得可验证的结果。

## 业务生命周期分解
| 阶段 | 触发事件 | 角色与业务目标 | 可观察结果 | 来源概述 |
|---|---|---|---|---|
| 1.阶段一 | 业务事件 | 角色一完成目标 | 结果产生 | BG-TEST |
| 2.阶段二 | 前置完成 | 角色二交接 | 结果确认 | BG-TEST |

## 角色旅程矩阵
### 角色：角色一
| 阶段 | 触发与行为 | 触点/交接 | 结果与阻碍 | 路径类型 |
|---|---|---|---|---|
| 1.阶段一 | 执行行为 | 业务触点 | 未知阻碍 | normal |
| 2.阶段二 | alternative 行为 | 角色二交接 | 结果确认 | alternative |

## 路径与情绪
情绪与可观察信号：证据不足，标记 UNKNOWN。
路径覆盖：normal / alternative / exception / failure / handoff / recovery。

## 触点、痛点与机会
| ID | 阶段 × 角色 | 触点与行为 | 痛点/阻碍 | 机会（业务结果） |
|---|---|---|---|---|
| UJ-001 | 1.阶段一 × 角色一 | 完成行为 | UNKNOWN | 改善可观察结果 |

## 旅程覆盖与边界
已覆盖主路径和备选路径；异常路径待确认。

## 待确认与风险
异常路径和情绪证据待确认。

## 参考资料
BG-TEST：上游背景目标。
'''


def governance(main_text: str, artifact_id: str = "UJ-TEST") -> str:
    digest = hashlib.sha256(main_text.encode("utf-8")).hexdigest()
    return f'''---
artifact_id: {artifact_id}
main_artifact: user-journey.md
main_version: v0.1
main_sha256: {digest}
status: draft
board_artifact: ""
---

# 用户旅程治理伴随文件
## 类型判断与输入充分度
输入成熟度：L3。
## 主张来源与知识状态
| 主张 | 知识状态 | 来源/位置 | 主文档落点 | 影响 |
|---|---|---|---|---|
| 角色与阶段 | FACT | BG-TEST | 旅程矩阵 | — |
## 澄清记录
Q-001：异常路径待确认；A/B/C；PM；yes。
## HTML 审阅板记录
未生成。
## AI Audit
角色和路径已覆盖，情绪证据不足已标 UNKNOWN。
## PM 确认与变更
待确认。
'''


def write_pair(directory: Path, status: str = "draft", artifact_id: str = "UJ-TEST") -> Path:
    main = directory / "user-journey.md"
    text = main_doc(status, artifact_id)
    main.write_text(text, encoding="utf-8")
    (directory / "user-journey.governance.md").write_text(governance(text, artifact_id), encoding="utf-8")
    return main


def test_neutral_pair_passes() -> None:
    with tempfile.TemporaryDirectory() as temp:
        result = MODULE.validate(write_pair(Path(temp)))
        assert result["ok"], result


def test_missing_companion_is_warning_for_draft() -> None:
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "user-journey.md"
        path.write_text(main_doc(), encoding="utf-8")
        result = MODULE.validate(path)
        assert result["ok"], result
        assert any("Companion file" in warning for warning in result["warnings"])


def test_confirmed_is_rejected() -> None:
    with tempfile.TemporaryDirectory() as temp:
        result = MODULE.validate(write_pair(Path(temp), "confirmed"))
        assert not result["ok"]
        assert any("confirmed" in error for error in result["errors"])


def test_hash_mismatch_is_blocking() -> None:
    with tempfile.TemporaryDirectory() as temp:
        path = write_pair(Path(temp))
        companion = path.with_name("user-journey.governance.md")
        companion.write_text(companion.read_text(encoding="utf-8").replace("main_sha256:", "main_sha256: bad-"), encoding="utf-8")
        result = MODULE.validate(path)
        assert not result["ok"]
        assert any("main_sha256" in error for error in result["errors"])


def test_machine_governance_is_rejected_from_main() -> None:
    with tempfile.TemporaryDirectory() as temp:
        path = write_pair(Path(temp))
        path.write_text(path.read_text(encoding="utf-8") + "\n## Constitution Compliance\n", encoding="utf-8")
        result = MODULE.validate(path)
        assert not result["ok"]
        assert any("governance" in error.lower() for error in result["errors"])


def test_001_requires_meeting_baseline_record() -> None:
    with tempfile.TemporaryDirectory() as temp:
        result = MODULE.validate(write_pair(Path(temp), artifact_id="UJ-001"))
        assert not result["ok"], result
        assert any("飞书会议原文" in error for error in result["errors"])
