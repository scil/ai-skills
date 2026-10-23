// Dataview view: an OliveTin-style grid of buttons with switchable help text, optionally in tabs.
//
// In a console note, every group as a tab (`tabs: true`), a chosen list, or one group:
//   ```dataviewjs
//   await dv.view("_views/console-grid", { data: "<data note path>", tabs: true })
//   await dv.view("_views/console-grid", { data: "<data note path>", tabs: ["<group>", …] })
//   await dv.view("_views/console-grid", { data: "<data note path>", group: "<group>" })
//   ```
// In the data note, a group is a `## <group>` section (up to the next # or ## heading) that
// holds a Markdown table whose first header cell is 按钮:
//   | 按钮 | 动作 | 颜色 | 说明 |
//   |---|---|---|---|
//   | 🚀 Start all | 启动全部服务 | blue | `script.bat` → … |
// 动作 is a link (http, https, file), or, with a project runner, a key:
//   await dv.view("_views/console-grid", { data: "…", tabs: true, runner: "<alias>", confirmRunner: "<alias>" })
// A key is written into the Shell commands custom variable `_console_button`, then the runner command runs
// (the project's one `scripts\win\run_for_obsidian_console.ps1`); red, orange and yellow buttons use
// confirmRunner, which asks first. Without `runner`, 动作 is a Shell commands alias as before.
// 颜色 is blue | green | yellow | red | purple | orange or empty. 说明 is markdown; write | as \|.
// Everything else in the section (the callouts) is rendered under that group's buttons in tabs mode.
//
// Help visibility is one switch for the whole window (a body class); it and the open tab
// are remembered in localStorage, so Dataview's periodic re-render keeps them.

const SHOW_HELP_CLASS = 'console-grid-show-help';
const HELP_KEY = 'console-grid-show-help';
const SHELL_PREFIX = 'Shell commands: Execute: ';
const LINK = /^(https?|file):/;
const KEY_VARIABLE = '_console_button';
const CONFIRM_COLORS = new Set(['red', 'orange', 'yellow']);

// getVariables() returns a Set (Shell commands' VariableSet), not an array.
function shellVariable(name) {
  const plugin = app.plugins.plugins['obsidian-shellcommands'];
  const variables = plugin?.getVariables?.();
  return variables ? [...variables].find((v) => v.variable_name === name) : undefined;
}

function readStorage(key) {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

function writeStorage(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch {}
}

function setShowHelp(on) {
  document.body.classList.toggle(SHOW_HELP_CLASS, on);
  writeStorage(HELP_KEY, on ? '1' : '0');
}

function findCommand(name) {
  return Object.values(app.commands.commands).find((c) => c.name === name);
}

function isRow(line) {
  return line.trim().startsWith('|');
}

// Cells of one table row; `\|` is a literal pipe, as in Markdown tables.
function splitRow(line) {
  const row = line.trim().replace(/^\|/, '').replace(/(?<!\\)\|$/, '');
  const cells = [];
  let cell = '';
  for (let i = 0; i < row.length; i++) {
    if (row[i] === '\\' && row[i + 1] === '|') {
      cell += '|';
      i++;
    } else if (row[i] === '|') {
      cells.push(cell.trim());
      cell = '';
    } else {
      cell += row[i];
    }
  }
  cells.push(cell.trim());
  return cells;
}

// One group per `## ` section that contains a 按钮 table; the rest of the section is its cards.
function parseGroups(markdown) {
  const sections = [];
  let current = null;
  let inFence = false;
  for (const line of markdown.split(/\r?\n/)) {
    if (/^(```|~~~)/.test(line.trim())) inFence = !inFence;
    if (!inFence && /^#{1,2} /.test(line)) {
      current = line.startsWith('## ') ? { name: line.slice(3).trim(), lines: [] } : null;
      if (current) sections.push(current);
      continue;
    }
    if (current) current.lines.push(line);
  }

  const groups = {};
  for (const { name, lines } of sections) {
    const start = lines.findIndex(
      (line, i) => isRow(line) && splitRow(line)[0] === '按钮' && /^\s*\|?\s*:?-{3,}/.test(lines[i + 1] || ''),
    );
    if (start < 0) continue;
    let end = start + 2;
    while (end < lines.length && isRow(lines[end])) end++;
    const header = splitRow(lines[start]);
    const cell = (cells, column) => (header.indexOf(column) >= 0 ? cells[header.indexOf(column)] || '' : '');
    groups[name] = {
      buttons: lines.slice(start + 2, end).map(splitRow).map((cells) => ({
        name: cell(cells, '按钮'),
        action: cell(cells, '动作'),
        color: cell(cells, '颜色'),
        help: cell(cells, '说明'),
      })),
      cards: [...lines.slice(0, start), ...lines.slice(end)].join('\n').trim(),
    };
  }
  return groups;
}

function markBroken(tile, message) {
  tile.addClass('is-broken');
  tile.createDiv({ cls: 'console-grid-broken', text: message });
}

function addHelpToggle(parent) {
  const toggle = parent.createEl('button', {
    cls: 'console-grid-toggle',
    text: 'ⓘ 说明',
    attr: { 'aria-label': 'Show or hide help text' },
  });
  toggle.onclick = () => setShowHelp(!document.body.classList.contains(SHOW_HELP_CLASS));
}

function renderTiles(parent, buttons) {
  const tiles = parent.createDiv('console-grid-tiles');
  for (const spec of buttons) {
    const tile = tiles.createDiv('console-grid-tile');
    if (spec.color) tile.dataset.color = spec.color;
    const button = tile.createEl('button', { cls: 'console-grid-button', text: spec.name || '(no name)' });
    if (spec.help) dv.el('div', spec.help, { container: tile, cls: 'console-grid-help' });

    if (!spec.action) {
      markBroken(tile, '动作 is empty');
      continue;
    }
    if (LINK.test(spec.action)) {
      button.onclick = () => window.open(spec.action);
      continue;
    }
    const runner = input.runner
      ? (CONFIRM_COLORS.has(spec.color) && input.confirmRunner ? input.confirmRunner : input.runner)
      : null;
    const name = SHELL_PREFIX + (runner || spec.action);
    button.onclick = async () => {
      try {
        const command = findCommand(name);
        if (!command) {
          if (!tile.hasClass('is-broken')) markBroken(tile, `Command "${name}" not found`);
          return;
        }
        if (runner) {
          const variable = shellVariable(KEY_VARIABLE);
          if (!variable) {
            if (!tile.hasClass('is-broken')) markBroken(tile, `Custom variable "${KEY_VARIABLE}" not found`);
            return;
          }
          await variable.setValue(spec.action, 'manual');
        }
        app.commands.executeCommandById(command.id);
      } catch (error) {
        // An async click handler's error is otherwise swallowed: the button would just do nothing.
        if (!tile.hasClass('is-broken')) markBroken(tile, `console-grid: ${error?.message || error}`);
      }
    };
    if (!findCommand(name)) markBroken(tile, `Command "${name}" not found`);
  }
}

document.body.classList.toggle(SHOW_HELP_CLASS, readStorage(HELP_KEY) === '1');

const page = dv.page(input.data);
if (!page) {
  dv.container.createDiv({ cls: 'console-grid-error', text: `console-grid: note "${input.data}" not found` });
  return;
}
const groups = parseGroups((await dv.io.load(page.file.path)) || '');
const names = input.tabs === true ? Object.keys(groups) : input.tabs || [input.group];
const missing = names.filter((name) => !groups[name]);
if (!names.length || missing.length) {
  dv.container.createDiv({
    cls: 'console-grid-error',
    text: `console-grid: no 按钮 table under ${missing.map((m) => `"## ${m}"`).join(', ') || 'any ## heading'} in "${input.data}"`,
  });
  return;
}

const root = dv.container.createDiv('console-grid');

if (!input.tabs) {
  addHelpToggle(root.createDiv('console-grid-head'));
  renderTiles(root, groups[names[0]].buttons);
  return;
}

const tabKey = `console-grid-tab:${input.data}`;
const bar = root.createDiv('console-grid-tabbar');
const tabs = {};
const panels = {};

function select(name) {
  writeStorage(tabKey, name);
  for (const n of names) {
    tabs[n].toggleClass('is-active', n === name);
    panels[n].hidden = n !== name;
  }
}

for (const name of names) {
  tabs[name] = bar.createEl('button', { cls: 'console-grid-tab', text: name });
  tabs[name].onclick = () => select(name);
}
addHelpToggle(bar);

for (const name of names) {
  const panel = root.createDiv('console-grid-panel');
  panels[name] = panel;
  renderTiles(panel, groups[name].buttons);
  if (groups[name].cards) dv.el('div', groups[name].cards, { container: panel, cls: 'console-grid-cards' });
}

const saved = readStorage(tabKey);
select(names.includes(saved) ? saved : names[0]);
