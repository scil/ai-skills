// Checks a console's data note with the view's own parser, without Obsidian running.
//
//   node check-console.js <vault>/_views/console-grid/view.js "<data note>.md" <vault>/.obsidian/plugins/obsidian-shellcommands/data.json
//
// Prints one line per group (tab): button count, unknown aliases, cards found. Exit 1 when any
// alias is unknown, a table row leaked into the cards, or no group was found.
const fs = require('fs');

const [viewPath, dataPath, shellPath] = process.argv.slice(2);
if (!shellPath) {
  console.error('usage: node check-console.js <view.js> <data note.md> <shellcommands data.json>');
  process.exit(2);
}
const view = fs.readFileSync(viewPath, 'utf8');
const parser = view.slice(view.indexOf('function isRow'), view.indexOf('function markBroken'));
const parseGroups = new Function(parser + '; return parseGroups;')();

const aliases = new Set(JSON.parse(fs.readFileSync(shellPath, 'utf8')).shell_commands.map((c) => c.alias));
const groups = parseGroups(fs.readFileSync(dataPath, 'utf8'));
let failed = Object.keys(groups).length === 0;
if (failed) console.log('no ## section holds a 按钮 table');
for (const [name, group] of Object.entries(groups)) {
  const unknown = group.buttons.filter((b) => !/^(https?|file):/.test(b.action) && !aliases.has(b.action)).map((b) => b.name);
  const leak = group.cards.split('\n').some((line) => line.trim().startsWith('|'));
  const cards = group.cards.split('\n').filter((line) => line.startsWith('> [!')).length;
  if (unknown.length || leak) failed = true;
  console.log(`${unknown.length || leak ? 'FAIL' : 'ok  '} ${name}: ${group.buttons.length} buttons, unknown=${JSON.stringify(unknown)}, tableLeak=${leak}, cards=${cards}`);
}
process.exit(failed ? 1 : 0);
