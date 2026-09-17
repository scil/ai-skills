# code-plan-review — where the rules came from

One skill, one rule per kind of problem, one batch file per mechanism. Each rule in `references/<batch>.md` has a *tell*, a *write*, a *prove* and a *view* side; each incident below is told once, and the numbered "why" list at its end maps to the rule's bullets. This skill replaced three one-lesson skills (`scil-coding`, `scil-testing`, `scil-review`) on 2026-09-16 because every lesson touches all three phases and a rule costs less than a skill description. Later the same day the rules were split into batch files so a plan can be reviewed one batch per fresh context: the context that wrote a plan grades it poorly, and a subagent given one small batch file reads the rules it needs and nothing else. The *tell* side was added at the same time — a rule that only knows what wrong code looks like cannot be applied to a plan.
一个 skill，一类问题一条规则，一种机制一个批次文件。`references/<batch>.md` 里每条规则有*征兆*、*写*、*证*、*审*四面；每次事故在下面只讲一次，末尾编号的"为什么"对应规则的条目。本 skill 于 2026-09-16 取代了三个单课 skill，因为每个教训都横跨三个阶段，而一条规则比一个 skill 的 description 便宜。同日稍后把规则拆成批次文件，让计划可以一批一个新上下文地审：写计划的上下文给自己打分打不好，而拿到一个小批次文件的子代理只读它需要的规则。*征兆*一面同时加入——只知道错误代码长什么样的规则，用不到计划上。

Rules 2 to 9 were harvested on 2026-09-16 from one project's always-loaded contract, where they stood as repeated-trap guards; the general mechanism moved here, the project's bindings (type names, gate functions, test files) stayed in that contract. Where the contract recorded a dated instance, it is below; where it did not, the section says so.
规则 2 到 9 于 2026-09-16 从一个项目的常驻契约中收割，它们在那里是重复陷阱的守卫；通用机制搬到这里，项目绑定（类型名、门函数、测试文件）留在契约里。契约记录了事故的，写在下面；没有的，该节会说明。

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

**Why the plan would not have shown it** (→ *Tell*, added 2026-09-16). The design named the blocker and the "same guard as the editor"; a reviewer holding the Tell would have asked which event family the hook already owns before any code existed.
**为什么计划阶段没看出来**（→ *Tell*，2026-09-16 补）。设计里写了 blocker 和"和编辑器同一套守卫"；拿着征兆的审查者在写代码之前就会问这个 hook 已经接管了哪一类事件。

## Rule 2 — the `decide` / `ask` deadlock (ThanksPorch; date in that repository's history) / 事故二

Two request paths, one that decides on an access request and one that creates an ask, each touched the same two tables and took the row locks in opposite orders; under load they deadlocked. The change's design document had a Risks section listing five domain risks — privacy, leakage, expiry — and no mechanism trap; the lock order was never stated anywhere before code. The contract also records the surrounding rules the same guard carried: a cap checked in code rather than in the write, a uniqueness conflict treated as "the row is usable", a two-call test in one process that never overlapped, and helpers that took the pool inside a transaction until a type-level test forbade it.
两条请求路径，一条判定访问请求，一条创建 ask，各自触及同两张表，行锁顺序相反；负载下死锁了。该变更的设计文档有风险一节，列了五条领域风险——隐私、泄露、过期——机制陷阱一条没有；加锁顺序在写代码前从未在任何地方写下。契约还记录了同一守卫携带的相关规则：上限在代码里检查而不在写语句里、唯一性冲突被当成"这行可用"、单进程两次调用的测试从未真正重叠、以及事务内传入连接池的 helper，直到类型级测试禁止为止。

Why (→ *Tell*): a sequence diagram of the two paths would have shown two participants writing the same two tables with no order stated. (→ *Write*): one lock order, written beside the tables. (→ *Prove*): the two-connection test. (→ *View*): "which order do these two paths lock, and where is it written?"
为什么（→ *Tell*）：两条路径的时序图会显示两个参与者写同两张表而顺序未定。（→ *Write*）：一个加锁顺序，写在表旁边。（→ *Prove*）：双连接测试。（→ *View*）："这两条路径按什么顺序加锁，写在哪？"

## Rule 3 — invalidate is not replace (harvested from the contract; no single dated incident) / 规则三

Screens that mutated and then invalidated showed the old value until the refetch returned, and kept it when the refetch failed; entries the server derived from the write (counts, lists) went stale too. The guard's rule: write the cache from the mutation response first, then invalidate, and list the derived entries.
先变更再失效的页面在重新获取返回前显示旧值，重新获取失败时永远显示旧值；服务端由该写入派生的条目（计数、列表）也过期了。守卫的规则：先用变更响应写缓存，再失效，并列出派生条目。

## Rule 4 — the guest-claim branch moved client-side (ThanksPorch, `/api/guest-claim`) / 事故四

An endpoint's "attributed or claim" branch was chosen on the client from its session store; on first paint the store was unresolved, and it was cached for whoever had asked last. The fix was one endpoint that reads the cookie and reports which branch it took.
一个端点的"归属还是认领"分支由客户端根据会话存储选择；首次绘制时存储尚未解析，且缓存的是上一个询问者。修法是一个端点读 cookie 并报告它走了哪个分支。

## Rule 5 — naming a recipient from the one-grant budget (ThanksPorch) / 事故五

A card's recipient was inferred from "there is exactly one grant on this path", which held on the path the code was written for and not on the author-admission path that also reached it; the inferred value was write-once, so the wrong route could not be corrected afterwards.
卡片的收件人是从"这条路径上恰好只有一个授权"推断出来的，这在代码原本服务的路径上成立，在同样到达此处的作者准入路径上不成立；推断出的值只写一次，错误路径事后无法纠正。

## Rule 6 — distrust everything crossing a trust boundary (harvested from the contract; no single dated incident) / 规则六

Client-supplied ids were used after an existence check as if existence were permission. The contract routes every such read through one visibility gate and names it; the general rule keeps only "existence is not permission" and "name the gate in the plan".
客户端提供的 id 在存在性检查后被当作已授权使用。契约把每个这样的读取都路由到一个可见性门函数并点名；通用规则只保留"存在不等于允许"和"在计划里点名门函数"。

## Rule 7 — a screen frozen on the missing value (ThanksPorch) / 事故七

`useState(someProp)` seeded a draft from a session value on a screen that could mount before the session resolved; the draft kept the empty seed. Derive during render, or key the draft to the resolved value.
`useState(someProp)` 在一个可能先于会话解析而挂载的页面上用会话值初始化草稿；草稿一直保持空的初始值。渲染时派生，或把草稿键到已解析的值上。

## Rule 8 — text fields and a photo sharing one observer (ThanksPorch, `settings.tsx`) / 事故八

A settings screen saved text fields and a photo through one mutation observer; the photo upload could still be in flight when a text save resolved, and the screen reported whichever finished last. The text fields now share one observer, the photo has its own, with a shared scope id.
设置页面通过一个变更观察者保存文本字段和头像；文本保存完成时头像上传可能仍在进行，页面报告的是最后完成的那个。现在文本字段共用一个观察者，头像单独一个，共享一个 scope id。

## Rule 9 — `avatarApplied` (ThanksPorch, `porch.updateMine`) / 事故九

A profile update applied the text and could fail to apply the avatar without failing the call; "the call succeeded" was shown as "your change was saved". The response now carries whether the avatar applied, and the client renders that.
一次资料更新会应用文本，而头像可能应用失败但调用不失败；"调用成功"被显示为"你的更改已保存"。响应现在携带头像是否已应用，客户端据此渲染。

## How to maintain / 怎么维护

A new kind of problem: a new `## Rule N` with four sides in the mechanism's batch file, and a new incident section here. The same kind of problem: one more bullet under the existing rule's side that failed, and the incident appended to its section. A new mechanism: a new batch file and one row in the router's table. Never a new skill. Every batch runs on every plan and states its own applicability first; nothing in the plan selects batches, so a new batch needs no registration beyond its table row.
新的一类问题：在所属机制的批次文件里加一条四面的 `## Rule N`，这里加一节事故。同一类问题：在现有规则失守的那一面下加一条，事故追加到对应小节。新机制：新批次文件、路由表加一行。永远不新建 skill。每个批次对每份计划都会运行并先声明自己是否适用；计划里没有任何东西选择批次，所以新批次除了表里那一行不需要别的登记。
