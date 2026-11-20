# Checklist: every rule of the three old SKILL.md files and its new place

Register for [merge-docs-skills.md](merge-docs-skills.md). One row for each block of the old files. `S` is `project-docs/SKILL.md`. `P/x` is `project-docs/references/paths/x.md`. `R/x` is `project-docs/references/refresh/x.md`.

## ai-agents-md/SKILL.md

| Old block | New place |
|---|---|
| Hand-offs line | Deleted: the targets are now parts of the same skill. |
| Definition of the instruction file | S, intro paragraph |
| Principle 1, only what the repository cannot tell | S, principle 1. detail (vendor quotes, research) in P/instruction-file, "What earns a line" |
| Principle 2, one canonical file, one-line bridges | S, principle 2 (one owner) names the bridge. detail in P/instruction-file, "One canonical file" |
| Principle 3, a rule is a wish until enforced | S, principle 5 (every rule names its check). destructive-action and sandbox sentence in P/instruction-file |
| Principle 4, grow by incident, prune by review | S, principle 6 |
| Principle 5, bytes and attention are the budget | S, principle 3 (the loading layer sets the budget). the 32 KiB and 200-line facts in P/instruction-file |
| Refresh gate (7 days) | S, refresh gate (both registries, 30 days, D4) |
| Path Create, steps 1 to 5 | P/instruction-file, Create |
| Path Review, steps 1 to 4 | P/instruction-file, Review |
| Path Update, steps 1 to 4 | P/instruction-file, Update |
| Path Refresh, with tiers and disputes | S, path index row. R/refresh.md |

## ai-docs-organizing/SKILL.md

| Old block | New place |
|---|---|
| Hand-offs line | Deleted, except the hand-off to `ai-skill-audit`, which stays in S. |
| Definition of a harness | S, intro paragraph |
| The loading model comes first, with the probe | S, same heading |
| Principle 1, the loading layer sets the budget | S, principle 3 |
| Principle 2, the repository is the only shared memory | S, principle 4 |
| Principle 3, one meaning, one owner | S, principle 2 |
| Principle 4, information hierarchy | S, principle 7 |
| Principle 5, the environment is the truth, docs are a cache | S, principle 1 (merged with "only what the repository cannot tell" and "code wins") |
| Process steps 1 to 7 | P/loading-system, Process |
| Source and symptom | S, same heading (used by two paths) |
| Skills, hooks, memory (five bullets) | P/loading-system, same heading |
| Hot pointer docs | P/loading-system, same heading. P/docs-system Garden points to it |

## docs-maintainer/SKILL.md

| Old block | New place |
|---|---|
| Hand-offs line | Deleted. |
| Intro: discoverable, stable, linkable, safe. organized by loading layer | S, intro paragraph |
| Principle 1, code and records are the facts. code-wins. generated never hand-edited | S, principle 1 |
| Principle 2, one owner per fact. no parallel trees | S, principle 2 |
| Principle 3, route by layer 0 to 6 | S, principle 3 |
| Principle 4, future work has a decision state. ADR | S, principle 8 |
| Principle 5, non-functional facts get owners | S, principle 9 |
| Principle 6, every row names its check. gardening on a cadence | S, principles 5 and 6 |
| Refresh gate (30 days) | S, refresh gate |
| File-First Split Rule | P/docs-system, same heading |
| Alongside Matt Pocock's skills | P/docs-system, same heading |
| Path Adopting | P/docs-system, Adopt |
| Path Creating from nothing | P/docs-system, Create |
| Path Updating after a change | P/docs-system, Update |
| Path Auditing for staleness | P/docs-system, Garden |
| Path Refresh | S, path index row. R/refresh.md |
