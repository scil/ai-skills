"""Check Espanso prompt match files before asking the user to try them.

Reports: YAML that fails to parse; a trigger that ends with another trigger while lacking
left_word (typing the long one fires both); more than one $|$ cursor marker in a match;
an underscore-prefixed file that no other match file imports (Espanso skips it).

Usage: python -I -X utf8 check_espanso.py <match-dir> [<prompt-subdir-glob>]
  e.g. check_espanso.py D:\\A\\Scoop\\persist\\Espanso\\.espanso\\match "_prompts/*.yml"
"""
import sys
from pathlib import Path

import yaml


def main():
    match_dir = Path(sys.argv[1])
    pattern = sys.argv[2] if len(sys.argv) > 2 else "**/*.yml"
    files = sorted(match_dir.glob(pattern))
    all_yml = [p for p in match_dir.rglob("*.yml") if "packages" not in p.parts]
    config_dir = match_dir.parent / "config"
    importers = all_yml + (sorted(config_dir.glob("*.yml")) if config_dir.exists() else [])
    problems, matches = [], []

    for f in files:
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            problems.append(f"{f.name}: YAML error: {e}")
            continue
        for m in doc.get("matches", []):
            triggers = m.get("triggers") or [m.get("trigger")]
            for t in filter(None, triggers):
                matches.append((t, f.name, m))
            if str(m.get("replace", "")).count("$|$") > 1:
                problems.append(f"{f.name}: {triggers}: more than one $|$")
        if f.name.startswith("_"):
            imported = any(f.name in p.read_text(encoding="utf-8", errors="replace") for p in importers if p != f)
            if not imported:
                problems.append(f"{f.name}: underscore file imported by nothing, so Espanso never loads it")

    for short, sf, sm in matches:
        for long_, lf, lm in matches:
            if long_ != short and long_.endswith(short) and not (sm.get("left_word") or sm.get("word")):
                problems.append(f"typing {long_!r} ({lf}) also fires {short!r} ({sf}); add left_word: true to {short!r}")

    print(f"{len(matches)} triggers in {len(files)} files; {len({t for t, _, _ in matches})} distinct")
    missing = sorted({t for t, _, m in matches if not (m.get("left_word") or m.get("word"))})
    if missing:
        print("without left_word:", ", ".join(missing))
    print("\n".join(problems) if problems else "no problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
