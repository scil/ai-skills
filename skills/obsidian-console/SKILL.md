---
name: obsidian-console
disable-model-invocation: true
description: Build or extend an Obsidian console note - a tabbed grid of buttons (Dataview view + one Markdown table per group) that run Shell commands, with a switchable help line under each button and folded cards per tab.
---

# Obsidian Console

A **console** is one note a person operates by clicking: one tab per group of operations, a grid of buttons in each tab, the group's folded cards under the grid. This skill owns the note and its rendering. The plumbing under each button (repo scripts, Shell commands registration, the `data.json` protocol, escaping) belongs to `obsidian-vault-ops`; follow it for steps 1 and 3.

## Parts

| Part | Where | Holds |
|---|---|---|
| console note | `<vault>/<Project>/<Project> Console.md` | the `dataviewjs` block first, then a one-line intro, input sections, the folded memo |
| data note | `<vault>/<Project>/<Project> Console buttons.md` | one `## <group>` section per tab: a 按钮 table, then that group's folded cards |
| view | `<vault>/_views/console-grid/view.js` + `view.css` | rendering only; the canonical copy is `assets/console-grid/` in this skill |
| commands | Shell commands' `data.json` | alias → repo script (`obsidian-vault-ops`) |

The vault holds no logic: every button runs a script in the project's repo.

## Steps

1. **Survey** (`obsidian-vault-ops` §1). Done when you know the vault path, the project folder, and that `.obsidian/plugins/dataview/data.json` has `"enableDataviewJs": true`. Without Dataview, the owner installs and enables it; you stop there.
2. **Deploy the view.** Copy `assets/console-grid/view.js` and `view.css` to `<vault>/_views/console-grid/`. When a vault copy already exists and differs, diff it first: edits made there are merged into the skill's asset, then the asset is copied back, so other vaults get them too. Done when the two copies are byte-identical.
3. **Scripts and commands** (`obsidian-vault-ops` §3: scripts → run each once → register). Done when every button's alias exists in `data.json`.
4. **Write the data note** (format below). Done when every group of operations has its section, and every card that explains a group sits in that group's section.
5. **Write the console note** (skeleton below).
6. **Verify**: `node scripts/check-console.js <view.js> "<data note>.md" <shellcommands data.json>`. Done when it exits 0 and prints the button and card counts you expect for every tab.
7. **Hand off.** Say what the check covered and what only the owner can see in reading view: the grid, tab switching, cards folding, links inside cards. Name a read-only button as the safe first click.

## Data note format

```markdown
## 日常

| 按钮 | 动作 | 颜色 | 说明 |
|---|---|---|---|
| 🚀 启动全部服务 | 启动全部服务 | blue | `scripts\win\up.bat` → `docker compose up -d` |
| 🌐 Frigate | http://127.0.0.1:15000 |  | 打开 `http://127.0.0.1:15000` |

> [!tip]- 健康检查看什么(点开)
> …
```

- A tab is a `## ` section whose table has 按钮 as its first header cell. The section heading is the tab label, and the tab order is the section order. Other `##` sections (a field legend, say) are not tabs.
- The column names 按钮 / 动作 / 颜色 / 说明 are the format, matched literally, whatever language the note is in.
- 动作 is a Shell commands alias, which runs `Shell commands: Execute: <alias>`. A value starting with `http://`, `https://` or `file:///` makes the button open that link instead.
- 颜色 is `blue`, `green`, `yellow`, `red`, `purple`, `orange`, or empty. Red marks destructive buttons and yellow marks ones that make noise.
- 说明 is the **help line**: the script, then what it really runs (`` `scripts\win\x.bat` → `docker compose …` ``), read off the script and the registered command. One line. A literal `|` inside a cell is written `\|`.
- Everything in the section except the table is that tab's cards, rendered under its buttons. Cards fold (`> [!type]- title (点开)`), with the headline in the title. The links-to-files card in the files tab may stay open.

## Console note skeleton

````markdown
---
tags: [<project>, 控制台]
---

# <Project> 控制台

```dataviewjs
await dv.view("_views/console-grid", { data: "<Project>/<Project> Console buttons", tabs: true })
```

One-line description. Buttons and cards are edited in [[<Project> Console buttons]]; repo and doc links are in the files tab.

> [!abstract]- 📚 Background notes (点开)

## <input section: Buttons-plugin blocks for {{selection}} commands, plus plain-prose lines to select>

> [!abstract]- 备忘速查(点开)
````

- The grid comes first, directly under the title.
- File and folder links live in the files tab's card, never in the console's prose.
- A `{{selection}}` / `{{caret_paragraph}}` button stays a Buttons block in the console body, beside the plain prose it reads; it acts on a selection in this note.
- `tabs: ["<group>", …]` shows a subset, and `group: "<group>"` renders one grid with no tabs.

## The console's contract

This is what the owner can rely on. Keep it true when editing the view or the notes:

- **Reading view.** A click runs the command in the background, with no console window; the result comes back as a notification or a modal. A command that must stay alive (a foreground server) opens its own real terminal window, and closing that window stops it.
- **ⓘ 说明** sits at the right end of the tab bar. It is one switch for the whole window and shows every button's help line. It and the last open tab are remembered (localStorage) across restarts.
- **A tile turns red** with `Command "…" not found` when its alias matches no registered command.
- **Layout rule**: the button wall is first and always visible; everything else is a folded card.
- **Adding a button touches three places**: the repo script, the Shell commands registration (note the alias), and one row in the group's table with its help line.

## Known limits

- Dataview re-renders on vault changes, so an open card folds back; the tab and the help switch survive.
- DataviewJS gets `dv`, `input` and `app`, but no YAML parser. Frontmatter data works but is hard to read and edit, which is why the data lives in tables.
- Before replacing a live console with a rebuilt copy, diff the live note against the copy's starting point, and merge edits made since then. Other agents and the owner edit consoles between turns.
- Measured 2026-10-21 on Dataview 0.5.68: tabs, cards folding, links inside cards and the ⓘ switch all work in reading view.
