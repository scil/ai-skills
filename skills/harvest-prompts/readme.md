# harvest-prompts — where the rules came from

Written on 2026-10-20 after one session mined 3,275 prompts (2026-05 to 2026-10, 490 Claude Code transcripts and 12 Codex sessions) into about 20 Espanso triggers.

- **The selection test** ("would deleting this line change the agent's behaviour?") came from the same session's review of a `git-commit` skill and two commit prompts: most of their text restated defaults. A snippet earns its place only for non-default behaviour, because the user types it exactly when they want something other than the default.
- **Exact-repeat counting was not enough.** The top exact repeats were `commit`, `ok`, `继续`, `push`; the useful intents (act on pasted review findings, explain for a beginner, implement a design prototype) only appeared after grouping by keyword.
- **`left_word` on every match** followed a real clash: `planreview ;` and `codexreview ;` both end with `review ;`. The user tested `left_word: true` in an empty Claude input box and it expanded.
- **Skill paths in prompts**: the shared skills here are slash-command only, so a prompt that only names a skill's topic never loads it.
- **Commit format check**: ThanksPorch's history was 97% Conventional Commits without any rule; the 32 misses were invented types (`copy`, `i18n`, `ui`) and one June stretch of plain sentences. The fix was a one-line `AGENTS.md` rule allowing `copy` and `i18n`, not a snippet.
- Found while installing: the old `anki ;` trigger read a file that no longer existed and expanded to nothing — check every `type: shell` var's path.
