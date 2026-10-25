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
| runner | `<repo>\scripts\win\run_for_obsidian_console.ps1` | the project's one entry point: key → one fixed command |
| commands | Shell commands' `data.json` | per project `<P> 控制台` and `<P> 控制台(先确认)` → the runner with `{{_console_button}}` (`obsidian-vault-ops` → `project-console.md`, One runner per project) |

The vault holds no logic: every button sends a key to the project's runner, which runs a script in the repo.

## Steps

1. **Survey** (`obsidian-vault-ops` §1). Done when you know the vault path, the project folder, and that `.obsidian/plugins/dataview/data.json` has `"enableDataviewJs": true`. Without Dataview, the owner installs and enables it; you stop there.
2. **Deploy the view.** Copy `assets/console-grid/view.js` and `view.css` to `<vault>/_views/console-grid/`. When a vault copy already exists and differs, diff it first: edits made there are merged into the skill's asset, then the asset is copied back, so other vaults get them too. Done when the two copies are byte-identical.
3. **Scripts, runner and commands** (`obsidian-vault-ops` §3: scripts → runner → run each key once → register the runners). Done when every key is a case of the runner and the project's runner commands and the `console_button` custom variable exist in `data.json`.
4. **Write the data note** (format below). Done when every group of operations has its section, and every card that explains a group sits in that group's section.
5. **Write the console note** (skeleton below).
6. **Verify**: `node scripts/check-console.js <view.js> "<note>.md" <shellcommands data.json> <runner .ps1>` for the data note and for every console note holding Buttons blocks. Done when it exits 0 and prints the button and card counts you expect for every tab.
7. **Hand off.** Say what the check covered and what only the owner can see in reading view: the grid, tab switching, cards folding, links inside cards. Name a read-only button as the safe first click.

## Data note format

```markdown
## 日常

| 按钮 | 动作 | 颜色 | 说明 |
|---|---|---|---|
| 🚀 启动全部服务 | up | blue | `scripts\win\up.bat` → `docker compose up -d` |
| 🌐 Frigate | http://127.0.0.1:15000 |  | 打开 `http://127.0.0.1:15000` |

> [!tip]- 健康检查看什么(点开)
> …
```

- A tab is a `## ` section whose table has 按钮 as its first header cell. The section heading is the tab label, and the tab order is the section order. Other `##` sections (a field legend, say) are not tabs.
- The column names 按钮 / 动作 / 颜色 / 说明 are the format, matched literally, whatever language the note is in.
- 动作 is a key of the project's runner (with `runner` in the console's `dv.view` call): the view writes it into the custom variable `_console_button` and runs the runner command. A value starting with `http://`, `https://` or `file:///` makes the button open that link instead. Without `runner`, 动作 is a Shell commands alias, as in consoles built before 2026-10-22.
- 颜色 is `blue`, `green`, `yellow`, `red`, `purple`, `orange`, or empty. Red marks destructive buttons, orange ones that change the system or download, yellow ones that make noise; all three run through `confirmRunner`, which asks first.
- 说明 is the **help line**: the script, then what it really runs (`` `scripts\win\x.bat` → `docker compose …` ``), read off the script and the registered command. One line. A literal `|` inside a cell is written `\|`.
- Everything in the section except the table is that tab's cards, rendered under its buttons. Cards fold (`> [!type]- title (点开)`), with the headline in the title. The links-to-files card in the files tab may stay open.
- A `### <subgroup>` heading inside a tab starts a **subgroup**: a small title, its own 按钮 table, its own cards, rendered in order. Lines before the first `###` form an untitled part, so a tab without `###` renders as before. Use subgroups when buttons in one tab depend on different things the owner can swap, e.g. one per piece of hardware (`### PC + DJI 耳机（pc）`), plus one for steps that need no hardware.

## Which buttons a console needs

- **One button per independently verifiable step.** Besides the end-to-end run, every step of a flow that can be checked on its own (capture a frame, recognise it, record from the mic, synthesise speech, play it, reach the model) gets its own button, so the owner finds the broken link by clicking down the chain. Each runs on the flow's own code path (the same device selection, the same backend), not a parallel test path. A step that keeps an artifact the next step can reuse (a still, a clip) gets a second button that reuses the latest one, so one input can be retried without re-capturing it.
- Put these in one tab ordered along the flow, grouped by the hardware each depends on, with a folded card saying what to fix when each one fails. Only a step whose purpose is sound makes sound, and it is colored yellow.

## Console note skeleton

````markdown
---
tags: [<project>, 控制台]
---

# <Project> 控制台

```dataviewjs
await dv.view("_views/console-grid", { data: "<Project>/<Project> Console buttons", runner: "<P> 控制台", confirmRunner: "<P> 控制台(先确认)", tabs: true })
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
- **A tile turns red** with `Command "…" not found` when the runner (or, in an old console, its alias) matches no registered command, or `Custom variable "_console_button" not found`. An unknown key reaches the runner, which prints "Unknown console button" and runs nothing.
- **Layout rule**: the button wall is first and always visible; everything else is a folded card.
- **Adding a button touches the repo and the note only**: the script, one case in `run_for_obsidian_console.ps1`, and one row in the group's table with its help line. No `data.json` edit, no Obsidian restart.
- **Consoles of Buttons blocks** (older notes) reach the same runner with `type link` and `action obsidian://shell-commands/?vault=<vault>&_console_button=<key>&execute=<runner command id>`; the check covers them too.

## Known limits

- Dataview re-renders on vault changes, so an open card folds back; the tab and the help switch survive.
- DataviewJS gets `dv`, `input` and `app`, but no YAML parser. Frontmatter data works but is hard to read and edit, which is why the data lives in tables.
- Before replacing a live console with a rebuilt copy, diff the live note against the copy's starting point, and merge edits made since then. Other agents and the owner edit consoles between turns.
- Measured 2026-10-21 on Dataview 0.5.68: tabs, cards folding, links inside cards and the ⓘ switch all work in reading view. Subgroups (`###`) confirmed in reading view by the owner on 2026-10-25.
