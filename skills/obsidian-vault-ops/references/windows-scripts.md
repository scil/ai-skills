# Making scripts safe to call from a plugin (Windows)

A script written for double-clicking behaves differently when a plugin runs it headless: no console,
no stdin, output captured instead of displayed. These are the failures that result.

## `pause` hangs a headless run

`.bat` files written for double-clicking usually end with `pause` so the window does not vanish.
Under a plugin there is no console; the run can block forever and looks hung.

**Fix — redirect stdin from `nul` at the call site**, keeping the script itself unchanged:

```
cmd /c "cd /d C:\path\to\repo && scripts\win\thing.bat < nul"
```

`pause` reads stdin, gets EOF immediately, and returns. Verified: prints its message and continues.
This keeps one script usable from both the plugin and a double-click.

## `.ps1` with non-ASCII text needs a UTF-8 BOM

`powershell.exe` (Windows PowerShell 5.1) reads a `.ps1` without a BOM as **ANSI**. Any CJK,
accented or symbol characters are mangled, which corrupts string literals and produces baffling
parser errors far from the real cause:

```
Unexpected token '}' in expression or statement.
The string is missing the terminator: ".
```

**Fix:**

```powershell
$c = Get-Content $path -Raw -Encoding UTF8
Set-Content -Path $path -Value $c -Encoding utf8BOM -NoNewline
# verify: first three bytes are EF BB BF
[System.IO.File]::ReadAllBytes($path)[0..2] | ForEach-Object { $_.ToString('X2') }
```

`pwsh` (PowerShell 7+) defaults to UTF-8 and does not need this — but if the launcher says
`powershell`, the BOM is required. Most file-writing tools emit UTF-8 *without* BOM by default, so
this must be done deliberately after writing.

## Every command must terminate

A plugin waits for the process to exit. Anything that follows or tails runs forever:

| Interactive form | Plugin-safe form |
|---|---|
| `docker compose logs -f svc` | `docker compose logs --tail 60 svc` |
| `tail -f app.log` | `Get-Content app.log -Tail 40` |
| `ping -t host` | `ping -n 4 host` |
| `npm run dev` | not suitable for a button — start it detached instead |

Ship both when the interactive form is genuinely useful: `logs.bat` (follows, for a terminal) and
`logs-tail.bat` (bounded, for the button).

## Keep one source of truth

Put the real logic in the **project repo** as a script; let the vault config only invoke it. Commands
inlined into plugin config drift the moment the project changes, and they are invisible to anyone
reading the repo.

Corollary: prefer `.ps1` for anything with logic (loops, JSON parsing, formatting) with a thin `.bat`
wrapper for double-click convenience:

```bat
@echo off
cd /d "%~dp0..\.."
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\win\thing.ps1"
pause
```

`%~dp0` makes the script location-independent — it resolves relative to the script, so the repo can
move without breaking anything.

## Health-check scripts are worth writing

Once a plugin can display output in a modal, a one-shot "is everything alive" script becomes
genuinely useful in a way it never was as a flashing console window. A good one:

- checks each moving part and prints a per-line verdict (`[OK]` / `[X]` / `[--]`),
- includes the numbers that indicate *degradation*, not just up/down (reconnect counts, dropped
  frames, error tallies),
- says what "normal" looks like, so the reader does not need to remember,
- ends with the last few error lines, trimmed of noisy path prefixes.

## Passing arbitrary text

Do not route user-supplied text through a `.bat`. Even under a safe outer shell, the `.bat` layer
re-introduces cmd parsing of its arguments. Invoke the target program directly:

```
.venv\Scripts\python.exe -m mypackage --say {{selection}}
```

with the command's shell set to PowerShell so the plugin's escaper applies. Then handle empty input
explicitly in the program — a button pressed with nothing selected should say "select some text
first", not fail silently or with a stack trace.
