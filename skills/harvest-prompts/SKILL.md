---
name: harvest-prompts
disable-model-invocation: true
description: Mine the prompts the user typed into Claude Code and Codex, merge similar ones into intents, rank them by frequency, and turn the recurring ones that change agent behaviour into Espanso text-expansion triggers. Use when asked to collect, rank or organize past prompts, to find which prompts are worth a snippet, or to refresh the Espanso prompt set.
---

# Harvest past prompts into Espanso

Hand-offs: reviewing one prompt's wording → the `prompt ;` Espanso trigger (a prompt-review prompt); a lesson that belongs in a skill or doc rather than a snippet → [harvest-exp](../harvest-exp/SKILL.md). Origin: [`readme.md`](readme.md).

Scripts need Python 3.10+ and PyYAML. On Windows run them as `python -I -X utf8 …`: `-I` ignores `PYTHONIOENCODING`, so without `-X utf8` printing Chinese fails with `UnicodeEncodeError` (cp1252). Keep every output in the session scratchpad.

## Path

1. **Extract.** `scripts/extract_prompts.py <out> [--claude DIR] [--codex DIR]`. Defaults: `~/.claude/projects` and `~/.codex/sessions`; pass `--claude` when the Claude config lives elsewhere (on this user's machine `E:\A\backup\link\.claude\projects`). It drops tool results, meta and compact-summary messages, system reminders, command tags and pasted blocks; dedupes by message id and by same text in the same minute (forked sessions copy their parent's messages under new ids). Codex prompts come from `event_msg` / `user_message` only; `response_item` also carries injected `AGENTS.md` text.
2. **Read the noise for what it is.** Exact repeats are mostly acknowledgements (`ok`, `继续`, `commit`): too short to need a snippet. Prompts the agent itself wrote for a new session (start with `Repo <path> (read AGENTS.md first` or `In <repo>, …`) are recorded as user messages; discount them. A pasted review report (`[P1] …`, `发现 N 个问题`) is a real recurring intent: "act on these findings".
3. **Group into intents.** Copy `scripts/intents.json` to the scratchpad, then run `scripts/rank_intents.py <out> <intents.json>`. Counts are multi-label and approximate. Read `listing.txt` in chunks (about 700 lines fit one read) and `unmatched.txt` for intents the regexes miss; add a regex per new intent and rerun until the top of the ranking stops changing.
4. **Select.** Rank intents by count, then keep an intent only if a snippet would change what an agent does by default. Drop it when it is:
   - a one-off or one project's need → that project's `AGENTS.md` or skill, not a global snippet;
   - shorter to type than any trigger (`已改 检查`, `重构`);
   - already covered by the global instruction file, settings, or an existing trigger;
   - a format the agent already follows (check the repository: `git log` showed 97% Conventional Commits with no rule).
5. **Write each prompt.** Only the lines that change default behaviour; the global instruction file already carries reply language and term definitions. A skill with `disable-model-invocation: true` never loads on its own, so name its path in the prompt (`按 skill [$fix-bugs](<path>/SKILL.md) …`). Put `$|$` where the user types the subject (one per match), a `label:` for Espanso's search bar, and `left_word: true` on every match.
6. **Install.** Back up the match files first (the Espanso folder is usually not a git repository). Match files whose names start with `_` load only when another file imports them: add the new file to the importing file (here `match/_ai.yml`, itself included by `config/ai.yml`, whose `filter_exec` limits these prompts to `Codex.exe|claude.exe`). Edit with the editor tools or a script that keeps each file's line endings.
7. **Verify.** `scripts/check_espanso.py <match-dir> "_prompts/*.yml"`: parse errors, a trigger that ends with another trigger lacking `left_word` (typing `planreview ;` also fires `review ;`), more than one `$|$`, an unimported underscore file. The Espanso CLI prints nothing in the agent's shell, so loading cannot be checked from there: ask the user to type one trigger in an empty Claude or Codex input box.
8. **Report** a table — rank, intent, approximate count, trigger, new / rewritten / existing — then the files changed, the backup location, and the assumptions made. Done when the check passes and the user has the trigger list.

## Espanso facts this relies on

- A trigger fires when the typed text ends with it. `left_word: true` also requires a word separator (space, comma, newline) before it; `word: true` checks both sides, so a trigger ending in ` ;` would need one more keystroke. Chinese characters are not separators: `请看 review ;` fires, `请看review ;` does not.
- Two matches with the same trigger show a pick-one menu.
- There is no file-level default for match options; `global_vars` share variables, not options. A `type: echo` global var can hold a block of rules shared by several prompts (`{{name}}` in each `replace`).
