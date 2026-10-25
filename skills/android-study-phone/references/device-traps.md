# Device traps

Observed on the owner's phones, 2026-10-24. Each entry: symptom, cause, what works.

## Any vendor

- `pm disable <package>/<activity>` (one component, such as a launcher icon) fails on Android 9 and 11 with `Shell cannot change component state`: the shell may disable whole packages only.
- `am start -n <activity>` fails with `not exported from uid 1000` for most vendor Settings pages: give the owner the menu path instead.
- `DELETE_FAILED_INTERNAL_ERROR` from `pm uninstall` can be real (vivo `com.bbk.iqoo.feedback`: disable it) or stale (Samsung Snaplii was already gone): re-check with `pm list packages -u` before reporting.

## vivo (Funtouch OS 9, Android 9)

- `adb install` returns `Failure [-200]` until Developer options → "USB 安装" is on and the owner taps "继续安装" on the unlocked phone.
- `pm uninstall --user 0` on a vivo preinstall opens the vivo account login page and the command hangs. Kill the stuck `cmd` process (`ps -A | grep -w cmd`, then `kill <pid>`) and disable instead. `pm disable-user` needs no login.
- App lock and app hiding: 设置 → 指纹、面部与密码 (or 安全与隐私) → 隐私与应用加密. It needs its own privacy password.

## Samsung (One UI 3, Android 11)

- `pm uninstall --user 0` works on system apps without a Samsung account.
- Many Samsung preloads (`com.samsung.android.app.tips`, AR Emoji, video editor parts) are user-partition packages: uninstalling deletes the APK, so `install-existing` cannot restore them; reinstall from Galaxy Store.
- `lastDisabledCaller: auto_disabler` with `enabled=4` means One UI disabled an unused app ("disabled until used"). Tapping its icon re-enables it, so it is not locked. The shell can neither `pm enable` nor `pm disable-user` such an app; `pm uninstall` works. To keep its data, the owner re-enables it in Settings → Apps by hand first (untested whether `disable-user` then succeeds).

## Shizuku

- Install the release APK from `github.com/RikkaApps/Shizuku` (asking the owner before downloading). Start it without opening the app:

  ```
  adb shell 'p=$(pm path moe.shizuku.privileged.api | sed "s/package://; s/base.apk//"); $p/lib/*/libshizuku.so'
  ```

- Android 10 and below have no wireless debugging: the start command must run over USB after every reboot. Android 11+ can start Shizuku by wireless debugging.
