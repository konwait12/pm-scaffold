#!/usr/bin/env python3
"""feishu_fetch.py — 飞书 CLI 材料提取脚本（项目内置，以飞书为主链路）

从飞书文档提取原始需求材料到 requirements/REQ-XXX/00-input/：
  1. 调用 lark-cli docs +fetch 读取文档（markdown 格式）
  2. 清洗：HTML 表格 → Markdown 表格（处理 colspan/rowspan、h8 等 wiki 标签）、
     callout → 引用块、synced_reference/grid/whiteboard/img → 移除并警告、
     cite/a → 链接文本
  3. 脱敏：账号/密码模式替换为 <REDACTED>，长 token 打码
  4. 输出材料文件 + 可选 --register 自动登记 source-register.md

用法:
  python3 src/scripts/feishu_fetch.py <doc-token|url> --output <path.md> [--register] [--register-dir <dir>] [--src-id SRC-001] [--src-title "标题"] [--feishu-domain <domain>]

示例:
  python3 src/scripts/feishu_fetch.py <doc-token> \
    --output requirements/REQ-NNN-<topic>/00-input/SRC-001-<topic>-brd.md \
    --register --src-id SRC-001 --src-title "<src-title>"

依赖: lark-cli 已安装并认证（lark-cli auth status 见 README/04 资源库）。
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

# ── 脱敏模式库 ─────────────────────────────────────────────
SECRET_PATTERNS = [
    # 账号/密码类（中英文冒号）
    (re.compile(r'((?:密码|账号|口令|password|Password|account)\s*[:：]\s*)(\S+)'), r'\1<REDACTED>'),
    # 疑似长 token / 密钥（30+ 位字母数字混合）
    (re.compile(r'\b([A-Za-z0-9_-]{30,})\b'), '<REDACTED>'),
    # URL 中内嵌凭据（https://user:pass@host）
    (re.compile(r'(https?://)([^/@\s]+):([^/@\s]+)@'), r'\1<REDACTED>:<REDACTED>@'),
]

KNOWN_EMPTY_BLOCKS = ('whiteboard', 'grid', 'synced_reference', 'img')
DEFAULT_FEISHU_DOMAIN = 'ccegroup.feishu.cn'


def run_lark_fetch(token: str, scope: str = 'full', doc_format: str = 'markdown',
                   max_depth: int | None = None, start_block_id: str | None = None,
                   detail: str | None = None, fmt: str = 'json') -> dict | str:
    """调用 lark-cli docs +fetch 读取文档。

    身份认证由 Trae Lark 插件外部注入托管，不传 --as / --profile。
    - scope='full' (默认) + fmt='json' + doc_format='markdown'：返回 dict（向后兼容）
    - scope='outline'：返回 pretty XML 字符串（仅大纲，不写正文）
    - scope='section'：需传 start_block_id，返回 dict
    - scope='full' + doc_format='xml' + detail='with-ids'：返回含 block_id 的 XML dict
      （供 extract_sheets / extract_tables 抽内嵌资源）
    """
    cmd = ['lark-cli', 'docs', '+fetch', '--doc', token,
           '--doc-format', doc_format, '--scope', scope, '--format', fmt]
    if max_depth is not None:
        cmd += ['--max-depth', str(max_depth)]
    if start_block_id:
        cmd += ['--start-block-id', start_block_id]
    if detail:
        cmd += ['--detail', detail]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120,
                          encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f'lark-cli 失败: {proc.stderr[:500]}')
    if fmt == 'json':
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f'lark-cli 输出非 JSON: {exc}\n{proc.stdout[:300]}') from exc
    return proc.stdout


def extract_sheets(content: str) -> list[tuple[str, str, str]]:
    """从抓取内容里抽 <sheet> 节点三元组，返回 [(block_id, sheet_id, token)]。

    属性名（实测 lark-cli XML 输出）：id / sheet-id / token，属性顺序不固定；
    markdown 输出里 sheet 节点不含 id，block_id 返回空串。
    """
    matches: list[tuple[str, str, str]] = []
    for m in re.finditer(r'<sheet\b[^>]*>', content):
        tag = m.group(0)
        bid = re.search(r'\bid="([^"]+)"', tag)
        sid = re.search(r'\bsheet-id="([^"]+)"', tag)
        tok = re.search(r'\btoken="([^"]+)"', tag)
        if sid and tok:
            matches.append((bid.group(1) if bid else '', sid.group(1), tok.group(1)))
    return matches


def extract_tables(content: str) -> list[tuple[str, str]]:
    """从 XML 内容里抽 <table id="...">...</table> 节点，返回 [(block_id, table_xml)]。"""
    matches: list[tuple[str, str]] = []
    for m in re.finditer(r'<table\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</table>',
                         content, re.DOTALL):
        matches.append((m.group(1), m.group(0)))
    return matches


def table_xml_to_csv(tbl_xml: str) -> str:
    """<table> DocxXML → CSV 字符串（含表头行）。"""
    import csv as _csv
    import io as _io
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbl_xml, re.DOTALL)
    if not rows:
        return ''
    buf = _io.StringIO()
    writer = _csv.writer(buf)
    for r in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
        cleaned = []
        for c in cells:
            t = re.sub(r'<br\s*/?>', ' ', c)
            t = re.sub(r'<[/!]?[a-zA-Z][^>]*>', '', t)
            t = html.unescape(t).strip()
            cleaned.append(t)
        writer.writerow(cleaned)
    return buf.getvalue().rstrip('\n') + '\n'


def fetch_sheet_csv(token: str, sheet_id: str, range_str: str = 'A1:Z200') -> str:
    """调 lark-cli sheets +csv-get 拉一个 sheet 的 CSV 字符串。"""
    cmd = ['lark-cli', 'sheets', '+csv-get',
           '--spreadsheet-token', token, '--sheet-id', sheet_id,
           '--range', range_str, '--include-row-prefix=false',
           '--format', 'json']
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120,
                          encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f'lark-cli sheets +csv-get 失败: {proc.stderr[:500]}')
    data = json.loads(proc.stdout)
    if not data.get('ok'):
        raise RuntimeError(f"csv-get 返回 ok=false: {data}")
    return data.get('data', {}).get('annotated_csv', '')


def route_embedded_resources(content: str, base_dir: Path) -> tuple[int, int, list[str]]:
    """扫描 XML 内容里的内嵌 <sheet>/<table>，落盘到 base_dir/sheets|tables/。

    返回 (sheet_count, table_count, paths)。
    """
    paths: list[str] = []
    sheets = extract_sheets(content)
    tables = extract_tables(content)

    if sheets:
        sheets_dir = base_dir / 'sheets'
        sheets_dir.mkdir(parents=True, exist_ok=True)
        for _block_id, sheet_id, token in sheets:
            try:
                csv_text = fetch_sheet_csv(token, sheet_id)
            except RuntimeError as exc:
                print(f'  ⚠ sheet {sheet_id} 拉取失败: {exc}', file=sys.stderr)
                continue
            target = sheets_dir / f'{sheet_id}.csv'
            target.write_text(csv_text, encoding='utf-8')
            paths.append(str(target))

    if tables:
        tables_dir = base_dir / 'tables'
        tables_dir.mkdir(parents=True, exist_ok=True)
        for block_id, tbl_xml in tables:
            csv_text = table_xml_to_csv(tbl_xml)
            if not csv_text.strip():
                continue
            target = tables_dir / f'{block_id}.csv'
            target.write_text(csv_text, encoding='utf-8')
            paths.append(str(target))

    return len(sheets), len(tables), paths


def cell_text(cell: str) -> str:
    """单元格：<br> 转空格、去标签、HTML 反转义。

    标签匹配限定为真正的 HTML 标签（<字母 / </字母 / <!），避免表格文本
    中的 "<" 字符（如交互规则「用户点击"<"返回」）被误认为标签起始而
    吞掉后续内容（OBS-002 根因）。"""
    t = re.sub(r'<br\s*/?>', ' ', cell)
    t = re.sub(r'<[/!]?[a-zA-Z][^>]*>', '', t)
    return html.unescape(t).strip()


def table_to_md(tbl: str) -> str:
    """HTML <table> → Markdown 表格。

    colspan 的单元格输出为空占位（信息已由原单元格覆盖），rowspan 同理；
    表头取首个 <tr>；无行时返回空串（调用方跳过）。
    """
    rows = re.findall(r'<tr>(.*?)</tr>', tbl, re.DOTALL)
    md_rows: list[str] = []
    for r in rows:
        cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.DOTALL)
        md_rows.append('| ' + ' | '.join(cell_text(c) for c in cells) + ' |')
    if not md_rows:
        return ''
    header = md_rows[0]
    sep = '|' + '---|' * (header.count('|') - 1)
    return header + '\n' + sep + '\n' + '\n'.join(md_rows[1:])


def sanitize(raw: str) -> tuple[str, list[str]]:
    """清洗 + 脱敏。返回 (文本, 警告列表)。"""
    warnings: list[str] = []

    # 1. 表格转换（先于通用标签清理，保留结构）
    raw = re.sub(r'<table>.*?</table>', lambda m: table_to_md(m.group(0)), raw,
                 flags=re.DOTALL)

    # 2. wiki 特有块：callout → 引用；其余已知空块移除并警告
    raw = re.sub(r'<callout[^>]*>(.*?)</callout>',
                 lambda m: '> 💡 ' + cell_text(m.group(1)), raw, flags=re.DOTALL)
    for kind in KNOWN_EMPTY_BLOCKS:
        before = raw
        raw = re.sub(rf'<{kind}[^>]*>.*?</{kind}>', '', raw, flags=re.DOTALL)
        raw = re.sub(rf'<{kind}[^>]*/>', '', raw)
        if len(raw) < len(before):
            warnings.append(f'移除 {kind} 块（无法转文本）')

    # 3. cite / 链接
    raw = re.sub(r'<cite[^>]*title="([^"]*)"[^>]*>.*?</cite>', r'[\1]', raw, flags=re.DOTALL)
    raw = re.sub(r'<cite[^>]*>.*?</cite>', '', raw, flags=re.DOTALL)
    raw = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', raw, flags=re.DOTALL)

    # 4. 剩余标签与空白（限定真标签，避免文本内 "<" 字符误删）
    raw = re.sub(r'<[/!]?[a-zA-Z][^>]*>', '', raw)
    raw = html.unescape(raw)
    raw = re.sub(r'\n{3,}', '\n\n', raw)
    raw = re.sub(r'[ \t]+\n', '\n', raw)

    # 5. 脱敏
    for pattern, repl in SECRET_PATTERNS:
        raw, n = pattern.subn(repl, raw)
        if n > 0:
            warnings.append(f'脱敏替换 {n} 处（{pattern.pattern[:40]}…）')
    return raw, warnings


def build_header(src_id: str, title: str, token: str) -> str:
    return (f'# {title}（{src_id}）\n\n'
            f'> 来源：飞书文档（doc-id: {token}），经 lark-cli 提取。\n'
            f'> 提取日期：{date.today().isoformat()}，由 `src/scripts/feishu_fetch.py` 生成；'
            f'账号密码等敏感信息已脱敏为 <REDACTED>。\n'
            f'> 测试线说明：本材料为真实 BRD 提取整理，用于脚手架全流程跑测。\n\n---\n\n')


def update_source_register(register_path: Path, src_id: str, title: str, token: str,
                           out_rel: str, feishu_domain: str = DEFAULT_FEISHU_DOMAIN) -> None:
    """在 source-register.md 的表格追加一行（存在表头则复用，否则新建）。"""
    line = (f'| {src_id} | 飞书文档（BRD） | `{out_rel}`'
            f'（原文：https://{feishu_domain}/docx/{token}） | {title} | '
            f'{date.today().isoformat()} | 全流程 |\n')
    if register_path.is_file():
        text = register_path.read_text(encoding='utf-8')
        if '|---' in text and src_id not in text:
            # 追加到表尾：从后往前找最后一个「以 | 开头」的行插到它后面——
            # 是数据行则为真正的表尾；若只有表头+分隔行（无数据行），则插到分隔行后。
            lines = text.splitlines()
            insert_idx = None
            for idx in range(len(lines) - 1, -1, -1):
                if lines[idx].lstrip().startswith('|'):
                    insert_idx = idx + 1
                    break
            if insert_idx is not None:
                lines.insert(insert_idx, line.rstrip('\n'))
                register_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        else:
            register_path.write_text(text + line, encoding='utf-8')
    else:
        register_path.write_text(
            '# 来源登记 (Source Register)\n\n'
            '> 登记所有原始需求材料。格式: SRC-NNN → 材料位置 / URL / 飞书链接\n\n'
            '| 来源 ID | 类型 | 位置 | 摘要 | 登记日期 | 权威范围 |\n'
            '|---|---|---|---|---|---|\n' + line, encoding='utf-8')


def find_requirements_parent(path: Path) -> Path | None:
    """返回路径上方第一个名为 requirements 的目录；没有则返回 None。"""
    return next((parent for parent in path.parents if parent.name == 'requirements'), None)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('token', help='飞书文档 token 或 URL（/docx/ 与 /wiki/ 均可）')
    parser.add_argument('--output', required=True, help='输出材料文件路径')
    parser.add_argument('--register', action='store_true', help='同步更新 source-register.md')
    parser.add_argument('--register-dir', type=Path, default=None,
                        help='登记目录（默认从 --output 向上查找 requirements）')
    parser.add_argument('--src-id', default='SRC-001', help='来源 ID（默认 SRC-001）')
    parser.add_argument('--src-title', default='飞书需求文档', help='材料标题')
    parser.add_argument('--feishu-domain', default=DEFAULT_FEISHU_DOMAIN,
                        help=f'飞书域名（默认 {DEFAULT_FEISHU_DOMAIN}）')
    parser.add_argument('--scope', choices=('full', 'outline', 'section'),
                        default='full',
                        help='抓取范围：full=整文（默认）｜outline=仅大纲（heading+block_id）｜'
                             'section=按 --start-block-id 切片')
    parser.add_argument('--max-depth', type=int, default=3,
                        help='outline heading 层级上限（仅 --scope outline 用，默认 3）')
    parser.add_argument('--start-block-id', default=None,
                        help='section 切片锚点 block_id（仅 --scope section 必填）')
    args = parser.parse_args()
    if not args.register and args.register_dir is not None:
        parser.error('--register-dir requires --register')
    if args.scope == 'section' and not args.start_block_id:
        parser.error('--scope section requires --start-block-id')

    token = args.token.rsplit('/', 1)[-1]
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    # ── E2E-019：outline 模式只写大纲 sidecar，不写正文 ──────────────
    if args.scope == 'outline':
        outline_text = run_lark_fetch(token, scope='outline', doc_format='xml',
                                     max_depth=args.max_depth, detail='with-ids',
                                     fmt='pretty')
        if not isinstance(outline_text, str):
            print('提取失败: outline 模式期望 pretty 文本输出', file=sys.stderr)
            return 1
        outline_md = (f'# {args.src_title} 大纲（{args.src_id}）\n\n'
                      f'> 来源：飞书文档（doc-id: {token}），经 lark-cli --scope outline 提取。\n'
                      f'> 提取日期：{date.today().isoformat()}；max-depth={args.max_depth}。\n\n'
                      f'```xml\n{outline_text}\n```\n')
        outline_path = out.with_suffix(out.suffix + '.outline.md') if out.suffix \
            else Path(str(out) + '.outline.md')
        outline_path.write_text(outline_md, encoding='utf-8')
        heading_count = len(re.findall(r'<h[1-6]\b', outline_text))
        block_id_count = len(re.findall(r'\bid="[^"]+"', outline_text))
        print(f'✅ outline 已写入 {outline_path}'
              f'（heading {heading_count} 条，block_id {block_id_count} 个）')
        return 0

    # ── full / section 模式：抓 markdown → 清洗 → 落盘 ──────────────
    if args.scope == 'section':
        result = run_lark_fetch(token, scope='section',
                                start_block_id=args.start_block_id)
    else:
        result = run_lark_fetch(token)
    if not isinstance(result, dict) or not result.get('ok'):
        print(f"提取失败: {result.get('error', '未知错误') if isinstance(result, dict) else '返回非 dict'}",
              file=sys.stderr)
        return 1
    content = result['data']['document']['content']

    text, warnings = sanitize(content)
    out.write_text(build_header(args.src_id, args.src_title, token) + text, encoding='utf-8')

    print(f'✅ 已写入 {out}（{len(text)} 字符，scope={args.scope}）')
    for w in warnings:
        print(f'  ⚠ {w}')

    # ── E2E-020：full 模式额外抓 XML，路由内嵌 sheet/table ──────────
    if args.scope == 'full':
        try:
            xml_result = run_lark_fetch(token, scope='full', doc_format='xml',
                                        detail='with-ids', fmt='json')
        except RuntimeError as exc:
            print(f'  ⚠ 内嵌资源 XML 抓取失败（跳过 sheet/table 路由）: {exc}',
                  file=sys.stderr)
            xml_result = None
        if isinstance(xml_result, dict) and xml_result.get('ok'):
            xml_content = xml_result['data']['document']['content']
            sheet_n, table_n, paths = route_embedded_resources(xml_content, out.parent)
            print(f'  📎 发现内嵌 sheet {sheet_n} 个 / table {table_n} 个；'
                  f'落盘 {len(paths)} 个 CSV')
            for p in paths:
                print(f'     - {p}')

    if args.register:
        requirements_parent = find_requirements_parent(out)
        if args.register_dir is not None:
            register = args.register_dir / 'source-register.md'
        else:
            register = out.parent / 'source-register.md'
        relative_root = requirements_parent or args.register_dir or out.parent

        try:
            out_rel = out.relative_to(relative_root)
        except ValueError:
            out_rel = Path(out.name)
        register.parent.mkdir(parents=True, exist_ok=True)
        update_source_register(register, args.src_id, args.src_title, token,
                               out_rel.as_posix(), args.feishu_domain)
        print(f'✅ source-register 已更新：{register}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
