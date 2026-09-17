---
name: ai-skills-manager
disable-model-invocation: true
description: Review, slim or grow one skill's SKILL.md — a description that is only the trigger, a router body with paths ending on done-criteria, large blocks behind references — and fold a drifted project-local fork back into its shared skill. Use when a skill's steps are being skipped or buried under reference, when a description is over-long or restates work rules, when a copy of a shared skill has drifted, when deciding whether a rule belongs in a skill's description, body, references or the instruction file, or when the vendor skill format may have changed (every run first checks a 7-day refresh gate). Not for creating a skill from nothing or running evals, nor for the skills roster and its budget.
---

# One skill's SKILL.md

Hand-offs: the roster (which directories each harness scans, provenance classes, how many skills load under what budget) → ai-docs-organizing; the instruction file's content → ai-agents-md; creating a skill from nothing or measuring it with evals → skill-creator; where any other project fact lives → docs-maintainer.

A **skill** is a directory with a `SKILL.md`: its `description` is loaded into every session by every harness; its body loads only when the skill triggers. The two halves have different budgets and different failure modes. Origin: [`readme.md`](readme.md).

## Principles

1. **The description is the trigger and nothing else.** It is paid on every turn by every harness, and Codex shortens *every* description when the roster exceeds its budget — the skill with the longest trigger list is the one that misses its own case first ([`harness-loading.md`](../ai-docs-organizing/references/harness-loading.md)). An order of work ("settle behaviour before implementing") is a rule about the work and lives in the instruction file once, not in three descriptions; ownership prose shrinks to one **Hand-offs:** line under the body's H1, naming only where the agent sends work this skill does not own — what the skill *covers* is a table of contents and goes.
2. **The body's budget is attention, not bytes.** It loads on trigger, so the reason to slim is that steps buried under reference get skipped. A router is: a two-line purpose; the principles that change behaviour; the split rule; the paths, each a numbered list of steps ending on a *done when …* line. Each reference is linked at the step that uses it; a closing "References" list is a second copy of those links. Large blocks move **verbatim** into one-level-deep `references/`, one topic per file — nothing rewritten in transit, so the move is reviewable. All three vendors say under 500 lines and one level of references ([`sources.md`](references/sources.md)).
3. **The no-op test is model-relative.** Delete a sentence a current model obeys unprompted ("prefer clear headings"); keep one the model gets wrong without it. Vendor guidance for newer models says skills written for older ones are often too prescriptive ([`sources.md`](references/sources.md)). Settle a disagreement by running the skill, not by debate.
4. **A word count is a guideline, not the goal.** Stop when every remaining sentence is a rule, a step or a done-criterion; cutting a rule to hit a number is the failure. Report the number you landed on, not the one you aimed at.
5. **A rule has one home.** A skill body that restates the instruction file's architecture rules, a spec's requirements or conventions readable from the code is a second copy that drifts. The tell is a "recommended shape" section describing what shipped months ago. Point to the owner; keep the two or three facts that have no other owner.
6. **One shared skill, no drifted forks.** A project-local copy of a shared skill diverges within weeks. Generic value goes up into the shared skill; the project's bindings by name go into a project doc its agents read (an ownership map); the fork is deleted; the shared skill is linked in — the harness lists it the moment the link exists.
7. **Every sentence in the body is for the agent doing the task; sentences for the maintainer go to `readme.md`.** Four kinds of filler survive reviews because each looks reasonable alone; each has one disposition ([`filler.md`](references/filler.md)):
   - *Self-description* — scope essays, "this skill encodes…", origin stories, "since <date>", "owned by X since…" → the story to `readme.md`, the date to git, the ownership to the Hand-offs line.
   - *Justification beside a rule that stands alone* — round counts, token figures, incident narrative, a "why this matters" paragraph under a heading that said it → one line each in `readme.md`; the rule keeps at most a parenthetical.
   - *The same content twice in one file* — a closing references list, an anti-pattern table restating the rules above it, a "when this applies" section restating the description, a rule stated at three steps → keep the copy at the step that uses it, delete the rest.
   - *A project, machine or product name in a shared skill* — a repo's commands and paths, "this machine's config", a user's shorthand, a product's vocabulary in an example → stack- or tool-generic mechanics to `references/<stack-or-tool>.md`; project bindings to the project's own instruction file; user shorthand to the user's own file; examples re-told in neutral terms.

## Every run starts with the refresh gate

Read the `last-refresh` line at the top of [`references/sources.md`](references/sources.md). If it is more than 7 days old, run the Refresh path first (short when nothing changed), then continue. Never skip the gate silently; without network, say so and continue with the sources as they stand.

## Paths

### Review (and apply)

1. Refresh gate. Measure: `description` length in characters; body words; bytes of each file under `references/`; every relative link resolves (`Test-Path`). Run the filler detector ([`filler.md`](references/filler.md) → Detector); its hits are candidates, not findings.
2. Walk [`references/review-checklist.md`](references/review-checklist.md) against the description, then the body, then the references.
3. Report one row per finding: location, defect, disposition (trim description → Hand-offs line · move block verbatim to a reference · delete as no-op · delete as second copy, naming the owner · move to `readme.md` as origin or incident · move to `references/<stack-or-tool>.md` · move to the instruction file · keep). Apply only what the user approves.
4. If the approved rows restructure the file, follow [`references/slimming.md`](references/slimming.md) for the mechanics: classify every section, move disclosed blocks verbatim, write the router, record the old-section → new-home map in the commit message, mark human mirrors as lagging, report the landed number.
5. Done when: every approved row is applied and every rejected row is recorded with its reason; every link resolves; and, for a restructure, the map is in the change and the mirror's header says how it lags.

### Grow (from an incident)

1. Refresh gate. State the incident: what the agent did with the skill loaded, what it should have done, how many times.
2. Place the fix by layer: a missed trigger → one phrase in the description; a skipped step → a step in the path, ending on its done-criterion; a rule needed on one path only → that path's reference; a rule about the work in general → the instruction file (ai-agents-md), not this skill.
3. Done when: the rule is in one place, the description is no longer than before unless a trigger was missing, and the body still reads as steps.

### Fold a fork back

1. Diff the fork against the shared skill; classify each divergence as *generic* (belongs upstream), *project binding* (a path, a command, an owner's name) or *stale*.
2. Generic → the shared skill's paths or templates. Bindings → a project doc the agents read, pointed at from the instruction file. Stale → dropped.
3. Delete the fork; link the shared skill in the way the project links shared skills; update every reference to the fork (hook reason text, in-flight tasks) in the same commit; leave archived history alone.
4. Done when: the harness lists the shared skill, no live reference names the fork, and the project doc holds every binding the fork held.

### Refresh (sources)

Procedure in [`references/refresh.md`](references/refresh.md): run the shared checker ([`ai-agents-md/scripts/check-sources.ps1`](../ai-agents-md/scripts/check-sources.ps1)) against this skill's `sources.md`, read only the sources whose fingerprint moved, search for vendor changes to the skill format since the last refresh, write the dated entry in [`references/changelog.md`](references/changelog.md), and *propose* edits for the user to accept. Disputes between sources are named with the tier of each side. Fingerprints and `last-refresh` update only after the user has seen the report.
