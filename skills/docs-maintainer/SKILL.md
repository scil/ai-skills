---
name: docs-maintainer
description: Create, organize, audit, or maintain an AI-agent-first software project documentation system. Use when an AI agent needs to scaffold a docs/ structure, route facts into a documentation system the project already has (an agent contract, a spec system, a plan doc) instead of building a parallel tree, decide where a durable fact belongs, prepare agent-readable project context, define documentation facts of record, add C4 architecture docs, create ADR/API/runbook documentation, review code changes for documentation impact, or audit docs for staleness.
---

# AI Agent Project Documentation System

## Purpose

Use this skill to create and maintain project documentation whose primary consumer is an AI coding agent. Human readability still matters, but the documentation system must first make project facts discoverable, stable, linkable, and safe for agents to use.

For the human-readable Chinese equivalent of this skill, see `for-human/SKILL.zh.md`. Do not load that file during normal agent operation unless the user explicitly asks for the Chinese human version.

## Operating Model

Use the path that matches the task.

### Creating Documentation

1. Inspect the repository shape, source code, existing docs, API contracts, deployment files, tests, and examples.
2. If this is the first time this documentation system is being created in the repository (no existing `docs/` tree), ask the user whether the documentation should live in the in-repo `docs/` tree or in a local Obsidian vault. Keep exactly one location; do not create both. If the user picks a vault, load the `obsidian-vault-ops` skill, create the Annotated Structure inside the vault instead of `docs/`, and leave a single short pointer note in the repository (for example in the repository `README.md` or `docs/ai.md`) recording the vault name and folder so later agents can find it. If the user picks `docs/`, or if a `docs/` tree already exists, proceed with the in-repo `docs/` tree only and do not ask again in this session.
3. Identify facts of record: source code, schemas, tests, ADRs, deployment config, API specs, runbooks, and product glossary.
4. Choose owning nodes from the Annotated Structure, then apply the File-First Split Rule.
5. Create the smallest useful documentation structure. Do not scaffold empty folders or many tiny files that the project cannot maintain.
6. Prefer stable, agent-readable docs with clear headings, short sections, explicit links, and unambiguous ownership.
7. Add PlantUML diagrams for architecture, key runtime flows, and hard-to-follow nodes per the Diagramming rules below.
8. Validate documentation with available checks such as Markdown lint, link checks, spell checks, OpenAPI/AsyncAPI validation, diagram rendering, or repo-specific CI.

### Adopting An Existing System (route, do not scaffold)

Most repositories that already run agents have a documentation system before this skill arrives: an agent contract (`AGENTS.md` / `CLAUDE.md`), a requirements or spec system (OpenSpec or similar), a plan or product doc, package code whose types *are* the API contract. Do not create the Annotated Structure beside them — a parallel tree gives every fact two owners.

1. Build an **Ownership Map** first (`templates/ownership-map.md`): one row per fact type → the owner that already exists → notes. Walk every node of the Annotated Structure and either map it to an existing owner or mark it deliberately skipped, with the reason, so the skip reads as a decision and not an omission.
2. Typical mappings: `ai` → the agent contract (no `docs/ai.md`; nested contracts are thin pointers upward) · `product/requirements` and `architecture/adr` → the spec system (a change's design doc is the ADR) · `architecture` → one hand-maintained C4 L1/L2 file, no L3/L4 subtree · `api` → the code, when routers, validators and shared types are the contract (no `docs/api/`) · `engineering/setup` and `testing` → the contract's command and testing sections · `engineering/code-locator` → one curated file · `product` → the plan doc · `operations` and `changelog` → skipped until incidents or releases exist.
3. Add a new file only when no owner fits and the File-First Split Rule justifies it, and follow the repository's existing human-docs convention (its folder naming, numbering, language) rather than this skill's node names.
4. Mark prose that mirrors code as **code-wins**: when the two disagree, the code is the fact of record and the prose is corrected in the same change.

### Auditing For Staleness

1. Check each owner against current code, schemas, and tests as facts of record; flag prose that contradicts code rather than trusting the prose.
2. Verify that every path, route, command, and file a doc names still exists (`ls` it); a sentence about something that is gone is the most common stale fact.
3. Refresh a `<!-- Last reviewed: YYYY-MM-DD -->` marker whenever an owner is revised; a marker older than the code it describes is a queue.
4. Move any fact duplicated across owners back to its single owner and delete the copies; when a section keeps regrowing or a fact keeps reappearing, trace what produces it (a rule, a tool, a habit) and fix that too — `ai-docs-organizing` → "Source and symptom".

### Updating Documentation

1. Inspect the code or architecture change, affected source files, existing docs, tests, and recent diffs.
2. Start from the owning nodes in the Annotated Structure and update only the affected docs.
3. If an implemented change introduces a new concept, domain term, UI label category, config/API name, status, role, or grouping, add it to the owning vocabulary, glossary, data dictionary, or API/config documentation.
4. Keep volatile implementation details close to code and schemas; link to them instead of duplicating them across prose docs.
5. When a change crosses boundaries, update each affected owner in the same change.
6. Record consequential architecture, technology, or policy decisions as ADRs.
7. Update or add PlantUML diagrams in the same change when an architecture boundary, key flow, or diagrammed hard-to-follow node changes; treat an outdated diagram as a documentation defect equal to outdated prose.
8. Validate changed docs with the available project checks.

## File-First Split Rule

Use the Annotated Structure to choose the owning node, then decide whether that node should be a section, standalone file, or directory.

Start with one Markdown file per documentation topic. Split only when the topic is large, high-risk, independently owned, heavily linked, machine-readable, frequently reviewed, or likely to create real edit conflicts.

When splitting, do not create a directory `README.md` by default. The directory structure and file names are already useful index information. Put navigation in the parent topic file, repository `README.md`, or `docs/ai.md` only when it adds real value.

## Agent Documentation Principles

- Treat code, schemas, tests, deployment files, and ADRs as facts of record.
- Make the repository `README.md` and `docs/ai.md` short, current, and highly linkable; do not create separate index or context-map files unless the project explicitly asks for them.
- Keep one canonical `docs/ai.md` for project-specific navigation anchors, routing pointers, agent operating rules, and gotchas. Do not make its entry-point list a required reading list.
- Keep `docs/ai/prompts/` and `docs/ai/evals/` for reusable task assets. Do not move project facts, agent rules, navigation anchors, routing pointers, or gotchas there.
- Keep C4 L1 and L2 stable and hand-maintained; use C4 L3 for complex containers, and use C4 L4 only for code structures that cannot be understood locally.
- Keep future work out of current-fact docs until accepted or implemented. Store optional libraries, provider candidates, rollout advice, and backlog notes under product requirements or an ADR with explicit decision status.
- Write ADRs for consequential architecture, technology, or policy decisions, not routine implementation details.
- Prefer machine-readable contracts for APIs and events.
- Avoid duplicating setup commands, environment variables, and API examples across many prose files.
- Use normal relative Markdown links between project docs, and use same-file `#anchors` for headings.
- Avoid root-relative links such as `/docs/architecture/config.md` unless the repository already requires them. After moving or renaming docs, validate changed links.
- When multiple agent instruction files exist, keep one canonical source and link or mirror intentionally.
- The agent contract is read under a byte budget by at least one harness (Codex cuts its `AGENTS.md` chain at 32 KiB with no notice), so it holds rules, not inventories: an executable recipe, a list of scripts, a retired environment's history, and any per-skill listing leave it. A skill's trigger lives in that skill's own `description`; which shared skills a repo links in lives in the ignore-file manifest its link script reads; a project override of a vendored skill lives in an `OVERLAY.md` inside that skill's directory. Loading model, budgets, and the diet procedure: `ai-docs-organizing`.
- Repeated AI mistakes belong in the contract's guard register as positive rules, each with its incident and the test or spec that carries the detail — not in helper prose, and not in one agent's private memory, which the other agent never sees.
- Treat the annotated structure as categories to preserve, not files to blindly create. Prefer fewer, denser, well-indexed files over many thin stubs.
- Treat split C4 component filenames as project-specific. Avoid placeholder component files that do not match the actual system.
- Treat code locators as curated maps, not generated inventories. They should help an agent choose where to start, then point back to code as the fact of record.

## Diagramming

Use PlantUML for architecture, key runtime flows, and hard-to-follow nodes. Do not diagram trivial or self-evident structures.

- Add a PlantUML diagram to C4 architecture docs (`c4-system-context`, `c4-container`, `c4-components`) to depict actors, containers, components, and their boundaries, alongside the required prose.
- Add a PlantUML sequence or activity diagram to important runtime flows such as `dynamic-login-flow` and other cross-boundary flows named in the Annotated Structure.
- Add a PlantUML diagram to a `code-locator` or `repo-map` entry only when the structure is a genuine trap: nontrivial state machines, retry/rollback paths, concurrency, or multi-service handoffs that are hard to reconstruct from code alone. Do not diagram straightforward call chains.
- Write diagrams as fenced ` ```plantuml ` code blocks directly in the owning node, next to the prose they illustrate. Use a linked `.puml` file only when the project's documentation tooling requires external diagram files.
- Keep each diagram small and focused on one boundary, flow, or component group. Split into multiple diagrams instead of building one dense diagram.
- Validate diagrams the project's checks can render, such as a PlantUML CLI, editor preview, or CI rendering step, before treating a diagramming task as complete.
- Update the diagram in the same change as the code, boundary, or flow it depicts.

## Annotated Structure

Use this as an information architecture, not a required file tree. Route durable project facts to the owning node below; do not duplicate product, architecture, API, testing, operations, repo-map, or code-locator facts in AI helper docs. Node labels intentionally omit `.md`: each node may be a section, a standalone file, or a directory with child files according to the File-First Split Rule. The comments explain ownership and update triggers; do not include the comments in actual names.

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

## Cross-Cutting Change Rule

Start from the owning node named in the Annotated Structure. When a change crosses boundaries, update each affected owner in the same change instead of copying the same facts into multiple places.

- API behavior changes may affect API docs, machine-readable contracts, examples, tests, and changelog entries.
- Config schema, profile, path, or default changes may affect architecture config docs, engineering setup/migration docs, examples, and tests.
- Destructive-operation, permission, preview, confirmation, or rollback behavior may affect architecture security docs, operations rollback docs, API safety notes, and tests.
- Architecture boundary, runtime topology, or responsibility changes may affect architecture overview, C4 views, deployment or operations docs, and ADRs when the decision is consequential.
- Local setup, build, packaging, release, or test workflow changes may affect engineering docs and the repository README when the project entry point changes.
- New concepts or terms may cross documentation boundaries; route them through the owning glossary, data model, API/config docs, or AI gotchas as appropriate.
- Command, build, environment, or workflow changes belong in the agent contract's command section and the environment example file; do not duplicate them into other prose.
- Schema, enum, or contract changes update the owner in code (schema, validators, routers), the spec scenarios that describe the behaviour, the validators derived from the schema, and the tests, in the same change; a new domain term or status goes to the owning spec requirement and the plan's terminology, never scattered across helper prose.
- Framework-specific command or API bridge changes must load the relevant rule file, such as `rules/tauri-command-api.md`, before updating API docs and wrappers.
- Future-work suggestions belong in product requirements or roadmap docs with decision status until accepted or implemented; promote only stable resulting facts into current-fact docs.
- Repeated AI mistakes or retrieval failures belong in `docs/ai.md`; duplicated cross-topic facts should be moved to their owning docs and removed from helper prose.

## Repo Map And Code Locator Rule

Keep structural navigation and problem-first navigation separate when both are useful.

`repo-map` is the system map. It helps an agent understand the codebase shape before making changes.

`code-locator` is the problem entry index. It answers: for this issue or workflow, where should I look first, what invariant must not break, and what focused check should I run?

Entry discipline: add an entry after solving a recurring or subtle problem — the trigger, the start files, the invariant or trap, the smallest verifying check; refresh an entry in the same change as a fix that touches a path it names; delete entries that go stale. Keep an entry an entry: when one has grown into an essay, its invariant stays and its rationale moves to the spec, ADR, or code comment it cites.

## Templates

Use `templates/docs-ai.md` as the starter template for project `docs/ai.md` files. Keep the generated file short, project-specific, and navigational: it should point to the owning documentation system rather than duplicate product, architecture, API, config, safety, testing, repo-map, or code-locator facts.

Use `templates/ownership-map.md` when adopting an existing system: it is the table a project-local docs skill is built around, one row per fact type, and the deliverable of the Adopting path.

## Future Work Promotion Rule

Future work, backlog, optional providers, rollout advice, and candidate ideas must stay out of current-fact docs until accepted or implemented.

When a candidate becomes accepted or implemented, promote only the stable resulting facts into the owning current-fact nodes. Leave historical candidate context in `product/requirements`, `product/feature-roadmap`, or an ADR.

## Framework-Specific Rules

For Tauri desktop apps, load `rules/tauri-command-api.md` before creating or updating Tauri command API documentation.

## Obsidian Location Rule

Ask about the storage location only once per project, at first-time creation of the documentation system; do not ask again on later updates.

Store the Annotated Structure in exactly one location: the in-repo `docs/` tree, or a local Obsidian vault chosen via the `obsidian-vault-ops` skill. Do not create both and do not mirror content between them; a single location is the only source of record. When the vault is chosen, apply every rule in this skill (Annotated Structure, File-First Split Rule, Cross-Cutting Change Rule, Diagramming) inside the vault folder in place of `docs/`, and keep the repository pointer note current if the vault name or folder moves.
