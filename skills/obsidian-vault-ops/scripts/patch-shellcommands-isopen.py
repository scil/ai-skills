"""Patch Shell commands 0.23.0 for Obsidian 1.14+: output modals never open.

Obsidian 1.14 gives every Modal instance an own `isOpen` boolean field. Shell commands' SC_Modal defines an
`isOpen()` method, which that field shadows, so `setExitCode()` (buffered output, always called with an exit
code) and `_handleRealtime()` throw "isOpen is not a function" and no output modal ever opens; the command
itself runs. The two call sites read SC_Modal's own `_isOpen` flag instead. Idempotent; re-run after every
plugin update (upstream 0.23.0 of 2024-11-09 is the latest release; the default branch has no fix as of
2026-10-22).

    python patch-shellcommands-isopen.py <vault>
"""

import shutil
import sys
from pathlib import Path

main = Path(sys.argv[1]) / ".obsidian/plugins/obsidian-shellcommands/main.js"
with open(main, encoding="utf-8", newline="") as f:  # keep the file's own line endings
    text = f.read()
eol = "\r\n" if "\r\n" in text else "\n"
pairs = [
    ("        if (this.isOpen()) {\n            if (null === this.exit_code) {",
     "        if (this._isOpen) {\n            if (null === this.exit_code) {"),
    ("        if (!this.modal.isOpen()) {", "        if (!this.modal._isOpen) {"),
]
pairs = [(old.replace("\n", eol), new.replace("\n", eol)) for old, new in pairs]
changed = 0
for old, new in pairs:
    if new in text:
        continue
    if text.count(old) != 1:
        sys.exit(f"pattern not found exactly once (plugin changed?): {old.strip()[:60]!r}")
    text = text.replace(old, new)
    changed += 1
if changed:
    shutil.copy2(main, main.with_suffix(".js.before-isopen-patch"))
    main.write_text(text, encoding="utf-8", newline="")
print(f"patched {changed} call site(s); {len(pairs) - changed} already patched")
