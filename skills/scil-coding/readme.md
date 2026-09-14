# scil-coding — where this came from

One incident, one lesson: **use the library's API fully before writing code beside it.** This is the coding-phase half of it; `scil-testing` holds the testing half and `scil-review` the reviewing half. All three came out of the same afternoon.
一次事故，一个教训：**先把库的 API 用足，再在它旁边写代码。** 这是编码阶段的那一半；`scil-testing` 是测试的一半，`scil-review` 是评审的一半。三个都来自同一个下午。

## The incident (2026-09-11, ThanksPorch) / 事故

**Symptom.** On `/settings`, changing only the avatar and then refreshing the page produced the browser's "information you've entered may not be saved" prompt — although the photo was already in the database and R2.
**症状。** `/settings` 只改头像然后刷新，浏览器弹"你输入的信息可能未保存"——但头像早已存进数据库和 R2。

**Root cause.** The screen's own `beforeunload` handler was correctly gated on `hasUnsavedText`. But TanStack Router's `useBlocker`, used on the same screen for in-app navigation, registers its *own* `beforeunload` listener, and its option `enableBeforeUnload` defaults to `true` — which arms the prompt for as long as a blocker is mounted, without ever consulting `shouldBlockFn`. So the prompt fired on every refresh, avatar or not. The avatar change was only where someone noticed.
**根因。** 页面自己的 `beforeunload` 处理器门控是对的。但同一页面用来拦应用内导航的 `useBlocker` 会注册它自己的监听器，选项 `enableBeforeUnload` 默认 `true`——只要 blocker 挂着就一律弹，根本不看 `shouldBlockFn`。所以每次刷新都弹，和头像无关。

**Spread.** The identical pairing — `useBlocker` + hand-rolled listener — existed on five screens (`settings`, `cards.new`, `offerings.new`, `offerings.$id`, `offering-edit-all-screen`), each commented "the same guard the full offering editor carries". All five had the bug.
**扩散。** 同样的组合在五个页面都有，每处注释都写"和 offering 编辑器同一套"。五处全错。

**Fix.** First pass: `enableBeforeUnload: false` on all five, keeping the own handler. Second pass, after comparing both designs in code: `enableBeforeUnload: () => <same predicate>` and the five hand-rolled effects deleted — one predicate for both exits.
**修法。** 第一版：五处都传 `enableBeforeUnload: false`，保留自写 handler。用代码对比两种设计后改为第二版：`enableBeforeUnload: () => <同一判断>`，删掉五个手写 effect——一个判断管两种离开。

**Why it happened** (asked afterwards, and the source of every rule in `SKILL.md`):
**为什么会这样**（事后追问，`SKILL.md` 每条规则的来源）：

1. The options type has four fields; the code read two. → *Read the whole options type.*
2. The unread option's default was `true` and did something. → *Unset ≠ off.*
3. A DOM listener was written beside a hook that already handled the event. → *Same event, stop sign.*
4. The comment encoded a plain-DOM mental model ("the browser's to prompt for, all we can do is opt in") until it read as knowledge. → *A comment is a claim.*
5. The pairing was copied four times without an audit. → *The second copy is the audit; fix all copies in one change.*
6. Two listeners both preventing was correct whenever dirty, so nobody saw it. → *Replace, don't add.*

## How to maintain / 怎么维护

This skill is one lesson deep on purpose. Add a rule only if it is about the same thing — reaching for what the library already gives — and it comes from a real incident; put the incident in the readme and the rule in `SKILL.md`. A lesson about a different thing is a different skill.
这个 skill 有意只有一课深。只有关于同一件事——用上库已经给的东西——且来自真实事故的规则才加进来；事故写在 readme，规则写在 `SKILL.md`。别的事是别的 skill。
