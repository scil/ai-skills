# Annotated Structure, and where it lives

Use this as an information architecture, not a required file tree. Route durable project facts to the owning node below; do not duplicate product, architecture, API, testing, operations, repo-map, or code-locator facts in AI helper docs. Node labels intentionally omit `.md`: each node may be a section, a standalone file, or a directory with child files according to the File-First Split Rule. The comments explain ownership and update triggers; do not include the comments in actual names. Treat the structure as categories to preserve, not files to blindly create; split C4 component filenames are project-specific, and a placeholder component file that does not match the actual system is a defect.

```text
docs/                                      # Long-lived project documentation root
  product                                 # Owns product goals, users, vocabulary, requirements, boundaries, and non-goals; update when product behavior, naming, UX contracts, accepted requirements, or future scope changes.
    requirements                          # Owns accepted, implemented, candidate, rejected, or historical requirements with decision state labels such as Candidate, Proposed, Accepted, Rejected, or Implemented; update when scope, acceptance criteria, UX contracts, or decision state changes.
    feature-roadmap                       # Owns optional candidate backlog/roadmap with decision state labels, sources, trigger conditions, constraints, and rollout order; update when candidate scope, decision state, or rollout order changes.

  architecture                            # Owns architecture overview, C4 L1/L2, data model, config summary, security summary, deployment summary, and quality attributes; update when boundaries, responsibilities, state model, topology, major flows, or quality constraints change.
    overview                              # Owns major modules, dependencies, boundaries, responsibility splits, and design principles; update when architecture boundaries or responsibilities change.
    c4-system-context                     # Owns C4 L1 users, external systems, system boundary, and trust boundary, with a PlantUML diagram; update when actors, external systems, or trust boundaries change.
    c4-container                          # Owns C4 L2 apps, services, databases, queues, workers, and third-party containers, with a PlantUML diagram; update when containers or runtime topology change.
    c4-components                         # Owns C4 L3 component views for real containers or component groups, with a PlantUML diagram; update when component boundaries, ownership, or important interactions change.
    data-model                            # Owns entities, relationships, constraints, migrations, status definitions, enum semantics, and data ownership; update when schema, states, lifecycle semantics, or data dictionary entries change.
    config                                # Owns config roots, profiles, schema, path rules, examples, environment expansion, removed names, and migrations; update when config fields, profile behavior, paths, defaults, or migrations change.
    security                              # Owns authentication, authorization, secrets, data protection, destructive-operation safety, permissions, and threat model; update when safety, preview/confirmation, permissions, or trust behavior changes.
    dynamic-login-flow                    # Owns one important runtime sequence, state transition, or cross-boundary flow, with a PlantUML sequence or activity diagram; update when that flow changes.
    deployment                            # Owns hosted environments, networks, runtime topology, deployment trust boundaries, and production layout; update when deployment topology or runtime architecture changes.
    adr                                   # Owns Architecture Decision Records; add an ADR when a consequential architecture, technology, or policy decision is made.
      0001-record-architecture-decisions

  engineering                             # Owns setup, repo map, conventions, testing, debugging, release, migrations, and code locator; update when commands, workflow, build/package layout, migration guidance, tests, repo structure, or problem entry paths change.
    setup                                 # Owns local setup, dependencies, environment variables, initialization, common failures, and local runtime layout; update when install, run, debug, env, or local path behavior changes.
    testing                               # Owns test strategy, check commands, fixtures, coverage boundaries, and required regression themes; update when test commands, coverage expectations, or fixture profiles change.
    release                               # Owns versioning, build/package steps, release defaults, approval, deployment handoff, and verification; update when packaging, release config, or release verification changes.
    migrations                            # Owns database, config, data repair, and rollback migration guidance; update when schema, config, or data migration behavior changes.
    repo-map                              # Owns system map: directory/module responsibilities, major feature distribution, entry points, and ownership; update when repo structure, module boundaries, feature locations, or entry points move.
    code-locator                          # Owns problem-to-file entry index and change recipes, with a PlantUML diagram for genuinely hard-to-follow nodes; update after solving recurring or subtle problems with files involved, invariants/traps, and focused verification.

  api                                     # Owns API contracts and direction rules; keep direction-specific auth, errors, examples, quotas, and adapters under the relevant direction; update when signatures, payloads, return types, errors, examples, events, webhooks, or upstream contracts change.
    command-api                           # Owns optional local app command bridge; load framework-specific rules when applicable and update when command signatures, payloads, side effects, or safety behavior change.
    provided                              # Owns interfaces this project exposes to callers: HTTP routes, RPC methods, SDK methods, events, webhooks, plugin hooks, schemas, and error contracts; facts of record are server routes/controllers, handlers, schemas, OpenAPI/AsyncAPI files, contract tests, and implementation tests; update when exposed routes, methods, SDKs, events, webhooks, schemas, errors, examples, or compatibility behavior change.
    consumed                              # Owns upstream interfaces this project calls or depends on: backend services, third-party APIs, SDKs, payment/auth/map/email providers, vendor webhooks, and sibling services; facts of record are clients/adapters, upstream official docs, observed responses, fixtures, mocks, and integration tests; update when upstream contracts, adapters, auth, quotas, mocks, fixtures, or risks change.
    openapi.yaml                          # Owns REST API machine-readable contract; update with REST paths, requests, responses, errors, and examples.
    asyncapi.yaml                         # Owns event/message machine-readable contract; update with channels, payloads, producers, consumers, and compatibility notes.

  operations                              # Owns monitoring, runbooks, incidents, rollback, and recovery procedures; update when logging, alerting, rollback, manual repair, partial-failure, or incident response changes.
    rollback                              # Owns application, data, config, and post-rollback verification; update when recovery, undo, backup/restore, or partial-failure repair behavior changes.
    monitoring                            # Owns metrics, logs, traces, dashboards, alerts, and thresholds; update when observability, logging, or alert behavior changes.
    runbook-alert-name                    # Owns step-by-step operational procedure for one alert or scenario; update when manual action, escalation, or verification changes.
    incident-YYYY-MM-DD-title             # Owns incident record: timeline, impact, root cause, fix, and prevention; add after notable incidents.

  ai                                      # Owns compact project navigation anchors, routing pointers, agent operating rules, and gotchas; update when agent rules, navigation anchors, retrieval paths, repeated AI mistakes, guardrails, or docs routing changes. Use templates/docs-ai.md as the starter shape.
    prompts                               # Optional reusable AI prompts; keep only when actually reused. Not a facts-of-record area.
      doc-audit                           # Owns reusable human/CI/agent documentation audit prompt; must not contain project truth; update when audit output expectations or docs impact categories change.
      adr-writer                          # Owns reusable ADR drafting prompt; must not contain project truth; update when ADR format or decision workflow changes.
    evals                                 # Optional reusable documentation evals; keep only when actually reused. Not a facts-of-record area.
      doc-freshness                       # Owns reusable eval for whether agents can answer project questions from current docs and code; update when questions, expected source docs, or facts of record change.

  ownership                               # Owns owners, update cadence, facts of record, and stale-document review rules; update when ownership, review cadence, or canonical fact sources change.
  changelog                               # Owns user-visible changes, migrations, breaking changes, and release notes; update for releases, breaking changes, migrations, and user-visible behavior changes.
```

## Mapping the structure onto a system the project already has

When adopting (the Adopting path in `SKILL.md`), each node above maps to an existing owner or is skipped with a reason. Typical mappings:

| Node | Existing owner | Note |
| --- | --- | --- |
| `ai` | the agent contract (`AGENTS.md` / `CLAUDE.md`) | no `docs/ai.md`; nested contracts are thin pointers upward; the contract lists no skills |
| `product/requirements`, `architecture/adr` | the spec system (OpenSpec or similar) | a change's design doc is the ADR; no `adr/` directory |
| `architecture` | one hand-maintained C4 L1/L2 file | no L3/L4 subtree; architecture *rules* stay in the contract |
| `api` | the code, when routers, validators and shared types are the contract | no `docs/api/` |
| `engineering/setup`, `engineering/testing` | the contract's command and testing sections | plus the environment example file |
| `engineering/code-locator` | one curated file | see entry discipline below |
| `product` | the plan doc | |
| `ownership` | the ownership map itself (`templates/ownership-map.md`) | |
| `operations`, `changelog` | skipped until incidents or releases exist | written down as skipped, with the reason |

## Where the structure lives

Ask about the storage location only once per project, at first-time creation; never on later updates. The structure lives in exactly one place: the in-repo `docs/` tree, or a local Obsidian vault chosen through the `obsidian-vault-ops` skill. Never both, never mirrored — a single location is the only source of record. When the vault is chosen, apply every rule of this skill inside the vault folder in place of `docs/`, and leave one short pointer note in the repository (`README.md` or `docs/ai.md`) recording the vault name and folder; keep it current if the vault moves.

## Repo map and code locator

Keep structural navigation and problem-first navigation separate when both are useful. `repo-map` is the system map: what each directory or module is, so an agent understands the shape before changing it. `code-locator` is the problem entry index: for this issue or workflow, where to look first, what invariant must not break, what focused check to run. Both are curated maps, not generated inventories, and both point back to code as the fact of record.

Locator entry discipline: add an entry after solving a recurring or subtle problem — the trigger, the start files, the invariant or trap, the smallest verifying check; refresh an entry in the same change as a fix that touches a path it names; delete entries that go stale. Keep an entry an entry: when one has grown into an essay, its invariant stays and its rationale moves to the spec, ADR, or code comment it cites.
