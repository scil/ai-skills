# Adopting the structure in a project that uses OpenSpec

OpenSpec (`@fission-ai/openspec`) is a spec-driven change system: accepted behaviour lives in `openspec/specs/<capability>/spec.md`; work in progress is a change folder under `openspec/changes/<id>/` with `proposal.md`, `design.md`, `tasks.md` and `specs/` deltas (`ADDED / MODIFIED / REMOVED Requirements`); completed changes move to `openspec/archive/` (older layouts: `openspec/changes/archive/`) and the deltas are merged into the specs. `openspec init` writes a managed instruction block into `AGENTS.md` and `CLAUDE.md`; `openspec update` regenerates it. Layout verified against the project README on 2026-09-15 ([`sources.md`](sources.md) → `openspec-readme`).

OpenSpec already owns most of layers 1 and 2. Follow the Adopting path: route onto it, add only what it has no home for.

## Mapping

| Layer / node | OpenSpec owner | Note |
|---|---|---|
| 0 map | `AGENTS.md`, with OpenSpec's managed block inside it | the block is always loaded and counts against the Codex 32 KiB chain; keep it, budget for it. Let OpenSpec write **one** file: `AGENTS.md`. `CLAUDE.md` stays the one-line `@AGENTS.md` bridge; a second managed block there is a duplicate paid twice by Claude Code. |
| 1 `plans/active/<slug>` | `openspec/changes/<id>/` | `proposal.md` = purpose and scope; `tasks.md` = progress (checkboxes); `design.md` = technical approach and decision log. The change folder *is* the plan; no `docs/plans/active/`. |
| 1 `plans/completed` | `openspec/archive/<id>/` | archive only after the retrospective section exists (below) and stable facts were promoted. |
| 1 `plans/tech-debt` | **gap** → `docs/plans/tech-debt.md` | OpenSpec tracks changes, not debt. |
| 2 `product` requirements and decision states | `openspec/specs/<capability>/spec.md` (accepted) and a change's `specs/` deltas (proposed) | OpenSpec's lifecycle replaces Candidate · Proposed · Accepted · Implemented; a rejected proposal is archived with a one-line reason in `proposal.md`. |
| 2 `product` vocabulary, goals, non-goals | the plan or product doc the project already keeps, or `docs/product.md` | specs describe behaviour, not vocabulary; a term used across capabilities needs one owner. |
| 2 `decisions` (ADR) | the change's `design.md` | no `docs/decisions/`. A consequential decision gets MADR-shaped sections inside `design.md` (context · options · outcome · consequences · confirmation) and is superseded by a later change, never edited after archive. |
| 2 `architecture/*`, `quality-attributes/*`, `engineering/*` | **gap** → `docs/architecture/`, `docs/engineering/` | specs say what the system does; these say how it is shaped. Create only nodes with facts in hand. |
| 3 `generated/*` | **gap** → `docs/generated/` | schema, API index, dependency graph; OpenSpec has no generated layer. |
| 4 `references/*` | **gap** → `docs/references/` | vendored `llms.txt`; only when a dependency is needed offline. |
| 5 skills | `.agents/skills/` + the `/opsx:*` commands | the OpenSpec commands are the change procedure; project skills that route to specs name the capability, not a path they copy. |
| 6 `ownership-map`, `quality` | **gap** → `docs/ownership-map.md`, `docs/quality.md` | the map is this table filled in with real ids. |

## Three sections OpenSpec's templates stop short of

Add to each change, as short sections, so the change folder is a full ExecPlan:

- **Surprises & discoveries** in `tasks.md` or `design.md`: what the tree, tests or environment turned out to be, with the date.
- **Decision log** entries in `design.md`: one line per decision — what, why, date — beyond the initial technical approach.
- **Outcomes & retrospective** in `tasks.md` before `/opsx:archive`: achieved, remaining, lessons. A change archived without it loses the only record of *why*.

## Rules that matter in an OpenSpec repository

1. **Specs are written from shipped behaviour and its tests, never from the contract's prose.** When the two disagree, the prose is the stale party. (ThanksPorch, 2026-09-13; `ai-docs-organizing/readme.md`.)
2. **One scenario, one test.** A `#### Scenario:` names the situation so it maps to a test name; the ownership map's *Enforced by* column for a spec row is that test.
3. **Hot specs get a map.** A capability that skills route to by name is read whole on every task of its kind; above ~20 KB, add a question-first map at the top of `spec.md` and put the reading rule (map → requirement → test) in the skill that names it.
4. **The managed block is the contract's, not yours.** Do not hand-edit inside the markers; `openspec update` overwrites them. Rules you add to the contract go outside the block.
5. **Promote before archiving.** A term, state or grouping introduced by a change goes to its layer-2 owner (vocabulary, data-model meaning, config doc) in the same change; archive moves the deltas into specs but nothing else.
6. **Deltas are facts of record in transit.** A `MODIFIED Requirements` block that contradicts a test is a defect in the delta, and the change is not applied until they agree.

## Ownership-map excerpt to start from

```
| Fact / change type | Owner | Layer | Enforced by | Reading rule / notes |
| Accepted behaviour of <capability> | openspec/specs/<capability>/spec.md | 2 | scenario → test names | map at top if > 20 KB |
| Proposed behaviour change | openspec/changes/<id>/specs/ | 1 | openspec validate; apply blocked until tests agree | |
| Work in progress, decisions, retrospective | openspec/changes/<id>/{proposal,design,tasks}.md | 1 | template sections present before archive | three added sections above |
| Consequential decision | openspec/changes/<id>/design.md (MADR sections) | 2 | superseded by a later change, never edited after archive | no docs/decisions/ |
| Completed work | openspec/archive/<id>/ | 1 | archive lint: retrospective present | |
| Contract lines | AGENTS.md (managed block + project lines) | 0 | chain byte-budget test; block written once | CLAUDE.md = @AGENTS.md |
| Known debt | docs/plans/tech-debt.md | 1 | gardening run | gap OpenSpec does not fill |
```
