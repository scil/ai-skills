# fix-bugs — React web (jsdom + Playwright)

Stack-specific mechanics behind `SKILL.md` §3–§4 for a React web app tested with jsdom component tests and Playwright end-to-end specs. The project's own paths and commands come from its `AGENTS.md`, not from here.

## §3 Drift the type checker cannot see

- `useState(initialValue)` reads its argument once, at mount. A component moved so that it mounts before the value resolves keeps the missing value forever. Derive during render instead of seeding state.
- A hook moved across an early return is valid code with different mount timing; check what it read at the old position (a prop, a context, a resolved query) that may not exist at the new one.
- A `useEffect` dependency list that assumed a resolved value silently stops re-running when the value arrives by another route.

## §4 Which layer can observe the defect

- **jsdom component test**: logic, copy, state, wiring. jsdom does **no hit-testing and no stacking** — a test there cannot tell that an element is covered, `pointer-events: none`, or too small to tap.
- **Real browser (Playwright)**: stacking, `pointer-events`, overlap, tap-target size, painted colour, hydration timing.
  - Press **coordinates**, not elements: `page.mouse.click(x, y)` off a `boundingBox()`. A locator `.click()` correctly refuses `pointer-events: none`, so it cannot prove the dead strip is gone.
  - Assert both directions: the inert region does the general thing, *and* a real control inside it still wins its own pixels.

## §4 Browser gotchas, each learned once

- **Hydration**: an SSR element is "actionable" before hydration attaches its handler. Gate on something only true after hydration (`toBeEnabled()`), never `toBeVisible()`.
- **Server writes in helpers**: a helper that triggers a server write waits for it *inside the helper*, or the next database read races it.
- **Seed by id, not by title**: specs that seed the same fixture names and look them up by title find whichever ran first — passes alone, fails in the suite.
- **Oklab read as RGB**: Tailwind's `/25` opacity compiles to `color-mix(in oklab, …)` and Chromium reports the computed colour as `oklab(L a b / α)`; parsing those numbers as RGB gives near-black and a wildly wrong contrast ratio. Cross-check any colour harness against a known pair before trusting it.
- **Transitions**: an element with `transition-colors` reads two different values within ~400 ms; wait for it to settle.
