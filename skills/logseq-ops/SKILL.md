---
name: logseq-ops
disable-model-invocation: true
description: Use when you change a Logseq graph through code. Covers edits to page files, a graph's custom.js, and block data read from custom.js. Also covers buttons that run local programs (runCli and :commands-allowlist), a page in the Journals view, and interactive HTML in a page. Applies to Logseq OG 0.10.x and Logseq DB 2.0.x.
---

# Logseq Ops

Logseq can run local programs from a graph without a rebuild. A graph's `custom.js` runs in the app window, where `window.apis.doAction` reaches the Electron main process. Community plugins run in a sandbox and cannot do this.

## Console panel

To build a panel of buttons that run a project's commands, read `references/console-panel.md`. The panel script lives only in the main graph, `E:\GitHub\scil-only-me\Logseq-scil\logseq\custom.js`, and `scripts/console2logseq.py` moves an Obsidian console into a page.

## Journals view and embedded pages (OG)

1. No setting pins a page above the Journals view. Pick by where it must show:
   - Under today's journal, after its blocks, in every session: an entry in `:default-queries {:journals [...]}` of `logseq/config.edn`. Past days do not show it. List order sets its place among the other default queries. To show a page's top-level blocks with their children: `[:find (pull ?b [*]) :where [?p :block/name "<lower-case name>"] [?b :block/page ?p] [?b :block/parent ?p]]`.
   - At the top of each new day: `{{embed [[page]]}}` as the first child of the template named in `:default-templates {:journals "<name>"}`. Days that already exist keep their content.
   - Above everything: `:default-home {:page "<page>"}`. This replaces the Journals view as the start page.
2. The Diagrams as Code plugin (`{{renderer code_diagram,mermaid}}`) sends the diagram text to kroki.io to render it. For private data (schedules, plans), use a local HTML page instead.
3. Interactive local HTML: put it in `<graph>/assets/` and embed it in a block with `<iframe data-src="../assets/x.html" style="width:100%;height:470px;border:0;"></iframe>`. Logseq keeps `<iframe>` and `data-*` through its sanitizer, but it never rewrites an iframe `src`: a relative `src` resolves against Logseq's own app folder, and it rewrites `../assets/` only in `custom.css`. A short script at the end of the main graph's `custom.js` sets `src` to `file:///<graph path>/assets/x.html`, with the path from `logseq.api.get_current_graph()`. Without that script, write an absolute `file:///` URL in `src`. Checked in OG 0.10.15: the frame loads, and its relative `<script src>` loads too.
   - The frame is a `file://` page like Logseq's own window, so it shares Logseq's `localStorage`. Prefix its keys (`gantt:`).
4. Keep the page's data in a sibling `x-data.js` that sets `window.X = [ ...JSON... ]`, loaded with `<script src="x-data.js">`. A page opened from `file://` cannot `fetch` a JSON file, but a script tag loads. An agent then edits only the data file. If `window.X` is missing, show a visible error. Then a typo in the data does not leave a blank frame.
5. To test the page outside Logseq, serve the folder: `python -m http.server 8765 --bind 127.0.0.1`. The Claude desktop browser pane shows a `file://` page as a `data:` snapshot, where relative scripts do not load. Stop the server after the test.

## Edit a page file (OG)

1. An OG page is `<graph>/pages/<name>.md`. Each block is a line `- text`, and the tab count before the dash sets the nesting level. Use tabs, not spaces, and keep the file's own line endings.
2. The Read tool puts a tab between the line number and the line. That tab looks like one more indent level. An Edit string copied from the Read view then has one tab too many and does not match. Count the real tabs first: `cat -T <file>` shows each tab as `^I`.
3. For a large insert, a script that finds the anchor line by its text and splices in the new lines is safer than an Edit. Assert that the anchor matches once, and print the result with `cat -T` after the change.
4. If the file changes on disk, Logseq reads it again. If the page is open with unsaved typing, Logseq can ask which version to keep. Close the page or stop typing before an agent edits it.

## custom.js

1. Where it lives:
   - OG: the file `<graph>/logseq/custom.js`.
   - DB: a file entity inside the graph database. Open it with Ctrl+K, then type `custom.js`.
2. Logseq asks the user before it runs a new or changed `custom.js`, and asks again after 7 days. Logseq runs the script once, at window start or at the first open of the graph. You edit the file, then restart Logseq.
3. A one-time guard such as `if (window.__x) return; window.__x = true;` blocks a newer script after a graph switch in the same window. The cause is that the old graph's script already set the guard. Version the guard and let the newer script replace the older one, or restart Logseq after a switch.
4. In 2.0, Logseq takes pointer events before they reach a block and starts edit mode. Controls drawn inside a block need capture listeners on `window` for `pointerdown`, `pointerup`, `mousedown`, `mouseup` and `click`. These listeners call `stopPropagation()` and run the control there.
5. Read block data with `logseq.api.get_block(uuid, { includeChildren: true })`. It works in OG and in 2.0, and it returns the children of folded blocks. In 2.0 it returns a promise, so always `await` it. A block element is `.ls-block` with the attribute `blockid`. OG block text is in `content` and includes `key:: value` property lines. 2.0 block text is in `title`.
6. Logseq redraws blocks often. Find the elements you change with a `MutationObserver` on `document.body`, and mark each handled element. To redraw after an edit, watch the block element, and ignore mutations inside your own drawn elements.
7. If a drawn view hides its source blocks, give the user a way to reach them. `logseq.api.edit_block(uuid)` does nothing while a parent block is folded. First walk up with `get_block(b.parent.id)` and call `set_block_collapsed(uuid, false)` on each parent. OG saves each unfold as a change in the page file. OG draws a long list of child blocks lazily, and `edit_block` also does nothing on a block that is not drawn. Fold the sibling blocks that are not on the path, and wait until `.ls-block[blockid="<uuid>"]` exists before you call `edit_block`.
10. OG draws the next part of a long page only on a scroll near the bottom. If CSS hides many child blocks, the page gets short, no scroll comes, and the blocks after them stay missing. After you hide them, send `scroll` events to the scrolling ancestors until the count of `.ls-block` elements stops growing.
9. A redraw timer from a `MutationObserver` can fire after the view already redrew itself. If its view is no longer connected, the timer must do nothing. Each render must also remove an older view first. Otherwise two views show. If the block folds or unfolds, redraw at once without the timer, because a 600 ms timer makes the view show 0.7 seconds late. While CSS hides the child blocks, ignore changes inside them. OG adds them in parts after an unfold, and each part otherwise causes a full redraw.
8. A fold, an unfold or an edit makes Logseq rebuild the block's element. Keep view state, such as "source shown", in a script variable keyed by block uuid. Copy it to the element on each render, because a class on the old element is lost.

## Inspect a running Logseq

Screenshots do not show which block is in edit mode, or whether a block is drawn. Read the state from inside the app:

1. Quit Logseq. Start OG with a local debug port: `Logseq.exe --remote-debugging-port=9333`.
2. Read `http://127.0.0.1:9333/json`, and take the `webSocketDebuggerUrl` of the page whose URL ends with `electron.html`.
3. Send `Runtime.evaluate` with `awaitPromise: true` and `returnByValue: true` over that WebSocket. `scripts/cdp.mjs` does steps 2 and 3: `node scripts/cdp.mjs "<expression>"`. Node 22 has `WebSocket` built in.
4. Useful expressions: `logseq.api.check_editing()` returns the uuid of the block in edit mode, or `false`. `document.querySelector('.ls-block[blockid="<uuid>"]')` tells whether a block is drawn. `logseq.api.push_state('page', { name: '<page>' })` opens a page.
5. After the test, restart Logseq without the flag. Then make sure that the port is closed.

Risk: while the port is open, any local program can run code in Logseq. Keep it open only for the test.

Do not look for the editor with `document.querySelector('textarea')`. A rendered code block also contains a textarea.

## Shell runner

1. `window.apis.doAction(['runCli', { command, args, returnResult: true }, 'js-obj'])` runs `command + ' ' + args` through `child_process.spawn` with `shell: true`. With `returnResult`, each output chunk becomes a Logseq notification, so a long output shows many notifications. The trailing `'js-obj'` makes the call work in OG and in 2.0, where messages use transit.
2. Logseq has a built-in set of commands: `git`, `pandoc`, `ag`, `grep`, `alda`. Any other command must be in `:commands-allowlist` of `%APPDATA%\Logseq\configs.edn`. An example is `{:commands-allowlist ["pwsh" "powershell"]}`. Logseq reads this file only at startup. OG and a normal 2.0 install share this file.
3. Risk: an allowed shell lets any graph's `custom.js` run commands. Open only graphs you trust, and accept the custom.js prompt only for code you read.
4. Write Windows paths in JS strings with forward slashes. Logseq lost the backslashes, and `\f` became a form-feed character.
5. Pass only fixed keys as arguments, and check them with a pattern such as `/^[a-z0-9-]+$/`. The command runs in a shell, so free text is executable. To send free text, encode it as base64 of UTF-8 and decode it in the program (the console panel's `free` field does this).
6. `window.apis.openExternal(url)` opens only `https:`, `http:`, `mailto:`, `zotero:` and `file:` URLs. A custom protocol does not work. `doAction(['readFile', path, 'js-obj'])` reads a local file in both versions.
7. `custom.js` is a public Logseq feature, and `logseq.api.*` is the API that plugins use. `window.apis.doAction` is internal: Logseq uses it for its own features and does not document it, so a new version can rename or remove it without notice. It works in OG 0.10.x and DB 2.0.x. If a panel draws after a Logseq update but its buttons do nothing, look at `doAction` first. Run `typeof window.apis?.doAction` in the window, as "Inspect a running Logseq" shows.
