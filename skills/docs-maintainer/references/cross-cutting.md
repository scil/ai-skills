# Cross-cutting changes, future work, framework rules

## Cross-Cutting Change Rule

Start from the owning node named in the Annotated Structure (or the project's ownership map). When a change crosses boundaries, update each affected owner in the same change instead of copying the same facts into multiple places.

- API behavior changes may affect API docs, machine-readable contracts, examples, tests, and changelog entries.
- Config schema, profile, path, or default changes may affect architecture config docs, engineering setup/migration docs, examples, and tests.
- Destructive-operation, permission, preview, confirmation, or rollback behavior may affect architecture security docs, operations rollback docs, API safety notes, and tests.
- Architecture boundary, runtime topology, or responsibility changes may affect architecture overview, C4 views, deployment or operations docs, and ADRs when the decision is consequential.
- Local setup, build, packaging, release, or test workflow changes may affect engineering docs and the repository README when the project entry point changes; in a project with an agent contract they belong in its command section and the environment example file, never duplicated into other prose.
- Schema, enum, or contract changes update the owner in code (schema, validators, routers), the spec scenarios that describe the behaviour, the validators derived from the schema, and the tests, in the same change.
- New concepts, terms, statuses, roles, or groupings go to the owning vocabulary, glossary, data model, API/config docs, or spec requirement and the plan's terminology — never scattered across helper prose.
- Repeated AI mistakes or retrieval failures belong in the agent context doc's guard register as positive rules with their incident and enforcing test; duplicated cross-topic facts move back to their owning docs and are removed from helper prose.
- Framework-specific command or API bridge changes must load the relevant rule file before updating API docs and wrappers — for Tauri desktop apps, `rules/tauri-command-api.md`.

## Future Work Promotion Rule

Future work, backlog, optional providers, rollout advice, and candidate ideas stay out of current-fact docs until accepted or implemented; store them under product requirements, a roadmap doc, or an ADR with explicit decision status (Candidate, Proposed, Accepted, Rejected, Implemented).

When a candidate becomes accepted or implemented, promote only the stable resulting facts into the owning current-fact nodes. Leave the historical candidate context where it was.

## Links

Use normal relative Markdown links between project docs and same-file `#anchors` for headings. Avoid root-relative links such as `/docs/architecture/config.md` unless the repository already requires them. After moving or renaming docs, validate the changed links.
