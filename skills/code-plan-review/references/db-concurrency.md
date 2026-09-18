# Batch: database concurrency — Rules 2, 11, 12

Three safety cells of interleaving: the bad thing happens at a moment you can point at, so each is testable. They need different tools — a condition in the write (2), a happens-before (11), one snapshot (12) — and landing in the wrong cell reaches for the wrong one: a condition added to a `WHERE` cannot cure "it happened too early". A bug that survives serialization does not belong here at all (domain-model, Rule 10).

## Rule 2 — The statement that writes must be the statement that decides

Under READ COMMITTED, PostgreSQL's default, every statement sees a fresh snapshot. A check in one statement and a write in the next have a gap between them, even inside one transaction, and another request fits in that gap.

### Stack

Bound to PostgreSQL: the syntax (`FOR UPDATE`, `ON CONFLICT`, rows affected), the READ COMMITTED default and its re-check of a `WHERE` after a blocking writer commits. Holds for any SQL database with row locks and per-statement snapshots (MySQL InnoDB, SQL Server, Oracle, SQLite in WAL with `BEGIN IMMEDIATE`) with the syntax translated, and for any store with an atomic conditional write (DynamoDB condition expressions, MongoDB filtered `findOneAndUpdate`) for the condition-in-the-write half only. Skip where the store has neither a conditional write nor a row lock — and say which store.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- The spec states a cap, quota, budget, "only one", "first wins", "single use", "never holds two", or "a decline closes the allowance".
- Two request paths (two endpoints, an endpoint and a job, a job and a retry of itself) write the same table, or two tables between them.
- A write depends on what another row or a count currently says.
- A helper that touches the database is called from inside a caller's transaction.
- The same call can arrive twice at once: a double-click, a retry, a webhook redelivered, a cron overlapping its last run.

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **The condition beside its write.** Each numbered write states the `WHERE` it carries and what the caller does with the rows-affected count. A condition that sits in an `if` above the write, with no `WHERE` restating it, is visible as such.
- **A path × table matrix.** One row per path that writes, one column per table it touches, each cell `R`, `W` or `RW`, and the order the path takes its locks written beside the row. Two rows sharing two `W` columns with different orders, or no order, is the finding. The matrix is a projection of the update-source table, a living intermediate (SKILL.md, "Project intermediates"): the project's `update-sources.md` holds every writer of every table, so the plan's matrix includes the paths that already write the change's tables — read from the file, not from memory — and the plan carries the delta rows it adds to the file.
- **Handles on the pseudocode.** Each helper call inside a transaction is annotated with the handle it receives — `pool`, `client` or `tx` — and the helper's signature says which it accepts.
- **The isolation level, once**, and the reason if anything beyond a conditional write is planned.
- **The concurrency test's connections.** The test plan says how many connections it opens and which one holds a transaction open across the other's write.

### Tell

- Pseudocode reads a row or a count, tests it in code (`if count < limit`, `if status == open`, `if not exists`), then writes the same row or table in a later statement.
- A cap, quota, budget, "only one", "first wins" or "single use" rule is enforced anywhere but in the write itself.
- An insert whose conflict branch says "the row exists, use it".
- An insert guarded by `WHERE NOT EXISTS`, `if not exists` or a count, with no unique constraint on the columns the guard tests.
- Two rows of the matrix write the same two tables and no lock order is stated, or the orders differ.
- A helper annotated `pool` inside a `tx`; a helper whose signature accepts "the database".
- A test plan that says "call it twice at once" or `Promise.all` with no second connection named.
- A rule the spec states ("never holds two", "a decline closes the allowance", "only one wins") that no write in the plan enforces in its `WHERE`.

### Write

- **Condition in the write, outcome from rows affected.** `UPDATE … SET granted = granted + 1 WHERE id = $1 AND granted < limit`; `UPDATE … WHERE id = $1 AND status = 'open'`; `DELETE … WHERE status = …`. Zero rows affected is the failed check, and it failed atomically — because the statement locks the row it found and, once a blocking writer commits, re-evaluates its `WHERE` on that row's newest version.
- **An insert has no row to lock, so its guard is the unique constraint.** `INSERT … SELECT … WHERE NOT EXISTS (…)` is not the conditional write above: under READ COMMITTED two transactions both see absence and both insert. What decides "only one" for an insert is a unique constraint on the columns the condition tests, with `INSERT … ON CONFLICT DO NOTHING` and rows affected as the outcome — or the conflict handled by the next bullet. A `WHERE NOT EXISTS` with no such constraint is a check in one statement and a write in the next, wearing one statement's clothes.
- **A uniqueness conflict proves a row exists, never that it is usable.** The row that exists may be expired, consumed, or another caller's. Lock it (`SELECT … FOR UPDATE`), read it again, then decide.
- **Two paths that touch the same two tables take the locks in the same order.** Write the order down once, beside the tables, and say which path holds for which; a path that needs the other order restructures, never improvises.
- **A helper's signature says which handle it needs** — a pool or client, an executor, or a transaction — and no call site casts one into another. A helper that takes the pool while its caller holds a transaction silently escapes that transaction.
- **Say the isolation level once** in the plan; if the design needs `SERIALIZABLE` or an advisory lock, say why the conditional write is not enough.

### Prove

- **A second connection holding a transaction open.** Open a transaction on connection A, run the first path up to its write, leave it open; run the second path on connection B; assert it waits or fails as designed; commit A; assert the final state. Two calls fired from one process usually serialise on one connection and pass without ever overlapping.
- **Test either side of the cap, never at it**: at N−1 the write affects one row; at N it affects zero and the caller reports the failure.
- **The double insert**: two connections, each past the absence check and before its insert, both commit; assert one row — the assertion that goes red when the unique constraint is dropped and `WHERE NOT EXISTS` is left to decide.
- **The conflict re-read**: seed the existing-but-unusable row (expired, consumed, another owner), run the path, assert it does not use it.
- **The lock-order test**: run path A and path B against each other on two connections and assert both complete; a deadlock surfaces as the driver's deadlock error or a timeout, and the test fails, not hangs.
- **The handle test**: a compile-time or test-time check that fails when a helper declares a wider handle than it uses, or when a call site asserts one handle type into another.

### View

- **Does the matrix match the files?** Open each path the plan names and list every table it writes; a table the file touches and the matrix omits is a finding against the matrix, before any finding against the design.
- **Where is the read between the check and the write?** Any condition on a value read in an earlier statement, followed by a write, is a finding unless the write's `WHERE` re-states the condition.
- **Which order do these two paths lock, and where is it written?** If the answer is "they don't touch the same tables", grep both paths for every table they touch.
- **For each insert guarded on absence: which unique constraint decides?** "The `WHERE NOT EXISTS`" is a finding.
- **On conflict, does the handler lock and re-read, or use the row it did not write?**
- **Does any test hold a transaction open on a second connection?** If every concurrency test runs in one process on one connection, the concurrent half is untested.
- **Which handle does each helper take, and does any call site inside a transaction pass the outer one?**
- **Did the count of rows affected get read?** A conditional write whose result is discarded decided nothing.
- **Does the bug this row fixes survive serialization?** If the plan's lock or conditional write answers a bug that also fails single-threaded, the row belongs to domain-model, Rule 10: say so on an OUT-OF-BATCH line instead of a row.

## Rule 11 — A dependent read waits for the commit

Only one writer, and the write does happen; what is wrong is the order of two events. A redirect fires before the transaction that justifies it commits, and the next screen reads a snapshot from before the commit: the flow that just said "welcome in" says "you are not in", and a refresh fixes it. A condition in a `WHERE` cannot help — nothing raced, nothing was stolen.

### Stack

Any transactional store and any client that navigates or refetches after a write. Never skipped.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A client navigates, redirects or refetches after a write, and the destination reads what the write produced.
- A write's result is read in a later request, a later job or a later event rather than in the write's own response.
- One transaction performs two effects where one records the other ("mark the claim redeemed" and "create the edge").
- A request is answered before its work is done: a streamed response, a fire-and-forget, a queued job whose result the caller shows.

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **An ordering column on the pseudocode.** For each pair (write → read, redirect or record that depends on it): what establishes the order — the same response carries the result; the navigation awaits the commit; both are in one transaction with the grant before the record. An empty cell is visible as such.
- **On the sequence diagram**, the commit message numbered before every message that depends on it; a dependent message drawn inside the writer's activation is visible as such.

### Tell

- The redirect or refetch message on the diagram precedes the commit message, or the plan says "navigate on success" where success is the request returning, not the commit.
- The plan's recovery for a stale next screen is "the user can refresh".
- Record-then-grant: the row that says what happened is written before the effect that may still be refused.
- A response returned at the start of a stream, before the procedure that sets a cookie or header has run.

### Write

- **Return the result in the same response**: the write's handler hands back what the next screen needs, and the client renders from it rather than reading again.
- **Await the commit before navigating**, and write the cache from the response (Rule 3) so the destination does not fetch a stale snapshot.
- **Grant first, then record**: the effect that can be refused runs before the row that claims it happened, in the same transaction.
- **Where a response must leave early**, the part that needs the procedure's result (a cookie, a header) is scoped to the requests that need it, not switched off for everyone.

### Prove

- **Hold the commit open on connection A**, trigger the dependent read on B; assert it waits or returns the pre-commit state *and the client does not render the post-commit screen* until A commits — the assertion that goes red when the ordering is removed.
- **The record-then-grant test**: make the grant refuse; assert no record claims it happened.

### View

- **Does the ordering column match the handler and the client?** Open both; a navigation, refetch or record whose order the column does not state is a finding against the column, before any finding against the design.
- **What does the destination read, and from which snapshot?** If the answer is "whatever is there when it lands", the order is not established.
- **Which effect is written first, the one that may be refused or the one that records it?**

## Rule 12 — Reads that must agree share one snapshot

Two reads are each correct, but they read two moments, and the state assembled from them never existed: the list says "this card has reached nobody" while the seat card below says "Sam is holding it". Read skew. The fix is not a lock — the procedure writes nothing — it is one query, or one snapshot for both.

### Stack

The server half is bound to PostgreSQL's `REPEATABLE READ` and holds for any SQL database with snapshot isolation (MySQL InnoDB's `REPEATABLE READ`, SQL Server's `SNAPSHOT`) with the name translated; skip the server half where the store has no multi-statement snapshot (a store where the fix is "one query" only, and say so). The client half — two queries assembling one fact — is any client and is never skipped.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A read-only procedure issues two or more statements whose results must agree, over rows another path writes.
- A screen composes two or more queries about one entity (a list and a detail; a summary and its members) and both can describe the same fact.
- The plan raises an isolation level, or the reviewer expects one and the plan says nothing.

### Asks for

- **A reads-that-must-agree list**, per procedure and per screen: the reads, the fact they must agree on, and the mechanism — one statement; `REPEATABLE READ` on the read-only transaction; or on the client, one view derived from the other. An empty mechanism cell is visible as such.
- **The isolation level of every multi-statement read-only transaction**, stated once, with "default" written out where it is the default.

### Tell

- Two statements over rows a concurrent path writes, no isolation stated, and a fact spanning both.
- Two client queries whose union names one holder, one count or one status, with no derivation between them.
- A lock proposed for a procedure that writes nothing.

### Write

- **One query where the fact fits in one**; otherwise `REPEATABLE READ` on the read-only transaction — one fixed snapshot, no lock, nobody blocked — and say in the plan why this procedure is the one that needs it.
- **On the client, derive one view from the other** (the detail from the list's row, or the list's cell from the detail) rather than fetching both and hoping.
- **Never a lock for tidiness**: a lock to make a list consistent blocks real writers for a read.

### Prove

- **Two connections**: between the procedure's first and second statement on A, commit a write that changes the fact on B; assert the procedure's result does not contradict itself — the assertion that goes red when the isolation level is dropped.
- **The client test**: resolve the two queries from different moments; assert the screen shows one fact, not both.

### View

- **Does the list match the procedure?** Open it; every statement in a multi-statement read-only transaction is a row, and a fact two of them share needs a mechanism.
- **Under the default isolation, can a write between statement 1 and 2 make these two rows disagree?**
- **Fixing the server does not fix the screen**: which client queries can still assemble two moments, and which derives from which?
