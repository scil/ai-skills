# Batch: navigation flow — Rule 22

A journey across routes. The other batches ask what one screen holds, what one statement writes, who one request is from; this one asks where the person ends up, by every path they can take. Its failures are single-threaded and single-user, no state drifts and no permission leaks — a route simply has an exit the journey never accounted for, and the person walks out through it with nothing failing. The batch is the boundary *between* screens; state *inside* a screen is ui-state-ownership, and whether a value arriving by query string can be trusted is auth-trust-boundary (Rule 6) — this batch asks only whether it arrives.

## Rule 22 — A journey completes from every exit

The 2026-09-18 lesson: a scanned card had to survive scan → sign in → first run → back to the card, riding in the URL as `share`. Every hop copied it forward, and the setup component returned to the card "from EVERY way out of the form, including the two shortcuts" — a sentence written after an earlier round lost the token on a shortcut. Then first run moved to its own route, which had one more exit the component could not see: the signed-out fallback, `<Link to="/signin">` with no `search`. The token stopped there. The component had enumerated its exits; the route wrapping it had not enumerated the route's.

### Stack

Any router with routes and navigations — TanStack Router `search`, React Router `state` and query, Expo Router params, a server redirect, an OAuth `callbackURL`. Never skipped.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- The spec describes a journey that crosses more than one route before its goal (scan → sign in → set up → back to the card; invite → accept → land on the thing).
- A route's search or param schema accepts a value another route put there so that a later route can act on it.
- A route on the journey has an exit that is not the happy path: a signed-out fallback, a "you already did this" redirect, a retry, a shortcut, a Cancel, Back.
- A sign-in or OAuth round trip sits inside the journey, so the context must survive a callback URL as well as client navigation.
- Two routes redirect to each other on conditions (home sends the unset-up person to setup; setup sends the set-up person home).

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **The journey's goal, stated once**: where the person must end up, and what context that route needs in order to be the goal (the card's token, the invite's id).
- **The navigation graph** — the routing term (Android Jetpack Navigation's) for what UX calls a screen flow: a directed graph whose nodes are routes and whose edges are the navigations out of them, so that an exit *is* an outgoing edge — as fenced Mermaid (`flowchart` or `stateDiagram-v2`), every edge labelled with the context it carries or `—`. It is a living intermediate (SKILL.md, "Project intermediates"): the project's `navigation-graph.md` holds the whole graph, and the plan carries the delta — the routes and edges it adds, removes or re-targets, each naming the file's row — or one line saying no edge changes, checked against the file. A UX user flow drawn along the happy path is not this graph; the graph is complete only when every route on the journey has as many outgoing edges as its file has navigations.
- **A hop × exit table, the edge list of the graph.** One row per edge out of every route on the journey — the happy path, each shortcut, the signed-out link, the already-done redirect, the error branch, Back — with: where it goes; the context it forwards; or, where it forwards nothing, the reason the journey may end there. A row whose forward cell is empty with no reason is visible as such; so is an edge with no row, or a row with no edge. The table carries what the picture cannot: the forwarded context and, below, push or `replace`.
- **For each redirecting exit**: push or `replace`, and where Back lands afterwards.
- **For each pair of routes that redirect to each other**: the two conditions side by side, and the states (including a failed read) under which neither holds.

### Tell

- A route whose `validateSearch` (or param schema) accepts the context and whose file contains a `Link`, `navigate`, `redirect` or `callbackURL` built without it.
- A comment in one component saying "from EVERY way out" while the route that renders it has an exit the comment's list does not cover.
- The context is forwarded on the happy path and the plan calls the other exits "edge cases".
- The plan describes the journey as a sequence of routes and carries no table of exits.
- The journey crosses a route the change does not write, and the living graph gives that route fewer outgoing edges than its file has `Link`, `navigate`, `redirect` or `callbackURL` calls — the incident's exit was on exactly such a route.
- The delta adds a route and its happy-path edge, and the graph shows the new route with one outgoing edge.
- A conditional redirect written as a push (no `replace`), so Back lands on a page that bounces again.
- Two routes that redirect to each other, and a state — the read is pending, the read failed — under which both conditions, or neither, hold.

### Write

- **The property the spec needs**: the person reaches the goal by whichever exit they take, or the journey ends on purpose at a named exit with its reason shown to them ("your card is still where you left it").
- **Forward the context from every exit in the same file that reads it**; the route that accepts the value owns every navigation out of itself, including the ones inside a fallback branch.
- **Where the journey has more than two hops or crosses a sign-in, consider one holder instead of N forwards**: the goal reads the context from a place the URL does not carry — the session, a cookie, a pending row keyed on the account — and no exit can lose it. An option under its conditions (an anonymous visitor, a token that must not be stored, may rule it out), not this batch's reflex.
- **A conditional redirect uses `replace`**, so Back returns to where the person came from, not to the page that sent them on.
- **A pair of mutual redirects has conditions that cannot both hold and a third state that holds neither**: "no porch" and "has a porch" are not exhaustive — "could not read" goes to neither, and is shown as such (Rule 15 owns what it shows).

### Prove

- **Enter the journey at its first hop with the context, take each non-happy exit in turn, and assert arrival at the goal with the context** — the assertion that goes red when one `search` is removed. One test per row of the hop × exit table, or one parameterised test over the table.
- **Through the sign-in**: the same journey with the OTP or OAuth round trip in the middle, asserting the context survives the callback.
- **Back after the bounce**: navigate to the redirecting route, then Back; assert the page before it, not the bouncing page.
- **The mutual pair under a failed read**: fail the read on each route of the pair, assert neither redirects.

### View

- **Does the navigation graph, with the delta applied, match the files?** Open every route on the journey — the ones the change writes and the ones it only crosses; grep each file for `<Link`, `navigate(`, `redirect(`, `callbackURL`. Each hit is an edge and a row, or a finding against the graph (`intermediate differs from code`, anchored to the file's row) before any finding against the design. A route with fewer edges than hits is the usual answer.
- **Does the hop × exit table match the graph?** One row per edge, one edge per row; a row without an edge, or an edge without a row, is a finding against the table.
- **Which exit is not in the table?** The signed-out branch and the already-done redirect are the usual answers.
- **Where does Back land after each redirect?** A push on a conditional redirect is a finding.
- **For the mutual pair, what happens when the read fails on either side?** Both redirecting, or both looping, is a finding.
- **Could the context live in one holder instead?** Ask, and record the answer with its reason; either answer can be right.
