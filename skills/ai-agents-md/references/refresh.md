# Refresh — keeping the sources and this skill current

Runs when the `last-refresh` date at the top of [`sources.md`](sources.md) is more than 7 days old, or on request. It is a report-and-propose step: nothing in `SKILL.md`, `rules.md` or the templates changes without the user's yes. State lives in the repo (`sources.md`, `changelog.md`), never in an agent's memory — Codex has none, and the two harnesses must see the same date.

## 1. Fingerprint the sources

```powershell
pwsh -File skills/ai-agents-md/scripts/check-sources.ps1
```

The script is shared: `docs-maintainer` runs the same file with `-Path <its sources.md> -GateDays 30` (a `gate-days:` line in a sources file sets the default gate for that file). It reads every row of the given `sources.md`, recomputes each fingerprint (`gh:` = latest commit SHA of the file via the GitHub API; `sha:` = SHA-256 of the page text with scripts, tags and whitespace stripped) and prints `UNCHANGED`, `CHANGED`, `NEW` or `ERROR` per row. `-GateOnly` prints only the days since `last-refresh`. `-Update` rewrites fingerprints and the `last-refresh` date — run it only after step 5.

A row whose fingerprint is `manual:<date>` is a site that answers 403/429 to scripts (openai.com, morphllm.com); the script prints `MANUAL` and skips it. Open it in the browser, compare with the `purpose` column, and set the date by hand.

Page hashes can move for cosmetic reasons (a nav change, a date stamp). Treat `CHANGED` as "read it", not as "it matters".

## 2. Read only what moved

For each `CHANGED` or `NEW` row, fetch the source and answer three questions: what changed; does it alter a fact in `harness/*.md`, a rule in `rules.md`, a template line, or the exemplar's own shape (an exemplar that grew past 32 KiB or shrank to a bridge is itself a finding); does it add a claim that needs a second source before this skill repeats it.

## 3. Search for new research and vendor changes

Two searches, dated, domain-restricted — general search returns SEO copies of the same three posts:

- Research: `AGENTS.md OR CLAUDE.md context files coding agents study <year>` with `allowed_domains` `arxiv.org`, `infoq.com`, `github.blog`, `openai.com`, `anthropic.com`, `code.claude.com`, `learn.chatgpt.com`.
- Vendor: `Codex AGENTS.md changelog <month year>` and `Claude Code CLAUDE.md memory changelog <month year>`, same allowlist plus `github.com/openai/codex` and `github.com/anthropics/claude-code`.

A claim enters this skill by the authority tier of its source (the tier table at the top of `sources.md`):

- **Tier 1, vendor documentation** (Anthropic for Claude Code, OpenAI for Codex, the agents.md site for the format): enters on its own. When the two vendors differ, record both and let the file follow the harness that reads it.
- **Tier 2, research**: enters when two independent studies agree, or when one study explains a Tier 1 rule. A single study is written as "one study finds" and changes no rule by itself. Record each study's scope (agents, languages, task type, whether files were generated or developer-written, whether correctness was measured), because the studies so far disagree precisely along those lines.
- **Tier 3, exemplars**: illustrate a pattern; never the source of a rule.
- **Tier 4, reports and blogs**: point to a Tier 1 or 2 source, or are recorded as "reported". A vendor's first-hand engineering post about its own practice carries more weight than secondary coverage but stays Tier 4.

Blog numbers without a cited study are recorded as "reported" in the changelog and go no further.

## 4. Write the changelog entry

Append to [`changelog.md`](changelog.md):

```
## yyyy-mm-dd

- Sources: <n> checked, <n> changed (<ids>), <n> errors.
- <id>: <what changed> → <no effect | affects rules.md §x | affects harness/x.md | affects template>.
- New: <source or study> — <one-line finding> → <proposal or "recorded only">.
- Proposals: <numbered list of concrete edits to this skill, or "none">.
```

## 5. Propose, then update state

Show the entry and the proposals to the user. Apply the accepted edits (each with its source named in the commit). Then `check-sources.ps1 -Update` to store the new fingerprints and today's date. Add any new primary source as a row in `sources.md` with `kind`, `purpose` and an empty fingerprint; the next run fills it.

## Anti-patterns

Running the refresh on every invocation regardless of the gate. Fetching all sources when the script says two moved. Editing `rules.md` from a blog post. Updating fingerprints before the report was seen (the change is then invisible forever). Keeping the last-refresh date in a memory file.
