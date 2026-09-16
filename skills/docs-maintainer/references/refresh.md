# Refresh — keeping the standards, vendor guidance and research current

Runs when `last-refresh` in [`sources.md`](sources.md) is older than `gate-days` (30), or on request. Report-and-propose: nothing in `SKILL.md`, `structure.md` or the templates changes without the user's yes. State lives in the repo, never in an agent's memory.

## 1. Fingerprint

The checker is shared with `ai-agents-md`; both skills live in the same skills directory (a repo's `.agents/skills/` when both are linked, otherwise the shared source that the machine's global `AGENTS.md` names):

```powershell
pwsh -File <skills>/ai-agents-md/scripts/check-sources.ps1 -Path <skills>/docs-maintainer/references/sources.md -GateDays 30
```

`-GateOnly` prints the days since `last-refresh` and exits 1 when the gate is due. `-Update` stores new fingerprints and today's date; run it only after step 4. Rows marked `manual:<date>` (sites that answer 403/429 to scripts) are opened in a browser and compared against the `purpose` column by hand. If `ai-agents-md` is not reachable, do the same for every row and say so in the changelog entry.

## 2. Read only what moved

For each `CHANGED` or `NEW` row: what changed; does it alter a layer's writing rule in `structure.md`, a row or column of `templates/ownership-map.md`, a step in `SKILL.md`, or the diagramming rules; does it introduce a claim that needs a second source. Read Tier 1 vendor rows first (skills, plans, memory docs move fastest), standards second, research last.

## 3. Search for new standards, vendor changes and research

Dated, domain-restricted:

- Vendor: `Claude Code skills OR memory OR rules changelog <month year>` and `Codex skills OR AGENTS.md OR plans changelog <month year>` with `allowed_domains` `code.claude.com`, `platform.claude.com`, `learn.chatgpt.com`, `developers.openai.com`, `github.com/anthropics/claude-code`, `github.com/openai/codex`.
- Standards: `C4 model` / `MADR release` / `llms.txt` / `OpenAPI release` on their own domains.
- Research: `coding agents documentation OR "context files" OR skills empirical study <year>` with `allowed_domains` `arxiv.org`, `dl.acm.org`, `ieeexplore.ieee.org`.

Admission by tier (table at the top of `sources.md`): Tier 1 alone; Tier 2 in pairs or as the explanation of a Tier 1 rule; Tier 3 illustrates; Tier 4 points. A blog number without a cited study is "reported" and goes no further.

## 4. Write the changelog entry, then propose

Append to [`changelog.md`](changelog.md) the same shape as `ai-agents-md`: sources checked / changed / errors; per changed source, effect; new findings; numbered proposals. Show it; apply what the user accepts, each edit naming its source; then `-Update`. Add new Tier 1 or Tier 2 sources as rows with `-` fingerprints for the next run.

## Anti-patterns

Refreshing every invocation. Fetching everything when two rows moved. Changing the ownership-map template from a blog. Updating fingerprints before the report was seen. A Tier 2 finding rewriting a layer rule on its own.
