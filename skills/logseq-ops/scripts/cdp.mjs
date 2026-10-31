// usage: node cdp.mjs "<js expression>"
// Runs the expression in the Logseq main page through the local debug port 9333 (see SKILL.md, "Inspect a running Logseq").
const list = await (await fetch('http://127.0.0.1:9333/json')).json();
const page = list.find((p) => p.type === 'page' && p.url.includes('electron.html'));
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
ws.addEventListener('message', (m) => {
  const d = JSON.parse(m.data);
  if (d.id !== 1) return;
  const r = d.result?.result;
  console.log(d.result?.exceptionDetails ? 'EXC ' + JSON.stringify(d.result.exceptionDetails.exception?.description) : (r?.value !== undefined ? JSON.stringify(r.value, null, 1) : r?.description));
  ws.close();
});
ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: process.argv[2], awaitPromise: true, returnByValue: true } }));
