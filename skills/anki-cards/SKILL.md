---
name: anki-cards
description: Turn newly-learned concepts/technology from a conversation (or a given term list) into bilingual (English-first) Anki flashcards — atomic Q&A + cloze + linking cards — and push them into Anki via the scripts in scripts/ (AnkiConnect), optionally with EN/ZH TTS audio. Also covers editing, re-voicing, and deleting existing cards. Use when the user wants to "做成 Anki 卡 / 复习卡片 / 把知识存进 Anki / 收录到 anki / 加音频". Personal skill; needs Anki open with the AnkiConnect add-on.
---

# Anki cards

Distill the concepts that are **new to the user** from a conversation into flashcards and, on confirmation, add them to Anki. Also works on a term list the user gives.

## Tooling
All Anki operations go through the Python scripts in `scripts/` (docs + file formats:
[`scripts/README.md`](scripts/README.md)). `S` below = this skill's `scripts/` directory.

| Task | Command |
|---|---|
| probe / inspect | `python $S/anki.py ping` · `anki_info.py --decks --models --fields 问答题 --tags` |
| see recent / find notes | `anki_info.py --last 5 --format table` · `--query "tag:x"` · `--out review.json` |
| add cards | write `cards.md` (format below) → `anki_add.py --file cards.md --dry-run` → without `--dry-run` |
| add + audio | `anki_add.py --file cards.md --audio` |
| edit existing | `anki_update.py --ids … --replace PAT REPL` / `--set-file 背面=x.html` / `--add-tags` / `--file review.json` |
| audio for existing | `anki_audio.py --ids … [--dry-run]` · `--replace` to regenerate |
| delete | `anki_delete.py --ids … --yes [--delete-media]` (always previews first) |
| media | `anki_media.py --check --query "deck:ai-teach-me"` · `--orphans --prefix note` |
| realtime audio (no files) | `anki_config_HyperTTS_realtime.py --model … --front F:TYPE:VOICE --back …` → **restart Anki** → `--check` (see "Realtime audio") |

Every script: `--dry-run`, `--json`, `--url`. Update/audio/delete/realtime back up what they change to
`D:\A\Scoop\persist\anki\backups\anki-cards\` (with an `INDEX.md` row: tool, file, what, context) before
writing. `anki.ps1` (skill root) is the legacy PowerShell helper — do not use it for new work.

## Two ways to get audio — pick per deck
- **Realtime** (`anki_config_HyperTTS_realtime.py`): a `{{tts}}` tag in the card template, spoken at review time by the
  HyperTTS add-on with Azure voices on desktop, by a system voice on phones. Zero media, cloze-aware
  through Anki's own `cloze` / `cloze-only` filters. **Current choice in both profiles** (`Caoxie` and
  `Yuan`) for `问答题` and `填空题` — so cards this skill adds to `ai-teach-me` already have audio;
  **do not pass `--audio`** for those note types.
- **Pre-generated files** (`anki_add.py --audio` / `anki_audio.py`): `[sound:]` MP3s in the collection,
  edge-tts neural voices, works offline and on every device, counts against the AnkiWeb media quota
  (~0.3 MB per card English-only). Only for note types / decks without a realtime tag, or when the
  user explicitly wants files (offline phone use).
- Never mix both on the same cards — they'd play twice (`anki_audio.py --remove --delete-media` first).

## Prerequisites
- Anki desktop **open**, with the **AnkiConnect** add-on (`http://127.0.0.1:8765`). Probe first:
  `python $S/anki.py ping` (prints `{"version": 6}` if reachable).
- Audio needs `python -m pip install edge-tts` (once).
- If unreachable → do NOT fail; still write `cards.md` (the add script's input) so the user can
  run `anki_add.py --file cards.md` later, and tell them so.

## Defaults (this machine's Anki — also in `scripts/anki.json`)
- Deck: **ai-teach-me** (`anki_add.py --create-deck` if missing). Cards added to this deck get the
  base tag `ai-teach-me` automatically; other decks do not.
- Note types & their fields (Chinese — do not assume Front/Back):
  - `问答题` (Basic) — fields `正面` / `背面`
  - `问答题（同时生成翻转的卡片）` (Basic + reversed) — `正面` / `背面`
  - `填空题` (Cloze) — `文字` / `背面额外`  (cloze text uses `{{c1::…}}`)
- Card-type mapping: concepts/Q&A → Basic; hard facts → a few Cloze; term↔definition & 对比/关系 → reversed.
- Audio: realtime via HyperTTS for `问答题` / `填空题` (see below). When files are generated instead:
  **English clips only by default** (`audio_langs: "en"`); `--lang en,zh` adds Chinese. Voices
  `en-US-JennyNeural` / `zh-CN-XiaoxiaoNeural`; override with `--en-voice` / `--zh-voice` / `--rate`.
  **The user wants English voices everywhere** (learning English) — never a Chinese voice; for text
  that may be entirely Chinese use `en-US-JennyMultilingualNeural`.

## Workflow
1. **Pick** genuinely-new, worth-understanding concepts; skip what the user clearly knows / pure project trivia. Merge closely-related (e.g. NFC/NFKC). Order shallow→deep.
2. **Atomic cards** — build every technical card with the required anatomy below. Split one concept into several small notes, but keep enough background on each note for it to stand alone months later. Lead with the situation, not the term.
3. **Linking cards (必做)** — comparison / relationship / structure / "one method, many uses" cards that connect a cluster; shared `::` tag (e.g. `unicode::skeleton`). A linking card must state a relation that **no single member card already states** — see the no-redundancy rule below.
4. **Tags (every note)** — `ai-teach-me` (auto) + 1–3 `::`-hierarchy topic tags + the `lib::` tag from the stack-attribution rule below; lowercase-kebab, ≤5 per note, reuse existing tags (`anki_info.py --tags` first).
5. **Author `cards.md`** (Write tool) in the Markdown cards format — front-matter for deck/model/shared
   tags, one `# ` heading per card, `## 正面` / `## 背面` (or `## 文字` / `## 背面额外`) sections, code
   in fenced blocks (the script escapes them). Start from `scripts/templates/card.md`.
6. **Confirm before writing** — this writes to the user's REAL Anki. Run
   `anki_add.py --file cards.md --dry-run` (validates field names against the model and shows each
   card's first line), show the user the candidate cards (front/back or cloze + tags), then write.
7. **Write** — `anki_add.py --file cards.md`. No `--audio` for `问答题` / `填空题` (realtime audio
   is in their templates); add `--audio` only for a note type without a realtime tag or on explicit
   request. Report the new ids and `anki_info.py --stats`.
8. **Learning notes** — optionally also save the human-readable cards to a notes file for the user (ask path). Do NOT put these in the agent memory system (that's for the agent's own working context).

## Style & quality

**The test for every card: could the user answer it three months from now, having forgotten
this conversation entirely?** If the back needs re-deriving from compressed jargon, rewrite it.
Compression is the enemy here — a card is not an index entry.

### Required anatomy for every technical card (必做)

A technical card must be self-contained enough that a beginner can recover the original lesson
months later without the conversation, repository, or project nouns. Use this order:

1. **Scope banner** — name the library/stack, or say the principle is general. Follow the stack-
   attribution rules below.
2. **Independent, familiar scenario** — explain who is doing what, what they expect, and what goes
   wrong. Rebuild project-specific incidents as a todo list, article editor, product grid, shopping
   cart, photo editor, or another context that makes sense on its own.
3. **Plausible broken code** — show a small complete component/function, not an extracted fragment.
   The reader should be able to see why the wrong version looked reasonable.
4. **Plain-language conclusion first** — answer in one ordinary sentence before naming the
   abstraction. Follow it with an analogy when one materially helps.
5. **Mechanism and context** — walk through the relevant timeline, state changes, ownership, or
   data flow one step at a time. Explain why the bug happens, what information is lost, and what the
   user observes; do not jump from symptom to rule.
6. **Corrected key code** — show the fixed complete component/function or a complete focused
   before/after. Explain why each load-bearing line exists and what invariant it restores.
7. **English vocabulary section** — teach several useful terms from the lesson inline with Chinese.
   For every term, give its plain Chinese meaning, its meaning in this exact context, and any nearby
   term it is commonly confused with (for example `pending` vs `in-flight` vs `settled`, or `reset`
   vs `cancel` vs `abort`). Do not dump an unexplained word list. Heading text must be exactly
   `English vocabulary` and each entry `<li><strong>term</strong>：中文…</li>` — the audio script
   keys on this.
8. **One-sentence memory hook** — end with the smallest accurate sentence worth recalling, headed
   `Memory line:` (EN) / `记忆句：` (ZH).

### Bilingual layout (必做, since 2026-09-11): English first, Chinese right after

The user is learning English alongside the subject. Every section of a card is written **in English
first, then its Chinese version immediately after**, using this HTML convention (the audio script
depends on it — see `scripts/README.md` "Speech convention"):

- English text: plain elements (`<p>`, `<li>`, `<div>`).
- Chinese text: the same content in an element styled `style="color:#888"` — a following
  `<p style="color:#888">` for paragraphs, or `<br><span style="color:#888">…</span>` inside a `<li>`.
- Front: `<div>English question</div><div style="color:#888;margin-top:.4em">中文问题</div>` under the banner.
- Section labels: `Plain answer:` / `白话结论：`, `Analogy:` / `类比：`, `Memory line:` / `记忆句：`.
- Keep English terms inline in the Chinese text too (silent failure / rollback) — do not translate
  the technical term itself.
- Code blocks appear once (they are language-neutral); comments in code may be English.

Older cards in the deck are Chinese-first; do not rewrite them unless asked.

This structure is mandatory for technical Q&A cards even when it makes the back long. Long backs
are acceptable; missing context is not. Pure vocabulary, hard-fact Cloze, and linking cards may omit
broken/fixed code only when code would be artificial, but they still need scope, enough background
to stand alone, plain-language explanation, and contrasts with commonly confused terms.

- **通俗第一 (plain language first)** — explain it the way you would to a sharp colleague who
  lacks *this* context. Lead with the conclusion in one plain sentence, then an **analogy**, then
  the mechanism. Never open with an abstract principle.
- **写给小白 (必做)** — assume the reader knows the language but not this API, and has **zero**
  memory of the project the lesson came from. Two failure modes, both observed and both rejected
  by the user:
  - **Scenario built from project nouns.** A card opening "资料页的头像在冷启动时…" or using
    `useSession()` / `updateProfile()` is unreadable later — the reader cannot tell what is the
    library, what is the app, and what is the point. Rebuild the scenario out of something
    *anyone* recognises: a todo list, an article editor, a product grid, a shopping cart. The
    generic example is usually also the **clearer** one (every row spinning at once shows the
    shared-observer bug better than any real screen did).
  - **Compressed prose.** "判据是并发不是数量；排队在全局 MutationCache，跨实例仍串行" packs
    four ideas into one line and is unparseable cold. One idea per sentence, plain words first,
    the term named after the idea it labels.
  - Code must be **a small complete component**, readable top to bottom without imagining the
    rest of the file — not a two-line fragment lifted from real code.
- **For foundational APIs, go wide, not just deep** — when the subject is something like
  `useState` / `useQuery` / `useMutation`, the user wants the **core points and the contrasts**
  covered, not only the one bug that prompted the session: the gotcha that started it, plus the
  neighbouring traps a beginner hits, plus at least one card that lines the APIs up against each
  other. "少而精" governs *within* a topic; it is not a reason to leave a foundational API
  half-covered.
- **Give the background** — state the concrete situation that produces the problem ("你改了名，
  保存成功，但右上角菜单还是旧名字") before naming the concept. A card that starts at the
  abstraction is unanswerable later.
- **Code example in nearly every technical card.** Show a real snippet, not pseudocode. When the
  lesson is "the wrong version looks correct", show **before/after** — the value is re-experiencing
  why the broken one looked fine. Use `<pre><code>…</code></pre>` with `<br>` for newlines.
- **Bilingual**: English first, Chinese immediately after, per the layout rule above; keep the
  **English term inline** in the Chinese text too (silent failure / vacuous test / rollback).
- **Name the stack on every card (必做)** — see below.
- Cite the **standard / CVE / year** when relevant (NFC is a Unicode standard; Trojan Source =
  CVE-2021-42574, 2021).
- **少而精** — fewer, sharper cards beat many shallow ones. Long backs are fine; shallow ones are not.

### No redundancy (the #1 reason cards get deleted)

Before proposing a card, check it against the backs of the cards already in the batch:
**if its answer is already fully contained in another card's back, it is a duplicate in disguise —
merge it or drop it.** Splitting one idea into more cards is only "atomic" when each card carries
knowledge the others do not; re-asking the same fact from a new angle is just repetition the user
has to delete by hand.

Concrete traps, all observed:
- **Don't clozify a fact that a Q&A card already explains.** A cloze on "staged upload 是 single-use，
  promote 后变 consumed" adds nothing when a basic card's back already walks through exactly that.
- **Don't make a summary card out of a point every member card already makes.** If three cards each
  end with "所以 API 测试全绿，只有 e2e 抓得到", a fourth card asking "这三个有什么共同点?" is
  answered by any one of them.
- **Two linking cards on one cluster is usually one too many** — "有什么共同点" and "分别被哪层
  测试抓到" were the same insight twice.

A genuine linking card asks something **no member card can answer**: a contrast between two
mechanisms, a decision rule for choosing between them, or a structure that only appears when you
line them up.
- Mark **speculation as speculation**; never state guesses as fact. No secrets (passwords/tokens/keys).

### Stack / library attribution (必做)

Months later the user must be able to tell *"does this only hold for that library, or everywhere?"*
without opening the codebase. So **every technical card declares its scope in two places**:

1. **A banner line at the top of the front field** (so the scope is visible while answering):
   ```html
   <div data-lib-banner style="font-size:.8em;color:#888;margin-bottom:.5em">Better Auth · React client</div>
   ```
   - Library-specific → name it and the flavor: `Better Auth · React client`,
     `TanStack Query（useMutation onSuccess）`, `tRPC（靠 TRPCError.code 分流）`.
   - General principle → say so explicitly: `通用原则（不限库）· 例子来自 Drizzle 事务`.
     A card whose *conclusion* is universal but whose *examples* come from one library gets
     `Better Auth（举例）· 原则本身通用`.
   - The `data-lib-banner` marker makes the banner findable/idempotent for later scripts.
2. **A `lib::` tag** — `lib::better-auth`, `lib::tanstack-query`, `lib::trpc`, `lib::drizzle`,
   `lib::vitest`, `lib::playwright`. This axis is **orthogonal** to the topic tags: topic says
   *what it teaches*, `lib::` says *where it applies*. General-principle cards get no `lib::` tag
   (their banner already says "不限库"), and multiple libraries → multiple tags.

## Realtime audio (HyperTTS) — procedure

Prereqs: HyperTTS add-on (`111623432`) installed; a service enabled in *Tools → HyperTTS → Configure
Services* (Azure with the user's key — region `westus2` on this machine — or *Windows* for a dry run).
Confirm with `anki_config_HyperTTS_realtime.py --show` (keys are redacted; never print the raw `meta.json`).

1. Decide per side: field, type (`Regular` / `Cloze` = sentence with "blank" on front, revealed on back /
   `ClozeOnly` = answer only), voice, and whether to `--strip-cjk` (English-only reading; the regex drops
   CJK after HTML stripping). **Voice rule (user, 2026-09-12): always an English voice — never a
   Chinese one — because any field may contain English and the user is learning English.** English
   content → `en-US-JennyNeural` + `--strip-cjk`; a field that may be *entirely* Chinese (e.g. a
   Chinese prompt) → `en-US-JennyMultilingualNeural` **without** stripping (English voice that reads
   Chinese natively when it meets it; verified to work on Azure F0). Prefer `Cloze` on the back so the
   learner hears the whole phrase. For image-only cards set `--error-mode Tooltip` so empty text
   doesn't pop a dialog. A preset used by another profile can be edited with `--preset realtime_N`.
2. `anki_config_HyperTTS_realtime.py --model M --front … --back … --dry-run` → shows the resulting templates.
   Ask the user to confirm (it edits the note type, i.e. every card of that type, and the add-on config).
3. Run it without `--dry-run`. It backs up `meta.json` + the model's templates, writes preset
   `realtime_N` (reusing N if the template already has one), appends the `{{tts …}}` tags.
4. **Tell the user to restart Anki** (HyperTTS reads its config only at startup; opening any HyperTTS
   dialog before restarting can overwrite the edit). Then `anki_config_HyperTTS_realtime.py --check` → must print `ok: true`.
5. Verify by reviewing one card: play icon + autoplay; `R` replays.

Undo: `--model M --remove` (strips tags, disables the preset) or `--restore <stamp>` (both files back).

**Other computers.** Templates sync via AnkiWeb; add-on config does **not**. On the source PC:
`--export realtime-presets.json` (presets referenced by templates + the tags; contains no API key).
On the target PC: install HyperTTS `111623432`, enable Azure with the key + region, install
AnkiConnect, copy the `scripts/` folder, run `--import realtime-presets.json`, **restart Anki**, sync,
then `--check`. Without the scripts there: paste the exported `realtime_config` block into
`addons21/111623432/meta.json` → `config.realtime_config` while Anki is closed. Phones need nothing —
they fall back to a system voice (`--fallback-voices` picks which).

Current configuration (2026-09-12), reproducible with (run inside the named profile):
```bash
# profile Yuan  (问答题 = Chinese prompt → English answer)
python $S/anki_config_HyperTTS_realtime.py --model 问答题 --front 正面:Regular:en-US-JennyMultilingualNeural --back 背面:Regular:en-US-JennyNeural --strip-cjk back
python $S/anki_config_HyperTTS_realtime.py --model 填空题 --front 文字:Cloze --back 文字:Cloze --strip-cjk front,back
# profile Caoxie (问答题 spans ai-teach-me / En / Gurmukhi decks → also strip Gurmukhi script)
python $S/anki_config_HyperTTS_realtime.py --model 问答题 --front 正面:Regular:en-US-JennyNeural --back 背面:Regular:en-US-JennyNeural --strip-cjk front,back --rule "[\u0A00-\u0A7F]+" " " --error-mode Tooltip
python $S/anki_config_HyperTTS_realtime.py --model 填空题 --front 文字:Cloze --back 文字:Cloze --strip-cjk front,back
```
Presets: `realtime_0` = 填空题 (both profiles), `realtime_1` = Yuan 问答题, `realtime_2` = Caoxie 问答题.

## Gotchas (learned the hard way)
- Anki **renders HTML** in fields — to show a literal tag like `<bdi>` in prose, write `&lt;bdi&gt;`.
  **Code goes in fenced blocks in `cards.md`** — the add script escapes `<`, `>`, `&` and converts
  newlines to `<br>` — so write code **raw** inside fences, never pre-escaped.
- **Escape exactly once.** Prose in `cards.md` is HTML as-is (hand-escape there); fenced code is
  escaped by the script. Pre-escaping code inside a fence stores `&amp;lt;` and the card shows the
  literal `&lt;`.
- **Grep the batch for double-escaping after writing.** `&amp;(lt|gt|amp);` in any field is almost
  always the bug above. It is invisible in a tag-stripped preview, so check the **raw** field values
  (`anki_info.py --ids … --json`), in a separate later call per the read-after-write rule below.
- Reversed model = 2 cards/note; a 2-deletion cloze = 2 cards/note → deck card-count > note-count is normal.
- **Read-after-write is stale.** A `notesInfo` / `findNotes` issued right after a write — in the
  same script or the very next call — can still return the *pre-write* state, making a write that
  actually succeeded look like it failed. Do not retry on that basis (you will double-apply); verify
  in a **separate, later** call. The scripts print the AnkiConnect result; `null` error = success.
- **Match notes by their own text, not by tag**, when updating in bulk
  (`--query '"a distinctive phrase"'`) — a tag query can sweep in unrelated cards, and `added:1`
  also catches notes the user added by hand today. Prefer `--ids` from the add step's output.
- Never inline long Chinese+HTML in a shell argument — write `cards.md` / `x.html` with the Write
  tool and pass the file (`--file`, `--set-file`).
- **Audio**: run `anki_audio.py --dry-run` when the card layout is unusual — it prints exactly what
  each voice will read. The splitter keys on `color:#888` (Chinese), `<pre>` (skipped), the
  `English vocabulary` / `Memory line` labels; deviate from the layout and the clips come out wrong.
  `--replace` regenerates (and deletes the old media); the media name prefix is `note<id>` by default.
- **HyperTTS voice keys are the long Azure names** — `Microsoft Server Speech Text to Speech Voice
  (en-US, JennyNeural)`, not `en-US-JennyNeural`. A short name in `meta.json` gives "Voice not found"
  at review time. `anki_config_HyperTTS_realtime.py` converts short → long and validates against the add-on's
  `services/voicelist.py`; `--check` flags keys that aren't in that list.
- **HyperTTS config lives in memory.** Editing `addons21/111623432/meta.json` while Anki runs is only
  safe if Anki is restarted immediately afterwards and no HyperTTS dialog is opened in between — the
  add-on writes back its stale in-memory copy on any save. `anki_config_HyperTTS_realtime.py` prints this reminder.
- **Never dump `meta.json` or HyperTTS config to the conversation** — it holds the Azure API key in plain
  text. Use `anki_config_HyperTTS_realtime.py --show` (redacted). If a key does get exposed, tell the user to regenerate it.
- **Realtime tags are per note type, not per deck.** The same `问答题` type is used in several profiles /
  decks; check which profile is open (`anki_info.py --decks`) before applying.
- The user **curates after import** — they delete cards they do not want, and the reason is almost
  always **redundancy with another card in the same batch**, not card type. Never silently re-add a
  missing card; if notes disappear, report the exact counts and ask. Do not infer the reason for a
  deletion — ask, then encode the real answer here.

## Usage sketch
```bash
S=E:/GitHub/scil/ai-skills/skills/anki-cards/scripts
python $S/anki.py ping                                   # AnkiConnect up?
python $S/anki_info.py --tags                            # reuse existing tags
# … write cards.md (see scripts/templates/card.md) …
python $S/anki_add.py --file cards.md --dry-run          # validate + preview → show user
python $S/anki_add.py --file cards.md --audio --out ids.txt
python $S/anki_info.py --stats
# later fixes (ids from ids.txt / the add output)
python $S/anki_update.py --ids 1789190587573,1789190587580 --replace "old" "new"
python $S/anki_audio.py  --ids 1789190587573,1789190587580 --replace
```

Cloze cards: `model: 填空题` in the card's key lines, sections `## 文字` (with `{{c1::…}}`) and
optionally `## 背面额外`.
