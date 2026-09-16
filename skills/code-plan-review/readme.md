# code-plan-review — where the rules came from

One skill, one rule per kind of problem. Each rule in `SKILL.md` has a *write* side, a *prove* side and a *view* side; each incident below is told once, and the numbered "why" list at its end maps to the rule's bullets. This skill replaced three one-lesson skills (`scil-coding`, `scil-testing`, `scil-review`) on 2026-09-16 because every lesson touches all three phases and a rule costs less than a skill description.
一个 skill，一类问题一条规则。`SKILL.md` 里每条规则有*写*、*证*、*审*三面；每次事故在下面只讲一次，末尾编号的"为什么"对应规则的条目。本 skill 于 2026-09-16 取代了三个单课 skill（`scil-coding`、`scil-testing`、`scil-review`），因为每个教训都横跨三个阶段，而一条规则比一个 skill 的 description 便宜。

## Rule 1 — the `useBlocker` incident (2026-09-11, ThanksPorch) / 事故一

**Symptom.** On `/settings`, changing only the avatar and then refreshing produced the browser's "information you've entered may not be saved" prompt — although the photo was already in the database and R2.
**症状。** `/settings` 只改头像然后刷新，浏览器弹"你输入的信息可能未保存"——但头像早已存进数据库和 R2。

**Root cause.** The screen's own `beforeunload` handler was correctly gated on `hasUnsavedText`. But TanStack Router's `useBlocker`, used on the same screen for in-app navigation, registers its *own* `beforeunload` listener, and its option `enableBeforeUnload` defaults to `true` — arming the prompt for as long as a blocker is mounted, without consulting `shouldBlockFn`. So the prompt fired on every refresh; the avatar change was only where someone noticed.
**根因。** 页面自己的 `beforeunload` 处理器门控是对的。但同一页面用来拦应用内导航的 `useBlocker` 会注册它自己的监听器，选项 `enableBeforeUnload` 默认 `true`——只要 blocker 挂着就一律弹，根本不看 `shouldBlockFn`。所以每次刷新都弹，和头像无关。

**Spread.** The identical pairing existed on five screens (`settings`, `cards.new`, `offerings.new`, `offerings.$id`, `offering-edit-all-screen`), each commented "the same guard the full offering editor carries". All five had the bug.
**扩散。** 同样的组合在五个页面都有，每处注释都写"和 offering 编辑器同一套"。五处全错。

**Fix.** First pass: `enableBeforeUnload: false` on all five, keeping the own handler. Second pass, after comparing both designs in code: `enableBeforeUnload: () => <same predicate>` and the five hand-rolled effects deleted — one predicate for both exits.
**修法。** 第一版：五处都传 `enableBeforeUnload: false`，保留自写 handler。用代码对比两种设计后改为第二版：`enableBeforeUnload: () => <同一判断>`，删掉五个手写 effect——一个判断管两种离开。

**Why it was written** (→ *Write*):
**为什么写成这样**（→ *Write*）：

1. The options type has four fields; the code read two. → *Read the whole options type.*
2. The unread option defaulted to `true` and did something. → *Unset ≠ off.*
3. A DOM listener was written beside a hook that already handled the event. → *Same event, stop sign.*
4. The comment encoded a plain-DOM model ("the browser's to prompt for, all we can do is opt in") until it read as knowledge. → *A comment is a claim.*
5. The pairing was copied four times without an audit. → *The second copy is the audit.*
6. Two listeners both preventing was correct whenever dirty, so nobody saw it. → *Replace, don't add.*

**Why no test caught it** (→ *Prove*). The bug lived for months behind a green gate (typecheck, lint, 581 unit tests, the settings e2e file):
**为什么没测出来**（→ *Prove*）。门禁全绿，bug 活了好几个月：

1. Every test asked one direction — "does the prompt appear with a draft open?" — never "does it stay silent when clean?" → *Arms when dirty AND silent when clean.*
2. Every component suite stubbed the hook (`useBlocker: () => ({ status: "idle" })` in six files), so the router's listener never existed in jsdom. → *A stubbed hook is an absent library.*
3. Playwright's `page.reload()` does not fire `beforeunload`; the existing tests reloaded with dirty drafts and never saw a dialog. → *Probe what the harness bypasses.*

What was added: one e2e test (`porch-profile-edit.spec.ts`): untouched screen → no prompt; photo removed and confirmed → no prompt; name draft typed → prompt arms (positive control); Cancel → no prompt. Revert check run for real: fix undone → red on the first silence assertion; restored → green. Coverage stated as "probed on settings, four siblings verified by identical option shape".
加了一个 e2e 测试：未动→不弹；头像删除并确认→不弹；输入名字草稿→弹（正向对照）；Cancel→不弹。回退检查真跑了：回退→红，恢复→绿。覆盖如实说明。

**Why review passed it** (→ *View*). Five screens went through Claude, codex loops and manual passes without a question:
**评审为什么放过了**（→ *View*）。五处都过了评审，从没被质疑：

1. Nobody listed the unset options. → *List the unset options.*
2. The duplicate listener read as "belt and braces", not as "the library already does this". → *A hand-rolled listener for an event the library handles.*
3. The comment was reviewed as an explanation, not as a claim to verify. → *A comment describing library behaviour is a claim.*
4. "The same guard X carries" ended the inquiry. → *Has X been audited?*
5. The tests were one-sided and stubbed, and review did not ask for the other side. → *Where is the silence test?*
6. The symptom was reported on one screen and could have been fixed on one. → *One symptom, how many sites?*

The review round after the fix confirmed no `addEventListener("beforeunload")` remained; confirmed the function-form option sits in the hook's effect deps; found the thanks-card spec already said *"Leaving with nothing written SHALL simply leave, without a prompt"* — compliance, no MODIFIED delta; fixed one stale sentence in `AGENTS.md`. The design choice was settled by putting both versions in code side by side, not by argument.
修复后那轮评审确认没剩 `beforeunload` 监听器、函数形式的选项在 effect deps 里、规格本来就写了"没写东西离开不提醒"（所以不需要 MODIFIED）、改掉 `AGENTS.md` 一句过时的话。两种设计的取舍是把代码并排放出来定的。

## How to maintain / 怎么维护

A new kind of problem: a new `## Rule N` in `SKILL.md` (three sides) and a new incident section here. The same kind of problem: one more bullet under the existing rule, and the incident appended to its section. Never a new skill.
新的一类问题：`SKILL.md` 加一条 `## Rule N`（三面），这里加一节事故。同一类问题：在现有规则下加一条，事故追加到对应小节。永远不新建 skill。
