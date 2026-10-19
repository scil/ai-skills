---
name: ai-docs-organizing
disable-model-invocation: true
description: Organize the docs AI agents load — AGENTS.md / CLAUDE.md, skills, hooks, per-agent memory — so every harness receives the contract within its budget, each fact in one owner. Use when auditing or reorganizing a project's AI docs, when a second harness joins a repo (Claude Code beside Codex or the reverse), when an instruction file passes ~25 KB or a hot pointer-reached doc (a plan, a domain model, a locator) passes ~40 KB, when an agent keeps missing a rule that is "written down", or before adding an AGENTS.md section.
---

# Organizing the documents agents read

Hand-offs: the content of one instruction file, including how a guard is phrased and why prose is not the brake → ai-agents-md; one skill's `SKILL.md` → ai-skills-manager; where any other project fact lives → docs-maintainer or the project's own docs skill.

A **harness** is the program that runs a model (Claude Code, Codex CLI). Each decides on its own what it loads, what it truncates and which stores it can see — and none tells you when it drops something. Origin: [`readme.md`](readme.md). `§n` points into [`references/process.md`](references/process.md).

## The loading model comes first

Before judging any document, establish per harness, and write down with the method used ([`references/harness-loading.md`](references/harness-loading.md)): **what it auto-loads and where it silently stops** (file names, imports, nested files, byte caps, skills directories, hooks), and **which stores it can see** — one agent's memory is invisible to the other.

Never take either from documentation alone. **Probe**: ask the agent, with file reads forbidden, to quote the last lines of the instructions it received and name the last heading. One minute settles what a week of "but it's in AGENTS.md" cannot.

## Principles

1. **The loading layer sets the budget.** Always-loaded material (an instruction file, a skill description, a memory index) is paid on every turn, for some harnesses against a hard byte cap; pointer-reached material costs only its pointer — until the pointer turns *hot* (below).
2. **The repository is the only memory all agents share.** Agent memory holds how the user wants *that* agent to behave and *that* harness's quirks; project facts go to the repo.
3. **One meaning, one owner.** Route each fact to its existing owner (the project's ownership map; docs-maintainer for the generic system). Three copies are three edits and one drift.
4. **Respect the information hierarchy.** Steps performed, reference consulted, reference disclosed by pointer: three tiers. Recipes, retired-environment history and environment inventories leave the contract; rules stay as invariant + `Instance:` + the test or spec that enforces them — so does a code-locator entry grown into an essay.
5. **The environment is the source of truth; docs are a cache.** A script list or "app X exists" copies what `ls` or `package.json` answers, and goes stale. Cache only what cannot be looked up: the unwritten convention, the reason, the gotcha.

## Process

1. **Inventory by loading layer**, not by folder (§1).
2. **Measure** the bytes of every instruction chain an agent can start in (root, nested files on the path, the user-level global file); probe each harness; count skills and check for a roster-budget warning.
3. **Verify every claim against the tree** and tag its provenance: `[repo]`, `[user-config]`, `[external-local]`, `[runtime]` (with the probe), `[session]` (dated). Name each dispute between documentation, probes and sources, with the evidence on each side and the finding its weight supports.
4. **Review the plan with the other agent before editing** — read-only, as a design and as claims (§8, `codex-review`); it knows its own loading model. Verify each finding; reject with evidence.
5. **Decide a disposition per block** (§2): stay compressed · move to an existing owner · delete because the environment is the truth · delete as stale. Amend the ownership map deliberately; never invent an owner to legalize a move. Trace every problem to its source first (next section).
6. **Execute in order**: the byte-budget guard, red on the old contract (§3; raising the harness's limit restores text, not attention); specs for contract-only rules, written from shipped behaviour and tests, never the prose (§4); the contract; skills; hooks; memory; the user-level file.
7. **Prove**: guard green; probe again (the file's last heading arrives, no mid-sentence cut); the full gate; a rule-by-rule checklist giving every original rule its new home.

## Source and symptom — fix both

A stale sentence, a duplicated fact, a regrowing section is a **symptom** of a producer still running: a rule, a generator, a hook's nudge, a memory, or an event nobody propagated. In one change: **name the producer** (`git log -S`, `git grep` every store); **fix it where first written and in every copy**, or it re-propagates; **fix the existing instances**; **add a guard** where one can exist; **record the trace** — *commit · rule · copies touched · guard*. Commands and known sources: §7; worked example: [`readme.md`](readme.md).

## Skills, hooks, memory

- **The contract lists no skills.** A skill is registered by existing; a "Project Skills" section is a second copy of every description. Delete it with the meta-rule that forced it, and write no "skills are not listed here" line — that rule belongs in the docs-ownership skill. Shared-skill membership lives in the ignore manifest the link script reads.
- **Four provenance classes, four policies** (§1); **the roster is a budget** — Codex shortens *every* description once it overflows (§11).
- **A Stop-hook nudge needs a SessionStart baseline**, or a stray edit silences it forever; count only owner paths (§5).
- **Memory triage, four bins** (§6); regenerate the index from what survives.
- **User-level preferences live in one file**, where the harness without imports reads natively, imported by the other and sized within the shared budget.

## Hot pointer docs

A doc that the contract or two or more skills name as *the* place for a kind of question costs bytes × reads, and every read is whole-file. Diet before splitting (§10): measure sections in bytes; hand shipped behaviour to its spec, keeping concept, reasoning and owner (unshipped target state stays whole); history to an archive; a question-first map on top, and the reading rule — map, section, owner — in the skill that routes there; split last, by purpose; prune the pointers that named it. Instance: [`readme.md`](readme.md) item 9.
