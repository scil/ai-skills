# Source tiers

## 1. The tiers and what each may do

| Tier | `kind` prefix | What it is | What it may do |
|---|---|---|---|
| 1 | `T1-vendor` · `T1-standard` | The owner's own documentation: a vendor's docs for its product, a standard's own site, a specification, a project's own README for its layout | **Decides alone.** A tier-1 statement enters a rule or a fact table by itself. When two tier-1 owners differ (two vendors, a vendor and a standard), record both; the artefact follows the owner it is read by. |
| 2 | `T2-research` | Peer-reviewed or preprint empirical studies | **Corroborates or qualifies.** Enters when two independent studies agree, or when one explains a tier-1 rule. A lone study is written "one study finds" and shapes no conclusion. Always record scope (§2): studies disagree along their scope lines. |
| 3 | `T3-exemplar` | The real thing in the wild: a file in a popular repository, a shipped configuration | **Illustrates.** Shows a pattern in use; never the source of a rule. Verified by direct access (API, tree, raw file), never through an article about it. |
| 4 | `T4-report` | Blogs, engineering posts, secondary coverage, vendor guides, chat transcripts | **Points.** Leads to a tier-1 or tier-2 source, or is recorded as "reported". A vendor's first-hand engineering post about its own practice is tier 4 with weight: primary, but one team's account. |

Tier is about *ownership of the fact*, not prestige. A vendor blog about its own product's roadmap is tier 4; the same vendor's reference docs are tier 1. A famous author's post about a paper is tier 4; the paper is tier 2.

## 2. Scope fields for a study

Record these before the findings; they are where the disagreements live:

- **Agents / models tested**, with versions.
- **Languages and task type** (bug fixes from issues, feature work, small PRs under N lines).
- **Input provenance**: generated vs developer-written artefacts; repositories with or without existing documentation.
- **What was measured**: success/correctness, cost (which tokens), time, behaviour counts — and what was *not* measured (a study with no correctness check cannot speak to quality).
- **Sample**: repositories, tasks, files, sessions.
- **Stated limitations**, in the authors' words.
- **Versions and dates**: v1, revisions, venue.

Two studies that "contradict" each other usually differ on two of these fields. Write the difference; that *is* the finding.

## 3. Admission rules in one line each

- Tier 1 alone → yes.
- Tier 2, two independent studies agreeing → yes, with both cited.
- Tier 2, one study → "one study finds …", no rule.
- Tier 2 explaining a tier-1 rule → yes, as the explanation.
- Tier 3 → example only.
- Tier 4 with a cited tier-1/2 source → follow the citation and register that.
- Tier 4 with a number and no cited study → "reported", goes no further.
