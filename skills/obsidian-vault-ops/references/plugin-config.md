# Configuring plugins by writing data.json

Writing a plugin's config file directly saves the user from hand-entering dozens of fields through a
settings UI. It is safe *only* with the protocol below.

## Layout

```
<vault>/.obsidian/
    community-plugins.json        # array of enabled plugin ids
    plugins/<plugin-id>/
        manifest.json             # id, name, version  <- the display name and version live here
        main.js                   # bundled code — the source of truth for schemas
        data.json                 # the plugin's settings (may not exist until first save)
```

`data.json` **missing** means the plugin has never saved settings. That is normal for a freshly
installed plugin, and it means you have no example to copy — extract the schema from `main.js`.

## The protocol

1. **Confirm the app is not running.**
   ```powershell
   Get-Process Obsidian -ErrorAction SilentlyContinue
   ```
   If it is, stop. Ask the user to fully quit (not just close the window). A running plugin holds
   settings in memory and rewrites `data.json` on its next save, silently discarding your work.
2. **Extract the schema from `main.js`** (recipes below). Never invent field names.
3. **Check how settings are loaded.** Most plugins merge with defaults
   (`Object.assign({}, DEFAULTS, await this.loadData())` or similar), so a partial file is fine. If
   they do not merge, you must supply every field.
4. **Set the version field to the installed version** where one exists, so the plugin does not run
   migrations against your file.
5. **Validate the JSON, then back up any existing file, then write.**
6. **Verify by re-reading and parsing** the written file.
7. **Tell the user to reopen and test**, and what to do if the plugin did not pick it up (disable and
   re-enable the plugin, or restart).

## Schema-extraction recipes

Bundled `main.js` is large but greppable. Useful targets:

```powershell
$m = Get-Content "<plugin>\main.js" -Raw

# Default settings object
$i = $m.IndexOf('getDefaultSettings'); $m.Substring($i, 1500)

# Per-item factory (commands, prompts, fields...)
$i = $m.IndexOf('newShellCommandConfiguration'); $m.Substring($i, 1200)

# Registries: valid enum values live here
[regex]::Matches($m, 'registerOutputChannel\("([^"]+)"') | ForEach-Object { $_.Groups[1].Value }

# Class names, to know what exists at all
[regex]::Matches($m, 'class (\w+Escaper|OutputChannel_\w+|Shell_\w+)') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique

# How settings are loaded (does it merge with defaults?)
$i = $m.IndexOf('loadSettings'); $m.Substring($i, 800)
```

**When a feature needs three interlocking schemas you could not extract verbatim, do not hand-author
it.** Pick a simpler mechanism that achieves the same goal, or have the user create that one item
through the settings UI (the plugin then writes correct config itself, at zero risk).

---

# Verified reference: Shell commands (Taitava), v0.23.0

## Top-level settings that matter

| Field | Notes |
|---|---|
| `settings_version` | Set to the installed plugin version (`"0.23.0"`) to skip migrations |
| `working_directory` | Global cwd for all commands — set it once instead of `cd` in every command |
| `obsidian_command_palette_prefix` | Default `"Execute: "`; contributes to the palette name |
| `shell_commands` | Array of command objects |
| `prompts`, `custom_variables`, `builtin_variables` | Needed only for the prompt-dialog feature |

Settings are merged with defaults on load, so a partial file is accepted.

## Command object (verbatim field set)

```json
{
  "id": "unique-id",
  "platform_specific_commands": { "default": "<the command>" },
  "shells": {},
  "alias": "Human readable name",
  "icon": "activity",
  "confirm_execution": false,
  "ignore_error_codes": [],
  "input_contents": { "stdin": null },
  "output_handlers": {
    "stdout": { "handler": "notification", "convert_ansi_code": true },
    "stderr": { "handler": "notification", "convert_ansi_code": true }
  },
  "output_wrappers": { "stdout": null, "stderr": null },
  "output_channel_order": "stdout-first",
  "output_handling_mode": "buffered",
  "execution_notification_mode": null,
  "events": {},
  "debounce": null,
  "command_palette_availability": "enabled",
  "preactions": [],
  "variable_default_values": {}
}
```

**Palette name** = `Shell commands: ` + `obsidian_command_palette_prefix` + `alias`
→ `Shell commands: Execute: <alias>`. This exact string is what a button must target.

**Output handlers**: `ignore`, `notification`, `modal`, `status-bar`, `clipboard`,
`current-file-top`, `current-file-bottom`, `current-file-caret`, `open-files`,
`assign-custom-variables`.
Route by size: one or two lines → `notification`; a report → `modal`.

**Shell selection** — identifiers are the shell's binary name, keyed by platform:

```json
"shells": { "win32": "PowerShell.exe" }
```

Known: `CMD.EXE`, `PowerShell.exe` (5.1), `pwsh.exe` (Core), `bash`, `dash`, `zsh`.
Empty `{}` uses the platform default.

## The three command-string forms (Windows, verified)

Every console button so far is one of these. Pick by the checklist in `project-console.md` §3;
do not compose new forms.

| Job | `platform_specific_commands.default` | `shells` | `output` |
|---|---|---|---|
| Run a repo `.bat` headless, show its output | `cmd /c "cd /d <repo> && scripts\win\<x>.bat < nul"` | `{}` | `modal` (report) / `notification` (a line) |
| Long-running process in its own console window | `cmd /c start "<window title>" "<repo>\scripts\win\<x>.bat"` | `{}` | `ignore` |
| Act on user-selected text | `powershell -NoProfile -ExecutionPolicy Bypass -File "<repo>\scripts\win\<x>.ps1" {{selection}}` | `{"win32":"PowerShell.exe"}` | `modal` |

Absolute repo paths in every string: `working_directory` is global to the vault and already
points at some other project. The `< nul` is what lets a double-clickable `.bat` ending in `pause`
return under the plugin (`windows-scripts.md`).

**One `data.json` serves every project's console**, so give each project an alias prefix
(`门廊 …`, `Composer …`) and an id prefix (`tp-`, `pc-`). The id prefix is what makes
re-registration idempotent (below).

## Registration script (reusable)

Adapt the table, keep the rest. It refuses while Obsidian runs, replaces only this project's
entries, validates, backs up, writes, re-reads. ~1 minute instead of hand-authoring 20 fields ×
N commands.

```powershell
$path = '<vault>\.obsidian\plugins\obsidian-shellcommands\data.json'
if (Get-Process Obsidian -ErrorAction SilentlyContinue) { throw 'Obsidian is running - quit it first.' }
$cfg = Get-Content $path -Raw | ConvertFrom-Json
$repo = '<repo>'

function Cmd($id, $alias, $icon, $command, $out, [bool]$confirm = $false, $shells = @{}) {
    [ordered]@{
        id = $id
        platform_specific_commands = [ordered]@{ default = $command }
        shells = $shells; alias = $alias; icon = $icon
        confirm_execution = $confirm; ignore_error_codes = @()
        input_contents = [ordered]@{ stdin = $null }
        output_handlers = [ordered]@{
            stdout = [ordered]@{ handler = $out; convert_ansi_code = $true }
            stderr = [ordered]@{ handler = $out; convert_ansi_code = $true } }
        output_wrappers = [ordered]@{ stdout = $null; stderr = $null }
        output_channel_order = 'stdout-first'; output_handling_mode = 'buffered'
        execution_notification_mode = $null; events = @{}; debounce = $null
        command_palette_availability = 'enabled'; preactions = @(); variable_default_values = @{}
    }
}
function Bat($name) { "cmd /c `"cd /d $repo && scripts\win\$name.bat < nul`"" }
function Win($title, $name) { "cmd /c start `"$title`" `"$repo\scripts\win\$name.bat`"" }
function Sel($name) { "powershell -NoProfile -ExecutionPolicy Bypass -File `"$repo\scripts\win\$name.ps1`" {{selection}}" }

$prefix = 'pc-'
$new = @(
    (Cmd "${prefix}health"  '<Proj> 项目体检'   'lucide-activity' (Bat 'health')  'modal')
    (Cmd "${prefix}dev-web" '<Proj> Web 开发服务器' 'lucide-monitor' (Win '<Proj> web dev :3000' 'dev-web') 'ignore')
    (Cmd "${prefix}test-one" '<Proj> 跑选中的测试' 'lucide-target' (Sel 'test-one') 'modal' $false @{ win32 = 'PowerShell.exe' })
    (Cmd "${prefix}build"   '<Proj> 打包'       'lucide-disc'     (Bat 'build')   'modal' $true)
)

$cfg.shell_commands = @($cfg.shell_commands | Where-Object { $_.id -notlike "$prefix*" }) + $new
$json = $cfg | ConvertTo-Json -Depth 20
$null = $json | ConvertFrom-Json                       # validate before touching the file
Copy-Item $path "$path.bak-$(Get-Date -Format yyyyMMdd-HHmmss)"
Set-Content -Path $path -Value $json -Encoding UTF8 -NoNewline
$check = Get-Content $path -Raw | ConvertFrom-Json
"commands: $($check.shell_commands.Count) / version: $($check.settings_version)"
```

Icons are Lucide names with the `lucide-` prefix (`lucide-activity`, `lucide-monitor`,
`lucide-shield-check`, `lucide-flask-conical`, `lucide-target`, `lucide-package`, `lucide-drama`).

## Escaping — the security rule

| Shell | Escaper | Safe to interpolate `{{variables}}`? |
|---|---|---|
| `CMD.EXE` | `getEscaper()` returns **`null`** | **No. Never.** |
| `PowerShell.exe` / `pwsh.exe` | `PowerShellEscaper` | Yes |
| `bash` / `dash` / `zsh` | `ShEscaper` | Yes |

A command like `script.bat {{selection}}` under cmd will happily execute whatever `& | > "` the user
had selected. Under PowerShell the same text arrives as one properly quoted argument.

Corollary: when passing arbitrary text, **also skip the `.bat` wrapper** and invoke the target
program directly (`.venv\Scripts\python.exe -m mymodule --say {{selection}}`), because a `.bat` in
the chain re-introduces cmd-level parsing of its arguments.

## Built-in variables (selected)

`selection` · `caret_paragraph` · `clipboard` · `title` · `file_path` · `file_name` · `file_content`
· `note_content` · `folder_path` · `vault_path` · `tags` · `yaml_value` · `date` · `newline` ·
`output` · `passthrough`

- `{{selection}}` — text the user selected. Explicit and precise; empty if nothing is selected, so
  the receiving program should fail loudly with a helpful message rather than silently.
- `{{caret_paragraph}}` — the paragraph containing the cursor. Lower friction than selecting: click
  into a line, press the button.

These two make a **"scratch note as input"** pattern possible: the user keeps a list of lines in a
note, edits them freely, and runs one against a command by selecting it. Usually better than a
prompt dialog — the inputs persist, are editable, and are visible.

## Prompt dialogs — deliberately not hand-authored

The prompt feature requires three interlocking config objects (`custom_variables` entry, `prompts`
entry with fields whose `target_variable_id` points at it, and a `preactions: [{type:"prompt",
enabled:true, prompt_id:...}]` on the command). The defaults for those were not extractable verbatim
in one pass. Prefer the variables above; if a dialog is genuinely required, walk the user through
creating it in the settings UI.

---

# Verified reference: Buttons (shabegom)

Rendered from a fenced ` ```button ` block; **only visible in reading view**.

````markdown
```button
name 🩺 Health check
type command
action Shell commands: Execute: Health check
color blue
```
````

- `type command` — run any Obsidian command, including those registered by other plugins.
- `type link` — open a URL (`http://…`, and `file:///…` for local paths).
- Other types exist (`text`, `template`, `calculate`, `copy`, `chain`, `swap`).
- `color`: `blue`, `green`, `red`, `yellow`, `purple`, `default`.

**Matching is exact.** The plugin does:

```js
allCommands.filter(c => c.name.toUpperCase() === action.toUpperCase().trim())[0]
```

Case-insensitive and trimmed, but otherwise byte-for-byte: one wrong character, a different dash, a
missing plugin prefix, and the button shows `Command "..." not found`. Cross-check every action
against the real command list programmatically before handing over (recipe in SKILL.md).
