# Batch: authorization and trust boundaries — Rules 4, 5, 6

## Rule 4 — The client renders outcomes; the server decides who the caller is

"Is this reader signed in, and as whom" is answered from the request's cookie or token on the server. The client's session store is unresolved on first paint, cached for whoever asked last, and changeable from another tab.

### Tell

- Client code branches on "if signed in" or "as user X" to choose between two behaviours.
- A control's enabled state, or a link's target, depends on a session value read on the client.
- The plan reads a session store, local storage or a cached "me" query to decide what a request will do.
- Two endpoints, "the signed-in one" and "the guest one", chosen by the client.

### Write

- **One endpoint that reports what it did**: the server reads the request's credentials, chooses the branch, and returns which (`{ mode: "attributed" }` / `{ mode: "claim" }`); the client renders the outcome.
- **Where the client must know first**, it asks on its own query key, trusts only a succeeded answer, and keeps the control inert until then. An unresolved answer is not "guest".
- **Never carry the identity decision in a request body** the client could set.

### Prove

- **Three client states, one server answer**: unresolved on first paint; cached for a different user; changed in another tab. Each must produce the server's answer for the actual request, and the control must be inert until the answer arrives.
- **A request with the client's claim and a different cookie**: the cookie wins.

### View

- **For each branch on identity in client code: who decided, and from what?** A client-side decision is a finding unless it only chooses what to render after a server answer.
- **What does the control do before the identity answer arrives?**

## Rule 5 — An inference is valid only on the routes that carry its warrant

A value inferred "because only X can reach here" is correct on the route that guarantees X and wrong on every other route that reaches the same code. A comment stating the warrant is not a check.

### Tell

- The plan derives a value from a precondition ("the caller must be the author here", "there is exactly one grant, so it is this one").
- A comment or a sentence states a precondition and nothing checks it.
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

- **List the routes that reach this code. Which carry the warrant?** A comment stating a precondition is a claim: where is the check?
- **Is any value set here permanent or authorizing?** If so, which route guarantees the inference, and is that the only route?

## Rule 6 — Distrust everything crossing a trust boundary

Client to server, one user's request touching another user's data, external to internal (webhook, callback, upload): existence is not permission.

### Tell

- A client-supplied id is used to load, modify or delete a row.
- "The row exists" is used as "the caller may act on it".
- One user's request reads or writes data owned by another user.
- External input (a webhook, an OAuth callback, an upload, a query string) is parsed and acted on without a stated validation.
- A boundary appears in the plan's diagram with no check named at the crossing.

### Write

- **At every crossing, validate shape, authorization and consistency**, in that order, before the first read that depends on the input.
- **Ownership-check every client-supplied id** against the caller, or route the read through the project's one visibility gate — and name that gate in the plan.
- **Existence is not permission.** A "not found" and a "not yours" are the same answer to the caller.

### Prove

- **The non-owner id test**: a valid id belonging to another user returns the same answer as an unknown id, at the API layer.
- **The wrong-shape test**: malformed input is rejected before any read.
- **The cross-user test** on every path that touches two users' data, asserting each user sees only what the rule allows.

### View

- **For each id from the client: where is the ownership check, or which gate does the read go through?**
- **Which single function is the visibility gate, and does this path use it or re-implement it?**
- **Does any crossing in the diagram lack a check?**
