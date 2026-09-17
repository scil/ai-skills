# Batch: server state and cache — Rules 3, 9

## Rule 3 — Invalidate is not replace

Invalidating a cached query marks it stale and *starts* a refetch. Until the round trip returns the screen shows the old value; if the refetch fails, it shows the old value forever.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A mutation changes a value that some cached query on the client also holds.
- The server computes anything from the row the mutation changes — a count, a list the row belongs to, a "mine" view, a badge, a sort position.
- The screen that fires the mutation stays mounted and shows the changed value.
- An optimistic update is planned.

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **A mutation × entries table.** One row per mutation; columns: the fields its response returns; the cache entries written from the response, each by its key helper; the derived entries invalidated, each by key prefix; the rollback if the write is optimistic. An empty "written from response" cell on a mutation whose screen shows the value is visible as such.
- **The three screen states named** for each entry the screen shows: no data, refetching with data, fresh. "Loading" alone hides the second.
- **Key helpers, not keys.** Every entry in the table is named by the query's own key helper; a hand-typed key is visible as such.

### Tell

- The plan says "mutate, then invalidate" or "refetch after save" and nothing about the mutation's response.
- A table row whose "written from response" cell is empty while the screen displays the value.
- A table row whose "derived entries" cell is empty while the server, in the named file, reads the changed row from another query.
- The plan mentions an optimistic update without a rollback; a table row with "optimistic" and an empty rollback cell.
- A key in the table typed by hand.

### Write

- **Write the cache from the mutation response first, then invalidate.** `setQueryData` (or the library's direct cache write) for every entry the response can fill; invalidation then repairs whatever the response could not.
- **Enumerate the derived entries** — every query the server computes from the row that changed — and invalidate them by their key or key prefix, never by a hand-typed key.
- **An optimistic write carries its rollback**: keep the previous value, restore it on error, invalidate on settle.
- **"No cached data" and "refetching" are different UI states**; the second still shows data.

### Prove

- **Delay the refetch, then fail it.** After the mutation resolves, with the refetch pending, assert the screen shows the new value; fail the refetch, assert the screen still shows the new value and does not revert.
- **Derived entries refresh**: for each entry in the enumerated list, assert it changes after the mutation, at the layer that can observe it.
- **Optimistic rollback**: fail the mutation, assert the previous value returns and the error is shown.

### View

- **Does the table match the server?** Open the server file the plan names and list every query that reads the row or table the mutation writes; a derived entry the table omits is a finding against the table, before any finding against the design.
- **For each mutation in the diff: where is the cache write from the response?** "It invalidates" alone is a finding.
- **Which derived entries does the server compute from this write, and are all of them invalidated?**
- **What does the screen show if the refetch never returns?** If the answer is the old value, the write from the response is missing.
- **Is any cache key typed by hand** rather than taken from the query's own key helper?

## Rule 9 — A step that may fail without failing the call reports whether it applied

### Where

- One call performs two or more effects: save the text and apply the photo; create the row and send the mail; write the row and publish an event.
- One of the effects goes to something that can fail on its own — object storage, mail, a third-party API, a cache, a queue.
- The spec or the plan says "best effort", "non-blocking", "optional", "if X fails, continue".

### Asks for

- **A may-fail-alone mark on each numbered step**, and for each marked step: the response field that carries whether it applied, and the client message that reads it. A marked step with an empty field cell is visible as such.
- **The degradable steps named in the response contract**, not only in the handler.

### Tell

- The plan says "best effort", "non-blocking", "if X fails, continue", or "log and move on" for a step inside a call that otherwise succeeds.
- One call has two effects and one of them may fail alone.
- A marked step with no response field, or a client message that reads the call's status and not the step's field.

### Write

- **The result carries, per degradable step, whether it applied** (`{ applied: false, reason }`), and the caller renders that fact. "The call succeeded" must never be shown as "your change was saved" when part of it was not.
- **Name the degradable steps in the contract**, so a client cannot mistake a partial success for a full one.

### Prove

- **Force the degraded step to fail** and assert the response says so and the UI says so; assert the non-degraded part still applied.

### View

- **Do the marks match the handler?** Open the named handler; every `try`/`catch` that swallows, `.catch(() => {})`, `allSettled`, or "log and continue" inside a call that still succeeds is a step that must carry the mark.
- **Which steps in this call may fail without failing the call, and where in the response does each say so?**
- **Does the client message read the per-step flag, or the call's status?**
