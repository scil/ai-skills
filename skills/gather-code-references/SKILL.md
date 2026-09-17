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

3. Gather credible resources:
   - Prefer official docs, official examples, source/types, migration guides, changelogs, and security advisories.
   - Use mature open-source projects and templates as pattern sources.
   - Inspect notable third-party dependencies used by mature projects; dependency choices are often a major part of the reference value.
   - Use blogs, issues, discussions, and AI summaries only as secondary evidence.
   - If an existing Codex skill may help, use skill discovery before designing the workflow from scratch.

4. Create open resource dossiers:
   - Use `references/reference-collection-template.md`.
   - Give each resource a minimum identity block: source, credibility, context, project fit, adoptable points, and non-adoptable points.
   - After the minimum block, let the resource determine its own shape. Preserve rich internal structure when it matters.
   - For high-density resources such as excellent skills, project rules, architecture docs, or compact source files, keep the original or near-original structure when allowed.
   - For copyrighted external material, summarize decisions, structures, and short compliant excerpts instead of reproducing large passages.

5. Extract greedily by theme:
   - Dependencies and why they exist.
   - Module boundaries and project structure.
   - API style, data flow, validation, serialization, and contracts.
   - Error handling, logging, observability, and recovery.
   - Configuration, environments, secrets, and runtime behavior.
   - Testing layers, fixtures, mocks, CI checks, and quality gates.
   - Build, release, deployment, migrations, rollback, and maintenance.
   - Developer experience, scripts, docs, onboarding, and upgrade path.
   - Security, performance, accessibility, compatibility, and known failure modes.

6. Synthesize the reference collection:
   - Build cross-resource theme indexes so the same insight can be compared across sources.
   - Maintain a decision pool with adopt, defer, reject, and needs-user-confirmation items.
   - Keep candidate project rules traceable to source resources.
   - Call out research gaps that would affect a future implementation plan.

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

