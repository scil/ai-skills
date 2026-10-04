# Binding: TanStack Query

How the catalog's questions show up when the client's server state goes through TanStack Query (`@tanstack/*-query` v5), including the tRPC integration (`trpc.x.y.queryOptions()`). Load this file when the manifest holds `@tanstack/react-query` or a sibling adapter. The question is the catalog's; this file only says what it looks like here. Defaults below are v5's — check the installed version's docs when a default matters.

Each entry: **shows up as** · **look for** · **fix**.

## A. The client sends a request

**A1.1 / A3.4 — a control usable while its mutation is in flight.**
- *Look for:* a button whose `disabled` does not read the mutation's `isPending`, or reads it from a different `useMutation` than the one it fires.
- *Fix:* `disabled={mutation.isPending}`; keep it disabled through the `onSuccess` work that follows (`await` the cache write or navigation inside `onSuccess`, which `isPending` waits for when `onSuccess` returns a promise).

**A1.5 — two saves sharing one pending state.**
- *Shows up as:* one `useMutation` reused for two independent saves; its `isPending`/`error` report whichever ran last.
- *Fix:* one `useMutation` per save that can overlap; give the saves that must not interleave the same `scope: { id }` — mutations sharing a scope run one after another (client-side only; ordering across clients is the server's condition, B1).

**A2.3 — the reader changes under the screen.**
- *Fix:* the signed-in user's id is part of the query key (or the cache is cleared on sign-out with `queryClient.clear()`), so one account's entry is never served to the next.

**A3.5 — write, then refetch.**
- *Shows up as:* `onSuccess: () => queryClient.invalidateQueries(…)` alone. `invalidateQueries` resolves whether or not its refetch succeeded, so a "Saved" shown after it can sit beside the old value.
- *Fix:* `queryClient.setQueryData(key, fromResponse)` first, then `invalidateQueries` as background reconciliation. A response that carries only part of the cached object is merged into it, never written over it.

**A3.6 — derived entries left stale.**
- *Fix:* refresh each through the key factory the project already has — `queryOptions(…).queryKey`, or with tRPC `trpc.x.y.queryKey()` / `trpc.x.pathFilter()` — never a hand-typed array, which silently matches nothing after a rename.

**A3.7 — optimistic update without rollback.**
- *Fix:* `onMutate`: `cancelQueries`, snapshot with `getQueryData`, write the optimistic value, return the snapshot; `onError`: restore it from the context; `onSettled`: invalidate.

**A3.9 — a failure painted as "nothing here".**
- *Shows up as:* `if (!isPending && !data) return <Empty/>`, or a branch on `isSuccess`. When a refetch fails v5 keeps `data` and sets `status: 'error'`, so `isSuccess` turns false while the data is still good; and `isPending` means "no data yet", not "a request is running" (`isFetching` is that).
- *Fix:* branch on `isError` (with a retry action) before the empty state; decide from `data` once it exists; `isLoading` (no data and fetching) ≠ `isFetching` (any request).

**A3.11 — a refusal retried.**
- *Shows up as:* nothing set. Queries retry every failed request 3 times on the client with exponential backoff (up to 30 s between tries), so a 403/404 surfaces seconds late. Mutations do not retry by default.
- *Fix:* `retry: (count, error) => !isAccessRefusal(error) && count < 3` on the queries that can be refused, or as the client default with the refusal codes named once.

## D. A screen holds state

**D1.1 — state seeded from a query result.**
- *Shows up as:* `useState(query.data?.x)` — runs once, usually before the data arrives. With `useSuspenseQuery`, a key that changes with a user choice re-suspends and remounts the subtree, throwing away its local state, which reads as a control that does nothing.
- *Fix:* derive from `data` during render; a draft keyed to the loaded id; for a key the user flips, `useQuery` with `placeholderData: keepPreviousData` instead of a suspense query.

**D3.2 — a poll.**
- *Fix:* `refetchInterval` (the query also fetches on mount, so there is no missing first tick); `refetchIntervalInBackground` defaults to false, which keeps polling to the visible tab.

**D4.2 — "none" and "not known" sharing a branch.**
- *Fix:* branch on `status` (`'pending' | 'error' | 'success'`) before testing `data == null`; only a `'success'` with no data reaches the branch that offers to create.

## H. Someone already owns this

**H1.2 — a hand-written retry or poll beside the client.**
- *Look for:* `setInterval` + `refetch()`, or a `for` loop around a fetch inside `queryFn`.
- *Fix:* `refetchInterval`, `retry`, `retryDelay` own it; delete the hand-written half.
