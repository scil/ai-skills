---
name: ai-project-docs-maintainer
description: Create, organize, audit, or maintain an AI-agent-first software project documentation system. Use when an AI agent needs to scaffold a docs/ structure, prepare agent-readable project context, define documentation facts of record, add C4 architecture docs, create ADR/API/runbook documentation, or review code changes for documentation impact.
---

# AI Agent Project Documentation System

## Purpose

Use this skill to create and maintain project documentation whose primary consumer is an AI coding agent. Human readability still matters, but the documentation system must first make project facts discoverable, stable, linkable, and safe for agents to use.

For the human-readable Chinese equivalent of this skill, see `for-human/SKILL.zh.md`. Do not load that file during normal agent operation unless the user explicitly asks for the Chinese human version.

## Operating Model

Use the path that matches the task.

### Creating Documentation

1. Inspect the repository shape, source code, existing docs, API contracts, deployment files, tests, and examples.
2. Identify facts of record: source code, schemas, tests, ADRs, deployment config, API specs, runbooks, and product glossary.
3. Choose owning nodes from the Annotated Structure, then apply the File-First Split Rule.
4. Create the smallest useful documentation structure. Do not scaffold empty folders or many tiny files that the project cannot maintain.
5. Prefer stable, agent-readable docs with clear headings, short sections, explicit links, and unambiguous ownership.
6. Validate documentation with available checks such as Markdown lint, link checks, spell checks, OpenAPI/AsyncAPI validation, diagram rendering, or repo-specific CI.

### Updating Documentation

1. Inspect the code or architecture change, affected source files, existing docs, tests, and recent diffs.
2. Start from the owning nodes in the Annotated Structure and update only the affected docs.
3. Keep volatile implementation details close to code and schemas; link to them instead of duplicating them across prose docs.
4. When a change crosses boundaries, update each affected owner in the same change.
5. Record consequential architecture, technology, or policy decisions as ADRs.
6. Validate changed docs with the available project checks.

## File-First Split Rule

Use the Annotated Structure to choose the owning node, then decide whether that node should be a section, standalone file, or directory.

Start with one Markdown file per documentation topic. Split only when the topic is large, high-risk, independently owned, heavily linked, machine-readable, frequently reviewed, or likely to create real edit conflicts.

When splitting, do not create a directory `README.md` by default. The directory structure and file names are already useful index information. Put navigation in the parent topic file, repository `README.md`, or `docs/ai.md` only when it adds real value.

## Agent Documentation Principles

- Treat code, schemas, tests, deployment files, and ADRs as facts of record.
- Make the repository `README.md` and `docs/ai.md` short, current, and highly linkable; do not create separate index or context-map files unless the project explicitly asks for them.
- Keep one canonical AI first-read list. Keep AI-specific first-read links, question routing, agent operating rules, and gotchas in `docs/ai.md` by default.
- Keep `docs/ai/prompts/` and `docs/ai/evals/` for reusable task assets. Do not move project facts, agent rules, first-read routing, or gotchas there.
- Keep C4 L1 and L2 stable and hand-maintained; use C4 L3 for complex containers, and use C4 L4 only for code structures that cannot be understood locally.
- Keep future work out of current-fact docs until accepted or implemented. Store optional libraries, provider candidates, rollout advice, and backlog notes under product requirements or an ADR with explicit decision status.
- Write ADRs for consequential architecture, technology, or policy decisions, not routine implementation details.
- Prefer machine-readable contracts for APIs and events.
- Avoid duplicating setup commands, environment variables, and API examples across many prose files.
- Use normal relative Markdown links between project docs, and use same-file `#anchors` for headings.
- Avoid root-relative links such as `/docs/architecture/config.md` unless the repository already requires them. After moving or renaming docs, validate changed links.
- When multiple agent instruction files exist, keep one canonical source and link or mirror intentionally.
- Treat the annotated structure as categories to preserve, not files to blindly create. Prefer fewer, denser, well-indexed files over many thin stubs.
- Treat split C4 component filenames as project-specific. Avoid placeholder component files that do not match the actual system.
- Treat code locators as curated maps, not generated inventories. They should help an agent choose where to start, then point back to code as the fact of record.

## Annotated Structure

Use this as an information architecture, not a required file tree. Route durable project facts to the owning node below; do not duplicate product, architecture, API, testing, operations, repo-map, or code-locator facts in AI helper docs. Node labels intentionally omit `.md`: each node may be a section, a standalone file, or a directory with child files according to the File-First Split Rule. The comments explain ownership and update triggers; do not include the comments in actual names.

```text
docs/                                      # Long-lived project documentation root
  product                                 # Owns product goals, users, vocabulary, requirements, boundaries, and non-goals; update when product behavior, naming, UX contracts, accepted requirements, or future scope changes.
    requirements                          # Owns accepted, implemented, candidate, rejected, or historical requirements with decision state labels such as Candidate, Proposed, Accepted, Rejected, or Implemented; update when scope, acceptance criteria, UX contracts, or decision state changes.
    feature-roadmap                       # Owns optional candidate backlog/roadmap with decision state labels, sources, trigger conditions, constraints, and rollout order; update when candidate scope, decision state, or rollout order changes.

  architecture                            # Owns architecture overview, C4 L1/L2, data model, config summary, security summary, deployment summary, and quality attributes; update when boundaries, responsibilities, state model, topology, major flows, or quality constraints change.
    overview                              # Owns major modules, dependencies, boundaries, responsibility splits, and design principles; update when architecture boundaries or responsibilities change.
    c4-system-context                     # Owns C4 L1 users, external systems, system boundary, and trust boundary; update when actors, external systems, or trust boundaries change.
    c4-container                          # Owns C4 L2 apps, services, databases, queues, workers, and third-party containers; update when containers or runtime topology change.
    c4-components                         # Owns C4 L3 component views for real containers or component groups; update when component boundaries, ownership, or important interactions change.
    data-model                            # Owns entities, relationships, constraints, migrations, status definitions, enum semantics, and data ownership; update when schema, states, lifecycle semantics, or data dictionary entries change.
    config                                # Owns config roots, profiles, schema, path rules, examples, environment expansion, removed names, and migrations; update when config fields, profile behavior, paths, defaults, or migrations change.
    security                              # Owns authentication, authorization, secrets, data protection, destructive-operation safety, permissions, and threat model; update when safety, preview/confirmation, permissions, or trust behavior changes.
    dynamic-login-flow                    # Owns one important runtime sequence, state transition, or cross-boundary flow; update when that flow changes.
    deployment                            # Owns hosted environments, networks, runtime topology, deployment trust boundaries, and production layout; update when deployment topology or runtime architecture changes.
    adr                                   # Owns Architecture Decision Records; add an ADR when a consequential architecture, technology, or policy decision is made.
      0001-record-architecture-decisions

  engineering                             # Owns setup, repo map, conventions, testing, debugging, release, migrations, and code locator; update when commands, workflow, build/package layout, migration guidance, tests, repo structure, or problem entry paths change.
    setup                                 # Owns local setup, dependencies, environment variables, initialization, common failures, and local runtime layout; update when install, run, debug, env, or local path behavior changes.
    testing                               # Owns test strategy, check commands, fixtures, coverage boundaries, and required regression themes; update when test commands, coverage expectations, or fixture profiles change.
    release                               # Owns versioning, build/package steps, release defaults, approval, deployment handoff, and verification; update when packaging, release config, or release verification changes.
    migrations                            # Owns database, config, data repair, and rollback migration guidance; update when schema, config, or data migration behavior changes.
    repo-map                              # Owns system map: directory/module responsibilities, major feature distribution, entry points, and ownership; update when repo structure, module boundaries, feature locations, or entry points move.
    code-locator                          # Owns problem-to-file entry index and change recipes; update after solving recurring or subtle problems with files involved, invariants/traps, and focused verification.

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

  ai                                      # Owns agent rules, first-read map, question routing, and gotchas; update when repeated AI mistakes, retrieval paths, guardrails, or docs routing changes.
    prompts                               # Optional reusable AI prompts; keep only when actually reused. Not a facts-of-record area.
      doc-audit                           # Owns reusable human/CI/agent documentation audit prompt; must not contain project truth; update when audit output expectations or docs impact categories change.
      adr-writer                          # Owns reusable ADR drafting prompt; must not contain project truth; update when ADR format or decision workflow changes.
    evals                                 # Optional reusable documentation evals; keep only when actually reused. Not a facts-of-record area.
      doc-freshness                       # Owns reusable eval for whether agents can answer project questions from current docs and code; update when questions, expected source docs, or facts of record change.

  ownership                               # Owns owners, update cadence, facts of record, and stale-document review rules; update when ownership, review cadence, or canonical fact sources change.
  changelog                               # Owns user-visible changes, migrations, breaking changes, and release notes; update for releases, breaking changes, migrations, and user-visible behavior changes.
```

## Cross-Cutting Change Rule

Start from the owning node named in the Annotated Structure. When a change crosses boundaries, update each affected owner in the same change instead of copying the same facts into multiple places.

- API behavior changes may affect API docs, machine-readable contracts, examples, tests, and changelog entries.
- Config schema, profile, path, or default changes may affect architecture config docs, engineering setup/migration docs, examples, and tests.
- Destructive-operation, permission, preview, confirmation, or rollback behavior may affect architecture security docs, operations rollback docs, API safety notes, and tests.
- Architecture boundary, runtime topology, or responsibility changes may affect architecture overview, C4 views, deployment or operations docs, and ADRs when the decision is consequential.
- Local setup, build, packaging, release, or test workflow changes may affect engineering docs and the repository README when the project entry point changes.
- Framework-specific command or API bridge changes must load the relevant rule file, such as `rules/tauri-command-api.md`, before updating API docs and wrappers.
- Future-work suggestions belong in product requirements or roadmap docs with decision status until accepted or implemented; promote only stable resulting facts into current-fact docs.
- Repeated AI mistakes or retrieval failures belong in `docs/ai.md`; duplicated cross-topic facts should be moved to their owning docs and removed from helper prose.

## Repo Map And Code Locator Rule

Keep structural navigation and problem-first navigation separate when both are useful.

`repo-map` is the system map. It helps an agent understand the codebase shape before making changes.

`code-locator` is the problem entry index. It answers: for this issue or workflow, where should I look first, what invariant must not break, and what focused check should I run?

## Future Work Promotion Rule

Future work, backlog, optional providers, rollout advice, and candidate ideas must stay out of current-fact docs until accepted or implemented.

When a candidate becomes accepted or implemented, promote only the stable resulting facts into the owning current-fact nodes. Leave historical candidate context in `product/requirements`, `product/feature-roadmap`, or an ADR.

## Framework-Specific Rules

For Tauri desktop apps, load `rules/tauri-command-api.md` before creating or updating Tauri command API documentation.
