---
name: ai-skills-manager
disable-model-invocation: true
description: Review, slim or grow one skill's SKILL.md — a description that is only the trigger, a router body with paths ending on done-criteria, large blocks behind references — and fold a drifted project-local fork back into its shared skill. Use when a skill's steps are being skipped or buried under reference, when a description is over-long or restates work rules, when a copy of a shared skill has drifted, when deciding whether a rule belongs in a skill's description, body, references or the instruction file, or when the vendor skill format may have changed (every run first checks a 7-day refresh gate). Not for creating a skill from nothing or running evals, nor for the skills roster and its budget.
---

# One skill's SKILL.md

Hand-offs: the roster (which directories each harness scans, provenance classes, how many skills load under what budget) → ai-docs-organizing; the instruction file's content → ai-agents-md; creating a skill from nothing or measuring it with evals → skill-creator; where any other project fact lives → docs-maintainer.

A **skill** is a directory with a `SKILL.md`: its `description` is loaded into every session by every harness; its body loads only when the skill triggers. The two halves have different budgets and different failure modes. Origin: [`readme.md`](readme.md).

## Principles

1. **The description is the trigger and nothing else.** It is paid on every turn by every harness, and Codex shortens *every* description when the roster exceeds its budget — the skill with the longest trigger list is the one that misses its own case first ([`harness-loading.md`](../ai-docs-organizing/references/harness-loading.md)). An order of work ("settle behaviour before implementing") is a rule about the work and lives in the instruction file once, not in three descriptions; ownership prose ("owns X; Y belongs to Z") goes in a **Scope.** paragraph under the body's H1, where it costs nothing until the skill fires.
2. **The body's budget is attention, not bytes.** It loads on trigger, so the reason to slim is that steps buried under reference get skipped. A router is: a two-line purpose; the principles that change behaviour; the split rule; the paths, each a numbered list of steps ending on a *done when …* line; a references list. Large blocks move **verbatim** into one-level-deep `references/`, one topic per file — nothing rewritten in transit, so the move is reviewable. All three vendors say under 500 lines and one level of references ([`sources.md`](references/sources.md)).
3. **The no-op test is model-relative.** Delete a sentence a current model obeys unprompted ("prefer clear headings"); keep one the model gets wrong without it. Vendor guidance for newer models says skills written for older ones are often too prescriptive ([`sources.md`](references/sources.md)). Settle a disagreement by running the skill, not by debate.
4. **A word count is a guideline, not the goal.** Stop when every remaining sentence is a rule, a step or a done-criterion; cutting a rule to hit a number is the failure. Report the number you landed on, not the one you aimed at.
5. **A rule has one home.** A skill body that restates the instruction file's architecture rules, a spec's requirements or conventions readable from the code is a second copy that drifts. The tell is a "recommended shape" section describing what shipped months ago. Point to the owner; keep the two or three facts that have no other owner.
6. **One shared skill, no drifted forks.** A project-local copy of a shared skill diverges within weeks. Generic value goes up into the shared skill; the project's bindings by name go into a project doc its agents read (an ownership map); the fork is deleted; the shared skill is linked in — the harness lists it the moment the link exists.

## Every run starts with the refresh gate

Read the `last-refresh` line at the top of [`references/sources.md`](references/sources.md). If it is more than 7 days old, run the Refresh path first (short when nothing changed), then continue. Never skip the gate silently; without network, say so and continue with the sources as they stand.

## Paths

### Review

1. Refresh gate. Measure: `description` length in characters; body words; bytes of each file under `references/`; every relative link resolves (`Test-Path`).
2. Walk [`references/review-checklist.md`](references/review-checklist.md) against the description, then the body, then the references.
3. Report one row per finding: location, defect, disposition (trim description → Scope paragraph · move block verbatim to a reference · delete as no-op · delete as second copy, naming the owner · move to the instruction file · keep). Apply only what the user approves.
4. Done when: the checklist passes, or each rejected row is recorded with its reason.

### Slim

Procedure in [`references/slimming.md`](references/slimming.md): land pending edits as their own commit first; classify every section as *step*, *in-file reference* or *disclosed reference*; move disclosed blocks verbatim; write the router; apply the no-op test; check every pointer; record the old-section → new-home map in the commit message; mark human mirrors as lagging; report the landed number.

Done when: every sentence left in `SKILL.md` changes what the agent does, every link resolves, the map is in the change, and the mirror's header says how it lags.

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
