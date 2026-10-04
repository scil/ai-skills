# Binding: React

How the catalog's questions show up in a React UI (web or React Native). Load this file when the manifest holds `react`. The question is the catalog's; this file only says what it looks like here. Version-dependent notes name the version.

Each entry: **shows up as** · **look for** · **fix**.

## A. The client sends a request

**A2.2 — the response lands after the screen is gone.**
- *Shows up as:* a `fetch` in an effect or handler whose `.then` sets state or navigates after the component unmounted or the route changed. Since React 18 there is no warning; the write still happens, and a navigate still fires.
- *Fix:* an `AbortController` aborted in the effect's cleanup; or a data library that ties the request to the component (`useMutation`, a route loader).

## D. A screen holds state

**D1.1 — state seeded once.**
- *Shows up as:* `const [draft, setDraft] = useState(props.value)` (or from a session or query) — the initializer runs on the first render only.
- *Fix:* derive during render; where a local draft is needed, mount the editor with `key={resolvedValue.id}` so it starts fresh when the source changes, and only after the source has arrived.

**D1.2 — an effect that copies a value.**
- *Shows up as:* `useEffect(() => setY(f(x)), [x])` — one render late, and a second source of truth.
- *Fix:* `const y = f(x)` during render (memoised only if measured); or set both in the event handler that changes `x`. An effect is for synchronising with something outside React (a subscription, a DOM API, a timer).

**D3.4 — a re-ask keyed on identity.**
- *Shows up as:* an effect whose dependency array holds a callback or object recreated each render, so it re-runs every render (a storm), or a re-ask that depends on a value which never changes again (it fires once and waits forever).
- *Fix:* depend on the disagreement itself (the mismatching id or version); read the latest callback with `useEffectEvent` (stable from React 19.2) or a ref; cap the attempts and render a visible retry.

**D4.1 — a parent's error branch hides a child.**
- *Look for:* an early `return <Error/>` above children that read their own queries; an error boundary placed so high that one section's failure blanks the page.
- *Fix:* an error boundary (or `Suspense` + boundary) per section.

## F. A branch over a value with several states

**F1.1 — the conditional render that leaks `0`.**
- *Shows up as:* `{items.length && <List/>}` renders the text `0` when empty (on React Native, a crash: text outside `<Text>`).
- *Fix:* `{items.length > 0 && …}` or a ternary.

## H. Someone already owns this

**H2.1 / H2.2 — an interaction hand-written as a hook.**
- *Shows up as:* a new `useClickOutside`, `useFocusTrap`, `useDebounce`, `useHotkeys`, `useVirtualizer`, `useMediaQuery` in a tree whose manifest already holds Radix / React Aria / Headless UI / a `use-*` utility package, TanStack Virtual, or a form library.
- *Fix:* search the manifest and those packages' exports first; the headless kits already handle focus return, nested layers, IME, RTL and touch.
