---
name: android-study-phone
description: Strip an Android phone down to a child's study device over adb, following the owner's standing preferences, and log every change with app ids to Logseq. Use when a phone is connected over USB to list, classify, uninstall, disable, hide or restore its apps, or to install Shizuku.
---

# Android study phone

The owner turns old Android phones into study devices for a child: learning apps stay, nearly everything else goes. Done so far: `vivo Android 9` (vivo Y3s) and `Samsung Android 11` (Galaxy A70s). Their Logseq pages are the precedent for every decision below.

Terms used here:

- **app id**: the Android package name, such as `com.vivo.gallery`. Every list, reply and log line names an app by its label *and* its app id.
- **uninstall**: `pm uninstall <id>` for a user-installed app (APK and data gone), `pm uninstall --user 0 <id>` for a preinstalled one (APK stays on the system partition, so `cmd package install-existing <id>` restores it, data cleared).
- **disable**: `pm disable-user --user 0 <id>`. Icon gone, app cannot run, data kept; `pm enable <id>` restores it.

## Owner's preferences

Apply these as defaults; present them in the classified list so the owner can override.

- **Keep**: study and English-learning apps; Settings; the vendor's device-care app (vivo i管家 `com.iqoo.secure`, Samsung `com.samsung.android.sm_cn`); Google Play services, TTS and sync adapters; calculator; any app the owner names for that phone (Samsung: Android Auto, Alipay, China Merchants Bank).
- **Settings stays enabled, always.** USB debugging lives there; with Settings disabled, a phone whose debugging switches off can only be recovered by factory reset. Hiding only its icon needs root or device owner: adb's shell is refused.
- **Remove** (uninstall where possible, otherwise disable):
  - games, short video, social apps;
  - browsers and app stores (the Play Store is disabled, not uninstalled);
  - **search**, a standing instruction: the home-screen swipe-down search page, app suggestions, the Google search app and search widgets (vivo `com.vivo.globalsearch`, `com.vivo.puresearch`; Samsung `com.samsung.android.app.galaxyfinder`, `com.samsung.android.smartsuggestions`, `com.samsung.android.app.searchwidget`);
  - voice assistants (Jovi, Bixby);
  - vendor entertainment and promotion preloads: game centres, quick apps, lock-screen magazine, vendor shop, karaoke, music, minus-one screen, live wallpapers, tips;
  - on both phones the owner went on to disable gallery, camera, file manager, clock, calendar, contacts, messages and phone ("the phone does not need calls"). Propose them in the first list, each with its consequence: no outgoing or emergency calls, SMS and verification codes unreadable, no way to view photos, alarms silent.
- **Ask per phone**:
  - AI assistants (kept on vivo, removed on Samsung);
  - chat apps (uninstalled on vivo, disabled on Samsung): uninstalling loses chat history.
- **Banking and payment apps**: keep their data, so disable rather than uninstall. When adb refuses, the owner deletes them by hand.
- **Installing apps**: the owner installs from the store personally. Re-enable the Play Store (and restore the vendor store if needed), wait for "installed", then close the stores again and log the new apps with names taken from their Google Play pages.
- **Recommend against** ShizuStore: with Shizuku running it installs apps silently, bypassing the disabled stores.

## Steps

1. **Identify the phone.** `adb devices -l`; with several attached, pass `-s <serial>` on every command. Read `ro.build.version.release`, `ro.build.display.id`, `ro.build.version.security_patch` and the model. Done when the Logseq page name `<Brand> Android <version>` is known.
2. **Inventory.** `pm list packages -3`, `pm list packages -s -e`, `pm list packages -d`, and launcher apps via `cmd package query-activities --brief -a android.intent.action.MAIN -c android.intent.category.LAUNCHER`. For every already-disabled app read `lastDisabledCaller` and `enabled=` from `dumpsys package <id>`. Done when every launcher app and every disabled app has a state and, where disabled, a caller.
3. **Classify and present, changing nothing.** One table grouped by category (study, games, social, payment, browsers and stores, search, assistants, vendor preloads, core system), each row label plus app id, the owner's default action marked. Flag games and short-video apps first.
4. **Confirm.** Wait for the owner's choices. Wiping SMS, call logs or other data inside an app is permanent deletion: the owner does it on the phone; you disable afterwards.
5. **Execute** one package per command, checking each result. On uninstall failure, fall back to disable and record both results. Watch for a hang: read `dumpsys window | grep mCurrentFocus` to see what the phone is showing. Vendor and Android-version traps: [references/device-traps.md](references/device-traps.md).
6. **Verify.** Re-list enabled launcher apps and disabled apps; compare `pm list packages -u` with `pm list packages` to see which uninstalled apps `install-existing` can restore. After disabling a phone or contacts app, confirm the remaining default dialer with `cmd package resolve-activity --brief -a android.intent.action.DIAL`.
7. **Log.** Done when every package changed this session appears in the phone's Logseq page with label, app id and method, and the page's restore commands still match what was done.

## Logseq log

- Page file: `D:\A\data\Logseq-scil\pages\<Brand> Android <version>.md`; the `logseq://graph/Logseq-scil?page=...` URL maps to that file name.
- The owner edits these pages too: Read the file before every edit and keep their changes.
- Layout, matching the existing pages: a top block `adb操作日志`, tab-indented children, `collapsed:: true` under each group, written in Chinese with app ids in backticks. Groups: device facts; restore commands; disabled; uninstalled but restorable; fully uninstalled; kept (with reasons); apps the owner installed; current state (browser, store, phone).
- When an app moves group (re-enabled store, kept app later disabled), edit both groups so the page stays the current truth, noting the date and why.
