# Cross-cutting changes, future work, framework rules

## Cross-Cutting Change Rule

Start from the owning node named in the Annotated Structure (or the project's ownership map). When a change crosses boundaries, update each affected owner in the same change instead of copying the same facts into multiple places.

- API behaviour changes update the code that is the contract (routers, handlers, validators, shared types), regenerate the layer-3 API index or machine-readable spec, and update contract tests and the changelog; there is no hand-written API doc to update unless the project recorded one as an exception.
- Config schema, profile, path, or default changes may affect the architecture config doc, the environment example file, the setup skill's bindings, and tests.
- Destructive-operation, permission, preview, confirmation, or rollback behaviour may affect the security and reliability quality-attribute docs, the recovery skill, the contract's Boundaries block, and tests; if it is enforceable, the hook changes too.
- Architecture boundary, runtime topology, or responsibility changes may affect the architecture overview, C4 L1/L2, the deployment doc, the dependency lint that enforces the boundary, and an ADR when the decision is consequential.
- Local setup, build, packaging, release, or test workflow changes belong in the manifest and the environment example file, and in the skill that owns the procedure; the contract keeps only the non-obvious pick and the scoped verification line; never duplicated into other prose.
- Schema, enum, or contract changes update the owner in code (schema, validators, routers), regenerate `generated/db-schema`, update the spec scenarios that describe the behaviour, the data-model doc's meaning of any new state, and the tests, in the same change.
- New concepts, terms, statuses, roles, or groupings go to the owning vocabulary, glossary, data model, config doc, or spec requirement and the plan's terminology — never scattered across helper prose.
- Every decision taken during a change goes in the active plan's decision log with its rationale and date; a consequential one becomes an ADR (MADR; proposed → accepted; supersede rather than edit). On completion the plan's stable facts are promoted to layer 2 and the plan moves to `completed/` with its retrospective.
- A changed dependency version updates the vendored reference in `docs/references/` (or deletes it) and the skill bindings that name the version.
- Repeated AI mistakes or retrieval failures belong in the contract's guard register as positive rules with their incident and enforcing test or hook (content rules: `ai-agents-md`); duplicated cross-topic facts move back to their owning docs and are removed from helper prose.
- Framework-specific command or API bridge changes must load the relevant rule file before updating wrappers, generated contracts and safety notes — for Tauri desktop apps, `rules/tauri-command-api.md`.

## Future Work Promotion Rule

Future work, backlog, optional providers, rollout advice, and candidate ideas stay out of current-fact docs until accepted or implemented; they live in a plan (layer 1) or a requirement with an explicit decision state (Candidate, Proposed, Accepted, Rejected, Implemented), or in an ADR with a MADR status (proposed, accepted, deprecated, superseded by N).

When a candidate becomes accepted or implemented, promote only the stable resulting facts into the owning layer-2 nodes. Leave the historical candidate context in the completed plan or the ADR.

## Links

Use normal relative Markdown links between project docs and same-file `#anchors` for headings. Avoid root-relative links such as `/docs/architecture/config.md` unless the repository already requires them. After moving or renaming docs, validate the changed links.
