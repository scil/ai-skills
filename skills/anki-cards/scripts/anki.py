#!/usr/bin/env python
"""Single entry point: anki.py <command> [args...]  ==  anki_<command>.py [args...]

Commands
  info     inspect decks/models/fields, find & export notes
  add      add notes from a .md / .json cards file
  update   edit fields / tags of existing notes
  audio    generate + attach EN/ZH TTS clips to notes
  media    store / get / delete / check media files
  delete   delete notes (needs --yes)
  realtime configure HyperTTS Realtime audio for a note type (template tag + add-on preset)
  tts      text -> mp3 (standalone)
  ping     check AnkiConnect is reachable

Run `anki.py <command> --help` for that command's options.
"""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMMANDS = {
    "info": "anki_info.py", "add": "anki_add.py", "update": "anki_update.py", "audio": "anki_audio.py",
    "media": "anki_media.py", "delete": "anki_delete.py", "realtime": "anki_config_HyperTTS_realtime.py", "tts": "tts.py",
}


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__); return
    cmd = sys.argv[1]
    if cmd == "ping":
        sys.argv = [sys.argv[0], "--ping", *sys.argv[2:]]
        cmd = "info"
    elif cmd not in COMMANDS:
        raise SystemExit(f"unknown command {cmd!r}\n{__doc__}")
    else:
        sys.argv = [sys.argv[0], *sys.argv[2:]]
    script = HERE / COMMANDS[cmd]
    sys.argv[0] = str(script)
    sys.path.insert(0, str(HERE))
    runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
