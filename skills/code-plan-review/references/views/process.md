# P · Process view

What runs at the same time and over time: server writes, concurrent callers, locks and retries, deadlines, latency, calls with several effects, and checks that conclude something. The 4+1 process view. Ask each gate first. If the plan has no surface for a gate, skip its subtree.

## CWE-664 · Resource lifetime

### P1. Can two requests, jobs or processes act on the same data at the same time?

- **P1.1** One statement reads a condition (a count under a limit, a status, an absent row) and a later statement writes. Another request fits in the gap, even inside one transaction. A uniqueness conflict is read as "it exists, use it". Suggest: put the condition into the write (a conditional update, a unique constraint with an insert that does nothing on conflict). Read the outcome from the rows changed. On a conflict, lock, re-read and decide by the row's state.
  - **P1.1.1** The rows-affected count is never read, or zero rows has two meanings ("refused" and "nothing to do"). Suggest: branch on the count, and give zero rows one meaning. Where it has two, the guard is its own first statement, and both cases are tested.
- **P1.2** The same call can arrive twice at once (a double click, a retry, another tab, a redelivered webhook, an overlapping cron) and nothing makes the second a no-op. Suggest: an idempotency key the caller controls, or the conditional write.
- **P1.3** Two paths write the same tables in different orders or with no stated order, and deadlock under load. Or a helper takes a fresh connection while its caller holds a transaction. Suggest: one lock order, written once beside the tables. The helper's signature names the handle it needs.
- **P1.4** Exclusion between processes rests on something that is not a lock (a lease file read then written, an expiry a slow holder outlives), or not every writer takes the lock. Suggest: an operating-system lock or an atomic create, held for the whole operation, and a list of every writer, including work that outlives cancellation. Better: partition the resource by owner so no exclusion is needed.
- **P1.5** Several reads that must agree run as separate statements and read two moments, or a screen builds one fact from two queries. Suggest: one query or one read-only snapshot, never a lock for a read. Derive one view from the other.
- **P1.6** The concurrency test fires two calls on one connection and never overlaps. Suggest: a second connection holds a transaction open across the other's write. Test at N−1 and at N.

### P2. Does a path that outsiders or many callers reach take a lock, wait, or retry?

- **P2.1** A write lock sits on a row a public path reaches, or waiting has no ceiling. Once arrivals exceed service, each waiter holds a pool connection and unrelated requests fail. Suggest: public paths read without write locks and write through a conditional statement. Set a lock or statement timeout and say what the caller sees. State the cost as arrival against service.
- **P2.2** A retry has no backoff or maximum, or two writers retry on each other's zero-rows signal. Suggest: jittered backoff, a ceiling, and a message after the last attempt. Zero rows is usually an answer, not a reason to retry.
- **P2.3** A cap on a hot row is exact where the spec tolerates eventual, or the reverse. Or a sweep takes the same lock as the interactive path. Suggest: say which the spec needs. Sweep in small conditional batches.

### P3. Does a state change, or must something happen, because time passes (an expiry, a trial end, a hold lapsing, a reminder)?

- **P3.1** The state is derived at read time ("shown as expired once the date passed"), so every decision that reads the stored state never sees the deadline: a unique index, a "still held" check, a quota. Suggest: name who writes the transition (a sweep and its runner, or the next touch at every decision point). List every decision that reads the state and which value it reads.
- **P3.2** Something must happen at the deadline (a mail, a charge, a release) and the plan names no scheduler, or the host scales to zero. Suggest: name the runner and what happens when it is down or late. Or compute the state at read time and say in the spec who sees it first.
- **P3.3** The client and the server each decide one deadline from their own clock or time zone. Suggest: one side computes it, the server, and the response carries the result.

### P4. Does the plan promise or measure a latency?

- **P4.1** One target covers a path whose stages use different mechanisms (a local stage, a cache, a remote call, a device start-up, a per-item handshake), or the stage allowances already sum past it. Suggest: one budget per thing the person perceives, each listing its stages with measured p50 and p95 on the real device. A stage that cannot meet a budget moves off that path. Each path states when it gives up and what the person sees.
- **P4.2** The probe that measures shares the device or channel with what it measures, or its own delay is unknown. Suggest: an independent probe, calibrated first against a known event and placed where the person is.

## CWE-703 · Exceptional conditions

### P5. Does one call have more than one effect (a write and a mail, a record and a grant, a stream and a header)?

- **P5.1** A second step is "best effort", so the caller cannot tell it did not happen. Suggest: the response carries, per step that can fail alone, whether it applied and why.
- **P5.2** The record is written before an effect that can still be refused ("mark redeemed, then grant"). Suggest: the effect first, then the record, in one transaction.
- **P5.3** The response leaves early (a stream) before the step that sets a cookie or header. Suggest: an early return only for callers that do not need that step.
- **P5.4** A baseline of what was last written (a "last applied" value, a cursor) takes the new value even when the target refused or dropped the write. The next run reads the unchanged target as a change made elsewhere. Suggest: the baseline holds only values read back after the write. Tests cover a refused write followed by a second run.

### P6. Does the system turn an observation (a reading, a probe, a check, a scan) into a verdict or an automatic reaction?

- **P6.1** An observation (a word heard differently, a face not seen) is recorded as a judgement about the person or the world, with no evidence independent of the observing stage. Suggest: keep observations and judgements apart. A judgement needs independent evidence. "Unsure" and "unavailable" are outcomes distinct from "wrong".
- **P6.2** An absence, or a missing or substituted subject, is read as a result: silence means "muted", a scan of no files means "clean", a redirect to a login page is measured as the page. Suggest: a positive control through the same probe. Before measuring, assert that the subject exists and is the one requested. A missing subject is a failure, never a zero.
- **P6.3** One observation (a timeout, a 404, an empty page) has several causes but drives one reaction (back off, retry, stop). Suggest: list every cause and the signal that tells them apart. Each cause gets its own outcome, tested on a sample of real responses.
- **P6.4** The check compares against the wrong thing: a reference picked by a matching name and version but from another channel, or a liveness probe answered by a cache or proxy in front of the subject. Suggest: name what answers each check and where each reference came from. Probe a path the layer never serves from storage. Compare only what both channels share.
- **P6.5** A new check reads its subject in the one form its author saw first, so other valid forms show as defects or pass unread. Suggest: run the check on every real instance before acting on it. An unparsed form is its own outcome.
- **P6.6** Does a sensor, a threshold or a device choice decide events?
  - **P6.6.1** A threshold is set on synthetic input or one clean recording, with no measured noise floor of the real sensor in place. Suggest: per threshold, the two real measurements that bracket it and the margin between them.
  - **P6.6.2** A recognizer assumes the framing of its input (upright, centered, large enough), and a person places the device. Suggest: a run-time check of the framing, a fallback when it fails, and a calibration on real captures before promising accuracy.
  - **P6.6.3** The input device is the system default at open time, and the default can change to one that delivers empty frames. Suggest: name the device in configuration and log the one opened. Treat a bounded stretch of empty input as a lost device, distinct from silence.
