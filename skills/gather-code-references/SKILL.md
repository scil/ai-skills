---
name: gather-code-references
disable-model-invocation: true
description: Use when Codex needs to research, inspect, compare, and organize third-party coding resources before implementation or project planning. Trigger for requests to gather references, build a reference collection/corpus, study official docs, mature open-source projects, templates, package source/types, changelogs, migration guides, security advisories, architecture examples, dependency choices, existing Codex skills, or ecosystem conventions for a software project.
---

# Gather Code References

Turn external software resources into an open Markdown reference collection. The goal is greedy understanding: extract every useful reference point from good resources without forcing them into a narrow matrix.

## Workflow

1. Inspect the local project first:
   - Read project instructions such as `AGENTS.md`.
   - Inspect package files, lockfiles, entrypoints, tests, build scripts, docs, and existing architecture.
   - Identify actual versions from the repo or installed packages.
   - Record project facts separately from assumptions.

2. Classify the research mode:
   - Greenfield or full rewrite.
   - Dependency, framework, runtime, or tooling upgrade.
   - Template, boilerplate, starter, or example mining.
   - Specific framework, language, library, or ecosystem work.
   - Release, deployment, CI, Docker, observability, or ops work.
   - Load `references/research-modes.md` for mode-specific source checklists.
   - Write a coverage plan. For each of the five views in step 5, write the questions this project needs answered. If the project does not touch a view, write "not needed" and the reason. Plan at least one source for every other view.

3. Gather credible resources:
   - Prefer official docs, official examples, source/types, migration guides, changelogs, and security advisories.
   - Use mature open-source projects and templates as pattern sources.
   - Inspect notable third-party dependencies used by mature projects; dependency choices are often a major part of the reference value.
   - Use blogs, issues, discussions, and AI summaries only as secondary evidence.
   - Search for failure modes on purpose. For the `code-plan-review` gates of the views in the coverage plan, search the chosen technologies' issues, security advisories, migration guides and changelogs.
   - If an existing Codex skill may help, use skill discovery before designing the workflow from scratch.

4. Create open resource dossiers:
   - Use `references/reference-collection-template.md`.
   - Give each resource a minimum identity block: source, credibility, context, project fit, adoptable points, and non-adoptable points.
   - After the minimum block, let the resource determine its own shape. Preserve rich internal structure when it matters.
   - For high-density resources such as excellent skills, project rules, architecture docs, or compact source files, keep the original or near-original structure when allowed.
   - For copyrighted external material, summarize decisions, structures, and short compliant excerpts instead of reproducing large passages.

5. Extract greedily, asking each resource one question per architecture view. The views and the quality model are the same standards `code-plan-review` uses, recorded in its `references/taxonomy.md`. They index findings across resources. A dossier keeps its own shape.
   - Scenarios: usage examples, user journeys, request flows, sign-in round trips, and reach. Reach covers machine visitors (search crawlers, link previews, AI-agent interfaces such as MCP) and people using assistive technology, another language or another device. A reach pitfall goes to `code-plan-review` gate S7.
   - Logical: API style, contracts, validation, serialization, entities and states, access rules.
   - Process: concurrency, queues, retries, timeouts, error handling, recovery, observability.
   - Development: module boundaries, dependencies and why they exist, testing layers, CI checks, scripts, docs, upgrade path.
   - Operations: configuration, environments, secrets, build, release, deployment, migrations, rollback, maintenance.
   - Tag each finding with the ISO/IEC 25010 characteristic it serves (security, performance efficiency, compatibility, reliability, maintainability, interaction capability, flexibility, safety, functional suitability).
   - File each known failure mode or pitfall under the `code-plan-review` node it matches, with the technology. It is a candidate binding entry for `code-plan-review/references/stacks/`. A pitfall no node names goes under "Outside the tree".

6. Synthesize the reference collection:
   - Build cross-resource theme indexes so the same insight can be compared across sources.
   - Maintain a decision pool with adopt, defer, reject, and needs-user-confirmation items.
   - Keep candidate project rules traceable to source resources.
   - Call out research gaps that would affect a future implementation plan.
   - Check coverage. Every view in the coverage plan ends with findings, a stated gap, or "not needed" with its reason.

7. Harvest the run into this skill. This step runs after every use. Its goal is to widen what the skill covers and what it can extract.
   - List what this run taught: a source type that paid off, a question a view was missing, a gap found late, a method that extracted more.
   - Put each lesson in its one home. A source type or checklist item goes in `references/research-modes.md`. A view question or template field goes in `references/reference-collection-template.md`. A workflow change goes in this file. A failure mode goes to `code-plan-review` as a binding entry. A fact true of one project stays in that project.
   - Widen an existing line before adding one. Never add a step or a file for one incident.
   - Record each change in `readme.md` under "Harvest log", dated, with the run that taught it.
   - Show the user the list and the planned edits, and edit only after a yes.

## Output

Default to one Markdown reference collection unless the user asks for a directory of reports. The collection should be useful as input to `$derive-project-plan`.

Do not write an implementation plan as the main output. Stop at researched reference material, structured options, source-backed candidates, and open questions.

## Guardrails

- Do not flatten rich resources into a closed table.
- Do not copy templates wholesale or import architectures just because they are polished.
- Do not rely on stars, popularity, or aesthetics alone.
- Do not skip version, peer dependency, license, or migration checks.
- Do not paste large chunks of copyrighted external source or documentation.
- Do not invent current facts for fast-moving libraries; verify them from local packages or current sources.

