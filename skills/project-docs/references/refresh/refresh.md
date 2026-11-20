# Refresh — keeping the sources and this skill current

Runs when the `last-refresh` date at the top of a registry is older than its `gate-days` (30 by default), or on request. It is a report-and-propose step: nothing in `SKILL.md`, the path files, the references or the templates changes without the user's yes. State lives in the repo (the registries and their changelogs), never in an agent's memory — Codex has none, and the two harnesses must see the same date.

There are two registries, one per subject area, each with its own changelog:

| Registry | Subject | Changelog | A moved source can change |
|---|---|---|---|
| [`sources-instruction-file.md`](sources-instruction-file.md) | Vendor docs for instruction files, context-file research, exemplar instruction files | [`changelog-instruction-file.md`](changelog-instruction-file.md) | a fact in `instruction-file/harness/*.md`, a rule in `instruction-file/rules.md`, a template line, or the exemplar's own shape (an exemplar that grew past 32 KiB or shrank to a bridge is itself a finding) |
| [`sources-docs-system.md`](sources-docs-system.md) | Documentation standards (C4, MADR, OpenAPI, llms.txt), vendor docs on skills, plans and memory, research on agent documentation | [`changelog-docs-system.md`](changelog-docs-system.md) | a layer's writing rule in `docs-system/structure.md`, a row or column of `templates/ownership-map.md`, a step in a path file, or the diagramming rules |

## Authority tiers

Rows are ordered by tier, and the tier is the first part of `kind`. This table serves both registries.

| Tier | kind prefix | What it is | What it may do in this skill |
|---|---|---|---|
| 1 | `T1-vendor` · `T1-standard` | The harness vendor's own documentation (Anthropic for Claude Code, OpenAI for Codex), the AGENTS.md format's own site, or a standard's own site | **Decides.** A T1 statement enters on its own. Where vendors or standards differ, both are recorded and the file follows the harness or standard it is read by. |
| 2 | `T2-research` | Peer-reviewed or arXiv empirical studies | **Corroborates or qualifies.** A finding enters only when two independent studies agree, or when it explains a T1 rule. A lone study is recorded as "one study finds" and shapes no rule by itself. Record each study's scope (agents, languages, task type, whether files were generated or developer-written, whether correctness was measured), because the studies so far disagree precisely along those lines. |
| 3 | `T3-exemplar` | Real instruction files or `docs/` trees in popular repositories | **Illustrates.** Shows a pattern in use; never the source of a rule. |
| 4 | `T4-report` | Vendor blogs, engineering posts, secondary coverage, guides | **Points.** Leads to a T1 or T2 source, or records a claim as "reported". An engineering post from a harness vendor about its own practice (OpenAI's Harness engineering) is T4 with weight: first-hand, but one team's account. A blog number without a cited study is "reported" and goes no further. |

Columns read by `scripts/check-sources.ps1`: `id`, `kind`, `url`, `fingerprint` (`gh:<sha12>` GitHub file · `sha:<hex12>` page · `manual:<date>` site that blocks scripts, read in a browser · `-` not yet computed), `checked` (when we fingerprinted it), `purpose` (what is taken, and what is not), `source-date` (the date the source itself states — published, revised, version released; GitHub rows get `commit <date>` filled by the script on `-Update`; a page that shows no date says `undated (living …)` rather than a guess).

## 1. Fingerprint the sources

```powershell
pwsh -NoProfile -File <skills>/project-docs/scripts/check-sources.ps1 -Path <skills>/project-docs/references/refresh/<registry>.md
```

The script reads every row of the given registry, recomputes each fingerprint (`gh:` = latest commit SHA of the file via the GitHub API; `sha:` = SHA-256 of the page text with scripts, tags and whitespace stripped) and prints `UNCHANGED`, `CHANGED`, `NEW` or `ERROR` per row. `-GateOnly` prints only the days since `last-refresh` and exits 1 when the gate is due. `-GateDays N` overrides the registry's `gate-days:` line. `-Update` rewrites fingerprints and the `last-refresh` date — run it only after step 5. Other skills (`ai-skill-audit`, `tiered-research`) run the same script on their own registries.

A row whose fingerprint is `manual:<date>` is a site that answers 403/429 to scripts (openai.com, morphllm.com); the script prints `MANUAL` and skips it. Open it in the browser, compare with the `purpose` column, and set the date by hand.

Page hashes can move for cosmetic reasons (a nav change, a date stamp). Treat `CHANGED` as "read it", not as "it matters".

## 2. Read only what moved

For each `CHANGED` or `NEW` row, fetch the source and answer three questions: what changed; does it alter anything in the registry's "can change" column above; does it add a claim that needs a second source before this skill repeats it. In the docs-system registry, read Tier 1 vendor rows first (skills, plans, memory docs move fastest), standards second, research last.

## 3. Search for new research and vendor changes

Dated, domain-restricted — general search returns SEO copies of the same three posts.

Instruction-file registry:

- Research: `AGENTS.md OR CLAUDE.md context files coding agents study <year>` with `allowed_domains` `arxiv.org`, `infoq.com`, `github.blog`, `openai.com`, `anthropic.com`, `code.claude.com`, `learn.chatgpt.com`.
- Vendor: `Codex AGENTS.md changelog <month year>` and `Claude Code CLAUDE.md memory changelog <month year>`, same allowlist plus `github.com/openai/codex` and `github.com/anthropics/claude-code`.

Docs-system registry:

- Vendor: `Claude Code skills OR memory OR rules changelog <month year>` and `Codex skills OR AGENTS.md OR plans changelog <month year>` with `allowed_domains` `code.claude.com`, `platform.claude.com`, `learn.chatgpt.com`, `developers.openai.com`, `github.com/anthropics/claude-code`, `github.com/openai/codex`.
- Standards: `C4 model` / `MADR release` / `llms.txt` / `OpenAPI release` on their own domains.
- Research: `coding agents documentation OR "context files" OR skills empirical study <year>` with `allowed_domains` `arxiv.org`, `dl.acm.org`, `ieeexplore.ieee.org`.

A claim enters this skill by the authority tier of its source (table above).

## 4. Write the changelog entry

Append to the registry's changelog:

```
## yyyy-mm-dd

- Sources: <n> checked, <n> changed (<ids>), <n> errors.
- <id>: <what changed> → <no effect | affects <file> §x | affects template>.
- New: <source or study> — <one-line finding> → <proposal or "recorded only">.
- Proposals: <numbered list of concrete edits to this skill, or "none">.
```

## 5. Propose, then update state

Show the entry and the proposals to the user. Apply the accepted edits (each with its source named in the commit). Then `check-sources.ps1 -Path <registry> -Update` to store the new fingerprints and today's date. Add any new Tier 1 or Tier 2 source as a row in the registry with `kind`, `purpose` and a `-` fingerprint; the next run fills it.

## Anti-patterns

Running the refresh on every invocation regardless of the gate. Fetching all sources when the script says two moved. Editing `rules.md` or the ownership-map template from a blog post. Updating fingerprints before the report was seen (the change is then invisible forever). Keeping the last-refresh date in a memory file. A Tier 2 finding rewriting a layer rule on its own.
