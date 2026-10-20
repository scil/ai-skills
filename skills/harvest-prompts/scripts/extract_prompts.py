"""Extract the prompts a user typed from Claude Code and Codex transcripts.

Writes <out>/prompts.jsonl (one record per prompt) and <out>/listing.txt (time-sorted,
one line per prompt, truncated) and prints the most repeated prompt heads.

Usage: python -I -X utf8 extract_prompts.py <out-dir> [--claude DIR] [--codex DIR]
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

SKIP_PREFIXES = (
    "<", "Caveat:", "[Request interrupted", "This session is being continued",
    "Tool loaded.", "[SYSTEM", "Base directory for this skill",
)
PASTED = re.compile(r"<pasted_content[^>]*>.*?</pasted_content[^>]*>", re.S)
TAGGED = re.compile(r"<(system-reminder|command-[a-z]+|local-command-[a-z]+)>.*?</\1>", re.S)


def clean(text):
    text = PASTED.sub(" [pasted] ", text)
    return TAGGED.sub("", text).strip()


def claude_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
            return None
        parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
        return "\n".join(parts) if parts else None
    return None


def from_claude(root):
    seen = set()
    for f in root.rglob("*.jsonl"):
        if "subagents" in f.parts:
            continue
        with f.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if '"type":"user"' not in line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if o.get("type") != "user" or o.get("isMeta") or o.get("isCompactSummary"):
                    continue
                if o.get("uuid") in seen:
                    continue
                raw = (claude_text(o.get("message", {}).get("content")) or "").strip()
                if not raw or raw.startswith(SKIP_PREFIXES):
                    continue
                text = clean(raw)
                if text:
                    seen.add(o.get("uuid"))
                    yield {"src": "claude", "project": f.parent.name, "ts": o.get("timestamp") or "", "text": text}


def from_codex(root):
    for f in root.rglob("*.jsonl"):
        with f.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                p = o.get("payload") or {}
                # event_msg/user_message is what the user typed; response_item also carries injected AGENTS.md text.
                if o.get("type") == "event_msg" and p.get("type") == "user_message":
                    text = clean(p.get("message", ""))
                    if text and not text.startswith(SKIP_PREFIXES):
                        yield {"src": "codex", "project": f.stem, "ts": o.get("timestamp") or "", "text": text}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--claude", default=str(Path.home() / ".claude" / "projects"))
    ap.add_argument("--codex", default=str(Path.home() / ".codex" / "sessions"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    for root, reader in ((Path(a.claude), from_claude), (Path(a.codex), from_codex)):
        if root.exists():
            rows.extend(reader(root))
    # A forked session copies its parent's messages under new ids: same text in the same minute is one prompt.
    uniq, keys = [], set()
    for r in sorted(rows, key=lambda r: r["ts"]):
        k = (r["text"], r["ts"][:16])
        if k not in keys:
            keys.add(k)
            uniq.append(r)

    with (out / "prompts.jsonl").open("w", encoding="utf-8") as fh:
        for r in uniq:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with (out / "listing.txt").open("w", encoding="utf-8") as fh:
        for i, r in enumerate(uniq):
            line = re.sub(r"\s+", " ", r["text"])[:160]
            fh.write(f"{i}|{r['project'][-14:]}|{line}\n")

    print(f"{len(uniq)} prompts ({len(rows)} before dedupe), {uniq[0]['ts'][:10] if uniq else '-'} to {uniq[-1]['ts'][:10] if uniq else '-'}")
    heads = Counter(re.sub(r"\s+", " ", r["text"]).strip().lower()[:40] for r in uniq)
    print("most repeated heads (mostly acknowledgements; intents need grouping):")
    for head, n in heads.most_common(30):
        if n > 1:
            print(f"  {n:4} | {head}")


if __name__ == "__main__":
    main()
