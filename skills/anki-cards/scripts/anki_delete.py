#!/usr/bin/env python
"""Delete notes (all their cards). Always previews; requires --yes to actually delete. Backs up first.

Examples
  anki_delete.py --ids 1,2 --dry-run
  anki_delete.py --query "deck:ai-teach-me tag:draft" --yes
  anki_delete.py --last 1 --yes --delete-media       # also remove media only these notes referenced
"""
import sys

from anki_lib import run, AnkiClient, add_selection_args, backup_notes, base_parser, emit, export_notes, select_note_ids, strip_html
from anki_media import refs_in


def main() -> None:
    p = base_parser(__doc__)
    add_selection_args(p)
    p.add_argument("--yes", action="store_true", help="actually delete")
    p.add_argument("--delete-media", action="store_true", help="also delete media referenced only by these notes")
    p.add_argument("--no-backup", action="store_true")
    a = p.parse_args()

    c = AnkiClient(a.url)
    ids = select_note_ids(c, a)
    notes = export_notes(c, ids)
    for n in notes:
        first = next(iter(n["fields"].values()), "")
        print(f"{n['id']}  [{n['model']}] {' '.join(n['tags'])}\n   {strip_html(first, 100)}", file=sys.stderr)
    if a.dry_run or not a.yes:
        emit({"would_delete": len(notes), "hint": "add --yes to delete"}, a.json); return

    media = sorted({r for n in notes for v in n["fields"].values() for r in refs_in(v)})
    out = {"deleted": len(ids)}
    if not a.no_backup:
        out["backup"] = str(backup_notes(c, ids, "delete"))
    c("deleteNotes", notes=ids)
    if a.delete_media and media:
        # keep any file still referenced by a surviving note
        still = set()
        rest = c.find_notes("deck:*")
        for i in range(0, len(rest), 500):
            for n in c.notes_info(rest[i:i + 500]):
                for v in n["fields"].values():
                    still.update(refs_in(v["value"]))
        gone = [m for m in media if m not in still]
        for m in gone:
            c("deleteMediaFile", filename=m)
        out["deleted_media"] = gone
    emit(out, a.json)


if __name__ == "__main__":
    run(main)
