# Designing a project console

A **console** is one panel that replaces "which command, in which directory, with which flags". The reader operates it and does not read it, so the buttons come first and every explanation is a folded card. `console-panel.md` covers how the panel draws in Logseq. This file covers what goes on it and how the runner behind it works. `runner-scripts.md` covers the scripts that the runner calls.

If the project has recurring operations (start and stop services, apply configuration, run a check, run tests), a console pays off. A project with one command does not need one.

## Architecture: one source of truth

```
button (a block in the panel's data)   grouped, labelled, with a help line; sends a key
  └─ runner (in the repo)              scripts\win\run_for_obsidian_console.ps1: key → one fixed command
       └─ script (in the repo)         the real logic: committed, reviewable, reusable
            └─ the real work           docker / python / whatever
```

The graph holds no logic. The marker block names the project's runner, and the runner names scripts. A command written into the page is a second source of truth that drifts and that nobody reading the repo sees.

**One runner per project** (owner decision 2026-10-22). Every button of a project reaches the same file with a key:

```powershell
param([Parameter(Mandatory = $true)][string]$Button, [string]$Selection = '', [string]$SelectionB64 = '')
$ErrorActionPreference = 'Stop'
switch ($Button) {
    'health' { cmd /c "cd /d <repo> && scripts\win\health.bat < nul"; Done }   # one line: the button's label
    { $_ -in 'tg-on', 'tg-off' } { & "$PSScriptRoot\tg.ps1" -State $Button.Substring(3) }
    default { Write-Output "Unknown console button: $Button"; exit 2 }
}
```

- The `default` case runs nothing. An unknown key prints `Unknown console button` and exits non-zero.
- The runner calls a script that takes a value in-process (`& "$PSScriptRoot\x.ps1" -Line $Selection`), not with `pwsh -File`. `pwsh -File` reads a value that starts with `-` as a parameter name.
- The file name `run_for_obsidian_console.ps1` stays. It dates from the retired Obsidian console, and every project and every panel marker uses it.
- Adding a button touches the repo and the page only: the script, one case in the runner, and one button block with its help line.

## 1. Inventory the operations

Do not invent the button set. Derive it, from these sources in this order:

- The project's own docs: `README`, the commands section of `AGENTS.md` or `CLAUDE.md`. The author already decided that these commands matter.
- What the user typed more than once in this session.
- Setup and teardown steps in prose that nobody remembers.

In a pnpm or npm monorepo, the `scripts` blocks of the `package.json` files are the inventory. Note ports and prerequisites while you read them (a dev server `--port`, `wrangler dev` uses 8787, a static-assets Worker needs the web `dist` built first):

```powershell
foreach ($p in '.', 'apps/web', 'apps/api') { "=== $p"; (Get-Content "$p/package.json" -Raw | ConvertFrom-Json).scripts | ConvertTo-Json }
```

Every script there becomes one button or is left out on purpose. A prerequisite becomes a guard in the script (`if not exist apps\web\dist\index.html` → print what to run first, `exit /b 1`), not prose in a card.

Then ask what a button makes newly possible. The most useful button is usually a **health check**: a one-shot report on every moving part (`runner-scripts.md` has a skeleton).

## 2. Which buttons a console needs

- **One button per independently verifiable step.** The end-to-end run gets a button. Each step of the flow that you can test on its own also gets one: capture a frame, recognise it, record from the mic, synthesise speech, play it, reach the model. Then the owner finds the broken link by clicking down the chain. Each button runs on the flow's own code path (the same device selection, the same backend), not on a parallel test path.
- A step that keeps an artifact the next step can reuse (a still, a clip) gets a second button that reuses the latest one. Then one input can be retried without capturing it again.
- Put these buttons in one tab, in the order of the flow, grouped by the hardware each one depends on. For each one, a folded card says what to fix if it fails. A step that makes sound is colored yellow.

## 3. Decide each button

| Question | If yes |
|---|---|
| Does it not stop on its own? | Write a bounded variant (`--tail 60`, not `-f`). |
| Is it destructive, irreversible, or physically noticeable? | Color it red, orange or yellow, so the panel asks first. |
| Is its output long? | Each output chunk is one Logseq notification. Print a short summary. |
| Does it take arbitrary text? | A form button with a `free` field (`console-panel.md` → Form buttons). |
| Does it need a terminal (prompts, a TUI, a foreground server)? | The script opens its own window (`start "<title>" …`). Closing that window stops it. |

A button that plays audio through a speaker in someone's home is physically noticeable. It needs the same question first as one that deletes data.

## 4. How to group buttons

- **Tabs by what the user wants to do**, not by how it is built. A typical set, in this order:
  1. the product's own features
  2. checks, which find a fault
  3. evaluations, which measure and tune
  4. the machine: start, stop and watch services
  5. configuration and data: privacy, backups
  6. links: web pages, files The most used tab comes first. A button belongs to the tab its user opens to look for it.
- **Checks and evaluations are separate tabs.** A check answers ok or FAIL and finds a fault. An evaluation prints numbers with the parameters that produced them, and, where a decision depends on a threshold, the score of every candidate. If the output of a step always has a quality level (recognition, scoring), the step is an evaluation, also as a link in a flow. The flow's card points to it.
- **Subgroups by what a button acts on**: one piece of hardware, one service, one data store, one feature. If a tab has only one such kind, it has no subgroups.
- **Opposites together**: start and stop of the same thing, install and uninstall, back up and prune.
- **A feature's own tools stay with the feature**: its editor page, its mock run, its sound test. This is also true for a tool that changes configuration. The configuration tab can point to it in a card.
- **Cards go with the buttons they explain**, in that subgroup. A card about several subgroups belongs to the tab: put it before the first subgroup, and make its title name the subgroups it covers. A card or help line that sends the user to a button in another tab names the tab: 「机器」tab 的【🔁 重启 go2rtc】.
- Five to fifteen buttons in a tab is the useful range. Above that, the reader scans instead of seeing.
- When you regroup, move blocks verbatim. Then make sure that the button count and the set of keys did not change: `scripts/check-panel.py` prints the count per tab.

## 5. Buttons that ask what to act on

When a button needs a choice before it runs (which hosts, which playbook, which environment), use one of two forms:

- If the list is short and fixed, use a **form button** (`console-panel.md` → Form buttons). The list lives in the page, so a new value is a page edit.
- If the list changes, use a **picker window**. The key's script opens it, and the button stays an ordinary button. On every click, the script reads its lists again: the files in a folder, the inventories, a header line in each file. Then a new host or playbook shows without a page edit.

The picker is `assets/picker/Show-Picker.ps1`. Copy it next to the runner and dot-source it in the key's script. It is an always-on-top WinForms window with an optional drop-down for one choice and a tick list of targets (`-Single` for one target). An item with a `Blocked` reason shows that reason but cannot be ticked, so the owner sees why it is out. A picker opens its own window with a Cancel button, so do not color its button red, orange or yellow: the owner is not asked twice.

- **Validate again after the window.** An unknown choice, nothing ticked, an unlisted or blocked name, or too many targets each stop with `[X] …`. Give the script parameters for the same values (`-Play`, `-Hosts`), so that it runs and is tested without the window.
- **Copy, do not run, when the action changes a real system** (a server's configuration, its firewall, its users). The script builds the command line, puts it on the clipboard and prints it. The owner reads it and runs it in a terminal. Placeholders left for the owner are UPPERCASE words (`SITE`, `LOGIN`), never `<...>`: bash reads an unreplaced `<` or `>` as a redirection, and `>` can overwrite a file.

## 6. How to write a card

Every card has the same shape, so the owner can scan titles and stop at the first line:

- **Title: the question the card answers**, ending `(点开)`: `关卡失败了先看哪一层?(点开)`, not a topic label.
- **First line: the answer**, plain, with no label in front. A reader who stops here has what they need.
- **Then short sections** under bold labels (`**怎么用**`, `**为什么**`, `**别做**`), a few short lines each. A symptom → cause → fix lookup is a table. Commands, outputs and tables stay verbatim.
- **History last**, in one `**来历:** <date> …` line. Dates and "why it used to be different" stay out of the body.
- **One fact, one card.** Explain a fact once, at the narrowest place that covers every reader. Other cards point to it by tab and button or by card title.
- When you rewrite cards, keep every fact: move it or merge it, never drop it without a word.

A help line (the fourth field of a button) is the script, then what it really runs: `` `scripts\win\x.bat` → `docker compose …` ``. Read it off the script, not from memory. One line.

## 7. Verify before handing over

1. Run each script once from a real shell, in the form the runner uses: `cmd /c "cd /d <repo> && scripts\win\x.bat < nul"` for the headless ones. Run a script that takes text twice: with no text (it must print its hint and exit 1) and with real text.
2. Run the runner once per new key, and once with an unknown key: `pwsh -NoProfile -File <runner> -Button nope` must print `Unknown console button` and exit non-zero.
3. Make sure that no command follows or tails.
4. Run `python -I scripts/check-panel.py "<graph>/pages/<page>.md"`. It must exit 0: every key is a runner case, and the runner parses. One lost line break in the runner fails every button.
5. Do the steps of `console-panel.md` → Check a panel.
6. Hand over with a **safe first click**: a read-only button with visible output. A good result proves the whole chain with no side effects.

## Build order

For a new console: survey → scripts → runner → run each key once → panel blocks → verify. Nothing waits on Logseq except the first panel in a new graph (`console-panel.md` → Set up a graph once). A second console reuses the first project's `scripts\win\` shapes verbatim (`health.bat` + `health.ps1`, `gate.bat` with `goto :fail`, `dev-*.bat` with `title` for long-running windows). Copy and adjust; do not redesign.

## Maintenance

When the project changes ports, paths or procedures, the console's cards go stale first. Keep them thin: state only what has no home in the repo, and link out for the rest.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| A button per command-line flag | Nobody scans 40 buttons. |
| A button that starts a foreground server in the runner | It never returns. Open its own window instead. |
| A console that repeats the repo's documentation | Two sources of truth drift. |
| A button with no help line | The reader trusts the label, and label and script drift apart. |
| Notes and tables open between buttons | The buttons stop scanning, and the panel reads as a document. Fold them into cards. |
| A command written into the page instead of the repo | The project changes, and the console lies. |
| No confirmation on a destructive or noisy button | One stray click has real effects. |
