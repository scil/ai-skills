# Binding: the web platform

How the tree's nodes show up in browser APIs, whatever framework sits on top. Load this file for any plan with a web client. The node is the tree's. This file only says what it looks like here.

Each entry: **shows up as** · **look for** · **fix**.

## S · Scenarios

**S7.1 — what a crawler or a link preview receives.**
- *Shows up as:* a page moved behind sign-in or rendered only in the browser, so crawlers and previews get a login page or an empty shell. A redirect with 302 where 301 was meant. A changed URL with no `rel="canonical"` or redirect from the old one.
- *Look for:* `robots.txt`, `<meta name="robots">`, `X-Robots-Tag`, `rel="canonical"`, Open Graph tags (`og:title`, `og:image`), the sitemap, and the status code per route.
- *Fix:* per changed route, state the status, the server-rendered content and the indexing tags. Keep public pages server-rendered. Move a URL with a 301 and update the sitemap. An AI-agent interface (for example MCP) exposing actions also passes L1.

**S7.2 — a control only some people can use.**
- *Look for:* a `div` or `span` with a click handler and no `role`, `tabindex` or key handler. An icon button with no `aria-label`. A hard-coded string beside translated ones. A fixed width with no media query.
- *Fix:* use a native `button` or link. Give every control an accessible name. Route text through the translation layer. Check the smallest supported viewport and a keyboard-only pass (axe or a similar checker).

**S3.1 — a second Enter.**
- *Shows up as:* a form submitted by Enter while a previous submit is in flight; disabling the button does not stop Enter in a text field unless the submit handler checks too.
- *Fix:* the submit handler returns early while pending.

**S6.1 — an error status treated as success.**
- *Shows up as:* `const data = await (await fetch(url)).json()` — `fetch` resolves on 4xx and 5xx; only a network failure rejects.
- *Fix:* `if (!res.ok) throw …` before reading the body; or a client wrapper that does it once.

## L · Logical

**L1.1 / S1.2 — sign-in or sign-out in another tab.**
- *Look for:* a session cached in memory or `localStorage` with no cross-tab signal.
- *Fix:* the server decides from the cookie on every request; listen for the `storage` event or a `BroadcastChannel` to refresh the session view.

## S · Scenarios

**S1.4.1 — a poll in a hidden tab.**
- *Fix:* pause on `document.visibilityState === 'hidden'` (`visibilitychange`), and read once when the tab returns.

**S5.2 — the leave-page guard.**
- *Shows up as:* a `beforeunload` listener that sets `returnValue` unconditionally, so every refresh prompts; or one wired to one editor while another holds the draft.
- *Fix:* call `event.preventDefault()` only while some editor is dirty (one predicate for all editors); the browser shows its own text, never yours.

**S4.2 — a redirect Back bounces into.**
- *Fix:* `location.replace(url)` / `history.replaceState`, not `location.href = url` / `pushState`.

## D · Development

**D5.2 — a hand-written listener beside a library.**
- *Look for:* `beforeunload`, `resize`, `keydown`, `scroll` listeners added in components that also use a router guard, a layout or resize hook, a menu or dialog primitive.

**D3.1.1 — an interaction the platform already provides.**
- *Fix:* `<dialog>` with `showModal()` (focus trap, Escape, inert background), the `popover` attribute (light dismiss, top layer), CSS `scroll-snap`, `<details>`, `inputmode`/`enterkeyhint` on mobile keyboards.
- *IME:* a key handler that acts on Enter must ignore it while composing — `event.isComposing` (or `keyCode === 229` for older engines) — or Chinese, Japanese, Korean and other IME users send half-typed text.
- *Touch:* "Enter sends" belongs to fine pointers; on `(pointer: coarse)` Enter inserts a newline and a button sends.
