# scil-review — where this came from

One incident, one lesson: **a reviewer should look for the library API that was not used, and for the guard tested on one side only.** This is the review-phase half of the 2026-09-11 `useBlocker` incident; `scil-coding` holds the coding half and `scil-testing` the testing half. The incident is told in full in `scil-coding/readme.md`; this file is about why review passed it, and what questions would have stopped it.
一次事故，一个教训：**评审者要找没用上的库 API，和只测了一面的守卫。** 这是 2026-09-11 `useBlocker` 事故的评审阶段那一半。事故全文在 `scil-coding/readme.md`；这里讲评审为什么放过了它、哪些问题本可以拦住。

## Why review passed it / 评审为什么放过了

Five screens with `useBlocker` + a hand-rolled `beforeunload` listener went through review (Claude, codex loops, manual passes) and were never questioned. Each reason is now a check in `SKILL.md`:
五处 `useBlocker` + 手写 `beforeunload` 都过了评审（Claude、codex 循环、手测），从没被质疑。每个原因现在都是 `SKILL.md` 里的一条检查：

1. **Nobody listed the unset options.** The reviewer read the two options the code set and never asked what the other two defaulted to. → *List the unset options.*
2. **The duplicate listener looked like diligence.** A hand-written listener beside the hook read as "belt and braces", not as "the library already does this". → *A hand-rolled listener for an event the library handles.*
3. **The comment was taken as evidence.** "The browser owns this prompt; all we can do is opt in" was reviewed as an explanation, not as a claim to verify. → *A comment describing library behaviour is a claim.*
4. **"The same guard X carries" ended the inquiry.** Consistency with a sibling was read as correctness. → *Has X been audited?*
5. **The tests were one-sided and stubbed, and review did not ask for the other side.** → *Where is the silence test? Does the test run the real library?*
6. **The symptom was reported on one screen** and could have been fixed on one. → *One symptom, how many sites?*

## What the review round after the fix did / 修复后那一轮评审做了什么

Applied these checks to the fix itself: confirmed no `addEventListener("beforeunload")` remained in the app; confirmed the function-form option is in the hook's effect deps so it cannot go stale; found that the thanks-card spec already said *"Leaving with nothing written SHALL simply leave, without a prompt"* — so the fix brought code into compliance and no MODIFIED delta was needed; found one stale sentence in `AGENTS.md` and fixed it; reported coverage as "probed on settings, shape-verified on four".
把这些检查用在修复本身上：确认应用里没剩 `beforeunload` 监听器；确认函数形式的选项在 effect deps 里；发现感谢卡规格本来就写了"没写东西离开不提醒"，所以不需要 MODIFIED；发现并改掉 `AGENTS.md` 一句过时的话；覆盖如实报告。

The design choice — own handler + `false` versus the library's function form — was decided by putting both in code side by side, not by argument.
两种设计的取舍是把代码并排放出来定的，不是靠说理。

## How to maintain / 怎么维护

Add a check only if it is about the same thing — an API the diff did not use, or a guard proven on one side — and it comes from a real review miss. The miss goes in the readme, the check in `SKILL.md`.
只有关于同一件事——diff 没用上的 API、只证了一面的守卫——且来自真实的评审漏网才加。漏网写 readme，检查写 `SKILL.md`。
