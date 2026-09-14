#!/usr/bin/env python
"""Read-only inspection of Anki via AnkiConnect.

Examples
  anki_info.py --ping
  anki_info.py --decks --models --tags
  anki_info.py --fields 问答题
  anki_info.py --last 3 --format table
  anki_info.py --query "tag:media::subtitles" --out review.json
  anki_info.py --ids 1789190587573 --format md --fields-only 背面
  anki_info.py --query "deck:ai-teach-me added:1" --browse
  anki_info.py --stats ai-teach-me
  anki_info.py --sync
"""
import json
from pathlib import Path

from anki_lib import (run, CONFIG, AnkiClient, add_selection_args, base_parser, emit, export_notes,
                      select_note_ids, strip_html)


def main() -> None:
    p = base_parser(__doc__)
    g = p.add_argument_group("collection")
    g.add_argument("--ping", action="store_true", help="print AnkiConnect version")
    g.add_argument("--decks", action="store_true")
    g.add_argument("--models", action="store_true")
    g.add_argument("--fields", metavar="MODEL", help="field names of a note type")
    g.add_argument("--tags", action="store_true", help="all tags in the collection")
    g.add_argument("--stats", metavar="DECK", nargs="?", const=CONFIG["deck"], help="note/card counts of a deck")
    g.add_argument("--sync", action="store_true", help="trigger AnkiWeb sync")
    add_selection_args(p, required=False)
    n = p.add_argument_group("notes")
    n.add_argument("--out", metavar="FILE.json", help="export selected notes (interchange JSON)")
    n.add_argument("--format", choices=["json", "md", "table"], default="json", help="stdout format for notes")
    n.add_argument("--fields-only", metavar="F1,F2", help="restrict shown/exported fields")
    n.add_argument("--raw", action="store_true", help="table: show raw HTML instead of stripped text")
    n.add_argument("--browse", action="store_true", help="open Anki's Browser on the selection")
    a = p.parse_args()

    c = AnkiClient(a.url)
    out = {}
    if a.ping:
        out["version"] = c.version()
    if a.decks:
        out["decks"] = c("deckNames")
    if a.models:
        out["models"] = c("modelNames")
    if a.fields:
        out["fields"] = c.model_fields(a.fields)
    if a.tags:
        out["tags"] = c("getTags")
    if a.stats:
        out["stats"] = {"deck": a.stats,
                        "notes": len(c.find_notes(f'"deck:{a.stats}"')),
                        "cards": len(c("findCards", query=f'"deck:{a.stats}"'))}
    if a.sync:
        c("sync")
        out["sync"] = "requested"
    if out:
        emit(out, a.json or True)

    ids = select_note_ids(c, a)
    if not ids and not (a.ids or a.query or a.last):
        if not out:
            p.print_help()
        return

    if a.browse:
        q = a.query or ("nid:" + ",".join(map(str, ids)))
        c("guiBrowse", query=q)

    notes = export_notes(c, ids)
    if a.fields_only:
        keep = [f.strip() for f in a.fields_only.split(",")]
        for n_ in notes:
            n_["fields"] = {k: v for k, v in n_["fields"].items() if k in keep}
    if a.out:
        Path(a.out).write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")
        emit({"exported": len(notes), "file": a.out}, a.json)
        return

    if a.format == "json" or a.json:
        print(json.dumps(notes, ensure_ascii=False, indent=2))
    elif a.format == "md":
        for n_ in notes:
            print(f"# {n_['id']}\ndeck: {n_['deck']}\nmodel: {n_['model']}\ntags: {' '.join(n_['tags'])}")
            for k, v in n_["fields"].items():
                print(f"\n## {k}\n{v}")
            print()
    else:
        for n_ in notes:
            first = next(iter(n_["fields"].values()), "")
            print(f"{n_['id']}  [{n_['model']}]  {' '.join(n_['tags'])}")
            print("   " + (first if a.raw else strip_html(first, 110)))


if __name__ == "__main__":
    run(main)
