# Refresh changelog

Newest first. Written by the Refresh path (`refresh.md` §4); proposals apply only after the user accepts them.

## 2026-09-15 — baseline and restructure

- Sources: 23 registered (16 Tier 1, 6 Tier 2, 1 Tier 4); fingerprints computed for the first time. No Tier 3 exemplar yet.
- Restructure by loading layer (0 always-loaded · 1 working notes · 2 system of record · 3 generated · 4 vendored references · 5 skills · 6 governance), driven by: Gao & Chen (60.5% of agent documentation reads are instruction files and working notes, 1.3% API references); Anthropic and OpenAI docs (procedures are skills; the main file references task files; `/doctor` trims layouts and overviews); C4's own guidance (component diagrams only if valuable and automated; no code diagrams); MADR 4.0.0; llms.txt; the OpenAI Harness-engineering tree (`exec-plans`, `generated/`, `references/*-llms.txt`, quality score, doc-gardening); Chatlatanagulchai et al. (security 14.8%, performance 14.5% coverage); Shepard & Albrecht (navigation is where guidance gains come from); Gao et al. (skills: 53% never modified; bindings are what changes).
- Removed `templates/docs-ai.md`: its content is the instruction file's content, owned by `ai-agents-md` since 2026-09-15.
- Ownership map gains three columns: Layer, Enforced by, Reading rule.
- Removed `rules/tauri-command-api.md`: a framework-specific rule in a project-agnostic skill; its content is recorded in `readme.md` for the Tauri project to re-home.
- Added `references/adopting-openspec.md` and the `openspec-readme` source: change folders as layer-1 plans, `design.md` as ADR, the gaps `docs/` fills, and the rule that OpenSpec's managed block is written into one file only.
- Proposals: none (initial build).
