# Batch: server state and cache — Rules 3, 9, 15

## Rule 3 — Invalidate is not replace

Invalidating a cached query marks it stale and *starts* a refetch. Until the round trip returns the screen shows the old value; if the refetch fails, it shows the old value forever.

### Stack

Bound to TanStack Query (`setQueryData`, `invalidateQueries`, key helpers, `dataUpdatedAt`). Holds for any client cache with keyed entries and invalidation (SWR, Apollo, RTK Query, Pinia Colada, urql) with the calls translated. Skip where the screen has no client cache — data fetched and held in component state — and say so; Rule 7 then owns the value.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A mutation changes a value that some cached query on the client also holds.
- The server computes anything from the row the mutation changes — a count, a list the row belongs to, a "mine" view, a badge, a sort position.
- The screen that fires the mutation stays mounted and shows the changed value.
- An optimistic update is planned.
- A query's result depends on who is reading (a session, a guest id, a locale) and the reader can change under a mounted screen, or the entry is prefetched on the server for one reader and hydrated for another.

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **A mutation × entries table.** One row per mutation; columns: the fields its response returns; the cache entries written from the response, each by its key helper; the derived entries invalidated, each by key prefix; the rollback if the write is optimistic. An empty "written from response" cell on a mutation whose screen shows the value is visible as such.
- **The four screen states named** for each entry the screen shows: no data, refetching with data, fresh, error. "Loading" alone hides the second; an empty state that also covers the fourth is Rule 15's finding.
- **Key helpers, not keys.** Every entry in the table is named by the query's own key helper; a hand-typed key is visible as such.
- **For a reader-dependent entry**: what in the key changes when the reader changes. A key that does not name the reader, or a plan that detects the change by comparing timestamps, is visible as such.

### Tell

- The plan says "mutate, then invalidate" or "refetch after save" and nothing about the mutation's response.
- A table row whose "written from response" cell is empty while the screen displays the value.
- A table row whose "derived entries" cell is empty while the server, in the named file, reads the changed row from another query.
- The plan mentions an optimistic update without a rollback; a table row with "optimistic" and an empty rollback cell.
- A key in the table typed by hand.
- The plan stops a previous reader's copy from painting by comparing `dataUpdatedAt` (server-stamped) against a client-recorded time — two clocks — instead of by changing the key.

### Write

- **Write the cache from the mutation response first, then invalidate.** `setQueryData` (or the library's direct cache write) for every entry the response can fill; invalidation then repairs whatever the response could not.
- **Enumerate the derived entries** — every query the server computes from the row that changed — and invalidate them by their key or key prefix, never by a hand-typed key.
- **An optimistic write carries its rollback**: keep the previous value, restore it on error, invalidate on settle.
- **"No cached data" and "refetching" are different UI states**; the second still shows data.
- **To stop a previous copy painting, change the key — never compare times.** Put the reader, or a generation number that advances when the reader changes, into the key; a different reader is then a different entry with no previous copy to show. Keep generation 0 key-neutral so the first visit still matches what the loader prefetched.
- **Draw the boundary before adding keys**: the rows that belong to this screen come from the response; everything derived from them converges through invalidation. A review that finds one more stale key per round is a boundary not yet drawn.

### Prove

- **Delay the refetch, then fail it.** After the mutation resolves, with the refetch pending, assert the screen shows the new value; fail the refetch, assert the screen still shows the new value and does not revert.
- **Derived entries refresh**: for each entry in the enumerated list, assert it changes after the mutation, at the layer that can observe it.
- **Optimistic rollback**: fail the mutation, assert the previous value returns and the error is shown.
- **The reader-change test**: render for reader A, change the reader to B while mounted; assert A's copy is never painted, not even for one frame — the assertion that goes red when the reader leaves the key.

### View

- **Does the table match the server?** Open the server file the plan names and list every query that reads the row or table the mutation writes; a derived entry the table omits is a finding against the table, before any finding against the design.
- **For each mutation in the diff: where is the cache write from the response?** "It invalidates" alone is a finding.
- **Which derived entries does the server compute from this write, and are all of them invalidated?**
- **What does the screen show if the refetch never returns?** If the answer is the old value, the write from the response is missing.
- **Is any cache key typed by hand** rather than taken from the query's own key helper?
- **What in this key changes when the reader changes?** Nothing, or a timestamp comparison, is a finding.
- **Is this the second stale-key row in this review?** Then the finding is the boundary, not the key (Principle 7).

## Rule 9 — A step that may fail without failing the call reports whether it applied

### Stack

Any. Never skipped.

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

## Rule 15 — A failed read is not an empty answer

Two shapes. A failure painted as success: `fetch` rejects only on network errors, so a `try/catch` around a call that never checks `res.ok` treats a 500 as done. A failure painted as "there is nothing here": with no error branch, `!isPending && data === undefined` renders the empty state, and an author who can no longer manage their own cards is told they have none.

### Stack

The branch-table half is any client and is never skipped. The `res.ok` half is bound to WHATWG `fetch` and any HTTP client that resolves on an error status; skip that half where the client rejects on non-2xx (axios, ky, got by default) — and confirm the default was not turned off.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A query's empty result renders an empty state ("no cards yet", "nobody here").
- A raw `fetch` or HTTP client call whose result is acted on.
- A parent query's failure would remove a child block that has its own data.
- A step is described as "best effort" on the read side: "if it fails, show nothing".

### Asks for

- **A response-branch table per read**: pending; success with data; success and empty; error — and for each, what the screen shows and what the user can do. An error row that shows the empty row's content, or is missing, is visible as such.
- **The `res.ok` line** for every raw fetch, numbered in the pseudocode, and what happens on a non-ok status.

### Tell

- `data ?? []`, `data?.length === 0 → empty`, or `!isPending && !data → empty` with no `isError` branch.
- `try/catch` around `fetch` with no status check; "the call succeeded" measured by the promise resolving.
- A branch table with three rows.
- A parent's error branch that returns early above a child block which could still render.

### Write

- **Give `isError` its own branch, with a way to look again**; the empty state is reserved for a successful read that found nothing.
- **Check `res.ok`**, and retry once only where the endpoint is idempotent.
- **A failure one level up does not make the whole block disappear**: a child with its own data renders, and the failed parent says it failed.
- **A degraded read reports what actually happened** (Rule 9's shape on the read side): "could not check; will ask again", not silence.

### Prove

- **Fail the read twice** — a 500 and a network error — and assert the error state renders, not the empty state; this is the assertion that goes red when the branch is removed.
- **Fail the parent**, assert the child block is still there and the parent says it failed.
- **A non-ok status through the raw fetch path**, assert it is treated as failure.

### View

- **Does the branch table match the component?** Open it; every place the query's result is read is a row with four branches. A read with three is a finding against the table, before any finding against the design.
- **What does this screen show when the read fails?** If the answer is the empty state, the failure is swallowed.
- **Where is `res.ok` checked for this fetch?**
- **Which blocks disappear when this parent fails, and should they?**
