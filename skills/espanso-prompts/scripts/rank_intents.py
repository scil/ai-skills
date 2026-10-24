"""Count prompts per intent with keyword regexes (multi-label) and list what no intent matched.

intents.json maps an intent name to a case-insensitive regex. Writes <out>/unmatched.txt.

Usage: python -I -X utf8 rank_intents.py <out-dir> <intents.json>
"""
import json
import re
import sys
from pathlib import Path


def main():
    out, intents_file = Path(sys.argv[1]), Path(sys.argv[2])
    rows = [json.loads(l)["text"] for l in (out / "prompts.jsonl").open(encoding="utf-8")]
    intents = {k: re.compile(v, re.I | re.M) for k, v in json.loads(intents_file.read_text(encoding="utf-8")).items()}

    hits = {k: [t for t in rows if p.search(t)] for k, p in intents.items()}
    for name, items in sorted(hits.items(), key=lambda kv: -len(kv[1])):
        print(f"\n=== {name}: {len(items)}")
        for t in items[:: max(1, len(items) // 5)][:5]:
            print("   -", re.sub(r"\s+", " ", t)[:110])

    unmatched = [t for t in rows if not any(p.search(t) for p in intents.values())]
    with (out / "unmatched.txt").open("w", encoding="utf-8") as fh:
        for t in unmatched:
            fh.write(re.sub(r"\s+", " ", t)[:160] + "\n")
    print(f"\n{len(unmatched)} of {len(rows)} prompts matched no intent -> {out / 'unmatched.txt'}")


if __name__ == "__main__":
    main()
