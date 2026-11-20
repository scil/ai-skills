---
name: obsidian-vault-ops
disable-model-invocation: true
description: Use when creating or editing notes in a local Obsidian vault: writing primers, runbooks, decision records or reference docs, and restructuring existing notes. Trigger for requests mentioning Obsidian, vault, notes, callouts, wikilinks, or "write this up as a note". A panel of buttons that run project commands is a Logseq console panel (logseq-ops), not an Obsidian note.
---

# Obsidian Vault Ops

This skill covers **authoring**: notes that a person reads. Authoring fails softly, because the note is pitched at the wrong reader. The Obsidian console (buttons that run project commands) was retired on 2026-11-20. Consoles are Logseq panels now, per `logseq-ops`.

## Rules

1. **Locate the vault fresh, every session.** Users reorganize (project folders, renamed notes). Never reuse a path from memory or from earlier in a conversation. Search for it.
2. **Quit Obsidian before you write any `.obsidian/**/data.json`.** A running plugin keeps its settings in memory. On its next save, it writes the file again and your edits are lost. Check for the process in the same script that writes.
3. **Read a plugin's `main.js` to learn its configuration schema. Do not guess it.** A field shape that you invent can break the plugin.

## Workflow

### 1. Survey

**Ask Obsidian where its vaults are. Do not sweep the filesystem.** The app keeps a registry of every vault it opened, and marks the one that is open now:

| OS | Registry file |
|---|---|
| Windows | `%APPDATA%\obsidian\obsidian.json` |
| macOS | `~/Library/Application Support/obsidian/obsidian.json` |
| Linux | `~/.config/obsidian/obsidian.json` |

```powershell
# Registered vaults; `open: true` marks the active one
(Get-Content "$env:APPDATA\obsidian\obsidian.json" -Raw | ConvertFrom-Json).vaults.PSObject.Properties |
    ForEach-Object { [pscustomobject]@{ path = $_.Value.path; open = [bool]$_.Value.open } }
```

If that file is missing (a portable install, or a vault folder that was copied in but never opened), sweep:

```powershell
Get-ChildItem <likely-root> -Recurse -Depth 3 -Filter ".obsidian" -Directory -Force |
    ForEach-Object { $_.Parent.FullName }
```

The sweep also returns look-alikes: other note apps' folders, an old copy of a vault. Ask the user about a hit before you write anything.

If one vault holds several projects, do not assume the top hit. Pick by evidence, in this order: a folder already named after the project, then the `open: true` vault, then ask.

```powershell
# Existing conventions to follow: folder per project? frontmatter style? naming?
Get-ChildItem "<vault>" -Recurse -Filter "*.md" | Select-Object -First 20 FullName
```

Match the vault's structure and naming. If notes live in project folders, put yours there too. If an existing note must link to the new one, add the link in both directions.

### 2. Author

**Decide the reader and the job before you write.** Who reads this? What words do they already know? Will they read it once to act, or many times to learn? A note pitched at the wrong level is the most common failure, and it shows only after delivery. If the reader is new to the domain, define the words in their own section first. Then reuse them, and do not spread definitions through the text.

Then pick a structure that fits the job (`references/document-design.md` has the full patterns):

| Job | Shape |
|---|---|
| Teach a domain | cast → concept cards → architecture (naive, then real) → incidents → methodology → folded self-test → glossary |
| Run something | actions first, every reference table folded underneath |
| Record a decision | context → options → choice → **why the others were rejected** |

Write Obsidian-flavored Markdown, not plain Markdown (`references/obsidian-markdown.md`):

- **Collapsible callouts** (`> [!tip]- title`) for anything the reader does not need on a first pass: glossaries, cheat sheets, self-test answers. A long note then reads like a short one.
- **Wikilinks with heading anchors** (`[[Note#Heading]]`), so that a link points at the exact explanation and not at a whole document.
- **Native Mermaid** (```` ```mermaid ````) for architecture. Show the design that failed before the one that works.
- **Backlink both ways.** If you add a companion note, link it from both notes. A link in one direction rots.

File-level care:

- Match the vault's folder shape and naming.
- Avoid `# ^ [ ] |` in filenames.
- Read a note again before you edit it. Notes get moved and edited by hand between turns.
- Prefer targeted edits to a full rewrite. The user can have the note open.

### 3. Hand off

Say what you wrote and where, and which links you added in both directions.
