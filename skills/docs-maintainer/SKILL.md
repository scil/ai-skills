---
name: docs-maintainer
description: Create, organize, audit, or maintain the documentation system of a software project whose first reader is an AI coding agent. Use when an agent needs to decide where a durable fact belongs (a contract line, a plan, a system-of-record doc, a generated artefact, a vendored reference, a skill, or governance), route facts into a system the project already has (an agent contract, a spec system, a plan doc) instead of building a parallel tree, scaffold docs/ from nothing, set up execution plans, add C4 architecture docs or ADRs, decide whether an API needs a document at all, review a code change for documentation impact, audit docs for staleness (gardening), or check whether the documentation standards, vendor guidance and research this skill rests on have changed (30-day refresh gate). Owns layers 1–6 of the docs system; the always-loaded instruction file's content is ai-agents-md's, and loading budgets are ai-docs-organizing's.
---

# Documentation for a repository whose first reader is an agent

Facts must be discoverable, stable, linkable, and safe for an agent to act on. Since 2026-09-15 the system is organized by **loading layer** — how a fact reaches the agent and what each read costs — and its rules carry tiered sources. Why, and on what evidence: [`readme.md`](readme.md).

## Principles

1. **Code, schemas, tests, deployment files and ADRs are the facts of record.** Prose that mirrors them is *code-wins*: when they disagree, fix the prose in the same change. Anything a generator can produce is generated and never hand-edited.
2. **One owner per fact.** The Annotated Structure ([`references/structure.md`](references/structure.md)) is categories to preserve, not files to create. No parallel trees, no index files, no directory `README.md` by default.
3. **Route by layer.** 0 always-loaded map · 1 working notes (plans) · 2 system of record · 3 generated · 4 vendored references · 5 skills · 6 governance. The layer sets the writing rules: the map carries rules and pointers only (content: `ai-agents-md`); plans are what agents read most and are living documents; a procedure is a skill, never a doc section; a hand-written API reference is not created by default.
4. **Future work has a decision state**, in a plan or a requirement, until accepted or implemented; a consequential decision is an ADR in MADR shape and is superseded, never edited ([`references/cross-cutting.md`](references/cross-cutting.md)).
5. **Non-functional facts get explicit owners** — security, reliability, performance — because they are the least documented in the wild and the least inferable from code.
6. **Every row names its check.** A doc without a link check, freshness marker, generated-diff, path-exists check or test is `advisory`, written out; gardening runs on a cadence, not when someone notices.

## Every run starts with the refresh gate

Read `last-refresh` and `gate-days` at the top of [`references/sources.md`](references/sources.md). If the gate is due, run the Refresh path first, then continue. If the network is unavailable, say so and continue with the sources as they stand.

## File-First Split Rule, and hot docs

Choose the owning node, then decide section, file, or directory. One file per topic; split only when the topic is large, high-risk, independently owned, heavily linked, machine-readable, or a real source of edit conflicts. A layer-2 doc that the map or two or more skills route to is *hot*: above ~20 KB it gets a question-first map at the top and a reading rule in every skill that names it (`structure.md` → Hot documents).

## Paths

### Adopting a system the project already has (route, do not scaffold)

1. Refresh gate. Inventory what already owns facts: contract, spec system, plans, package code, skills, CI checks.
2. Build the **Ownership Map** from [`templates/ownership-map.md`](templates/ownership-map.md): one row per fact type → existing owner → layer → enforced by → reading rule. Walk every node of the Annotated Structure (`structure.md` → Mapping) and map it or mark it *skipped — reason*.
3. Hand every procedure found in a doc to layer 5; declare every artefact a generator could produce as layer 3 with its command; mark prose that mirrors code as code-wins.
4. Add a file only when no owner fits and the split rule allows, in the repository's own naming.
5. Done when every node has an owner or a recorded skip, every row names its check, and the map is committed where the agents read it.

### Creating from nothing

1. Refresh gate. Inspect source, existing docs, contracts, deployment files, tests. Ask once where the system lives (`structure.md` → Where the structure lives).
2. Create layers 0, 1 and 6 first: the map (via `ai-agents-md`), `plans/` with one active plan for this work, the ownership map.
3. Create layer-2 nodes only for facts you hold now; layer 3 with a generator and a CI diff; layer 4 only for a dependency the agent needs offline. No empty folders, no stubs.
4. Diagram C4 L1 and L2 and each genuinely hard flow ([`references/diagramming.md`](references/diagramming.md)).
5. Validate: links, lint, diagrams render, generated files match.
6. Done when every created node has an owner, an update trigger and a check, and the checks pass.

### Updating after a change

1. Inspect the change: source, tests, affected owners, the active plan.
2. Record the decision in the plan's decision log; touch only the owners the change affects; a new term, status or grouping goes to its owning vocabulary, data model, config doc or requirement.
3. Cross-boundary changes update every affected owner in the same change (`cross-cutting.md`); a consequential decision becomes an ADR; a changed boundary or flow updates its diagram; a changed generator input regenerates layer 3.
4. On completion, promote stable facts to layer 2, write the retrospective, move the plan to `completed/`.
5. Done when no owner the change touched still describes the old behaviour.

### Auditing for staleness (gardening)

1. Refresh gate. Run the mechanical checks first: links, freshness-marker age, generated diff, path-exists over repo-map and locator.
2. Check each owner against code, schemas and tests; prose that contradicts code is the defect. `ls` every path, command and file a doc names.
3. Move duplicated facts back to their owner and delete copies; when a section keeps regrowing, trace what produces it (`ai-docs-organizing` → Source and symptom). Check linked skills' project bindings still hold.
4. Refresh markers and grades in `docs/quality`; done when every owner is reviewed and dated and no fact has two owners.

### Refresh (standards, vendor guidance, research)

Procedure in [`references/refresh.md`](references/refresh.md): run the shared checker (`ai-agents-md/scripts/check-sources.ps1 -Path … -GateDays 30`), read only what moved, search with the domain allowlist, write the dated entry in [`references/changelog.md`](references/changelog.md), and *propose* edits. Tier 1 (vendor, standard) decides alone; Tier 2 (research) corroborates in pairs; exemplars illustrate; reports point.

## References and templates

- [`references/structure.md`](references/structure.md) — the seven layers, what moved and why, adoption mappings, where the structure lives, repo map vs code locator, hot-doc reading rule.
- [`references/adopting-openspec.md`](references/adopting-openspec.md) — the mapping for a project that runs OpenSpec: change folders as plans, `design.md` as ADR, the gaps `docs/` fills, six rules, a starter ownership-map excerpt.
- [`references/cross-cutting.md`](references/cross-cutting.md) — cross-cutting checklist, decision states and promotion, link rules, where framework-specific rules live.
- [`references/diagramming.md`](references/diagramming.md) — PlantUML rules for C4 L1/L2, flows and trap entries.
- [`references/sources.md`](references/sources.md), [`references/refresh.md`](references/refresh.md), [`references/changelog.md`](references/changelog.md) — the tiered sources and the refresh machinery.
- [`templates/ownership-map.md`](templates/ownership-map.md) — the Adopting path's deliverable and the layer-6 owner.
