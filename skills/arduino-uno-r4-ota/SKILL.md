---
name: arduino-uno-r4-ota
description: Configure and verify Arduino UNO R4 WiFi uploads over Wi-Fi on Windows with Arduino IDE and Juraj Andrassy's ArduinoOTA library; troubleshoot network-port discovery. Use for IDE-style OTA uploads, rather than the official OTAUpdate download workflow or ESP32 OTA.
---

# Arduino UNO R4 WiFi OTA

OTA (over-the-air updating) replaces the board's running program through the network. Use Juraj Andrassy's ArduinoOTA library with WiFiS3 for Arduino IDE network-port uploads. The official Renesas OTAUpdate library implements a different download workflow.

## Configure

1. Read applicable project instructions. Inspect the existing sketch before replacing board firmware; preserve its behavior when adding OTA. A request to configure OTA authorizes the necessary installation and uploads, but does not authorize discarding unrelated application behavior.
2. Locate Arduino IDE's bundled `arduino-cli.exe`, commonly under `%LOCALAPPDATA%\Programs\Arduino IDE\resources\app\lib\backend\resources` or `C:\Program Files\Arduino IDE\resources\app\lib\backend\resources`. Use it when CLI is absent from PATH. Run `core list`, `lib list --format json`, and `board list --format json`; confirm the target board, not just an arbitrary COM port. UNO R4 WiFi's fully qualified board name (FQBN, the compiler's board identifier) is `arduino:renesas_uno:unor4wifi`.
3. Install Arduino UNO R4 Boards if absent and `ArduinoOTA` maintained by Juraj Andrassy. WiFiS3 is supplied by the board package. Inspect the library's reported `install_dir`; Windows Documents can be redirected to another drive.
4. Copy the installed library's `extras/renesas/platform.local.txt` beside the active board package's `platform.txt`, normally `%LOCALAPPDATA%\Arduino15\packages\arduino\hardware\renesas_uno\<version>`. Back up and merge an existing override. Use the Renesas file, not the AVR or ESP files. It includes IDE 2's `upload.tool.network=arduino_ota` recipe. Restart the IDE to load the configuration. Repeat for a new package version after upgrading.
5. Obtain the user's network choice. Read a saved Windows Wi-Fi password only when authorized, capturing `netsh wlan show profile name=... key=clear` privately; never print the command's secret-bearing output. Generate a separate OTA password. Store credentials in an ignored local `arduino_secrets.h`, never in this skill, committed examples, command literals, or logs. Do not commit build binaries containing credentials.
6. For a new sketch, adapt [assets/UnoR4OTA/UnoR4OTA.ino](assets/UnoR4OTA/UnoR4OTA.ino) and its placeholder secrets header. For an existing sketch, add the same connection and OTA calls. Include WiFiS3 before ArduinoOTA. Do not wait indefinitely for USB Serial. Call `ArduinoOTA.poll()` frequently in `loop()`; avoid lengthy blocking application code. Every subsequent OTA-uploaded sketch must retain OTA support.
7. Compile into a separate output directory. InternalStorage reserves approximately half the available program flash for the incoming binary; check `InternalStorage.maxSize()`, not only the IDE's full-flash compilation limit. Upload the initial program by USB after confirming the board identity.

## Verify

1. Confirm Wi-Fi connection and the printed IP address, or run `board list --discovery-timeout 15s --format json`. Network discovery uses mDNS (multicast DNS, a local-network service discovery protocol). WiFiS3 supports the required multicast. Do not define `NO_OTA_PORT` when network discovery is desired.
2. Close Serial Monitor before testing updates. Select the discovered network port and UNO R4 WiFi in the IDE, then use normal Upload and supply the OTA password. Without GUI access, use the installed `arduinoOTA.exe` under the board tools directory with `-address <ip> -port 65280 -username arduino -password <local-secret-variable> -sketch <compiled-bin> -upload /sketch -b`. Avoid verbose commands that expose the password.
3. Make an observable harmless change, such as the template's LED interval, compile, and upload over Wi-Fi. Require upload success plus renewed discovery or another post-reboot observation. Do not claim visual LED verification unless observed. The CLI uses the same underlying upload tool but does not prove the IDE UI selection works.
4. Open the sketch in Arduino IDE when useful and explain how to select its network port. Network upload does not supply a wireless Serial Monitor.

Done when the initial upload succeeds, a subsequent Wi-Fi upload succeeds, the board returns with OTA available, and credentials remain local. Report partial completion accurately if hardware or network access prevents verification.

## Troubleshoot only when needed

- No discovered port: verify the board has an IP, the computer can reach it, and the network allows device communication. Check guest-network/client isolation, VPN routing, and Windows private-network firewall permissions. Discovery uses UDP 5353; upload uses TCP 65280. Test the latter with `Test-NetConnection -ComputerName <ip> -Port 65280`. Do not disable the entire firewall.
- No multicast discovery but TCP works: follow the maintainer's manual-IP programmer workaround in the [README](https://github.com/JAndrassy/ArduinoOTA#ota-upload-from-ide-without-network-port). The Renesas override already contains `tools.arduinoOTA.program.pattern`; add the IP-based entry to existing `programmers.txt`, configure its password to match the sketch, restart IDE, and use Upload Using Programmer with Serial Monitor closed.
- Unauthorized: check the OTA password, not the Wi-Fi password. Only one successful update: check that the new sketch retained OTA initialization and polling.
- Failure after about ten seconds: consult the maintainer's uploader timeout guidance before changing tools; newer uploader versions support a longer timeout. Do not repeatedly flash unchanged firmware without a diagnostic reason.

Use the installed library as the configuration source. If compatibility or versions differ, verify current primary sources: [ArduinoOTA README](https://github.com/JAndrassy/ArduinoOTA), [Renesas upload configuration](https://github.com/JAndrassy/ArduinoOTA/blob/master/extras/renesas/platform.local.txt), and [Arduino's Windows data-folder documentation](https://support.arduino.cc/hc/en-us/articles/360018448279-Open-the-Arduino15-folder).
