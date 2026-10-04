# Binding: PostgreSQL

How the catalog's questions show up when the plan writes to PostgreSQL, and the concrete fix. Load this file when the project's manifest or schema shows PostgreSQL (a `pg`/`postgres`/`postgres.js` driver, a Drizzle `pgTable`, a Prisma `provider = "postgresql"`, a `*.sql` migration with Postgres syntax). The question is the catalog's; this file only says what it looks like here. A question with no entry has nothing Postgres-specific to add. Defaults below are PostgreSQL 14–17.

Each entry: **shows up as** — the shape in a Postgres plan or diff; **look for** — what to read or search; **fix** — the Postgres way to reach the catalog's suggestion.

## B. The server handles a write

**B1.1 — check, then write.**
- *Shows up as:* a `SELECT count(*)` / `SELECT status` followed by an `UPDATE` or `INSERT`, even inside one transaction. Under the default READ COMMITTED, each statement sees its own snapshot; the gap is real.
- *Look for:* a read whose result decides a later write in the same procedure.
- *Fix:* `UPDATE … SET … WHERE id = $1 AND status = 'open' RETURNING id`; zero rows returned means another writer won. Under READ COMMITTED a concurrent `UPDATE` of the same row waits, then re-evaluates the `WHERE` against the committed version, so the condition decides correctly without a lock.

**B1.2 — insert guarded by "not exists".**
- *Shows up as:* `INSERT … SELECT … WHERE NOT EXISTS (…)` or a count-then-insert. Two READ COMMITTED transactions both see absence; an insert has no row to lock.
- *Fix:* a unique index on the guarded columns and `INSERT … ON CONFLICT (cols) DO NOTHING RETURNING id`; no row returned means it already existed. For a rule over live rows only, a partial unique index (`CREATE UNIQUE INDEX … ON t (user_id) WHERE status IN ('open','held')`), and the conflict target must repeat its predicate: `ON CONFLICT (user_id) WHERE status IN ('open','held') DO NOTHING`.

**B1.3 — a conflict read as "it exists, use it".**
- *Fix:* `SELECT … FOR UPDATE` the existing row and decide by its state; `ON CONFLICT DO UPDATE … RETURNING` returns the row but cannot tell "I inserted" from "I updated" unless you return `xmax = 0 AS inserted`.

**B1.4 — rows affected never read.**
- *Look for:* a driver call whose result is discarded (`await db.update(…)` with no `.returning()` / `rowCount` read).
- *Fix:* `RETURNING` and branch on the array's length, or the driver's `rowCount`.

**B2.1 — two paths, no lock order.**
- *Shows up as:* two transactions touching the same two tables in opposite orders. Postgres detects the cycle after `deadlock_timeout` (1 s default) and aborts one with SQLSTATE `40P01`.
- *Look for:* the first statement that locks each table in each path — including the implicit `FOR KEY SHARE` a foreign-key insert takes on the referenced row.
- *Fix:* one order written beside the tables; take the first lock explicitly with `SELECT … FOR UPDATE` (or `FOR NO KEY UPDATE`, which does not block foreign-key inserts referencing the row) at the top of each path.

**B2.2 — a helper escapes the transaction.**
- *Shows up as:* a helper that issues its query on the pool while the caller holds a transaction. It runs on another connection, does not see the uncommitted writes, and if it touches a row the transaction locked it waits on the caller's own lock until a timeout — Postgres cannot see a cycle that runs through the application.
- *Fix:* the helper's parameter type names the transaction client; no call site passes the pool where a transaction is required.

**B2.4 — a concurrency test that never overlaps.**
- *Fix:* two clients; client A runs `BEGIN; UPDATE …;` and holds; client B issues the competing write and must block or lose; A commits; assert B's outcome. `pg_sleep` inside A's transaction widens the window deterministically.

**B3.1 — a write lock on a public path.**
- *Shows up as:* `SELECT … FOR UPDATE`, `pg_advisory_xact_lock(…)`, or `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE` (whose failures arrive as `40001` and must be retried) on a row an anonymous or high-rate path reaches.
- *Fix:* the public path reads without locking and writes with a conditional `UPDATE` (B1.1).

**B3.2 — no ceiling on waiting.**
- *Shows up as:* nothing set: `lock_timeout` and `statement_timeout` both default to `0`, disabled.
- *Fix:* `SET LOCAL lock_timeout = '2s'` at the top of the transaction on that path (it then fails with `55P03`); say what the caller is shown.

**B3.5 — a sweep fights the interactive path.**
- *Fix:* small batches that skip what is busy: `UPDATE t SET … WHERE id IN (SELECT id FROM t WHERE … ORDER BY touched_at LIMIT 500 FOR UPDATE SKIP LOCKED)`.

**B5.1 — reads that must agree.**
- *Fix:* one statement (CTEs keep it readable), or `BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY` so every statement reads the same snapshot.

## C. Who is asking

**C4.1 — outcomes told apart by "can ask again".**
- *Shows up as:* a partial unique index whose predicate counts one outcome (`WHERE status <> 'declined'`), so a declined asker may insert again and a waiting one may not — the difference is visible.
- *Fix:* the predicate treats the outcomes the spec hides as one.

## G. The domain says what exists

**G1.1 — a rule with no column.**
- *Fix:* the constraint that expresses it: a `CHECK` for a same-row rule; a partial unique index for "at most one live"; an exclusion constraint (`EXCLUDE USING gist (resource_id WITH =, during WITH &&)`, needs `btree_gist`) for "no two overlapping ranges".

**G4.2 — new rows meet old constraints.**
- *Look for:* every constraint on the table: `\d+ table`, or `SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid = 'table'::regclass`. A composite foreign key is `MATCH SIMPLE` by default: a null in any of its columns skips the check entirely.

**G4.3 — new constraints meet old writers (and old rows).**
- *Shows up as:* `ALTER TABLE … ADD CHECK (…)` or `SET NOT NULL` validates every existing row and fails the migration if one violates it; afterwards, every existing writer that omits the new value fails at runtime with `23514` (check) or `23502` (not null).
- *Fix:* list the writers (search the codebase for inserts and updates of the table, tests and seed scripts included); for large tables, `ADD CONSTRAINT … NOT VALID` then `VALIDATE CONSTRAINT` separately.

## J. Time passes

**J1.1 — a derived state the stored state cannot see.**
- *Shows up as:* the wish for a partial index such as `WHERE expires_at > now()`. Index predicates may only use `IMMUTABLE` functions; `now()` is `STABLE`, so Postgres rejects it. A `CHECK` that calls `now()` is accepted but checked only when the row is written, never again as time passes.
- *Fix:* a stored status the transition writes (by a sweep, or at each decision point), and the index predicate on that status.

**J1.3 — two clocks.**
- *Shows up as:* `now()` and `CURRENT_TIMESTAMP` return the transaction's start time, constant for the whole transaction — so two rows inserted in one transaction share it, and ordering by it ties (order by an identity column instead); `clock_timestamp()` is the wall clock. A `date` column has no time zone; "the end of that day" needs a zone (`(day + 1)::timestamp AT TIME ZONE 'Europe/London'`).
- *Fix:* store instants as `timestamptz`; decide deadlines in one place, on the server, in a named zone.
