# Ownership Map — template

The deliverable of the Adopting path and the layer-6 owner of "where does this fact live". One row per fact type, routed to an owner the project already has. Copy it to where the project's agents will read it (`docs/ownership-map.md`, or the project's local docs skill), fill in real paths, and keep the five columns:

- **Owner** — the one place the fact lives; code where code is the fact of record.
- **Layer** — 0 always-loaded · 1 working notes · 2 system of record · 3 generated · 4 vendored reference · 5 skill · 6 governance. The layer sets the writing rules (`references/structure.md`).
- **Enforced by** — the check that catches drift: a test, a lint, a CI diff, a freshness-marker age, a generator, a hook; or `advisory`, written out.
- **Reading rule** — for a hot doc, how to read it (map → section → owner); for generated, the regenerate command; otherwise blank.

A node of the Annotated Structure that maps to nothing is written down as **skipped — reason**, so the gap reads as a decision.

| Fact / change type | Owner | Layer | Enforced by | Reading rule / notes |
| --- | --- | --- | --- | --- |
| Destructive-action boundaries, non-obvious commands, scoped verification, architecture rules, traps, pointers | `AGENTS.md` (+ `CLAUDE.md` = `@AGENTS.md`) | 0 | chain byte-budget test; `PreToolUse` / Codex hook for the forbidden paths | content per `ai-agents-md`; lists no skills, no overview, no directory listing |
| Work in progress: purpose, progress, surprises, decisions, retrospective | `docs/plans/active/<date>-<slug>.md` → `completed/` | 1 | plan lint: required sections present; a completed plan has a retrospective | one plan per piece of work that outlives a session; promote stable facts to layer 2 before moving to `completed/` |
| Known technical debt | `docs/plans/tech-debt.md` | 1 | gardening run updates grade and owner | item · owner · grade · paying trigger |
| Product goals, users, vocabulary, accepted requirements with decision state, non-goals | `docs/product.md` or the spec system | 2 | spec scenarios → tests | decision states: Candidate · Proposed · Accepted · Rejected · Implemented |
| Architecture overview, boundaries, principles; C4 L1 and L2 | `docs/architecture/overview.md`, `c4-context.md`, `c4-container.md` | 2 | architecture test or dependency lint for the boundaries it states; diagram renders in CI | the overview the contract does not carry |
| Data-model meaning: lifecycle semantics, enum meaning, ownership | `docs/architecture/data-model.md` | 2 | the generated schema is the fact; a test names each state transition | read with `docs/generated/db-schema.md` |
| Config semantics, profiles, removed names | `docs/architecture/config.md` + the env example file | 2 | config schema validation in tests | |
| One important runtime flow | `docs/architecture/flows/<name>.md` | 2 | the E2E test that walks it | one diagram per flow |
| Deployment topology | `docs/architecture/deployment.md` | 2 | IaC is the fact; doc holds boundaries and reasons | |
| Security: authn, authz, secrets, destructive-op safety, threat model | `docs/architecture/quality-attributes/security.md` | 2 | secret scan; authz tests; `PreToolUse` hook on protected paths | least-covered category in the wild; give it an owner even when short |
| Reliability: SLOs, failure modes, backup and recovery facts | `docs/architecture/quality-attributes/reliability.md` | 2 | alert thresholds in monitoring config; restore test | recovery *procedure* is a skill |
| Performance budgets and their checks | `docs/architecture/quality-attributes/performance.md` | 2 | budget assertions in CI (bundle size, latency test) | |
| Consequential architecture, technology or policy decision | `docs/decisions/NNNN-<slug>.md` (MADR) or the change's design doc | 2 | ADR lint: status ∈ {proposed, accepted, deprecated, superseded by N}; accepted ADRs are never edited | supersede, do not rewrite |
| Directory and module responsibilities, entry points | `docs/engineering/repo-map.md` | 2 | path-exists check over every path it names | curated, not `ls` output |
| Problem → files → invariant → check | `docs/engineering/code-locator.md` | 2 | path-exists check; the named check exists | search for the symptom or the user's term, read only matching entries, never the whole file; trigger lines are written in the user's words, code term beside; entry discipline in `structure.md` |
| Conventions that differ from defaults and no linter encodes | `docs/engineering/conventions.md` | 2 | each row names its lint or `advisory` | a convention a linter encodes is deleted here |
| Test strategy facts: layers, fixtures, never-mock list, regression themes | `docs/engineering/testing.md` | 2 | the suite's structure | commands: manifest; run recipe: skill |
| Versioning, compatibility policy, release channels | `docs/engineering/versioning.md` | 2 | version-bump check in CI | release *procedure* is a skill |
| Incident record | `docs/incidents/<date>-<title>.md` | 2 | — | prevention item becomes a rule, test or hook |
| User-visible changes | `docs/changelog.md` or release notes | 2 | release lint | |
| DB schema, API route/command/event index, dependency graph, C4 L3 | `docs/generated/*` | 3 | CI regenerates and diffs; hand edit fails the build | each file states `generated by <command> from <source>`; C4 L4 skipped — IDEs render it |
| Machine-readable API contract for an external consumer | `docs/generated/openapi.yaml` / `asyncapi.yaml`, emitted from code | 3 | spec validation + contract test | skipped when no external consumer — reason recorded |
| Third-party docs needed offline | `docs/references/<lib>-llms.txt` (version, URL, date) | 4 | dependency-version check against the recorded version | prefer the upstream `llms.txt`; pinned excerpt otherwise |
| Setup, release, migration, alert runbook, doc audit, ADR drafting | `.agents/skills/<name>/` (project or shared) | 5 | the skill's scripts are runnable; project bindings in one place | a procedure found in a doc moves here; facts it needs are referenced from layers 2–4, never copied |
| Which shared skills this repo links | the ignore-file lines the link script reads | 5 | link script | no prose list |
| A project override of a vendored skill | `OVERLAY.md` inside that skill | 5 | outside the upstream hash | |
| Where every fact type lives (this table) | `docs/ownership-map.md` | 6 | ownership lint: every layer-2 file appears in one row | |
| Freshness, quality grades, gardening cadence, doc-lint config | `docs/quality.md` + the lint config | 6 | scheduled gardening run: link check, marker age, generated diff, path-exists | |
| Doc evals (questions answerable from current docs) | `docs/evals/` | 6 | run in CI or skipped — reason: not yet needed | |
| Repeated agent mistakes | the contract's guard register (layer 0) with `Instance:` + enforcing test, or a hook | 0 | the test or hook | positive rule, not a "don't" list |
| Operations runbooks, monitoring dashboards | skipped until the first alert — reason: none exist yet | — | — | |
