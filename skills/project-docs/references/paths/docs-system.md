# Path: the docs system (every other durable fact)

Read this to decide where a durable fact belongs, to route facts into a system the project already has, to scaffold `docs/` from nothing, to set up plans or ADRs, to review a code change for documentation impact, or to audit docs for staleness (gardening). The layer model and principles are in [`SKILL.md`](../../SKILL.md).

## File-First Split Rule

Choose the owning node, then decide section, file, or directory. One file per topic; split only when the topic is large, high-risk, independently owned, heavily linked, machine-readable, or a real source of edit conflicts. A doc every task of a kind is routed through is *hot* and gets a map before any split ([`../docs-system/structure.md`](../docs-system/structure.md) → Hot documents; [`loading-system.md`](loading-system.md) → Hot pointer docs).

## Alongside Matt Pocock's skills

When the project also uses `mattpocock-skills` (plugin or vendored), its skills read fixed paths; map them as owners, never move or duplicate them:

- Vocabulary → `GLOSSARY.md` at the root; decisions → `docs/adr/`.
- `docs/agents/issue-tracker.md` and `docs/agents/domain.md` are layer-5 project bindings for those skills; one ownership-map row, `advisory`. A pointer they repeat from the contract stays: the skills read only that path.
- The issue tracker (`.scratch/` when local and gitignored) is layer-1 scratch, not a record; give it a row saying where its decisions move (the plan's decision log or an ADR) before the work closes.

Where the two rule sets disagree — ADR shape (MADR here; one paragraph with optional `status` there), where planned work lives (plans here; tracker there), or any new case — the owner decides. Do not pick silently: list each conflict with both rules and a recommendation, ask once, then record the choice in the plan's decision log and `conventions`, or as an ADR when it changes an accepted one. The known conflicts, each with a recommendation: [`../docs-system/alongside-mattpocock.md`](../docs-system/alongside-mattpocock.md).

## Adopt a system the project already has (route, do not scaffold)

1. Refresh gate. Inventory what already owns facts: contract, spec system, plans, package code, skills, CI checks. A project that runs OpenSpec has a ready mapping in [`../docs-system/adopting-openspec.md`](../docs-system/adopting-openspec.md).
2. Build the **Ownership Map** from [`../../templates/ownership-map.md`](../../templates/ownership-map.md): one row per fact type → existing owner → layer → enforced by → reading rule. Walk every node of the Annotated Structure (`structure.md` → Mapping) and map it or mark it *skipped — reason*.
3. Hand every procedure found in a doc to layer 5; declare every artefact a generator could produce as layer 3 with its command; mark prose that mirrors code as code-wins.
4. Add a file only when no owner fits and the split rule allows, in the repository's own naming.
5. Done when every node has an owner or a recorded skip, every row names its check, and the map is committed where the agents read it.

## Create from nothing

1. Refresh gate. Inspect source, existing docs, contracts, deployment files, tests. Ask once where the system lives (`structure.md` → Where the structure lives).
2. Create layers 0, 1 and 6 first: the map ([`instruction-file.md`](instruction-file.md) → Create), `plans/` with one active plan for this work, the ownership map.
3. Create layer-2 nodes only for facts you hold now; layer 3 with a generator and a CI diff; layer 4 only for a dependency the agent needs offline. No empty folders, no stubs.
4. Diagram C4 L1 and L2 and each genuinely hard flow ([`../docs-system/diagramming.md`](../docs-system/diagramming.md)).
5. Validate: links, lint, diagrams render, generated files match.
6. Done when every created node has an owner, an update trigger and a check, and the checks pass.

## Update after a change

1. Inspect the change: source, tests, affected owners, the active plan.
2. Record the decision in the plan's decision log; touch only the owners the change affects; a new term, status or grouping goes to its owning vocabulary, data model, config doc or requirement.
3. Cross-boundary changes update every affected owner in the same change ([`../docs-system/cross-cutting.md`](../docs-system/cross-cutting.md)); a consequential decision becomes an ADR; a changed boundary or flow updates its diagram; a changed generator input regenerates layer 3.
4. On completion, promote stable facts to layer 2, write the retrospective, move the plan to `completed/`.
5. Done when no owner the change touched still describes the old behaviour.

## Garden (audit for staleness)

1. Refresh gate. Run the mechanical checks first: links, freshness-marker age, generated diff, path-exists over repo-map and locator.
2. Check each owner against code, schemas and tests; prose that contradicts code is the defect. `ls` every path, command and file a doc names.
3. Move duplicated facts back to their owner and delete copies; when a section keeps regrowing, trace what produces it ([`SKILL.md`](../../SKILL.md) → Source and symptom). Check linked skills' project bindings still hold.
4. Refresh markers and grades in `docs/quality`; done when every owner is reviewed and dated and no fact has two owners.
