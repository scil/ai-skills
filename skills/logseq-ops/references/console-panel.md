# Console panel in a Logseq graph

A console panel is a block that shows tabs of colored buttons. A button runs one fixed command of a project. The only copy of the panel script is `E:\GitHub\scil-only-me\Logseq-scil\logseq\custom.js`, in the main graph. Change it there, and copy it from there. It works in Logseq OG 0.10.x and in Logseq DB 2.0.x. The panel reads its data from the child blocks of its own block, so you edit the data in Logseq.

## Parts

| Part | Where | Job |
|---|---|---|
| panel script | `<graph>/logseq/custom.js` (OG), or the `custom.js` file entity (DB) | draws every panel in the graph |
| allowlist | `%APPDATA%\Logseq\configs.edn` | lets Logseq start the shell |
| runner | `<repo>\scripts\win\run_for_obsidian_console.ps1` | the project's one entry point: key to one fixed command |
| marker block | any page | the panel's place, its runner, and its data as child blocks |

A Logseq panel adds no logic of its own. `console-design.md` says which buttons a console needs, how to group them and write its cards, and how the runner works. `runner-scripts.md` covers the scripts behind a button.

## How a click reaches the runner

Logseq is an Electron app with two processes. The renderer process shows the window and runs page scripts. The main process has full system access and can start programs. A click passes through both:

```
renderer: custom.js draws the panel, checks the values, builds the command line
   └─ window.apis.doAction(['runCli', ...])                       (bridge to the main process)
main:     runCli checks the first word against the allowlist      ("pwsh"? allowed)
   └─ child_process.spawn(..., { shell: true })  →  cmd.exe /d /s /c "<line>"
         └─ pwsh -NoProfile -File <runner> -Button <key> [-Param "value" ...]
               └─ the runner's fixed command for that key
```

- A page is only text, and Logseq has no button that runs a program. custom.js is the only code that runs in the window and can call `window.apis.doAction`. Community plugins run in a sandbox without that bridge, so they cannot start a program.
- Logseq runs custom.js once for each window, at window start or at the first open of the graph. The script stays loaded while you change pages. A `MutationObserver` reports the blocks that each opened page draws. The script draws a panel only where it finds a `console-grid` marker. After you edit custom.js, restart Logseq.
- The allowlist decides only which program Logseq can start. It does not remove `cmd.exe`. With `shell: true` on Windows, `cmd.exe` reads the whole line first. A `&`, `|`, `>`, `^` or extra `"` in a value acts there, before `pwsh` starts. For example, `-Selection "a" & calc & "b"` starts Calculator.
- `pwsh -File` passes each argument to the runner as plain text and does not run it. The risk is only in the `cmd.exe` layer.
- custom.js therefore allows only safe characters in keys and form values. A `free` field sends its text as base64 of UTF-8 in `-<Param>B64 "<base64>"`. Base64 uses only letters, digits, `+`, `/` and `=`, which have no meaning in `cmd.exe`. The runner decodes it:

  ```powershell
  param([Parameter(Mandatory = $true)][string]$Button, [string]$Selection = '', [string]$SelectionB64 = '')
  if ($SelectionB64) { $Selection = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($SelectionB64)) }
  ```

- Logseq asks before it runs a new or changed custom.js, because any code in that file can reach the bridge. Read the script before you accept it.

## Set up a graph once

1. The main graph already has the script. For another graph, copy the main graph's `custom.js` to `<graph>/logseq/custom.js`. If that graph already has a `custom.js`, append the script to it. The copy does not follow later changes.
2. Add the shells to `%APPDATA%\Logseq\configs.edn`: `{:commands-allowlist ["pwsh" "powershell"]}`. Keep any entries that are already there.
3. Quit Logseq completely and start it again. Logseq reads `configs.edn` only at startup.
4. Accept the prompt that asks to run `custom.js`. Read the script before you accept it.

Risk: an allowed shell lets any graph's `custom.js` run commands. Open only graphs you trust.

## Add a panel to a page

1. Pick the project's page. If there is none, make a page with the project's name.
2. Add a block whose text holds the marker as inline code, after a title:

   ```
   - <Project> 控制台 `console-grid <shell> <runner path>`
     collapsed:: true
   ```

   `<shell>` is `pwsh` or `powershell`. Use `pwsh` for a new project. Write the runner path with forward slashes, for example `E:/GitHub/scil/Leafi/scripts/win/run_for_obsidian_console.ps1`. The marker splits on spaces. If the path holds a space, write the folder's 8.3 short name instead, for example `E:/GitHub/scil/UNITYM~1/scripts/win/run_for_obsidian_console.ps1`. Get it with `pwsh -NoProfile -Command '(New-Object -ComObject Scripting.FileSystemObject).GetFolder("<folder>").ShortPath'`. If it prints the long name, 8.3 names are off on that volume: move the repository to a path without spaces.
3. Add the data as child blocks of the marker block, in this shape:

   ```
   - <Project> 控制台 `console-grid pwsh E:/GitHub/x/scripts/win/run_for_obsidian_console.ps1`
     collapsed:: true
   	- 开发
   		- 🌐 Web 开发服务器 | dev-start | blue | Starts the dev server on :3001
   		- 数据库
   			- 🗑 清空数据库 | db-fresh | red | Deletes all rows
   		- 为什么打不开?(点开)
   			- The answer, as one or more child blocks.
   		- A note line with no children.
   ```

   | Child block | Becomes |
   |---|---|
   | a direct child of the marker, with children | a tab |
   | `name \| key \| color \| help`, one line, no children | a button |
   | the same line, with field lines as children | a form button (see "Form buttons") |
   | a title whose children include buttons, or subgroups | a subgroup with a frame; a subgroup inside a subgroup has a thinner frame |
   | a subgroup title that ends in `` `side-by-side` `` | a subgroup whose child subgroups stand in columns; the keyword is not shown |
   | a title with children and no buttons or subgroups | a folded card, with the children as its body |
   | a block with no children that is not a button | a note line |

   Use `side-by-side` only for parallel subgroups, such as one set of buttons for each of two targets, so the reader can compare them line by line. Inside the columns, each subgroup shows its buttons in one column, so the same buttons line up across the columns. Without the keyword, child subgroups stand one below the other. A narrow window also puts the columns one below the other.

   Two or more cards and notes in a row fold into one closed **📖 说明 · N** card. Then they do not push the buttons apart. A run at the end of a tab shows as it is, because no buttons follow it. The panel remembers whether each 说明 card is open.
4. A button's key is a runner key, which must match `^[a-z0-9-]+$`. A key can also be an `http`, `https` or `file` link, and the button then opens that link.
5. Colors are `blue`, `green`, `yellow`, `orange`, `red` and `purple`. A `red`, `orange` or `yellow` button asks for confirmation before it runs.
6. Fold the marker block. The panel draws within one second.

## Form buttons

A button whose children are all field lines opens a form. The form sends each field to the runner as `-Param "value"`, after `-Button <key>`:

```
- 🚀 启动开发服务器… | dev-start | blue | Asks for six values
	- Name | 库名(可空) | text |  | ^$|^[a-z][a-z0-9_-]{0,62}$
	- Port | 端口 | select | 3001 | 3001,3002,3003,3004,3005
	- Panel | 开面板 | check | 0
	- Otp | 验证码送到哪 | select |  | ,auto,capture,email
```

A field line is `Param | label | type | default | extra`:

| Type | Input | extra |
|---|---|---|
| `text` | a text box | a pattern that the value must match, or nothing |
| `select` | a drop-down list | the options, separated by commas. A leading comma adds an empty option. |
| `check` | a tick box that sends `1` or `0` | not used |
| `free` | a wide text box that takes any one line of text | not used. Its child blocks, one line each, are suggestions in a drop-down list. |

- `Param` must match `^[A-Z][A-Za-z0-9]*$`, and the runner must declare it as a `[string]` parameter.
- Every value of `text`, `select` and `check` must use only letters, digits and `_ . : @ / -`. The panel refuses other characters, because the values go through `cmd.exe`. The panel also refuses a select value that is not an option, and a text value that does not match the pattern.
- A `free` value can hold any characters, for example Chinese text, quotes, `&` or `|`. The panel sends it as `-<Param>B64 "<base64 of the UTF-8 text>"`, so `cmd.exe` sees only base64 characters. The runner declares `[string]$<Param>B64 = ''` and decodes it after `$ErrorActionPreference = 'Stop'`:

  ```powershell
  if ($SelectionB64) { $Selection = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($SelectionB64)) }
  ```

  Then the runner passes the text to its command as one PowerShell argument. Never paste the text into a `cmd /c` string, because `cmd.exe` then parses it again.
- The form shows the runner arguments as you type, and an error line under them. If a field is not valid, 启动 does nothing.
- The runner passes the values to its script, and the script must make sure that they are valid again. Do not rely on the form alone.
- If one child line does not parse as a field, the block is not a button. It becomes a subgroup or a card.

## Use and edit a panel

- A folded marker block shows only its title line. Unfold it with the arrow or with Ctrl+Down, and the panel shows without the data.
- A click on a button runs `<shell> -NoProfile -File <runner> -Button <key>`. Each output chunk of the runner shows as a Logseq notification.
- Alt+click on a tab, button, card or note shows the data below the panel and puts the cursor on that element's own block. It also folds the other tabs, so that the data stays short. The green ✓ 完成编辑 hides the data again.
- The panel redraws about 0.6 seconds after a change to its data. An edit made elsewhere, for example in the right sidebar, does not redraw it. Fold and unfold the marker block to read the data again. ⓘ shows each button's help text.
- ▲ folds the marker block. Each button in the bar shows its job as a tooltip.

## Text that changes meaning in Logseq

Logseq reads some text as structure. Change it before you paste text into a data block:

| Text | Logseq makes | Write instead |
|---|---|---|
| `[[x]]` | a page link, and a new page | `x` |
| `#tag` after a space | a tag, and a new page | `＃tag` |
| `{{x}}` | a macro | `｛｛x}}` |
| `key:: value` | a block property | `key：: value` |
| a line that starts with `- ` | a new child block | `• ` |

Inline code in backticks keeps its text. Never paste passwords or tokens into a panel. Put a pointer to the file that holds them.

## Move an Obsidian console to Logseq

The Obsidian console is retired (2026-11-20), and every project panel is in Logseq now. If an old console note turns up, `scripts/console2logseq.py` turns it into the block tree, and makes the text changes in the table above:

```
python scripts/console2logseq.py <out.md> "<title> \`console-grid <shell> <runner>\`" "<buttons note>.md:data" "<console note>.md:page"
```

- `:data` reads a console-grid data note. The script skips the text before the first `##`.
- `:page` reads a console note with `button` blocks. The text before the first `##` becomes the tab 概览.
- `##` becomes a tab, `###` a subgroup, a `按钮` table or a `button` block a button, and a callout a card.
- The script skips cards whose title holds 登录信息, 编辑入口 or 按钮怎么用.
- A button that sends the selected text, the caret line or a pop-up form has no automatic Logseq version. The script writes it as a note that starts with 🔘. Rewrite a pop-up form button by hand as a form button (see "Form buttons"). Rewrite a button that sends the selected text or the caret line as a form button with one `Selection` field. Use `select` for a fixed list of values, and `text` with a pattern for a keyword. Use `free` for any text, such as a sentence or a prompt line. Move the lines that the user selected from, for example a list of sentences, under the `free` field as suggestions.

Read the output before you paste it. Then put it at the top of the project's page, and keep the page's other blocks below it. Close Logseq while a script edits a page file, or edit the page in Logseq.

## Check a panel

1. Run `python -I scripts/check-panel.py "<graph>/pages/<page>.md"`. It counts the buttons per tab, lists each key that is not a runner case, and parses the runner. It must exit 0.
2. Open the page and unfold the marker block. Each tab must show the buttons and cards that you expect.
3. Click one read-only button, for example a status key. A notification must show the runner's output.
4. Alt+click one button. The cursor must go to that button's own block. Do this once more with two large tabs unfolded, and make sure that only one panel shows.
5. Open each form button, and cancel it. The form must show the runner arguments that you expect.

If the panel shows `console-grid: add the tabs as child blocks of this block`, the marker block has no child with children. If nothing draws, restart Logseq: the script runs once for each window.
