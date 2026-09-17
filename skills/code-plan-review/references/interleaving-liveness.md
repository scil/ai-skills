# Batch: interleaving liveness — Rules 13, 14

Both rules in this batch are marked **liveness**. A liveness failure is "something good never happens": the request does not fail, it is never served; the page does not error, it never learns. There is no moment at which an assertion turns red, so the Prove side of these rules is not a test — it is the argument the plan carries (arrival against service, subscribe against fire) and the metric that would show the failure in production. A row from this batch whose proof cell names a test is suspect; one whose proof names neither an argument nor a metric is returned to the batch once at merge, then listed under Unresolved. Deadlock is the one liveness failure the database reports (`40P01`) and it lives in db-concurrency, Rule 2; starvation and lost wakeup get no such courtesy.

## Rule 13 — Every pessimistic lock answers for its arrival rate

A write lock on a row that a public path can reach is not "a bit slower": once arrivals exceed the rate the lock can serve, the queue only grows, waiting time diverges, and every waiter holds a pool connection — so requests with nothing to do with that row start failing. The lock does not fail where it is; it makes something else fail. And the correct move in the safety cell — a conditional write whose failure signal is zero rows — comes back here as livelock if the reaction to zero rows is a naive retry.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- The plan takes `SELECT … FOR UPDATE`, an advisory lock, a table lock or `SERIALIZABLE` on a row or table that a path without authorization can reach: a public resolve, a scan, a landing page, an unauthenticated submit, a webhook.
- A plan chooses "exact" over "eventual" for a count or cap on a row many callers touch.
- The plan retries on a zero-rows result, a conflict, a deadlock error or a timeout.
- No `lock_timeout` or `statement_timeout` is stated for a path that waits on a lock.
- A background sweep and an interactive path contend for the same rows.

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **A lock × arrival table.** One row per lock the plan takes (including the foreign-key `FOR KEY SHARE` an insert takes on its parent, which the code does not show): the row or table locked; every path that takes it, marked public or authorized; an arrival estimate for the busiest public path (per second, with the assumption named); the service time from lock to commit; the ceiling on waiting (`lock_timeout` or `statement_timeout`, with the value); and what a waiter's caller sees when the ceiling is hit. An empty arrival cell on a public path, or an empty ceiling cell, is visible as such.
- **A retry policy per retry**, on the pseudocode: the signal retried on, the backoff (fixed or jittered), the maximum attempts, and what the caller is told after the last attempt.
- **For an exact cap on a shared row: the eventual alternative considered**, in one sentence, and why exactness was worth a queue.

### Tell

- A lock × arrival row marked public with a write lock; a plan that locks a share, an event, a listing or a token row on every resolve or view "to count exactly".
- A retry with no backoff, no maximum, or a fixed interval; "retry until it succeeds"; two writers that both retry on each other's zero-rows signal.
- An empty ceiling cell; a plan that says "the request will fail" for a lock wait, when `lock_timeout` defaults to no timeout.
- The plan describes the cost of a lock as latency ("a few ms slower") rather than as a queue.
- A sweep that takes the same write lock as the interactive path it cleans up after.

### Write

- **Public reads take no write lock.** A path anyone can trigger reads without `FOR UPDATE` and writes, if at all, through a conditional statement (Rule 2). That statement still waits for a writer holding the row, and still holds the row lock until its own transaction ends, so it is a row in the lock × arrival table like any other; what makes it cheap is a service time of one statement — which holds only when it is the transaction's last statement or runs in autocommit. A conditional write followed by more work in the same transaction has the service time of that work, measured from the lock to the commit or rollback.
- **A cap on a hot row is as exact as the spec requires, and no more.** Where the spec tolerates eventual — a storage limit, a cleanup threshold, "roughly N" — sweep the excess later, ordered by what was last shown or touched, instead of counting under a lock on every request. Where the spec demands exact, the cap stays exact and the lock × arrival table shows what bounds the queue; relaxing to eventual is a spec change to propose, not a mitigation to apply.
- **A retry has jittered backoff and a ceiling**, and the caller is told what happened after the last attempt; a zero-rows result on a conditional write is an answer to report, not always a reason to try again.
- **Set a ceiling on waiting.** `lock_timeout` on the path, or `statement_timeout`, so a waiter fails on its own instead of holding a pool connection until the pool is empty.
- **Write the queue's cost in the plan** as arrival against service, not as milliseconds.

### Prove (liveness)

- **The argument**: for the busiest public path, arrival per second against one over the service time; if arrival can exceed service, the plan says what bounds the queue. This sentence is the proof; a test cannot stand in for it.
- **The metric**: p99 lock wait on the locked table, pool occupancy, queue length or `pg_stat_activity` waiters — named in the plan as what would show the failure, with the threshold that pages someone.
- **The retry test is a test**: exhaust the attempts with a row that always conflicts; assert the caller is told after the last attempt and the loop ends — this one does turn red.

### View

- **Does the table match the paths?** Open each path the plan names and list every lock it takes, foreign-key locks included; a lock the code takes and the table omits is a finding against the table, before any finding against the design.
- **Which locks can a public path reach, and what is the arrival estimate?** "It's just a read" is a finding when the read takes `FOR UPDATE`.
- **What bounds the queue on this row?** If the answer is "the database", the answer is nothing.
- **Where is the ceiling on waiting, and what does the caller see when it is hit?**
- **What does this retry do on the fifth failure?** Fixed interval, no maximum, or silence is a finding.
- **Could anyone on this path never get a turn?** The question must be asked in the plan, because no test will ask it later.

## Rule 14 — Subscribe, then read once

A push tells a screen that something changed. If the change happens between the screen's first render and the moment its subscription is live, the notification goes out into a window where nobody is listening, and the screen waits forever for an event that has already fired.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A screen waits on a push — a websocket, SSE, a channel, a poll that is started later, a notification permission — to leave a "waiting" or "pending" state.
- The event the screen waits for can be caused by another actor at any time, including before the screen mounts.
- The plan's sequence diagram has a subscribe message and a fire message from different participants.

### Asks for

- **On the sequence diagram**: the subscribe message and the first read after it, numbered; and one row beside the diagram, "if the event fires before message N", saying what the screen does then.
- **The source of truth for the waited-on state named**: the read, with the push as its hint.

### Tell

- The screen's state flips only in the push handler; no read after the subscription is established.
- The "if the event fires before message N" row is empty or says "cannot happen" with no argument.
- The plan reads once on mount and subscribes afterwards, with nothing between them.
- A poll that starts on a timer after the first render, with no immediate first tick.

### Write

- **Subscribe, then read once.** Establish the subscription, then ask "what is my state right now"; the push is a hint that the read should run again, never the only source.
- **Make the handler idempotent** so the read and a late push can both arrive without double effect.
- **Where the withheld-outcome rule applies (Rule 18), the extra read obeys it too**: what it returns for "declined" and "still waiting" is identical.

### Prove (liveness)

- **The argument**: the sequence diagram shows no window between mount and subscribe in which a fire can be missed, or shows the read that covers it.
- **The metric**: screens in the waiting state longer than the expected resolution time, or a count of reads that found the state already resolved on arrival.
- **The convergence test is a test**: fire the event before the screen subscribes (two browser contexts, or resolve the state before navigating to the screen); assert the screen leaves the waiting state within the read's latency — this one does turn red.

### View

- **Does the diagram match the component?** Open the named component; the order of the subscription's setup and the first read in the code is the order on the diagram, or the diagram is wrong.
- **What happens if the event fired a second before this subscription went live?**
- **Where is the read after subscribe?** A screen that leaves "waiting" only from a push handler is a finding.
