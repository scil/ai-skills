# Cross-cutting changes, future work, framework rules

## Cross-Cutting Change Rule

A change that crosses boundaries updates every affected owner in the same change; the project's ownership map says which owner holds which fact type. Four cases the map does not make obvious:

- **API behaviour**: the code is the contract (routers, handlers, validators, shared types). Regenerate the layer-3 index or machine-readable spec; update contract tests and the changelog. There is no hand-written API doc to update unless the project recorded one as an exception.
- **Safety behaviour** (destructive operations, permissions, preview, confirmation, rollback): beyond the security and reliability docs, the recovery skill, the contract's Boundaries block and the tests, the hook that enforces it changes too.
- **A dependency version**: update or delete its vendored reference in `docs/references/`, and every skill binding that names the version.
- **A framework bridge or command API** (a desktop app's frontend↔backend commands, a plugin's hook surface) follows the API shape — a generated index owns the surface; hand-written text covers only the safety and permission behaviour a generator cannot know. The project-specific rule lives in that project's ownership map or local docs skill, never in this shared skill.

## Future Work Promotion Rule

Future work, backlog, optional providers, rollout advice, and candidate ideas stay out of current-fact docs until accepted or implemented; they live in a plan (layer 1) or a requirement with an explicit decision state (Candidate, Proposed, Accepted, Rejected, Implemented), or in an ADR with a MADR status (proposed, accepted, deprecated, superseded by N).

When a candidate becomes accepted or implemented, promote only the stable resulting facts into the owning layer-2 nodes. Leave the historical candidate context in the completed plan or the ADR.

## Links

Relative links, not root-relative (`/docs/architecture/config.md`), unless the repository already requires them.
