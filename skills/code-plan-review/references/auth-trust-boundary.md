# Batch: authorization and trust boundaries — Rules 4, 5, 6

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

- **One endpoint that reports what it did**: the server reads the request's credentials, chooses the branch, and returns which (`{ mode: "attributed" }` / `{ mode: "claim" }`); the client renders the outcome.
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

### Asks for

- **A route × warrant table** for each inference: one row per route, job or event that reaches the inferring code — found by grepping the named file's callers, not from memory; columns: the constraint the inference rests on; where on that route it is checked, as file and line, or "not checked". A "not checked" cell is visible as such.
- **The check in the pseudocode at the point of inference**, numbered, not a comment above it.

### Tell

- The plan derives a value from a precondition and the table has no row for one of the routes grep finds.
- A route row that says "not checked"; a comment or a sentence states a precondition and no numbered step checks it.
- A helper written for one route is reused by a second route.
- A write-once or authorizing value is set from an inference.

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
