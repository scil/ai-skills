#!/usr/bin/env python
"""Text -> speech file. Standalone (no Anki needed). Default engine: edge-tts (Microsoft neural voices).

Examples
  tts.py --text "Hello world" --out hello.mp3
  tts.py --file reply.md --out reply.mp3 --voice en-US-GuyNeural --rate=-10%
  echo 你好 | tts.py --out hi.mp3 --voice zh-CN-XiaoxiaoNeural
  tts.py --file mixed.txt --split-lang --out card          # -> card-en.mp3 + card-zh.mp3
  tts.py --file x.txt --out x.mp3 --subtitles               # also writes x.srt (word-timed)
  tts.py --list-voices --lang en
  tts.py --text "offline test" --out t.wav --engine sapi --voice "Microsoft Zira Desktop"
  tts.py --file x.html --html --out x                       # use the Anki card HTML convention to split EN/ZH
"""
import asyncio
import json
import re
import sys
from pathlib import Path

from anki_lib import (CONFIG, html_to_speech, split_plain_by_script, synthesize, synthesize_many)


def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_argument_group("input (one of)")
    src.add_argument("--text")
    src.add_argument("--file", help="text file, or - for stdin (default when no --text)")
    src.add_argument("--html", action="store_true", help="input is HTML; strip tags and apply the card EN/ZH convention")
    p.add_argument("--out", help="output path (.mp3; .wav for --engine sapi). With --split-lang: a base name")
    p.add_argument("--engine", choices=["edge", "sapi"], default="edge")
    p.add_argument("--voice", help=f"edge voice ShortName or SAPI voice name (default {CONFIG['en_voice']})")
    p.add_argument("--rate", help="edge: e.g. +10%% / -20%%; sapi: -10..10 integer")
    p.add_argument("--pitch", help="edge only, e.g. -5Hz")
    p.add_argument("--volume", help="edge only, e.g. +20%%")
    p.add_argument("--subtitles", action="store_true", help="edge only: also write word-timed .srt next to --out")
    p.add_argument("--split-lang", action="store_true",
                   help="split English/Chinese and write <out>-en.mp3 + <out>-zh.mp3")
    p.add_argument("--en-voice", default=CONFIG["en_voice"])
    p.add_argument("--zh-voice", default=CONFIG["zh_voice"])
    p.add_argument("--list-voices", action="store_true")
    p.add_argument("--lang", help="filter --list-voices by locale prefix, e.g. en, zh, en-GB")
    p.add_argument("--json", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="print the text that would be spoken")
    a = p.parse_args()

    if a.list_voices:
        import edge_tts
        voices = asyncio.run(edge_tts.list_voices())
        rows = [{"name": v["ShortName"], "gender": v["Gender"], "locale": v["Locale"]}
                for v in voices if not a.lang or v["Locale"].lower().startswith(a.lang.lower())]
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            for r in rows:
                print(f"{r['name']:<32} {r['gender']:<7} {r['locale']}")
        return

    if a.text is not None:
        text = a.text
    else:
        text = sys.stdin.read() if (a.file in (None, "-")) else Path(a.file).read_text(encoding="utf-8")
    if not text.strip():
        raise SystemExit("error: empty input")
    if not a.out:
        raise SystemExit("error: --out is required")

    if a.split_lang or a.html:
        en, zh = html_to_speech(text) if a.html else split_plain_by_script(text)
        base = Path(a.out)
        base = base.with_suffix("") if base.suffix.lower() in (".mp3", ".wav") else base
        jobs = [(t, v, base.parent / f"{base.name}-{lang}.mp3")
                for lang, t, v in (("en", en, a.en_voice), ("zh", zh, a.zh_voice)) if t]
        if a.dry_run:
            for t, v, o in jobs:
                print(f"===== {o} ({v}) =====\n{t}\n")
            return
        if a.engine == "sapi":
            outs = [synthesize(t, a.voice, o, "sapi", sapi_rate=int(a.rate or 0)) for t, v, o in jobs]
        else:
            asyncio.run(synthesize_many(jobs, a.rate, a.pitch, a.volume))
            outs = [o for _, _, o in jobs]
        print(json.dumps([str(o) for o in outs]) if a.json else "\n".join(str(o) for o in outs))
        return

    if a.dry_run:
        print(text); return
    out = Path(a.out)
    voice = a.voice or CONFIG["en_voice"]
    if a.engine == "sapi":
        written = synthesize(text, a.voice, out, "sapi", sapi_rate=int(a.rate or 0))
    else:
        written = synthesize(text, voice, out, "edge", rate=a.rate, pitch=a.pitch, volume=a.volume,
                             subtitles=out.with_suffix(".srt") if a.subtitles else None)
    print(json.dumps({"file": str(written)}) if a.json else str(written))


if __name__ == "__main__":
    main()
