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

Skeleton worth adapting:

````markdown
---
tags: [project-name, console]
---

# <Project> Console

One-line description. Repo: [path](file:///...)
📚 Background: [[Companion primer note]]

> [!info]+ How the buttons work
> Powered by Buttons + Shell commands. Runs in the background, no console window —
> results come back as notifications or a popup. **Use reading view.**

## 🚀 Daily

```button
name 🚀 Start everything
type command
action Shell commands: Execute: Start everything
color blue
```

```button
name 🩺 Health check
type command
action Shell commands: Execute: Health check
```

> [!tip]- How to read the health output (click)
> - `[OK] stream …` — normal. "not connected" with no viewer is also normal (lazy connect).
> - `fps 5.0 / dropped 0` — healthy. fps 0 means the feed died.
> - **reconnect count**: single digits over hours is fine; several per minute means unstable.

… more groups …

---

> [!abstract]- Memo (click)
> Port table, mode-switch steps, hard constraints — anything you would otherwise
> have to remember. Link to repo docs rather than restating them.
````

Three things that make the difference between a console only its author can use and one anyone can:

1. **Context help folded under the button** — how to read the output, what "normal" looks like.
   Written once, saves every future "is this bad?".
2. **Warnings where the risk is** — next to the button, not in a preamble nobody reads
   ("changing config needs *apply*, plain restart won't re-read it").
3. **A folded memo at the bottom** — ports, switch procedures, hard constraints. Keep it minimal and
   link to the repo for anything that lives there; a console that duplicates repo docs goes stale.

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

- Run each script once from a real shell, in the exact invocation form the plugin will use.
- Cross-check every button `action` against the registered aliases programmatically (recipe in
  `SKILL.md`) — exact-match failures are silent-ish and easy to miss by eye.
- Confirm no command is a follow/tail form.
- Then hand over with a **safe first test**: a read-only button with visible output. Green means the
  whole chain works, with no side effects.

## Maintenance

Adding a button later touches four places: script → command registration → button block →
re-verification. Adding it in only two produces a button that reports "command not found".

When the project changes ports, paths or procedures, the console's folded memo is the thing that goes
stale first. Keep it thin: state only what has no home in the repo, and link out for the rest.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| A button per command-line flag | Combinatorial explosion; nobody scans 40 buttons |
| Buttons that start foreground servers | Never returns; looks hung |
| Console duplicating repo documentation | Two sources of truth, drifts |
| No context help under the outputs | Only the author can interpret it |
| Inlining commands in plugin config | Project changes, console silently lies |
| No confirmation on destructive or noisy actions | One stray click, real consequences |
