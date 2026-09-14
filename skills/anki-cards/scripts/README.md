# anki-cards scripts

Python 3.9+ CLI tools for the `anki-cards` skill. They talk to Anki through the
**AnkiConnect** add-on (Anki must be open) and to Microsoft's neural TTS through **edge-tts**.

```bash
python -m pip install edge-tts          # only needed for audio
python scripts/anki.py ping             # -> {"version": 6}
```

| Script | Purpose |
|---|---|
| `anki.py <cmd>` | single entry point: `info` `add` `update` `audio` `media` `delete` `realtime` `tts` `ping` |
| `anki_info.py` | read-only: decks / models / fields / tags / stats; find, show, export notes; `--browse`, `--sync` |
| `anki_add.py` | add notes from a `.md` or `.json` cards file; `--audio` chains into `anki_audio.py` |
| `anki_update.py` | set / append / prepend / regex-replace fields, add / remove / rename tags, move deck; bulk from JSON |
| `anki_audio.py` | generate EN + ZH TTS clips per field and attach `[sound:…]`; `--replace`, `--remove`, `--dry-run` |
| `anki_media.py` | store / get / list / delete media; `--check` missing refs; `--orphans` |
| `anki_delete.py` | delete notes (preview by default, `--yes` to act) |
| `anki_config_HyperTTS_realtime.py` | HyperTTS **Realtime** audio for a note type: writes the add-on preset + the `{{tts}}` template tag; `--preset` (edit a preset only), `--rule`, `--error-mode`, `--show`, `--check`, `--remove`, `--restore`, `--export` / `--import` |
| `tts.py` | standalone text → mp3/wav (edge-tts or Windows SAPI); `--split-lang`, `--list-voices` |
| `anki_lib.py` | shared: client, formats, HTML→speech splitter, TTS, backups |
| `anki.json` | defaults (url, deck, model, voices, rate, …) |

Common flags on every `anki_*` script: `--url`, `--dry-run`, `--json`, `-v`.
Note selection (where applicable): `--ids 1,2,3` | `--query "<anki search>"` | `--last N [--deck D]`.

**Backups.** `anki_update.py`, `anki_audio.py`, `anki_delete.py`, `anki_config_HyperTTS_realtime.py` save what they are
about to change into `backup_dir` (anki.json; currently `D:\A\Scoop\persist\anki\backups\anki-cards\`,
next to Anki's own data so it survives Scoop updates) and append a row to `INDEX.md` there:
when · tool · file · what · context. Restore notes with `anki_update.py --file <backup>.json`;
restore templates + HyperTTS config with `anki_config_HyperTTS_realtime.py --restore <stamp>`.
HyperTTS `meta.json` backups contain the Azure key in plain text — don't share them.

---

## File formats

### 1. Note interchange JSON (`anki_info.py --out`, `anki_add.py --file`, `anki_update.py --file`)

A list of notes. `id` is present on export and required for `anki_update.py --file`; ignored by `anki_add.py`.
`deck` / `model` / `tags` are optional on add (fall back to CLI flags, then `anki.json`).

```json
[
  {
    "id": 1789190587573,
    "deck": "ai-teach-me",
    "model": "问答题",
    "tags": ["ai-teach-me", "media::subtitles"],
    "fields": { "正面": "<div>…html…</div>", "背面": "<p>…html…</p>" }
  }
]
```

Field values are **raw Anki HTML** — exactly what is stored in the note. Escape literal `<`, `>`, `&`
once (`&lt;` …). Cloze notes use the model `填空题` with fields `文字` / `背面额外`.

### 2. Markdown cards file (`anki_add.py --file cards.md`) — see `templates/card.md`

```markdown
---                        ← optional front-matter: defaults for every card
deck: ai-teach-me
model: 问答题
tags: [topic::x, lib::y]   ← merged with anki.json base_tags and --tags
---

# Any title                ← one card per "# " heading (title is not stored)
tags: [only::this-card]    ← optional per-card key: value lines (deck / model / tags)

## 正面                     ← "## <field name>" — must match the model's field names
…HTML…
## 背面
…HTML…
```

- Section bodies are **HTML as-is**, with one convenience: fenced code blocks
  ```` ```lang … ``` ```` become `<pre><code>…</code></pre>` with `<`, `>`, `&` escaped and
  newlines turned into `<br>` — so write code raw inside fences, never pre-escaped.
- A `.json` file (or stdin starting with `[`/`{`) is parsed as the interchange format instead.

### 3. Speech convention (what `anki_audio.py` reads aloud from a field)

| HTML | Spoken as |
|---|---|
| element with `style="…color:#888…"` or `data-lang="zh"` | **Chinese** clip |
| `data-lang="en"` | **English** clip (even if it contains CJK) |
| `<pre>` (unless `--no-skip-pre`), `data-lib-banner`, `data-lang="skip"`, `[sound:…]`, `<img>` | not spoken |
| glossary block: from the text `English vocabulary` to `Memory line` | `<strong>` terms → English clip; each whole `<li>` (term + gloss) → Chinese clip |
| everything else | English clip; embedded CJK stripped (`--cjk-in-en zh` moves it to the Chinese clip instead) |

Output per note (default `audio_langs: "en"`): `<prefix>-front-en.mp3` and `<prefix>-back-en.mp3`
(prefix defaults to `note<id>`), stored in `collection.media`, and a `<div>[sound:…]</div>` appended
to the field (`--position start` to prepend). `--lang en,zh` (or `audio_langs` in `anki.json`) adds
`…-front-zh.mp3` / `…-back-zh.mp3`; Anki then plays English first, then Chinese. English-only keeps
media at roughly 0.3 MB per card, which matters for the AnkiWeb media quota.

**When to use this at all:** only for note types whose templates have *no* realtime tag (see §4) or
when files are explicitly wanted (offline phone use). `问答题` / `填空题` in both profiles are on
realtime now — `[sound:]` files there would play twice. Strip old ones with
`anki_audio.py --query … --remove --delete-media`.

### 4. HyperTTS Realtime (`anki_config_HyperTTS_realtime.py`)

Realtime = no audio files: Anki's built-in `{{tts}}` tag in the card template, answered at review time
by the HyperTTS add-on (desktop, Azure neural voices) or by a system voice (mobile). Two things must
agree, and the script writes both:

1. **The add-on preset** in `<anki data>/addons21/111623432/meta.json` → `config.realtime_config.realtime_N`
   with a `front` / `back` side each: `source` (`field_name`, `field_type` = `Regular|Cloze|ClozeOnly`),
   `voice_selection` (`{"voice_key": {"name": "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)"}, "service": "Azure"}` —
   Azure voices use this long name; the script converts short `en-US-JennyNeural` and validates against
   the add-on's `services/voicelist.py`), `text_processing`
   (regex rules run after HTML stripping; the `--strip-cjk` rule is `[　-〿一-鿿＀-￯]+ → " "`).
2. **The template tag**: `{{tts en_US hypertts_preset=Front_realtime_N voices=HyperTTS[,fallbacks]:cloze:文字}}`
   appended to the Front / Back template. `Front_`/`Back_` + key selects the side; `cloze:` / `cloze-only:`
   are Anki's own filters (front reads the deletion as "blank", back reads it revealed / only it).

Side spec on the command line: `--front FIELD[:TYPE[:VOICE]]` / `--back …`, TYPE = `Regular|Cloze|ClozeOnly`
(default Regular), VOICE = Azure short name (default `en_voice`). Text rules: `--strip-cjk front,back`,
`--rule REGEX REPL` (repeatable, both sides). `--error-mode Tooltip|Nothing|Dialog` sets how HyperTTS reports
realtime errors (empty text on image-only cards raises `SourceTextEmpty` — use `Tooltip`).
`--preset realtime_N` edits that preset's voices/rules without touching any template — needed when the
preset is referenced by a note type in *another* profile (presets are global, templates are per profile).

**Voice rule (user, 2026-09-12): English voices only.** Any field may contain English and the user is
learning English, so never a Chinese voice. Text that is normally English → `en-US-JennyNeural` +
`--strip-cjk`. A field that may be *entirely* Chinese (e.g. a Chinese prompt) →
`en-US-JennyMultilingualNeural` **without** stripping: English by default, native Chinese only for
Chinese runs. Multilingual voices are served on the Azure F0 tier (verified). Plain Jenny mangles
Chinese; Xiaoxiao reads English with Chinese prosody — both wrong for this purpose.

Facts that shape the workflow:
- HyperTTS loads `meta.json` **once at startup** and writes its in-memory copy back whenever one of its
  dialogs saves → **restart Anki right after `anki_config_HyperTTS_realtime.py`**, and don't open HyperTTS dialogs in between.
- The preset key is reused if the model's template already carries one (`existing_key`), so re-running is
  idempotent; otherwise the next free `realtime_N` is allocated.
- Presets live in the shared `addons21` folder, so one preset can serve same-named note types in several
  profiles (`realtime_0` = 填空题 in Caoxie and Yuan); but each profile's template needs its own tag.
- Anki hands HyperTTS plain text, so `<pre>` code blocks and banner lines *are* read aloud on
  `ai-teach-me` cards — accepted trade-off of realtime mode.
- AnkiWeb syncs templates (so the tag reaches every device) but **not** add-on config. To move the presets:
  `--export presets.json` here (no API keys inside), then on the other desktop install HyperTTS + enable Azure,
  `--import presets.json`, restart Anki, sync, `--check`. Phones fall back to the first available `voices=`
  entry or any system voice for the language.
- Anki hands HyperTTS the field **after** HTML stripping and cloze rendering, so `<pre>` blocks can't be
  skipped here (unlike `anki_audio.py`); only regex on plain text is possible.
- `--show` redacts API keys; the raw `meta.json` contains them.

### 5. `anki.json`

```json
{
  "url": "http://127.0.0.1:8765",
  "deck": "ai-teach-me", "model": "问答题", "fields": ["正面", "背面"],
  "base_tags": ["ai-teach-me"],
  "en_voice": "en-US-JennyNeural", "zh_voice": "zh-CN-XiaoxiaoNeural",
  "audio_langs": "en",
  "rate": "+0%", "pitch": "+0Hz", "volume": "+0%",
  "backup_dir": "D:/A/Scoop/persist/anki/backups/anki-cards",
  "grey_style": "#888", "glossary_start": "English vocabulary", "glossary_end": "Memory line"
}
```
`ANKI_URL` env var and `--url` override `url`. `backup_dir` may be absolute or relative to `scripts/`.

---

## Typical flows

```bash
S=E:/GitHub/scil/ai-skills/skills/anki-cards/scripts

# author → preview → add  (no --audio for 问答题/填空题: their templates carry realtime audio)
python $S/anki_add.py --file cards.md --dry-run
python $S/anki_add.py --file cards.md

# pre-generated files, only for note types without a realtime tag
python $S/anki_audio.py --last 3 --dry-run            # see what would be spoken
python $S/anki_add.py --file cards.md --audio --en-voice en-US-JennyNeural

# fix text across a tag
python $S/anki_update.py --query "tag:media::subtitles" --replace "Blu-ray" "Blu‑ray"

# export → hand-edit → import back
python $S/anki_info.py --last 3 --out review.json
python $S/anki_update.py --file review.json

# housekeeping
python $S/anki_media.py --check --query "deck:ai-teach-me"
python $S/anki_media.py --orphans --prefix note --delete-orphans --yes
python $S/anki_delete.py --query "tag:draft" --yes --delete-media

# standalone TTS
python $S/tts.py --file reply.md --out reply.mp3 --voice en-GB-RyanNeural --rate=-10%
python $S/tts.py --list-voices --lang zh

# HyperTTS Realtime (no media files) — run inside the named profile, then RESTART ANKI, then --check
# profile Yuan  (问答题 = Chinese prompt → English answer)
python $S/anki_config_HyperTTS_realtime.py --model 问答题 --front 正面:Regular:en-US-JennyMultilingualNeural --back 背面:Regular:en-US-JennyNeural --strip-cjk back
python $S/anki_config_HyperTTS_realtime.py --model 填空题 --front 文字:Cloze --back 文字:Cloze --strip-cjk front,back
# profile Caoxie (问答题 spans ai-teach-me / En / Gurmukhi → also strip Gurmukhi; image-only cards → Tooltip)
python $S/anki_config_HyperTTS_realtime.py --model 问答题 --front 正面:Regular:en-US-JennyNeural --back 背面:Regular:en-US-JennyNeural --strip-cjk front,back --rule "[\u0A00-\u0A7F]+" " " --error-mode Tooltip
python $S/anki_config_HyperTTS_realtime.py --model 填空题 --front 文字:Cloze --back 文字:Cloze --strip-cjk front,back
python $S/anki_config_HyperTTS_realtime.py --check
python $S/anki_config_HyperTTS_realtime.py --preset realtime_1 --front 正面:Regular:en-US-JennyMultilingualNeural --back 背面:Regular:en-US-JennyNeural --strip-cjk back   # edit a preset from any profile
python $S/anki_config_HyperTTS_realtime.py --model 问答题 --remove          # undo for one model
python $S/anki_config_HyperTTS_realtime.py --restore 20260912-170033        # undo from a backup stamp
python $S/anki_config_HyperTTS_realtime.py --export presets.json           # → other PC: --import presets.json
```

Current presets (2026-09-12): `realtime_0` = 填空题 (both profiles, Jenny, CJK stripped) ·
`realtime_1` = Yuan 问答题 (front Jenny-Multilingual unstripped, back Jenny stripped) ·
`realtime_2` = Caoxie 问答题 (Jenny, CJK + Gurmukhi stripped).

## Gotchas
- **Read-after-write can be stale**: a `notesInfo` right after `updateNoteFields` may show the old
  value. The scripts avoid relying on it; verify in a later call, don't retry blindly.
- Chinese survives because every request is sent as UTF-8 bytes; stdout is forced to UTF-8 too.
- `edge-tts` is an unofficial endpoint: occasional 403/timeouts are retried 3×; if it keeps failing,
  `tts.py --engine sapi` works offline (worse voices, WAV output).
- `anki.ps1` in the skill root is the older PowerShell helper; the Python scripts supersede it.
