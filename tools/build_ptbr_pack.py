#!/usr/bin/env python3
"""Builds a Brazilian Portuguese localization pack for CK3 from a community pack.

Why this exists
    CK3 has no Portuguese language slot (game/localization/languages.yml). The community
    translation "Tradução PT-BR" (Emerson Antunes) reaches Portuguese by replacing the
    SPANISH localization files, which means the player must set the game to Español.

    This script converts that pack into an ENGLISH override instead, so the game keeps its
    normal language setting (English) and shows Portuguese. For every vanilla key the
    community pack does not translate, the original English line is appended, so no key
    ever renders as `raw_key_like_this`.

What it does
    1. Reads the vanilla English localization tree (source of truth for which keys exist).
    2. Reads the community pack (`localization/spanish/*_l_spanish.yml`).
    3. Writes `localization/replace/english/<same path>_l_english.yml` with:
         - `l_english:` header
         - every translated line, unchanged
         - every missing vanilla key, appended verbatim in English
    4. Prints a coverage report. Nothing is uploaded anywhere.

Usage
    python3 tools/build_ptbr_pack.py \
        --source /tmp/ptbr2/traducao_pt_br \
        --game "$HOME/Downloads/Crusader Kings III/Crusader Kings III/game" \
        --out "<CK3 user dir>/mod/traducao_ptbr_120"

The community pack is third-party work: keep the credits, do not commit its files here.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

KEY_RE = re.compile(r'^\s*([A-Za-z0-9_.\-]+):\d*\s+"')


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def split_lines(text: str) -> list[str]:
    return [line.rstrip("\r") for line in text.split("\n")]


def keys_and_lines(path: Path) -> tuple[dict[str, str], list[str]]:
    """Returns (key -> raw line, all raw lines without the language header)."""
    keys: dict[str, str] = {}
    body: list[str] = []
    for line in split_lines(read_text(path)):
        if re.match(r"^\s*l_[a-z_]+:\s*$", line):
            continue
        body.append(line)
        match = KEY_RE.match(line)
        if match:
            keys[match.group(1)] = line
    return keys, body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="community pack root (…/traducao_pt_br)")
    parser.add_argument("--game", required=True, help="CK3 install root (…/Crusader Kings III/game)")
    parser.add_argument("--out", required=True, help="output mod directory")
    args = parser.parse_args()

    vanilla_root = Path(args.game).expanduser() / "localization" / "english"
    source_root = Path(args.source).expanduser() / "localization" / "spanish"
    out_root = Path(args.out).expanduser() / "localization" / "replace" / "english"

    if not vanilla_root.is_dir():
        print(f"FAIL: vanilla English localization not found at {vanilla_root}")
        return 1
    if not source_root.is_dir():
        print(f"FAIL: community pack Spanish folder not found at {source_root}")
        return 1

    translated_keys = 0
    appended_keys = 0
    files_written = 0
    files_with_fallback = 0
    skipped: list[str] = []
    untranslated: list[str] = []

    for pt_path in sorted(source_root.rglob("*.yml")):
        rel = pt_path.relative_to(source_root)
        target_rel = Path(str(rel).replace("_l_spanish.yml", "_l_english.yml"))
        vanilla_path = vanilla_root / target_rel
        if not vanilla_path.is_file():
            skipped.append(str(rel))
            continue

        pt_keys, pt_body = keys_and_lines(pt_path)
        van_keys, van_lines = keys_and_lines(vanilla_path)

        missing = [key for key in van_keys if key not in pt_keys]
        out_lines = ["l_english:"]
        while pt_body and not pt_body[-1].strip():
            pt_body.pop()
        out_lines.extend(pt_body)
        if missing:
            files_with_fallback += 1
            out_lines.append("")
            out_lines.append(
                f" # srd-tools: {len(missing)} key(s) not translated yet - English kept as fallback."
            )
            for key in missing:
                out_lines.append(van_keys[key])

        target = out_root / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = "\n".join(out_lines).rstrip("\n") + "\n"
        target.write_bytes(b"\xef\xbb\xbf" + payload.encode("utf-8"))

        files_written += 1
        translated_keys += len([key for key in pt_keys if key in van_keys])
        appended_keys += len(missing)

    for van_path in sorted(vanilla_root.rglob("*.yml")):
        rel = van_path.relative_to(vanilla_root)
        if not (out_root / rel).is_file():
            untranslated.append(str(rel))

    print(f"files written          : {files_written}")
    print(f"translated keys        : {translated_keys}")
    print(f"English fallback keys  : {appended_keys} (in {files_with_fallback} files)")
    print(f"vanilla files untouched: {len(untranslated)}")
    print(f"pack files ignored     : {len(skipped)} (keys absent from CK3 1.20.1)")
    if untranslated:
        print("\nstill English:")
        for rel in untranslated[:15]:
            print(f"  {rel}")
        if len(untranslated) > 15:
            print(f"  … and {len(untranslated) - 15} more")
    print("\nReminder: this pack is third-party work by Emerson Antunes (Tradução PT-BR).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
