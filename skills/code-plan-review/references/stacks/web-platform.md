# Binding: the web platform

How the catalog's questions show up in browser APIs, whatever framework sits on top. Load this file for any plan with a web client. The question is the catalog's; this file only says what it looks like here.

Each entry: **shows up as** · **look for** · **fix**.

## A. The client sends a request

**A1.1 — a second Enter.**
- *Shows up as:* a form submitted by Enter while a previous submit is in flight; disabling the button does not stop Enter in a text field unless the submit handler checks too.
- *Fix:* the submit handler returns early while pending.

**A3.9 — an error status treated as success.**
- *Shows up as:* `const data = await (await fetch(url)).json()` — `fetch` resolves on 4xx and 5xx; only a network failure rejects.
- *Fix:* `if (!res.ok) throw …` before reading the body; or a client wrapper that does it once.

## C. Who is asking

**C1.1 / A2.3 — sign-in or sign-out in another tab.**
- *Look for:* a session cached in memory or `localStorage` with no cross-tab signal.
- *Fix:* the server decides from the cookie on every request; listen for the `storage` event or a `BroadcastChannel` to refresh the session view.

## D. A screen holds state

**D3.2 — a poll in a hidden tab.**
- *Fix:* pause on `document.visibilityState === 'hidden'` (`visibilitychange`), and read once when the tab returns.

**D2.4 — the leave-page guard.**
- *Shows up as:* a `beforeunload` listener that sets `returnValue` unconditionally, so every refresh prompts; or one wired to one editor while another holds the draft.
- *Fix:* call `event.preventDefault()` only while some editor is dirty (one predicate for all editors); the browser shows its own text, never yours.

## E. A journey across routes

**E2.1 — a redirect Back bounces into.**
- *Fix:* `location.replace(url)` / `history.replaceState`, not `location.href = url` / `pushState`.

## H. Someone already owns this

**H1.2 — a hand-written listener beside a library.**
- *Look for:* `beforeunload`, `resize`, `keydown`, `scroll` listeners added in components that also use a router guard, a layout or resize hook, a menu or dialog primitive.

**H2.1 — an interaction the platform already provides.**
- *Fix:* `<dialog>` with `showModal()` (focus trap, Escape, inert background), the `popover` attribute (light dismiss, top layer), CSS `scroll-snap`, `<details>`, `inputmode`/`enterkeyhint` on mobile keyboards.
- *IME:* a key handler that acts on Enter must ignore it while composing — `event.isComposing` (or `keyCode === 229` for older engines) — or Chinese, Japanese, Korean and other IME users send half-typed text.
- *Touch:* "Enter sends" belongs to fine pointers; on `(pointer: coarse)` Enter inserts a newline and a button sends.
