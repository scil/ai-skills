---
name: android-study-phone
description: Strip an Android phone or tablet down to a child's study device over adb, following the owner's standing preferences, and log every change with app ids to Logseq. Use when a phone or tablet is connected over USB to list, classify, uninstall, disable, hide or restore its apps, to find out who changed them, or to install Shizuku.
---

# Android study phone

The owner turns old Android phones and tablets into study devices for a child: learning apps stay, nearly everything else goes. Done so far: `vivo Android 9` (vivo Y3s), `Samsung Android 11` (Galaxy A70s) and `Xiaomi Android 13` (Xiaomi Pad 5). Their Logseq pages are the precedent for every decision below.

Terms used here:

- **app id**: the Android package name, such as `com.vivo.gallery`. Every list, reply and log line names an app by its label *and* its app id.
- **uninstall**: `pm uninstall <id>` for a user-installed app (APK and data gone), `pm uninstall --user 0 <id>` for a preinstalled one (APK stays on the system partition, so `cmd package install-existing <id>` restores it, data cleared).
- **disable**: `pm disable-user --user 0 <id>`. Icon gone, app cannot run, data kept; `pm enable <id>` restores it.

## Owner's preferences

Apply these as defaults; present them in the classified list so the owner can override.

- **Keep**: study and English-learning apps; Settings; the vendor's device-care app (vivo i管家 `com.iqoo.secure`, Samsung `com.samsung.android.sm_cn`); Google Play services, TTS and sync adapters; WebView `com.google.android.webview` (other apps render pages with it); calculator; any app the owner names for that phone (Samsung: Android Auto, Alipay, China Merchants Bank).
- **Settings stays enabled, always.** USB debugging lives there; with Settings disabled, a phone whose debugging switches off can only be recovered by factory reset. Hiding only its icon needs root or device owner: adb's shell is refused. Settings is therefore the remaining bypass: whoever opens Settings → Apps can re-enable a disabled app. Tell the owner, and offer the vendor's app lock where it can lock Settings ([references/device-traps.md](references/device-traps.md)).
- **Remove** (uninstall where possible, otherwise disable):
  - games, short video, social apps;
  - browsers and app stores; the Play Store `com.android.vending` per device: disabled on vivo and Samsung, uninstalled `--user 0` on Xiaomi;
  - **search**, a standing instruction: the home-screen swipe-down search page, app suggestions, the Google search app `com.google.android.googlequicksearchbox` and search widgets (vendor app ids in device traps);
  - voice assistants (Jovi, Bixby);
  - vendor entertainment and promotion preloads: game centres, quick apps, lock-screen magazine, vendor shop, karaoke, music, minus-one screen, live wallpapers, tips;
  - on both phones the owner went on to disable gallery, camera, file manager, clock, calendar, contacts, messages and phone ("the phone does not need calls"). Propose them in the first list, each with its consequence: no outgoing or emergency calls, SMS and verification codes unreadable, no way to view photos, alarms silent.
- **Ask per phone**:
  - AI assistants (kept on vivo, removed on Samsung);
  - chat apps (uninstalled on vivo, disabled on Samsung): uninstalling loses chat history.
- **Banking and payment apps**: keep their data, so disable rather than uninstall. When adb refuses, the owner deletes them by hand.
- **Installing apps**: the owner installs from the store personally. Bring the Play Store (and the vendor store if needed) back the way it left: disabled → `pm enable <id>`; uninstalled `--user 0` → `cmd package install-existing <id>`. Wait for "installed", then remove the store the same way again. Find the new apps by today's `firstInstallTime` in `dumpsys package <id>`, and log each with the name from the `<title>` of `https://play.google.com/store/apps/details?id=<id>&hl=zh_CN`.
- **Recommend against** ShizuStore: with Shizuku running it installs apps silently, bypassing the disabled stores.

## Steps

1. **Identify the phone.** `adb devices -l`; with several attached, pass `-s <serial>` on every command. Read `ro.build.version.release`, `ro.build.display.id`, `ro.build.version.security_patch` and the model. Done when the Logseq page name `<Brand> Android <version>` is known.
2. **Inventory.** `pm list packages -3`, `pm list packages -s -e`, `pm list packages -d`, and launcher apps via `cmd package query-activities --brief -a android.intent.action.MAIN -c android.intent.category.LAUNCHER`. For every already-disabled app read `lastDisabledCaller` and `enabled=` from `dumpsys package <id>`. When the owner asks for an immediate removal (stores, browsers), do it before the inventory: a dropped USB link should cost the inventory, not the protection. Done when every launcher app and every disabled app has a state and, where disabled, a caller.
3. **Classify and present, changing nothing.** One table grouped by category (study, games, social, payment, browsers and stores, search, assistants, vendor preloads, core system). Each row: label, app id, last used and this month's use (`lastTimeUsed`, `totalTimeUsed` from `dumpsys usagestats`), the owner's default action marked. Flag first, each with its risk: games and short-video apps; Expo Go `host.exp.exponent` (runs apps from the internet); file managers such as ES File Explorer `com.estrongs.android.pop` (install APK files); video apps; Settings itself (re-enables disabled apps).
4. **Confirm.** Wait for the owner's choices. Offer optional groups (video, social) as a multi-select list; an option left unanswered means keep. Wiping SMS, call logs or other data inside an app is permanent deletion: the owner does it on the phone; you disable afterwards.
5. **Execute** one package per command, checking each result. USB can drop mid-session: run `adb -s <serial> get-state` before each chain of commands. On uninstall failure, fall back to disable and record both results. Watch for a hang: read `dumpsys window | grep mCurrentFocus` to see what the phone is showing. Vendor and Android-version traps: [references/device-traps.md](references/device-traps.md).
6. **Verify.** Re-list enabled launcher apps and disabled apps; compare `pm list packages -u` with `pm list packages` to see which uninstalled apps `install-existing` can restore. Prove no browser is left: `cmd package query-activities --brief -a android.intent.action.VIEW -d https://example.com -c android.intent.category.BROWSABLE` returns nothing. After disabling a phone or contacts app, confirm the remaining default dialer with `cmd package resolve-activity --brief -a android.intent.action.DIAL`.
7. **Log.** Done when every package changed this session appears in the phone's Logseq page with label, app id and method, and the page's restore commands still match what was done.

## When something changed back

A disabled store runs again, a kept app is gone, or a new app appears. Build the timeline from the records:

- `dumpsys package <id>`: `enabled=1` means someone enabled it by hand (no caller is recorded for enables); `installerPackageName` and `firstInstallTime` say how and when an app arrived.
- `dumpsys usagestats`: `ACTIVITY_RESUMED` events give a minute-by-minute timeline, only for the last few days; the monthly stats give `totalTimeUsed` and `lastTimeUsed` per package, a longer history that survives uninstall.
- Uninstall screens never name the removed app, and an app removed before the check may leave no name at all: say so rather than guess which app it was.

The records tell a person from the system, never parent from child. Present the timeline, mark which steps look like parental setup and which like a workaround, and ask the owner: they may have done some of it themselves.

## Logseq log

- Page file: `E:\GitHub\scil-only-me\Logseq-scil\pages\<Brand> Android <version>.md`, for a phone or a tablet alike; the `logseq://graph/Logseq-scil?page=...` URL maps to that file name.
- The owner edits these pages too: Read the file before every edit and keep their changes.
- Write a log line only after the command's output confirms success.
- Layout, matching the existing pages: a top block `adb操作日志`, tab-indented children, `collapsed:: true` under each group, written in Chinese with app ids in backticks. Groups: device facts; device info (chip, memory, storage, screen, system version, bootloader lock and verified-boot state, battery, app counts; never accounts or personal data); the reason for the session, as the owner reported it; restore commands; disabled; uninstalled but restorable; fully uninstalled; kept (with reasons); kept because the owner has not decided (with the risk); apps the owner installed; current state (browser, store, phone).
- When an app moves group (re-enabled store, kept app later disabled), edit both groups so the page stays the current truth, noting the date and why. When the owner reports a fact ("I deleted the game"), replace the page's guesses with it.
