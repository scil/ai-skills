---
name: ai-docs-organizing
description: Organize the documents AI agents consume — instruction files (AGENTS.md / CLAUDE.md), skills, hooks, and per-agent memory — so that every agent working in a repository actually receives the contract, within its harness's budget, with each fact in one owner. Use when auditing or reorganizing a project's AI docs, when a second agent or harness joins a repo (Claude Code beside Codex or the reverse), when an instruction file has grown past ~25 KB, when an agent keeps missing a rule that is "written down", or before adding a skill or an AGENTS.md section. Covers measuring what each harness loads and where it silently stops, the byte budget and its guard, always-loaded versus pointer-reached material, what belongs in memory versus the repo, the diet procedure, and reviewing the plan with the other agent before editing.
---

# Organizing the documents agents read

A **harness** is the program that runs a model (Claude Code, Codex CLI). Each harness decides what it loads into the model's context on its own, what it truncates, and what stores it can see — and none of them tells you when it drops something. The lesson this skill was born from: a 66 KB `AGENTS.md` maintained "for both agents" for months had been arriving at Codex cut mid-sentence at 32 KiB (its default `project_doc_max_bytes`), with the discipline, guards, testing rules and skill routing never received, while Claude Code — which loads `CLAUDE.md`, not `AGENTS.md` — received none of it automatically. Both agents worked the whole time and nothing looked wrong. See [`readme.md`](readme.md).

## The loading model comes first

Before judging any document, establish two things per harness and write them down with the method used ([`references/harness-loading.md`](references/harness-loading.md)):

1. **What it auto-loads, and where it silently stops** — instruction file names, import syntax, nested-file rules, byte caps, skills directories, slash commands, hooks.
2. **Which stores each agent can see** — one agent's memory is invisible to the other; the repository is the only store they share.

Never assume either from documentation alone. **Probe**: ask the agent, with file reads forbidden, to quote the last lines of the instructions it received and to name the last heading. A probe costs one minute and settles what a week of "but it's in AGENTS.md" cannot.

## Principles

1. **The loading layer sets the budget.** Always-loaded material (an instruction file, a skill description, a memory index) is paid by every model on every turn whether or not it fires; pointer-reached material costs only its pointer. For some harnesses the budget is a hard byte cap, not a soft attention cost. Push anything not every task needs behind a pointer.
2. **The repository is the only memory all agents share.** A project fact living only in one agent's memory is a fact the other engineer cannot see. Memory is for how the user wants *that* agent to behave, and for tool quirks of *that* harness.
3. **One meaning, one owner.** Route each fact to its existing owner (the project's ownership map; `docs-maintainer` for the generic system). The same meaning in the contract, the code locator and a memory file is three edits and one drift.
4. **Respect the information hierarchy.** Steps the agent performs, reference it consults, and disclosed reference reached by pointer are three tiers. Executable recipes, retired-environment history and inventories of the environment leave the contract; rules stay, compressed to invariant + `Instance:` + the test or spec that enforces them.
5. **Guards are model-relative.** A rule is a no-op for an agent that already behaves that way and load-bearing for one that does not. Write each guard for the agent that failed, tag its incident and date, prune it when neither agent trips on it. Phrase positively — a list of "Do not…" keeps the forbidden behaviour activated.
6. **The environment is the source of truth; docs are a cache.** A list of scripts, a command block, "app X exists" — each is a copy of what `ls` or `package.json` answers, and copies go stale. Cache only what cannot be looked up: the unwritten convention, the reason, the gotcha no config confesses.
7. **Instructions are a behavioural layer, not the brake.** The brake is the harness's sandbox and approval configuration. Put destructive-action policy at the top of the contract, short — and fix the config when the config is the problem.

## Process

1. **Inventory by loading layer**, not by folder: always-loaded contract · skills (descriptions always, bodies on trigger) · harness wiring (hooks, settings) · pointer-reached docs · human mirrors · residue. Template in [`references/process.md`](references/process.md).
2. **Measure.** Bytes of every instruction chain an agent can be started in (root; each nested file on the path to a working directory; the user-level global file counts too). Probe each harness. Count skills and check whether the harness reports its skill budget as exceeded.
3. **Verify every claim against the tree** and tag its provenance: `[repo]`, `[user-config]`, `[external-local]`, `[runtime]` (with the probe), `[session]` (one observation, dated). A plan built on an unverified number sends the wrong block to the wrong owner.
4. **Review the plan with the other agent before editing** — a read-only design review (`codex-review` skill: `codex exec -s read-only`, "review as a design and as claims"). The other harness knows its own loading model; it will catch the one you got wrong. Verify each finding yourself; reject with evidence.
5. **Decide a disposition per block**: stay (compressed) · move to an existing owner · delete because the environment is the truth · delete because stale. Amend the ownership map deliberately if a new owner is needed; never invent one to legalize a move.
6. **Execute in order**: the byte-budget guard first, so it goes red on the old contract; specs for rules that lived only in the contract, written from *shipped behaviour and its tests*, never from the prose (the prose is the stale party); the contract rewrite under budget; skills; hooks; memory triage; the user-level preference file.
7. **Prove**: guard green, probe again (the last heading is the file's last heading, no mid-sentence cut), the project's full gate, and a rule-by-rule checklist showing every original rule's new home.

## Skills, hooks, memory

- **The contract lists no skills.** Every harness discovers a skill by scanning the skills directory and reading its `description`; a skill is registered by existing. A "Project Skills" section in the instruction file is a second copy of every description, paid on every turn, and a meta-rule like "routing stays here; skills must not reference each other" is what forces it to grow — delete it. A description carries its trigger and nothing else: an order of work ("settle behaviour before implementing") is a rule about the work and lives in the contract once, not in three descriptions that every turn pays for. Shared-skill membership belongs in the ignore manifest the link script reads, not in prose.
- **Skills come in four provenance classes**, each with its own policy: *project-owned routers* (a router of 500–900 words, worked examples in `references/`); *shared through directory junctions* (gitignored; an explicit, optional bootstrap script with a configurable source — never an install step; the contract marks them machine-local); *vendored* (never edited selectively — a compiled duplicate is part of the upstream interface; one sanctioned project-owned `OVERLAY.md` inside the folder, outside the upstream hash, pointed at from inside the budget); *generated by a tool* (regenerate, never hand-edit, and never keep a second copy as a slash command for one harness).
- **A Stop-hook nudge needs a SessionStart baseline**, or a stray edit already in the tree silences it forever; count only owner paths as "docs touched".
- **Memory triage, four bins**: already owned in the repo → delete or pointer; a project fact the repo lacks → write it into its owner, then delete; a preference about that agent's own behaviour → keep; stale → delete. Regenerate the index from what survives.
- **User-level preferences live in one file** — where the harness without an import syntax reads natively — imported by the other harness's file, and sized as part of the shared budget (≤ 4 KiB when the cap is 32 KiB).

## Anti-patterns

Raising the byte limit instead of dieting (restores text, not attention). A brake written in prose. A spec written from the contract's prose instead of the tests. Two copies of a generated skill. Junction creation wired into `prepare`. A code-locator entry that has grown into an essay — the invariant stays, the rationale goes to the spec it cites. A plan whose numbers nobody re-counted.
