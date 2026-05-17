# AI Agent Context

This file owns compact project navigation anchors, agent operating rules, and gotchas. Reusable task prompts and documentation evals live under `docs/ai/prompts/` and `docs/ai/evals/` because they are executable assets, not project facts.

## Agent Rules

### Scope

This file is an agent operating guardrail. It should not repeat product, architecture, config, safety, testing, repo-map, or code-locator facts that already have owning documents.

### Working Session Rules

- At the start of each working session, before the first edit, read this file once and follow these Agent Rules.
- Re-read this file if `AGENTS.md` or `docs/ai.md` changes, if the working context is reset or compacted, or if you are unsure you have the current rules.
- Treat source code, tests, config examples, and the owning docs listed in [docs/ownership.md](ownership.md) as facts of record.
- Use [docs/ai.md#ai-context-map](#ai-context-map) to find the owning document before changing behavior.
- When documentation must be created, updated, or checked for impact, use the `docs-maintainer` skill and follow its Updating Documentation and Cross-Cutting Change Rule.
- Update the owning document in the same change when behavior moves.
- Add focused regression tests for subtle config, filesystem, status, export, state, API, or tree/grouping bugs.

## AI Context Map

### Project Entry Points

Use these as project-specific navigation anchors, not a required reading list. After applying Document Routing, read only the entries relevant to the task.

- `docs/product.md#glossary`: project vocabulary and naming.
- `docs/product/frontend-ux.md`: implemented UI behavior and copy, if the project has a frontend.
- `docs/engineering/code-locator.md`: problem-to-file implementation entry points.
- `<backend facts-of-record file>`: backend facts of record.
- `<frontend facts-of-record file>`: frontend facts of record.
- `<default config/example file>`: default config example.
- `<test fixture config/example file>`: test fixture config example.

### Document Routing

Use the `docs-maintainer` skill's Annotated Structure to choose the owning document for product, architecture, API, config, security, operations, engineering, and AI-rule changes.

Use [docs/engineering/code-locator.md](engineering/code-locator.md) when you need problem-to-file implementation entry points, invariants, or focused verification commands.

## Gotchas

This document captures repeated mistakes and hidden traps. Keep canonical product, architecture, config, API, safety, testing, repo-map, and code-locator facts in their owning docs; use this file to prevent repeat errors.

### Example

- Replace this section with project-specific gotchas only after they are observed or high-risk.
