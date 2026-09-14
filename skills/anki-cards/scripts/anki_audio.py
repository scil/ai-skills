#!/usr/bin/env python
"""Generate TTS audio for notes and attach it as [sound:...] tags (English + Chinese clips per field).

How a field is split into speech (see README.md "Speech convention"):
  - elements with style color:#888 (or data-lang="zh")  -> Chinese clip
  - <pre>, data-lib-banner, [sound:], data-lang="skip"   -> not spoken
  - glossary block ("English vocabulary" .. "Memory line"): <strong> terms -> EN clip, whole <li> -> ZH clip
  - everything else -> English clip (embedded CJK stripped, or moved to ZH with --cjk-in-en zh)

Examples
  anki_audio.py --last 3 --dry-run                   # print the exact EN/ZH text per field
  anki_audio.py --ids 1,2,3                          # default: English only -> front-en + back-en per note
  anki_audio.py --ids 1,2,3 --lang en,zh             # also Chinese clips (4 per note)
  anki_audio.py --query "tag:media::subtitles" --fields 背面
  anki_audio.py --ids 1 --en-voice en-GB-RyanNeural --zh-voice zh-CN-YunxiNeural --rate=-10%
  anki_audio.py --ids 1 --replace                    # drop old [sound:] + media, regenerate
  anki_audio.py --ids 1 --remove                     # strip [sound:] tags only (media kept unless --delete-media)
  anki_audio.py --ids 1 --prefix sdh-cc-1 --keep out/audio
"""
import asyncio
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from anki_lib import (run, CONFIG, HERE, SOUND_RE, AnkiClient, add_selection_args, backup_notes, base_parser, emit,
                      export_notes, html_to_speech, select_note_ids, synthesize_many)


def main() -> None:
    p = base_parser(__doc__)
    add_selection_args(p)
    p.add_argument("--fields", default=",".join(CONFIG["fields"]), help="fields to voice (comma-separated)")
    p.add_argument("--lang", default=CONFIG["audio_langs"],
                   help=f"which clips to make: en, zh, or en,zh (default {CONFIG['audio_langs']}, from anki.json)")
    p.add_argument("--en-voice", default=CONFIG["en_voice"])
    p.add_argument("--zh-voice", default=CONFIG["zh_voice"])
    p.add_argument("--rate", help="e.g. -10%%")
    p.add_argument("--pitch")
    p.add_argument("--volume")
    p.add_argument("--prefix", help="media file name prefix (default note<id>); with several notes gets -1, -2 …")
    p.add_argument("--position", choices=["end", "start"], default="end", help="where to put the [sound:] tags")
    p.add_argument("--replace", action="store_true", help="remove existing [sound:] tags (+ their media) first")
    p.add_argument("--remove", action="store_true", help="only strip [sound:] tags; no generation")
    p.add_argument("--delete-media", action="store_true", help="with --remove: also delete the referenced media")
    p.add_argument("--keep", metavar="DIR", help="also keep the generated mp3s in DIR")
    p.add_argument("--concurrency", type=int, default=4)
    r = p.add_argument_group("speech rules")
    r.add_argument("--no-skip-pre", action="store_true", help="read <pre> blocks too")
    r.add_argument("--grey", default=None, help=f"style substring marking Chinese (default {CONFIG['grey_style']!r}; '' to disable)")
    r.add_argument("--cjk-in-en", choices=["strip", "zh"], default="strip", help="CJK inside English text")
    r.add_argument("--glossary-start", default=None)
    r.add_argument("--glossary-end", default=None)
    p.add_argument("--no-backup", action="store_true")
    a = p.parse_args()

    c = AnkiClient(a.url)
    ids = select_note_ids(c, a)
    notes = export_notes(c, ids)
    fields = [f.strip() for f in a.fields.split(",") if f.strip()]
    langs = [l.strip() for l in a.lang.split(",") if l.strip()]
    voices = {"en": a.en_voice, "zh": a.zh_voice}
    keep = Path(a.keep) if a.keep else None
    if keep:
        keep.mkdir(parents=True, exist_ok=True)
    work = Path(HERE / ".audio-tmp"); work.mkdir(exist_ok=True)

    # -------- plan
    plan: List[Tuple[int, str, str, str, str]] = []   # (nid, field, lang, filename, text)
    strip_updates: Dict[int, Dict[str, str]] = {}
    old_media: List[str] = []
    for i, n in enumerate(notes, 1):
        slug = (a.prefix + (f"-{i}" if len(notes) > 1 else "")) if a.prefix else f"note{n['id']}"
        for f in fields:
            if f not in n["fields"]:
                raise SystemExit(f"error: note {n['id']} has no field {f!r} (has {list(n['fields'])})")
            src = n["fields"][f]
            if a.replace or a.remove:
                old_media += [m.group(0)[7:-1] for m in SOUND_RE.finditer(src)]
                stripped = re.sub(r"<div>\s*(\[sound:[^\]]+\]\s*)+</div>", "", src)
                stripped = SOUND_RE.sub("", stripped).strip()
                if stripped != src:
                    strip_updates.setdefault(n["id"], {})[f] = stripped
                src = stripped
            if a.remove:
                continue
            # file name part for the field: front/back for the usual 2-field models
            side = ["front", "back"][fields.index(f)] if len(fields) == 2 else ("" if len(fields) == 1 else f)
            en, zh = html_to_speech(src, grey=a.grey, glossary_start=a.glossary_start, glossary_end=a.glossary_end,
                                    skip_pre=not a.no_skip_pre, cjk_in_en=a.cjk_in_en)
            for lang, text in (("en", en), ("zh", zh)):
                if lang in langs and text:
                    name = "-".join(x for x in (slug, side, lang) if x) + ".mp3"
                    plan.append((n["id"], f, lang, name, text))

    if a.dry_run or a.verbose:
        for nid, f, lang, name, text in plan:
            print(f"===== {nid} {f} {lang} -> {name} ({voices[lang]}) =====\n{text}\n", file=sys.stderr)
        if strip_updates:
            print(f"would strip [sound:] from {len(strip_updates)} note(s); old media: {old_media}", file=sys.stderr)
    if a.dry_run:
        emit({"clips": len(plan), "strip": len(strip_updates), "old_media": old_media}, a.json); return

    if not a.no_backup and (plan or strip_updates):
        emit({"backup": str(backup_notes(c, ids, "audio"))}, a.json)

    # -------- strip old
    for nid, flds in strip_updates.items():
        c("updateNoteFields", note={"id": nid, "fields": flds})
    if old_media and (a.replace or a.delete_media):
        for m in old_media:
            try:
                c("deleteMediaFile", filename=m)
            except Exception as e:
                print(f"warn: could not delete {m}: {e}", file=sys.stderr)
    if a.remove:
        emit({"stripped_notes": len(strip_updates), "deleted_media": old_media if a.delete_media else []}, a.json)
        return

    # -------- synthesize
    jobs = [(text, voices[lang], work / name) for _, _, lang, name, text in plan]
    asyncio.run(synthesize_many(jobs, a.rate, a.pitch, a.volume, a.concurrency))

    # -------- store + attach
    per_note: Dict[int, Dict[str, List[str]]] = {}
    for nid, f, lang, name, _ in plan:
        data = (work / name).read_bytes()
        c.store_media(name, data)
        if keep:
            (keep / name).write_bytes(data)
        per_note.setdefault(nid, {}).setdefault(f, []).append(f"[sound:{name}]")
    current = {n["id"]: n["fields"] for n in export_notes(c, ids)}
    for nid, flds in per_note.items():
        new = {}
        for f, tags in flds.items():
            block = "<div>" + " ".join(tags) + "</div>"
            new[f] = (block + current[nid][f]) if a.position == "start" else (current[nid][f] + block)
        c("updateNoteFields", note={"id": nid, "fields": new})
    for f_ in work.glob("*.mp3"):
        f_.unlink(missing_ok=True)

    emit({"notes": len(per_note), "clips": [x[3] for x in plan], "kept_in": str(keep) if keep else None}, a.json)


if __name__ == "__main__":
    run(main)
