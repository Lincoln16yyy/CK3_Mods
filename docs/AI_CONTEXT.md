# AI_CONTEXT.md

Context needed to continue this project without re-deriving it.

## Hard facts

- **Game**: CK3 1.20.1 (`titus/release/1.20.1`), installed at
  `~/Downloads/Crusader Kings III/Crusader Kings III/`. The install is a repack under a
  Hydra wine prefix with the Goldberg emulator; DLC-gated script is unreliable to test.
- **Mod folder**: `~/.config/hydralauncher/wine-prefixes/1158310/drive_c/users/steamuser/Documents/Paradox Interactive/Crusader Kings III/mod`.
- **Active mods**: 13 automation mods, load order in `dlc_load.json`, plus three
  compatibility patches (`caa_ca_compatch`, `strategist_nomad_compatch`,
  `loc_compatch_ca_court`) installed outside this repository, loaded last.
- **Repo**: `~/KDC3_Mods` → https://github.com/Lincoln16yyy/CK3_Mods, branch `main`.
  Work happens on `feat/...` branches with a PR into `main`.
- **No Portuguese in the engine.** Nine languages only. Portuguese docs live in `docs/`.

## What exists

`Smart_Realm_Director/` — Phase 1, module **Smart Vassals**: game rule with four modes,
yearly hook on `yearly_playable_pulse`, candidate selection over the player's vassals,
real gift execution (`remove_short_term_gold` + `reverse_add_opinion`), cooldowns via timed
character flags, supervised event, report decision, English localization.

`tools/validate.py` — the gate for every commit. `tools/install.sh` — local install.

## What has been proven and what has not

- Proven **by reading the installed files**: every primitive used (see
  `ENGINE_CAPABILITIES.md`, with file and line).
- Proven **by static checks**: structure, braces, localization, references.
- **Not proven**: any runtime behaviour. `RUNTIME_TESTS.md` is 100% `PENDENTE`.

## Traps discovered so far

1. `gui/window_council.gui` and `gui/window_military.gui` are already double-owned. Any new
   file at those paths silently disables someone else's UI. SRD ships no `gui/` at all.
2. Two mods shipping the same loc file name (`ca_l_<lang>.yml`) means one of them loses all
   its text. Check file-name collisions before adding localization.
3. `set_variable = { name = X }` and `name = loc_key` look identical to naive tooling; the
   validator therefore excludes variable names from the loc-key check.
4. `yearly_playable_pulse` may be declared again only with `on_actions` (appended lists);
   re-declaring `effect` would overwrite vanilla.
5. `has_game_rule` is a plain trigger (`has_game_rule = <setting>`), not a `{ name = … }`
   block, in this build.

## Next actions

1. Runtime pass (R0–R13). Fill `RUNTIME_TESTS.md` with real observations.
2. `script_docs` capture, then extend `ENGINE_CAPABILITIES.md`.
3. Phase 2: succession readiness audit (recommendation-first) and a shared treasury
   reserve used by every module.
