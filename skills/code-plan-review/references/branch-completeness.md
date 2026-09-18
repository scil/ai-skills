# Batch: branch completeness — Rule 23

The first batch of the **logic error** family: defects visible from the code and its types alone, with no spec needed to see them. The family's label invites the wrong inference — "lint covers it, review can skip it". Half of this batch is lint-able (whether every state has a branch); the other half is not, and is why the batch exists as a review step: **where the residue lands and what that branch does** — shows something, offers a write, performs a write, decides access. That is a code-level fact, not a business one, and only a reader can weigh it.

## Rule 23 — A branch covers every state, and the residue lands somewhere safe

A value has N distinguishable states; the branch names K < N of them; the rest fall silently into whichever branch is last. The harm is not the missing branch but what the landing branch does. The 2026-09-18 lesson: a first-run route read `porch.getMine`, whose `data` is `undefined` (not known — pending *or failed*), `null` (the server said none) or an object. The guard was `if (isPending || porch) return <Loading/>` and then fell through — so a failed read, `undefined` with `isPending` false, took the branch written for `null`, and on that route that branch is the **creation form**. Nothing was wrong on the home route it was copied from, which had a retry branch; the copy dropped it, and the fallthrough was the one branch that invites a write.

### Stack

Any language. The TypeScript spellings (`never` exhaustiveness, `strict-boolean-expressions`) translate to any typed language's closed unions and nullability; in untyped code the ledger is built from the schema or the producer's contract instead of the type. Never skipped.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A conditional — `if`/`else if`, a ternary, a `switch`, `??`, `||`, `&&`-render — over a value whose type or producer admits three or more distinguishable states: a value that can be both `null` and `undefined` with different meanings; a status union or enum; a number where `0` is meaningful; a query result with pending, error, empty and data.
- A boolean derived from such a value (`hasX = !!x`, `isEmpty = !data?.length`, `ok = res.status < 400`) and then branched on.
- The last branch, or the fallthrough after the guards, offers a write (renders a form, enables a button), performs one (calls a mutation, redirects), or decides access.
- A `switch` or `if` chain over a union or enum that the change extends with a member.
- A branch structure copied from a sibling screen or handler.

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **A branch ledger per conditional the Where names.** The states, enumerated from the type, the enum or the producer's contract in the named file — not from the plan's prose; for each state, the branch it takes and, in one phrase, what that branch does; the **residue** — states no branch names explicitly — and its landing branch; and the landing branch's **effect class**: *shows* (read-only), *offers a write* (a form, an enabled button), *performs a write or navigation*, *decides access*. A residue whose landing branch is anything but *shows* is visible as such; a ledger with fewer states than the type has members is visible as such.
- **For a copied branch structure**: the sibling's ledger beside this one, with the rows that differ.

### Tell

- Truthiness (`if (x)`, `x ? a : b`, `x && <UI/>`) on a value whose type includes `null`, `undefined`, `0` or `""` with distinct meanings.
- `=== null` with no sibling `=== undefined` or `isError` on a value that can be both; `data ?? []`, `?? ""`, `?? 0` where "absent" and "empty" mean different things.
- A `switch` with no `default`, or a `default` that returns a normal case rather than throwing or `assertNever`.
- An `if`/`else if` chain that ends in an unguarded `else` or a fallthrough whose effect class is *offers*, *performs* or *decides*.
- A boolean named `has*`/`is*` computed from a three-state value before the branch.
- The plan's description of the branch names fewer cases than the type has members; a ledger row missing for a state the type admits.
- A branch structure copied from a sibling where one of the sibling's branches did not come along.

### Write

- **Branch on the discriminant, not on a projection of it**: the union tag, `status`, `isError` — never `data === null` when `data` can also be `undefined`, never `!!x` when `x` has three states.
- **Name the residue.** Where the type is closed, `default: assertNever(x)` so an added member fails to compile; where it is open at runtime, an explicit "unknown" branch that says so.
- **The fallthrough is the safest branch.** Order the guards so error and unknown are handled *before* any branch that offers, performs or decides; what the residue reaches must be read-only or disabled — never a form, a mutation, a redirect or a grant. (What the error branch shows is Rule 15's; this rule owns that it comes first.)
- **Extend the type, extend every switch**: `assertNever` at each closed `switch` is what makes the compiler find them.
- **Turn the mechanical half into lint where the stack allows**: `@typescript-eslint/switch-exhaustiveness-check` (with `considerDefaultExhaustiveForUnions: false`), `@typescript-eslint/strict-boolean-expressions`, `no-fallthrough`. The review then reads only what lint cannot — the effect class of the landing branch.

### Prove

- **One test per row of the ledger, the residue included**: feed each state, assert the branch it reaches. The residue's test is the one that goes red when the guard order changes or the explicit branch is removed — for a creation form, assert the form's field is **absent** (`toHaveCount(0)`), not merely that the safe surface is present, because "present" stays green when both render.
- **Compile-time**: `assertNever` / `satisfies never` on every closed `switch`, so adding a member breaks the build before any test runs.
- **For a copied structure**: the sibling's tests run against the copy.

### View

- **Does the ledger match the type?** Open the `.d.ts`, the enum, the schema or the query hook's result type; a state the type admits that the ledger lacks is a finding against the ledger, before any finding against the design.
- **For every conditional in the diff over a three-state value: which state is not named, and where does it land?**
- **What does the landing branch do?** If it offers or performs a write, or decides access, the guard order is the finding — not the missing branch.
- **Is any `has*`/`is*` boolean hiding a third state?** Trace it to its source and count.
- **Was this branch structure copied?** Grep for the sibling; diff the two ledgers.
