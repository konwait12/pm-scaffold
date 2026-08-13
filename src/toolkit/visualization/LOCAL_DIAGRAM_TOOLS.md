# 本地画图工具集成 · Agent 无关

> 所有工具均为开源、本地运行、CLI 可调用，任何 AI Agent 均可使用。
> 不依赖特定 Agent 的内置能力（Figma MCP / frontend-design Skill 等）。

---

## 推荐安装（按零依赖优先级）

### Tier 1: `diagram` — Rust 单二进制，零依赖 ⭐

```bash
# 安装 (需要 Rust)
cargo install --git https://github.com/yingkitw/diagram

# 或下载预编译二进制 (macOS/Linux/Windows)
# https://github.com/yingkitw/diagram/releases
```

**支持格式**: Mermaid, PlantUML, Graphviz DOT, D2 → SVG / PNG / PDF

**常用命令**:
```bash
diagram render input.mmd --output out.svg
diagram render input.mmd --output out.png
diagram render input.puml --output out.svg    # PlantUML
diagram render input.dot --output out.png     # Graphviz

# MCP 模式 (任何 MCP 客户端可调用)
diagram mcp
```

**适用**: 无 Node/Python/Docker 环境，单文件部署。

---

### Tier 2: `mermaid-cli` (mmdc) — 官方 CLI，Markdown 内嵌渲染

```bash
npm install -g @mermaid-js/mermaid-cli
```

**核心能力: Markdown → 渲染后的 Markdown**
```bash
# 提取 .md 中所有 ```mermaid 块 → 渲染为 SVG → 替换为图片引用
mmdc -i input.md -o output.md

# 单图渲染
mmdc -i diagram.mmd -o output.svg
mmdc -i diagram.mmd -o output.png -t dark -b transparent -s 2

# 批量转换
for f in *.mmd; do mmdc -i "$f" -o "${f%.mmd}.svg"; done
```

**适用**: 已有 Node 环境，需要处理含 Mermaid 的 Markdown 文件。

---

### Tier 3: `@neverprepared/mcp-kroki` — 28+ 格式，MCP 服务器

```bash
# 需要 Docker
npx -y @neverprepared/mcp-kroki
```

**支持的图类型**: PlantUML, Mermaid, Graphviz, D2, C4, BPMN, Excalidraw, Vega, Bytefield, 等 28+ 种

**MCP 配置** (claude_desktop_config.json / settings.json):
```json
{
  "mcpServers": {
    "kroki": {
      "command": "npx",
      "args": ["-y", "@neverprepared/mcp-kroki"]
    }
  }
}
```

**适用**: 需要多种图格式，已安装 Docker。

---

### Tier 4: `diagramify-ai` — AI 辅助生成

```bash
npm install -g diagramify-ai
```

**能力**: 分析代码库或自然语言描述 → 生成 Mermaid 图 → SVG/PNG/HTML
```bash
diagramify generate "用户旅程: 求职者浏览职位到投递" --output journey
diagramify render diagram.mmd --format svg
diagramify diff base.mmd modified.mmd
```

**适用**: 需要 AI 从描述/代码中自动生成图。

---

## 按 PM 场景选择

| 场景 | 推荐工具 | 命令 |
|---|---|---|
| 画用户旅程图 (Mermaid) | `mermaid-cli` | `mmdc -i journey.md -o journey-rendered.md` |
| 画功能流程图 | `mermaid-cli` | `mmdc -i functional-flow.md -o functional-flow-rendered.md` |
| 画架构图 (PlantUML/D2) | `diagram` | `diagram render arch.puml -o arch.svg` |
| 画 ER 图/数据模型 | `mermaid-cli` | `mmdc -i erd.mmd -o erd.svg` |
| 画甘特图 | `mermaid-cli` | `mmdc -i gantt.mmd -o gantt.svg` |
| 批量 Markdown→带图的 MD | `mermaid-cli` | `mmdc -i prd.md -o prd-rendered.md` |
| 网页端可交互图 | `diagramify-ai` | `diagramify preview diagram.mmd` |
| Agent 通过 MCP 调用 | `diagram` (MCP) 或 `kroki` (MCP) | `diagram mcp` |
| 无任何依赖 (纯文本) | VS Code 原生 Mermaid 预览 | `Cmd+Shift+V` 打开 .md |

---

## 脚手架集成方式

### 方案 A: CLI 脚本封装 (推荐)

```bash
# src/scripts/render_diagrams.sh
#!/bin/bash
# 将指定 .md 文件中所有 Mermaid 块渲染为 SVG
# 用法: bash render_diagrams.sh requirements/REQ-002-.../001-business-requirements/02-user-journey-stories/journey-and-stories.md

INPUT="$1"
OUTPUT="${INPUT%.md}-rendered.md"

if command -v mmdc &> /dev/null; then
    mmdc -i "$INPUT" -o "$OUTPUT"
    echo "✅ Rendered: $OUTPUT"
elif command -v diagram &> /dev/null; then
    # diagram 逐图渲染
    echo "Using diagram CLI..."
else
    echo "⚠️  No diagram CLI found. Install: npm install -g @mermaid-js/mermaid-cli"
fi
```

### 方案 B: Python 脚本 (无需 Node)

```python
# src/scripts/render_diagrams.py
# 提取 Markdown 中的 Mermaid 块，调用 subprocess 渲染
import subprocess, re, sys
from pathlib import Path

def render_mermaid(md_path: Path):
    text = md_path.read_text()
    blocks = re.findall(r'```mermaid\n(.*?)```', text, re.DOTALL)
    for i, block in enumerate(blocks):
        tmp = md_path.with_suffix(f'.tmp{i}.mmd')
        tmp.write_text(block)
        subprocess.run(['diagram', 'render', str(tmp), '--output', 
                       str(md_path.with_name(f'{md_path.stem}-{i}.svg'))])
        tmp.unlink()
```

### 方案 C: CI 自动化

```yaml
# .github/workflows/render-diagrams.yml
- name: Render Mermaid diagrams
  run: |
    npm install -g @mermaid-js/mermaid-cli
    find requirements/ -name "*.md" -exec mmdc -i {} -o {} \;
```

---

## 对比: Agent 内置 vs 开源工具

| 能力 | Agent 内置 (Claude Code) | 开源本地工具 |
|---|---|---|
| Mermaid 渲染 | VS Code 原生预览 | `mmdc` → SVG/PNG/PDF |
| PlantUML | ❌ | `diagram` / `kroki` |
| D2 图 | ❌ | `diagram` |
| Graphviz DOT | ❌ | `diagram` / `kroki` |
| 批量 Markdown→图 | ❌ | `mmdc -i input.md -o output.md` |
| HTML 原型 | `frontend-design` Skill | `diagramify-ai` |
| FigJam 导出 | Figma MCP | ❌ (需 Figma API) |
| 零依赖本地 | VS Code 预览 | `diagram` (Rust binary) |
| MCP 标准接口 | Figma MCP | `diagram mcp` / `kroki` MCP |

**结论**: Agent 内置能力用于交互式预览和 Figma 协作；开源 CLI/MCP 用于批量渲染、CI 集成、和 Agent 无关的本地持久化输出。
