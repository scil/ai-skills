# Claude Code — what it does with the file's content

Verified 2026-09-15 against [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) and [debug-your-config](https://code.claude.com/docs/en/debug-your-config). Loading table (file names, chain, budgets) lives in [ai-docs-organizing/references/harness-loading.md](../../../ai-docs-organizing/references/harness-loading.md); this file holds only what changes how you *write* the content.

| Fact | Consequence for the file |
|---|---|
| Reads `CLAUDE.md`, not `AGENTS.md`; `@AGENTS.md` import is the documented bridge; a symlink also works (Windows symlinks need Developer Mode or admin — use the import) | `CLAUDE.md` = `@AGENTS.md` + Claude-only lines |
| Imported files are expanded at launch and consume context in full | `@import` organizes; it does not save tokens |
| Nested `CLAUDE.md` in subdirectories load on demand when files there are read | scope-specific rules go nested; the root stays small |
| `.claude/rules/*.md`: with a `paths:` frontmatter, loaded only when matching files are touched; without it, always loaded. `~/.claude/rules/` for user-level | the real context saver for path-scoped rules; always-loaded rule files are just more root |
| `CLAUDE.local.md` is per-user, should be gitignored | personal preferences never enter `AGENTS.md` |
| Target under 200 lines per file (official) | count lines as well as bytes |
| Block-level HTML comments are stripped before injection | maintainer notes cost Claude nothing (they still reach Codex) |
| CLAUDE.md and auto memory are context, not enforced configuration; `PreToolUse` hooks block unconditionally | every hard rule names its hook or is tagged `advisory` |
| Official add-triggers: same mistake twice · review caught something Claude should have known · you typed a correction you typed before · a new teammate would need it | matches admission criterion c |
| `/init` generates or proposes improvements; `CLAUDE_CODE_NEW_INIT=1` makes it read `AGENTS.md`, `.devin/rules/`, `.windsurf/rules/`, `.clinerules` | a generated file still needs the admission pass — the study found generated files cost more and help nothing |
| `/import` migrates another agent's config (v2.1.213+); `/doctor` proposes trims of inferable content (v2.1.206+); `/context` lists loaded memory files | verification of "is it loaded" is `/context`, not belief |

## Model behaviour notes (official, verified 2026-09-15)

- **Verification instructions cause over-verification** — [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5): "If your prompt contains explicit verification instructions ('include a final verification step for any non-trivial task', 'use a subagent to verify'), remove them: instructions like these cause over-verification on Claude Opus 5, and removing them reduces wasted tokens with no loss in quality." And under Self-correction: "Avoid instructing re-checks it already performs ('double-check your answer', 're-verify before responding'); … these compound with the model's own behavior and add cost without improving results." Consequence: the Verification section carries scoped done-criteria (which check for which change), never "verify your work".
- **Aggressive language over-triggers** — [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices): "Claude Opus 4.5 and Claude Opus 4.6 are also more responsive to the system prompt… The fix is to dial back any aggressive language. Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'." Consequence: no ALWAYS / CRITICAL / IMPORTANT in the file; MUST is reserved for the Boundaries block.
- **Older prescriptive instructions degrade newer models** — [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5): "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality. Review and consider removing older instructions if default performance is better." Consequence: the refresh and review passes ask of every guard whether the current model still trips on it (ai-docs-organizing principle 5: guards are model-relative).
- **Long files thin attention rather than truncate** (observed): a rule at line 300 is received but less often applied. Order by cost of the mistake.
