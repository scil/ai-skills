# Batch: database concurrency — Rule 2

## Rule 2 — The statement that writes must be the statement that decides

Under READ COMMITTED, PostgreSQL's default, every statement sees a fresh snapshot. A check in one statement and a write in the next have a gap between them, even inside one transaction, and another request fits in that gap.

### Tell

- Pseudocode reads a row or a count, tests it in code (`if count < limit`, `if status == open`, `if not exists`), then writes the same row or table in a later statement.
- A cap, quota, budget, "only one", "first wins" or "single use" rule is enforced anywhere but in the write itself.
- An insert whose conflict branch says "the row exists, use it".
- A sequence diagram or two flows in which two participants write the same two tables, with no lock order stated.
- A helper that takes "the database" and is called from inside a caller's transaction.
- A test plan that says "call it twice at once" or `Promise.all`.

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

- **Where is the read between the check and the write?** Any condition on a value read in an earlier statement, followed by a write, is a finding unless the write's `WHERE` re-states the condition.
- **Which order do these two paths lock, and where is it written?** If the answer is "they don't touch the same tables", grep both paths for every table they touch.
- **On conflict, does the handler lock and re-read, or use the row it did not write?**
- **Does any test hold a transaction open on a second connection?** If every concurrency test runs in one process on one connection, the concurrent half is untested.
- **Which handle does each helper take, and does any call site inside a transaction pass the outer one?**
- **Did the count of rows affected get read?** A conditional write whose result is discarded decided nothing.
