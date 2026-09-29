"""Shared helpers for the anki-cards scripts.

- AnkiClient: thin AnkiConnect wrapper (UTF-8, retries, error -> exception)
- config: anki.json next to this file, overridable by env / CLI
- note JSON interchange format (see README.md)
- Markdown card parser (see README.md)
- HTML -> speech text splitter (English / Chinese)
- TTS via edge-tts (default) or Windows SAPI (offline fallback)
- backup helper
"""
import argparse
import asyncio
import base64
import datetime as _dt
import html as _html
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "anki.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "url": "http://127.0.0.1:8765",
    "deck": "ai-teach-me",
    "model": "问答题",
    "fields": ["正面", "背面"],
    "base_tags": ["ai-teach-me"],
    "en_voice": "en-US-JennyNeural",
    "zh_voice": "zh-CN-XiaoxiaoNeural",
    "audio_langs": "en",          # which clips anki_audio.py makes by default: "en", "zh" or "en,zh"
    "rate": "+0%",
    "pitch": "+0Hz",
    "volume": "+0%",
    "backup_dir": "D:/A/Scoop/persist/anki/backups/anki-cards",
    "grey_style": "#888",
    "glossary_start": "English vocabulary",
    "glossary_end": "Memory line",
}


def load_config() -> Dict[str, Any]:
    cfg = dict(DEFAULT_CONFIG)
    if CONFIG_PATH.exists():
        cfg.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    if os.environ.get("ANKI_URL"):
        cfg["url"] = os.environ["ANKI_URL"]
    return cfg


CONFIG = load_config()


# --------------------------------------------------------------------------- output

def say(*parts: Any) -> None:
    """Print to stderr (keeps stdout clean for --json / piping)."""
    print(*parts, file=sys.stderr)


def emit(obj: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    elif isinstance(obj, (list, tuple)):
        for x in obj:
            print(x if isinstance(x, str) else json.dumps(x, ensure_ascii=False))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            print(f"{k}: {v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)}")
    else:
        print(obj)


def _force_utf8_stdout() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except Exception:
            pass


_force_utf8_stdout()


# --------------------------------------------------------------------------- AnkiConnect

class AnkiError(RuntimeError):
    pass


class AnkiClient:
    def __init__(self, url: Optional[str] = None, retries: int = 3, timeout: int = 30):
        self.url = url or CONFIG["url"]
        self.retries = retries
        self.timeout = timeout

    def __call__(self, action: str, **params: Any) -> Any:
        body = json.dumps({"action": action, "version": 6, "params": params}, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(self.url, body, {"Content-Type": "application/json; charset=utf-8"})
        last: Optional[Exception] = None
        for attempt in range(self.retries):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    res = json.load(r)
                if res.get("error"):
                    raise AnkiError(f"{action}: {res['error']}")
                return res.get("result")
            except AnkiError:
                raise
            except Exception as e:  # connection problems -> retry
                last = e
                time.sleep(0.5 * (attempt + 1))
        raise AnkiError(f"AnkiConnect unreachable at {self.url} ({last}). Is Anki open with the AnkiConnect add-on?")

    # convenience --------------------------------------------------------------
    def version(self) -> int:
        return int(self("version"))

    def find_notes(self, query: str) -> List[int]:
        return list(self("findNotes", query=query))

    def notes_info(self, ids: Iterable[int]) -> List[Dict[str, Any]]:
        ids = list(ids)
        return list(self("notesInfo", notes=ids)) if ids else []

    def model_fields(self, model: str) -> List[str]:
        return list(self("modelFieldNames", modelName=model))

    def store_media(self, name: str, data: bytes) -> str:
        return self("storeMediaFile", filename=name, data=base64.b64encode(data).decode())

    def retrieve_media(self, name: str) -> Optional[bytes]:
        b64 = self("retrieveMediaFile", filename=name)
        return base64.b64decode(b64) if b64 else None


# --------------------------------------------------------------------------- argparse parents

def base_parser(description: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--url", default=None, help=f"AnkiConnect URL (default {CONFIG['url']}, env ANKI_URL)")
    p.add_argument("--dry-run", action="store_true", help="show what would happen; write nothing")
    p.add_argument("--json", action="store_true", help="machine-readable JSON on stdout")
    p.add_argument("-v", "--verbose", action="store_true")
    return p


def add_selection_args(p: argparse.ArgumentParser, required: bool = True) -> None:
    g = p.add_argument_group("note selection (one of)")
    g.add_argument("--ids", help="comma-separated note ids")
    g.add_argument("--query", help='Anki search, e.g. "deck:ai-teach-me tag:media::subtitles"')
    g.add_argument("--last", type=int, metavar="N", help="N most recently created notes in --deck")
    g.add_argument("--deck", default=None, help=f"deck for --last (default {CONFIG['deck']})")
    p.set_defaults(_selection_required=required)


def select_note_ids(client: AnkiClient, args: argparse.Namespace) -> List[int]:
    if getattr(args, "ids", None):
        return [int(x) for x in re.split(r"[,\s]+", args.ids.strip()) if x]
    if getattr(args, "query", None):
        return client.find_notes(args.query)
    if getattr(args, "last", None):
        deck = args.deck or CONFIG["deck"]
        ids = client.find_notes(f'"deck:{deck}"')
        return sorted(ids, reverse=True)[: args.last]
    if getattr(args, "_selection_required", True):
        raise SystemExit("error: select notes with --ids, --query or --last N")
    return []


# --------------------------------------------------------------------------- note JSON format

def info_to_json(info: Dict[str, Any], deck: Optional[str] = None) -> Dict[str, Any]:
    """AnkiConnect notesInfo -> interchange format."""
    return {
        "id": info["noteId"],
        "deck": deck,
        "model": info["modelName"],
        "tags": info.get("tags", []),
        "fields": {k: v["value"] for k, v in info["fields"].items()},
    }


def export_notes(client: AnkiClient, ids: List[int]) -> List[Dict[str, Any]]:
    infos = client.notes_info(ids)
    # deck comes from the first card of each note
    card_ids = [i["cards"][0] for i in infos if i.get("cards")]
    decks: Dict[int, str] = {}
    if card_ids:
        for c in client("cardsInfo", cards=card_ids):
            decks[c["note"]] = c["deckName"]
    return [info_to_json(i, decks.get(i["noteId"])) for i in infos]


def json_to_add_note(n: Dict[str, Any], deck: Optional[str], model: Optional[str], extra_tags: List[str],
                     allow_dup: bool, dup_scope: str) -> Dict[str, Any]:
    deck_name = n.get("deck") or deck or CONFIG["deck"]
    base = CONFIG["base_tags"] if deck_name == CONFIG["deck"] else []   # base_tags belong to the default deck only
    tags = list(dict.fromkeys([*base, *n.get("tags", []), *extra_tags]))
    return {
        "deckName": deck_name,
        "modelName": n.get("model") or model or CONFIG["model"],
        "fields": n["fields"],
        "tags": tags,
        "options": {"allowDuplicate": allow_dup, "duplicateScope": dup_scope},
    }


# --------------------------------------------------------------------------- Markdown card format

def _fence_to_html(text: str) -> str:
    """```lang ... ``` -> <pre><code>escaped<br>...</code></pre> (Anki-safe, escaped exactly once)."""
    def repl(m: "re.Match[str]") -> str:
        code = _html.escape(m.group(2).rstrip("\n"), quote=False)
        return "<pre><code>" + code.replace("\n", "<br>") + "</code></pre>"
    return re.sub(r"```([^\n]*)\n(.*?)```", repl, text, flags=re.S)


def _parse_kv(line: str) -> Optional[Tuple[str, Any]]:
    m = re.match(r"^(\w+):\s*(.*)$", line)
    if not m:
        return None
    k, v = m.group(1), m.group(2).strip()
    if k == "tags":
        v = [t.strip() for t in re.split(r"[,\s]+", v.strip("[]")) if t.strip()]
    return k, v


def parse_markdown_cards(text: str) -> List[Dict[str, Any]]:
    """See README.md: optional front-matter (defaults), then one card per '# ' heading,
    optional key: value lines under the heading, then '## <field name>' sections (HTML + fenced code)."""
    defaults: Dict[str, Any] = {}
    body = text.lstrip("﻿")
    fm = re.match(r"^---\n(.*?)\n---\n", body, flags=re.S)
    if fm:
        for line in fm.group(1).splitlines():
            kv = _parse_kv(line)
            if kv:
                defaults[kv[0]] = kv[1]
        body = body[fm.end():]

    cards: List[Dict[str, Any]] = []
    for title, rest in _split_headings(body.split("\n"), "# ")[1:]:
        card: Dict[str, Any] = {"title": title.strip(), "fields": {}, "tags": list(defaults.get("tags", []))}
        for k in ("deck", "model"):
            if k in defaults:
                card[k] = defaults[k]
        head, *sections = _split_headings(rest, "## ")
        # key: value lines before the first '## '
        for line in head[1]:
            kv = _parse_kv(line)
            if kv:
                if kv[0] == "tags":
                    card["tags"] = list(dict.fromkeys([*card["tags"], *kv[1]]))
                else:
                    card[kv[0]] = kv[1]
        for name, content in sections:
            card["fields"][name.strip()] = _fence_to_html("\n".join(content).strip())
        cards.append(card)
    return cards


def _split_headings(lines: List[str], prefix: str) -> List[Tuple[Optional[str], List[str]]]:
    """Split lines at headings starting with `prefix`, ignoring lines inside ``` fences.
    Returns [(None, lines before the first heading), (heading text, lines under it), ...]."""
    parts: List[Tuple[Optional[str], List[str]]] = [(None, [])]
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith(prefix):
            parts.append((line[len(prefix):], []))
            continue
        parts[-1][1].append(line)
    return parts


def load_cards_file(path: str) -> List[Dict[str, Any]]:
    text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    if path != "-" and path.lower().endswith((".md", ".markdown")):
        return parse_markdown_cards(text)
    stripped = text.lstrip("﻿").lstrip()
    if stripped.startswith(("[", "{")):
        data = json.loads(stripped)
        return data if isinstance(data, list) else [data]
    return parse_markdown_cards(text)


# --------------------------------------------------------------------------- HTML -> speech

CJK_RE = re.compile(r"[　-〿一-鿿＀-￯]+")
SOUND_RE = re.compile(r"\[sound:[^\]]+\]")


class _SpeechSplitter(HTMLParser):
    """Convention (matches the ai-teach-me cards):
    - elements styled color:#888 (or data-lang="zh") -> Chinese
    - <pre>, data-lib-banner, <img>, [sound:] -> skipped
    - glossary block (from glossary_start text until glossary_end text): <strong> term -> EN, whole <li> -> ZH
    - remaining text -> English; embedded CJK either stripped or moved to ZH (cjk_in_en)
    """
    VOID = {"br", "hr", "img", "input", "meta", "link"}

    def __init__(self, grey: str, g_start: str, g_end: str, skip_pre: bool, cjk_in_en: str):
        super().__init__()
        self.grey, self.g_start, self.g_end, self.skip_pre, self.cjk_in_en = grey, g_start, g_end, skip_pre, cjk_in_en
        self.en: List[str] = []
        self.zh: List[str] = []
        self.stack: List[Optional[str]] = []
        self.glossary = False
        self.in_strong = False
        self.li_buf: Optional[List[str]] = None

    def _mode(self) -> Optional[str]:
        for m in reversed(self.stack):
            if m:
                return m
        return None

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        a = dict(attrs)
        if tag not in self.VOID:
            mode = None
            if (tag == "pre" and self.skip_pre) or "data-lib-banner" in a or a.get("data-lang") == "skip":
                mode = "skip"
            elif a.get("data-lang") == "zh" or (self.grey and self.grey in (a.get("style") or "")):
                mode = "grey"
            elif a.get("data-lang") == "en":
                mode = "en"
            self.stack.append(mode)
        if tag == "strong":
            self.in_strong = True
        if tag == "li" and self.glossary:
            self.li_buf = []
        if tag in ("p", "li", "div", "br", "tr", "h1", "h2", "h3"):
            self.en.append("\n")
            self.zh.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag not in self.VOID and self.stack:
            self.stack.pop()
        if tag == "strong":
            self.in_strong = False
        if tag == "li" and self.li_buf is not None:
            self.zh.append("".join(self.li_buf))
            self.li_buf = None

    def handle_data(self, data: str) -> None:
        mode = self._mode()
        if mode == "skip":
            return
        t = data.strip("\n")
        if not t.strip():
            return
        if self.g_start and self.g_start in t:
            self.glossary = True
            self.en.append(self.g_start + ". ")
            return
        if self.g_end and self.g_end in t:
            self.glossary = False
        if mode == "grey":
            self.zh.append(t)
            return
        if self.glossary and self.li_buf is not None:
            self.li_buf.append(t)
            if self.in_strong:
                self.en.append(t + ". ")
            return
        if mode == "en":
            self.en.append(t)
            return
        if self.cjk_in_en == "zh":
            for m in CJK_RE.finditer(t):
                self.zh.append(m.group(0) + " ")
        self.en.append(CJK_RE.sub(" ", t))


def _tidy(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def _tidy_en(text: str) -> str:
    text = _tidy(text)
    text = re.sub(r"\s*/\s*(?=[:(])", "", text)      # "Sound effects / :" -> "Sound effects:"
    text = re.sub(r"\[\s*\]", "", text)               # "[ ]" left from stripped CJK
    text = re.sub(r",\s*(?=[,\n]|$)", "", text)       # dangling commas
    text = re.sub(r"[ ,/]+\n", "\n", text)
    return text.strip()


def html_to_speech(html_src: str, grey: Optional[str] = None, glossary_start: Optional[str] = None,
                   glossary_end: Optional[str] = None, skip_pre: bool = True,
                   cjk_in_en: str = "strip") -> Tuple[str, str]:
    """Return (english_text, chinese_text) to be spoken for one field."""
    p = _SpeechSplitter(
        grey=CONFIG["grey_style"] if grey is None else grey,
        g_start=CONFIG["glossary_start"] if glossary_start is None else glossary_start,
        g_end=CONFIG["glossary_end"] if glossary_end is None else glossary_end,
        skip_pre=skip_pre, cjk_in_en=cjk_in_en,
    )
    p.feed(_html.unescape(SOUND_RE.sub("", html_src)))
    return _tidy_en("".join(p.en)), _tidy("".join(p.zh))


def split_plain_by_script(text: str) -> Tuple[str, str]:
    """For plain text (no HTML convention): CJK runs -> zh, the rest -> en."""
    zh = " ".join(m.group(0) for m in CJK_RE.finditer(text))
    en = CJK_RE.sub(" ", text)
    return _tidy_en(en), _tidy(zh)


# --------------------------------------------------------------------------- TTS

def _edge_kwargs(rate: Optional[str], pitch: Optional[str], volume: Optional[str]) -> Dict[str, str]:
    return {"rate": rate or CONFIG["rate"], "pitch": pitch or CONFIG["pitch"], "volume": volume or CONFIG["volume"]}


async def tts_edge_async(text: str, voice: str, out: Path, rate: Optional[str] = None, pitch: Optional[str] = None,
                         volume: Optional[str] = None, subtitles: Optional[Path] = None, retries: int = 3) -> None:
    import edge_tts  # lazy: only needed for this engine
    last: Optional[Exception] = None
    for attempt in range(retries):
        try:
            comm = edge_tts.Communicate(text, voice, **_edge_kwargs(rate, pitch, volume))
            if subtitles is None:
                await comm.save(str(out))
            else:
                sub = edge_tts.SubMaker()
                with open(out, "wb") as f:
                    async for chunk in comm.stream():
                        if chunk["type"] == "audio":
                            f.write(chunk["data"])
                        elif chunk["type"] == "WordBoundary":
                            sub.feed(chunk)
                subtitles.write_text(sub.get_srt(), encoding="utf-8")
            return
        except Exception as e:
            last = e
            await asyncio.sleep(1.0 * (attempt + 1))
    raise RuntimeError(f"edge-tts failed after {retries} tries: {last}")


def tts_sapi(text: str, voice: Optional[str], out: Path, rate: int = 0) -> None:
    """Offline fallback: Windows System.Speech -> WAV. rate: -10..10."""
    txt = out.with_suffix(".sapi.txt")
    txt.write_text(text, encoding="utf-8")
    ps = f"""
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
{f'$s.SelectVoice("{voice}")' if voice else ''}
$s.Rate = {rate}
$s.SetOutputToWaveFile("{out}")
$s.Speak([IO.File]::ReadAllText("{txt}", [Text.Encoding]::UTF8))
$s.Dispose()
"""
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], check=True)
    txt.unlink(missing_ok=True)


def synthesize(text: str, voice: str, out: Path, engine: str = "edge", **kw: Any) -> Path:
    """Blocking one-shot TTS. Returns the written path (extension may change for sapi)."""
    if engine == "sapi":
        out = out.with_suffix(".wav")
        tts_sapi(text, voice, out, rate=int(kw.get("sapi_rate", 0)))
        return out
    asyncio.run(tts_edge_async(text, voice, out, kw.get("rate"), kw.get("pitch"), kw.get("volume"), kw.get("subtitles")))
    return out


async def synthesize_many(jobs: List[Tuple[str, str, Path]], rate: Optional[str] = None, pitch: Optional[str] = None,
                          volume: Optional[str] = None, concurrency: int = 4) -> None:
    """jobs: (text, voice, out_path). Runs edge-tts with bounded concurrency."""
    sem = asyncio.Semaphore(concurrency)

    async def one(text: str, voice: str, out: Path) -> None:
        async with sem:
            await tts_edge_async(text, voice, out, rate, pitch, volume)

    await asyncio.gather(*(one(*j) for j in jobs))


# --------------------------------------------------------------------------- backups

def backup_dir() -> Path:
    """CONFIG['backup_dir']: absolute, or relative to the scripts folder."""
    d = Path(CONFIG["backup_dir"])
    d = d if d.is_absolute() else HERE / d
    d.mkdir(parents=True, exist_ok=True)
    return d


def _stamp() -> str:
    return f"{_dt.datetime.now():%Y%m%d-%H%M%S}"


def _unique(path: Path) -> Path:
    """Never overwrite an earlier backup written in the same second."""
    n, cand = 1, path
    while cand.exists():
        n += 1
        cand = path.with_name(f"{path.stem}-{n}{path.suffix}")
    return cand


def record_backup(path: Path, tool: str, what: str, context: str = "") -> None:
    """Append one line to INDEX.md in the backup dir: when, which tool, what was saved, why."""
    idx = backup_dir() / "INDEX.md"
    if not idx.exists():
        idx.write_text("# anki-cards backups\n\nWritten automatically by the scripts in "
                       "`E:\\GitHub\\scil\\ai-skills\\skills\\anki-cards\\scripts\\` before they change anything.\n"
                       "Restore notes with `anki_update.py --file <backup>.json`; restore templates / HyperTTS config "
                       "with `anki_config_HyperTTS_realtime.py --restore <backup>`.\n\n| when | tool | file | what | context |\n|---|---|---|---|---|\n",
                       encoding="utf-8")
    with idx.open("a", encoding="utf-8") as f:
        f.write(f"| {_dt.datetime.now():%Y-%m-%d %H:%M:%S} | `{tool}` | `{path.name}` | {what} | {context} |\n")


def backup_notes(client: AnkiClient, ids: List[int], label: str, context: str = "") -> Optional[Path]:
    if not ids:
        return None
    path = _unique(backup_dir() / f"{_stamp()}-{label}.json")
    path.write_text(json.dumps(export_notes(client, ids), ensure_ascii=False, indent=2), encoding="utf-8")
    record_backup(path, f"anki_{label}.py", f"{len(ids)} note(s) before {label}", context)
    return path


def backup_file(src: Path, label: str, tool: str, what: str, context: str = "") -> Path:
    """Copy an arbitrary file (e.g. an add-on's meta.json) into the backup dir and index it."""
    dst = _unique(backup_dir() / f"{_stamp()}-{label}{src.suffix}")
    dst.write_bytes(src.read_bytes())
    record_backup(dst, tool, what, context)
    return dst


def backup_json(data: Any, label: str, tool: str, what: str, context: str = "") -> Path:
    dst = _unique(backup_dir() / f"{_stamp()}-{label}.json")
    dst.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    record_backup(dst, tool, what, context)
    return dst


def run(main_fn: Any) -> None:
    """Entry-point wrapper: AnkiConnect problems become a one-line error, not a traceback."""
    try:
        main_fn()
    except AnkiError as e:
        raise SystemExit(f"error: {e}")
    except KeyboardInterrupt:
        raise SystemExit(130)


def strip_html(s: str, limit: int = 80) -> str:
    t = re.sub(r"<[^>]+>", " ", _html.unescape(s))
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= limit else t[: limit - 1] + "…"
