# code-plan-review — where the rules came from

One skill, one rule per kind of problem, one batch file per mechanism. Each rule in `references/<batch>.md` has a *tell*, a *write*, a *prove* and a *view* side; each incident below is told once, and the numbered "why" list at its end maps to the rule's bullets. This skill replaced three one-lesson skills (`scil-coding`, `scil-testing`, `scil-review`) on 2026-09-16 because every lesson touches all three phases and a rule costs less than a skill description. Later the same day the rules were split into batch files so a plan can be reviewed one batch per fresh context: the context that wrote a plan grades it poorly, and a subagent given one small batch file reads the rules it needs and nothing else. The *tell* side was added at the same time — a rule that only knows what wrong code looks like cannot be applied to a plan.
一个 skill，一类问题一条规则，一种机制一个批次文件。`references/<batch>.md` 里每条规则有*征兆*、*写*、*证*、*审*四面；每次事故在下面只讲一次，末尾编号的"为什么"对应规则的条目。本 skill 于 2026-09-16 取代了三个单课 skill，因为每个教训都横跨三个阶段，而一条规则比一个 skill 的 description 便宜。同日稍后把规则拆成批次文件，让计划可以一批一个新上下文地审：写计划的上下文给自己打分打不好，而拿到一个小批次文件的子代理只读它需要的规则。*征兆*一面同时加入——只知道错误代码长什么样的规则，用不到计划上。

Rules 2 to 9 were harvested on 2026-09-16 from one project's always-loaded contract, where they stood as repeated-trap guards; the general mechanism moved here, the project's bindings (type names, gate functions, test files) stayed in that contract. Where the contract recorded a dated instance, it is below; where it did not, the section says so.
规则 2 到 9 于 2026-09-16 从一个项目的常驻契约中收割，它们在那里是重复陷阱的守卫；通用机制搬到这里，项目绑定（类型名、门函数、测试文件）留在契约里。契约记录了事故的，写在下面；没有的，该节会说明。

Rules 10 to 21, three new batches and Principles 6 and 7 were harvested later on 2026-09-16 from the same project's classification of its 22 traps by *bug type* (the Obsidian set "Bug Types and Defenses": three families — interleaving, single source of truth, model error — the six safety/liveness cells inside interleaving, and a three-question test that locates any incident). Mapping that classification onto the skill showed 4 types covered, 7 partial and 7 missing, with the missing ones concentrated in the two families the notes call most expensive: model error, which nothing here asked about, and the liveness half, which the four-sided rule shape could not hold because its Prove side assumed a test. The trap numbers below are that project's; the mechanism is general.
规则 10 到 21、三个新批次和原则 6、7 于 2026-09-16 稍后从同一项目对 22 个坑按*错误类型*的分类中收割（Obsidian 那组"错误类型与应对"：交错、单一真相源、模型错误三族，交错内部的安全性/活性六格，以及一条三问定位判据）。把分类映射到 skill 上，得出 4 类已覆盖、7 类部分、7 类缺失，缺失的集中在笔记称为最贵的两族：模型错误——这里从来没问过；活性那一半——四面规则的形状装不下它，因为"证"一面默认是测试。下面的坑号是该项目的；机制是通用的。

## Vocabulary / 名词

The skill's words, in the order a reader meets them. Each is defined once here; `SKILL.md` and the batch files use them without explanation.
skill 用到的词，按读者遇到的顺序。每个只在这里定义一次；`SKILL.md` 和批次文件直接使用，不再解释。

**Rule / 规则.** One kind of problem, harvested from at least one incident, written so it can be applied to a plan before code exists. Numbered across the whole skill (Rule 1 … Rule 23); the number never changes once assigned, so a review can cite it.
一类问题，从至少一次事故中收割，写成在代码存在之前就能用到计划上的形式。全 skill 统一编号，编号一旦分配不再变，评审可以引用。

**Batch / 批次.** One mechanism, one file under `references/`, holding the rules that share that mechanism (database concurrency; UI state ownership; …). A batch is the unit of review: one subagent, one fresh context, one batch file. Every batch runs on every plan.
一种机制一个文件，放同一机制下的规则。批次是评审的单位：一个子代理、一个新上下文、一个批次文件。每个批次对每份计划都运行。

**The three gates / 三道门 — Stack, Where, Asks for.** Every rule opens with them. **Stack** names the technology the rule's tells and writes are phrased for (PostgreSQL, React, TanStack Query), what the mechanism holds for with the syntax translated, and when the rule is skipped; most rules say "any — never skipped", and a rule skipped for stack is written on a `SKIPPED` line, never silently omitted. **Where** lists the situations that make the rule apply, judged from the spec and the code — *not* from whether the plan already guards against it; a well-guarded plan is applicable and clean, not inapplicable. **Asks for** names the structured intermediate the plan must carry so the rule's tells can be checked by inspection rather than inferred from prose: a column on the pseudocode, a table beside the diagram. An empty cell in that table is what makes the trap visible.
每条规则以这三道门开头。**Stack** 说明规则的征兆和写法是对着哪种技术写的（PostgreSQL、React、TanStack Query）、机制在翻译语法后还对哪些技术成立、什么情况下跳过；多数规则写"any — never skipped"，因技术栈跳过的规则写成一行 `SKIPPED`，永远不静默省略。**Where** 列出让规则适用的处境，从 spec 和代码判断——*不*看计划是否已经防了它；防得好的计划是"适用且干净"，不是"不适用"。**Asks for** 点名计划必须携带的结构化中间物，让征兆能靠检查而不是靠从散文推断来核对：伪代码上的一列、图旁边的一张表。表里的空格就是陷阱显形的地方。

**Intermediate / 中间物.** The table or column an Asks for names: the `WHERE` beside each write, the path × table matrix, the state ledger, the lock × arrival table, the promise table. Filled by the author, never by the reviewer — a table the author fills makes absence visible; a table the reviewer infers hides it again.
Asks for 点名的表或列。由作者填，评审者永远不填——作者填的表让缺失可见，评审者推断出的表把它重新藏起来。

**Living intermediate / 常驻中间物** (added 2026-09-18). Five intermediates whose rows are facts about the codebase rather than about one change — the navigation graph, the update-source table, the state ledgers with the cap-owner table, the trust-boundary rows with the route × warrant table, the site list with the rule × site table — kept as five files in one folder per repository (`openspec/intermediates/` in an OpenSpec repository). The plan carries the **delta** — rows added, removed or altered, each naming the file's row — and the file carries the whole; archive merges the delta in, the way spec deltas merge into the living specs. The row that hides a trap is usually one the change did not write (the Rule 22 exit was on a route the change never touched; a column's second writer arrives weeks after its first), and a per-change table cannot show it. A living row the files contradict is a finding with effect `intermediate differs from code`, whether or not the change touched it.
五种中间物的行是关于代码库、而不是关于某一次变更的事实——导航图、update-source 表、状态账本（含 cap-owner 表）、信任边界行（含 route × warrant 表）、site list（含 rule × site 表）——每个仓库放在一个文件夹里的五个文件（OpenSpec 仓库是 `openspec/intermediates/`）。计划带 **delta**（新增、删除、修改的行，每行点名文件里的哪一行），文件带全量；归档时把 delta 合入，和 spec delta 合入常驻 spec 一样。藏着陷阱的那一行通常不是这次变更写的（Rule 22 的出口在变更没碰过的路由上；一列的第二个写者比第一个晚几周），按变更的表显示不出它。文件里与代码矛盾的行是一条 `intermediate differs from code` 的发现，不管这次变更有没有动它。

**Navigation graph / 导航图.** The routing term (Android Jetpack Navigation's) for what UX calls a user flow or screen flow: a directed graph whose nodes are routes and whose edges are the navigations out of them, so an *exit* is an outgoing edge and Rule 22's hop × exit table is the graph's edge list. Asked for as fenced Mermaid, complete only when each route has as many outgoing edges as its file has navigation calls — a UX flow drawn along the happy path is exactly the picture the incident's missing exit was absent from.
路由领域（Android Jetpack Navigation）对 UX 所说的 user flow / 页面流转图的叫法：节点是路由、有向边是从它出去的跳转，所以一个 *exit* 就是一条出边，Rule 22 的 hop × exit 表就是这张图的边表。以 fenced Mermaid 提供，只有当每个路由的出边数等于其文件里的跳转调用数时才算完整——沿主路径画的 UX 流程图恰恰就是事故里那条出口所缺席的那种画面。

**The four sides / 四面 — Tell, Write, Prove, View.** After the three gates, every rule has four sides, one per phase of the work. **Tell** (征兆): what the problem looks like in a plan, before code — the sentence, the diagram shape, the empty cell. **Write** (写): the property the spec needs, then how the code is made to hold it; the incident's fix is one implementation under its conditions, not the property. **Prove** (证): the assertion that goes red when the mitigation is reverted. **View** (审): the questions the reviewer asks; the first is always whether the intermediate matches the named files, and some Views say "grep the tree".
三道门之后每条规则有四面，对应工作的四个阶段。**Tell**：问题在代码之前、在计划里长什么样——那句话、那个图形、那个空格。**Write**：spec 要求的属性，然后是让代码守住它的写法；事故的修法是该属性在其条件下的一种实现，不是属性本身。**Prove**：回退缓解后会变红的那条断言。**View**：审查者问的问题；第一个永远是中间物与点名文件是否一致，有些 View 会说"grep 全树"。

**Proof / 证明.** Not "a test exists" — the specific assertion that fails when the mitigation is removed. A test that stays green without the mitigation is coverage impersonated, worse than none (Principle 6). Only a rule marked **liveness** may prove by argument and metric instead, because a liveness failure ("it never happens") has no moment at which an assertion turns red.
不是"有测试"——是去掉缓解后会失败的那条具体断言。没有缓解也绿的测试是冒充的覆盖，比没有更糟（原则 6）。只有标为 **liveness** 的规则可以改用论证和指标，因为活性失败（"它一直没发生"）没有断言会红的那一刻。

**Plan / 计划, diff, spec deltas, scenario.** The plan is what is reviewed before code: a design document with numbered pseudocode at the deciding statements and the mechanism's diagram as fenced text. The diff is the code change reviewed afterwards. The spec deltas are the requirement changes the plan implements; a **scenario** is one `#### Scenario:` block in them — the unit the confirmation round checks.
计划是代码之前被审的东西：带编号伪代码（只在做决定的语句处）和机制图（fenced 文本）的设计文档。diff 是之后被审的代码改动。spec deltas 是计划实现的需求变更；**scenario** 是其中一个 `#### Scenario:` 块——确认轮检查的单位。

**Plan pass / diff pass / confirmation round.** The three paths in `SKILL.md`. Plan pass: every batch reviews the plan; blocking rows are resolved in the plan before the first edit. Diff pass: every batch reviews the diff, anchored to file and line, and checks each plan-pass row's proof for a fake. Confirmation round: one subagent with the spec deltas and the diff only — the one round that looks from the spec toward the code — answering per scenario `SATISFIED`, `MISSING`, `UNIMPLEMENTABLE` or `UNVERIFIED`.
`SKILL.md` 里的三条路径。Plan pass：每个批次审计划，阻塞行在第一次编辑之前就在计划里解决。Diff pass：每个批次审 diff，锚到文件和行，并检查 plan pass 每一行的证明是不是假的。确认轮：一个子代理只拿 spec deltas 和 diff——唯一一轮从 spec 朝代码看——按 scenario 回答四种结果之一。

**Row / 行, anchor / 锚点, blocking / advisory.** A finding is one row of the output table: anchor, rule, effect, why it would be silent, mitigation, proof, blocking or advisory. The **anchor** is the numbered step, message or transition (or file and line in the diff pass) the finding points at; the author verifies every row at its anchor before acting on it. **Blocking** rows are resolved before the first edit; **advisory** rows never block.
一个发现就是输出表的一行。**锚点**是发现指向的编号步骤、消息或转换（diff pass 里是文件和行）；作者在处理任何一行之前先到锚点核实。**Blocking** 行在第一次编辑前解决；**advisory** 行永不阻塞。

**Verdicts and lines / 判定与行.** `APPLIES: yes | no` — the batch's first line, its own decision whether any of its rules' Where holds; a "no" with its reason is the record that the batch was considered. `SKIPPED: <rule> — bound to <stack>; plan uses <stack>`: a rule whose Stack gate does not hold for the plan's stack, checked in the named files; the record that the rule was read and set aside, not forgotten. `VERDICT: CLEAN | FINDINGS | INCOMPLETE`. `INCOMPLETE` with `MISSING` lines: a Where holds and an Asks for is absent — the plan is returned, not reviewed from prose. `SEARCHED`: every file read and grep run, the record of what the review actually looked at. `OUT-OF-BATCH`: a correctness problem outside this batch's rules, one line, never a row.
`APPLIES`——批次的第一行，它自己判断是否有规则的 Where 成立；"no"带理由是"这个批次考虑过"的记录。`SKIPPED`：Stack 门对计划的技术栈不成立的规则（在点名文件里核实过），是"读过并搁置"而不是"忘了"的记录。`INCOMPLETE` 加 `MISSING` 行：Where 成立而 Asks for 缺失——退回计划，不从散文里审。`SEARCHED`：读过的每个文件、跑过的每次 grep。`OUT-OF-BATCH`：本批次规则之外的正确性问题，一行，永远不是一整行发现。

**Merge / 合并, Accepted, Unresolved.** The author's context assembles batch outputs verbatim, verifies each row at its anchor, and resolves blocking rows — one **class fix** per rule (remove the possibility) rather than an **instance fix** per anchor (add a check where the finding pointed; Principle 7). A row missing its anchor or proof is returned to its batch once, never dropped. **Accepted** holds risks somebody chose to carry, each with that person's reason. **Unresolved** holds what nobody has looked at yet: a row still unanchored after its return, an `UNVERIFIED` scenario, an out-of-batch line with no disposition. Done requires Unresolved empty; moving a line to Accepted needs the reason, not the move (Principle 8).
作者的上下文原样拼接批次输出，逐行到锚点核实，解决阻塞行——每条规则一个**类修复**（消除可能性），而不是每个锚点一个**实例修复**（在发现指到的地方加个检查；原则 7）。缺锚点或证明的行退回批次一次，永不丢弃。**Accepted** 放有人决定承担的风险，附那个人的理由。**Unresolved** 放还没人看过的：退回后仍无锚点的行、`UNVERIFIED` 的 scenario、没有处置的 out-of-batch 行。Done 要求 Unresolved 为空；把一行挪到 Accepted 需要理由，不是挪动本身（原则 8）。

**Harvest / 收割.** Turning an incident into a rule: state what was written, what should have been, what let it pass on all four sides; classify into a family (below); add one bullet to an existing rule, or a new rule, or a new batch — never a new skill; tell the story once here.
把事故变成规则：写下写了什么、本该写什么、四面各是怎么放过的；归入一个族（见下）；给现有规则加一条、或加一条新规则、或加一个新批次——永远不新建 skill；事故在这里讲一次。

**Family / 族 and batch / 批次 — two partitions for two readers.** A **family** is for the harvester filing a lesson, and is defined by *what you must know to see the defect*: the code and its types alone (**logic error**); which side or actor is supposed to decide or own (**misplaced responsibility**); how many copies or writers exist (**multiplicity**); when things happen relative to each other (**ordering**); what the domain says the states and rules are (**model**). Asked in that order, cheapest first. A **batch** is for the reviewer running a pass, and is defined by *what evidence checks the rule*: the rules one reviewer can check with the same files open and the same intermediate filled. A rule joins an existing batch when its Asks-for table shares rows with that batch's; otherwise it opens one. The two partitions are not one-to-one — multiplicity has two batches, misplaced responsibility four — and a question can match while the evidence does not, which is how two rules were first mis-filed on 2026-09-18 (Rules 22 and 23, below). The families are open; the first three came from one project's 22 traps, not from a theory, and the fourth and fifth were named when incidents fell between them. Candidates already seen but not yet filed, each waiting on an incident to become a rule: **failure handling** (what happens when a step fails — Rules 9 and 15 are really this, filed where they surfaced); **environment and build** (the shipped artifact differs from source; a stray manifest silencing a gate; a symlink mode breaking a deploy); **representation** (one value in two encodings — NFC and decomposed nukta letters, locale number notation, bidi isolation); **lifetime** (processes not stopped, listeners not removed, unbounded growth). For comparison, IBM's Orthogonal Defect Classification (Chillarege et al., 1992) partitions defects into Assignment, Checking, Algorithm, Timing/Serialization, Interface, Function, Build/Package/Merge, Documentation: Checking ≈ logic error, Timing ≈ ordering, Interface ≈ misplaced responsibility, Function ≈ model, Build ≈ the unfiled environment family; ODC has no multiplicity — that family is this skill's own.
**族**给收割教训的人用，按*看出缺陷需要知道什么*划分：只需代码和类型（**逻辑错误**）；需要知道该由哪一侧或哪个角色决定或拥有（**职责错位**）；需要知道有几份副本或几个写者（**多副本**）；需要知道先后（**时序**）；需要知道领域规定的状态和规则（**模型**）。按此顺序问，最便宜的在前。**批次**给跑评审的人用，按*什么证据能核对这条规则*划分：同一个评审者、同样打开的文件、同一张填好的中间表能一起核对的规则。新规则的 Asks-for 表和某批次的表有共享的行就进那个批次，否则新开。两种划分不是一一对应——多副本有两个批次，职责错位有四个——而且问题对上了证据也可能对不上，2026-09-18 两条规则（下文 22、23）起初就是这样归错的。族是开放的：前三个来自一个项目的 22 个坑，不是来自理论；第四、第五个是事故掉在缝里时才命名的。已经见过但尚未立案、各等一次事故成规则的候选：**失败处理**（某一步失败后发生什么——规则 9、15 其实属于此，只是在浮现处立的案）；**环境与构建**（交付物和源码不一致；多余的 manifest 让门禁静默；symlink 模式弄坏部署）；**表示**（同一个值两种编码——NFC 与分解的 nukta 字母、区域数字写法、双向隔离）；**生命周期**（进程没停、监听没摘、无界增长）。可对照 IBM 的正交缺陷分类（Chillarege 等，1992）：Checking≈逻辑错误、Timing≈时序、Interface≈职责错位、Function≈模型、Build≈尚未立案的环境族；ODC 没有"多副本"——那一族是本 skill 自己的。

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

Classify first, with the three questions in SKILL.md's Harvest step 2 — serialize: does the bug survive? then concept or copies? or moment or "still nothing"? — because the fix that was at hand is not the classification, and three of the domain-model traps above spent time filed as races. Then: a new kind of problem is a new `## Rule N` in the mechanism's batch file — the three gates (Stack: what it is bound to, what it holds for, when it is skipped — "any" for most; Where: the situations that make it apply; Asks for: the table or column whose empty cell would have shown the trap) and the four sides — and a new incident section here. The same kind of problem: one more bullet under the existing rule's gate or side that failed, and the incident appended to its section. A new mechanism: a new batch file and one row in the router's table. A rule whose failure has no moment to assert on is marked *liveness* and proves by argument and metric; nothing else may. The *Write* side states the property the spec needs before the fix the incident used; the fix is one implementation under its conditions, and a Write side that carries only the fix turns the next correct alternative into a false finding — which is what the review of 2026-09-16 found in Rules 4 and 13. Never a new skill. Every batch runs on every plan and states its own applicability first; nothing in the plan selects batches, so a new batch needs no registration beyond its table row.
先分类，用 SKILL.md 收割第 2 步的三问——序列化：问题还在吗？然后缺概念还是多副本？或者指得出那一刻还是"一直没有"？——因为顺手的修法不是分类，上面模型错误的七个坑里有三个曾被归为竞态。然后：新的一类问题，在所属机制的批次文件里加一条 `## Rule N`——三道门（Stack：绑定什么技术、翻译后对什么成立、何时跳过——多数是"any"；Where：什么处境下它适用；Asks for：哪张表、哪一列的空格本可以暴露这个陷阱）加四面——这里加一节事故。同一类问题：在现有规则失守的那道门或那一面下加一条，事故追加到对应小节。新机制：新批次文件、路由表加一行。失败没有可断言那一刻的规则标为 *liveness*，靠论证和指标证明；别的规则不可以。*Write* 一面先写 spec 要求的属性，再写事故当时的修法；修法是该属性在其条件下的一种实现，只写修法的 Write 面会把下一个正确的替代实现报成假阳性——2026-09-16 的评审在规则 4 和 13 里发现的正是这个。永远不新建 skill。每个批次对每份计划都会运行并先声明自己是否适用；计划里没有任何东西选择批次，所以新批次除了表里那一行不需要别的登记。
