#!/usr/bin/env python
"""Media housekeeping for the Anki collection (collection.media via AnkiConnect).

Examples
  anki_media.py --store clip.mp3                     # copy into collection.media (same name)
  anki_media.py --store clip.mp3 --name sdh-1.mp3
  anki_media.py --get sdh-cc-1-back-en.mp3 --out ./dl
  anki_media.py --list "sdh-*"                        # glob on media file names
  anki_media.py --delete sdh-cc-1-back-en.mp3 --yes
  anki_media.py --check --query "deck:ai-teach-me"    # [sound:]/<img> refs whose file is missing
  anki_media.py --orphans --prefix sdh-               # media files no note references
  anki_media.py --orphans --prefix sdh- --delete-orphans --yes
"""
import fnmatch
import re
from pathlib import Path
from typing import List, Set

from anki_lib import run, AnkiClient, add_selection_args, base_parser, emit, export_notes, select_note_ids

REF_RE = re.compile(r"\[sound:([^\]]+)\]|<img[^>]+src=[\"']?([^\"'\s>]+)", re.I)


def refs_in(html: str) -> List[str]:
    return [a or b for a, b in REF_RE.findall(html)]


def main() -> None:
    p = base_parser(__doc__)
    p.add_argument("--store", metavar="FILE", action="append", default=[])
    p.add_argument("--name", help="media name for a single --store (default: file name)")
    p.add_argument("--get", metavar="NAME", action="append", default=[])
    p.add_argument("--out", metavar="DIR", default=".", help="directory for --get")
    p.add_argument("--list", metavar="GLOB", help="list media files matching a glob")
    p.add_argument("--delete", metavar="NAME", action="append", default=[])
    p.add_argument("--check", action="store_true", help="report missing media referenced by selected notes")
    p.add_argument("--orphans", action="store_true", help="media files referenced by no note")
    p.add_argument("--prefix", default="", help="restrict --orphans to files starting with PREFIX")
    p.add_argument("--delete-orphans", action="store_true")
    p.add_argument("--yes", action="store_true", help="required for any deletion")
    add_selection_args(p, required=False)
    a = p.parse_args()
    c = AnkiClient(a.url)
    out = {}

    for f in a.store:
        name = a.name if (a.name and len(a.store) == 1) else Path(f).name
        if not a.dry_run:
            c.store_media(name, Path(f).read_bytes())
        out.setdefault("stored", []).append(name)
    for name in a.get:
        data = c.retrieve_media(name)
        if data is None:
            out.setdefault("missing", []).append(name); continue
        dst = Path(a.out) / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        out.setdefault("saved", []).append(str(dst))
    if a.list:
        out["files"] = c("getMediaFilesNames", pattern=a.list)
    if a.delete:
        if not a.yes and not a.dry_run:
            raise SystemExit("error: --delete needs --yes")
        for name in a.delete:
            if not a.dry_run:
                c("deleteMediaFile", filename=name)
        out["deleted"] = a.delete

    if a.check:
        ids = select_note_ids(c, a) or c.find_notes("deck:*")
        missing = []
        for n in export_notes(c, ids):
            for f, v in n["fields"].items():
                for ref in refs_in(v):
                    if c.retrieve_media(ref) is None:
                        missing.append({"note": n["id"], "field": f, "file": ref})
        out["missing_refs"] = missing

    if a.orphans:
        files = [f for f in c("getMediaFilesNames", pattern=a.prefix + "*") if not f.startswith("_")]
        referenced: Set[str] = set()
        ids = c.find_notes("deck:*")
        for i in range(0, len(ids), 500):
            for n in c.notes_info(ids[i:i + 500]):
                for v in n["fields"].values():
                    referenced.update(refs_in(v["value"]))
        orphans = [f for f in files if f not in referenced]
        out["orphans"] = orphans
        if a.delete_orphans and orphans:
            if not a.yes and not a.dry_run:
                raise SystemExit("error: --delete-orphans needs --yes")
            if not a.dry_run:
                for f in orphans:
                    c("deleteMediaFile", filename=f)
            out["deleted_orphans"] = len(orphans)

    out["dry_run"] = a.dry_run
    emit(out, a.json)


if __name__ == "__main__":
    run(main)
