---
name: obsidian-vault-ops
description: Use when working inside an Obsidian vault - authoring or restructuring notes, building dashboard/control-panel notes with clickable buttons, wiring notes to shell commands or scripts, or configuring community plugins by writing their data.json directly. Trigger for requests mentioning Obsidian, vault, callouts, wikilinks, "a note with buttons", the Buttons plugin, the Shell commands plugin, or "make a note that runs X".
---

# Obsidian Vault Ops

Two kinds of work happen in a vault: **authoring** (notes a human reads) and **wiring** (notes that
*do* things via plugins). Authoring is forgiving. Wiring is not: plugin config lives in JSON files
that the running app owns, button actions are matched by exact string, and shell interpolation can
execute arbitrary text. This skill encodes the failure modes that are invisible until they bite.

## Non-negotiable rules

1. **Locate the vault fresh, every session.** Users reorganize (project folders, renamed notes).
   Never reuse a path from memory or from earlier in a conversation — search for it.
2. **Obsidian must be fully quit before writing any `.obsidian/**/data.json`.** A running plugin
   holds settings in memory and rewrites the file on its next save, silently discarding your edits.
   Check for the process, ask the user to quit, then write.
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

```powershell
# Find the vault (a folder containing .obsidian)
Get-ChildItem <likely-root> -Recurse -Depth 3 -Filter ".obsidian" -Directory -Force

# What is enabled
Get-Content "<vault>\.obsidian\community-plugins.json"
Get-ChildItem "<vault>\.obsidian\plugins"

# Existing conventions to honour: folder-per-project? frontmatter style? naming?
Get-ChildItem "<vault>" -Recurse -Filter "*.md" | Select-Object -First 20 FullName
```

Match the vault's existing structure and naming. If notes live in project folders, put yours there
too; if an existing note should link to the new one, add the link in both directions.

### 2. Author

Write Obsidian-flavored Markdown, not plain Markdown — callouts, wikilinks, collapsible sections and
native Mermaid are what make a note feel native. See `references/obsidian-markdown.md`.

High-value patterns:
- **Collapsible callouts** (`> [!tip]- title`) for reference material that would otherwise bury the
  actionable content — memos, glossaries, self-test answers.
- **Wikilinks with heading anchors** (`[[Note#Heading]]`) so a dashboard can point at the exact
  explanation instead of a whole document.
- **Backlink both ways** when adding a companion note.

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
- Details, exact schemas and the full data.json protocol: `references/plugin-config.md`.
- Windows script pitfalls (`pause` hanging, `.ps1` encoding): `references/windows-scripts.md`.

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

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Writing plugin config while Obsidian runs | Overwritten on next plugin save |
| `{{selection}}` in a cmd.exe command | No escaper; text becomes executable |
| Guessing a plugin's config schema | Silent load failure or reset settings |
| Button action typed by hand | Exact-match failure, no obvious error |
| Inlining project commands into vault config | Two sources of truth, drifts silently |
| A button that runs a follow/tail command | Never returns; looks hung |
| Reusing a remembered vault path | Users reorganize; writes land in the wrong place |

## References

- `references/obsidian-markdown.md` — callouts, wikilinks, embeds, Mermaid, frontmatter, `file:///`
  links and their encoding traps.
- `references/plugin-config.md` — the data.json protocol, schema-extraction recipes, and verified
  reference for Shell commands + Buttons.
- `references/windows-scripts.md` — making scripts safe to call from a plugin on Windows.
