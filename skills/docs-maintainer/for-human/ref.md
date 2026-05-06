# Human Maintainer Reference

Reference date: 2026-05-04

This file is for humans maintaining `ai-project-docs-maintainer`. It lives under `for-human/` because it is not part of the runtime skill instructions and should not be copied wholesale into `SKILL.md`.

## Why This File Exists

Keep ecosystem notes, candidate skills, links, and maintenance rationale here so `SKILL.md` stays small and agent-focused.

Use this file when:

- Comparing this skill with existing documentation-related skills.
- Deciding whether to borrow patterns from another skill.
- Updating the human-facing Chinese reference.
- Reviewing whether reusable prompts should stay as examples or be moved into project docs.

## Discovery Commands Used

```powershell
npx skills find documentation
npx skills find ADR documentation
```

## Candidate Skills Found

### `github/awesome-copilot@documentation-writer`

- Installs: 16.5K
- Link: https://skills.sh/github/awesome-copilot/documentation-writer
- Install command: `npx skills add github/awesome-copilot@documentation-writer`
- Useful reference: general documentation writing workflow, especially Diataxis-style documentation categories.
- Maintenance note: good source for writing behavior, but this project should stay focused on documentation information architecture for AI agents.

### `addyosmani/agent-skills@documentation-and-adrs`

- Installs: 2K
- Link: https://skills.sh/addyosmani/agent-skills/documentation-and-adrs
- Install command: `npx skills add addyosmani/agent-skills@documentation-and-adrs`
- Useful reference: ADRs, README updates, changelog writing, and agent-oriented documentation conventions.
- Maintenance note: closest conceptual neighbor for this skill. Borrow ADR workflow patterns if needed, but avoid turning this skill into a general writing assistant.

### `anthropics/knowledge-work-plugins@documentation`

- Installs: 2.6K
- Link: https://skills.sh/anthropics/knowledge-work-plugins/documentation
- Install command: `npx skills add anthropics/knowledge-work-plugins@documentation`
- Useful reference: broad documentation tasks such as README, API docs, runbooks, architecture docs, and onboarding docs.
- Maintenance note: useful for coverage checks. Keep this skill narrower: structure, facts of record, agent context, and maintenance rules.

### `supercent-io/skills-template@api-documentation`

- Installs: 11.7K
- Link: https://skills.sh/supercent-io/skills-template/api-documentation
- Install command: `npx skills add supercent-io/skills-template@api-documentation`
- Useful reference: API documentation patterns, especially OpenAPI/Swagger-oriented workflows.
- Maintenance note: verify quality before borrowing. API docs should remain contract-first in this skill.

### `github/awesome-copilot@create-oo-component-documentation`

- Installs: 7K
- Link: https://skills.sh/github/awesome-copilot/create-oo-component-documentation
- Install command: `npx skills add github/awesome-copilot@create-oo-component-documentation`
- Useful reference: component-level documentation creation patterns.
- Maintenance note: relevant only if adding deeper C4 L3/L4 or component documentation guidance.

### `github/awesome-copilot@update-oo-component-documentation`

- Installs: 7K
- Link: https://skills.sh/github/awesome-copilot/update-oo-component-documentation
- Install command: `npx skills add github/awesome-copilot@update-oo-component-documentation`
- Useful reference: maintaining component documentation after code changes.
- Maintenance note: useful as a comparison point for change-impact workflows.

### Lower-install ADR/documentation candidates

These appeared in search results but should be treated cautiously unless manually reviewed:

- `dralgorhythm/claude-agentic-framework@writing-adrs` - 31 installs
- `jellydn/my-ai-tools@adr` - 28 installs
- `datadrivenconstruction/ddc_skills_for_ai_agents_in_construction@claims-documentation` - 21 installs
- `datadrivenconstruction/ddc_skills_for_ai_agents_in_construction@as-built-documentation` - 19 installs
- `nguyenhuuca/assessment@writing-adrs` - 11 installs

## Maintenance Guidance

- Keep `SKILL.md` concise and operational. It should tell an agent what to do, not preserve ecosystem research.
- Keep concrete project prompts out of the skill unless they are short starter examples.
- Prefer project-owned reusable prompts under a project directory such as `docs/ai/prompts/`, `docs/ai/tasks/`, `.github/prompts/`, or the team's automation config.
- Keep Diataxis as an intent layer, not as the top-level folder structure.
- Keep C4 L1/L2 stable and hand-maintained; use L3/L4 only where complexity justifies the upkeep.
- Re-run the discovery commands before making major recommendations, because install counts and available skills can change.
