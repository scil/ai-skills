# Open Reference Collection Template

Use this as a shape, not a cage. Add, remove, rename, and expand sections to match the resources being studied.

## Project Context

- Project path:
- User goal:
- Current stack and versions:
- Existing architecture:
- Important constraints:
- Known assumptions:

## Resource Dossiers

Create one dossier per resource. Keep the minimum identity block, then expand freely.

### Resource: `<name>`

Minimum identity block:

- Source:
- Resource type:
- Credibility:
- Version/date inspected:
- License or reuse constraints:
- Applicable context:
- Fit for this project:
- Adoptable points:
- Non-adoptable or overbuilt points:

Open extraction area:

Use whatever headings the resource deserves. Examples:

- Dependency map and why each dependency exists.
- Module structure and ownership boundaries.
- Runtime lifecycle, entrypoints, jobs, workers, or plugins.
- API, schema, validation, and serialization patterns.
- Error handling, retries, fallback, and recovery.
- Configuration, environment variables, secrets, and feature flags.
- Data storage, migrations, transactions, caching, and queues.
- Testing strategy, fixtures, mocks, contract tests, and coverage gates.
- Build tooling, package manager, monorepo model, lint, format, and typecheck.
- CI/CD, release, versioning, changelog, deployment, rollback, and observability.
- Security, permissions, auth/session, supply chain, and hardening.
- Performance, accessibility, compatibility, and operational constraints.
- Documentation, examples, onboarding, scripts, and developer experience.
- Code or docs worth reading again.
- Surprising patterns, anti-patterns, and unanswered questions.

## Theme Indexes

Use these to compare findings across resources. One index per architecture view (Kruchten 4+1, as in `code-plan-review/references/taxonomy.md`). Tag each entry with the ISO/IEC 25010 characteristic it serves.

### Scenarios

- Pattern:
- Sources:
- Quality:
- Benefits:
- Costs:
- Project fit:

### Logical

- Pattern:
- Sources:
- Quality:
- Benefits:
- Costs:
- Project fit:

### Process

- Pattern:
- Sources:
- Quality:
- Benefits:
- Costs:
- Project fit:

### Development

Dependencies go here, each with why it appears.

- Pattern or candidate:
- Sources:
- Quality:
- Benefits:
- Costs:
- Project fit:

### Operations

- Pattern:
- Sources:
- Quality:
- Benefits:
- Costs:
- Project fit:

### Failure Modes

- `code-plan-review` node:
- Technology:
- Shows up as:
- Fix:
- Sources:

A failure mode no node names goes under "Outside the tree", as a candidate node.

## Decision Pool

### Adopt

- Decision:
- Sources:
- Why:
- Conditions:

### Defer

- Decision:
- Sources:
- Why deferred:
- Trigger to revisit:

### Reject

- Decision:
- Sources:
- Why rejected:

### Needs User Confirmation

- Question:
- Options:
- Recommendation:
- Sources:

## Candidate Project Rules

- Rule:
- Basis:
- Source mapping:
- Confidence:
- Scope:

## Research Gaps

- Gap:
- Why it matters:
- How to resolve:
- Blocking level:
