---
name: harvest-exp
disable-model-invocation: true
description: Harvest the reusable lessons of a session — failed and working paths, review findings, tool and environment behaviour — and route each into the one place that owns it, after the user approves a candidate list. Use when asked to harvest, keep or write down what a session taught.
---

# Harvest a session's lessons

Hand-offs: a plan-review question or binding → [code-plan-review](../code-plan-review/SKILL.md); a skill's content → [ai-skill-audit](../ai-skill-audit/SKILL.md); where a repository fact lives, and an instruction file's wording → [project-docs](../project-docs/SKILL.md); flashcards of new concepts → [anki-cards](../anki-cards/SKILL.md). Origin: [`readme.md`](readme.md).

## Principles

1. **One lesson, one home**, an owner that already exists; never a parallel doc tree. A lesson with a general shape and a project instance puts the shape in the general home and the instance in the project, linked, not copied.
2. **Keep only what changes future behaviour.** Drop a one-off bug fixed with no pattern, what the repository's docs, code or git history already hold, and detail that matters only to this conversation.
3. **Evidence over recollection.** After compaction, early detail survives only as a summary: take error text, commands and versions from terminal output, `git log`/`git diff` or the files; what cannot be re-checked is marked *speculation*.
4. Everything written to a file is English. No secrets; commands carry placeholders.

## Path

1. Read the repository's `AGENTS.md` / `CLAUDE.md` for its owner docs and its skill directory.
2. Scan the whole session, not only the final problem; skip a kind with nothing in it:
   - **failed attempts**: what was tried, why it looked right, what happened (error text verbatim), the real cause, the signal that should steer away from it next time, the premise under which it still works;
   - **the path that worked**: the key idea, preconditions, commands, the verification command and its expected output;
   - **review findings**: the defect class, and which question asked of the plan would have raised it;
   - **by-catch**: how a tool, shell, encoding, line ending, path, port, process or log behaved; what an error message turned out to mean.
3. Write each candidate as **Rule** (one imperative sentence) · **Trigger** ("when doing X, first check Y", so it is recalled at the right moment) · **Evidence** (one line from this session) · **Scope** (general / this project / this machine, naming the tool and version it depends on). Strip project names unless the fact belongs to the project.
4. Route each candidate by [Destinations](#destinations). Look for an existing entry there; an update beats a new entry.
5. Show the candidate table — rule | scope | destination file | new or update | evidence — and write nothing until the user approves.
6. Write the approved rows, following the destination's own skill. Run `git diff --stat` in each repository touched and look for whole-file rewrites.
7. Done when every approved row is written and the final list states what was written, what was updated, and what was skipped with the reason.

## Destinations

| The lesson is | Goes to | Follow |
|---|---|---|
| a defect shape a plan review could have caught (most review findings) | code-plan-review: a question under its scenario, or a binding in `references/stacks/` | its *Harvest a lesson*; never a new skill for an incident |
| a repeatable multi-step procedure | a skill: extend an existing one first; else the repository's skill directory; the shared skills directory only when it is project-agnostic | ai-skill-audit; propose a new skill's name and description before creating it |
| any other fact about this repository: rules, commands, how to start and verify, environment traps, architecture, decisions, troubleshooting | its owner per the ownership map; a local fact a reader would misread away from the code → a code comment | project-docs (docs-system path); wording inside `AGENTS.md` / `CLAUDE.md` per its instruction-file path |
| a fact about a tool on this machine, unrelated to any project | the Obsidian-AI vault named in the user's global instructions | the vault's English, agent-facing format: facts, commands, limits |
| a cross-project working preference that fits in two sentences | the user's global instruction file | project-docs (instruction-file path); it sits near its 4 KiB cap, so propose only a compression or a replacement, with the resulting byte count; anything longer becomes a skill |
| a collaboration preference or in-flight fact of this project only | the agent's own memory (Claude: the project memory directory and its `MEMORY.md` index) | memory loads only in this project, so never a cross-project lesson |
