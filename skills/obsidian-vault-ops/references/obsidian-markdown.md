# Obsidian-flavored Markdown

What separates a note that feels native from one that reads like a pasted README.

## Callouts

```markdown
> [!tip] Title
> Body text.

> [!warning]+ Expanded by default
> The `+` suffix renders open.

> [!question]- Collapsed by default
> The `-` suffix renders folded — the reader clicks to reveal.
```

Common types: `note` `abstract` `info` `tip` `success` `question` `warning` `caution` `failure`
`danger` `bug` `example` `quote` `important`.

**The `-` (collapsed) variant is the highest-value formatting device in a long note.** Use it for:

- **Self-test Q&A** — question visible, answer folded. Turns a document a reader skims into one they
  actually learn from.
- **Reference tables** (port lists, glossaries, cheat sheets) that would otherwise bury the
  actionable content.
- **Context help next to a control** — a button with a folded "how to read this output" beneath it.

Callouts nest and contain full Markdown, including tables and code blocks. Indent continuation lines
with `> `.

## Links

| Form | Use |
|---|---|
| `[[Note name]]` | Link to a note (no path needed if the name is unique in the vault) |
| `[[Note name#Heading]]` | Link to a heading inside another note |
| `[[#Heading]]` | Link within the current note — use for a table of contents |
| `[[Note\|display text]]` | Custom link text |
| `![[Note]]` / `![[image.png]]` | **Embed** the target inline rather than link to it |
| `[text](file:///C:/path/to/file)` | Open a file or folder outside the vault |

Traps:

- **Wikilinks are name-based, not path-based.** Renaming or moving a note breaks hand-written links
  unless the name stays the same. After moving a note, grep the vault for its old name.
- **Heading anchors must match the heading text exactly**, including punctuation and emoji. Copy the
  heading rather than retyping it.
- **`file:///` URLs need percent-encoding for non-ASCII and spaces.** A path with CJK characters
  will not resolve as-is: `方案.md` → `%E6%96%B9%E6%A1%88.md`. Encode, or the link silently does
  nothing.
- A `[[wikilink]]` to a note that does not exist yet is legal — it renders as an "unresolved" link
  and creates the note when clicked. Useful for planned notes; verify you did not simply typo.

## Mermaid

Fenced ` ```mermaid ` blocks render natively — no plugin required.

````markdown
```mermaid
flowchart LR
    A["Camera"] --> B["Translator"]
    subgraph BOX["Container"]
        C["Consumer"]
    end
    B --> C
```
````

Keep diagrams simple. Quote node labels containing punctuation, parentheses or CJK: `A["文字 (说明)"]`.
Emoji inside labels generally render but add failure risk in exchange for little value. Use `<br/>`
for line breaks inside a label.

## Frontmatter

```yaml
---
tags: [project-name, topic]
project: Project Name
created: 2026-08-08
status: draft
---
```

Fields become queryable properties. Match whatever convention the vault already uses; if the vault
has none, keep it minimal — `tags` plus one or two facts that would be useful to filter on later.

## Structural conventions worth following

- **One H1** matching the note's purpose; the filename is the identity, the H1 is the title.
- **Table of contents** via `[[#Heading]]` links for anything over ~200 lines. Obsidian has an
  outline pane, but an in-note TOC works in preview, on mobile, and when exported.
- **Horizontal rules (`---`) between major sections** give long notes a scannable rhythm.
- **Companion notes link both ways.** When adding a note that belongs with an existing one, edit the
  existing note too. One-directional links rot.
- **Tables**: Obsidian (and some linters) reformat table column widths on save. Do not be surprised
  when a table you wrote comes back re-padded — it is cosmetic.

## Editing existing notes

- Users reorganize between sessions. **Confirm the file exists at the expected path before editing**;
  if the edit fails, search the vault by name rather than recreating the note.
- Preserve the user's own edits. If a note has changed since you wrote it (new lines, reworded
  content), work around their changes rather than overwriting the file wholesale.
