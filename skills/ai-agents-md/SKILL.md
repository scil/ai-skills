---
name: scil:ai-agents-md
description: Create, review, update or grow a repository's agent instruction file — AGENTS.md (Codex, the cross-tool standard) and CLAUDE.md (Claude Code), root or nested. Use when a repo has no instruction file, when /init or a generated file is proposed, when an agent repeats a mistake that "should be in AGENTS.md", when reviewing or slimming an existing AGENTS.md / CLAUDE.md, when deciding whether a rule belongs in the file, a hook, a linter or a skill, or when the reference sources for these files may have changed (every run first checks a 7-day refresh gate). Owns the content of one instruction file: which rules earn a line, how a rule is worded and enforced, the templates, and the sources it is derived from. Which files each harness loads, byte budgets across the chain, and the diet of an oversized contract belong to ai-docs-organizing; where any other project fact lives belongs to docs-maintainer.
---

# Agent instruction files: AGENTS.md and CLAUDE.md

An **instruction file** is the Markdown a coding harness injects into every session it starts in a repository: `AGENTS.md` for Codex and most other tools, `CLAUDE.md` for Claude Code. It is a behavioural layer, not a brake, and it is paid for on every turn. This skill decides what earns a line there, writes it, reviews it, and keeps its own sources current. Origin, and what was kept or rejected from the two conversations it grew from: [`readme.md`](readme.md).

## Principles

1. **Only what the repository cannot tell the agent — the two vendors say so first.** Anthropic: "For each line, ask: would removing this cause Claude to make mistakes? If not, cut it"; `/doctor` trims "directory layouts, dependency lists, and architecture overviews" and keeps "pitfalls, rationale, and conventions that differ from tool defaults". OpenAI: "A short, accurate AGENTS.md is more useful than a long file full of vague rules… add new rules only after you notice repeated mistakes." Research corroborates the direction and is mixed on the details (seven studies in [`references/sources.md`](references/sources.md), tier 2): developer-written beats generated in every study that compares them; unconditional testing instructions raise cost; whether a navigational map helps is contested, so a map is a Pointers line, not a directory listing. A line earns its place by passing the admission threshold in [`references/rules.md`](references/rules.md): non-inferable, costly when wrong, repeated, a team agreement, an architecture boundary, or a verification requirement.
2. **One canonical file, one-line bridges.** `AGENTS.md` is the shared source; `CLAUDE.md` is `@AGENTS.md` plus Claude-only lines. A rule written only in the bridge is a rule the other agent never sees.
3. **A rule is a wish until it has an enforcement layer.** Each rule names its layer: a hook, a CI check, a linter rule, a test, or the explicit tag `advisory`. Destructive-action policy sits at the top, short; the real brake is the sandbox and approval config.
4. **Grow by incident, prune by review.** A rule enters when a failure repeats, with `Instance:` and date; every PR asks *add, change, delete?*; a stale rule is worse than none because the file is trusted.
5. **Bytes and attention are the budget.** Codex cuts the whole chain at 32 KiB silently; Claude Code has no cut but a 200-line target per file. Measure before and after; the harness table lives in [ai-docs-organizing](../ai-docs-organizing/references/harness-loading.md).

## Every run starts with the refresh gate

Read the `last-refresh` line at the top of [`references/sources.md`](references/sources.md). If it is more than 7 days old, run the Refresh path first (it is short when nothing changed), then continue. Never skip the gate silently; if the network is unavailable, say so and continue with the sources as they stand.

## Paths

### Create

1. Refresh gate. Confirm no instruction file exists in the chain (`AGENTS.md`, `CLAUDE.md`, nested copies, `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`); if one does, switch to Review.
2. Learn the repo the way the agent will: manifest, lockfile, CI config, lint config, test runner, generated directories, migrations. Everything found here is *inferable* and stays out of the file.
3. Collect non-inferable facts: from the user, from `git log` of past corrections, from `CONTRIBUTING`, from any hook or CI check that encodes a rule. Offer, do not insert, the candidates in [`references/stacks/`](references/stacks/) that match the stack.
4. Fill [`templates/AGENTS.md`](templates/AGENTS.md): delete every section whose comment says the repo already answers it; keep the file under 4 KB and under 80 lines. Write [`templates/CLAUDE.md`](templates/CLAUDE.md) as the bridge. Add a nested file ([`templates/AGENTS.nested.md`](templates/AGENTS.nested.md)) only for a subtree with rules that differ from the root.
5. Done when: every remaining line passes the admission threshold, names its enforcement layer or `advisory`, the byte count is reported, and the growth loop (principle 4) is stated in the file's maintainer comment.

### Review

1. Refresh gate. Measure: bytes of the chain per start directory, lines per file.
2. Walk [`references/review-checklist.md`](references/review-checklist.md) line by line against the file; verify each claim against the tree (`Test-Path` the paths, the command in the manifest, the tool in the lockfile).
3. Report one row per finding: line, defect, disposition (delete as inferable · delete as stale · reword · move to hook/CI/linter · move to a skill or `.claude/rules/` · keep). Apply only what the user approves.
4. Done when: the file passes the checklist, or the rows the user rejected are recorded with the reason.

### Update (grow from an incident)

1. Refresh gate. State the incident: what the agent did, what it should have done, how many times it has happened.
2. Test it against the admission threshold. A first occurrence is not a rule; a one-off is a prompt. A rule the harness can enforce becomes a hook or check first, and a one-line rule second.
3. Write it in the shape from `rules.md`: positive invariant, `Instance:` with date, enforcement layer. Place it in the root, a nested file, or a `.claude/rules/` path-scoped file by scope. Then ask the three PR questions of the whole file.
4. Done when: the rule is in one file only, the bridge still reads `@AGENTS.md`, the byte count is reported.

### Refresh (sources and research)

Procedure in [`references/refresh.md`](references/refresh.md): run `scripts/check-sources.ps1`, read only the sources whose fingerprint moved, search for research and vendor announcements since the last refresh with the domain allowlist, write the dated entry in [`references/changelog.md`](references/changelog.md), and *propose* edits to this skill for the user to accept. Sources carry an authority tier: vendor documentation decides, research corroborates (two independent studies, or one that explains a vendor rule), exemplars illustrate, reports point. Fingerprints and `last-refresh` update only after the user has seen the report.

## References and templates

- [`references/rules.md`](references/rules.md) — admission threshold, wording, rule shape, section menu, what never enters.
- [`references/review-checklist.md`](references/review-checklist.md) — the review pass.
- [`references/refresh.md`](references/refresh.md), [`scripts/check-sources.ps1`](scripts/check-sources.ps1), [`references/sources.md`](references/sources.md), [`references/changelog.md`](references/changelog.md) — the refresh machinery.
- [`references/harness/claude-code.md`](references/harness/claude-code.md), [`references/harness/codex.md`](references/harness/codex.md) — what each harness does with the file's content, verified with dates.
- [`references/stacks/`](references/stacks/) — candidate non-inferable rules per stack; a menu, never auto-inserted.
- [`templates/`](templates/) — root, nested, bridge.

