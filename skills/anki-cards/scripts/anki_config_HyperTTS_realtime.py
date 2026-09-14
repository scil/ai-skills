#!/usr/bin/env python
"""Configure HyperTTS *Realtime* audio for a note type: writes the HyperTTS preset into the add-on's
meta.json and puts the matching {{tts ...}} tag into the card template. No files are generated —
audio is synthesized at review time by HyperTTS (desktop) or a system voice (mobile fallback).

ANKI MUST BE RESTARTED after --apply / --remove: HyperTTS keeps its config in memory and only reads
meta.json at startup (and would overwrite our edit if one of its dialogs saves first).

Examples
  # 问答题: Chinese prompt on the front (Xiaoxiao), English answer on the back (Jenny, CJK stripped)
  anki_config_HyperTTS_realtime.py --model 问答题 --front 正面:Regular:zh-CN-XiaoxiaoNeural --back 背面:Regular:en-US-JennyNeural --strip-cjk back
  # 填空题: cloze sentence both sides, English only
  anki_config_HyperTTS_realtime.py --model 填空题 --front 文字:Cloze --back 文字:Cloze --strip-cjk front,back
  # back reads only the revealed answer
  anki_config_HyperTTS_realtime.py --model 填空题 --front 文字:Cloze --back 文字:ClozeOnly
  # one side only / mobile fallback voices appended to the tag
  anki_config_HyperTTS_realtime.py --model 问答题 --back 背面:Regular --fallback-voices Apple_Samantha,Google_en-US
  anki_config_HyperTTS_realtime.py --model 问答题 --remove               # strip tags + disable preset sides
  anki_config_HyperTTS_realtime.py --show                                 # presets in meta.json + tags in every template (keys redacted)
  anki_config_HyperTTS_realtime.py --check                                # every template tag has a preset, services enabled
  anki_config_HyperTTS_realtime.py --restore 20260912-170033              # put back meta.json + templates from that backup stamp
  # move the setup to another computer (templates go via AnkiWeb sync; presets via this file, no API keys inside)
  anki_config_HyperTTS_realtime.py --export realtime-presets.json         # on this PC
  anki_config_HyperTTS_realtime.py --import realtime-presets.json         # on the other PC, then restart Anki, sync, --check

Side spec: FIELD[:TYPE[:VOICE]]  TYPE = Regular | Cloze | ClozeOnly (default Regular);
VOICE = Azure voice name (default en_voice from anki.json). --service defaults to Azure.
"""
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from anki_lib import (run, CONFIG, AnkiClient, backup_dir, backup_file, backup_json, base_parser, emit)

HYPERTTS_ID = "111623432"
CJK_RULE = {"rule_type": "Regex", "source": "[　-〿一-鿿＀-￯]+", "target": " "}
TAG_RE = re.compile(r"[ \t]*\{\{tts [^}]*hypertts_preset=(Front|Back)_(realtime_\d+)[^}]*\}\}[ \t]*\n?")
TYPES = ("Regular", "Cloze", "ClozeOnly")


# --------------------------------------------------------------------------- locate HyperTTS

def addons_dir(client: AnkiClient) -> Path:
    media = Path(client("getMediaDirPath"))          # <data>/<profile>/collection.media
    return media.parent.parent / "addons21"


def meta_path(client: AnkiClient) -> Path:
    p = addons_dir(client) / HYPERTTS_ID / "meta.json"
    if not p.exists():
        raise SystemExit(f"HyperTTS not found at {p} — install add-on {HYPERTTS_ID} first")
    return p


def load_meta(p: Path) -> Dict[str, Any]:
    return json.loads(p.read_text(encoding="utf-8"))


def redact(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: ("***" if k in ("api_key", "hypertts_pro_api_key") and v else redact(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(x) for x in obj]
    return obj


# --------------------------------------------------------------------------- config building

def lang_tag(voice: str) -> str:
    """'en-US-JennyNeural' -> 'en_US' (the language token Anki's {{tts}} tag needs)."""
    m = re.match(r"([a-z]{2,3})-([A-Za-z]{2,4})-", voice)
    if not m:
        raise SystemExit(f"cannot derive language from voice name {voice!r}")
    return f"{m.group(1)}_{m.group(2)}"


def parse_side(spec: str) -> Tuple[str, str, str]:
    parts = spec.split(":")
    field = parts[0]
    ftype = parts[1] if len(parts) > 1 and parts[1] else "Regular"
    voice = parts[2] if len(parts) > 2 and parts[2] else CONFIG["en_voice"]
    if ftype not in TYPES:
        raise SystemExit(f"field type must be one of {TYPES}, got {ftype!r}")
    return field, ftype, voice


def voice_key(voice: str, service: str, client: AnkiClient) -> Dict[str, str]:
    """HyperTTS voice_key for a voice. Azure uses the long name
    'Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)'; short 'en-US-JennyNeural' is converted.
    The result is checked against HyperTTS's bundled services/voicelist.py."""
    name = voice
    if service == "Azure" and not voice.startswith("Microsoft Server Speech"):
        m = re.match(r"^([a-z]{2,3}-[A-Za-z]{2,4})-(.+)$", voice)
        if not m:
            raise SystemExit(f"cannot convert Azure voice name {voice!r}")
        name = f"Microsoft Server Speech Text to Speech Voice ({m.group(1)}, {m.group(2)})"
    vl = addons_dir(client) / HYPERTTS_ID / "hypertts_addon" / "services" / "voicelist.py"
    if vl.exists() and repr({"name": name}) not in vl.read_text(encoding="utf-8"):
        raise SystemExit(f"voice {name!r} (service {service}) not in HyperTTS voice list {vl}")
    return {"name": name}


def side_config(field: str, ftype: str, voice: str, service: str, strip_cjk: bool,
                rules: List[Dict[str, str]], client: AnkiClient) -> Dict[str, Any]:
    all_rules = ([CJK_RULE] if strip_cjk else []) + rules
    return {
        "side_enabled": True,
        "source": {"mode": "AnkiTTSTag", "field_name": field, "field_type": ftype},
        "voice_selection": {"voice_selection_mode": "single",
                            "voice": {"voice_id": {"voice_key": voice_key(voice, service, client), "service": service},
                                      "options": {}}},
        "text_processing": {"html_to_text_line": True, "strip_brackets": False, "strip_cloze": False,
                            "ssml_convert_characters": True, "run_replace_rules_after": True,
                            "ignore_case": False, "text_replacement_rules": all_rules},
    }


def tts_tag(side: str, key: str, field: str, ftype: str, voice: str, fallback: List[str]) -> str:
    fmt = {"Regular": field, "Cloze": f"cloze:{field}", "ClozeOnly": f"cloze-only:{field}"}[ftype]
    voices = ",".join(["HyperTTS", *fallback])
    return f"{{{{tts {lang_tag(voice)} hypertts_preset={side}_{key} voices={voices}:{fmt}}}}}"


def existing_key(templates: Dict[str, Dict[str, str]]) -> Optional[str]:
    for t in templates.values():
        for html in (t.get("Front", ""), t.get("Back", "")):
            m = TAG_RE.search(html)
            if m:
                return m.group(2)
    return None


def free_key(rt: Dict[str, Any]) -> str:
    i = 0
    while f"realtime_{i}" in rt:
        i += 1
    return f"realtime_{i}"


def strip_tags(html: str) -> str:
    return TAG_RE.sub("", html).rstrip("\n")


# --------------------------------------------------------------------------- commands

def cmd_show(client: AnkiClient, as_json: bool) -> None:
    meta = load_meta(meta_path(client))
    cfg = meta.get("config", {})
    out: Dict[str, Any] = {
        "meta_json": str(meta_path(client)),
        "services_enabled": {k: v for k, v in cfg.get("configuration", {}).get("service_enabled", {}).items() if v},
        "azure_region": cfg.get("configuration", {}).get("service_config", {}).get("Azure", {}).get("region"),
        "realtime_config": redact(cfg.get("realtime_config", {})),
        "templates": {},
    }
    for model in client("modelNames"):
        tags = []
        for cname, t in client("modelTemplates", modelName=model).items():
            for side_name in ("Front", "Back"):
                for m in TAG_RE.finditer(t.get(side_name, "")):
                    tags.append({"card": cname, "side": side_name, "preset": f"{m.group(1)}_{m.group(2)}"})
        if tags:
            out["templates"][model] = tags
    emit(out, as_json or True)


def cmd_check(client: AnkiClient, as_json: bool) -> int:
    meta = load_meta(meta_path(client))
    cfg = meta.get("config", {})
    rt = cfg.get("realtime_config", {})
    enabled = cfg.get("configuration", {}).get("service_enabled", {})
    vl = addons_dir(client) / HYPERTTS_ID / "hypertts_addon" / "services" / "voicelist.py"
    voicelist = vl.read_text(encoding="utf-8") if vl.exists() else ""
    problems: List[str] = []
    for model in client("modelNames"):
        for cname, t in client("modelTemplates", modelName=model).items():
            for side_name in ("Front", "Back"):
                for m in TAG_RE.finditer(t.get(side_name, "")):
                    side, key = m.group(1), m.group(2)
                    conf = rt.get(key, {}).get(side.lower())
                    if not conf:
                        problems.append(f"{model}/{cname}/{side_name}: preset {side}_{key} missing in meta.json")
                    elif not conf.get("side_enabled"):
                        problems.append(f"{model}/{cname}/{side_name}: preset {side}_{key} is disabled")
                    else:
                        vid = conf["voice_selection"]["voice"]["voice_id"]
                        svc = vid["service"]
                        if not enabled.get(svc):
                            problems.append(f"{model}/{cname}/{side_name}: service {svc} not enabled in HyperTTS")
                        if repr(vid["voice_key"]) not in voicelist:
                            problems.append(f"{model}/{cname}/{side_name}: voice {vid['voice_key']} not in HyperTTS voice list")
    emit({"ok": not problems, "problems": problems}, as_json)
    return 0 if not problems else 1


def cmd_restore(client: AnkiClient, stamp: str, as_json: bool, dry: bool) -> None:
    d = backup_dir()
    meta_b = next(iter(sorted(d.glob(f"{stamp}*-hypertts-meta.json"))), None)
    tmpl_bs = sorted(d.glob(f"{stamp}*-templates*.json"))
    if not meta_b and not tmpl_bs:
        raise SystemExit(f"no backups matching {stamp}* in {d}")
    done: Dict[str, Any] = {"dry_run": dry}
    if meta_b:
        if not dry:
            meta_path(client).write_bytes(meta_b.read_bytes())
        done["meta_json"] = str(meta_b)
    done["templates"] = []
    for tmpl_b in tmpl_bs:
        data = json.loads(tmpl_b.read_text(encoding="utf-8"))
        for model, templates in data.items():
            if not dry:
                client("updateModelTemplates", model={"name": model, "templates": templates})
            done["templates"].append(f"{model} <- {tmpl_b.name}")
    done["note"] = "restart Anki so HyperTTS reloads meta.json"
    emit(done, as_json)


def cmd_export(client: AnkiClient, out: str, as_json: bool) -> None:
    """Realtime presets referenced by any template + those tags, for another computer. No API keys."""
    meta = load_meta(meta_path(client))
    rt = meta.get("config", {}).get("realtime_config", {})
    presets: Dict[str, Any] = {}
    templates: Dict[str, Dict[str, Dict[str, str]]] = {}
    for model in client("modelNames"):
        for cname, t in client("modelTemplates", modelName=model).items():
            for side_name in ("Front", "Back"):
                for m in TAG_RE.finditer(t.get(side_name, "")):
                    key = m.group(2)
                    if key in rt:
                        presets[key] = rt[key]
                    templates.setdefault(model, {}).setdefault(cname, {})[side_name] = m.group(0).strip()
    services = sorted({side["voice_selection"]["voice"]["voice_id"]["service"]
                       for cfg in presets.values() for side in (cfg["front"], cfg["back"]) if side.get("side_enabled")})
    data = {"realtime_config": presets, "templates": templates, "services_needed": services,
            "exported_from": Path(client("getMediaDirPath")).parent.name}
    Path(out).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    emit({"exported": out, "presets": list(presets), "models": list(templates), "services_needed": services}, as_json)


def cmd_import(client: AnkiClient, src: str, as_json: bool, dry: bool) -> None:
    """Write exported presets into this computer's HyperTTS meta.json (templates arrive via AnkiWeb sync)."""
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    mp = meta_path(client)
    meta = load_meta(mp)
    cfg = meta.setdefault("config", {})
    enabled = cfg.get("configuration", {}).get("service_enabled", {})
    missing = [s for s in data.get("services_needed", []) if not enabled.get(s)]
    result: Dict[str, Any] = {"dry_run": dry, "presets": list(data["realtime_config"]), "services_not_enabled": missing}
    if not dry:
        result["backup"] = str(backup_file(mp, "hypertts-meta", "anki_config_HyperTTS_realtime.py",
                                           "HyperTTS meta.json before importing realtime presets", f"from {src}"))
        cfg.setdefault("realtime_config", {}).update(data["realtime_config"])
        mp.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        result["next"] = "RESTART ANKI, sync (so the templates arrive), then run --check"
    if missing:
        result["warning"] = f"enable {missing} in Tools → HyperTTS → Configure Services (Azure: key + region)"
    emit(result, as_json)


def cmd_apply(client: AnkiClient, a: Any) -> None:
    mp = meta_path(client)
    meta = load_meta(mp)
    rt = meta.setdefault("config", {}).setdefault("realtime_config", {})
    if a.preset:                      # preset-only edit: no template access, templates already reference it
        templates, cards = {}, []
        key = a.preset
        if key not in rt:
            raise SystemExit(f"preset {key!r} not in meta.json (has {list(rt)})")
    else:
        templates = client("modelTemplates", modelName=a.model)
        cards = [a.card] if a.card else list(templates)
        for cname in cards:
            if cname not in templates:
                raise SystemExit(f"card template {cname!r} not in {a.model} (has {list(templates)})")
        key = existing_key(templates) or free_key(rt)
    strip = {s.strip() for s in (a.strip_cjk or "").split(",") if s.strip()}
    rules = [{"rule_type": "Regex", "source": s, "target": t} for s, t in (a.rule or [])]

    new_rt: Dict[str, Any] = {"front": {"side_enabled": False}, "back": {"side_enabled": False}}
    new_tags: Dict[str, str] = {}
    if not a.remove:
        for side_name, spec in (("front", a.front), ("back", a.back)):
            if not spec:
                continue
            field, ftype, voice = parse_side(spec)
            new_rt[side_name] = side_config(field, ftype, voice, a.service, side_name in strip, rules, client)
            new_tags[side_name.capitalize()] = tts_tag(side_name.capitalize(), key, field, ftype, voice,
                                                       [v for v in (a.fallback_voices or "").split(",") if v])
        if not new_tags:
            raise SystemExit("nothing to do: give --front and/or --back (or --remove)")

    new_templates: Dict[str, Dict[str, str]] = {}
    for cname in cards:
        t = templates[cname]
        nt = {"Front": strip_tags(t["Front"]), "Back": strip_tags(t["Back"])}
        for side_name, tag in new_tags.items():
            nt[side_name] = nt[side_name] + "\n" + tag
        new_templates[cname] = nt

    plan = {"model": a.model, "preset_key": key, "cards": cards, "realtime_config": redact(new_rt),
            "tags": new_tags, "dry_run": a.dry_run}
    if a.dry_run or a.verbose:
        for cname, nt in new_templates.items():
            print(f"--- {a.model} / {cname} / Front ---\n{nt['Front']}\n--- Back ---\n{nt['Back']}\n", file=sys.stderr)
    if a.dry_run:
        emit(plan, a.json); return

    ctx = f"model={a.model} key={key} profile={Path(client('getMediaDirPath')).parent.name}"
    plan["backups"] = [
        str(backup_file(mp, "hypertts-meta", "anki_config_HyperTTS_realtime.py", "HyperTTS meta.json before realtime change", ctx))]
    if templates:
        plan["backups"].append(str(backup_json({a.model: templates}, f"templates-{a.model}", "anki_config_HyperTTS_realtime.py",
                                               f"{a.model} card templates before realtime change", ctx)))
    rt[key] = new_rt
    if a.error_mode:
        meta["config"].setdefault("preferences", {}).setdefault("error_handling", {})["realtime_tts_errors_dialog_type"] = a.error_mode
        plan["error_mode"] = a.error_mode
    mp.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    if templates:
        client("updateModelTemplates", model={"name": a.model, "templates": new_templates})
    plan["next"] = "RESTART ANKI now (HyperTTS reads meta.json only at startup), then run --check"
    emit(plan, a.json)


def main() -> None:
    p = base_parser(__doc__)
    p.add_argument("--model", help="note type, e.g. 问答题")
    p.add_argument("--preset", metavar="realtime_N",
                   help="edit this preset only (voices / rules), leaving templates alone — e.g. one used by another profile")
    p.add_argument("--card", help="card template name inside the model (default: all cards of the model)")
    p.add_argument("--front", metavar="FIELD[:TYPE[:VOICE]]")
    p.add_argument("--back", metavar="FIELD[:TYPE[:VOICE]]")
    p.add_argument("--service", default="Azure", help="HyperTTS service the voice belongs to (default Azure)")
    p.add_argument("--strip-cjk", metavar="front,back", help="drop Chinese/CJK characters before speaking on these sides")
    p.add_argument("--rule", nargs=2, action="append", metavar=("REGEX", "REPL"), help="extra text-processing rule (both sides)")
    p.add_argument("--fallback-voices", metavar="A,B", help="voices tried after HyperTTS (used on mobile), e.g. Apple_Samantha")
    p.add_argument("--remove", action="store_true", help="strip the model's realtime tags and disable its preset")
    p.add_argument("--show", action="store_true")
    p.add_argument("--check", action="store_true")
    p.add_argument("--restore", metavar="STAMP", help="restore meta.json + templates from backups named STAMP*")
    p.add_argument("--error-mode", choices=["Dialog", "Tooltip", "Nothing"],
                   help="how HyperTTS reports realtime errors (e.g. empty text on image-only cards); written with --apply")
    p.add_argument("--export", metavar="FILE.json", help="write presets used by templates (no keys) for another PC")
    p.add_argument("--import", dest="import_", metavar="FILE.json", help="merge exported presets into this PC's HyperTTS")
    a = p.parse_args()

    c = AnkiClient(a.url)
    if a.show:
        cmd_show(c, a.json); return
    if a.check:
        sys.exit(cmd_check(c, a.json))
    if a.restore:
        cmd_restore(c, a.restore, a.json, a.dry_run); return
    if a.export:
        cmd_export(c, a.export, a.json); return
    if a.import_:
        cmd_import(c, a.import_, a.json, a.dry_run); return
    if not a.model and not a.preset:
        p.error("--model (or --preset) is required, or use --show / --check / --restore / --export / --import")
    cmd_apply(c, a)


if __name__ == "__main__":
    run(main)
