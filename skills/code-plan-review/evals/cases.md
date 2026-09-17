# Validation cases

Each case names its inputs, the batch or step it exercises, the exact lines the output must contain, and the wrong output it exists to catch. Half the cases are correct code that must come back clean: a review that only ever meets known bugs never learns that it over-prescribes. Run a case by dispatching the named prompt from `SKILL.md` verbatim with the fixture below saved as the plan or diff; the spec deltas are the `#### Scenario:` blocks inside each fixture. A case passes when every "must" line appears and no "must not" line does.

Cases 1–3 and 6 exercise a batch; 4 exercises the merge; 5 exercises the diff pass without a plan; 7 and 8 exercise the confirmation round; 9 and 10 exercise the Stack gate.

## 1. A known bug is found (true positive)

**Inputs.** The card-access-requests design of 2026-08-28 in the ThanksPorch repository, with the reviewable-plan sections added and the lock order removed — the acceptance run recorded in `readme.md`. Batch: `db-concurrency.md`. Prompt: plan.

**Must.** `APPLIES: yes`; `VERDICT: FINDINGS`; one blocking row naming Rule 2, anchored to the `decide` and `ask` paths, whose mitigation states one lock order and whose proof names the two-connection lock-order test.

**Must not.** A row for the same fact under Rule 11 or 13; a second Rule 2 row with an instance mitigation ("add a lock at step N") beside the first (Principle 7).

## 2. A correct alternative implementation comes back clean — two endpoints, server decides on both

**Inputs.** Plan fixture, batch `auth-trust-boundary.md`, prompt: plan.

```
Participants: Client, Server, DB.
Trust boundary:
  1. Client sends POST /api/claim or POST /api/attribute — its choice, from its session store, as a hint.
  2. Server, on either route, decides identity from the request cookie (readSession(req.cookies)).
  3. /api/attribute with no valid cookie → 303 to /api/claim's outcome, computed server-side; the client's hint is overruled.
  4. /api/claim with a valid cookie → the attributed outcome, computed server-side; the client's hint is overruled.
Endpoint count: two; who chooses: the client hints, the server decides (rows 3, 4).
Before-answer state: the Claim button is inert until the "me" query has succeeded; unresolved is not guest.
#### Scenario: a signed-in reader who reaches the guest route is attributed
```

**Must.** `APPLIES: yes`; `VERDICT: CLEAN`.

**Must not.** A row citing Rule 4's Tell "two endpoints chosen by the client", or a mitigation that reads "one endpoint". The property holds on both routes; the Tell is for two endpoints where the guest one trusts that it was chosen by a guest.

## 3. A correct alternative implementation comes back clean — an exact cap with a bounded queue

**Inputs.** Plan fixture, batch `interleaving-liveness.md`, prompt: plan.

```
Spec: "a card holds at most 3 seats; a fourth seating is refused, never admitted and swept" — exact.
Pseudocode:
  1. BEGIN; SET LOCAL lock_timeout = '200ms';
  2. UPDATE cards SET seats = seats + 1 WHERE id = $1 AND seats < 3;   -- rows affected decides
  3. if 0 rows: COMMIT; return { refused: "full" }
  4. INSERT INTO seats (card_id, user_id) VALUES ($1, $2);
  5. COMMIT.
Lock × arrival table:
  | lock | paths | public? | arrival (busiest public) | service (lock→commit) | ceiling | on ceiling |
  | cards row (step 2) | seat (authenticated author only) | no | n/a — no public path | steps 2–5, ~4 ms | lock_timeout 200 ms | caller sees "busy, retry" once, then "try later" |
  | cards row FOR KEY SHARE (step 4, FK) | seat | no | n/a | same tx | same | same |
Retry policy: one retry after 100 ms jitter on lock_timeout; then report.
Exact-vs-eventual: exact, because the spec refuses the fourth seat; the row is reached only by authors, arrival ≤ 1/s per card by the product's own flow.
#### Scenario: the fourth seating on a full card is refused
```

**Must.** `APPLIES: yes`; `VERDICT: CLEAN`.

**Must not.** A row whose mitigation is "sweep the excess later" or "make the cap eventual" — that is a spec change, and the spec says exact. A row that calls step 2 "a conditional write that does not wait" as if it were not in the table.

## 4. A finding with incomplete evidence is not dropped (merge step)

**Inputs.** Plan pass merge, step 5, fed this batch output for `ui-state-ownership.md` (fabricated; the plan behind it does refill an editable field from the response):

```
APPLIES: yes — a save response is written back into an editable field
VERDICT: FINDINGS
SEARCHED: src/screens/settings.tsx
| ? | 16 | the response clobbers what was typed during the round trip | nothing fails; the write is the success path | guard the refill by a baseline token captured at send | ? | blocking |
```

**Must.** The merge returns the row to the batch once, naming both empty cells. If the re-run still returns `?` in either cell, the row appears under `## Unresolved` with the cell it lacks, and the review reports Done as not reached. If the re-run fills them, the row is merged as an ordinary blocking row.

**Must not.** The row absent from the review artifact; the row under `## Accepted` without a written reason; the author's context filling the anchor or the proof itself; a review marked done while the row sits under Unresolved.

## 5. A diff with no plan is reviewable

**Inputs.** Diff fixture, every batch, prompt: diff with `<plan path>` = NONE and `<review path>` = NONE. The diff adds one function:

```diff
+export async function consumeToken(tx: Tx, id: string): Promise<boolean> {
+  const r = await tx.query(
+    `UPDATE tokens SET status = 'consumed', consumed_at = now()
+       WHERE id = $1 AND status = 'open' AND expires_at > now()`, [id]);
+  return r.rowCount === 1;
+}
```
plus a test that opens a transaction on connection A, runs `consumeToken` up to its write, runs it on connection B, asserts B waits, commits A, asserts B returned `false`.

**Must.** Every batch returns an `APPLIES` line; `db-concurrency.md` returns `APPLIES: yes` and `VERDICT: CLEAN`; no batch returns `INCOMPLETE`; no row has effect `plan differs from code`; the db-concurrency `SEARCHED` lines list the diff's file and the test.

**Must not.** `VERDICT: INCOMPLETE` or a `MISSING` line anywhere — the code exists, the batch builds the intermediate; a row asking for a plan.

## 6. A caller the plan omitted is found

**Inputs.** Plan fixture, batch `auth-trust-boundary.md`, prompt: plan. The tree contains `src/cards/recipient.ts` exporting `inferRecipient(grantId)`, called from `src/routes/answer.ts` (the route the plan names) and from `src/routes/admit.ts` (which the plan does not name).

```
Files: src/cards/recipient.ts, src/routes/answer.ts.
Pseudocode (answer route):
  1. grant = the one open grant on this share   -- warrant: answer runs only after exactly one grant was issued
  2. recipient = inferRecipient(grant.id)         -- write-once
  3. INSERT INTO cards (recipient_id) VALUES (recipient)
Route × warrant table:
  | route | constraint | checked at |
  | answer | exactly one open grant | src/routes/answer.ts:41 |
#### Scenario: a card names the reader who answered
```

**Must.** A `SEARCHED` line showing a grep for `inferRecipient` that hits `src/routes/admit.ts`; a blocking row naming Rule 5, anchored to step 2, whose "why it would be silent" names the admit route as a caller with no warrant row; the View side's first question answered first ("the table omits a caller grep finds").

**Must not.** `VERDICT: CLEAN`; a `SEARCHED` list containing only the two files the plan named — that is the old prompt's behaviour and the reason this case exists.

## 7. A scenario satisfied by unchanged code is not `MISSING` (confirmation round)

**Inputs.** Confirmation prompt. The spec delta carries `#### Scenario: a non-owner's id returns the same answer as an unknown id`. The diff changes only `src/routes/cards.ts` to call `visibleCard(callerId, cardId)`; the helper `visibleCard` in `src/access/visibility.ts`, unchanged, already returns `null` for both cases, and `src/routes/cards.ts` maps `null` to 404.

**Must.** `SATISFIED: <scenario> — src/access/visibility.ts:<line> via src/routes/cards.ts:<line>`; a `SEARCHED` line for `src/access/visibility.ts`.

**Must not.** `MISSING` — the round concluded from the diff's changed lines alone; `UNVERIFIED` when the helper's file was readable.

## 8. Missing, unimplementable and unverifiable are told apart (confirmation round)

**Inputs.** Confirmation prompt, three scenarios in the deltas over one diff:

- `#### Scenario: a declined requester sees the same screen as a waiting one` — the diff has no test and no code path for the declined case, and the existing files the diff touches have none either.
- `#### Scenario: a declined requester is told they were declined` — beside the first scenario in the same spec.
- `#### Scenario: the reminder email is sent within one minute` — the mailer lives in a file the round cannot read (a path outside the checkout, or a permission refused).

**Must.** `MISSING: <first scenario> — …` with the existing files read named on `SEARCHED`; `UNIMPLEMENTABLE: <second scenario> — cannot hold with "<first scenario>": one screen cannot be identical for both outcomes and tell one of them apart`; `UNVERIFIED: <third scenario> — <the mailer's path>`. At merge, the `UNVERIFIED` line sits under Unresolved and Done is not reached.

**Must not.** The first scenario as `UNIMPLEMENTABLE` (nothing contradicts it — it is unimplemented); the second as `MISSING`; the third as `MISSING` because its file was absent from the diff.

## 9. A rule bound to another stack is skipped, a rule that holds translated is not

**Inputs.** Plan fixture, batch `db-concurrency.md`, prompt: plan. The tree's `package.json` depends on `@aws-sdk/lib-dynamodb`; `src/db/tokens.ts` calls `UpdateCommand` with a `ConditionExpression`.

```
Stack: DynamoDB via @aws-sdk/lib-dynamodb; no SQL; Fastify; React with TanStack Query.
Pseudocode (consume):
  1. UpdateItem tokens[id] SET status = 'consumed'
       ConditionExpression: status = 'open' AND expires_at > :now      -- ConditionalCheckFailedException is the zero-rows signal
  2. on ConditionalCheckFailedException → return { consumed: false }
Path × table: consume W tokens; expire-sweep W tokens; no lock order — DynamoDB takes none.
Isolation: none stated; conditional write only.
Test: two clients race step 1; exactly one succeeds.
#### Scenario: a token is consumed at most once
```

**Must.** No `SKIPPED` line for Rule 2 (its Stack gate holds for a store with an atomic conditional write, condition-in-the-write half); `SKIPPED: 12 — bound to PostgreSQL REPEATABLE READ (server half); plan uses DynamoDB, src/db/tokens.ts` or equivalent for the server half of Rule 12; `APPLIES: yes`; `VERDICT: CLEAN`; the `SEARCHED` lines include `package.json` or `src/db/tokens.ts` as the file that confirmed the stack.

**Must not.** A Rule 2 row asking for `FOR UPDATE`, a lock order or an isolation level — those are the PostgreSQL bindings, not the mechanism; `SKIPPED` for Rule 2; `APPLIES: no — stack` for the batch.

## 10. A stack line the files contradict is a finding, not a skip

**Inputs.** Plan fixture, batch `db-concurrency.md`, prompt: plan. The plan's stack line says `MongoDB`; the named file `src/db/seats.ts` imports `pg` and runs `SELECT … FOR UPDATE`; `drizzle/schema.ts` is `pgTable`.

**Must.** No `SKIPPED` line taken on the plan's word; the `SEARCHED` lines show `src/db/seats.ts` or `drizzle/schema.ts`; one `OUT-OF-BATCH` line or the merge's own note that the stack line is wrong (the plan says MongoDB, the files are PostgreSQL); Rule 2 judged as on PostgreSQL.

**Must not.** `SKIPPED: 2 — … plan uses MongoDB` — the gate is checked in the files, and the line is not the files.
