# Alongside Matt Pocock's skills: the conflicts

Read on 2026-11-03: `mattpocock-skills` plugin 1.3.1, `setup-matt-pocock-skills`, `domain-modeling` with `ADR-FORMAT.md` and `GLOSSARY-FORMAT.md`, and the local issue-tracker template. These skills read and write fixed paths, and nothing tells them to look elsewhere. So if a path differs, the Matt path wins and this skill maps onto it (`SKILL.md`, "Alongside Matt Pocock's skills"). If a rule differs, the owner decides once. Each conflict below gives both rules and a recommendation. Ask them together, then record the answers in the plan's decision log and in the ownership map.

## Paths: map, do not ask

| Fact | This skill | Matt | Use |
|---|---|---|---|
| Vocabulary | `docs/product` holds goals, users and vocabulary | `GLOSSARY.md` at the root, terms with `_Avoid_` lists. Multi-context: `GLOSSARY-MAP.md` plus one `GLOSSARY.md` per context. | `GLOSSARY.md`. An existing `docs/product` keeps goals and requirements, and links the glossary for words. |
| Decisions | `docs/decisions/NNNN-<slug>.md` | `docs/adr/NNNN-<slug>.md`, created lazily. Multi-context: also `src/<context>/docs/adr/`. | `docs/adr/`. No `docs/decisions/`. |
| Skill bindings | Layer 5, one place per skill | `docs/agents/issue-tracker.md` and `docs/agents/domain.md`. With `triage` installed, also `docs/agents/triage-labels.md`. | One ownership-map row, layer 5, `advisory`. |
| Work in progress | `docs/plans/active/<yyyy-mm-dd>-<slug>.md` | The issue tracker. Local: `.scratch/<feature>/spec.md` and `.scratch/<feature>/issues/NN-<slug>.md` | See conflict 2. |

## Rules: ask the owner

1. **ADR shape.** This skill uses MADR (Context, Decision drivers, Considered options, Decision outcome, Consequences, Confirmation), with a required status. Matt uses one to three sentences: context, decision, why. Its `status` frontmatter, Considered Options and Consequences are optional. If the project runs `domain-modeling`, recommend Matt's shape, because that skill writes the ADRs. Keep two rules of this skill. A rejected option with a non-obvious reason is named in the paragraph. An accepted ADR is superseded, never edited.
2. **Where planned work lives.** This skill keeps a living plan per piece of work, and moves it to `completed/` at the end. The plan has Progress, Surprises, Decision log and Retrospective. Matt keeps a spec plus one ticket file per task in the tracker. Recommend both, with a split. The plan (or the project's existing plan doc) stays the record of decisions and progress. The tracker holds specs and tickets as scratch. Before a feature closes, each decision moves from the tracker to the plan's decision log or an ADR. A gitignored `.scratch/` is never a record.
3. **When a decision gets an ADR.** This skill writes one for an architecturally significant or consequential decision. Matt has three tests, and an ADR needs all three: hard to reverse, surprising without context, and the result of a real trade-off. Recommend Matt's three-part test. It is concrete, and it keeps easy-to-reverse choices in the decision log.
4. **The `## Agent skills` block.** `setup-matt-pocock-skills` writes a block into an existing `CLAUDE.md`, or else into `AGENTS.md`. This skill allows pointers in layer 0, but no skill list. Recommend three pointer lines to `docs/agents/*.md`. If the project has a `CLAUDE.md`, put them there. The plugin runs only in Claude Code, so the block then costs Codex nothing. Never paste the bindings themselves into layer 0.
5. **ADR enforcement.** This skill's ownership-map row says "ADR lint: status in proposed, accepted, deprecated, superseded by N". Matt makes status optional, so that lint fails on valid ADRs. Recommend no status lint. The row says `advisory`, and an ADR without a status counts as accepted.

## Gaps neither covers

- Matt's specs and tickets carry no dates, but this skill's plan file names do. If a project keeps dates out of tracked files, it names plans by slug alone and keeps the dates in its private notes.
- Matt has no generated layer, no ownership map and no architecture node. `GLOSSARY.md` and `docs/adr/` do not replace `docs/architecture/`. The Adopting path still applies to every other node.

## First applied

wordpress-Guesthouse-demo, 2026-11-03:

- One-paragraph ADRs in `docs/adr/`, without status frontmatter.
- `docs/plan.md` stays the living plan, with a decision log. Specs and tickets go to a gitignored `.scratch/`.
- The `## Agent skills` block is in `CLAUDE.md`.
- No triage labels, because `triage` was not installed.
- The project's prose lint read YAML frontmatter as the first sentence of the paragraph. That was one more reason to drop the optional status.
