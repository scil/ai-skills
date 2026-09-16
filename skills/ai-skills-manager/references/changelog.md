# Changelog — refresh entries

## 2026-09-16

- Birth. Split out of `ai-docs-organizing` (its SKILL.md "Slimming a skill, and folding a fork back", the description-is-a-trigger sentence, and `references/process.md` §9, moved verbatim into `references/slimming.md`). Roster budget, provenance classes and "the contract lists no skills" stayed there.
- Sources: 7 rows added, first fingerprints computed by `check-sources.ps1 -Path … -Update` the same day. Read in full: agentskills-spec, claude-code-skills-docs, anthropic-skill-best-practices, codex-build-skills. Not yet read: anthropic-agent-skills-post (date to confirm), ex-anthropic-skills-repo.
- Findings that shaped the skill: description ≤ 1,024 (spec) with Claude Code truncating the listing at 1,536 and Codex shortening the whole roster at 2 % of context / 8,000 chars → principle 1 and the checklist's "would it still fire if cut in half"; body under 500 lines and one-level references (all three T1) → principle 2; "skills for prior models are often too prescriptive" → principle 3.
- Disputes recorded in `sources.md`: frontmatter requiredness (spec vs Claude Code), description cap (three numbers), and the repository's `scil:` prefix against the spec's `name` grammar — decision left to the repository.
- Proposals: none beyond the birth; the `scil:` prefix question is raised to the user, not proposed as an edit.
