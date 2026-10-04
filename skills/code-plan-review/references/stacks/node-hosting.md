# Binding: server hosting (Node and serverless)

How the catalog's questions show up in where and how the server process runs. Load this file for any plan with a server; read the deployment config (a `Dockerfile`, a platform config such as `vercel.json` / `wrangler.toml` / `fly.toml`, the start script) to know which shape applies. The question is the catalog's; this file only says what it looks like here.

Each entry: **shows up as** · **look for** · **fix**.

## B. The server handles a write

**B3.1 / B3.2 — waiters hold connections.**
- *Shows up as:* a pool of `max` connections per process × the number of processes or warm function instances, against the database's connection limit (PostgreSQL's `max_connections` defaults to 100). Every request waiting on a lock holds one; serverless instances each open their own pool.
- *Fix:* state the arithmetic (pool size × instances ≤ the limit, minus admin headroom); a transaction-mode pooler (PgBouncer, a platform pooler) in front of the database for serverless; a lock or statement timeout so a waiter gives its connection back.

**B4.3 — a response that leaves early.**
- *Shows up as:* a streamed response (SSR streaming, `res.write`) begun before the step that sets a cookie or header; headers go with the first byte.
- *Fix:* set cookies and headers before the stream starts, or keep the early return off the paths that set them.

## J. Time passes

**J1.2 — who runs the deadline.**
- *Long-running process (a container, a VM):* an in-process interval or job library can run sweeps, but it dies with the process (a deploy, a crash) and runs once per replica — two replicas run every job twice unless one holds a lock (e.g. a database advisory lock) or a single scheduler owns it.
- *Serverless that scales to zero:* no in-process timer survives between requests. Use the platform's scheduler (a cron trigger, a scheduled function) or a queue with delayed delivery, and say what happens when it is late or down.
- *Fix:* name the runner, how many copies run, and what the reader sees between the deadline and the run (compute at read time where the gap matters).

**J1.3 — the process clock and zone.**
- *Shows up as:* `new Date()` formatted or truncated to a day in the server's local zone (whatever `TZ` the host has, often UTC), compared with a day the user picked in theirs.
- *Fix:* store instants; decide day boundaries in a named zone (the account's or the venue's), in one place.

## Process lifecycle

**B2.3, B4.1 — a request cut off mid-way.** A deploy sends `SIGTERM`; a process that exits at once abandons in-flight requests after their first write. Drain: stop accepting, finish in-flight requests within a deadline, then close the pool. Work that must happen after the response (mail, webhooks) goes to a queue, not a floating promise.
