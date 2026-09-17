# Batch: database concurrency — Rule 2

## Rule 2 — The statement that writes must be the statement that decides

Under READ COMMITTED, PostgreSQL's default, every statement sees a fresh snapshot. A check in one statement and a write in the next have a gap between them, even inside one transaction, and another request fits in that gap.

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
- **A path × table matrix.** One row per path that writes, one column per table it touches, each cell `R`, `W` or `RW`, and the order the path takes its locks written beside the row. Two rows sharing two `W` columns with different orders, or no order, is the finding.
- **Handles on the pseudocode.** Each helper call inside a transaction is annotated with the handle it receives — `pool`, `client` or `tx` — and the helper's signature says which it accepts.
- **The isolation level, once**, and the reason if anything beyond a conditional write is planned.
- **The concurrency test's connections.** The test plan says how many connections it opens and which one holds a transaction open across the other's write.

### Tell

- Pseudocode reads a row or a count, tests it in code (`if count < limit`, `if status == open`, `if not exists`), then writes the same row or table in a later statement.
- A cap, quota, budget, "only one", "first wins" or "single use" rule is enforced anywhere but in the write itself.
- An insert whose conflict branch says "the row exists, use it".
- Two rows of the matrix write the same two tables and no lock order is stated, or the orders differ.
- A helper annotated `pool` inside a `tx`; a helper whose signature accepts "the database".
- A test plan that says "call it twice at once" or `Promise.all` with no second connection named.
- A rule the spec states ("never holds two", "a decline closes the allowance", "only one wins") that no write in the plan enforces in its `WHERE`.

### Write

- **Condition in the write, outcome from rows affected.** `UPDATE … SET granted = granted + 1 WHERE id = $1 AND granted < limit`; `UPDATE … WHERE id = $1 AND status = 'open'`. Zero rows affected is the failed check, and it failed atomically. The same holds for `INSERT … WHERE NOT EXISTS` and `DELETE … WHERE status = …`.
- **A uniqueness conflict proves a row exists, never that it is usable.** The row that exists may be expired, consumed, or another caller's. Lock it (`SELECT … FOR UPDATE`), read it again, then decide.
- **Two paths that touch the same two tables take the locks in the same order.** Write the order down once, beside the tables, and say which path holds for which; a path that needs the other order restructures, never improvises.
- **A helper's signature says which handle it needs** — a pool or client, an executor, or a transaction — and no call site casts one into another. A helper that takes the pool while its caller holds a transaction silently escapes that transaction.
- **Say the isolation level once** in the plan; if the design needs `SERIALIZABLE` or an advisory lock, say why the conditional write is not enough.

### Prove

- **A second connection holding a transaction open.** Open a transaction on connection A, run the first path up to its write, leave it open; run the second path on connection B; assert it waits or fails as designed; commit A; assert the final state. Two calls fired from one process usually serialise on one connection and pass without ever overlapping.
- **Test either side of the cap, never at it**: at N−1 the write affects one row; at N it affects zero and the caller reports the failure.
- **The conflict re-read**: seed the existing-but-unusable row (expired, consumed, another owner), run the path, assert it does not use it.
- **The lock-order test**: run path A and path B against each other on two connections and assert both complete; a deadlock surfaces as the driver's deadlock error or a timeout, and the test fails, not hangs.
- **The handle test**: a compile-time or test-time check that fails when a helper declares a wider handle than it uses, or when a call site asserts one handle type into another.

### View

- **Does the matrix match the files?** Open each path the plan names and list every table it writes; a table the file touches and the matrix omits is a finding against the matrix, before any finding against the design.
- **Where is the read between the check and the write?** Any condition on a value read in an earlier statement, followed by a write, is a finding unless the write's `WHERE` re-states the condition.
- **Which order do these two paths lock, and where is it written?** If the answer is "they don't touch the same tables", grep both paths for every table they touch.
- **On conflict, does the handler lock and re-read, or use the row it did not write?**
- **Does any test hold a transaction open on a second connection?** If every concurrency test runs in one process on one connection, the concurrent half is untested.
- **Which handle does each helper take, and does any call site inside a transaction pass the outer one?**
- **Did the count of rows affected get read?** A conditional write whose result is discarded decided nothing.
