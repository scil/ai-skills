---
name: obsidian-vault-ops
disable-model-invocation: true
description: Use when creating or editing notes in a local Obsidian vault - writing primers, runbooks, decision records or reference docs, restructuring existing notes, and also building dashboard/control-panel notes whose buttons run shell commands, or configuring community plugins by writing their data.json directly. Trigger for requests mentioning Obsidian, vault, notes, callouts, wikilinks, "write this up as a note", "a note with buttons", the Buttons plugin, or the Shell commands plugin.
---

# Obsidian Vault Ops

Two kinds of work happen in a vault: **authoring** (notes a human reads; fails softly, by being
pitched at the wrong reader) and **wiring** (notes that *do* things via plugins; fails hard — the
running app owns the config JSON, button actions match by exact string, shell interpolation can
execute arbitrary text).

## Non-negotiable rules

1. **Locate the vault fresh, every session.** Users reorganize (project folders, renamed notes).
   Never reuse a path from memory or from earlier in a conversation — search for it.
2. **Obsidian must be fully quit before writing any `.obsidian/**/data.json`.** A running plugin
   holds settings in memory and rewrites the file on its next save, silently discarding your edits.
   Check for the process **in the same script that writes** (a guard line, not a separate earlier
   check — the user may open Obsidian between your survey and your write). For a wiring task, ask
   the user to quit Obsidian at the *start*, so the write step never stalls the task.
3. **Never interpolate a `{{variable}}` into a command that runs under `cmd.exe`.** Shell commands'
   `Shell_CMD.getEscaper()` returns `null` — there is no escaping. Arbitrary text containing
   `& | > "` becomes executable. Use PowerShell or sh, which have real escapers.
4. **A Buttons `action` must match the target command's full name exactly.** Matching is
   `name.toUpperCase() === action.toUpperCase().trim()` against the palette name. Verify
   programmatically (recipe below), never by eye.
5. **Read the plugin's `main.js` to extract schemas; do not guess them.** Hand-authored config with
   an invented field shape can break the plugin. Recipes in `references/plugin-config.md`.

## Workflow

### 1. Survey

**Ask Obsidian where its vaults are — do not sweep the filesystem.** The app keeps a registry of
every vault it has ever opened, including which one is open right now. It is instant, it is
authoritative, and it cannot be fooled by a look-alike folder:

| OS | Registry file |
|---|---|
| Windows | `%APPDATA%\obsidian\obsidian.json` |
| macOS | `~/Library/Application Support/obsidian/obsidian.json` |
| Linux | `~/.config/obsidian/obsidian.json` |

```powershell
# Registered vaults, newest-opened first; `open: true` marks the active one
(Get-Content "$env:APPDATA\obsidian\obsidian.json" -Raw | ConvertFrom-Json).vaults.PSObject.Properties |
    ForEach-Object { [pscustomobject]@{ path = $_.Value.path; open = [bool]$_.Value.open } }
```

Fall back to a filesystem sweep only when that file is missing (Obsidian never installed here, a
portable install, or a vault folder that was copied in but never opened):

```powershell
Get-ChildItem <likely-root> -Recurse -Depth 3 -Filter ".obsidian" -Directory -Force |
    ForEach-Object { $_.Parent.FullName }
```

The sweep also returns look-alikes (other note apps' folders, an abandoned copy of a vault), so
confirm a hit with the user before writing anything.

**When one vault holds several projects**, do not assume the top hit. Pick by evidence, in order:
a folder already named after the project, then the `open: true` vault, then ask. And check what the
*other* projects in that vault already do — `.obsidian/plugins/*/data.json` is shared, so a global
setting like Shell commands' `working_directory` is probably already pointing at someone else's
repo. Have your commands `cd` themselves rather than retargeting it.

```powershell
# What is enabled
Get-Content "<vault>\.obsidian\community-plugins.json"
Get-ChildItem "<vault>\.obsidian\plugins"

# Existing conventions to honour: folder-per-project? frontmatter style? naming?
Get-ChildItem "<vault>" -Recurse -Filter "*.md" | Select-Object -First 20 FullName
```

Match the vault's existing structure and naming. If notes live in project folders, put yours there
too; if an existing note should link to the new one, add the link in both directions.

**When a console already exists for another project, learn its conventions from the config, not by
reading the whole note** — an established console runs to 800+ lines. One line per registered
command tells you the alias prefix, shell choice, confirmation and output routing, and the exact
command-string forms in use:

```powershell
$cfg = Get-Content "<vault>\.obsidian\plugins\obsidian-shellcommands\data.json" -Raw | ConvertFrom-Json
"version $($cfg.settings_version) / working_directory '$($cfg.working_directory)' / $($cfg.shell_commands.Count) commands"
$cfg.shell_commands | ForEach-Object { "{0,-28} shells={1} confirm={2} out={3} | {4}" -f $_.alias,
    ($_.shells | ConvertTo-Json -Compress), $_.confirm_execution, $_.output_handlers.stdout.handler,
    $_.platform_specific_commands.default }
```

Then read only the existing note's frontmatter, its "how the buttons work" card and one group
(a button block plus its grey line) — that is the whole house style. Reuse the same `scripts\win\`
layout and script shapes from that project's repo rather than inventing new ones.

### 2. Author

**Decide the reader and the job before writing.** Who reads this, what vocabulary do they already
have, and will they read it once to act or repeatedly to learn? A document pitched at the wrong
level is the most common failure here, and it is only discovered after delivery. When the reader is
new to the domain, establish the vocabulary in its own section first and reuse it throughout —
do not sprinkle definitions inline as you go.

Then pick a structure that fits the job (`references/document-design.md` has the full patterns):

| Job | Shape |
|---|---|
| Teach a domain | cast → concept cards → architecture (naive, then real) → incidents → methodology → folded self-test → glossary |
| Run something | actions first, every reference table folded underneath |
| Record a decision | context → options → choice → **why the others were rejected** |

Write Obsidian-flavored Markdown, not plain Markdown (`references/obsidian-markdown.md`):

- **Collapsible callouts** (`> [!tip]- title`) for anything the reader does not need on first pass —
  glossaries, cheat sheets, self-test answers. They make a long note read like a short one.
- **Wikilinks with heading anchors** (`[[Note#Heading]]`) so a dashboard points at the exact
  explanation rather than a whole document.
- **Native Mermaid** (```` ```mermaid ````) for architecture; show the design that failed before the
  one that works.
- **Backlink both ways** when adding a companion note — one-directional links rot.

File-level care: match the vault's existing folder shape and naming, avoid `# ^ [ ] |` in filenames,
re-read before editing (notes get moved and hand-edited between turns), and prefer targeted edits
over wholesale rewrites of a note the user may have open.

### 3. Wire (only if button/automation plugins are installed)

Wiring is a two-layer design: a **button** layer (Buttons plugin renders a clickable block) invoking
an **execution** layer (Shell commands registers a shell command as an Obsidian command). Buttons
cannot execute shell directly.

```
```button
name 🩺 Health check
type command
action Shell commands: Execute: <alias>
```
```

Where the palette name is `<Plugin display name>: <palette prefix><alias>`, i.e.
`Shell commands: Execute: <alias>` with default settings.

Design rules that come from real breakage:
- **Call repo scripts, not inlined commands.** Keep one source of truth in the project; the vault
  config just invokes it. Inlined commands go stale silently.
- **Every command must terminate.** A follow-style command (`docker compose logs -f`, `tail -f`)
  never returns and the plugin waits forever. Write a bounded variant.
- **Set `confirm_execution: true`** on anything destructive, irreversible, or physically noticeable
  (stops a service, plays audio in someone's home, deletes data).
- **Route output by size**: `notification` for a line or two, `modal` for a report.

The usual shape of this work is a **project console** — one note grouping every recurring operation.
`references/project-console.md` is the end-to-end recipe: deriving the button set from the project's
own docs, grouping by intent, the per-button checklist, a note skeleton, the "scratch note as input"
pattern, and what to re-verify when adding a button later.

Its layout rule, in one line: **buttons out, everything else folded.** Only three things stay
unfolded — the button block, one grey line under it saying what it really runs, and the plain-prose
scratch section a `{{selection}}` button reads from. Every paragraph, table, warning and link list
goes into a `-` callout whose title carries the headline. Headings stay verbatim (other notes link
to them). Verify with the alias check plus "zero open callouts".

Order the work so nothing waits on the user: **scripts → run each once → register commands →
note → verify.** Scripts and their test runs need nothing from Obsidian; registration is the one
step that needs it quit, and by then you know every alias and command string for certain.

Exact schemas, the data.json protocol, the three proven command-string forms and a reusable
registration script: `references/plugin-config.md`.
Windows script pitfalls (`pause` hanging, `.ps1` encoding) and a health-check skeleton:
`references/windows-scripts.md`.

### 4. Verify

Never hand over unverified wiring. What can be checked without Obsidian running:

```powershell
# JSON is valid and complete
$cfg = Get-Content "<vault>\.obsidian\plugins\obsidian-shellcommands\data.json" -Raw | ConvertFrom-Json
"commands: $($cfg.shell_commands.Count) / version: $($cfg.settings_version)"

# Every button action resolves to a real command alias (rule 4)
$note = Get-Content "<note>.md" -Raw
$aliases = $cfg.shell_commands.alias
$actions = [regex]::Matches($note, 'action Shell commands: Execute: (.+)') |
    ForEach-Object { $_.Groups[1].Value.Trim() }
foreach ($a in $actions) { "{0} {1}" -f $(if($aliases -contains $a){"[ok]"}else{"[MISMATCH]"}), $a }
"unused commands: $(($aliases | Where-Object { $actions -notcontains $_ }) -join ', ')"
```

Also run each underlying script once from a real shell, using the exact invocation form the plugin
will use. Command strings are testable even though the plugin is not.

### 5. Hand off

State plainly what was verified and what only the user can confirm (button rendering, notification
display, prompts). Give them a **safe first test**: a read-only command with visible output, so a
green result proves the whole chain without side effects.

