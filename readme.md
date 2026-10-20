# ai-skills

Shared, project-agnostic skills, linked into each repository through directory junctions.

## The four docs skills

Each owns one object. When a task touches two, each skill does its own part and hands off the rest.

| Skill | Owns | Answers |
|---|---|---|
| `ai-agents-md` | the content of one instruction file (`AGENTS.md`, `CLAUDE.md`) | Which rule earns a line, how it is worded, what enforces it? |
| `ai-skill-audit` | the content of one skill's `SKILL.md` | What goes in the description, the body, the references? Is a project-local copy drifting from the shared skill? |
| `ai-docs-organizing` | the loading system across all of them | What does each harness actually load, where does it silently cut, does the skill roster fit its budget? |
| `docs-maintainer` | every other project fact (plans, specs, architecture, generated docs) | Where does this fact live, and what check keeps it current? |

A **harness** is the program that runs the model (Claude Code, Codex CLI). The **roster** is every skill a harness scans; their descriptions share one budget.

Typical hand-offs:

- Instruction file too large: `ai-docs-organizing` measures and plans the diet; `ai-agents-md` decides which lines stay.
- Too many skills, descriptions shortened: `ai-docs-organizing` trims the roster; `ai-skill-audit` trims each skill.
- A fact with no home: `docs-maintainer` places it; if the place is `AGENTS.md`, the wording is `ai-agents-md`'s.

All four are slash-command only (`disable-model-invocation: true`). `ai-agents-md` and `ai-skill-audit` re-check their vendor sources every 7 days, `docs-maintainer` every 30; `ai-docs-organizing` dates its harness facts instead.
