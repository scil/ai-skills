# Batch: server state and cache — Rules 3, 9

## Rule 3 — Invalidate is not replace

Invalidating a cached query marks it stale and *starts* a refetch. Until the round trip returns the screen shows the old value; if the refetch fails, it shows the old value forever.

### Tell

- The plan says "mutate, then invalidate" or "refetch after save" and nothing about the mutation's response.
- The screen that triggered the mutation displays the value the mutation changed.
- The server derives other cached entries from the write (a count, a list the row belongs to, a "mine" view, a badge) and the plan does not list them.
- The plan mentions an optimistic update without a rollback.

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

- **For each mutation in the diff: where is the cache write from the response?** "It invalidates" alone is a finding.
- **Which derived entries does the server compute from this write, and are all of them invalidated?**
- **What does the screen show if the refetch never returns?** If the answer is the old value, the write from the response is missing.
- **Is any cache key typed by hand** rather than taken from the query's own key helper?

## Rule 9 — A step that may fail without failing the call reports whether it applied

### Tell

- The plan says "best effort", "non-blocking", "if X fails, continue", or "log and move on" for a step inside a call that otherwise succeeds.
- One call has two effects (save the text, apply the photo; create the row, send the mail) and one of them may fail alone.

### Write

- **The result carries, per degradable step, whether it applied** (`{ applied: false, reason }`), and the caller renders that fact. "The call succeeded" must never be shown as "your change was saved" when part of it was not.
- **Name the degradable steps in the contract**, so a client cannot mistake a partial success for a full one.

### Prove

- **Force the degraded step to fail** and assert the response says so and the UI says so; assert the non-degraded part still applied.

### View

- **Which steps in this call may fail without failing the call, and where in the response does each say so?**
- **Does the client message read the per-step flag, or the call's status?**
