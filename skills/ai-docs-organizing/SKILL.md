---
name: scil:ai-docs-organizing
description: Organize the documents AI agents consume — instruction files (AGENTS.md / CLAUDE.md), skills, hooks, and per-agent memory — so that every agent working in a repository actually receives the contract, within its harness's budget, with each fact in one owner. Use when auditing or reorganizing a project's AI docs, when a second agent or harness joins a repo (Claude Code beside Codex or the reverse), when an instruction file has grown past ~25 KB, when an agent keeps missing a rule that is "written down", when a pointer-reached doc that the contract or several skills send every task of a kind to (a plan, a domain model, a locator) has grown past ~40 KB, or before adding a skill or an AGENTS.md section. Covers measuring what each harness loads and where it silently stops, the byte budget and its guard, always-loaded versus pointer-reached versus hot pointer-reached material, what belongs in memory versus the repo, the diet procedure for the contract and for a hot doc, tracing each problem to the rule, tool or habit that produced it so source and symptom are fixed together, and reviewing the plan with the other agent before editing. Owns only the docs a harness loads; where any other project fact belongs is docs-maintainer's (or the project's local docs skill's) question.
---

# Organizing the documents agents read

A **harness** is the program that runs a model (Claude Code, Codex CLI). Each harness decides what it loads into the model's context on its own, what it truncates, and what stores it can see — and none of them tells you when it drops something. The lesson this skill was born from: a 66 KB `AGENTS.md` maintained "for both agents" for months had been arriving at Codex cut mid-sentence at 32 KiB (its default `project_doc_max_bytes`), with the discipline, guards, testing rules and skill routing never received, while Claude Code — which loads `CLAUDE.md`, not `AGENTS.md` — received none of it automatically. Both agents worked the whole time and nothing looked wrong. See [`readme.md`](readme.md).

## The loading model comes first

Before judging any document, establish two things per harness and write them down with the method used ([`references/harness-loading.md`](references/harness-loading.md)):

1. **What it auto-loads, and where it silently stops** — instruction file names, import syntax, nested-file rules, byte caps, skills directories, slash commands, hooks.
2. **Which stores each agent can see** — one agent's memory is invisible to the other; the repository is the only store they share.

Never assume either from documentation alone. **Probe**: ask the agent, with file reads forbidden, to quote the last lines of the instructions it received and to name the last heading. A probe costs one minute and settles what a week of "but it's in AGENTS.md" cannot.

## Principles

1. **The loading layer sets the budget.** Always-loaded material (an instruction file, a skill description, a memory index) is paid by every model on every turn whether or not it fires; pointer-reached material costs only its pointer. For some harnesses the budget is a hard byte cap, not a soft attention cost. Push anything not every task needs behind a pointer. **A pointer is cheap only until something routes every task of a kind through it**: a plan that four skills name as "the domain model" is a *hot* doc, paid whole on each read — a Read tool reads the file, not the section — so it gets its own diet (below).
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
   **For every problem the inventory surfaces, trace its source before disposing of it** (next section): the block you are about to delete was put there by a rule, a tool, or a habit that is still running.
6. **Execute in order**: the byte-budget guard first, so it goes red on the old contract; specs for rules that lived only in the contract, written from *shipped behaviour and its tests*, never from the prose (the prose is the stale party); the contract rewrite under budget; skills; hooks; memory triage; the user-level preference file.
7. **Prove**: guard green, probe again (the last heading is the file's last heading, no mid-sentence cut), the project's full gate, and a rule-by-rule checklist showing every original rule's new home.

## Source and symptom — fix both

A stale sentence, a duplicated fact, a section that keeps regrowing: each is a **symptom**, and something produced it — a rule that says "put X here", a tool that generates it, a hook that nudges toward it, a memory that enshrined it, or an event nobody propagated (an app deleted, an environment retired). Deleting the symptom alone means meeting it again in a month; fixing the source alone leaves every instance it already produced. Do both, in the same change ([`references/process.md`](references/process.md) §7):

1. **Name the producer.** For a section: `git log -S'<its heading or key phrase>' -- <file>` finds the commit that introduced it; read that commit's message and diff for the rule that came with it. For a duplicated fact: `git grep` the phrase across the contract, the docs skill, memories, hook scripts and `.gitignore` comments — every copy is a place the rule propagated to.
2. **Fix the source where it was first written** — delete or invert the meta-rule, change the generator's input, retire the memory — and fix every copy in the same change, or the rule re-propagates from the copy you missed.
3. **Fix the symptom too**: the existing instances the source already produced.
4. **Add a guard where one can exist** (a byte budget, a path-exists check, a test that reads the file): a corrected rule regrows without one.
5. **Record the trace** (commit, rule, every copy touched) in the change, so the next reader can tell a decision from a leftover.

Worked example in [`readme.md`](readme.md): a skills section in the contract, traced to the meta-rule in the contract's first commit and to an ownership row it had spawned in the docs skill; both deleted, the section removed, the rule recorded here.

## Skills, hooks, memory

- **The contract lists no skills.** Every harness discovers a skill by scanning the skills directory and reading its `description`; a skill is registered by existing. A "Project Skills" section in the instruction file is a second copy of every description, paid on every turn, and a meta-rule like "routing stays here; skills must not reference each other" is what forces it to grow — delete it, and do not replace it with "skills are not listed here": a self-referential sentence is another always-loaded line, and the rule belongs in the project's docs-ownership skill (and here). A description carries its trigger and nothing else: an order of work ("settle behaviour before implementing") is a rule about the work and lives in the contract once, not in three descriptions that every turn pays for. Shared-skill membership belongs in the ignore manifest the link script reads, not in prose.
- **Skills come in four provenance classes**, each with its own policy: *project-owned routers* (a router of 500–900 words, worked examples in `references/`); *shared through directory junctions* (gitignored; an explicit, optional bootstrap script with a configurable source — never an install step; the contract marks them machine-local); *vendored* (never edited selectively — a compiled duplicate is part of the upstream interface; one sanctioned project-owned `OVERLAY.md` inside the folder, outside the upstream hash, pointed at from inside the budget); *generated by a tool* (regenerate, never hand-edit, and never keep a second copy as a slash command for one harness).
- **A Stop-hook nudge needs a SessionStart baseline**, or a stray edit already in the tree silences it forever; count only owner paths as "docs touched".
- **Memory triage, four bins**: already owned in the repo → delete or pointer; a project fact the repo lacks → write it into its owner, then delete; a preference about that agent's own behaviour → keep; stale → delete. Regenerate the index from what survives.
- **User-level preferences live in one file** — where the harness without an import syntax reads natively — imported by the other harness's file, and sized as part of the shared budget (≤ 4 KiB when the cap is 32 KiB).

## Hot pointer docs — the diet in a different form

Find them in the inventory's layer D: any doc that the contract or two or more skills name as *the* place to read for a kind of question. Its cost is bytes × reads, and the reads are whole-file. Then ([`references/process.md`](references/process.md) §10):

1. **Measure per section in bytes**, not lines — a padded Markdown table is half whitespace; the two heaviest sections usually carry the fat.
2. **Hand the shipped behaviour to its owner.** A section describing what already ships, with a spec or test elsewhere, is a copy that only drifts. It shrinks to the concept, the *reasoning* that produced it (the why is the plan's real value and has no other owner), and the owner's name. Target state that ships nowhere stays whole.
3. **History out.** Changelog comments, "revised by" narratives, old review notes → an archive file beside it; git holds the same story.
4. **A question-first map at the top**: section → the question it answers → the owner of its shipped behaviour. That, plus a one-line reading rule ("read the map, then the section, then the spec it names"), is what turns whole-file reads into range reads — and **put the reading rule in the skill that routes there**; a reader who was told "read the plan" reads the plan.
5. **Split last, by purpose, not by section**: only a section still heavy after the diet and read for a different reason than the rest moves to a sibling file with a two-line stub. Sixteen one-section files lose the narrative that made the doc worth reading and break every `§n` pointer.
6. **Prune the pointers that named it** the same way as any move: a sentence that stands without the pointer drops it (a stale pointer misleads; it never saved a token).

Instance: a 71 KB domain plan four skills routed to, ≈18k tokens per read; changelog out, table padding out, shipped blocks to their 49 specs, map in → 53 KB, and the routing skill told to range-read.

## Slimming a skill, and folding a fork back

A skill body is loaded on trigger, not every turn, so its budget is attention, not bytes: the reason to slim is that steps buried under reference get skipped. The ladder is the same as the contract's ([`references/process.md`](references/process.md) §9):

- **Commit the pending state first** when the file carries someone else's uncommitted edits — theirs as their commit, the rewrite as its own — so the diff of the slim is the slim.
- **Router = principles that change behaviour + paths that end on a done-criterion + the split rule + a references list.** Large blocks (a structure tree, a diagramming rule set, a cross-cutting checklist) move **verbatim** into one-level-deep references — nothing rewritten in transit, so nothing is lost and the move is reviewable.
- **A word count is a guideline, not the goal.** Stop when every remaining sentence changes what the agent does; cutting a rule to hit a number is the failure. Report the number you landed on, not the one you aimed at.
- **Check every pointer after the split** — a moved section breaks the links that named it — and put the old-section → new-home map in the commit message when the change has no design doc.
- **A human-language mirror lags after a restructure**: mark it in its header with *how* it lags; retranslating is its own task, never a side effect.
- **A project-local fork of a shared skill drifts.** Fold the generic value back into the shared skill (its Adopting path, its templates), move the project-specific owners into a project doc the agents read (an ownership map), delete the fork, and link the shared skill in; the harness lists it the moment the junction exists.

## Anti-patterns

Raising the byte limit instead of dieting (restores text, not attention). A brake written in prose. A spec written from the contract's prose instead of the tests. Two copies of a generated skill. Junction creation wired into `prepare`. A code-locator entry that has grown into an essay — the invariant stays, the rationale goes to the spec it cites. A plan whose numbers nobody re-counted. Calling a doc "free" because it is pointer-reached, while every domain task reads all of it. Splitting a hot doc by section before dieting it.

