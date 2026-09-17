---
name: code-plan-review
disable-model-invocation: true
description: Review a plan (design doc, diagram, pseudocode) or a diff against the rules harvested from incidents, one batch per mechanism, each batch in a fresh context. Use when a change touches a conditional database write, two paths over the same tables, a cache after a mutation, auth or visibility, a library hook beside a hand-written listener, or UI state seeded from a prop; when reviewing a diff that does any of these; and when harvesting a lesson from an incident — the lesson becomes a rule in a batch here, never a new skill.
---

# Rules harvested from incidents, reviewed in batches

One kind of problem, one rule; one mechanism, one batch file. Each rule has four sides — **tell** (what it looks like in a plan, before code exists), **write** (how the code is made), **prove** (how the test shows it), **view** (what the reviewer asks). Incidents behind the rules: [`readme.md`](readme.md).

## Principles

1. **A batch is graded in a context that did not write the plan.** Each batch runs as its own subagent with exactly two inputs: the plan (or diff) and that batch's file. The author's context selects, dispatches and merges; it never fills in a batch's findings itself.
2. **Only the batches whose surfaces the plan names run.** A plan describable in one sentence runs none. Batches are independent, so they run in parallel; sequencing buys nothing.
3. **A finding anchors to a numbered step, message or transition and names its rule.** Unanchored rows are dropped at merge; the plan is numbered so rows can anchor.
4. **Blocking rows are resolved in the plan before the first edit; advisory rows never block.** Every row is verified by the author against the anchor before it is acted on.

## Surfaces → batches

The plan's `## Surfaces` line names the surfaces it touches, from this vocabulary. A surface with no batch yet is noted in the review and skipped.

| Surface named in the plan | Batch file | Rules |
|---|---|---|
| `db-write-with-condition`, `two-paths-same-tables`, `migration` | [`references/db-concurrency.md`](references/db-concurrency.md) | 2 |
| `cache-after-mutation` | [`references/server-state-cache.md`](references/server-state-cache.md) | 3, 9 |
| `auth-visibility`, `public-contract` | [`references/auth-trust-boundary.md`](references/auth-trust-boundary.md) | 4, 5, 6 |
| `library-hook-pairing` | [`references/library-hooks-listeners.md`](references/library-hooks-listeners.md) | 1 |
| `ui-state` | [`references/ui-state-ownership.md`](references/ui-state-ownership.md) | 7, 8 |
| `lifecycle-state`, `retry-or-external` | no batch yet | — |

## Paths

### Plan pass

1. Read the plan. If it has no `## Surfaces` line, derive one from its content and write it in. Select batches from the table; if none applies, write `tier 1 — no batch applies` where the review goes and stop.
2. For each selected batch, dispatch one subagent in a fresh context (Claude Code: the Agent tool; Codex: `codex exec -s read-only "<prompt>"`) with the prompt below, the plan's path and the batch file's path. Dispatch all selected batches in one step.
3. Assemble the outputs verbatim, one `## <batch>` heading each, into the review artifact (`review.md` beside the plan, or the plan's own Traps section).
4. Merge: open each anchor and verify the row; drop rows with no anchor or no rule; resolve every blocking row in the plan; re-run only the batches whose surface the resolution touched.
5. Done when every selected batch has a verdict, every blocking row is resolved in the plan or accepted with a written reason, and no row is unanchored.

### Diff pass

1. Select batches from the plan's Surfaces line and from what the diff touches (a mutation, a listener, a state seed, a client-supplied id).
2. Dispatch as in the plan pass, with the diff and the plan as inputs and "the diff" in place of "the plan" in the prompt; the subagent applies the **view** side, anchored to file and line.
3. Done when every selected batch has a verdict and every blocking row is fixed in the diff or accepted with a reason.

### Harvest a lesson

1. State the incident: what was written, what should have been, what let it pass on all four sides.
2. Find the mechanism's batch. Same kind of problem as an existing rule → one bullet under that rule's side that failed. New kind → a new `## Rule N` in that batch with four sides. New mechanism → a new batch file, one row in the table above, and a surface name for it. Never a new skill.
3. Tell the story once in `readme.md`, with the date.
4. Done when the rule is in one batch, the table routes to it, and the readme holds the incident.

## Subagent prompt

Send verbatim, with the two paths filled in:

```
You review one plan against one batch of rules. Inputs: the plan at <plan path>; the batch at <batch path>. Read both. Read code only where the plan names a file, and only that file.
For each rule in the batch, compare its Tell to the plan. Where a Tell matches, write one row anchored to the plan's numbered step, message or transition, and fill mitigation from the rule's Write side and proof from its Prove side.
Report only findings that match a Tell in this batch or would change correctness. Do not rewrite the plan. Do not comment on style, naming or scope.
Output exactly this and nothing else:
VERDICT: CLEAN | FINDINGS
| anchor | rule | effect | why it would be silent | mitigation | proof | blocking or advisory |
```
