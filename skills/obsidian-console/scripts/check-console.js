// Checks a console's notes with the view's own parser, without Obsidian running.
//
//   node check-console.js <vault>/_views/console-grid/view.js "<note>.md" <vault>/.obsidian/plugins/obsidian-shellcommands/data.json [<runner .ps1>]
//
// A grid data note: one line per group (tab) with button count, unknown actions and cards. With a runner
// (the project's run_for_obsidian_console.ps1), a non-link 动作 must be one of its keys; without one, a
// Shell commands alias. A note of Buttons-plugin blocks: every `type command` alias must be registered, and
// every obsidian://shell-commands link must name a registered command id and, with a runner, one of its
// keys. Exit 1 on any unknown action, a table row leaked into the cards, or nothing to check.
const fs = require('fs');

const [viewPath, dataPath, shellPath, runnerPath] = process.argv.slice(2);
if (!shellPath) {
  console.error('usage: node check-console.js <view.js> <note.md> <shellcommands data.json> [<runner .ps1>]');
  process.exit(2);
}
const view = fs.readFileSync(viewPath, 'utf8');
const parser = view.slice(view.indexOf('function isRow'), view.indexOf('function markBroken'));
const parseGroups = new Function(parser + '; return parseGroups;')();

const commands = JSON.parse(fs.readFileSync(shellPath, 'utf8')).shell_commands;
const aliases = new Set(commands.map((c) => c.alias));
const ids = new Set(commands.map((c) => c.id));
// A runner's keys: its `switch` cases (`'key' {`) or the values of a [ValidateSet(...)] on its parameter.
function runnerKeys(text) {
  const out = new Set([...text.matchAll(/^\s*'([^']+)'\s*\{/gm)].map((m) => m[1]));
  for (const m of text.matchAll(/\[ValidateSet\(([^)]*)\)\]/g)) {
    for (const v of m[1].matchAll(/'([^']+)'/g)) out.add(v[1]);
  }
  return out;
}
const keys = runnerPath ? runnerKeys(fs.readFileSync(runnerPath, 'utf8')) : null;
const isLink = (a) => /^(https?|file):/.test(a);
const known = (a) => isLink(a) || (keys ? keys.has(a) : aliases.has(a));

const note = fs.readFileSync(dataPath, 'utf8');
const groups = parseGroups(note);
let failed = false;
let checked = 0;
for (const [name, group] of Object.entries(groups)) {
  const unknown = group.buttons.filter((b) => !known(b.action)).map((b) => b.name);
  const leak = group.cards.split('\n').some((line) => line.trim().startsWith('|'));
  const cards = group.cards.split('\n').filter((line) => line.startsWith('> [!')).length;
  if (unknown.length || leak) failed = true;
  checked++;
  console.log(`${unknown.length || leak ? 'FAIL' : 'ok  '} ${name}: ${group.buttons.length} buttons, unknown=${JSON.stringify(unknown)}, tableLeak=${leak}, cards=${cards}`);
}

const blocks = [...note.matchAll(/```button\r?\n([\s\S]*?)```/g)].map((m) => m[1]);
if (blocks.length) {
  const bad = [];
  for (const b of blocks) {
    const name = (b.match(/^name (.+)$/m) || [, '?'])[1].trim();
    const action = (b.match(/^action (.+)$/m) || [, ''])[1].trim();
    const cmd = action.match(/^Shell commands: Execute: (.+)$/);
    const uri = action.match(/^obsidian:\/\/shell-commands\/\?(.+)$/);
    if (!cmd && !uri && !isLink(action)) bad.push(`${name}: unrecognised action "${action}"`);
    if (cmd && !aliases.has(cmd[1].trim())) bad.push(`${name}: alias "${cmd[1].trim()}"`);
    if (uri) {
      const q = new URLSearchParams(uri[1]);
      if (!ids.has(q.get('execute'))) bad.push(`${name}: command id "${q.get('execute')}"`);
      const key = q.get('_console_button');
      if (keys && key !== null && !keys.has(key)) bad.push(`${name}: key "${key}"`);
    }
  }
  if (bad.length) failed = true;
  checked++;
  console.log(`${bad.length ? 'FAIL' : 'ok  '} button blocks: ${blocks.length}, unknown=${JSON.stringify(bad)}`);
}
if (!checked) {
  console.log('no ## section holds a 按钮 table and no button blocks');
  failed = true;
}
process.exit(failed ? 1 : 0);
