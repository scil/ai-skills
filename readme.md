# ai-skills

Shared, project-agnostic skills, linked into each repository through directory junctions.

## Skills by group

The groups exist only in this index. `skills/` stays flat, for two reasons. Each project links one junction per skill to `skills/<name>`, and the `link-shared-skills.ps1` scripts build that path. Claude Code documents only `.claude/skills/<name>/SKILL.md`, one level deep. A new skill gets a row in one group here.

The model never loads a skill on its own. You call it by name. Claude Code reads `disable-model-invocation: true` in `SKILL.md`. Codex reads `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

| Group | Skills |
|---|---|
| Agent setup | `ai-harness`, `ai-skill-audit`, `project-docs`, `harvest-exp`, `espanso-prompts` |
| Build | `tiered-research`, `explain`, `code-plan-review`, `codex-review`, `fix-bugs`, `derive-project-plan`, `gather-code-references`, `warm-product-design` |
| App | `anki-cards`, `logseq-ops`, `obsidian-vault-ops`, `android-study-phone`, `arduino-uno-r4-ota`, `playwright-real-phone`, `windows-c-drive-cleanup`, `create-scoop-manifest` |

## The two docs skills

Each owns one object. When a task touches both, each skill does its own part and hands off the rest.

| Skill | Owns | Answers |
|---|---|---|
| `project-docs` | the documents agents read in a project: the instruction file (`AGENTS.md`, `CLAUDE.md`), the loading system across harnesses, and every other durable fact (plans, specs, architecture, generated docs) | Which rule earns a line in the instruction file? What does each harness load, and where does it cut? Where does this fact live, and what check keeps it current? |
| `ai-skill-audit` | the content of one skill's `SKILL.md` | What goes in the description, the body, the references? Is a project-local copy drifting from the shared skill? |

A **harness** is the program that runs the model (Claude Code, Codex CLI). The **roster** is every skill a harness scans. Their descriptions share one budget.

Typical hand-off: too many skills, descriptions shortened. `project-docs` (loading-system path) trims the roster, and `ai-skill-audit` trims each skill.

Both are slash-command only (`disable-model-invocation: true`). `project-docs` re-checks its two sources registries every 30 days, and `ai-skill-audit` every 7 days. `project-docs` was three skills until 2026-11-20 (`ai-agents-md`, `ai-docs-organizing`, `docs-maintainer`).
