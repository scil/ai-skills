# Building a project console

A **console** is one note that replaces "which command, in which directory, with which flags". The
reader is *operating*, not reading — so actions come first and everything explanatory is folded
underneath.

It only pays off when the project has recurring operations (start/stop services, apply config, run
a check, run tests). A project with one command does not need one.

## Architecture: four layers, one source of truth

```
button (Buttons plugin)         the note — grouped, labelled, with context help
  └─ command (Shell commands)   registration: alias, shell, output routing, confirmation
       └─ script (in the repo)  the actual logic — committed, reviewable, reusable
            └─ the real work    docker / python / whatever
```

**The vault holds no logic.** Its config only names a script in the repo. Inlining commands into
plugin config creates a second source of truth that drifts silently and is invisible to anyone
reading the repo.

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
| Is it destructive, irreversible, or physically noticeable? | `confirm_execution: true` |
| Is the output more than a couple of lines? | route to `modal`, else `notification` |
| Does it consume arbitrary user text? | PowerShell shell, invoke the program directly, no `.bat` |
| Does it need a terminal (interactive prompts, TUI, a foreground server)? | Not a button. Leave it as a `file:///` link to a `.bat`, which opens a real console |

"Physically noticeable" is not a joke: a button that plays audio through a speaker in someone's home
deserves the same confirmation as one that deletes data.

## 4. Write the note

### The layout rule: buttons out, everything else folded

The reader is standing at the console to *click*, so the page must scan as a column of buttons.
Everything that is not a button is folded into a collapsed callout (`> [!type]- title`), and the
note says so in its own "how the buttons work" card so later editors keep the rule.

Exactly three kinds of content stay unfolded:

1. **The button block itself.**
2. **One grey line directly under it** — the script and what the script actually runs, e.g.
   `` `scripts\win\apply-env.bat` → `docker compose up -d --force-recreate frigate` ``. Read it off
   the registered command and the script, never from memory. It is the honesty line: the reader
   glances at it and knows what the click does, and the maintainer sees drift the moment the script
   changes. One line — a second line of explanation belongs in the card below.
3. **Input surfaces** — the plain-prose scratch section a `{{selection}}` / `{{caret_paragraph}}`
   button reads from (§5). It must stay selectable as ordinary body text, so it never goes into a
   callout.

Plus, sparingly, a single one-line orienting sentence at the top of a group ("edit → click A,
verify → click B; both can run at once"). Headings stay as they are — other notes may link
`[[Console#heading]]`, and renaming one silently breaks those links.

Everything else moves into the nearest card: parameter tables, "what happens when you click",
authorization notes, output-file locations, link lists, port tables, even the companion-notes
index. A **warning keeps its force when folded**: the callout *title* stays visible, so put the
headline there ("this button writes to production (open)") and the argument inside. The vault's
convention is a `(点开)` / "(open)" suffix on every collapsed title so the reader knows it opens.

Danger-coloured buttons (red) already say "this is destructive" on the button itself; the folded
danger card next to them is where the *why* and the recovery steps live.

Skeleton worth adapting:

````markdown
---
tags: [project-name, console]
---

# <Project> Console

One-line description. Repo: [path](file:///...)

> [!info]- How the buttons work (open)
> Powered by Buttons + Shell commands. Runs in the background, no console window —
> results come back as notifications or a popup. **Use reading view.**
> Every button is a script under `scripts\win\`; the console holds no logic.
> **The grey line under each button is what it really runs.**
> Layout rule: buttons and their grey line stay visible, everything else is folded.

> [!abstract]- 📚 Background (open)
> - [[Companion primer note]]

## 🚀 Daily

```button
name 🚀 Start everything
type command
action Shell commands: Execute: Start everything
color blue
```
`scripts\win\up.bat` → `docker compose up -d`

```button
name 🩺 Health check
type command
action Shell commands: Execute: Health check
```
`scripts\win\health.bat` → `health.ps1` (read-only)

> [!tip]- How to read the health output (open)
> - `[OK] stream …` — normal. "not connected" with no viewer is also normal (lazy connect).
> - `fps 5.0 / dropped 0` — healthy. fps 0 means the feed died.
> - **reconnect count**: single digits over hours is fine; several per minute means unstable.

… more groups …

---

> [!abstract]- Memo (open)
> Port table, mode-switch steps, hard constraints — anything you would otherwise
> have to remember. Link to repo docs rather than restating them.
> Adding a button touches four places: script → command → button block + grey line → verify.
````

Four things that make the difference between a console only its author can use and one anyone can:

1. **The grey line under every button** — what it really runs. Without it the reader trusts the
   label, and labels drift.
2. **Context help folded under the button** — how to read the output, what "normal" looks like.
   Written once, saves every future "is this bad?".
3. **Warnings where the risk is** — next to the button, not in a preamble nobody reads
   ("changing config needs *apply*, plain restart won't re-read it"). Folded, with the headline in
   the title.
4. **A folded memo at the bottom** — ports, switch procedures, hard constraints. Keep it minimal and
   link to the repo for anything that lives there; a console that duplicates repo docs goes stale.

### Restructuring an existing console

When a console has grown prose between its buttons, do not trim content — *move* it. Every
paragraph, table and link list goes into the nearest card; nothing is deleted in a layout pass.
Rewrite the file whole (it is a structural change), but re-read it first — the user edits these
notes by hand between turns — and keep every heading verbatim.

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
- Cross-check every button `action` against the registered aliases programmatically (recipe in
  `SKILL.md`) — exact-match failures are silent-ish and easy to miss by eye.
- Confirm no command is a follow/tail form.
- Check the layout rule held: button count unchanged, zero open callouts. One line, alongside the
  alias check:

  ```powershell
  "buttons: $(([regex]::Matches($note, '```button')).Count)   open callouts: $(([regex]::Matches($note, '(?m)^> \[!\w+\]([+ ]|$)')).Count)   collapsed: $(([regex]::Matches($note, '(?m)^> \[!\w+\]-')).Count)"
  ```

  (`$note` is the note's raw text, as in the `SKILL.md` recipe. When one `data.json` serves several
  projects' consoles, the "unused commands" list will name the *other* project's aliases — expected,
  not a mismatch.)
- Then hand over with a **safe first test**: a read-only button with visible output. Green means the
  whole chain works, with no side effects.

## Build order

For a new console: **survey → scripts → run each once → register (Obsidian quit) → note → verify.**
Registration is the only step that needs Obsidian closed, so ask for that when the task starts and
do everything else in the meantime; by the time you write `data.json` every alias and command
string has already been exercised. A second console in the same vault reuses the first project's
`scripts\win\` shapes verbatim (`health.bat` + `health.ps1`, `gate.bat` with `goto :fail`, a
`*-one.ps1` for selections, `dev-*.bat` with `title` for long-running windows) — copy and adjust,
do not redesign.

## Maintenance

Adding a button later touches four places: script → command registration → button block **with its
grey line** → re-verification. Adding it in only two produces a button that reports "command not
found"; skipping the grey line produces a button nobody can audit.

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
