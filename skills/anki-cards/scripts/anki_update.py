#!/usr/bin/env python
"""Modify fields / tags of existing notes. Backs up the pre-change state first (default on).

Examples
  # bulk: edit an exported JSON (anki_info.py --out) and write it back (matched by "id")
  anki_update.py --file review.json
  # set / append / prepend a field on selected notes
  anki_update.py --ids 123 --set "背面=<p>new html</p>"
  anki_update.py --ids 123 --set-file 背面=back.html
  anki_update.py --last 3 --append "背面=<div>[sound:x.mp3]</div>"
  # regex replace across fields (Python re syntax; \\1 groups ok)
  anki_update.py --query "tag:media::subtitles" --replace "Blu-ray" "Blu‑ray"
  anki_update.py --query "deck:ai-teach-me" --field 正面 --replace "(?s)<div data-lib-banner.*?</div>" ""
  # tags
  anki_update.py --ids 1,2 --add-tags media::subtitles --remove-tags draft
  anki_update.py --rename-tag old::tag new::tag
  # tell Anki to move selected notes' cards to another deck
  anki_update.py --ids 1,2 --move-to-deck En
"""
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

from anki_lib import (run, AnkiClient, add_selection_args, backup_notes, base_parser, emit, export_notes,
                      select_note_ids, strip_html)


def parse_assign(s: str) -> "tuple[str, str]":
    k, sep, v = s.partition("=")
    if not sep:
        raise SystemExit(f"error: expected FIELD=VALUE, got {s!r}")
    return k.strip(), v


def main() -> None:
    p = base_parser(__doc__)
    add_selection_args(p, required=False)
    p.add_argument("--file", metavar="notes.json", help="bulk update from interchange JSON (by id)")
    f = p.add_argument_group("field edits (repeatable)")
    f.add_argument("--set", action="append", default=[], metavar="FIELD=HTML")
    f.add_argument("--set-file", action="append", default=[], metavar="FIELD=path.html")
    f.add_argument("--append", action="append", default=[], metavar="FIELD=HTML")
    f.add_argument("--prepend", action="append", default=[], metavar="FIELD=HTML")
    f.add_argument("--replace", nargs=2, action="append", default=[], metavar=("PATTERN", "REPL"),
                   help="regex replace; restrict with --field")
    f.add_argument("--field", action="append", default=[], help="limit --replace to these fields")
    f.add_argument("--ignore-case", action="store_true")
    t = p.add_argument_group("tags")
    t.add_argument("--add-tags", default="", metavar="a,b")
    t.add_argument("--remove-tags", default="", metavar="a,b")
    t.add_argument("--rename-tag", nargs=2, metavar=("OLD", "NEW"), help="collection-wide, no selection needed")
    p.add_argument("--move-to-deck", metavar="DECK")
    p.add_argument("--no-backup", action="store_true")
    a = p.parse_args()

    c = AnkiClient(a.url)

    if a.rename_tag:
        if not a.dry_run:
            c("replaceTagsInAllNotes", tag_to_replace=a.rename_tag[0], replace_with_tag=a.rename_tag[1])
        emit({"renamed_tag": a.rename_tag, "dry_run": a.dry_run}, a.json)
        if not (a.ids or a.query or a.last or a.file):
            return

    # -------- collect target notes and the new field values
    updates: Dict[int, Dict[str, str]] = {}
    tag_targets: List[int] = []

    if a.file:
        data = json.loads(Path(a.file).read_text(encoding="utf-8"))
        for n in (data if isinstance(data, list) else [data]):
            if not n.get("id"):
                raise SystemExit("error: every note in --file needs an 'id'")
            updates[int(n["id"])] = dict(n.get("fields", {}))
            tag_targets.append(int(n["id"]))
        file_tags = {int(n["id"]): n.get("tags") for n in (data if isinstance(data, list) else [data])}
    else:
        file_tags = {}

    ids = select_note_ids(c, a)
    if ids:
        current = {n["id"]: n for n in export_notes(c, ids)}
        flags = re.I if a.ignore_case else 0
        for nid, n in current.items():
            fields = dict(n["fields"])
            changed = False
            for s in a.set:
                k, v = parse_assign(s); fields[k] = v; changed = True
            for s in a.set_file:
                k, v = parse_assign(s); fields[k] = Path(v).read_text(encoding="utf-8"); changed = True
            for s in a.append:
                k, v = parse_assign(s); fields[k] = fields.get(k, "") + v; changed = True
            for s in a.prepend:
                k, v = parse_assign(s); fields[k] = v + fields.get(k, ""); changed = True
            for pat, rep in a.replace:
                for k in (a.field or list(fields)):
                    new = re.sub(pat, rep, fields[k], flags=flags)
                    if new != fields[k]:
                        fields[k] = new; changed = True
            if changed:
                updates[nid] = {k: v for k, v in fields.items() if v != n["fields"].get(k)}
            tag_targets.append(nid)

    tag_targets = list(dict.fromkeys(tag_targets))
    add_tags = [t_ for t_ in a.add_tags.split(",") if t_.strip()]
    rem_tags = [t_ for t_ in a.remove_tags.split(",") if t_.strip()]

    # -------- report
    summary = {"field_updates": len(updates), "tag_targets": len(tag_targets) if (add_tags or rem_tags or file_tags) else 0,
               "move_to_deck": a.move_to_deck, "dry_run": a.dry_run}
    if a.dry_run or a.verbose:
        for nid, flds in updates.items():
            for k, v in flds.items():
                print(f"{nid} {k}: {strip_html(v, 100)}", file=sys.stderr)
    if a.dry_run:
        emit(summary, a.json); return
    if not updates and not add_tags and not rem_tags and not file_tags and not a.move_to_deck:
        emit("nothing to do", a.json); return

    # -------- write
    all_ids = list(dict.fromkeys([*updates, *tag_targets]))
    if not a.no_backup:
        bp = backup_notes(c, all_ids, "update")
        summary["backup"] = str(bp)

    for nid, flds in updates.items():
        if flds:
            c("updateNoteFields", note={"id": nid, "fields": flds})
    for nid, tags in file_tags.items():
        if tags is not None:
            cur = c.notes_info([nid])[0]["tags"]
            if sorted(cur) != sorted(tags):
                c("removeTags", notes=[nid], tags=" ".join(cur))
                c("addTags", notes=[nid], tags=" ".join(tags))
    if add_tags:
        c("addTags", notes=tag_targets, tags=" ".join(add_tags))
    if rem_tags:
        c("removeTags", notes=tag_targets, tags=" ".join(rem_tags))
    if a.move_to_deck:
        cards = c("findCards", query="nid:" + ",".join(map(str, all_ids)))
        c("changeDeck", cards=cards, deck=a.move_to_deck)
    emit(summary, a.json)


if __name__ == "__main__":
    run(main)
