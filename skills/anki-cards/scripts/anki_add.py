#!/usr/bin/env python
"""Add notes from a JSON or Markdown cards file (formats: README.md).

Examples
  anki_add.py --file cards.md --dry-run            # show resolved notes, write nothing
  anki_add.py --file cards.md                      # add to the deck/model in the file or anki.json
  anki_add.py --file cards.json --deck En --tags extra::tag
  anki_add.py --file cards.md --audio              # then run anki_audio.py on the new notes
  anki_add.py --file cards.md --audio --en-voice en-US-GuyNeural --rate=-10%
  cat cards.md | anki_add.py --file - --out ids.txt
"""
import json
import subprocess
import sys
from pathlib import Path

from anki_lib import (run, CONFIG, HERE, AnkiClient, base_parser, emit, json_to_add_note, load_cards_file,
                      strip_html)


def main() -> None:
    p = base_parser(__doc__)
    p.add_argument("--file", required=True, help="cards file: .md, .json, or - for stdin")
    p.add_argument("--deck", help=f"override deck (default from file, else {CONFIG['deck']})")
    p.add_argument("--model", help=f"override note type (default from file, else {CONFIG['model']})")
    p.add_argument("--tags", default="", help="comma-separated tags appended to every note")
    p.add_argument("--allow-duplicate", action="store_true", help="add even if the first field already exists")
    p.add_argument("--dup-scope", choices=["deck", "collection"], default="deck")
    p.add_argument("--create-deck", action="store_true", help="create the deck if missing")
    p.add_argument("--out", metavar="ids.txt", help="write new note ids, one per line")
    p.add_argument("--audio", action="store_true", help="after adding, run anki_audio.py on the new notes")
    a, audio_args = p.parse_known_args()   # unknown flags are forwarded to anki_audio.py

    cards = load_cards_file(a.file)
    extra = [t for t in a.tags.split(",") if t.strip()]
    notes = [json_to_add_note(c_, a.deck, a.model, extra, a.allow_duplicate, a.dup_scope) for c_ in cards]

    c = AnkiClient(a.url)
    # validate field names against the model before writing anything
    for n in notes:
        want = c.model_fields(n["modelName"])
        bad = [f for f in n["fields"] if f not in want]
        if bad:
            raise SystemExit(f"error: fields {bad} not in model {n['modelName']} (has {want})")
        if not n["fields"].get(want[0], "").strip():
            raise SystemExit(f"error: first field '{want[0]}' is empty for note: {n}")

    if a.dry_run or a.verbose:
        for n in notes:
            first = next(iter(n["fields"].values()))
            print(f"[{n['deckName']} / {n['modelName']}] {' '.join(n['tags'])}\n   {strip_html(first, 120)}",
                  file=sys.stderr)
    if a.dry_run:
        emit({"would_add": len(notes), "notes": notes} if a.json else f"would add {len(notes)} note(s)", a.json)
        return

    if a.create_deck:
        for d in {n["deckName"] for n in notes}:
            c("createDeck", deck=d)
    can = c("canAddNotesWithErrorDetail", notes=notes)
    problems = [(i, r["error"]) for i, r in enumerate(can) if not r["canAdd"]]
    if problems:
        for i, err in problems:
            print(f"cannot add note {i}: {err}", file=sys.stderr)
        raise SystemExit(2)

    ids = c("addNotes", notes=notes)
    ids = [i for i in ids if i]
    if a.out:
        Path(a.out).write_text("\n".join(map(str, ids)) + "\n", encoding="utf-8")
    emit({"added": len(ids), "ids": ids}, a.json)

    if a.audio and ids:
        sys.stdout.flush()
        cmd = [sys.executable, str(HERE / "anki_audio.py"), "--ids", ",".join(map(str, ids)), *audio_args]
        if a.url:
            cmd += ["--url", a.url]
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    run(main)
