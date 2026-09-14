# scil-testing — where this came from

One incident, one lesson: **a guard has two sides, and stubbing a library hides its half.** This is the testing-phase half of the 2026-09-11 `useBlocker` incident; `scil-coding` holds the coding half and `scil-review` the reviewing half. The incident itself is told in full in `scil-coding/readme.md`; this file is only about why no test caught it and what would have.
一次事故，一个教训：**守卫有两面，stub 掉库就藏起了它那一面。** 这是 2026-09-11 `useBlocker` 事故的测试阶段那一半。事故本身在 `scil-coding/readme.md` 里讲全了；这里只讲为什么没有测试抓到它、什么测试本可以抓到。

## Why no test caught it / 为什么没测出来

A leave-prompt was firing on every clean refresh of five screens, for months, through a green gate (typecheck, lint, 581 unit tests, the settings e2e file). Three reasons, each now a section in `SKILL.md`:
五个页面每次干净刷新都弹提醒，持续好几个月，门禁全绿。三个原因，各成 `SKILL.md` 一节：

1. **Every test asked only one direction.** "Does the prompt appear with a draft open?" — yes, always, because two listeners both prevented. Nobody asked "does it stay silent when nothing is dirty?" → *Test both directions.*
   **所有测试只问一个方向。** 没人问"干净时安静吗"。
2. **Every component suite stubbed the hook.** `useBlocker: () => ({ status: "idle", … })` in six test files. The router's listener never existed in jsdom, so that layer *could not* see it. → *Put one test where the library actually runs.*
   **所有组件测试把 hook stub 掉了。** 路由的监听器在 jsdom 里根本不存在。
3. **The e2e harness bypasses the behaviour.** Playwright's `page.reload()` does not fire `beforeunload`; the existing tests reloaded with dirty drafts and never saw a dialog. The prompt has to be *probed*: dispatch a cancelable `beforeunload` at `window` and read whether `dispatchEvent` returned `false`. → *Probe what the harness bypasses.*
   **e2e 工具绕过了这个行为。** 只能派发可取消事件来探测。

## What was added / 加了什么

One e2e test (`porch-profile-edit.spec.ts`, "a photo change is already saved, so leaving does not warn — only an open draft does"): untouched screen → no prompt; photo removed and confirmed → no prompt; name draft typed → prompt arms (positive control); Cancel → no prompt. Revert check run for real: fix undone → red on the first silence assertion (`Expected: false, Received: true`); restored → green. Coverage stated honestly: probed on settings, the other four screens verified by identical option shape only.
一个 e2e 测试：未动→不弹；头像删除并确认→不弹；输入名字草稿→弹（正向对照）；Cancel→不弹。回退检查真跑了：回退→红，恢复→绿。覆盖如实说明：只在 settings 探测，其余四屏靠形状相同。

## How to maintain / 怎么维护

Add a rule only if it is about the same thing — a guard's silent side, or a stub/harness hiding the library's behaviour — and it comes from a real incident. The incident goes in the readme, the rule in `SKILL.md`.
只有关于同一件事——守卫安静的那一面、或 stub/工具藏起库的行为——且来自真实事故的规则才加。事故写 readme，规则写 `SKILL.md`。
