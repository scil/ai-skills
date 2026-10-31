"""Convert Obsidian console notes into the Logseq console-grid block tree.

usage: console2logseq.py OUT MARKER_LINE SOURCE[:mode] ...
  mode data  = a console-grid data note (text before the first ## is skipped)
  mode page  = a console page with ```button blocks (text before the first ## becomes tab 概览)
Prints the outline (Logseq file format, tab indented) to OUT.
"""
import re, sys
from urllib.parse import urlparse, parse_qs

SKIP_CARDS = ('登录信息', '编辑入口', '按钮怎么用')
BS = chr(92)

def clean(line):
    """Make one Obsidian line safe as Logseq block text (outside code spans)."""
    parts = re.split(r'(`[^`]*`)', line)
    for i in range(0, len(parts), 2):
        p = parts[i]
        p = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', p)
        p = re.sub(r'\[\[([^\]]+)\]\]', r'\1', p)
        p = re.sub(r'(^|\s)#(?=[^\s#])', r'\1＃', p)
        p = p.replace('{{', '｛｛').replace('::', '：:')
        parts[i] = p
    return ''.join(parts)

def body_lines(lines):
    out, fence = [], False
    for l in lines:
        if l.strip().startswith('```'):
            fence = not fence; out.append(l); continue
        if fence: out.append(l); continue
        if not l.strip() or re.match(r'^-{3,}\s*$', l.strip()): continue
        l = re.sub(r'^(\s*)[-*] ', r'\1• ', l)
        l = re.sub(r'^#{1,6} (.*)$', r'**\1**', l)
        out.append(clean(l))
    return out

def node(lines, children=None):
    return {'lines': lines, 'children': children or []}

def cells(line):
    row = line.strip().strip('|')
    return [c.replace(BS + '|', '|').strip() for c in re.split(r'(?<!\\)\|', row)]

def button_line(name, action, color, help_):
    return ' | '.join([clean(name), action, color, clean(help_).replace('|', '/')])

def parse_button(block):
    f = {}
    for l in block:
        k, _, v = l.partition(' ')
        f[k] = v.strip()
    name, action, color = f.get('name', ''), f.get('action', ''), f.get('color', '')
    if action.startswith('obsidian://shell-commands/'):
        q = parse_qs(urlparse(action).query)
        key = q.get('_console_button', [''])[0]
        if key:
            if 'confirm' in q.get('execute', [''])[0] and color not in ('orange', 'red', 'yellow'): color = 'orange'
            return [name, key, color]
    if re.match(r'^(https?|file):', action): return [name, action, color]
    return None, f'🔘 {name}：Obsidian 专用按钮（{action}），Logseq 版未迁移'

def convert(text, mode):
    lines = text.splitlines()
    if lines and lines[0] == '---':
        end = lines.index('---', 1); lines = lines[end + 1:]
    groups = []
    group = node(['概览']) if mode == 'page' else None
    if group: groups.append(group)
    box = group
    para, i, last_button = [], 0, None

    def flush_para():
        nonlocal para
        if box is not None:
            ls = body_lines(para)
            if ls: box['children'].append(node(ls))
        para = []

    while i < len(lines):
        l = lines[i]
        if l.startswith('# ') and not l.startswith('## '):
            i += 1; continue
        if l.startswith('## '):
            flush_para(); group = node([clean(l[3:].strip())]); groups.append(group); box = group; last_button = None; i += 1; continue
        if l.startswith('### '):
            flush_para(); box = node([clean(l[4:].strip())]); group['children'].append(box); last_button = None; i += 1; continue
        if box is None:
            i += 1; continue
        if l.startswith('```dataviewjs'):
            flush_para()
            while i < len(lines) and not (lines[i].strip() == '```' and not lines[i].startswith('```dataviewjs')): i += 1
            i += 1; continue
        if l.startswith('```button'):
            flush_para(); blk = []
            i += 1
            while lines[i].strip() != '```': blk.append(lines[i]); i += 1
            i += 1
            b = parse_button(blk)
            if b[0] is None:
                box['children'].append(node([clean(b[1])])); last_button = None
            else:
                last_button = node([button_line(*b, '')]); box['children'].append(last_button); last_button['b'] = b
            continue
        if l.startswith('> [!'):
            flush_para()
            title = re.sub(r'^> \[!\w+\][-+]?\s*', '', l)
            body = []
            i += 1
            while i < len(lines) and lines[i].startswith('>'):
                body.append(lines[i][2:] if lines[i].startswith('> ') else lines[i][1:]); i += 1
            if not any(s in title for s in SKIP_CARDS):
                bl = body_lines(body)
                box['children'].append(node([clean(title)], [node(bl)] if bl else [node(['（空）'])]))
            last_button = None
            continue
        if l.startswith('|'):
            flush_para()
            rows = []
            while i < len(lines) and lines[i].startswith('|'): rows.append(cells(lines[i])); i += 1
            if rows and rows[0][0] == '按钮':
                for c in rows[2:]:
                    box['children'].append(node([button_line(c[0], c[1], c[2] if len(c) > 2 else '', c[3] if len(c) > 3 else '')]))
            else:
                para.extend('| ' + ' | '.join(r) + ' |' for r in rows)
            last_button = None
            continue
        if l.startswith('```'):
            para.append(l); i += 1
            while i < len(lines) and not lines[i].startswith('```'): para.append(lines[i]); i += 1
            if i < len(lines): para.append(lines[i])
            i += 1; continue
        if not l.strip():
            flush_para(); i += 1; continue
        if last_button is not None and not para and l.lstrip()[:1] not in '>#':
            last_button['lines'] = [button_line(*last_button['b'], l.strip())]
            last_button = None; i += 1; continue
        last_button = None
        para.append(l); i += 1
    flush_para()
    for g in groups:
        for c in g['children']:
            c.pop('b', None)
    return [g for g in groups if g['children']]

def emit(n, depth, out):
    pad = '\t' * depth
    out.append(pad + '- ' + n['lines'][0])
    out.extend(pad + '  ' + l for l in n['lines'][1:])
    for c in n['children']:
        c.pop('b', None)
        emit(c, depth + 1, out)

out_path, marker = sys.argv[1], sys.argv[2]
tabs = []
for arg in sys.argv[3:]:
    path, _, mode = arg.rpartition(':')
    if mode not in ('data', 'page'): path, mode = arg, 'data'
    tabs += convert(open(path, encoding='utf-8').read(), mode)
lines = []
emit({'lines': [marker, 'collapsed:: true'], 'children': tabs}, 0, lines)
open(out_path, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
