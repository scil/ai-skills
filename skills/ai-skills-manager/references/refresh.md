# Refresh — keeping the sources and this skill current

The procedure is [`ai-agents-md/references/refresh.md`](../../ai-agents-md/references/refresh.md), run against this skill's sources file. Only what differs is written here.

## 1. Fingerprint

```powershell
pwsh -File skills/ai-agents-md/scripts/check-sources.ps1 -Path skills/ai-skills-manager/references/sources.md
```

`-GateOnly` prints the days since `last-refresh`; `-Update` rewrites fingerprints and the date — only after step 4.

## 2. Read only what moved

For each `CHANGED` or `NEW` row ask: does it alter a frontmatter rule (name grammar, description cap), a loading fact (which directories, what is truncated where, how the roster budget shortens descriptions), or the body guidance (line count, one-level references)? A loading fact also belongs in [`ai-docs-organizing/references/harness-loading.md`](../../ai-docs-organizing/references/harness-loading.md) — propose the edit there, do not copy the fact here.

## 3. Search

Dated, domain-restricted:

- Vendor: `Claude Code skills SKILL.md changelog <month year>`, `Codex skills description budget <month year>`, `agentskills.io specification changelog` — `code.claude.com`, `platform.claude.com`, `learn.chatgpt.com`, `agentskills.io`, `github.com/anthropics/claude-code`, `github.com/openai/codex`, `github.com/agentskills/agentskills`.
- Research: `agent skills SKILL.md progressive disclosure study <year>` — `arxiv.org`.

Tiers as in `sources.md`. **Disputes**: when the spec, a harness's documentation and observed behaviour disagree, name each side, its tier, and which the weight supports; the `Disputes on record` section in `sources.md` is where a standing disagreement lives.

## 4. Changelog, propose, then update state

Append the dated entry to [`changelog.md`](changelog.md) in the sibling's format, show it, apply what the user accepts, then `-Update`.

## Anti-patterns

The sibling's list, plus: copying a loading fact into this skill instead of pointing at `harness-loading.md`; treating a Claude Code-only frontmatter field (`when_to_use`, `paths`, `context`) as portable.
