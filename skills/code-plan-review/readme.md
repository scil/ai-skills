# code-plan-review — where the questions came from

One skill, one catalog: lettered scenarios, numbered sub-scenarios, one question per kind of problem. The skill was created on 2026-09-16 as rules harvested from incidents — each rule with three gates and four sides, grouped into batch files, reviewed one batch per subagent against tables the plan's author had to fill. On 2026-10-02 it was reshaped into what it is now: a catalog of scenarios and the questions a reviewer asks of a plan, walked in one context, with possibility and suggestion in place of verdict and proof. The incident sections below are unchanged: they are where the questions came from, and the table after the vocabulary says which question each rule became. Where a section says *Rule N*, *Tell*, *Write*, *Prove*, *View*, *batch* or *intermediate*, it describes the shape the skill had then.
一个 skill，一份目录：字母编号的场景、数字编号的子场景、一类问题一个问题。本 skill 于 2026-09-16 以"从事故收割的规则"创建——每条规则三道门四个面，按批次文件分组，一个批次一个子代理，对着方案作者必须先填好的表来审。2026-10-02 改成现在的样子：一份场景目录，每个场景下是审查者对方案要问的问题，在一个上下文里走完，用"可能性 + 建议"取代"判定 + 证明"。下面的事故小节原样保留：它们是问题的来处，词汇表后面的对照表写明每条规则变成了哪个问题。小节里出现 *Rule N*、*Tell*、*Write*、*Prove*、*View*、*batch*、*intermediate* 这些词时，说的是 skill 当时的形状。

## Why it was reshaped / 为什么改

The machinery had grown past its findings. A plan could not be reviewed until its author had produced a stack line, a diagram, pseudocode and up to a dozen tables, five of them kept as living files per repository; a batch returned `INCOMPLETE` rather than an opinion; eleven subagents read eleven rule files to produce verdict lines a merge then reconciled; and the proof side demanded, at the plan stage, an assertion that cannot exist before code does. The findings that mattered came from a reader with the right question in mind, and that reader does not need a filled table to say "this may happen here, and this is what I would change". So: questions, not rules with sides; possibility and suggestion, not verdict and proof; one reader, in the context already open; material only the author can supply asked for once, and declined without stopping the review. What left this skill has an owner elsewhere: proving a fix is `fix-bugs` phase 4; reviewing the code is `codex-review`. The one thing the subagents bought — a grader that did not write the plan — survives as a single sentence: run the review in a session that did not write the plan where you can.
机器的成本已经超过了它的发现。一份方案要先补技术栈行、图、伪代码和最多十几张表，其中五张还是每个仓库常驻维护的文件，才能开始审；批次返回的是 `INCOMPLETE` 而不是意见；十一个子代理读十一个规则文件，输出判定行，再由合并步骤对账；"证"那一面还在方案阶段就要一条代码存在之前不可能存在的断言。真正有用的发现，来自一个心里带着正确问题的读者，而这个读者不需要填好的表就能说"这里可能出事，我会这样改"。于是：问题，而不是带面的规则；可能性和建议，而不是判定和证明；一个读者，在已经打开的上下文里；只有作者能提供的材料请示一次，拒绝了也不停下评审。离开本 skill 的东西在别处有主：证明修复是 `fix-bugs` 第 4 阶段；审代码是 `codex-review`。子代理换来的唯一一样东西——没写过方案的评分者——留成一句话：可以的话，在没写过这份方案的会话里跑评审。

## Vocabulary / 名词

**Scenario / 场景, sub-scenario / 子场景.** The moment in a change that raises a family of questions: *the client sends a request › after the response returns*. Scenarios are lettered (A–I), sub-scenarios numbered within them (A3), questions numbered within those (A3.1). New questions are appended; numbers never shift, so an old report still points at the question it cited.
一次变更里引出一组问题的那个时刻：*客户端发送请求 › 响应返回后*。场景用字母（A–I），子场景在场景内编号（A3），问题在子场景内编号（A3.1）。新问题追加在末尾；编号永不移动，旧报告引用的还是同一个问题。

**Question / 问题.** One kind of problem, written as the shape it takes in a plan, then *Suggest:* the change. Asked whether or not the plan already guards against it; the guard makes it unlikely, not absent.
一类问题，写成它在方案里的形状，然后是 *Suggest:* 该怎么改。不管方案是否已经防了它都要问；防住了是"不太可能"，不是"不存在"。

**Possibility / 可能性.** *Likely*, *possible* or *cannot tell*, each with its why, as a row of the report; *unlikely* questions are listed by number under the scenario's table with the guard that makes them so.
*likely*、*possible*、*cannot tell*，各带理由，占报告一行；*unlikely* 的问题按编号列在该场景表格下面的一行里，附上让它不太可能的那个防护。

**Material / 材料.** What only the author can supply: which paths write a table, a lock order, an arrival estimate, which exits end a journey on purpose, which spec rule governs. Asked for once, in one message; declining it turns the dependent questions into *cannot tell* and nothing else. Files the plan names and greps over the tree are reading, not material, and need no asking.
只有作者能提供的东西：哪些路径写这张表、加锁顺序、到达率估计、哪些出口是有意结束旅程的、哪条 spec 规则管着。一条消息里请示一次；拒绝只会让依赖它的问题变成 *cannot tell*，没有别的后果。方案点名的文件和对代码树的 grep 是阅读，不是材料，不需要请示。

**Outside the catalog / 目录之外.** A problem no question names; one line in the report, and a candidate for the next harvest.
没有任何问题点到的毛病；报告里一行，下一次收割的候选。

## Where each rule went / 每条规则去了哪

| Then | Now |
|---|---|
| Rule 1 — use the API you are already holding | H1.1–H1.5 |
| Rule 2 — the statement that writes decides | B1.1–B1.5, B2.1, B2.2, B2.4 |
| Rule 3 — invalidate is not replace | A2.4, A3.5–A3.7, D1.3 |
| Rule 4 — the server decides who the caller is | C1.1–C1.3 |
| Rule 5 — an inference is valid only with its warrant | C2.1–C2.3 |
| Rule 6 — distrust what crosses a trust boundary | C3.1–C3.3 |
| Rule 7 — pick the hook by who owns the value | D1.1, D1.2 |
| Rule 8 — one observer per save | A1.5 |
| Rule 9 — a step that may fail alone reports it | A3.8, B4.1 |
| Rule 10 — a concept must exist before it is guarded | G1.1, G2.1–G2.3, G3.1, G4.1 |
| Rule 11 — a dependent read waits for the commit | A3.10, B4.2, B4.3 |
| Rule 12 — reads that must agree share one snapshot | B5.1, B5.2 |
| Rule 13 — every lock answers for its arrival rate | B3.1–B3.5 |
| Rule 14 — subscribe, then read once | D3.1–D3.3 |
| Rule 15 — a failed read is not an empty answer | A3.9, D4.1, D4.2 |
| Rule 16 — a refill is computed on a baseline | A2.1, A3.1, A3.2 |
| Rule 17 — judge against the value that will be stored | A1.3, A1.4, D2.1–D2.4 |
| Rule 18 — a withheld outcome is indistinguishable | C4.1, C4.2 |
| Rule 19 — one policy, one place | I1.1, I1.2 |
| Rule 20 — a rule lives on the writing statement | I2.1, I2.2 |
| Rule 21 — a promise travels into the write | I3.1, I3.2 |
| Rule 22 — a journey completes from every exit | E1.1–E1.3, E2.1, E2.2 |
| Rule 23 — a branch covers every state | F1.1–F1.4, F2.1 |
| Rule 24 — search before you write an interaction | H2.1–H2.3 |
| Rule 25 — search the modules that exist | H3.1 |
| Rule 26 — one site is the owner | H3.2 |
| Rule 27 — an interface answers the question | H3.3, H3.4 |
| Principle 7 — one class fix for the second row of a shape | I2.2, and the suggestion rule in "What to report" |
| Principle 6 — a proof goes red when the mitigation is reverted | left this skill; `fix-bugs` phase 4 |
| The diff pass and the confirmation round | left this skill; `codex-review` |
| The five living intermediates | left this skill; E1.1 and C2.1 say "grep" where they said "the living file" |
| New on 2026-10-02, from the reshaping request | A1.1, A1.2, A2.2, A2.3, A3.3, A3.4 |
| New on 2026-10-03, from what the repost and porch-browsing reviews missed | A3.11, D3.4, G4.2 |

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

## Rule 10 — seven traps that looked like races (ThanksPorch traps 1, 2, 4, 11, 16, 19, 20) / 规则十

The project's most expensive type, and none of the seven looked alike until "what was missing" was listed. The edge carried no provenance, so "a card hands out at most N edges" could not be written down (1). "Is there a row" was asked of an entity with three states, and a unique conflict was read as "reuse it" (2); "is there an active edge" read `blocked` as "no relationship" when blocked is a stronger one (4). Both caps governed answering, and resolving — a read anyone could trigger — wrote rows nothing bounded (11). Removing write-once turned every path that could produce "a name with no seat" into a path that loses the name; the design said that state was "only constructible by hand" and an ordinary parameter of the create call reached it (16). Provenance's meaning was never pinned (19), and the holder was derived from edges while a column held it (20).
该项目最贵的一类；七个坑列出"缺的是什么"之前互不相像。边没有来路，"一张卡最多发 N 条边"连写都写不出来（1）。对一个有三种状态的实体问"有没有一行"，唯一冲突被读成"可以复用"（2）；"有没有 active 边"把 `blocked` 读成"没关系"，而拉黑是更强的关系（4）。两个上限都管答题，而解析——任何人都能触发的读——写的行没有任何东西约束（11）。取消 write-once 后，每条能产生"有名字没席位"的路都成了丢名字的路；design 说那个状态"只能手工构造"，create 调用的一个普通参数就到了（16）。来路的语义没定（19）；持有者从边推导，而列里就有它（20）。

Three of the seven were first filed under concurrency because a concurrency test found them and `FOR UPDATE` fixed them; run single-threaded, all three still fail. That is the incident behind the classification step in Harvest and the last View question in db-concurrency: the fix at hand is not the classification. (→ *Where*: a rule over an entity with states, a public write, a derived holder, a relaxed constraint. → *Asks for*: the state ledger with a "counts" column, the cap-owner table, the path list per removed constraint.) The "cannot happen" half of trap 16 went to Rule 5, whose route table is that enumeration.
七个里有三个先被归到并发，因为是并发测试发现、`FOR UPDATE` 修好的；单线程跑三个照样错。这就是收割里那一步分类和 db-concurrency 最后一个审问背后的事故：顺手的修法不是分类。坑 16 的"不可能发生"那一半归入规则 5，它的路由表就是那份枚举。

## Rules 11, 12 — the two safety cells not yet hit (ThanksPorch, hypothetical, with one real fix) / 规则十一、十二

Order violation: registration completes, the redirect to the porch fires, and the redemption's transaction has not committed; the next screen says "you are not in" and a refresh fixes it. Not hit; the real half is `guest-claim.ts`, whose comment records the order decision — grant first, then record, because the old order marked the claim redeemed before an edge that could still be refused. Inconsistent read: the seat list is several reads that must agree; under the default isolation a seating landing mid-read returned the old holder and the new one, and `cardAccess.seat` became the one procedure in the codebase that sets `REPEATABLE READ` — a snapshot, not a lock, because it writes nothing. Fixing the server did not fix the screen, which still issues two round trips; that sentence is Rule 12's last View question.
顺序违背：注册完成、跳转门廊已发生、兑换事务还没提交；下一屏说"你还没进来"，刷新就好。没踩到；真实的那一半是 `guest-claim.ts`，注释记录了顺序决定——先授予再记录，因为旧顺序在一条可能被拒的边之前就把认领标成已兑换。不一致读：席位列表是几次必须吻合的读；默认隔离下一次落座落在读的中间，就同时返回旧持有者和新持有者，`cardAccess.seat` 成了全库唯一设 `REPEATABLE READ` 的过程——是快照不是锁，因为它一个字都不写。修好服务端没修好屏幕，它仍然发两次往返；那句话是规则 12 最后一个审问。

## Rules 13, 14 — the liveness half, and why the rule shape had to change (ThanksPorch trap 11, hypothetical) / 规则十三、十四

Trap 11 had an exact plan — lock the share on every resolve, count, sweep — and rejected it in the words "that would be laying a queue in front of a flood". The notes name that sentence: starvation. Hundreds of scans a minute queue on one row; once arrivals exceed what the lock serves, waiting diverges; every waiter holds a pool connection and requests unrelated to that card start failing; `lock_timeout` defaults to no timeout and closing the browser does not cancel the wait. No test would have warned: nothing errors, nothing deadlocks, locally there is one scanner. The livelock half is Rule 2's own fix bouncing back — two evictions written as "zero rows → retry", colliding forever. Lost wakeup: a "still waiting" page that flips only on a push, and the author admits before the subscription is live.
坑 11 有一个精确方案——每次解析锁 share、计数、清理——被一句"那是在洪水前面排一条队"否掉。笔记给了这句话名字：饥饿。每分钟几百次扫码在一行上排队；到达一旦超过锁能服务的速度，等待就发散；每个等待者攥着一条池连接，和这张卡无关的请求开始失败；`lock_timeout` 默认不超时，关掉浏览器也不取消等待。没有测试会报警：不报错、不死锁、本地只有一个扫码者。活锁那一半是规则 2 自己的修法反弹——两个驱逐都写成"0 行就重试"，永远撞在一起。丢失唤醒：只靠推送翻转的"还在等"页面，作者在订阅建立之前就放行了。

The skill could not hold these until its Prove side admitted a non-test proof: a liveness failure has no moment at which an assertion turns red. The batch marks its rules *liveness*, the proof cell carries the argument (arrival against service) and the metric (p99 lock wait, pool occupancy), and the merge returns a liveness row that names a test as its proof (once; then Unresolved). (→ *Asks for*: the lock × arrival table, foreign-key locks included; the retry policy; the subscribe-then-read order on the diagram.)
在"证"一面接受非测试的证明之前，skill 装不下这两条：活性失败没有哪一刻断言会红。该批次把规则标为 *liveness*，proof 格写论证（到达对服务）和指标（p99 锁等待、池占用），合并时丢掉拿测试当证明的活性行。

## Rule 15 — a failed read painted as "nothing here" (ThanksPorch traps 15, 21) / 规则十五

`fetch` rejects only on network errors, so the `try/catch` around the guest-redeem call treated a 500 as done and the degraded path said nothing (15). The card management screen had no `isError` branch, so `!isPending && !data` rendered the empty state, and an author who could no longer manage her cards was told she had none (21). Rule 3's three screen states had no error row; it has four now, and this rule owns the branch table.
`fetch` 只在网络错误时 reject，所以 guest-redeem 调用外面的 `try/catch` 把 500 当成完成，降级路径一声不吭（15）。卡片管理页没有 `isError` 分支，`!isPending && !data` 画成了空态，一个管不了自己卡片的作者被告知她一张卡都没有（21）。规则 3 的三种屏幕状态没有错误那一行；现在四种，分支表归这条规则。

Rule 3 also took two bullets from trap 13 — the previous reader's porch flashed to the next reader; the first fix compared `dataUpdatedAt` against a browser-recorded time (two clocks) and was wrong, the second put a generation into the key — and the boundary sentence from the seat review, where nine of thirteen rounds were one stale key each until "rows of this screen come from the response; derived entries converge by invalidation" was written down.
规则 3 还从坑 13 拿了两条——上一个读者的门廊闪给了下一个读者；第一版拿 `dataUpdatedAt` 和浏览器时间比（两个时钟），错了，第二版把代数放进 key——以及席位评审的那句边界：十三轮里九轮各报一个过期 key，直到写下"这个屏幕自己的行从响应来，派生条目靠失效收敛"。

## Rules 16, 17 — the way back, and the value that will be stored (ThanksPorch, the edit-and-save section) / 规则十六、十七

The clobbering write in the first is the screen's own success response: the request leaves with "A", the user types "B" during the 1.2-second round trip, the response lands `{ intro: "A" }` and `setState(response)` swallows the B. Nothing failed. Two fatal spellings of the guard were recorded — a token read when the response arrives, and a token incremented from an effect — and one confusion: a disabled submit button stops the request going twice, not a late response landing. The second is the whole tap-to-edit section: a schema trims and collapses, so every check on the raw draft (dirty, valid, equal, Save enabled) answers about a value that will not be stored; the four gates — fetched, no write in flight, parses, differs — had an order, the editor could open before gate 1, `reset` wiped a draft opened during gate 2, a greyed Save gave no reason, an unparseable draft read as "unchanged" so Back discarded it, and the leave dialog was wired to the wrong editor.
前者盖掉输入的那次写是屏幕自己的成功响应：请求带着 "A" 出去，用户在 1.2 秒往返里打了 "B"，响应带回 `{ intro: "A" }`，`setState(response)` 把 B 吞了。什么都没失败。记录了守卫的两种致命写法——响应到达时才读 token、在 effect 里递增 token——和一个混淆：禁用提交按钮防的是请求发两次，不是响应回来太晚。后者是整个 tap-to-edit 那一节：schema 会 trim 和折叠，所以对原始草稿做的每个判断（脏、合法、相等、Save 可用）答的都是一个不会被存的值；四道闸——已取回、无在途写、能解析、有差异——有顺序，编辑器能在闸 1 之前打开，`reset` 清掉闸 2 期间打开的草稿，灰掉的 Save 不给理由，解析不过的草稿被读成"没变"于是 Back 丢掉它，离开对话框接错了编辑器。

## Rule 18 — a refusal that could be recognised (ThanksPorch traps 5, 6) / 规则十八

The landing page said why the ask had not succeeded (5); then "declined" and "still waiting" had to look identical, and the leak was not a field but a constraint: a unique index with a status condition let a declined person ask again, which is itself the answer (6). The fix touched three places at once — the constraint without a status condition, one `{ state: "waiting" }` on every path with the reason in a support-only column, one UI sentence — and the price, that a mistaken decline cannot be undone by asking, was written into the spec. Rule 6 already had the one phrase "not found and not yours are the same answer"; the table came from here.
落地页说出了求进门为什么没成（5）；然后"被拒"和"还在等"必须长得一样，而漏的不是字段是约束：带状态条件的唯一索引让被拒的人能再问一次，这本身就是答案（6）。修法同时动三处——不带状态条件的约束、每条路径同一个 `{ state: "waiting" }` 且原因只进排查列、一句 UI——代价（误拒不能靠再问撤销）写进了规格。规则 6 本来只有一句"not found 和 not yours 是同一个答案"；那张表从这里来。

## Rules 19, 20, 21 — one truth, three costumes (ThanksPorch traps 7, 8, 12; 9; 17) / 规则十九、二十、二十一

Two implementations: the landing page lost the author's `wordmark` because it painted the card with its own code (7), found only by putting two screenshots side by side; a prop named `recipientName` received a composed sentence (8); the client `trim()`med where the server normalized, so its own equality check disagreed with what was stored (12). Scattered rule: "someone who already left a note is not asked again" was reported in four costumes — the page's own state, an `orderId` obtained before the note, a correct answer in another browser merged at sign-in, a pending claim opened before the decline — and patched three times before it moved onto `grantEdgeThroughShare`, the one statement that creates an edge, with the admission exemption and its reason beside it (9). Promise drift: the confirmation said "take it from Sam", the click evicted Bob; three layers each lost the same promise — the server never checked who the author believed was holding it, the client recomputed `expectedHolderUserId` from fresh data at click and dismantled its own guard, and the sentence rendered after the whole list so on a phone it scrolled away while the button stayed (17). It is the point in the intersection of two families: two copies, and one state with several writers.
两份实现：落地页用自己的代码画卡，把作者选的 `wordmark` 弄丢了（7），把两边截图并排才发现；叫 `recipientName` 的 prop 收到了一整句话（8）；客户端 `trim()` 而服务端归一化，自己的相等判断和存进去的值对不上（12）。规则分散："留过言的人不再被问"换了四身衣服报出来——页面自身状态、留言前拿到的 `orderId`、另一个浏览器答对后登录合并、拒绝前开好的待领取——打了三次补丁才挪到 `grantEdgeThroughShare` 这条唯一建边的语句上，放行豁免和理由写在旁边（9）。承诺走样：确认语说"从 Sam 手里拿走"，点下去驱逐的是 Bob；三层各丢了一次同一个承诺——服务端从没查作者以为谁在拿着、客户端点击时从最新数据重算 `expectedHolderUserId` 拆了自己的守卫、那句话排在整个列表之后于是手机上它滚走了按钮还在（17）。它是两族交集里的那个点：两份副本，且一份状态多个写者。

The batch reads across layers on purpose — a promise is made in a component and kept in a `WHERE` — which no existing batch did. Principle 7 (one class fix for the second row of a shape) is trap 9's four rounds and trap 13's nine, written as a merge rule. Principle 6 (a proof is the assertion that goes red when the mitigation is reverted) is trap 3's `Promise.all` test, green with and without the fix, promoted from Rule 1's Prove to every row. The confirmation round in the Diff pass is trap 22: a spec that described something the implementation could never do survived every round that read code and fell to the one that read the spec.
这个批次故意跨层——承诺在组件里许下、在 `WHERE` 里兑现——现有批次没有一个这样做。原则 7（同一形状第二行只给一个类修复）是坑 9 的四轮和坑 13 的九轮写成合并规则。原则 6（证明是回退缓解后会红的那条断言）是坑 3 那个加不加修复都绿的 `Promise.all` 测试，从规则 1 的"证"提升到每一行。Diff pass 的确认轮是坑 22：一条实现永远做不到的规格熬过了每一轮读代码的评审，倒在唯一一轮读规格的。

## Rule 22 — the share that stopped at the signed-out link (2026-09-18, ThanksPorch `/onboarding`) / 规则二十二

The journey: scan a card → sign in → first run → back to the card. The share token rides in the URL and every hop forwards it: `signin` puts it in the OAuth `callbackURL`, `/` carries it on, `PorchSetup` returns to the card "from EVERY way out of the form, including the two shortcuts" — that sentence is in the component, written after an earlier round lost the token on a shortcut. Then first run moved to its own route, `/onboarding`, which had one more exit the component could not see: the signed-out fallback, `<Link to="/signin">` with no `search`. The token stopped there; nothing failed, the person just arrived at an empty porch with no way back to a URL they never held. The component had enumerated its own exits; the route wrapping it had not enumerated the route's. Caught by a codex round reading the diff, not by any batch, because no batch owned the space between screens.
旅程：扫卡 → 登录 → 首次运行 → 回到卡片。分享 token 在 URL 里，每一跳都转发它：`signin` 把它放进 OAuth `callbackURL`，`/` 接着带，`PorchSetup` 从"表单的每一个出口，包括两个快捷方式"都回到卡片——这句话写在组件里，是更早一轮在快捷方式上丢过 token 之后加的。然后首次运行搬到自己的路由 `/onboarding`，它多了一个组件看不见的出口：未登录兜底 `<Link to="/signin">`，没带 `search`。token 到此为止；什么都没失败，人只是落在一个空门廊上，回不到一个他从未持有过的 URL。组件枚举了自己的出口；包着它的路由没枚举路由的。是读 diff 的 codex 轮抓到的，不是任何批次，因为没有批次拥有屏幕之间的那段空间。

It was first filed under single-source-of-truth — "each hop is a copy, one copy was dropped" — and that was wrong: that batch's property is two copies that both exist and drift, and its defence is deleting the second; here nothing drifted, the edge was never made. The fix at hand (add `search` to the link) is not the classification, and neither is the tempting alternative (keep the token in the session): both are Write-side options. The three-question test ended at "the batch of the boundary it crossed", and the boundary between screens had no batch, so this one was opened, with two Tells taken from the same change where no incident occurred but the question was live: a conditional redirect that must `replace` so Back does not re-enter it, and the mutual pair (`/` sends porch-less to `/onboarding`, `/onboarding` sends porch-owner to `/`) whose conditions must leave a failed read to neither. Later the same day the rule's Asks for gained the navigation graph as a living intermediate, because the missing exit was on a route the change did not write: a table built per change lists the change's exits, and the route that hid the exit is by definition one that already existed.
起初归进了 single-source-of-truth——"每一跳一份副本，丢了一份"——归错了：那个批次的属性是两份都存在的副本会漂移，防御是删掉第二份；这里什么都没漂移，那条边根本没建。手边的修法（给链接加 `search`）不是分类依据，那个诱人的替代方案（把 token 放进 session）也不是：两者都是"写"一侧的选项。三问走到"它跨越的边界所在批次"，而屏幕之间的边界没有批次，于是开了这个批次；另从同一次改动里取了两条没出事但问题真实存在的 Tell：条件重定向必须 `replace`，否则 Back 会再进一次；互相重定向的一对（`/` 把没门廊的送去 `/onboarding`，`/onboarding` 把有门廊的送回 `/`）的条件必须让读取失败两边都不走。同日稍后，这条规则的 Asks for 加入了作为常驻中间物的导航图，因为丢失的出口在变更没写的路由上：按变更建的表列的是这次变更的出口，而藏着出口的那条路由按定义早已存在。

## Rule 23 — the failed read that fell into the creation form (2026-09-18, ThanksPorch `/onboarding`) / 规则二十三

Same change as Rule 22. The first-run route read `porch.getMine`, whose `data` has three states — `undefined` (not known: pending *or failed*), `null` (the server said none), an object — and guarded with `if (isPending || porch) return <Loading/>` before falling through to the setup form. A failed read is `undefined` with `isPending` false: neither guard held, and it took the branch written for `null`, which on this route is a **creation form** — an invitation to make a second porch to somebody whose first could not be read. The home route it was copied from had a retry branch; the copy dropped it. Rule 15's Tell (`!isPending && !data → empty` with no `isError` branch) matches word for word and codex cited it; it was not applied because a creation form did not read as an "empty state", and because no batch ran.
和规则 22 同一次改动。首次运行路由读 `porch.getMine`，它的 `data` 有三种状态——`undefined`（不知道：还在请求*或者失败了*）、`null`（服务器说没有）、对象——守卫写成 `if (isPending || porch) return <Loading/>` 然后落到建 porch 的表单。读取失败是 `undefined` 且 `isPending` 为 false：两个守卫都不拦，走进了为 `null` 写的分支，而这条路由上那个分支是**创建表单**——对一个第一个 porch 都读不出来的人发出"再建一个"的邀请。它抄形状的首页有重试分支；抄的时候丢了。规则 15 的 Tell（`!isPending && !data → empty` 且无 `isError` 分支）一字不差地匹配，codex 也引用了它；没被用上，是因为创建表单在作者眼里不算"空态"，也因为没有批次跑。

Filed three ways before it settled. First as four bullets on Rule 15 — right mechanism, too narrow: the same collapse is `if (user)` over `null | undefined | User`, a `switch` on a status with no `default`, `count ? :` where `0` is real, `hasX = !!x` before the branch. Then as a rule in domain-model — the classifier's "is a state defined wrongly?" said yes, but the state was already in the type and no column would ever hold it; the batch's evidence is the schema, and this rule's evidence is the type. So a new batch, branch-completeness, and with it a family the skill had not named: **logic error**, seen from the code and its types alone. The rule's two halves are split on purpose: whether every state has a branch is lint-able (`switch-exhaustiveness-check`, `strict-boolean-expressions`), and what the residue's landing branch *does* — shows, offers a write, performs one, decides access — is not, which is why the batch is a review step and not only a lint line. The proof is "assert the form's field is absent", not "assert Retry is present": the second stays green when both render.
定了三次才定下来。先是给规则 15 加四条——机制对，太窄：同样的坍缩还有 `null | undefined | User` 上的 `if (user)`、没有 `default` 的状态 `switch`、`0` 有意义时的 `count ? :`、分支前的 `hasX = !!x`。然后放进 domain-model——分类器的"状态定义错了？"答是，但那个状态本来就在类型里，永远不会有一列去装它；那个批次的证据是 schema，这条规则的证据是类型。于是新开批次 branch-completeness，并随之命名了 skill 还没有的一个族：**逻辑错误**，只看代码和类型就能看出来。规则的两半有意分开：每个状态有没有分支可以交给 lint（`switch-exhaustiveness-check`、`strict-boolean-expressions`）；剩余状态落到的分支*干什么*——显示、提供写入、执行写入、决定权限——lint 做不了，这就是批次作为评审步骤而不只是一行 lint 配置的理由。证明写"断言表单字段不存在"而不是"断言重试存在"：两个都渲染时后者仍是绿的。

## Rule 24 — search before you write an interaction (2026-09-18, a stated requirement, not an incident) / 规则二十四

No dated incident; the rule was asked for as a standing requirement on frontend work and filed in the batch whose ledger it extends. Rule 1 begins once a library is already in the plan and asks whether the hand-written listener beside it is redundant; Rule 24 begins one step earlier and asks whether the hand-written listener should exist at all. Its intermediate is a search ledger with two tiers in the order the requirement gave them — the stack and the dependency tree first (the framework, every package in the manifest, the transitive ones in the lockfile, checked in their docs or `.d.ts`), then the ecosystem by a web search on the concern's name — and a disposition per concern: adopt, reject with a number or a missing feature, or hand-write with an edge-case checklist that names what the library would have handled for free. It sits under misplaced responsibility (who owns a concern a library already handles, or a mature one would), in the library-hooks-listeners batch, because its "which of the two owns it" row is Rule 1's row asked before the second of the two is written. The Rule 1 incident is the nearest relative: five screens hand-rolled `beforeunload` beside a router that already owned it, and a search of the router's options type would have found it before the first copy. One change to the prompts came with it: a View side may now ask the reviewer for one web search by the concern's name, recorded on a `SEARCHED` line, so that a ledger whose tier 2 omits an obvious maintained candidate is a finding against the ledger — and the reviewer never runs the search *for* an author whose ledger left tier 2 blank, because that is the empty cell the rule exists to show.
没有日期事故；这条是 2026-09-18 对前端工作提出的常设要求，归入它所扩展的那本账所在的批次。规则 1 从库已经在计划里开始，问旁边手写的监听器是否多余；规则 24 早一步，问那个手写监听器该不该存在。它的中间物是两层搜索账，顺序照要求给的——先技术栈和依赖树（框架、manifest 里每个包、lockfile 里的传递依赖，查它们的文档或 `.d.ts`），再按关注点名字上网搜生态——每个关注点一个处置：采用、以数字或缺失功能为由拒绝、或手写并附一张列出库本来会白给你什么的边角用例清单。它归在职责错位（某个库已经处理、或某个成熟库能处理的关注点归谁）下、library-hooks-listeners 批次里，因为它"两者谁拥有"这一行就是规则 1 的那一行，只是在第二者写出来之前先问。规则 1 的事故是最近的亲戚：五个页面在已经拥有 `beforeunload` 的路由旁边手写了它，在第一份副本之前搜一遍路由的选项类型就能找到。随之改了提示词一处：View 面现在可以要求审查者按关注点名字做一次网络搜索，记在 `SEARCHED` 行上，这样第二层漏掉一个明显在维护的候选就是对账本的发现——而审查者永远不替第二层空着的作者去搜，因为那个空格正是这条规则要显出来的东西。

## Rules 25, 26, 27 — module depth (2026-09-19, ThanksPorch, incident plus a stated requirement) / 规则二十五、二十六、二十七

**Symptom.** A form's title/description fields were given a minimum length (reject "jjj" as a title, not just reject empty). Raising the floor from "non-empty" to a real number surfaced four independent copies of "is this long enough": the Zod schema (correct, the intended owner), a composer route's own `.trim().length` comparison, a tap-to-edit editor's own comparison, and an "is this added language version complete" check that had gone stale and still accepted a too-short value — silently disabling Publish with no on-screen reason.
**症状。** 给标题/详情字段加最小长度（拒绝"jjj"当标题，不只是拒绝空）。把门槛从"非空"提到一个真实数字后，暴露出"够不够长"这件事有四份独立实现：Zod schema（正确，本该是唯一 owner）、composer 路由自己的 `.trim().length` 比较、点按编辑器自己的比较，以及一个"新增语言版本是否完整"的检查——已经读的是旧规则，还在接受长度不够的值，让 Publish 静默失效、界面上却没有任何解释。

**Root cause.** The shared policy (`offeringContentPolicy`) exported its NUMBERS but not the DECISION that reads them. Every consumer that needed "is this valid" wrote its own comparison against the numbers instead of calling one function that already encoded the schema's own trim/normalize/min/max — the numbers were a shared constant; the predicate built from them was reimplemented four times.
**根因。** 共享策略（`offeringContentPolicy`）导出了数字，没导出读这些数字的判断。每个需要"这个合法吗"答案的调用方，都自己拼了一遍对数字的比较，而不是调用一个已经封装了 schema 自身 trim/normalize/min/max 的函数——数字是共享常量，用数字做判断的谓词却被重新实现了四遍。

**Spread.** Caught by a code review before merge, not in production: four sites — three application files plus a fifth, dormant DB-layer schema that hardcoded its own numbers and would have accepted the same too-short values through any future caller that used it instead of the tRPC path.
**扩散。** 在合并前的代码评审中发现，不是线上事故：四处——三个应用文件，加上第五处、休眠中的 DB 层 schema，它硬编码了自己的一套数字，将来任何绕开 tRPC 路径、直接用它的调用者都会接受同样长度不够的值。

**Fix.** Extracted the decision itself — `isOfferingTitleValid`, `isOfferingDescriptionValid`, and a richer `offeringTitleProblem`/`offeringDescriptionProblem` pair for callers that need to know which bound failed — backed by the same Zod schema the server parses with. Every consumer now calls one of these instead of comparing against the raw policy fields.
**修法。** 把判断本身提炼出来——`isOfferingTitleValid`、`isOfferingDescriptionValid`，以及给需要知道"具体哪个边界没过"的调用方用的 `offeringTitleProblem`/`offeringDescriptionProblem`——背后都是服务端解析用的同一个 Zod schema。所有调用方现在都调用这几个函数之一，不再直接比较原始策略字段。

**Widened by a stated requirement.** The incident's own shape — one policy, one predicate, several copies — was already Rule 19's territory (a value validated on two sides). What Rule 19 does not cover is what a design review asked for afterwards: (a) a decision (not just a rendered/parsed value) reimplemented instead of asked of its owner, at any granularity — a function, hook, component, schema, or package, not only client/server value duplication; (b) the same duplication arising within one plan's own new code, before any history exists to search; and (c) a module that is the only implementation of something and is still shallow — its interface making the caller assemble, order, or already know what the module could have owned itself — which has nothing to do with duplication at all. Three rules, one new batch, `module-depth.md`.
**被一条明确要求放宽了范围。** 这次事故本身的形状——一个策略、一个谓词、好几份拷贝——已经是规则 19 的地盘（一个值在两侧被校验）。规则 19 没覆盖到的，是设计评审之后提出的要求：(a) 一个**决定**（不只是渲染/解析出来的**值**）被重新实现、而不是问它的 owner——在任意颗粒度上，函数、hook、组件、schema、包，不只是 client/server 的值重复；(b) 同样的重复出现在**同一份计划自己的新代码**内部，根本还没有历史可搜；(c) 一个模块即使是某件事的**唯一**实现，接口依然可以是浅的——让调用者自己组装、自己排序、或者调用前就得先知道一个相关问题的答案——这和有没有重复毫无关系。三条规则，一个新批次 `module-depth.md`。

**Why it was written** (→ *Write*):
**为什么写成这样**（→ *Write*）：

1. A shared constant was exported; the decision built from it was not, so nothing stopped a fifth copy from appearing tomorrow. → Rule 25: export the question as a function, and search for it before writing a new one.
   共享常量导出了，用它做的判断没有导出，所以明天冒出第五份拷贝没有任何阻拦。→ 规则 25：把问题本身导出成函数，写新的之前先搜。
2. The four copies included three that were all new-ish application code written close together, not one old and one new — duplication that a "search the past" rule alone would not have caught if none of the copies pre-dated the others by much. → Rule 26: tally every site for one decision regardless of which was written first, and require an owner once the tally exceeds one.
   四份拷贝里有三份都是差不多同时写的新应用代码，不是"一份老的一份新的"——如果几份拷贝谁都不比谁老多少，光靠"搜过去"这条规则未必能抓到这种重复。→ 规则 26：不管先后，把同一个决定的所有站点汇总计数，数量一旦超过一就要求指定一个 owner。
3. Even the corrected version — one schema, one predicate function — could still have been shallow (e.g., requiring each caller to pass in the already-trimmed value AND the raw value AND which field it was) without any second copy existing anywhere. Nothing in Rules 19–26 would have caught that shape. → Rule 27: judge a new module's interface on its own terms, independent of whether anything else duplicates it.
   哪怕改完之后——一个 schema、一个判断函数——它依然可能是浅的（比如要求每个调用方同时传入已 trim 的值、原始值、和字段名），而且完全不需要存在第二份拷贝。规则 19 到 26 都抓不住这种形状。→ 规则 27：单独评判一个新模块的接口本身，跟别处有没有重复无关。

**Family.** 25 sits in misplaced responsibility, beside Rules 1 and 24 (who owns this: an existing internal module, or new code) — its batch differs from theirs because its evidence (a codebase-wide grep ledger) is not scoped to library/hook options the way Rule 24's ecosystem search is. 26 sits in multiplicity, beside Rules 19–21 (how many sites answer this) — its batch differs because its site tally spans old and new sites by design, where Rule 19's is about a value's rendered/parsed form specifically. 27 fits none of the five families cleanly: it depends on neither ownership, copy count, ordering, nor domain state — on how much a caller must learn versus how much the module hides. It is filed here, naming a sixth family, **interface depth**.
**归族。** 25 属于职责错位，和规则 1、24 同族（这该由仓库里已有的模块拥有，还是这份新代码拥有）——批次不同是因为它的证据（全仓库 grep 账本）不像规则 24 的生态搜索那样只框在库/hook 的选项上。26 属于多副本，和规则 19–21 同族（同一个问题有几个站点在回答）——批次不同是因为它的站点计数按设计横跨新旧，而规则 19 专指一个值的渲染/解析形式。27 五个族都套不上：既不依赖归属，也不依赖副本数、先后或领域状态——依赖的是调用者要学多少、模块藏了多少。它在这里立案，命名了第六个族：**接口深度**。

## A3.11, D3.4, G4.2 — what three reviews missed (2026-10-03, ThanksPorch `add-offering-repost`, `add-porch-browsing`) / 三轮评审漏掉的

The catalog was walked three times in one session — twice over a design that lets a porch owner's family members repost their offerings, once over the porch page that design turned out to need — and in each case it was the session that had written the design. The rows that mattered came from opening files, not from reading prose: the request path's lock order, an "already asked" check still keyed per offer, a selectable audience scope, a composer's local draft. Three problems got past every pass and were found later, each by something other than the review.
同一会话里把目录走了三遍——两遍审一份让门廊主人的家人转发其 offering 的设计，一遍审那份设计后来发现离不开的门廊页——每次都是写了设计的那个会话在审。有用的行都来自打开文件，不是读文字：请求路径的加锁顺序、仍按 offer 计数的"已经问过"、一个可选的受众范围、发布页的本地草稿。有三个问题穿过了每一轮，后来分别被评审以外的东西发现。

**G4.2 — found by implementation.** The design routed a request made through an owner-handled repost to the owner, with the reposter's handoff places. Writing the schema showed `fk_request_confirmed_handoff_location_provider`: a confirmed place must belong to the request's provider, so the owner could never confirm the reposter's place. G4.1 asks about a constraint being *removed*; nothing asked whether constraints that *stay* hold for the rows a new path writes. The founder settled it — whoever handles owns the places — and the model became cleaner (such a request is a request on the owner's own offer).
**G4.2 —— 实现时发现。** 设计把经"主人处理"的转发提出的请求路由给主人，交接地点用转发者的。写 schema 时看到 `fk_request_confirmed_handoff_location_provider`：确认的地点必须属于请求的处理人，所以主人永远确认不了转发者的地点。G4.1 问的是约束被*去掉*；没有问题问*留下的*约束对新路径写的行是否成立。创始人拍板——谁处理就用谁的地点——模型反而更干净了（这种请求就是主人自己 offer 上的请求）。

**A3.11 — found in the browser.** A porch page refusing a non-porchmate answered NOT_FOUND in 300 ms and drew the refusal about seven seconds later: React Query retries every error three times with backoff by default, and nothing in the plan said a refusal is an answer. The offering page had carried the same delay unnoticed.
**A3.11 —— 浏览器里发现。** 门廊页拒绝一个非 porchmate，服务端 300 ms 就回了 NOT_FOUND，拒绝画面约七秒后才出现：React Query 默认对每个错误带退避重试三次，计划里没有任何一句说拒绝本身就是答案。offering 页一直带着同样的延迟，没人注意。

**D3.4 — found by a diff review.** To stop a porch page cached for one account being drawn for the next, every answer carried `viewerUserId` and a mismatch triggered a re-ask. If the second answer still disagreed (a tab whose session store lagged a sign-in in another tab), the effect never fired again and the page waited forever. Its first fix storm-fetched in a test, because the effect depended on a function whose identity changed each render; `useEffectEvent`, keyed on the disagreement alone, settled it, with a visible retry after the one re-ask.
**D3.4 —— diff 评审发现。** 为了不把为一个账号缓存的门廊页画给下一个账号，每个回答都带 `viewerUserId`，不一致就重新请求。若第二个回答仍不一致（会话存储落后于另一个标签页登录的那个标签页），effect 不会再触发，页面永远等着。第一版修法在测试里狂发请求，因为 effect 依赖了一个每次渲染身份都变的函数；改成只以"不一致"为键的 `useEffectEvent`，重新请求一次后给出可见的重试，才定下来。

Two further gaps were proposed and not adopted: "is there any way in to the new thing" (the repost was unreachable because no page browsed a porch) and "a list calls a per-item loader" (the porch page would have read ~5 times per offering). Both were real in this change, and both were left out of the catalog by the owner's choice. And one usage lesson, not a question: all three passes ran in the authoring session, which the skill already advises against — the authoring session judged its own blind spots *unlikely*.
另有两个缺口被提出、没有采纳："新东西到底有没有入口"（转发到达不了，因为没有浏览门廊的页面）和"列表逐项调用加载器"（门廊页每个 offering 要读约 5 次）。在这次改动里两者都真实存在，按所有者的选择没有写进目录。还有一条用法教训，不是问题：三轮都在写设计的会话里跑，skill 本来就劝过别这样——写设计的会话会把自己的盲区判成 *unlikely*。

## J, G4.3, and the report's shape — the first delegated review (2026-10-04, ThanksPorch `add-request-conversation`) / J、G4.3 与报告的形状——第一次委托评审

The design gave owner and Porchmate a conversation about one thing, and reworked the request lifecycle around it. For the first time the authoring session followed the advice above and delegated the review to an agent that had not written the design. It paid: the first pass raised eighteen likely rows, all real — a mutation response written over a full cached DTO (A3.5), a value read before the transaction and written after it (B1.1), a conditional update missing its state (B1.5), an event and its line ordered by a random uuid (G1.1). The second pass, over the resolutions, raised three more. Three lessons became catalog entries or rules.
设计给主人和 Porchmate 一个围绕一件东西的会话，并围绕它改造了请求的生命周期。写设计的会话第一次照上面的建议，把评审委托给一个没写设计的 agent。这次值了：第一轮提出十八条 likely，全都是真的——变更返回值覆盖了缓存里的完整 DTO（A3.5）、事务前读的值在事务里写（B1.1）、条件更新漏了状态（B1.5）、事件和它的那句话按随机 uuid 排序（G1.1）。第二轮审处理结果，又提出三条。三条教训变成了目录条目或规则。

**J — a state that changes because time passed.** The founder asked that a loan close on its own seven days after the borrower said it was back. The author recommended deriving it at read time, the review did not question it — no scenario asked who writes a state the clock changes — and the author found the hole alone: derived "closed" was invisible to the one-live-request unique index, the "already out with someone" check and the refusal to take a thing down while a request is live. The thing would read as closed and stay live to every write. The founder then chose a reminder over an auto-close. Scenario J asks who makes the change, what happens *at* the deadline with no scheduler, and which clock decides.
**J —— 因时间流逝而改变的状态。** 创始人要求借用方说已归还七天后自动结束。作者建议读取时推导，评审没有质疑——没有场景问"时钟改变的状态由谁写入"——是作者自己发现的漏洞：推导出的"已结束"对"每人一条进行中请求"的唯一索引、"已经借给别人"的检查、"有进行中请求时不能下架"都不可见。东西看着关了，对每一次写入却还活着。创始人随后选择了提醒而不是自动结束。场景 J 问：谁来做这个改变、没有调度器时截止那一刻会发生什么、由哪个时钟决定。

**G4.3 — the reverse of G4.2.** The first pass asked G4.2 of every table the new paths write and found the fixtures that insert requests directly. It did not ask the reverse: the resolutions added `ck_request_return_report_fulfilled`, and "It's free again" (`resource.markAvailable`), in another router, completes a request with its own update and would have tripped it on any loan the borrower had reported back. The second pass found it. G4.3 asks every existing writer of a table to meet a constraint the plan adds.
**G4.3 —— G4.2 的反方向。** 第一轮对新路径写的每张表问了 G4.2，找出了直接插入请求的测试夹具。没有问反方向：处理结果加了 `ck_request_return_report_fulfilled`，而另一个 router 里的"It's free again"（`resource.markAvailable`）用自己的 update 完成请求，借用方报告过归还的借用会撞上它。第二轮才发现。G4.3 要求一张表的每个现有写入方都满足计划新加的约束。

**The report's shape.** Four changes, each from friction in this run. *Delegated mode*: the skill said "ask the author once" and "no subagents", the OpenSpec schema said "a session that did not write the design" — a delegated agent cannot ask anyone, and improvised a *Decisions for the owner* section; that section and *The model, restated* (which the schema, not the skill, had asked for) are now the skill's own. *Unspecified*: "likely" covered both "the plan describes the failing shape" and "the plan is silent", which put eighteen rows in one bucket; silence has its own label now, held to the same bar. *Most severe*: five rows ranked by what the failure costs, so a long report has a first page. *A second pass*: the schema asked for one and the skill did not say what it does; its most useful finding here was that the author had appended "D15 wins where the text differs" and left the old text standing — two copies of one truth — so the second pass now checks that every resolution reached every place the old decision was stated, and `references/openspec.md` says to resolve in place.
**报告的形状。** 四处改动，各来自这次运行的一处摩擦。*委托模式*：skill 说"问作者一次""不用子代理"，OpenSpec schema 说"由没写设计的会话来审"——委托的 agent 没人可问，只好临时加了一节 *Decisions for the owner*；这一节和 *The model, restated*（原本是 schema 要求的，不是 skill）现在归 skill 自己。*unspecified*：likely 同时装着"计划描述了会失败的形状"和"计划没说"，十八行挤在一个桶里；"没说"现在有自己的标签，门槛相同。*Most severe*：按失败代价排出五行，长报告有了第一页。*第二轮*：schema 要求了，skill 没说它做什么；这次它最有用的发现是作者追加了"文字不一致处以 D15 为准"，旧文字却原样留着——同一事实两份副本——所以第二轮现在要检查每条处理是否落到了旧决策出现过的每一处，`references/openspec.md` 也写明就地修改。

## The acceptance run (2026-09-16) / 验收运行

The batch layout was proven on the card-access-requests design of 2026-08-28 with the reviewable-plan sections added and no lock order stated: the db-concurrency batch returned the `decide`/`ask` lock order as its first blocking row, with the mitigation the shipped fix used. Two things were harvested. Every batch had filled full rows for one spec-versus-plan mismatch outside its rules, so the prompt now routes such findings to one `OUT-OF-BATCH` line and the merge dedupes them. And two of the batch's rows were reached by reading "a rule the spec states that no write enforces", which was not a Tell; it is now.
批次布局在 2026-08-28 的 card-access-requests 设计上验证：补上可审计划的章节、不写加锁顺序后，db-concurrency 批次的第一条阻塞行就是 `decide`/`ask` 的加锁顺序，缓解措施与已上线修复一致。收割两条：每个批次都为同一个规则外的 spec 与计划不一致填了整行，所以提示词现在把这类发现归为一行 `OUT-OF-BATCH`，由合并去重；该批次有两行是靠"spec 陈述而无写语句强制的规则"这种读法得出的，它当时不是 Tell，现在是了。

## The review of the skill itself (2026-09-16, later) / 对 skill 本身的评审

A second reader reviewed the skill's text, not a plan, and found that the rules had absorbed the incidents' fixes as if they were the properties — and that the pipeline could lose a real finding on the way to the merge. Eight corrections, in the order of their cost:
第二位读者审的是 skill 的文本而不是某份计划，发现规则把事故当时的修法当成了属性本身——而且流水线可能在合并前弄丢真发现。八处更正，按代价排序：

1. Rule 2 listed `INSERT … WHERE NOT EXISTS` beside the conditional `UPDATE`; it does not belong there — an insert has no row to lock, so two READ COMMITTED transactions both see absence and both insert; the guard is the unique constraint. Rule 13 said a conditional write "does not wait"; it waits like any other, holds the row to the end of its transaction, and its service time is lock to commit, short only when it is the last statement.
2. Rule 8's scope id "serialises writes on the server"; it is a client-side queue. Cross-client order is Rule 2's `WHERE`.
3. The merge dropped rows with no anchor or no proof. A row is now returned to its batch once and then listed under Unresolved; Principle 8 keeps Unresolved apart from Accepted, so a review cannot become clean by filing.
4. The prompt read only the files the plan named while the View sides of Rules 2, 5, 19 and 20 said "grep the tree" — a caller the plan omitted escaped by construction. The read scope is now the named files plus the batch's own greps, recorded on `SEARCHED` lines.
5. The confirmation round had two outcomes, satisfied or `UNIMPLEMENTABLE`, so a scenario nobody implemented was filed against the spec. Four now — and `MISSING` only after reading the existing files the diff touches, because a diff shows changed lines and an unchanged helper may already satisfy the scenario.
6. Rule 4 prescribed "one endpoint" where the property was "the server decides from credentials on whichever endpoint"; Rule 13 prescribed "sweep later" where the spec might demand an exact cap. Both Write sides now state the property first. That is the maintenance rule below.
7. Rule 21 captured the snapshot "at the click" while its own test required the value the sentence had shown; the moment is the confirmation's opening.
8. The diff pass reused a prompt that returns `INCOMPLETE` while forbidding it, and assumed a plan. Three prompts now, and the plan is an optional input.

What the acceptance run above could not have shown: every case in it was a known bug found. None of these eight would fail a true-positive run; six of them make a correct alternative implementation into a false finding, and two lose a true one. The cases in [`evals/cases.md`](evals/cases.md) exist for that reason — half of them are correct code that must come back clean.
上面的验收运行看不出这些：它的每个用例都是"已知 bug 被找到"。八条里没有一条会让真阳性用例失败；六条会把正确的替代实现报成假阳性，两条会丢掉真阳性。[`evals/cases.md`](evals/cases.md) 里的用例就是为此——一半是必须判 clean 的正确代码。

## How to maintain / 怎么维护

An incident becomes a question, not a rule. Find the moment in the change at which a reviewer holding the right question would have raised it; that moment is the sub-scenario. Append one numbered line there: the shape the problem takes in a plan, then *Suggest:* the change. Write the suggestion as the property the spec needs, with the incident's fix as one way to reach it — a suggestion that carries only the fix turns the next correct alternative into a likely row, which is what the 2026-09-16 review found in Rules 4 and 13 ("one endpoint" where the property was "the server decides on whichever endpoint"; "sweep later" where the spec might demand an exact cap). A moment no sub-scenario covers gets a new sub-scenario; a mechanism no scenario covers gets a new lettered scenario. Numbers are appended and never shifted. Never a new skill. Tell the story once here, dated, and add a row to the table above if the incident retires or splits a question. The old sorting questions still help find the scenario: a bug that survives serialization is G; a moment you can point at is B1 or B2; "still nothing" is B3 or D3; two copies is I; who decides is C; where the person ends up is E; the code and its types alone is F; a library or module that already owns it is H; what one screen holds is D; what one request does on its way out and back is A; a clock moved and nobody acted is J.
事故变成问题，不是规则。找到变更里那个时刻——手里握着正确问题的审查者会在这里提出它——那个时刻就是子场景。在那里追加一行编号：问题在方案里的形状，然后 *Suggest:* 该怎么改。建议写成 spec 要求的属性，事故当时的修法只是达到它的一种方式——只写修法的建议会把下一个正确的替代实现报成 likely，这正是 2026-09-16 的评审在规则 4 和 13 里发现的（属性是"无论打到哪个端点都由服务端决定"却写成"一个端点"；spec 可能要求精确上限却写成"事后清理"）。没有子场景覆盖的时刻新开子场景；没有场景覆盖的机制新开一个字母场景。编号只追加、不移动。永远不新建 skill。事故在这里讲一次、写上日期；若事故让某个问题退役或拆分，在上面的对照表里加一行。旧的分类三问仍然能帮你找场景：序列化后 bug 还在是 G；指得出那一刻是 B1 或 B2；"一直没发生"是 B3 或 D3；两份副本是 I；谁来决定是 C；人最终到哪是 E；只看代码和类型是 F；库或模块已经拥有它是 H；一个页面持有什么是 D；一次请求来回路上做了什么是 A；时钟动了而没人行动是 J。
