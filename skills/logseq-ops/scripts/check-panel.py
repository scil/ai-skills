"""Check the console panels in one Logseq OG page file against their runners.

Usage: python -I check-panel.py "<graph>/pages/<page>.md"

For each `console-grid <shell> <runner>` marker block in the page, it:
  - counts the buttons in each tab,
  - lists every button key that is not a case of the runner's switch,
  - parses the runner with the PowerShell parser (needs `pwsh` on PATH).
Exit code 0 when every key is a runner case and the runner parses, else 1.
"""
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

KEY = re.compile(r'^[a-z0-9-]+$')
LINK = re.compile(r'^(https?|file)://')
PARAM = re.compile(r'^[A-Z][A-Za-z0-9]*$')
FIELD_TYPES = {'text', 'select', 'check', 'free'}
MARKER = re.compile(r'`console-grid\s+(\S+)\s+([^`]+)`')
CASE = re.compile(r"^\s*'([^']+)'\s*\{", re.M)
CASE_IN = re.compile(r"^\s*\{\s*\$_\s+-in\s+([^}]+)\}\s*\{", re.M)


def blocks(path):
    """Yield (depth, text) for each block line; continuation lines are skipped."""
    with open(path, encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^(\t*)- (.*)$', line.rstrip('\r\n'))
            if m:
                yield len(m.group(1)), m.group(2)


def button_key(text):
    parts = [p.strip() for p in re.split(r'(?<!\\)\|', text)]
    if len(parts) < 3:
        return None
    if PARAM.match(parts[0]) and len(parts) >= 3 and parts[2] in FIELD_TYPES:
        return None  # a form field line, not a button
    key = parts[1]
    return key if KEY.match(key) or LINK.match(key) else None


def runner_cases(runner):
    with open(runner, encoding='utf-8-sig') as f:
        src = f.read()
    cases = set(CASE.findall(src))
    for group in CASE_IN.findall(src):  # { $_ -in 'a', 'b' } { ... }
        cases.update(re.findall(r"'([^']+)'", group))
    return cases


def runner_parses(runner):
    ps = ("$e=$null; [void][System.Management.Automation.Language.Parser]::ParseFile($args[0],[ref]$null,[ref]$e); "
          "$e | ForEach-Object { $_.Extent.StartLineNumber.ToString() + ': ' + $_.Message }")
    r = subprocess.run(['pwsh', '-NoProfile', '-Command', ps, runner], capture_output=True, text=True, encoding='utf-8')
    return r.stdout.strip()


def main(page):
    lines = list(blocks(page))
    ok = True
    found = False
    for i, (depth, text) in enumerate(lines):
        m = MARKER.search(text)
        if not m:
            continue
        found = True
        runner = m.group(2).strip()
        print(f'panel: {text[:m.start()].strip()}  runner: {runner}')
        cases = runner_cases(runner)
        tabs, tab, keys = {}, None, []
        for d, t in lines[i + 1:]:
            if d <= depth:
                break
            if d == depth + 1:
                tab = t
                tabs[tab] = 0
                continue
            k = button_key(t)
            if k:
                tabs[tab] = tabs.get(tab, 0) + 1
                keys.append(k)
        for name, n in tabs.items():
            print(f'  tab {name}: {n} buttons')
        missing = sorted({k for k in keys if KEY.match(k) and k not in cases})
        print(f'  buttons {len(keys)}, runner keys {len(keys) - sum(1 for k in keys if LINK.match(k))}, runner cases {len(cases)}')
        if missing:
            ok = False
            print('  [X] keys with no runner case: ' + ', '.join(missing))
        errors = runner_parses(runner)
        if errors:
            ok = False
            print('  [X] runner parse errors:\n    ' + errors.replace('\n', '\n    '))
        else:
            print('  [OK] runner parses')
    if not found:
        print('no console-grid marker in ' + page)
        ok = False
    return 0 if ok else 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
