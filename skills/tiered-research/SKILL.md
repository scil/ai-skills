---
name: tiered-research
disable-model-invocation: true
description: Research a question, verify a set of claims, or build the source base for a report or a skill, with sources ranked by authority tier and every verdict naming the corpus it searched. Use when asked to check whether claims are true, to critically absorb an article or a chat transcript, to find "the latest" on a topic, to compare studies that disagree, to write a report that cites sources, or to give a skill a sources registry with dates and fingerprints. Owns the method of judging and registering sources; collecting coding resources for an implementation is gather-code-references, and turning references into project decisions is derive-project-plan.
---

# Tiered research

Research whose output is a set of verdicts and a source table, not an impression. Origin: [`readme.md`](readme.md).

## Principles

1. **Authority tiers decide what a source may do.** Tier 1, the owner's own documentation (a vendor for its product, a standard's own site), decides alone. Tier 2, empirical research, corroborates when two independent studies agree or one explains a tier-1 rule; a single study is "one study finds" and shapes no conclusion by itself. Tier 3, real exemplars, illustrate. Tier 4, blogs, posts and secondary coverage, point to a tier-1 or tier-2 source or are recorded as "reported". Table and scope fields: [`references/source-tiers.md`](references/source-tiers.md).
2. **Name the corpus before the verdict.** Before writing *not found* or *contradicted*, ask which corpus would contain the claim if it were true, and search that one. A verdict states where it looked. A vendor has several documentation sites; a claim about "OpenAI" may be about a blog post, not a repository.
3. **Verify the object, not the description of it.** An exemplar, a file, a number: fetch or list it directly (API call, tree listing, the paper's own page). Articles that describe a thing are tier 4 about that thing.
4. **State disagreements; do not resolve them by preference.** When tier-1 sources or studies conflict, record both with the scope that explains the difference (models, languages, task type, what was measured). A clean conclusion the sources do not support is worse than a stated split.
5. **Splices are common.** A circulating sentence often joins a number from one study, a scope from another, and a rule of thumb from a guide. Pull the pieces apart and register each with its real source.
6. **Dates are two columns.** `source-date` is what the source states (published, revised, version); `checked` is when you looked. An undated living page is written as such, never given a guessed date.

## Paths

### Verify claims

1. List every checkable claim from the input, one row each, quoting it.
2. For each, name the corpus that would hold it if true (owner's docs, the paper, the repository, the standard). Search there first; widen only after.
3. Record the verdict with the vocabulary in [`references/verdict-protocol.md`](references/verdict-protocol.md): CONFIRMED · PARTLY · NOT FOUND (in `<corpus>`) · CONTRADICTED (by `<source>`) · CONFLATED (pieces listed) · WRONG OBJECT (the claim is about X, checked against Y).
4. Done when every row has a verdict, a corpus, a source URL and a source date, and every CONFLATED row lists its pieces.

### Research a question

1. Write the question and the decision it serves. Search tier 1 first, dated and domain-restricted; then tier 2 on arXiv and publisher sites; tier 3 and 4 last.
2. For each study, record scope fields before findings (`source-tiers.md` §2). Look for the study that disagrees before writing what "the research says".
3. Report: what tier-1 sources say (and where they differ), what studies agree on, what they dispute and along which scope line, what is only reported. Numbers go in a table.
4. Done when every sentence of the conclusion can be traced to a row of the source table, and no conclusion rests on a single tier-2 or tier-4 row.

### Build a sources registry for a skill

1. Copy [`templates/sources.md`](templates/sources.md); one row per source with tier in `kind`, `purpose` saying what is taken *and what is not*, `source-date`, `-` fingerprint.
2. Set `last-refresh` and `gate-days` (7 for fast-moving vendor topics, 30 for standards).
3. Run the shared checker to fill fingerprints and GitHub commit dates: `ai-agents-md/scripts/check-sources.ps1 -Path <registry> -Update`. Mark sites that answer 403/429 as `manual:<date>`.
4. Done when the checker reports no `-` fingerprints and every row has a `purpose` and a `source-date`.

