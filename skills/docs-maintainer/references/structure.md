# Annotated Structure — by loading layer

An information architecture, not a required file tree. Every durable project fact is routed to one owning node; a node may be a section, a file, or a directory (File-First Split Rule). Since 2026-09-15 the nodes are grouped by **loading layer**: how the fact reaches an agent and what it costs on each read. The layer decides the writing rules for the node. Node labels omit `.md`; comments explain ownership and update triggers and are not part of names. Sources for each rule: [`sources.md`](sources.md); reasoning: [`../readme.md`](../readme.md).

```text
# Layer 0 — always loaded: paid on every turn by every agent
AGENTS.md / CLAUDE.md                 # The map. Boundaries, non-obvious commands, scoped verification, architecture rules, traps, and POINTERS into layers 1–6. No overview, no directory listing, no skill list, no procedure. Content rules: the ai-agents-md skill. Budget: ai-docs-organizing.

# Layer 1 — working notes: what agents read most (60.5% of documentation interactions are instruction files and working notes)
docs/plans                            # Execution plans as living documents. One file per piece of work that outlives a session.
  active/<yyyy-mm-dd>-<slug>          # Purpose & big picture · Progress (checkboxes, timestamps) · Surprises & discoveries · Decision log (every decision, rationale, date) · Outcomes & retrospective. Update on every working step.
  completed/                          # Moved here on completion with the retrospective written; stable facts promoted to layer 2 first; historical context stays here.
  tech-debt                           # Known debt: item · owner · grade · trigger that would make it worth paying. Update when debt is found or paid.

# Layer 2 — system of record: hand-maintained, reached by pointer, code-wins
docs/product                          # Goals, users, vocabulary, accepted requirements with decision state (Candidate · Proposed · Accepted · Rejected · Implemented), boundaries, non-goals. Update when product behaviour, naming, UX contracts or accepted scope change.
docs/architecture                     # The overview the contract must not carry, plus the structural facts.
  overview                            # Modules, dependencies, boundaries, responsibility splits, design principles. Update when boundaries or responsibilities change.
  c4-context                          # C4 L1: users, external systems, system and trust boundary; one diagram. Update when actors or boundaries change.
  c4-container                        # C4 L2: apps, services, stores, queues, workers, third-party containers; one diagram. Update when containers or topology change.
  data-model                          # Entities, relationships, constraints, status and enum semantics, data ownership. Update when schema or lifecycle semantics change. The generated schema (layer 3) is the fact; this node holds meaning.
  config                              # Config roots, profiles, schema, path rules, environment expansion, removed names. Update when fields, defaults, paths or migrations change.
  flows/<name>                        # One important runtime sequence or state transition each, with a sequence or activity diagram. Update when that flow changes.
  deployment                          # Hosted environments, networks, runtime topology, deployment trust boundaries. Update when topology changes.
  quality-attributes                  # The least-documented and least-inferable facts (security 14.8%, performance 14.5% of 2,303 context files). One owner each:
    security                          #   authn, authz, secrets, data protection, destructive-operation safety, permissions, threat model. Update when trust or safety behaviour changes.
    reliability                       #   SLOs, failure modes, retries, backups, rollback and recovery facts. Update when recovery or partial-failure behaviour changes.
    performance                       #   budgets (latency, bundle, memory), the measurements that back them, and where profiling lives. Update when a budget or its check changes.
docs/decisions                        # ADRs in MADR shape: Context · Decision drivers · Considered options · Decision outcome · Consequences · Confirmation. Status: proposed · accepted · deprecated · superseded by N. Add when a decision is architecturally significant; never edit an accepted ADR — supersede it.
docs/engineering                      # Navigation and conventions. Facts, never steps (steps are layer 5).
  repo-map                            # System map: what each directory or module is and owns, entry points. Update when structure or boundaries move.
  code-locator                        # Problem → start files → invariant/trap → smallest verifying check. Add after a recurring or subtle problem; refresh with fixes that touch a named path; delete stale entries. Read by search (grep the symptom or term), never whole; write entries in the words the user used to report the problem. Navigation is where measured guidance gains come from.
  conventions                         # Only conventions that differ from tool defaults and that no linter encodes; each names its enforcement or `advisory`. Update when a convention or its enforcer changes.
  testing                             # Strategy facts: layers, fixtures, what is never mocked, coverage boundaries, regression themes. Commands live in the manifest; the run recipe is a skill.
  versioning                          # Versioning and compatibility policy, release channels. The release procedure is a skill.
docs/incidents/<yyyy-mm-dd>-<title>   # Timeline, impact, root cause, fix, prevention. Add after notable incidents.
docs/changelog                        # User-visible changes, migrations, breaking changes. Update for releases and breaking changes.

# Layer 3 — generated: regenerate, never hand-edit; a CI diff check proves it
docs/generated                        # Each artefact records its generator command and source. Hand edits are a defect.
  db-schema                           #   from the schema package or migrations.
  api                                 #   route/command/event index from routers, handlers, validators; openapi.yaml / asyncapi.yaml when an external consumer needs a machine-readable contract and the framework can emit it. Hand-written API prose is the least-read documentation type (1.3%) and is not created by default.
  dependency-graph                    #   module or package graph, when the architecture rules are enforced by a tool that can print it.
  components                          #   C4 L3 views, only if generated ("only create component diagrams if you feel they add value, and consider automating their creation"); C4 L4 never ("most IDEs can generate this level of detail on demand").

# Layer 4 — vendored references: third-party knowledge the agent needs offline
docs/references/<library>-llms.txt    # A library's llms.txt or a pinned excerpt of its docs, with version, source URL and fetch date. Update when the dependency version changes.

# Layer 5 — procedures: skills, not docs
.agents/skills/<name>/SKILL.md        # Setup, release, migration, runbook-for-an-alert, doc audit, ADR drafting: multi-step procedures with scripts/ and references/. The description is the trigger. Project bindings (paths, commands, owners) are the part that changes after adoption — keep them in one place inside the skill or read them from the ownership map; never copy layer-2 facts into a skill body. Content rules for one SKILL.md (description, router body, references, slimming): the ai-skills-manager skill. Roster and budget: ai-docs-organizing.

# Layer 6 — governance: how the system knows it is current
docs/ownership-map                    # This template filled in: fact type → owner → layer → enforcement → reading rule. Update when an owner, enforcer or layer changes.
docs/quality                          # Per-domain and per-layer quality grade, freshness dates, gardening cadence, and the doc-lint configuration (link check, freshness-marker age, generated-diff, cross-link). Update on every gardening run.
docs/evals                            # Optional: questions an agent must answer from current docs and code, with the expected owner per question. Keep only while run.
```

## What moved, and why (2026-09-15)

| Before | After | Reason (source) |
|---|---|---|
| `ai` node with `templates/docs-ai.md` | Layer 0, content owned by `ai-agents-md` | one owner per fact; the instruction file's content has its own skill |
| `product/feature-roadmap` and "future work" scattered | `plans/` as layer 1 with the ExecPlan shape | agents read working notes far more than classical docs (Gao & Chen); plans as first-class artefacts (OpenAI harness post; Codex ExecPlans) |
| `api/provided`, `api/consumed`, `openapi.yaml`, `asyncapi.yaml` as hand-maintained docs | `generated/api`, machine-readable only when a consumer needs it; consumed-API facts live in adapters, fixtures and `references/` | code is the contract; API references are 1.3% of agent documentation reads |
| `c4-components` hand-drawn | `generated/components`, or skipped | C4's own guidance on component and code diagrams |
| `engineering/setup`, `release`, `migrations`, `operations/runbook-*`, `ai/prompts` | Layer 5 skills; facts they need stay in layers 2–4 | "a section that has grown into a procedure rather than a fact" is a skill (Anthropic); reference task files rather than grow the main file (OpenAI) |
| `architecture/security` alone | `quality-attributes/{security, reliability, performance}` | the two least-covered categories in 2,303 files; least inferable from code |
| `ownership` node | Layer 6 `ownership-map` + `quality` + optional `evals` | mechanical enforcement and doc-gardening (OpenAI harness post); freshness as data, not a comment |
| `architecture/dynamic-login-flow` | `architecture/flows/<name>` | same content, named for what it is |

## Mapping the structure onto a system the project already has

When adopting, each node maps to an existing owner or is skipped with a reason. Typical mappings:

| Node | Existing owner | Note |
| --- | --- | --- |
| Layer 0 | the agent contract (`AGENTS.md`, `CLAUDE.md` bridge) | content per `ai-agents-md`; nested contracts point upward only |
| `plans/` | a spec system's change folders (proposal → design → tasks), or a plan doc | the change's design doc doubles as the ADR when it records a consequential decision; OpenSpec projects: [`adopting-openspec.md`](adopting-openspec.md) |
| `product`, `decisions` | the spec system | no separate `adr/` when the spec system carries decisions |
| `architecture` | one hand-maintained C4 L1/L2 file | no L3/L4 subtree; architecture *rules* stay in the contract |
| `generated/api` | the code, when routers, validators and shared types are the contract | no `docs/api/` |
| `engineering/testing`, `versioning` | the contract's verification lines + the manifest + the environment example file | no duplication into prose |
| `engineering/code-locator` | one curated file | entry discipline below |
| Layer 5 | the repo's `.agents/skills/` and linked shared skills | a procedure found in a doc moves here |
| `ownership-map` | the map itself | committed where the agents read it |
| `quality`, `references`, `incidents`, `changelog` | skipped until the first gardening run, vendored doc, incident or release | written down as skipped, with the reason |

## Where the structure lives

Ask once per project, at creation: the in-repo `docs/` tree or a local Obsidian vault (via `obsidian-vault-ops`). Never both. With a vault, apply every rule inside the vault folder in place of `docs/`, and leave one pointer in the repository naming the vault and folder. Layers 0, 3 and 5 always stay in the repository: the harness reads them there.

## Repo map and code locator

`repo-map` is the system map (what each directory is); `code-locator` is the problem entry index (for this issue, where to look first, what must not break, what to run). Both are curated, both point back to code. Locator entry discipline: add after a recurring or subtle problem — trigger, start files, invariant or trap, smallest verifying check; refresh in the same change as a fix that touches a named path; delete stale entries; when an entry has grown into an essay, the invariant stays and the rationale moves to the ADR, spec or code comment it cites.

Two rules that follow from the locator being a lookup table, not a narrative:

- **Read it by search, not whole.** The locator is a problem index; the reader arrives with a symptom. Grep the file for the symptom, the error text, the user's term or the path, and read only the matching entries. The skill or contract line that routes to the locator says so ("search `code-locator.md` for the term; do not read it whole"). A locator that has to be read end to end has become a doc and needs the hot-doc diet.
- **Write entries in the user's words.** The trigger line of an entry uses the vocabulary the user used when reporting the problem — their name for the feature, the error as they saw it, the phrase they typed — with the code's term beside it when the two differ. The next search will be in the user's words, not the code's. Refactoring an entry into "correct" terminology is how entries stop being found.

## Hot documents: the reading rule

A layer-2 doc that the contract or two or more skills name as *the* place for a kind of question is read whole by every task of that kind. Above ~20 KB, give it a question-first map at the top (section → question it answers → owner of the shipped behaviour) and put the reading rule — *map, then section, then the owner it names* — in every skill that routes to it. Diet before splitting: `ai-docs-organizing` → Hot pointer docs.
