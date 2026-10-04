# Binding: TanStack Router / TanStack Start

How the catalog's questions show up with TanStack Router file routes (and TanStack Start on top of it). Load this file when the manifest holds `@tanstack/react-router` or `@tanstack/react-start`. The question is the catalog's; this file only says what it looks like here. Option names and defaults move between minor versions — check the installed version's docs or `.d.ts` before relying on one.

Each entry: **shows up as** · **look for** · **fix**.

## A. The client sends a request

**A3.10 — navigating before the commit.**
- *Fix:* `await` the mutation, write the cache, then `navigate`; or have the destination's `loader` read what it needs rather than trusting a cache warmed before the write committed.

**A3.11 — a refusal shown late or as a crash.**
- *Shows up as:* a protected read inside `loader` that throws on 403/404 into the router's default error UI, after the data client's retries.
- *Fix:* map access refusals to `throw notFound()` (rendered by `notFoundComponent`) or an `errorComponent` that renders "not for you" as one answer; mark those errors non-retryable in the data client.

## E. A journey across routes

**E1.1 — context forwarded on one exit only.**
- *Look for:* every `<Link`, `navigate(`, `redirect(` and auth `callbackURL` on the journey's routes; `validateSearch` on the route that reads the token.
- *Fix:* forward with `search: (prev) => ({ ...prev, … })` (or `search: true` to keep all), from the same file that validates it.

**E2.1 — a redirect that Back bounces into.**
- *Fix:* `throw redirect({ to, replace: true })` in `beforeLoad`/`loader`, or `navigate({ to, replace: true })`.

**E2.2 — two routes redirecting to each other.**
- *Shows up as:* `beforeLoad` redirects decided from a session read that may still be pending or may have failed.
- *Fix:* `beforeLoad` awaits the session fetch; a failed read throws to the route's `errorComponent`, never into either redirect.

## H. Someone already owns this

**H1.1 — an option whose default does something.**
- *Shows up as:* `useBlocker({ shouldBlockFn })` with `enableBeforeUnload` unset. It defaults to true, so the browser's "Leave site?" prompt fires on every refresh and close, dirty or not.
- *Fix:* set `enableBeforeUnload` from the same dirty predicate as `shouldBlockFn` (it accepts a function).

**H1.2 — a hand-written listener beside the blocker.**
- *Look for:* `window.addEventListener('beforeunload', …)` in a component that also calls `useBlocker`.
- *Fix:* delete it; `useBlocker` owns both in-app navigation and unload.

## Data loading convention

**A3.5, D1.1 — loaders and the query cache.** In TanStack Start with TanStack Query, the loader prefetches (`context.queryClient.ensureQueryData` / `prefetchQuery`) and the component reads with `useSuspenseQuery` on the same options, so the server render and the client agree on one cache entry. A module-level `queryClient` in route code is shared across requests on the server; take it from the router context.
