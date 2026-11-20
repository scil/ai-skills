# Scripts behind a console button (Windows)

The panel runs the runner through Logseq's `runCli` (`console-panel.md` → How a click reaches the runner). The run is headless: no console window, no keyboard input, and the output comes back as Logseq notifications, one per chunk. A script written for a double-click fails in the ways below.

## `pause` hangs a headless run

A `.bat` file written for a double-click usually ends with `pause`, so that the window stays open. In a headless run, nobody presses a key, and the run waits forever.

Redirect stdin from `nul` where the runner calls the script, and keep the script unchanged:

```
cmd /c "cd /d C:\path\to\repo && scripts\win\thing.bat < nul"
```

`pause` reads stdin, gets the end of the input at once, and returns. The same script still works from a double-click.

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

`pwsh` (PowerShell 7+) defaults to UTF-8 and does not need this. If the marker block says
`powershell`, the BOM is required. Most tools write UTF-8 without a BOM, so add it after you write the file.

## Every command must stop

The runner process lives until its command stops. A command that follows or tails never stops, and it keeps running with no window to close:

| Interactive form | Form for a button |
|---|---|
| `docker compose logs -f svc` | `docker compose logs --tail 60 svc` |
| `tail -f app.log` | `Get-Content app.log -Tail 40` |
| `ping -t host` | `ping -n 4 host` |
| `npm run dev` | its own window: `start "dev" cmd /k npm run dev` |

If the interactive form is useful, ship both: `logs.bat` (follows, for a terminal) and `logs-tail.bat` (bounded, for the button).

## Keep one source of truth

Put the real logic in the project repo as a script. The page names only the runner, and the runner names the script. Use `.ps1` for anything with logic (loops, JSON parsing, formatting), with a thin `.bat` wrapper for a double-click:

```bat
@echo off
cd /d "%~dp0..\.."
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\win\thing.ps1"
pause
```

`%~dp0` resolves relative to the script, so the repo can move without breaking anything.

## A health check is the first button to write

A one-shot "is everything alive" report is the button that people click first. A good one:

- checks each moving part and prints a verdict per line (`[OK]` / `[X]` / `[--]`),
- includes the numbers that show degradation, not only up or down (reconnect counts, dropped frames, error tallies),
- says what normal looks like, so the reader does not need to remember,
- ends with the last few error lines, without long path prefixes.

Each output chunk is one notification, so keep the report to a few short sections.

This skeleton served several projects. Its sections: repo, toolchain, dependencies and build
products, ports. Adjust the pins and the artefact/port lists; keep the helpers and the
`[OK] / [! ] / [X ] / [--] / [ON]` vocabulary so consoles read alike:

```powershell
# <Project> health check: read-only. Called by scripts\win\health.bat.
$ErrorActionPreference = 'SilentlyContinue'
$repo = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent

function Newest([string]$path, [string]$filter) {
    if (-not (Test-Path $path)) { return $null }
    (Get-ChildItem $path -Recurse -File -Filter $filter | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime
}
function PortBusy([int]$port) { [bool](Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue) }

Write-Output "===== repo ====="
Push-Location $repo
Write-Output "  branch $(git rev-parse --abbrev-ref HEAD), uncommitted $(@(git status --porcelain).Count)"
Write-Output "  last   $(git log -1 --pretty=format:'%h %s (%cr)')"
Pop-Location

Write-Output ""; Write-Output "===== toolchain ====="
$node = node -v; Write-Output "  [$(if ($node -match '^v24\.') {'OK'} else {'! '})] node $node (.nvmrc wants 24)"
$pnpm = pnpm -v; Write-Output "  [$(if ($pnpm -eq '11.9.0') {'OK'} else {'! '})] pnpm $pnpm (packageManager pins 11.9.0)"

Write-Output ""; Write-Output "===== build products ====="
$dist = Join-Path $repo 'apps\web\dist'
if (Test-Path $dist) {
    if ((Newest (Join-Path $repo 'apps\web\src') '*.ts*') -gt (Get-Item $dist).LastWriteTime) {
        Write-Output "  [! ] apps/web/dist older than src - build first" } else { Write-Output "  [OK] apps/web/dist fresh" }
} else { Write-Output "  [--] apps/web/dist absent - only needed by dev:api" }

Write-Output ""; Write-Output "===== ports ====="
foreach ($p in @(@{ port = 3000; who = 'Vite dev server' }, @{ port = 8787; who = 'wrangler dev' })) {
    Write-Output ("  [{0}] :{1}  {2}" -f $(if (PortBusy $p.port) {'ON'} else {'--'}), $p.port, $p.who)
}
```

Save it with a UTF-8 BOM if it carries any non-ASCII text (the section on the UTF-8 BOM), and run it once
headless: `cmd /c "cd /d <repo> && scripts\win\health.bat < nul"`.

## Passing arbitrary text

Never route text that a person typed through a `.bat` or a `cmd /c` string: `cmd.exe` parses it again, and `& | > "` become commands. Use a form button with a `free` field. The panel sends the text as base64 (`-SelectionB64`), the runner decodes it, and the runner passes it to the program as one PowerShell argument (`console-panel.md` → Form buttons):

```powershell
& "$repo\.venv\Scripts\python.exe" -m mypackage --say $Selection
```

The program handles empty input itself. A button pressed with no text prints "type some text first". It does not fail without a word or with a stack trace.
