---
name: ai-project-docs-maintainer
description: Create, organize, audit, or maintain an AI-agent-first software project documentation system. Use when an AI agent needs to scaffold a docs/ structure, prepare agent-readable project context, define documentation facts of record, add C4 architecture docs, create ADR/API/runbook documentation, or review code changes for documentation impact.
---

# AI Agent Project Documentation System

## Purpose

Use this skill to create and maintain project documentation whose primary consumer is an AI coding agent. Human readability still matters, but the documentation system must first make project facts discoverable, stable, linkable, and safe for agents to use.

For the human-readable Chinese equivalent of this skill, see `for-human/SKILL.zh.md`. Do not load that file during normal agent operation unless the user explicitly asks for the Chinese human version.

## Operating Model

1. Inspect the repository shape, existing docs, API contracts, deployment files, tests, and recent diffs.
2. Identify facts of record: source code, schemas, tests, ADRs, deployment config, API specs, runbooks, and product glossary.
3. Create the smallest useful documentation structure from the information architecture below. Do not scaffold empty folders or many tiny files that the project cannot maintain.
4. Prefer stable, agent-readable files with clear headings, short sections, explicit links, and unambiguous ownership.
5. Keep volatile implementation details close to code and schemas; link to them instead of duplicating them across prose docs.
6. For each code or architecture change, update only the affected docs and record consequential decisions as ADRs.
7. Validate documentation with available checks such as Markdown lint, link checks, spell checks, OpenAPI/AsyncAPI validation, diagram rendering, or repo-specific CI.

## Annotated Structure

Use this as the default information architecture, not a required file tree. The comments explain each entry; do not include the comments in actual file or directory names.

## README-First Structure Rule

Prefer a README-first layout for small or medium projects. A leaf in the structure below may be represented as:

1. a section inside the nearest parent `README.md`;
2. a standalone Markdown file;
3. a machine-readable contract file such as `openapi.yaml` or `asyncapi.yaml`.

Default to a parent `README.md` when the topic is short, the topics change together, the project has no separate owner for that topic, or a standalone file would contain only a few paragraphs. Split a leaf into its own file only when at least one of these is true:

- the file is expected to exceed roughly 80-120 lines or needs its own table of contents;
- the topic is high risk or frequently reviewed, such as security, deployment, rollback, or public API contracts;
- the topic has independent ownership, update cadence, or many incoming links;
- the topic has a durable lifecycle, such as ADRs, incidents, runbooks, or release notes;
- the content is machine-readable or validated by tooling;
- splitting reduces real edit conflicts between people or agents.

For example, a compact client app may use `api/README.md` for API direction, consumed upstreams, auth, errors, and examples; `engineering/README.md` for setup, repo map, testing, debugging, release, and migrations; and `operations/README.md` for runbooks, monitoring, incidents, and rollback. A larger backend with a public API may split those same sections into standalone files.

## C4 Component View Rule

Derive `architecture/c4/03-components/` from the project's actual C4 L2 containers and module boundaries. This directory is a C4 L3 view area, not a fixed set of files.

When creating or refreshing component docs:

1. Start with `03-components/README.md` for compact projects or when the component view is short.
2. Create standalone component files only for real containers or component groups that are complex enough to need their own page.
3. Name files after the actual architecture, such as `web-api.md`, `mobile-app.md`, `admin-console.md`, `orchard-modules.md`, `checkout-service.md`, `background-jobs.md`, `integration-adapters.md`, or `ml-pipeline.md`.
4. Do not create `backend-api.md`, `worker.md`, or `frontend-app.md` just because they appear in an example. Create those files only when they are accurate, useful views for this specific project.
5. Omit component views that do not exist. For example, a client-only app should not have an empty `worker.md`, and a backend-only service should not have a placeholder frontend component doc.

## Code Locator Rule

Preserve high-value code-location knowledge when it helps future agents start in the right files. A code locator is a compact problem-to-code map, not an exhaustive source inventory.

Use a code locator when existing docs, handoffs, or repeated work contain practical "if you see this issue, start here" knowledge, such as feature entry points, owning repositories/controllers, state files, platform config, tests, and common traps.

Default placement:

1. Use a `Code Locator` section inside `engineering/README.md` for broad repo-wide or developer-workflow navigation.
2. Use a `Code Locator` section inside `architecture/c4/README.md` or `architecture/c4/03-components/README.md` when the paths are tied to C4 components, dynamic flows, or cross-cutting architecture concerns.
3. Create a standalone `engineering/code-locator.md` only when the locator is large, heavily linked, independently maintained, or would exceed the README-first split guidance.

Good code locator entries usually include:

- the problem, feature, or workflow;
- the first files or directories to inspect;
- the invariant, trap, or ownership rule that matters;
- the focused tests, smoke checks, runbooks, or source-of-truth docs to verify.

Avoid turning the locator into a generated file list. Keep complete file inventories in `other.md` or generated tooling output, and keep stable module maps in architecture or repo-map docs.

## Future Work And Requirement Backlog Rule

Keep unimplemented suggestions separate from current facts. Future development ideas, optional libraries, candidate providers, rollout sequences, "could/should later" advice, and backlog items must not be written as if they are current architecture, API, operations, or code facts.

Default placement:

1. Use `product/requirements/README.md` for a compact backlog or roadmap section.
2. Create a standalone `product/requirements/<feature>-roadmap.md`, `<feature>-backlog.md`, or dated requirement file when the suggestion set has its own lifecycle, acceptance criteria, owner, decision status, or many incoming links.
3. Use an ADR only after the team makes a consequential architecture or technology decision.

Future-work docs should label each item with its decision state, such as `Candidate`, `Proposed`, `Accepted`, `Rejected`, or `Implemented`. Include the source, trigger condition, constraints, rough rollout order, acceptance criteria needed before implementation, and which docs must move when the item becomes accepted or implemented.

When a candidate becomes accepted or implemented, promote only the stable resulting facts into architecture, C4, API, engineering, operations, runbooks, changelog, facts, or gotchas as appropriate. Leave historical candidate context in the requirement doc or ADR rather than copying it everywhere.

## API Direction Rule

Every `api/` document must state whether it documents provided APIs, consumed APIs, or both. Do not mix these directions without explicit headings.

- **Provided APIs** are interfaces this project exposes to callers: HTTP routes, RPC methods, SDK methods, events, webhooks, plugin hooks, schemas, and error contracts. Facts of record are server routes/controllers, handlers, schemas, OpenAPI/AsyncAPI files, contract tests, and implementation tests.
- **Consumed APIs** are upstream interfaces this project calls or depends on: backend services, third-party APIs, SDKs, payment/auth/map/email providers, webhooks received from vendors, or sibling services. Facts of record are client/adaptor code, upstream official docs, observed responses, fixtures, mocks, and integration tests.

Use README sections for small projects:

```text
api/README.md
  Provided APIs
    Authentication
    Error model
    Examples
  Consumed APIs
    Authentication
    Error model
    Examples
```

When a direction has no content, either omit that direction entirely or include only `(None)` under its heading. Direction-specific topics such as authentication, error model, examples, quotas, and adapters must be nested under the relevant direction heading, not placed as siblings of `Provided APIs` or `Consumed APIs`.

Use subdirectories when both directions are substantial or owned independently:

```text
api/
  README.md
  provided/README.md
  consumed/README.md
```

Backend services usually have substantial **provided** API docs and may also have **consumed** API docs for upstream dependencies. Client apps usually have substantial **consumed** API docs and may explicitly state that they provide no public API.

```text
docs/                                      # Long-lived project documentation root
  index.md                                # Entry point: what the project is and where each reader or agent should start
  doc-map.md                              # Question-to-document map for fast retrieval by humans and AI agents
  ownership.md                            # Owners, update cadence, facts of record, and stale-document review rules

  product/                                # Product and domain knowledge: why the system exists and who it serves
    vision.md                             # Product goals, boundaries, non-goals, and success criteria
    users.md                              # User roles, permissions, core jobs, and important workflows
    requirements/                         # PRDs, user stories, acceptance criteria, scope changes, and candidate roadmaps
      README.md                           # Requirements index with links to active, historical, and candidate requirement docs
      feature-roadmap.md                  # Optional candidate backlog/roadmap for unimplemented future capabilities; label decision status
    glossary.md                           # Domain vocabulary shared by people, code, tests, and AI agents

  architecture/                           # System design knowledge: how the system is organized and constrained
    overview.md                           # Architecture summary: major modules, dependencies, and design principles
    c4/                                   # C4 views from system boundary down to selected code-level structures
      01-system-context.md                # C4 L1: users, external systems, system boundary, and trust boundary
      02-container.md                     # C4 L2: apps, services, databases, queues, workers, and third-party containers
      03-components/                      # C4 L3: project-specific components inside selected containers
        README.md                         # Compact component view index with sections per real container or component group
        project-specific-component.md     # Optional standalone L3 view named after an actual container/module, not a template label
      04-code/                            # C4 L4: only complex code structures that need explanation
        core-domain.md                    # Core domain code: state machines, algorithms, plugin models, or invariants
      code-locator.md                     # Optional problem-to-code locator when tightly tied to C4 components or flows; prefer a README section when compact
      dynamic/                            # Runtime behavior: sequences, state transitions, and cross-boundary flows
        login-flow.md                     # Login flow: authentication, sessions, error paths, and security boundaries
        order-lifecycle.md                # Business lifecycle: important states from creation through completion/cancelation
      deployment.md                       # Deployment view: environments, networks, config, release topology
    adr/                                  # Architecture Decision Records explaining why decisions were made
      0001-record-architecture-decisions.md # ADR example/template: status, context, decision, alternatives, consequences
    data-model.md                         # Entities, relationships, constraints, migrations, and data ownership
    security.md                           # Authentication, authorization, secrets, data protection, and threat model
    quality-attributes.md                 # Performance, reliability, observability, compliance, maintainability

  engineering/                            # Developer workflow knowledge: how to safely change and ship the system
    setup.md                              # Local setup, dependencies, environment variables, initialization, common failures
    repo-map.md                           # Codebase map: directory responsibilities, module boundaries, main entry points
    conventions.md                        # Engineering conventions: naming, layering, errors, logging, commits
    testing.md                            # Testing strategy: unit, integration, end-to-end, fixtures, coverage boundaries
    debugging.md                          # Debugging guide: logs, traces, useful commands, common diagnosis paths
    code-locator.md                       # Optional problem-to-code map: first files, ownership notes, traps, and focused checks for AI handoff
    release.md                            # Release process: versioning, build, approval, deployment, verification
    migrations.md                         # Migration guide: database, config, data repair, and rollback considerations

  api/                                    # Interface contracts, separated by API direction
    README.md                             # API direction index: provided APIs, consumed APIs, auth, errors, examples
    provided/                             # APIs this project exposes to callers; use when substantial enough to split
      README.md                           # Provided routes/events/SDK/plugin contracts and source-of-truth links
    consumed/                             # APIs this project calls or depends on; use when substantial enough to split
      README.md                           # Upstream APIs, third-party services, auth, quotas, risks, and adapters
    openapi.yaml                          # REST API contract: paths, requests, responses, errors, examples
    asyncapi.yaml                         # Event/message contract: channels, payloads, producers, consumers
    auth.md                               # Authentication and authorization: tokens, scopes, roles, permissions
    errors.md                             # Error model: codes, semantics, retry behavior, user-facing messages
    examples.md                           # Integration examples: realistic requests, responses, edge cases

  operations/                             # Runtime operations knowledge for recovery and production safety
    runbooks/                             # Step-by-step operational procedures for alerts, incidents, and manual tasks
      README.md                           # Runbook index organized by alert, service, or scenario
    incidents/                            # Incident records: timeline, impact, root cause, fix, prevention
      README.md                           # Incident index organized by date, system, and severity
    monitoring.md                         # Metrics, logs, traces, dashboards, alerts, thresholds
    rollback.md                           # Rollback guide: application, data, config, and post-rollback verification

  ai/                                     # AI-agent context that helps models understand and modify the project reliably
    AGENTS.md                             # Agent operating rules: workflow, forbidden actions, tests, review expectations
    context-map.md                        # First-read map for agents: important files, module boundaries, facts of record
    facts.md                              # Stable facts that agents may rely on without re-deriving every time
    gotchas.md                            # Common traps, hidden constraints, and repeated agent mistakes
    prompts/                              # Optional reusable task prompts for humans, CI, and automation agents
      doc-audit.md                        # Prompt for finding stale, missing, duplicated, or inconsistent docs
      adr-writer.md                       # Prompt for turning a technical decision into an ADR draft
      release-notes.md                    # Prompt for generating release notes from diffs, issues, or PRs
    evals/                                # Documentation evals that test whether agents can answer project questions
      doc-freshness.md                    # Freshness eval: checks whether docs match code, config, API, and tests
      api-doc-consistency.md              # API consistency eval: checks examples, contracts, and implementation behavior
    llms.txt                              # Optional LLM entry file with curated links and recommended reading order

  changelog.md                            # User-visible changes, migrations, breaking changes, and release notes
```

## About `docs/ai/prompts/`

`docs/ai/prompts/` is optional. It is not a facts-of-record directory and should not contain project truth.

Use it for reusable task prompts that humans, CI jobs, scheduled agents, or documentation agents can run repeatedly. Good examples:

- Audit documentation after a large PR.
- Draft an ADR from a technical decision.
- Generate release notes from merged PRs.
- Check whether examples still match the API contract.
- Ask an agent to refresh `docs/ai/context-map.md`.

If the project already has a preferred automation system, `docs/ai/prompts/` may be renamed to `docs/ai/tasks/`, `docs/ai/workflows/`, or removed. Keep it only when the prompts are actually reused.

## Maintenance Rules

Apply this impact matrix when reviewing changes:

```text
Provided public API change -> Update docs/api/provided or docs/api/README.md#provided-apis, machine-readable contracts, examples, changelog
Consumed upstream API change -> Update docs/api/consumed or docs/api/README.md#consumed-apis, adapters, examples, runbooks, risks
Event/message change       -> Update docs/api/asyncapi.yaml or direction-specific event docs, consumer/provider notes, relevant runbooks
Architecture boundary      -> Update docs/architecture/c4/02-container.md or 03-components/, add ADR if consequential
Core technology decision   -> Add docs/architecture/adr/NNNN-title.md
Feature ownership or first-read code paths -> Update engineering/README.md#code-locator, architecture/c4/README.md#code-locator, or a split code-locator.md
Future feature suggestion  -> Update docs/product/requirements/README.md or a candidate roadmap/backlog; label decision status and do not present it as current architecture/API fact until accepted
Data model change          -> Update docs/architecture/data-model.md and docs/engineering/migrations.md
Deployment/config change   -> Update docs/architecture/deployment.md, docs/engineering/setup.md, rollback docs
Testing strategy change    -> Update docs/engineering/testing.md
Alert/incident change      -> Update docs/operations/runbooks/ or docs/operations/incidents/
Repeated AI mistake        -> Update docs/ai/AGENTS.md, docs/ai/context-map.md, or docs/ai/gotchas.md
```

If the project uses README-first consolidation, apply the same impact matrix to the matching section in the nearest parent `README.md`. For example, update `docs/api/README.md#examples` instead of creating `docs/api/examples.md` unless the examples have grown enough to justify a standalone file. For API changes, preserve direction first: update `docs/api/README.md#provided-apis` for exposed contracts and `docs/api/README.md#consumed-apis` for upstream dependencies.

## Agent Documentation Principles

- Treat code, schemas, tests, deployment files, and ADRs as facts of record.
- Make `docs/doc-map.md` and `docs/ai/context-map.md` short, current, and highly linkable.
- Keep C4 L1 and L2 stable and hand-maintained.
- Use C4 L3 for complex containers, deriving component docs from real L2 containers and module boundaries; use C4 L4 only for code structures that cannot be understood locally.
- Keep code locators current when feature ownership, first-read files, state entry points, platform config, or focused tests move.
- Keep future work out of current-fact docs until accepted or implemented. Store optional libraries, provider candidates, rollout advice, and backlog notes under product requirements or an ADR with explicit decision status.
- Write ADRs for consequential decisions, not routine implementation details.
- Prefer machine-readable contracts for APIs and events.
- Separate API direction clearly. Never let a client-side consumed API note masquerade as the service's provided API contract, and never document a backend's provided API as if it were merely a client dependency.
- Avoid duplicating setup commands, environment variables, and API examples across many prose files.
- When multiple agent instruction files exist, keep one canonical source and link or mirror intentionally.
- Treat the annotated structure as categories to preserve, not files to blindly create. Prefer fewer, denser, well-indexed files over many thin stubs.
- Treat `03-components/` filenames as project-specific. Avoid placeholder component files that do not match the actual system.
- Treat code locators as curated maps, not generated inventories. They should help an agent choose where to start, then point back to code as the fact of record.

## Starter Task Prompts

Use these as files under `docs/ai/prompts/` or as automation prompts.

```text
Review the current git diff and identify documentation impact.
Output affected docs, reasons, proposed updates, whether an ADR is needed, and whether API contracts, runbooks, changelog, or agent rules must change.
Do not edit files yet; provide the plan first.
```

```text
Generate or refresh docs/ai/context-map.md from the repository.
Include first-read files, module boundaries, facts of record, common traps, areas where agents must not guess, and docs that must be updated after code changes.
```

```text
Draft an ADR for the following technical decision.
Include Status, Context, Decision, Alternatives, Consequences, Migration, and Follow-up.
Explain why the decision was made; do not repeat low-level implementation details.
```

```text
Check whether documentation matches the codebase.
Focus on setup commands, environment variables, API examples, config options, directory descriptions, and test commands.
Output mismatches, evidence locations, and recommended fixes.
```
