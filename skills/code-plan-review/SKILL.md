---
name: code-plan-review
disable-model-invocation: true
description: Review a plan (design doc, diagram, pseudocode) or a diff against the rules harvested from incidents, one batch per mechanism, each batch in a fresh context. Use when a change touches a conditional database write, two paths over the same tables, a cache after a mutation, auth or visibility, a library hook beside a hand-written listener, or UI state seeded from a prop; when reviewing a diff that does any of these; and when harvesting a lesson from an incident — the lesson becomes a rule in a batch here, never a new skill.
---

# Rules harvested from incidents, reviewed in batches

One kind of problem, one rule; one mechanism, one batch file. Each rule opens with two gates — **where** (the situations that make it apply, judged from the spec and the code, whether or not the plan already guards against it) and **asks for** (the structured intermediate the plan must carry so the rule's tells can be checked by inspection: a column on the pseudocode, a table beside the diagram, never a separate document) — and has four sides — **tell** (what it looks like in a plan, before code exists), **write** (how the code is made), **prove** (how the test shows it), **view** (what the reviewer asks; its first question is always whether the intermediate matches the named files). Incidents behind the rules: [`readme.md`](readme.md). In an OpenSpec repository the plan pass is the change's `review` artifact, gated by the CLI: [`references/openspec.md`](references/openspec.md).

## Principles

1. **A batch is graded in a context that did not write the plan.** Each batch runs as its own subagent with exactly two inputs: the plan (or diff) and that batch's file. The author's context dispatches and merges; it never fills in a batch's findings, and it never decides which batches apply.
2. **Every batch runs; each decides its own applicability.** Whether any of its rules' **where** conditions hold is the first thing a batch subagent writes, judged from the plan, the spec deltas and the files the plan names — never from what the plan says about itself, and never from whether the plan already guards against the rule: a well-guarded plan is applicable and clean, not inapplicable. A batch that does not apply costs two lines. Batches are independent, so they run in parallel.
3. **An applicable rule whose intermediate is missing returns the plan, it does not review prose.** The subagent reports `INCOMPLETE` with the missing items; it never builds the table from the plan's sentences, because a table the author fills is what makes absence visible, and a table the reviewer infers hides it again.
4. **A finding anchors to a numbered step, message or transition and names its rule.** Unanchored rows are dropped at merge.
5. **Blocking rows are resolved in the plan before the first edit; advisory rows never block.** Every row is verified by the author against its anchor before it is acted on.

## What a reviewable plan contains

- **Numbered pseudocode at the deciding statements** — the write that carries its condition, each lock taken, the cache write after the mutation, the authorization check and what it reads. Not the whole feature.
- **The diagram the mechanism needs, as fenced text** (Mermaid or PlantUML), never an image: a sequence diagram with activations and error branches wherever two participants write the same tables or a request path forks; a state diagram wherever a lifecycle is introduced or changed; a trust-boundary list ("client sends X; server decides Y from Z") wherever identity or visibility is decided. Cache and UI-state work needs the pseudocode only.
- **Participants named; messages and transitions numbered.**
- **What each applicable rule asks for**, as columns on the pseudocode and tables beside the diagram: the `WHERE` beside each write and a path × table matrix (Rule 2); a mutation × entries table (Rule 3); may-fail-alone marks with their response fields (Rule 9); trust-boundary rows with the deciding side (Rule 4); a route × warrant table (Rule 5); a crossing table (Rule 6); an options ledger (Rule 1); a state ledger and a save ledger (Rules 7, 8). Each batch file's **Asks for** section defines its shape.
- **Assumptions, each with how it was verified.**

A plan that lacks the diagram or pseudocode where a mechanism is plainly in play is returned before dispatch. A plan that lacks a rule's intermediate where that rule's **where** holds is returned by that batch as `INCOMPLETE`.

## Batches

| Batch file | Rules | Catches |
|---|---|---|
| [`references/db-concurrency.md`](references/db-concurrency.md) | 2 | a read between the check and the write; a conflict row used unread; two paths with no lock order; concurrency tests on one connection; helpers taking the wrong handle |
| [`references/server-state-cache.md`](references/server-state-cache.md) | 3, 9 | invalidate treated as replace; derived entries left stale; partial success shown as saved |
| [`references/auth-trust-boundary.md`](references/auth-trust-boundary.md) | 4, 5, 6 | identity decided on the client; an inference without its warrant; a client-supplied id used as permission |
| [`references/library-hooks-listeners.md`](references/library-hooks-listeners.md) | 1 | a hand-written listener or helper beside a library feature that already owns the concern |
| [`references/ui-state-ownership.md`](references/ui-state-ownership.md) | 7, 8 | state seeded from a prop or query; overlapping saves sharing one observer |

## Paths

### Plan pass

1. Check the plan against "What a reviewable plan contains" for the diagram and pseudocode items only. Where a mechanism is plainly in play and one is missing, return the plan with the list of missing items and stop. Do not check the intermediates here: which rules apply is the batches' decision, not the author's.
2. Dispatch one subagent per batch file — all of them, in one step, in fresh contexts (Claude Code: the Agent tool; Codex: `codex exec -s read-only "<prompt>"`) — with the prompt below, the plan's path, the batch file's path and the spec deltas' paths.
3. Assemble the outputs verbatim, one `## <batch>` heading each, into the review artifact (`review.md` beside the plan, or the plan's own Traps section). Keep every `APPLIES` line: a "no" with its reason is the record that the batch was considered.
4. Return for `INCOMPLETE` first: collect every `MISSING` line across batches, add the intermediates to the plan, and re-run only the batches that reported `INCOMPLETE`. Their findings come from the filled tables, so nothing is merged from an `INCOMPLETE` batch.
5. Merge: open each anchor and verify the row; drop rows with no anchor or no rule; resolve every blocking row in the plan; re-run only the batches whose rules the resolution touched. Dedupe the `OUT-OF-BATCH` lines across batches into one list under the review's Accepted section, each with a one-line disposition.
6. Done when every batch has an `APPLIES` line and a verdict other than `INCOMPLETE`, every blocking row is resolved in the plan or accepted with a written reason, no row is unanchored, and every out-of-batch line has a disposition.

### Diff pass

1. Dispatch every batch as in the plan pass, with the diff and the plan as inputs and "the diff" in place of "the plan" in the prompt; the subagent applies the **view** side, anchored to file and line. Here `INCOMPLETE` is not returned: the code exists, so the subagent builds the intermediate from the diff and the view side's first question — does the plan's table match the files — becomes a finding against the plan where they differ.
2. Done when every batch has an `APPLIES` line and a verdict, and every blocking row is fixed in the diff or accepted with a reason.

### Harvest a lesson

1. State the incident: what was written, what should have been, what let it pass on all four sides — and whether a **where** would have caught the situation, and which intermediate would have shown the absence as an empty cell.
2. Find the mechanism's batch. Same kind of problem as an existing rule → one bullet under that rule's gate or side that failed. New kind → a new `## Rule N` in that batch with both gates and four sides. New mechanism → a new batch file and one row in the table above. Never a new skill.
3. Tell the story once in `readme.md`, with the date.
4. Done when the rule is in one batch, the table lists it, and the readme holds the incident.

## Subagent prompt

Send verbatim, with the paths filled in:

```
You review one plan against one batch of rules. Inputs: the plan at <plan path>; the batch at <batch path>; the spec deltas at <spec paths>. Read all of them. Read code only where the plan names a file, and only that file.
First decide whether any rule's Where in this batch holds for this plan, judged from the plan, the spec deltas and the named files — not from what the plan says about itself, and not from whether the plan already guards against the rule. Write that decision as the first line.
If it holds, check that the plan carries what each applying rule's Asks for section names. List each missing item on a MISSING line and set the verdict to INCOMPLETE; do not build the missing table from the plan's prose, and report no rows.
Otherwise, where a Tell matches, write one row anchored to the plan's numbered step, message or transition; fill mitigation from the rule's Write side and proof from its Prove side. Ask the View side's first question — does the intermediate match the named files — before any other.
Report as rows only findings that match a Tell in this batch. A correctness problem outside this batch's rules is one OUT-OF-BATCH line, never a row. Do not rewrite the plan. Do not comment on style, naming or scope.
Output exactly this and nothing else:
APPLIES: yes | no — <one-line reason>
VERDICT: CLEAN | FINDINGS | INCOMPLETE
MISSING: <rule> — <the item from Asks for>   (zero or more lines; INCOMPLETE only)
| anchor | rule | effect | why it would be silent | mitigation | proof | blocking or advisory |
OUT-OF-BATCH: <anchor> — <one sentence>   (zero or more lines)
```
