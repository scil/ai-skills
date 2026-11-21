# Validation cases

Each case names a plan fixture, what the report must contain, and the wrong output it exists to catch. Two of the seven are correct plans whose nodes must come back *unlikely*, and a third rightly accepts a residual risk. A review that only meets known bugs never learns that it over-prescribes. Run a case by invoking the skill with the fixture as the plan, in a session that did not write it. A case passes when every "must" holds and no "must not" does.

## 1. A known bug is raised (P1.3)

**Plan.** Two request paths, `decide` and `ask`, each with numbered pseudocode that updates `access_requests` and inserts into `edges`. No lock order is stated anywhere.

**Must.** A row for P1.3 marked *likely*, anchored to the two paths, whose suggestion names one lock order written beside the tables. Rows for P1.1 or P1.2, if raised, stay separate rows with their own anchors.

**Must not.** The same fact filed under P2 (load) or L2.3 (a model problem). Two suggestions of the form "add a lock at step N", one per path: rows with one cause get one class fix.

## 2. A correct alternative comes back unlikely (L1.1)

**Plan.**

```
1. Client sends POST /api/claim or POST /api/attribute — its choice, from its session store, as a hint.
2. Server, on either route, decides identity from the request cookie (readSession(req.cookies)).
3. /api/attribute with no valid cookie → 303 to /api/claim's outcome, computed server-side; the hint is overruled.
4. /api/claim with a valid cookie → the attributed outcome, computed server-side; the hint is overruled.
5. The Claim button is inert until the "me" query has succeeded; unresolved is not guest.
```

**Must.** `Unlikely: L1.1 (rows 2–4, cookie decides)`, under a table with no row for L1.1. S3.1 is not raised for identity (row 5 gates on it). A row for S3.1 about a second send while the claim is in flight is allowed: the plan does not gate on that.

**Must not.** L1.1 as a row of any kind, for example with "one endpoint" or "report the branch taken" as the suggestion: the property holds on both routes, and a node's `Suggest:` is not a requirement.

## 3. Material is asked for once, and the review continues when declined

**Plan.** "The seat procedure updates `cards` then `seats`; the release procedure updates `seats` then `cards`. Both run inside one transaction. Helpers `touchCard` and `touchSeat` do the writes." No diagram, no list of other writers of either table, and the files are not in the checkout. When asked, the user declines.

**Must.** Exactly one message asking for material: the other writers of the two tables (for P1.2 and P1.3) and the handle each helper takes (for P1.3), with anything else the review needs. After the decline: P1.3 *likely* from the two sentences alone (the orders differ as written), and the helper-handle question and P1.2 *cannot tell* with suggestions still given. Materials lists the items as declined. Every loaded gate has a row, an Unlikely entry or a Not reached line.

**Must not.** A second request. A list of writers built from the plan's prose and presented as supplied. The review stopped at the decline. A subagent.

## 4. The submit flow (S1, S3, S5)

**Plan.**

```
1. The user edits the intro field.
2. Save sends PATCH /me with the draft.
3. On response, reset the form from the response body.
4. Show a toast and keep the user on the page.
```

**Must.** S3.1 *unspecified* with "nowhere" as the anchor (nothing says Save is disabled in flight or when it is usable again). S1.1 *likely* at step 3, with one suggestion naming the token captured at send. S5.1 raised as *possible* or *unspecified* (the draft is sent raw).

**Must not.** S1.1 marked *unlikely* because Save is disabled while pending: a disabled button stops a second send, not a late response landing on a changed field.

## 5. Views the plan does not touch are listed, not dropped

**Plan.** A server-only change: one `status` enum gains a member, and one handler runs `UPDATE … WHERE id = $1 AND status = 'open'` and reads rows affected. No UI file, no route.

**Must.** Tables or Unlikely lines for P1, L5 (the enum's existing `switch` statements, L5.1.1) and L2.2. The scenarios view as a Not loaded line with the reason, or loaded with the reason it was. P1.1 under `Unlikely:` with the `WHERE` as the guard. P1.1.1 under `Unlikely:` with the rows-affected read as the guard. A P1.1.1 row is allowed only if it names two meanings of zero rows (for example "already paid" and "on hold").

**Must not.** The scenarios view absent from the report. L5 skipped because the plan is "server-only".

## 6. A binding supplies the fix, and the node stays neutral (P1.1 · postgres)

**Plan.** On PostgreSQL: "Before inserting a hold, check `SELECT 1 FROM holds WHERE user_id = $1 AND status = 'active'`; if none, `INSERT INTO holds …`. Expired holds keep `status = 'active'` until a nightly job flips them." The manifest shows `pg`.

**Must.** Materials lists `postgres` as loaded. A row `P1.1 · postgres` *likely*, whose suggestion is a partial unique index on `user_id WHERE status = 'active'` with `ON CONFLICT (user_id) WHERE status = 'active' DO NOTHING RETURNING`. A row for P3.1 (`· postgres` if it cites the immutable-predicate limit) *likely*: until the nightly job runs, an expired hold still blocks the insert.

**Must not.** A suggestion in another database's syntax. Postgres syntax quoted as if it were the node's own wording. A new node proposed for "Postgres partial index predicate": that is a binding entry, not a shape.

## 7. A proportionate residual is accepted, not padded (L1.4.2)

**Plan.**

```
1. GET /records/:id requires sign-in. Ids are random UUIDs, issued only in links the owner sends.
2. A missing id → 404 "not found", after one indexed read.
3. A record hidden from the caller → the same 404 "not found", byte for byte, after four more indexed reads
   (owner, audience rules, exclusions, share link). No lock is taken and no message or external call is
   made before the refusal.
4. Non-Goals: the hidden path's residual timing (a few reads) is accepted.
```

**Must.** `Unlikely: L1.4.1 (one body and status, step 3), L1.4.2 (ids unguessable and signed-in, gap is a few reads with no wait, named in Non-Goals)`. The model, restated, says what an outsider already holds (an unguessable id, a session). An L1.4.1 row is allowed only for a channel that step 3 does not cover. An example is a fault status that only an existing id can produce.

**Must not.** An L1.4.2 row whose suggestion pads every refusal to a fixed time, adds dummy reads, or uses a constant-time comparison. L1.4.2 marked *possible* because nothing in the plan rules a timing difference out.
