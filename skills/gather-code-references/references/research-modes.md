# Research Modes

Use these checklists to decide what to inspect. Add extra topics when a resource exposes more value.

## Greenfield Or Full Rewrite

Research broadly before implementation:

- Language, runtime, framework, package manager, and workspace model.
- Tooling: formatter, linter, typecheck, codegen, task runner.
- Project structure, module boundaries, API style, and contracts.
- Data, migrations, auth, sessions, permissions, and security posture.
- Error handling, validation, testing layers, and test runner.
- Logging, metrics, tracing, health checks, deployment, Docker, and configuration.
- Documentation, onboarding, CI/CD, release, changelog, semantic versioning, maintenance, and upgrade path.
- Dependencies worth studying separately.

Prefer a small walking skeleton first: app boot, one route/screen/job, one test, and one deployment path.

## Dependency Or Framework Upgrade

Inspect:

- Current package files, lockfiles, runtime version, and CI/test commands.
- Direct dependencies, transitive constraints, and peer dependencies.
- Official changelogs, migration guides, release notes, and security advisories.
- Installed package types/source when docs are ambiguous.
- Adapter/plugin compatibility and ecosystem constraints.

Do not bump major versions blindly or mix unrelated upgrades unless the dependency graph requires it.

## Template Or Example Mining

Compare at least two references when time allows:

- Maturity signals, dependency freshness, issue quality, docs, and license.
- Production-grade decisions versus demo shortcuts.
- Dependency list and the problems each dependency solves.
- Project structure, auth/security, data/migrations, API contracts, tests, CI/release/deploy.
- Required local adaptation.

Extract patterns, not file trees.

## Stack-Specific Research

Use for focused framework, language, library, or ecosystem work:

- Official docs, official examples, current stable version, and migration guide.
- Package source/types for unclear APIs.
- Compatibility notes for adapters/plugins.
- Mature open-source usage examples.
- Dependency lists from mature projects in the ecosystem.
- Known security, performance, and deployment guidance.

For fast-moving frameworks, verify current facts instead of relying on memory.

## Release And Ops

Inspect:

- Official deployment docs for the framework/runtime.
- Container image recommendations.
- Health/readiness/liveness conventions.
- Logging, metrics, tracing, secrets, and environment variable handling.
- CI examples from official docs or mature projects.
- Release tooling, changelog practices, rollback, and hardening guidance.

Do not add release automation before the repo's package and release boundaries are clear.
