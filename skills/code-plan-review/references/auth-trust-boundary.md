# Batch: authorization and trust boundaries — Rules 4, 5, 6, 18

## Rule 4 — The client renders outcomes; the server decides who the caller is

"Is this reader signed in, and as whom" is answered from the request's cookie or token on the server. The client's session store is unresolved on first paint, cached for whoever asked last, and changeable from another tab.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- The same screen or the same request serves a signed-in reader and a guest, or two different users, and does something different for each.
- A client file reads the session — a store, a client-side cookie, a cached "me" query, local storage — for anything other than choosing what to render after a server answer.
- Identity can change under the screen: first paint before the session resolves, a sign-in or sign-out in another tab, a query cached for the previous user.

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **A trust-boundary row per identity-dependent decision**: "client sends X; server decides Y from Z" — with the deciding side and the source (cookie or token, or a client value) filled. A row whose deciding side is the client, or whose source is a session store, is visible as such.
- **A before-answer state per identity-dependent control**: what the control does until the server's answer arrives — inert, hidden, a stated default. A control with no such state is visible as such.
- **The endpoint count**: one endpoint that reports which branch it took, or two; if two, the row says who chooses.

### Tell

- Client code branches on "if signed in" or "as user X" to choose between two behaviours.
- A trust-boundary row whose deciding side is the client, or whose source is a session store, local storage or a cached "me" query.
- A control's enabled state, or a link's target, depends on a session value read on the client; a control with no before-answer state.
- Two endpoints, "the signed-in one" and "the guest one", chosen by the client.

### Write

- **The property: whichever endpoint the request reaches, the server decides who the caller is from the request's credentials**, and a request whose claim disagrees with its cookie gets the cookie's outcome. The plain implementation is **one endpoint that reports what it did**: the server reads the credentials, chooses the branch, and returns which (`{ mode: "attributed" }` / `{ mode: "claim" }`); the client renders the outcome. Two endpoints hold the property only when each decides from the credentials and refuses, redirects or re-routes a caller the credentials do not match — then the client's choice is a hint the server may overrule, and the endpoint-count row says so. Two endpoints where the guest one trusts that it was chosen by a guest do not.
- **Where the client must know first**, it asks on its own query key, trusts only a succeeded answer, and keeps the control inert until then. An unresolved answer is not "guest".
- **Never carry the identity decision in a request body** the client could set.

### Prove

- **Three client states, one server answer**: unresolved on first paint; cached for a different user; changed in another tab. Each must produce the server's answer for the actual request, and the control must be inert until the answer arrives.
- **A request with the client's claim and a different cookie**: the cookie wins.

### View

- **Do the rows match the client files?** Open the named client files; every read of a session store, local storage or "me" query that feeds a branch rather than a render must have a row. A read with no row is a finding against the list, before any finding against the design.
- **For each branch on identity in client code: who decided, and from what?** A client-side decision is a finding unless it only chooses what to render after a server answer.
- **What does the control do before the identity answer arrives?**

## Rule 5 — An inference is valid only on the routes that carry its warrant

A value inferred "because only X can reach here" is correct on the route that guarantees X and wrong on every other route that reaches the same code. A comment stating the warrant is not a check.

### Where

- A value is derived from a precondition instead of read: "the caller must be the author here", "there is exactly one grant, so it is this one", "this only runs after approval".
- The code that makes the inference is a helper, or is reachable from more than one route, job or event.
- The derived value is write-once, authorizing, or names another user.
- The plan says a state is unreachable, "cannot happen", "can only be constructed by hand", or relies on it not happening. "I checked, it cannot happen" is the sentence that lets it in: if the enumeration cannot be written, it has not been thought of, which is not the same as impossible.

### Asks for

- **A route × warrant table** for each inference: one row per route, job or event that reaches the inferring code — found by grepping the named file's callers, not from memory; columns: the constraint the inference rests on; where on that route it is checked, as file and line, or "not checked". A "not checked" cell is visible as such.
- **The same table for each "cannot happen"**: one row per path that could produce the state, found by grepping every writer of the columns involved — the plainest create call with an ordinary parameter included; the cell says what stops it there. "Unreachable" with no rows is visible as such.
- **The check in the pseudocode at the point of inference**, numbered, not a comment above it.

### Tell

- The plan derives a value from a precondition and the table has no row for one of the routes grep finds.
- A route row that says "not checked"; a comment or a sentence states a precondition and no numbered step checks it.
- A helper written for one route is reused by a second route.
- A write-once or authorizing value is set from an inference.
- "Cannot happen" or "unreachable" with no path table, or a table that omits the ordinary create path.

### Write

- **Enumerate every route that reaches the code** and check, per route, that it holds the constraint; put the check in the code at the point of inference, not in a comment.
- **When the warrant changes, re-derive every rule that rested on it.** A rule kept after its premise is gone reads like a decision and is a leftover.
- **Never set a write-once or authorizing value from an inference** the route does not guarantee; read it from the source that does.

### Prove

- **One test per route reaching the code, including the route that does not hold the constraint**, asserting the inference is not made there.
- **Change the warrant in the test and watch the dependent rule fail**; a rule that survives its premise's removal is not connected to it.

### View

- **Does the route table match the callers?** Grep the tree for the inferring function; every caller, job and event handler is a row. A caller with no row is a finding against the table, before any finding against the design.
- **List the routes that reach this code. Which carry the warrant?** A comment stating a precondition is a claim: where is the check?
- **Is any value set here permanent or authorizing?** If so, which route guarantees the inference, and is that the only route?
- **For each "cannot happen": which paths write these columns, and what stops each?** An answer that starts with "only by hand" is a finding.

## Rule 6 — Distrust everything crossing a trust boundary

Client to server, one user's request touching another user's data, external to internal (webhook, callback, upload): existence is not permission.

### Where

- A request carries an id, a path segment, a body field or a query string that names a row.
- A request from one user can read or write data another user owns.
- Input arrives from outside the process: a webhook, an OAuth callback, an upload, a queue message, a query string.
- The plan's sequence diagram has a participant on the far side of a trust boundary.

### Asks for

- **A crossing table**: one row per boundary crossing in the diagram or the trust-boundary list; columns: each field that crosses; its shape check; its authorization check — an ownership check against the caller, or the project's one visibility gate by name; its consistency check. An empty check cell is visible as such. "The row exists" does not fill the authorization cell.
- **The visibility gate named once**, and per path whether it goes through the gate or re-implements it.

### Tell

- A client-supplied id is used to load, modify or delete a row; a crossing row whose authorization cell is empty or says "exists".
- "The row exists" is used as "the caller may act on it".
- One user's request reads or writes data owned by another user with no row for it.
- External input is parsed and acted on with an empty shape cell.
- A boundary appears in the plan's diagram with no crossing row.

### Write

- **At every crossing, validate shape, authorization and consistency**, in that order, before the first read that depends on the input.
- **Ownership-check every client-supplied id** against the caller, or route the read through the project's one visibility gate — and name that gate in the plan.
- **Existence is not permission.** A "not found" and a "not yours" are the same answer to the caller.

### Prove

- **The non-owner id test**: a valid id belonging to another user returns the same answer as an unknown id, at the API layer.
- **The wrong-shape test**: malformed input is rejected before any read.
- **The cross-user test** on every path that touches two users' data, asserting each user sees only what the rule allows.

### View

- **Does the crossing table match the handler?** Open the named handler; every field read from params, body, query or headers is a "what crosses" entry. A field with no entry is a finding against the table, before any finding against the design.
- **For each id from the client: where is the ownership check, or which gate does the read go through?**
- **Which single function is the visibility gate, and does this path use it or re-implement it?**
- **Does any crossing in the diagram lack a check?**

## Rule 18 — A withheld outcome is indistinguishable on every channel

When the product decides not to tell the caller something — that they were declined, that a row exists but is not theirs, that an account is registered — the refusal leaks through whichever channel differs: the response shape, a `reason` field, the status code, the timing, the copy, or the ability to ask again. Once a refusal can be recognised it is no longer a refusal. Rule 6 states one case ("not found" and "not yours" are the same answer); this rule is the table.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- The spec says an outcome is not revealed: "declined looks like waiting", "does not disclose whether the account exists", "the requester cannot tell".
- Two outcomes of one request are meant to be indistinguishable to one of the parties.
- A moderation, blocking, declining, rate-limiting or existence decision is returned to the party it was made about.

### Asks for

- **An indistinguishability table** per withheld outcome: one column per outcome the caller must not tell apart; one row per channel — response shape and fields, status code, timing or latency, the UI sentence, the ability to repeat the request and its result, the database constraint that decides the repeat, any email or push. Each cell is "same" or names the difference. A cell that names a difference, or a channel missing from the rows, is visible as such.
- **Where the reason lives**: the server-side column for support, named, and the statement that it never leaves the server.

### Tell

- A `reason`, `declined`, `blocked` or `exists` field in a response the party it concerns can read.
- A unique constraint with a status condition that lets one outcome ask again and the other not — being allowed to ask again is itself the answer.
- Two response shapes, two status codes or two UI sentences for outcomes the spec says look the same; a "still waiting" screen that behaves differently after a decline.
- A table row that says "same" while the named handler has two return statements for the two outcomes.
- An extra read (Rule 14) or a retry whose result differs by outcome.

### Write

- **One response for both outcomes on every path**: the same shape, the same fields, the same status; the reason is written to a server-side column for support and never returned.
- **The database decides the repeat identically**: the constraint carries no status condition, so a declined party cannot ask again any more than a waiting one can — the price (a mistaken decline cannot be undone by asking) is written into the spec.
- **One UI sentence**, identical for both, and identical on every later visit.
- **Timing and side channels considered**: no extra round trip, mail or push on one outcome only.

### Prove

- **Deep-equal the two outcomes**: for each channel in the table, capture it under both outcomes and assert equality — the response body, the status, the rendered UI, the result of asking again; this is the assertion that goes red when any channel diverges.
- **The repeat test**: ask again under both outcomes; assert the same result and the same stored state.

### View

- **Does the table match the handler?** Open it; every return statement, thrown error and side effect is a channel. A channel the table omits is a finding against the table, before any finding against the design.
- **On which channel could the declined party learn they were declined?** Walk the rows; "none" must be earned per row.
- **Can one outcome ask again and the other not?**
- **Where does the reason go, and who can read it?**
