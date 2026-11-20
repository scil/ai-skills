---
name: project-docs
disable-model-invocation: true
description: Create, review, organize or maintain the documents AI coding agents read in a project — the instruction file (AGENTS.md for Codex and the cross-tool standard, CLAUDE.md for Claude Code, root or nested), what each harness loads (skills, hooks, per-agent memory, byte budgets), and every other durable fact (plans, ADRs, specs, generated docs). Use when a repo has no instruction file or /init proposes one, when an agent repeats a mistake that "should be in AGENTS.md" or misses a rule that is written down, when slimming an instruction file or a hot doc, when a second harness joins a repo, when deciding whether a rule belongs in the file, a hook, a linter or a skill, when deciding where a fact belongs or scaffolding docs/, when reviewing a change for documentation impact, when auditing docs for staleness, or when its sources may have changed (every run first checks a refresh gate).
---

# Project docs for agents

Hand-off: the content of one skill's `SKILL.md` → ai-skill-audit.

A **harness** is the program that runs a model (Claude Code, Codex CLI). Each decides on its own what it loads, what it truncates and which stores it can see — and none tells you when it drops something. An **instruction file** is the Markdown a harness injects into every session it starts in a repository: `AGENTS.md` for Codex and most other tools, `CLAUDE.md` for Claude Code. It is a behavioural layer, not a brake, and it is paid for on every turn. Every other fact must be discoverable, stable, linkable, and safe for an agent to act on. The system is organized by **loading layer** — how a fact reaches the agent and what each read costs: 0 always-loaded map (the instruction file) · 1 working notes (plans) · 2 system of record · 3 generated · 4 vendored references · 5 skills · 6 governance. Origin and evidence: [`readme.md`](readme.md).

## Principles

1. **Only what the repository cannot tell the agent; the environment is the source of truth, docs are a cache.** Code, schemas, tests, deployment files and ADRs are the facts of record. Prose that mirrors them is *code-wins*: when they disagree, fix the prose in the same change. A script list or "app X exists" copies what `ls` or `package.json` answers, and goes stale; cache only what cannot be looked up: the unwritten convention, the reason, the gotcha. Anything a generator can produce is generated and never hand-edited.
2. **One meaning, one owner.** Route each fact to its existing owner (the project's ownership map; the Annotated Structure in [`references/docs-system/structure.md`](references/docs-system/structure.md) is categories to preserve, not files to create). No parallel trees, no index files, no directory `README.md` by default. Three copies are three edits and one drift. The instruction file follows the same rule: `AGENTS.md` is canonical, `CLAUDE.md` is a one-line bridge plus Claude-only lines ([`references/paths/instruction-file.md`](references/paths/instruction-file.md)).
3. **The loading layer sets the budget and the writing rules.** Always-loaded material (an instruction file, a skill description, a memory index) is paid on every turn, for some harnesses against a hard byte cap; pointer-reached material costs only its pointer — until the pointer turns *hot*. The map carries rules and pointers only; plans are what agents read most and are living documents; a procedure is a skill, never a doc section; a hand-written API reference is not created by default. Measure bytes before and after.
4. **The repository is the only memory all agents share.** Agent memory holds how the user wants *that* agent to behave and *that* harness's quirks; project facts go to the repo.
5. **A rule is a wish until it has an enforcement layer.** Each rule and each ownership-map row names its check: a hook, a CI check, a linter rule, a test, a link check, a freshness marker, a generated-diff, a path-exists check — or the explicit tag `advisory`, written out.
6. **Grow by incident, prune by review.** A rule enters when a failure repeats, with `Instance:` and date; every PR asks *add, change, delete?*; a stale rule is worse than none because the file is trusted. Gardening runs on a cadence, not when someone notices.
7. **Respect the information hierarchy.** Steps performed, reference consulted, reference disclosed by pointer: three tiers. Recipes, retired-environment history and environment inventories leave the contract; rules stay as invariant + `Instance:` + the test or spec that enforces them — so does a code-locator entry grown into an essay.
8. **Future work has a decision state**, in a plan or a requirement, until accepted or implemented; a consequential decision is an ADR in MADR shape and is superseded, never edited ([`references/docs-system/cross-cutting.md`](references/docs-system/cross-cutting.md)).
9. **Non-functional facts get explicit owners** — security, reliability, performance — because they are the least documented in the wild and the least inferable from code.

## The loading model comes first

Before judging any document, establish per harness, and write down with the method used ([`references/loading/harness-loading.md`](references/loading/harness-loading.md)): **what it auto-loads and where it silently stops** (file names, imports, nested files, byte caps, skills directories, hooks), and **which stores it can see** — one agent's memory is invisible to the other.

Never take either from documentation alone. **Probe**: ask the agent, with file reads forbidden, to quote the last lines of the instructions it received and name the last heading. One minute settles what a week of "but it's in AGENTS.md" cannot.

## Every run starts with the refresh gate

Two registries, one per subject area: [`references/refresh/sources-instruction-file.md`](references/refresh/sources-instruction-file.md) (instruction files, context-file research) and [`references/refresh/sources-docs-system.md`](references/refresh/sources-docs-system.md) (documentation standards, plans, skills). Run the gate on the registry the chosen path rests on, or both when unsure: `pwsh -NoProfile -File scripts/check-sources.ps1 -Path <registry> -GateOnly`. Each registry's `gate-days:` line sets its gate (30 by default). If the gate is due, run the Refresh path first; it is short when nothing changed. Never skip the gate silently; if the network is unavailable, say so and continue with the sources as they stand.

## Source and symptom — fix both

A stale sentence, a duplicated fact, a regrowing section is a **symptom** of a producer still running: a rule, a generator, a hook's nudge, a memory, or an event nobody propagated. In one change: **name the producer** (`git log -S`, `git grep` every store); **fix it where first written and in every copy**, or it re-propagates; **fix the existing instances**; **add a guard** where one can exist; **record the trace** — *commit · rule · copies touched · guard*. Commands and known sources: [`references/loading/process.md`](references/loading/process.md) §7; worked example: [`readme.md`](readme.md), the ai-docs-organizing part.

## Paths

A run takes one path. Read its file, then follow its steps.

| Object | Paths | File |
|---|---|---|
| The instruction file (`AGENTS.md`, `CLAUDE.md`) | Create · Review · Update (grow from an incident) | [`references/paths/instruction-file.md`](references/paths/instruction-file.md) |
| The loading system across harnesses (instruction chains, skills roster, hooks, memory, hot pointer docs) | Audit and reorganize | [`references/paths/loading-system.md`](references/paths/loading-system.md) |
| Every other durable fact (plans, ADRs, specs, generated docs, ownership map) | Adopt an existing system · Create from nothing · Update after a change · Garden | [`references/paths/docs-system.md`](references/paths/docs-system.md) |
| The sources of this skill | Refresh | [`references/refresh/refresh.md`](references/refresh/refresh.md) |

**Refresh, in short**: run `scripts/check-sources.ps1` on a registry, read only the sources whose fingerprint moved, search for research and vendor announcements since the last refresh with the domain allowlist, write the dated entry in that registry's changelog, and *propose* edits to this skill for the user to accept. Sources carry an authority tier: vendor documentation and standards decide, research corroborates (two independent studies, or one that explains a vendor rule), exemplars illustrate, reports point. **Disputes**: when sources conflict, name each disagreement in the report with the sources on each side, the tier of each source, and which recommendation the sources' weight supports. Fingerprints and `last-refresh` update only after the user has seen the report.
