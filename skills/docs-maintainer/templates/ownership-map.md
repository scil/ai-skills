# Ownership Map — template

The deliverable of the Adopting path: one row per fact type, routed to the owner the project already has. Copy it into the project's local docs skill (or the agent contract's canonical-sources section, if the project has no local skill) and fill in real paths. A node of the Annotated Structure that maps to nothing is written down as **skipped — reason**, so the gap reads as a decision.

| Fact / change type | Owner | Notes |
| --- | --- | --- |
| Repo-wide agent rules, command safety, architecture rules, testing discipline, domain guardrails | the agent contract (`AGENTS.md` / `CLAUDE.md`) | Rules, not inventories; read under a byte budget. Lists no skills. Nested contracts only point upward. |
| A skill's trigger | that skill's own `description` | Harnesses discover skills by scanning the skills directory; a skill is registered by existing. An order of work is a rule in the contract, never restated per skill. |
| Which shared skills this repo links in | the ignore-file lines the link script reads (e.g. `/.agents/skills/<name>/` in `.gitignore`) | One line per skill; the script has no list of its own. |
| A project override of a vendored skill | `OVERLAY.md` inside that skill's directory | The one project-owned file in a vendored tree; outside the upstream hash; read before the skill's own rules. |
| New or changed product behaviour, lifecycle, visibility, privacy, safety, payment | the spec system's change first (proposal → design → spec delta → tasks), then the main spec on archive | "Spec first" for functional decisions; each scenario names a test. |
| Consequential architecture / technology / policy decision (ADR) | the change's design doc | No separate `adr/` directory when the spec system already carries one. |
| Accepted behaviour contract, requirement + scenarios | the main spec for that capability | One scenario → one test at the right layer. |
| System boundary + containers (C4 L1/L2) | one hand-maintained architecture file | No L3/L4 subtree; architecture *rules* stay in the contract. |
| Product / domain plan, terminology, roadmap | the plan doc | |
| Origin story, audience, messaging guardrails | the product-context doc | Read before strategy or scoping work. |
| Market evidence | the research folder | Prioritization and risk, never a build blocker. |
| Design system, brand spec, visual direction, page copy | the design folder (+ the design and voice skills) | Code-wins where code embodies it (tokens, marks). |
| DB tables, relations, enums, indexes, derived validators | the schema package (code) | Facts of record; deltas documented as spec scenarios. |
| Cross-platform input contracts | the validators package (code) | |
| API contracts | the routers + validators (code) | No `docs/api/` when the code is the contract. |
| Auth config / generated schema | the auth package; generated output regenerated, never hand-edited | Document the regeneration step, not the diff. |
| Commands, build, env, workflow | the contract's command section + the env example file | Never duplicated into other prose. |
| Reusable AI prompts / evals | a prompts folder | Executable assets; must not hold project truth. |
| Structural repo map (what each directory is) | the contract's repository-map section | |
| Problem-to-file entry index | one curated code-locator file | Start / invariant / check per entry; grown after recurring problems; stale entries deleted. |
| Repeated AI mistakes / traps | the contract's guard register | Positive rule + incident + enforcing test. |
| Operations (runbooks, incidents, monitoring) | skipped until the first incident — reason: none exist yet | |
| Changelog | skipped — reason: releases are not user-facing yet | |
