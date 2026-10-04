# Validation cases

Each case names a plan fixture, what the report must contain, and the wrong output it exists to catch. Two of the six are correct plans whose questions must come back *unlikely*: a review that only ever meets known bugs never learns that it over-prescribes. Run a case by invoking the skill with the fixture as the plan, in a session that did not write it; a case passes when every "must" holds and no "must not" does.

## 1. A known bug is raised (B2.1)

**Plan.** Two request paths, `decide` and `ask`, each with numbered pseudocode that updates `access_requests` and inserts into `edges`; no lock order stated anywhere.

**Must.** A row for B2.1 marked *likely*, anchored to the two paths, whose suggestion names one lock order written beside the tables. Rows for B2.3 or B1 questions, if raised, stay separate rows with their own anchors.

**Must not.** The same fact filed under B3 (arrival rate) or G2.3 (a model problem); two suggestions of the form "add a lock at step N", one per path (I2.2 says one class fix).

## 2. A correct alternative comes back unlikely (C1)

**Plan.**

```
1. Client sends POST /api/claim or POST /api/attribute — its choice, from its session store, as a hint.
2. Server, on either route, decides identity from the request cookie (readSession(req.cookies)).
3. /api/attribute with no valid cookie → 303 to /api/claim's outcome, computed server-side; the hint is overruled.
4. /api/claim with a valid cookie → the attributed outcome, computed server-side; the hint is overruled.
5. The Claim button is inert until the "me" query has succeeded; unresolved is not guest.
```

**Must.** `Unlikely: C1.1 (rows 2–4), C1.2 (row 5), C1.3 (cookie decides)` under the C table, or a C table with no rows and that line.

**Must not.** C1.1 as *likely* or *possible* with "one endpoint" as the suggestion: the property holds on both routes.

## 3. Material is asked for once; the review continues when declined

**Plan.** "The seat procedure updates `cards` then `seats`; the release procedure updates `seats` then `cards`. Both run inside one transaction. Helpers `touchCard` and `touchSeat` do the writes." No diagram, no list of other writers of either table; the files are not in the checkout. When asked, the user declines.

**Must.** Exactly one message asking for material, listing the other writers of the two tables (for B2.1 and B2.3) and the handle each helper takes (for B2.2), together with anything else the review needs. After the decline: B2.1 as *likely* from the two sentences alone (the orders differ as written), B2.2 and B2.3 as *cannot tell* with suggestions still given; Materials lists the items as declined; every other scenario has its table or not-touched line.

**Must not.** A second request; a list of writers built from the plan's prose and presented as if supplied; the review stopped at the decline; a subagent.

## 4. The submit flow (A1, A3)

**Plan.**

```
1. The user edits the intro field.
2. Save sends PATCH /me with the draft.
3. On response, reset the form from the response body.
4. Show a toast and keep the user on the page.
```

**Must.** A1.1 *likely* with "nowhere" as the anchor (nothing disables Save); A3.1 *likely* at step 3; A3.4 *possible* (Save is usable the moment the response lands, before the reset settles); A1.3 *possible* (the draft is sent raw). A2.1, A3.1 and A3.2 share one suggestion naming the token captured at send.

**Must not.** A3.1 marked *unlikely* because Save is disabled while pending: a disabled button stops a second send, not a late response landing on a changed field.

## 5. Scenarios the plan does not touch are listed, not dropped

**Plan.** A server-only change: one `status` enum gains a member, and one handler runs `UPDATE … WHERE id = $1 AND status = 'open'` and reads rows affected. No UI file, no route.

**Must.** Tables or Unlikely lines for B, F (the enum's existing `switch` statements, F1.3) and G2; one *Not touched* line each for at least A, D and E, with the reason; B1.1 and B1.4 under `Unlikely:` with the `WHERE` and the rows-affected read as the guards.

**Must not.** D or E absent from the report; F skipped because the plan is "server-only".

## 6. A binding supplies the fix; the question stays neutral (B1.2 · postgres)

**Plan.** On PostgreSQL: "Before inserting a hold, check `SELECT 1 FROM holds WHERE user_id = $1 AND status = 'active'`; if none, `INSERT INTO holds …`. Expired holds keep `status = 'active'` until a nightly job flips them." The manifest shows `pg`.

**Must.** Materials lists `postgres` as loaded. A row `B1.2 · postgres` *likely*, whose suggestion is a partial unique index on `user_id WHERE status = 'active'` with `ON CONFLICT (user_id) WHERE status = 'active' DO NOTHING RETURNING`. A row for J1.1 (`· postgres` if it cites the immutable-predicate limit) *likely*: until the nightly job runs, an expired hold still blocks the insert.

**Must not.** A suggestion naming a different database's syntax; Postgres syntax quoted as if it were the catalog question's own wording; a new catalog question proposed for "Postgres partial index predicate" (that is a binding entry, not a shape).
