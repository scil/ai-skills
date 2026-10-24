---
name: espanso-prompts
disable-model-invocation: true
description: Turn prompts into Espanso text-expansion triggers for Claude Code and Codex. Three entries: mine past sessions (extract, merge similar prompts into intents, rank by frequency), distill the prompts of the current session, or install one prompt the user gives. Use when asked to collect or rank past prompts, to save a prompt from this conversation as a snippet, to add a prompt to Espanso, or to refresh the Espanso prompt set.
---

# Prompts into Espanso

Hand-offs: reviewing one prompt's wording → the `prompt ;` Espanso trigger (a prompt-review prompt); a lesson that belongs in a skill or doc rather than a snippet → [harvest-exp](../harvest-exp/SKILL.md). Origin: [`readme.md`](readme.md).

Pick the entry from the request, run its steps, then the shared steps **Write → Install → Verify → Report**.

| Entry | When | Steps |
|---|---|---|
| **Mine** | "collect / rank my past prompts", "refresh the prompt set" | M1–M4 |
| **Distill** | "save the prompts from this session", "which of today's prompts are worth a snippet" | D1–D2 |
| **Add** | the user gives one prompt (or names one from this conversation) and asks to put it in Espanso | A1 |

## Mine past sessions

Scripts need Python 3.10+ and PyYAML. On Windows run them as `python -I -X utf8 …`: `-I` ignores `PYTHONIOENCODING`, so without `-X utf8` printing Chinese fails with `UnicodeEncodeError` (cp1252). Keep every output in the session scratchpad.

- **M1. Extract.** `scripts/extract_prompts.py <out> [--claude DIR] [--codex DIR]`. Defaults: `~/.claude/projects` and `~/.codex/sessions`; pass `--claude` when the Claude config lives elsewhere (on this user's machine `E:\A\backup\link\.claude\projects`). It drops tool results, meta and compact-summary messages, system reminders, command tags and pasted blocks; dedupes by message id and by same text in the same minute (forked sessions copy their parent's messages under new ids). Codex prompts come from `event_msg` / `user_message` only; `response_item` also carries injected `AGENTS.md` text.
- **M2. Read the noise for what it is.** Exact repeats are mostly acknowledgements (`ok`, `继续`, `commit`): too short to need a snippet. Prompts the agent itself wrote for a new session (start with `Repo <path> (read AGENTS.md first` or `In <repo>, …`) are recorded as user messages; discount them. A pasted review report (`[P1] …`, `发现 N 个问题`) is a real recurring intent: "act on these findings".
- **M3. Group into intents.** Copy `scripts/intents.json` to the scratchpad, then run `scripts/rank_intents.py <out> <intents.json>`. Counts are multi-label and approximate. Read `listing.txt` in chunks (about 700 lines fit one read) and `unmatched.txt` for intents the regexes miss; add a regex per new intent and rerun until the top of the ranking stops changing.
- **M4. Select** by the selection test below, ranking intents by count.

## Distill the current session

- **D1. Collect candidates** from this conversation: prompts the user typed (pasted blocks included, since a pasted prompt is often the one worth keeping) and prompts the session wrote or rewrote at the user's request. Merge versions of one prompt into its final form; keep genuine variants (with / without a step) as separate candidates.
- **D2. Select** by the selection test, then list the survivors with a proposed trigger each and wait for the user to pick. Done when the user has chosen.

## Add a given prompt

- **A1. Take the prompt as given.** The user chose it, so skip the selection test; still flag a line that conflicts with the global instruction file or an existing trigger. Ask for the trigger only when no name follows from the prompt's intent.

## Selection test

Keep a prompt only if it would change what an agent does by default. Drop it when it is:

- a one-off or one project's need → that project's `AGENTS.md` or skill, not a global snippet;
- shorter to type than any trigger (`已改 检查`, `重构`);
- already covered by the global instruction file, settings, or an existing trigger;
- a format the agent already follows (check the repository: `git log` showed 97% Conventional Commits with no rule).

## Shared steps

1. **Write each prompt.** Only the lines that change default behaviour; the global instruction file already carries reply language and term definitions. A skill with `disable-model-invocation: true` never loads on its own, so name its path in the prompt (`按 skill [$fix-bugs](<path>/SKILL.md) …`). Put `$|$` where the user types the subject, and make it the last characters of the replace: Espanso reaches the marker by pressing Left once per character after it, visibly and slowly. So the prompt refers to "the X at the end" and closes with `X：$|$`, in block style `|-` (plain `|` leaves a newline after it). One `$|$` per match; name any other placeholder generically, "the system", and let the session's context fill it. Add a `label:` for Espanso's search bar, and `left_word: true` on every match. Variants of one prompt share one trigger with distinct labels: Espanso shows a pick-one menu. Write their common text once, in a `type: echo` global var in the same match file, and keep in each match only what differs (`{{analogy_steps}}` in `_prompts.yml`); move a small difference out of a shared paragraph into the variant's own lines so the paragraph can be shared. The same whole text under two triggers is one match with `triggers: [...]`.
2. **Install.** Back up each match file you change into the Espanso config root (outside `match/`, so the copy never loads). Match files whose names start with `_` load only when another file imports them: add a new file to the importing file (here `match/_ai.yml`, itself included by `config/ai.yml`, whose `filter_exec` limits these prompts to `Codex.exe|claude.exe`). `%APPDATA%\espanso` is a link to the real folder (`(Get-Item $env:APPDATA\espanso).Target`, here `D:\A\Scoop\persist\Espanso\.espanso`); edit through the real path, since the Edit tool's temp-file write fails with `EEXIST` through the link. Edit with the editor tools or a script that keeps each file's line endings.
3. **Verify.** `scripts/check_espanso.py <match-dir> "_prompts/*.yml"`: parse errors, a trigger that ends with another trigger lacking `left_word` (typing `planreview ;` also fires `review ;`), more than one `$|$`, text after `$|$`, an unimported underscore file, a long line repeated across matches (move it into a global var). The Espanso CLI prints nothing in the agent's shell, so loading cannot be checked from there: ask the user to type one trigger in an empty Claude or Codex input box.
4. **Report** a table — trigger, label, intent, new / rewritten / existing (Mine adds rank and approximate count) — then the files changed, the backup location, and the assumptions made. Done when the check passes and the user has the trigger list.

## Espanso facts this relies on

- A trigger fires when the typed text ends with it. `left_word: true` also requires a word separator (space, comma, newline) before it; `word: true` checks both sides, so a trigger ending in ` ;` would need one more keystroke. Chinese characters are not separators: `请看 review ;` fires, `请看review ;` does not.
- Two matches with the same trigger show a pick-one menu.
- There is no file-level default for match options; `global_vars` share variables, not options. A `type: echo` global var can hold a block of rules shared by several prompts (`{{name}}` in each `replace`).
