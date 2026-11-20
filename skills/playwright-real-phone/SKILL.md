---
name: playwright-real-phone
disable-model-invocation: true
description: Run Playwright tests in Chrome on a USB-connected Android phone: connect over CDP through adb, keep the page drawable, tap and type like a guest, and debug a paused test with playwright-cli. Use when tests must run on a real Android phone, or when a phone run hangs, misses taps or loses its output.
---

# Playwright on a real Android phone

Hand-offs: a failing test whose cause is unknown → fix-bugs. A plan-review question about the suite → code-plan-review. Origin: [`readme.md`](readme.md).

Device emulation (`devices['Pixel 7']`) tests the viewport. A real phone also tests the real screen, touch, the soft keyboard, the phone's language and the phone's network. The facts below come from Playwright 1.64 and Chrome for Android on a Samsung phone.

## Principles

1. **One suite, one more project.** Run the phone as a Playwright Test project, not as a separate script. It gets the same specs and the same report, with screenshots as attachments. A separate script drifts from the suite and needs its own report.
2. **The phone is shared state.** Use one worker and no parallel tests. Every test leaves the phone as it found it: signed out, cart empty, no extra tab.
3. **Change nothing on the phone.** Do not change how the phone behaves, for example its screen timeout. The owner accepts the terms of an app on the phone, not the agent.
4. **A failure names its owner.** A failed request to the site's own host fails the test. A failed request to another host can come from the phone's network. Record it as an annotation. Make sure that it also fails on another network before you call it a site bug.

## Path: set up the project

1. Make sure that the phone is ready. `adb devices` lists it as `device`. The output of `adb shell dumpsys package com.android.chrome` has a `versionName`, so Chrome is installed. A person opened Chrome once, so its first-run screens are gone. With several phones, pass `-s <serial>` on every adb command.
2. Connect in three commands. First, `adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main -d about:blank`. Second, `adb forward tcp:<port> localabstract:chrome_devtools_remote`. Third, `chromium.connectOverCDP('http://127.0.0.1:<port>')`, with a few retries.
3. If the site runs on the PC, run `adb reverse tcp:<site-port> tcp:<site-port>`. Then the phone reaches the same `localhost` address. Remove the reverse at the end.
4. Override the built-in `browser` fixture behind a worker option. The other projects keep their own launch:

   ```js
   export const test = base.extend({
   	phone: [false, { option: true, scope: 'worker' }],
   	browser: [
   		async ({ playwright, browserName, phone }, use) => {
   			if (!phone) {
   				const browser = await playwright[browserName].launch();
   				await use(browser);
   				await browser.close();
   				return;
   			}
   			const device = await connectPhone(playwright.chromium);
   			await use(device.browser);
   			await device.close();
   		},
   		{ scope: 'worker', timeout: 60_000 },
   	],
   	page: async ({ page, phone }, use) => {
   		if (phone) await page.bringToFront();
   		await use(page);
   	},
   });
   ```

   Specs that also run on the phone import this `test`, not the one from `@playwright/test`.
5. If an environment variable asks for the phone, add the phone project to the configuration. Without the variable, a normal run never looks for a phone. Give the project this configuration:
   - `testMatch` over the shared specs and the phone-only specs, and `grep: /@phone/`
   - `workers: 1` and `fullyParallel: false`
   - its own `outputDir`
   - `use: { phone: true, viewport: null, hasTouch: true }`. The `viewport: null` keeps the real screen.
6. Tag each shared test that suits a phone with `{ tag: '@phone' }`.
7. Done: without the variable, `npx playwright test --list` shows the same count as before and no phone project. With the variable, it lists only the tagged tests.

## Path: write a phone test

1. Act as a guest. Use `tap()` for buttons and links. Use `fill()` and then `blur()` for fields (see the keyboard trap below).
2. Attach evidence at each step: `testInfo.attach(name, { body: await page.screenshot(), contentType: 'image/png' })`.
3. Test the layout on each page. `document.documentElement.scrollWidth` is not more than `innerWidth`. No image has `complete && currentSrc && !naturalWidth`.
4. Watch the page in an auto fixture. Collect `pageerror`, console errors and `requestfailed`. Ignore `net::ERR_ABORTED`, because a navigation aborts the open requests of the old page. Split failed requests by host (principle 4).
5. Locate elements by state or data. Never locate by text that follows the phone's language (see the locale trap).
6. Done: the test passes on the phone, and the screenshots in the HTML report show each feature at work.

## Path: debug a failing test

1. Read `error-context.md` in the output folder of the test. It holds the accessibility snapshot of the page at the failure. It often shows the cause: a hidden element, a reload, or an unexpected page.
2. Read the trap table below before you change the test.
3. To look at the page live, pause the test and attach `playwright-cli`. This is Microsoft's `@playwright/cli`, and its skill reference `playwright-tests.md` describes the steps:
   1. Run `PLAYWRIGHT_HTML_OPEN=never npx playwright test <file> --debug=cli` in the background.
   2. Wait until it prints the debugging instructions with a session name.
   3. Run `playwright-cli attach <session>`. Each action that you do through `playwright-cli` prints the matching Playwright code. You can copy that code into the test.
   4. Stop the background run at the end.

   Nobody tried this with a phone project yet. Make sure that the session attaches to the browser on the phone before you rely on it.
4. Done: you name the cause with evidence from the snapshot, a screenshot or the page, and the test passes on the phone.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `click()` or `tap()` waits forever at "visible, enabled and stable". Screenshots hang. | A new page opens in a background tab. Chrome does not draw a hidden tab. | Call `page.bringToFront()` before the first action. |
| Actions hang, or `connectOverCDP` gets `ECONNRESET`, after about 30 seconds. | The screen turned off, so Chrome went to the background. | Send `adb shell input keyevent KEYCODE_WAKEUP` every 15 seconds. It does nothing while the screen is on. Call `unref()` on the timer. |
| `tap()` says that the context does not support tap. | The default context of the CDP browser has no touch. | Use `browser.newContext({ viewport: null, hasTouch: true })`. The `use` of the project gives this. |
| A locator by `aria-label` finds nothing in a widget such as a date picker. | The widget labels follow the phone's language, not the page's language. | Locate by data. For flatpickr, mark the day cell whose `dateObj` matches, then tap it. |
| The tap after a `fill()` hits the wrong element. | The soft keyboard is still open and moved the layout. | Call `blur()` on the field and wait about one second before the next tap. |
| A file in the test output folder is gone after a run. | Playwright empties the `outputDir` of every project in the run. | Never keep backups there. Give the phone project its own `outputDir`, and ignore it in git. |
| A submit reloads the page and does not run the page script. | The tap came before the page script took over the form. A test is faster than a person. | Wait for the ready signal of the script. If the page recovers from an early submit, do what a guest does there and assert it. |
| A third-party script fails only on the phone. | The network of the phone blocks that host. | Record an annotation, not a failure (principle 4). Try another network. |
