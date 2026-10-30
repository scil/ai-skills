# Building a project console

A **console** is one note that replaces "which command, in which directory, with which flags". The
reader is *operating*, not reading — so actions come first and everything explanatory is folded
underneath.

It only pays off when the project has recurring operations (start/stop services, apply config, run
a check, run tests). A project with one command does not need one.

## Architecture: four layers, one source of truth

```
button (grid row or Buttons block)   the note — grouped, labelled, with context help; sends a key
  └─ runner command (Shell commands)  one per project: "<P> 控制台", and "<P> 控制台(先确认)" that asks first
       └─ runner (in the repo)        scripts\win\run_for_obsidian_console.ps1: key → one fixed command
            └─ script (in the repo)   the actual logic — committed, reviewable, reusable
                 └─ the real work     docker / python / whatever
```

**The vault holds no logic.** Its config only names the project's runner; the runner names scripts.
Inlining commands into plugin config creates a second source of truth that drifts silently and is
invisible to anyone reading the repo.

**One runner per project** (owner decision 2026-10-22). Every button of a project reaches the same
file, `<repo>\scripts\win\run_for_obsidian_console.ps1`, with a key: `param([string]$Button)` and a
`switch` with one case per key (`'health' { cmd /c "… health.bat < nul"; Done }`) and a `default`
that runs nothing. Registered commands per project:

| Command | Command string | Why |
|---|---|---|
| `<P> 控制台` | `& '<repo>\scripts\win\run_for_obsidian_console.ps1' -Button {{_console_button}}` (PowerShell shell, so the key is escaped) | every button |
| `<P> 控制台(先确认)` | the same, `confirm_execution: true` | destructive, irreversible or noisy buttons |
| one per `{{selection}}` / prompt button | the same file with a fixed key: `-Button test-one -Selection {{selection}}` | the editor or a prompt supplies a value |

A choice from lists that change (hosts, playbooks) needs no command of its own: the key's script
opens a picker window (`obsidian-console` → Buttons that ask what to act on).

A grid row sets the key through the plugin (`console-grid` with `runner` / `confirmRunner`); a
Buttons block is `type link` with the plugin's URI,
`action obsidian://shell-commands/?vault=<vault>&_console_button=<key>&execute=<runner command id>`.
The custom variable `console_button` exists once in `custom_variables`. Adding a button then never
touches `data.json` and never needs Obsidian quit.

## 1. Inventory the operations

Do not invent the button set — derive it. Sources, in order of usefulness:

- The project's own docs (`README`, `CLAUDE.md` / `AGENTS.md` "commands" section) — these are the
  commands the author already decided matter.
- What the user has typed repeatedly this session.
- Setup/teardown steps buried in prose that nobody remembers.

**Fast path for a pnpm/npm monorepo:** the root `package.json` `scripts` block *is* the inventory.
Dump it plus each workspace's scripts in one command, and note ports and prerequisites while you
are there (dev server `--port`, `wrangler dev` defaults to 8787, a static-assets Worker needs the
web `dist` built first):

```powershell
foreach ($p in '.', 'apps/web', 'apps/api') { "=== $p"; (Get-Content "$p/package.json" -Raw | ConvertFrom-Json).scripts | ConvertTo-Json }
```

Every script there maps to one button or is deliberately left out; that decision, made against the
list, takes minutes. Prerequisites become guards in the wrapper (`if not exist apps\web\dist\index.html`
→ print what to run first, `exit /b 1`) rather than prose in the note.

Then ask what becomes *newly possible* because output can now render in a modal. The highest-value
button is usually one that did not exist before: **a health check**. As a flashing console window it
was worthless; as a modal report it is the first thing anyone clicks. See
`windows-scripts.md#health-check-scripts-are-worth-writing`.

## 2. Group by intent

Group by *what the person is trying to do*, not by which tool is involved:

| Group | Contents |
|---|---|
| Daily | start everything · health check · recent logs |
| Config & maintenance | edit config · apply config and restart · stop everything |
| Test & debug | dry-run · real-run · unit tests |
| Web | service UIs (`type link`) |
| Files | key project files (`type link` with `file:///`) |

Five to fifteen buttons is the useful range. Below that a console is overkill; above it, the reader
is scanning rather than seeing.

## 3. Decide each button

Run every candidate through this checklist:

| Question | If yes |
|---|---|
| Does it terminate on its own? | If no, write a bounded variant (`--tail 60`, not `-f`) |
| Is it destructive, irreversible, or physically noticeable? | the confirming runner: a grid row coloured red, orange or yellow; a Buttons link with `execute=<prefix>console-confirm` |
| Is the output more than a couple of lines? | the runners route to `modal`; keep a one-line result one line |
| Does it consume arbitrary user text? | PowerShell shell, invoke the program directly, no `.bat` |
| Does it need a terminal (interactive prompts, TUI, a foreground server)? | Not a button. Leave it as a `file:///` link to a `.bat`, which opens a real console |

"Physically noticeable" is not a joke: a button that plays audio through a speaker in someone's home
deserves the same confirmation as one that deletes data.

## 4. Write the note

The note's layout, its data format, the view script and the layout check are the
`obsidian-console` skill's: a tabbed grid of buttons first, one Markdown table per group, a help
line per button saying what it really runs, everything else in folded cards. The checklist above
decides each row of those tables.

## 5. The "scratch note as input" pattern

When a command should act on text the user writes, add a plain-prose section to the console and a
button that runs the selection:

```
.venv\Scripts\python.exe -m mypackage --say {{selection}}
```

(PowerShell shell, so the plugin escapes the value — see `plugin-config.md`.)

The user writes lines as ordinary paragraphs, selects one, clicks. `{{caret_paragraph}}` is an even
lower-friction variant: put the cursor in a line, no selecting.

This beats a prompt dialog for most cases: the inputs **persist, stay editable, and are visible** —
a dialog forces retyping every time. Have the receiving program fail loudly on empty input ("select
some text first") so a mis-click is not silent.

## 6. Verify before handing over

- Run each script once from a real shell, in the exact invocation form the plugin will use —
  `cmd /c "cd /d <repo> && scripts\win\x.bat < nul"` for the headless ones, and the `.ps1` that
  takes `{{selection}}` **twice**: with no argument (must print its hint and exit 1) and with a real
  keyword. Do this *before* registering — it is the last point where a mistake costs nothing.
- Run the runner once per new key, and once with an unknown key (it must print "Unknown console
  button" and exit non-zero).
- Confirm no command is a follow/tail form.
- Run `obsidian-console`'s `check-console.js <view.js> <note> <data.json> <runner .ps1>` on every
  console note (grid rows and Buttons blocks): each key must be a runner case, each command id and
  alias registered.
- Then hand over with a **safe first test**: a read-only button with visible output. Green means the
  whole chain works, with no side effects.

## Build order

For a new console: **survey → scripts → runner → run each key once → register the runners
(Obsidian quit, once per project) → note → verify.**
Registration is the only step that needs Obsidian closed, so ask for that when the task starts and
do everything else in the meantime; by the time you write `data.json` every alias and command
string has already been exercised. A second console in the same vault reuses the first project's
`scripts\win\` shapes verbatim (`health.bat` + `health.ps1`, `gate.bat` with `goto :fail`, a
`*-one.ps1` for selections, `dev-*.bat` with `title` for long-running windows) — copy and adjust,
do not redesign.

## Maintenance

Adding a button later touches the repo and the note only: a script, one case in the project's
`run_for_obsidian_console.ps1`, and one row (or block) with its help line. `data.json` changes only for
a new project or a new `{{selection}}` / prompt button.

When the project changes ports, paths or procedures, the console's folded memo is the thing that goes
stale first. Keep it thin: state only what has no home in the repo, and link out for the rest.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| A button per command-line flag | Combinatorial explosion; nobody scans 40 buttons |
| Buttons that start foreground servers | Never returns; looks hung |
| Console duplicating repo documentation | Two sources of truth, drifts |
| No context help under the outputs | Only the author can interpret it |
| A button with no grey "what it runs" line | Reader trusts the label; label and script drift apart |
| Prose, tables or link lists sitting open between buttons | The column of buttons stops scanning; the page reads as a document |
| A `{{selection}}` scratch section inside a callout | Folded text is not what the user selects; the button reads nothing |
| Renaming a heading during a layout pass | `[[Console#heading]]` links in other notes break silently |
| Inlining commands in plugin config | Project changes, console silently lies |
| No confirmation on destructive or noisy actions | One stray click, real consequences |
