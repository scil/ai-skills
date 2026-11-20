# playwright-real-phone

Origin: a session tested a served site on a Samsung phone. It started with a standalone Node script over `connectOverCDP`. Then it moved the script into Playwright Test as a phone project. Each trap in the table cost at least one failed run.

The `--debug=cli` step comes from the `playwright-tests.md` reference of Microsoft's `playwright-cli` skill. Nobody tried it against a phone yet.

Other skills, read before this one was written:

- Microsoft's `playwright-cli` covers device emulation (`--device`) and `attach --cdp`.
- Anthropic's `webapp-testing` covers local apps with Python Playwright.
- The community skill `playwright-best-practices` covers fixtures and projects.

None of the three covers a real Android phone. Other community skills were not read.

Not tried: the experimental `_android` API of Playwright. It drives Chrome on Android through adb without the manual forward.
