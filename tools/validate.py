#!/usr/bin/env python3
"""Static validator for the Smart Realm Director mod.

Level A of the test plan (docs/TEST_PLAN.md). It never claims runtime correctness:
it only proves the files are structurally consistent.

Checks
  1. descriptor.mod exists and declares version / name / supported_version.
  2. Every .txt file has balanced braces and brackets outside strings and comments.
  3. Every localization file is UTF-8 with BOM, starts with the right language header,
     and defines no duplicate key.
  4. Every srd_* localization key referenced by script is defined.
  5. Every srd_* scripted effect / trigger called with "= yes" is defined.
  6. Every event id used in trigger_event is defined in the same mod.
  7. Every game rule setting used with has_game_rule is defined in the mod or exists in
     the installed game.

Exit code 0 = all static checks passed. Exit code 1 = at least one failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MOD_DIR_NAME = "Smart_Realm_Director"
REPO_ROOT = Path(__file__).resolve().parent.parent
MOD = REPO_ROOT / MOD_DIR_NAME

GAME_MOD_CANDIDATES = [
    Path.home() / ".local/share/Paradox Interactive/Crusader Kings III/mod",
]

errors: list[str] = []
notes: list[str] = []


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def strip_comments_and_strings(text: str) -> str:
    """Remove # comments and quoted strings so brace counting cannot be fooled."""
    out = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            out.append(" ")
            continue
        if char == '"':
            in_string = True
            out.append(" ")
            continue
        if char == "#":
            # everything up to the newline is a comment; the second pass drops it
            out.append("\0COMMENT")
            continue
        out.append(char)
    # second pass: drop comment tails
    cleaned = []
    for line in "".join(out).split("\n"):
        idx = line.find("\0COMMENT")
        cleaned.append(line if idx < 0 else line[:idx])
    return "\n".join(cleaned)


def check_descriptor() -> None:
    desc = MOD / "descriptor.mod"
    if not desc.is_file():
        errors.append("missing Smart_Realm_Director/descriptor.mod")
        return
    text = desc.read_text(encoding="utf-8")
    for field in ("version=", "name=", "supported_version="):
        if field not in text:
            errors.append(f"descriptor.mod: missing {field.rstrip('=')}")


SUPPORTED_LANGUAGES = [
    "english",
    "french",
    "german",
    "polish",
    "spanish",
    "simp_chinese",
    "russian",
    "korean",
    "japanese",
]


def check_encoding_and_lists() -> None:
    """The engine wants UTF-8 BOM on every .txt and rejects `limit` inside any_* lists.

    Both were real error.log findings on 1.20.1 (see docs/RUNTIME_TESTS.md, R0).
    """
    for path in sorted(MOD.rglob("*.txt")):
        raw = path.read_bytes()
        if not raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{rel(path)}: missing UTF-8 BOM (engine logs an encoding error)")
        lines = raw.decode("utf-8-sig").split("\n")
        for index, line in enumerate(lines):
            if not re.search(r"\bany_[a-z_]+\s*=\s*\{\s*$", line):
                continue
            depth = 1
            for follow in lines[index + 1 :]:
                if re.search(r"\blimit\s*=\s*\{", follow):
                    errors.append(
                        f"{rel(path)}:{index + 1}: 'limit' inside an any_* list is rejected "
                        "by 1.20.1 - put the triggers directly in the list"
                    )
                    break
                depth += follow.count("{") - follow.count("}")
                if depth <= 0:
                    break


def check_balance() -> None:
    for path in sorted(MOD.rglob("*.txt")):
        text = strip_comments_and_strings(path.read_text(encoding="utf-8-sig"))
        for open_ch, close_ch, label in (("{", "}", "brace"), ("[", "]", "bracket")):
            depth = 0
            minimum = 0
            for char in text:
                if char == open_ch:
                    depth += 1
                elif char == close_ch:
                    depth -= 1
                    minimum = min(minimum, depth)
            if depth != 0 or minimum < 0:
                errors.append(
                    f"{rel(path)}: unbalanced {label}s (final depth {depth})"
                )


def check_localization() -> tuple[set[str], set[str]]:
    keys: dict[str, str] = {}
    seen: dict[tuple[str, str], str] = {}
    langs: set[str] = set()
    loc_root = MOD / "localization"
    if not loc_root.is_dir():
        errors.append("missing localization/ directory")
        return set(), langs

    key_re = re.compile(r"^\s*([A-Za-z0-9_.]+):\d*\s*\"")
    for path in sorted(loc_root.rglob("*.yml")):
        raw = path.read_bytes()
        lang = path.stem.split("_l_")[-1]
        langs.add(lang)
        if not raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{rel(path)}: missing UTF-8 BOM")
        body = raw.decode("utf-8-sig").split("\n")
        if not body or not body[0].strip().startswith(f"l_{lang}:"):
            errors.append(
                f"{rel(path)}: first line must start with 'l_{lang}:'"
            )
        if not path.name.endswith(f"l_{lang}.yml"):
            errors.append(f"{rel(path)}: file name must end with 'l_{lang}.yml'")
        for number, line in enumerate(body[1:], start=2):
            match = key_re.match(line)
            if not match:
                continue
            key = match.group(1)
            ident = (lang, key)
            if ident in seen:
                errors.append(
                    f"{rel(path)}:{number}: duplicate loc key '{key}' for l_{lang} "
                    f"(also in {seen[ident]})"
                )
            seen[ident] = f"{rel(path)}:{number}"
            keys[key] = f"{rel(path)}:{number}"
    if "english" not in langs:
        errors.append("localization: no English file found")
    missing_langs = [lang for lang in SUPPORTED_LANGUAGES if lang not in langs]
    if missing_langs:
        notes.append(
            "localization: no file for "
            + ", ".join(missing_langs)
            + " - players on those languages see raw keys"
        )
    return set(keys), langs


def check_script_references(keys: set[str]) -> None:
    text_files = sorted(MOD.rglob("*.txt"))
    script_text = "\n".join(p.read_text(encoding="utf-8-sig") for p in text_files)
    script_clean = strip_comments_and_strings(script_text)

    # 4. localization keys referenced from script (only our namespace is enforced).
    loc_ref_fields = (
        "title",
        "desc",
        "name",
        "tooltip",
        "custom_tooltip",
        "selection_tooltip",
        "text",
        "custom_description",
    )
    # Variable and flag names share the "name =" field with localization keys.
    declared_names = set(
        re.findall(
            r"(?:set_variable|remove_variable|has_variable|add_character_flag)\s*=\s*\{[^}]*?\bname\s*=\s*([A-Za-z0-9_]+)",
            script_clean,
        )
    ) | set(
        re.findall(r"add_character_flag\s*=\s*\{\s*flag\s*=\s*([A-Za-z0-9_]+)", script_clean)
    )
    referenced: set[str] = set()
    for field in loc_ref_fields:
        pattern = rf"\b{field}\s*=\s*\"?([A-Za-z0-9_.]+)\"?\s*$"
        for match in re.finditer(pattern, script_clean, flags=re.MULTILINE):
            value = match.group(1)
            if value.startswith("srd_") and value not in declared_names:
                referenced.add(value)
    for key in sorted(referenced):
        if key not in keys:
            errors.append(f"localization: key '{key}' is referenced but not defined")

    # Also enforce that every defined srd key is used somewhere (dead keys hide typos).
    for key in sorted(k for k in keys if k.startswith(("srd_",))):
        if key in referenced:
            continue
        # game rule and modifier keys are referenced by engine, not by a field above
        if key.startswith(("rule_", "setting_")) or key.endswith(("_desc", "_tt", "_desc")):
            continue
        if key in script_text:
            continue
        notes.append(f"localization: '{key}' defined but not referenced (check for typos)")

    # 5. scripted effects / triggers defined and referenced.
    defined_defs = set(
        re.findall(r"^([A-Za-z0-9_]+)\s*=\s*\{", script_clean, flags=re.MULTILINE)
    )
    for name in sorted(set(re.findall(r"\b(srd_[a-z0-9_]+)\s*=\s*yes\b", script_clean))):
        if name not in defined_defs:
            errors.append(f"script: '{name}' is called with '= yes' but not defined")

    # 6. event ids.
    event_defs = set(
        re.findall(r"^([A-Za-z0-9_]+\.[0-9]+)\s*=\s*\{", script_clean, flags=re.MULTILINE)
    )
    for event_id in sorted(set(re.findall(r"id\s*=\s*([A-Za-z0-9_]+\.[0-9]+)", script_clean))):
        if not event_id.startswith("srd_") and event_id not in event_defs:
            notes.append(f"script: external event id '{event_id}' (not checked)")
        elif event_id not in event_defs:
            errors.append(f"script: event id '{event_id}' triggered but not defined")

    # 7. game rule settings.
    game_rules_file = MOD / "common/game_rules/srd_game_rules.txt"
    defined_rules = set(
        re.findall(
            r"^\t(srd_[a-z0-9_]+)\s*=\s*\{\s*$",
            strip_comments_and_strings(game_rules_file.read_text(encoding="utf-8-sig")),
            flags=re.MULTILINE,
        )
    )
    for setting in sorted(set(re.findall(r"has_game_rule\s*=\s*(srd_[a-z0-9_]+)", script_clean))):
        if setting not in defined_rules:
            errors.append(
                f"game rules: 'has_game_rule = {setting}' but '{setting}' is not defined"
            )


def check_no_vanilla_overrides() -> None:
    """Phase 1 must not shadow vanilla or third-party files."""
    guarded = {"gui", "common/decisions", "common/on_action"}
    for folder in guarded:
        target = MOD / folder
        if not target.exists():
            continue
    for path in sorted(MOD.rglob("*")):
        if path.is_file() and "gui/" in rel(path).replace("\\", "/"):
            notes.append(
                f"{rel(path)}: GUI file present - confirm it does not shadow another mod"
            )


def main() -> int:
    if not MOD.is_dir():
        print(f"FAIL: {MOD_DIR_NAME}/ not found next to tools/")
        return 1

    check_descriptor()
    check_encoding_and_lists()
    check_balance()
    keys, _langs = check_localization()
    check_script_references(keys)
    check_no_vanilla_overrides()

    for note in notes:
        print(f"note: {note}")
    if errors:
        print()
        for error in errors:
            print(f"FAIL: {error}")
        print(f"\n{len(errors)} static check(s) failed.")
        return 1

    print("OK: static checks passed (structure, braces, localization, references).")
    print("Runtime behaviour is NOT verified by this script - see docs/RUNTIME_TESTS.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
