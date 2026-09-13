---
name: docs-maintainer
description: Create, organize, audit, or maintain an AI-agent-first software project documentation system. Use when an AI agent needs to scaffold a docs/ structure, route facts into a documentation system the project already has (an agent contract, a spec system, a plan doc) instead of building a parallel tree, decide where a durable fact belongs, prepare agent-readable project context, define documentation facts of record, add C4 architecture docs, create ADR/API/runbook documentation, review code changes for documentation impact, or audit docs for staleness.
---

# AI Agent Project Documentation System

Documentation whose first reader is an AI coding agent: project facts must be discoverable, stable, linkable, and safe for an agent to act on. (Chinese human-readable version: `for-human/SKILL.zh.md`; never loaded during operation.)

## Principles

1. **Code, schemas, tests, deployment files, and ADRs are the facts of record.** Prose that mirrors them is *code-wins*: when the two disagree, correct the prose in the same change. Keep volatile detail next to code and link to it rather than restating it.
2. **One owner per fact.** The Annotated Structure ([`references/structure.md`](references/structure.md)) is a set of categories to preserve, not files to create; route each fact to its owning node and never duplicate product, architecture, API, testing, operations, repo-map, or code-locator facts into helper docs. No separate index or context-map files unless the project asks; no directory `README.md` by default.
3. **The agent context doc holds rules, not inventories.** `docs/ai.md` — or the agent contract when the project has one; keep one canonical source and mirror only intentionally — carries navigation anchors, operating rules, and gotchas, and its entry-point list is not required reading. At least one harness reads the contract under a hard byte budget, so recipes, script lists, retired-environment history, and per-skill listings leave it (a skill's trigger is its own `description`; shared-skill membership is the ignore-file manifest; a vendored-skill override is its `OVERLAY.md`). Prompts and evals hold no project truth. Loading model and diet: `ai-docs-organizing`.
4. **Future work stays out of current-fact docs** until accepted or implemented; ADRs record consequential architecture, technology, or policy decisions, not routine implementation ([`references/cross-cutting.md`](references/cross-cutting.md)).
5. **Validate with what exists**: link checks (relative links, no root-relative ones), Markdown lint, OpenAPI/AsyncAPI validation, diagram rendering, repo CI. Machine-readable contracts are preferred for APIs and events.

## File-First Split Rule

Choose the owning node, then decide whether it is a section, a standalone file, or a directory. Start with one Markdown file per topic; split only when the topic is large, high-risk, independently owned, heavily linked, machine-readable, frequently reviewed, or a real source of edit conflicts. Fewer, denser, well-indexed files beat many thin stubs.

## Paths

Pick the one that matches the task. Each ends on the condition that says it is done.

### Adopting a system the project already has (route, do not scaffold)

Most repositories that run agents already own their facts — an agent contract, a spec system, a plan doc, package code whose types are the API contract. A parallel tree would give every fact two owners.

1. Build an **Ownership Map** from [`templates/ownership-map.md`](templates/ownership-map.md): one row per fact type → the owner that already exists → notes.
2. Walk every node of the Annotated Structure and map it to an existing owner (typical mappings: `references/structure.md` → "Mapping the structure") or mark it *skipped — reason*.
3. Add a new file only when no owner fits and the split rule justifies it, following the repository's own docs convention (naming, numbering, language) rather than this skill's node names.
4. Mark prose that mirrors code as code-wins.

Done when every node has an owner or a recorded skip, and the map is committed where the project's agents will read it.

### Creating from nothing

1. Inspect the repository: source, existing docs, API contracts, deployment files, tests, examples.
2. Ask once where the system lives — the in-repo `docs/` tree or an Obsidian vault (`references/structure.md` → "Where the structure lives"); never both.
3. Identify the facts of record, choose owning nodes, apply the split rule, and create the smallest structure the project can maintain — no empty folders, no stubs.
4. Diagram architecture, key flows, and genuine traps per [`references/diagramming.md`](references/diagramming.md).
5. Validate.

Done when every created node has an owner and an update trigger, and the checks pass.

### Updating after a change

1. Inspect the change: source, affected docs, tests, recent diffs.
2. Start from the owning nodes and touch only what the change affects; a new concept, term, status, role, or grouping goes to its owning vocabulary, data model, API/config doc, or spec requirement.
3. When the change crosses boundaries, update every affected owner in the same change — the checklist is `references/cross-cutting.md`; record a consequential decision as an ADR; update any diagram of a changed boundary or flow.
4. Validate.

Done when no owner the change touched still describes the old behaviour.

### Auditing for staleness

1. Check each owner against current code, schemas, and tests; prose that contradicts code is the defect, not the code.
2. `ls` every path, route, command, and file a doc names — a sentence about something that is gone is the most common stale fact.
3. Refresh `<!-- Last reviewed: YYYY-MM-DD -->` markers as owners are revised; a marker older than the code it describes is a queue.
4. Move duplicated facts back to their single owner and delete the copies; when a section keeps regrowing, trace what produces it and fix that too (`ai-docs-organizing` → "Source and symptom").

Done when every owner is reviewed and dated, and no fact has two owners.

## References and templates

- [`references/structure.md`](references/structure.md) — the Annotated Structure, the adoption mappings, where the structure lives, repo map vs code locator and the locator's entry discipline.
- [`references/diagramming.md`](references/diagramming.md) — PlantUML rules for C4 docs, flows, and trap entries.
- [`references/cross-cutting.md`](references/cross-cutting.md) — the cross-cutting change checklist, future-work promotion, link rules, framework rule files (`rules/tauri-command-api.md`).
- [`templates/docs-ai.md`](templates/docs-ai.md) — starter for a project `docs/ai.md`; [`templates/ownership-map.md`](templates/ownership-map.md) — the Adopting path's deliverable.
