# Codex — what it does with the file's content

Verified 2026-09-15 against [learn.chatgpt.com/docs/agent-configuration/agents-md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) (the `developers.openai.com/codex/guides/agents-md` URL redirects there) and the probe in [ai-docs-organizing/references/harness-loading.md](../../../ai-docs-organizing/references/harness-loading.md).

| Fact | Consequence for the file |
|---|---|
| Chain: `~/.codex/AGENTS.override.md` else `~/.codex/AGENTS.md`; then from repo root down to cwd, at each level `AGENTS.override.md`, then `AGENTS.md`, then `project_doc_fallback_filenames` | only files on the root→cwd path load; a sibling subtree's file is never seen |
| Files are joined with blank lines, root first; "files closer to your current directory override earlier guidance" by position | nested files carry only deltas; contradictions resolve silently in favour of the nested file |
| `project_doc_max_bytes` = 32 KiB combined; "Codex stops adding files once the combined size reaches the limit" — no notice | budget the chain in bytes for every start directory; the global file counts |
| No import syntax; `CLAUDE.md` means nothing to it | `AGENTS.md` is the canonical file; a rule only in `CLAUDE.md` never reaches Codex |
| HTML comments are not documented as stripped | maintainer comments are sent — keep them short or put them in `CLAUDE.md`'s bridge |
| Hooks: `.codex/hooks.json`, same event names as Claude Code | a forbidden command or path can be a hook here too |
| Approval/sandbox is user config (`approval_policy`, `sandbox_mode`); with `never` + `danger-full-access` the instruction file is the only behavioural layer | the Boundaries block at the top matters most for this harness |

## What OpenAI says belongs in the file ([Codex best practices](https://learn.chatgpt.com/guides/best-practices), verified 2026-09-15)

- "A good AGENTS.md covers: repo layout and important directories; how to run the project; build, test, and lint commands; engineering conventions and PR expectations; constraints and do-not rules; what done means and how to verify work."
- "A short, accurate AGENTS.md is more useful than a long file full of vague rules. Start with the basics, then add new rules only after you notice repeated mistakes."
- "If AGENTS.md starts getting too large, keep the main file concise and reference task-specific markdown files for things like planning, code review, or architecture."
- Three levels: `~/.codex/AGENTS.md` for personal defaults, the repo file for shared standards, subdirectory files for local rules; "if there's a more specific file closer to your current directory, that guidance wins."
- Divergence from Anthropic: OpenAI lists repo layout as content; Anthropic's `/doctor` trims directory layouts. This skill admits a layout as a Pointers line when the tree does not make it obvious (`rules.md` §1).

## Model behaviour notes (measured or observed, dated)

- **Instructions are followed, and following costs** (controlled study, 2026-02, GPT-5.2 and GPT-5.1 mini): tooling recommendations raised GPT-5.2 reasoning tokens by 22%; testing instructions raised cost significantly; more grep/read/write per task. Scope verification to the kind of change; never "run all checks before every change".
- **Truncation is silent**: a 66 KB contract arrived cut mid-sentence at 32 KiB and both agents worked for months without noticing (ai-docs-organizing readme, 2026-09-13). Probe with file reads forbidden after any sizeable edit.
