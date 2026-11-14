# DEVELOPMENT_GUIDE.md

## Environment on this machine

| Thing | Path / value |
| --- | --- |
| Game install | `~/Downloads/Crusader Kings III/Crusader Kings III/` |
| Game version | 1.20.1 (`clausewitz_branch.txt`, `titus_branch.txt`) |
| Vanilla scripts | `<install>/game/` |
| Mod folder (live) | `~/.config/hydralauncher/wine-prefixes/1158310/drive_c/users/steamuser/Documents/Paradox Interactive/Crusader Kings III/mod` |
| User directory | one level above the mod folder (holds `dlc_load.json`, `logs/`) |
| Repository | `~/KDC3_Mods` → https://github.com/Lincoln16yyy/CK3_Mods |
| Validator | `python3 tools/validate.py` |
| CI | `.github/workflows/validate.yml` (static checks only) |

The install is a repack running under a Hydra launcher prefix with the Goldberg Steam
emulator. That matters for scripting only in one way: the online/DLC features of the
repack are not a reliable test of DLC-gated script (`has_tgp_dlc_trigger` etc.).

## Debug mode

Run the executable with:

```
-debug_mode -develop
```

Expected effects: console available (`` ` ``), `error.log`/`debug.log` in the user
directory, and tooltips showing script names. **Not yet verified on this build** — recorded
as pending in `RUNTIME_TESTS.md`.

Reload behaviour (also unverified here, from CK3 modding practice):

- `common/`, `events/`, `localization/` — reloadable in a running session only if the mod
  was already loaded; a clean restart is the reliable path.
- `gui/` — needs a restart of the game.
- `descriptor.mod` / `.mod` — needs a launcher restart.

Always restart before judging a change; never conclude "it works" from a hot-reload alone.

## Console commands worth using

| Command | Use |
| --- | --- |
| `script_docs` | dumps the effect/trigger documentation for the installed build into `logs/` |
| `dump_data_types` | dumps data functions for GUI and loc |
| `debug_mode` | enables debug tooltips and the debug menu |
| `observe` | watch a realm without owning it (useful for AI-side checks) |
| `add_gold 500` | set up a treasury for a test, then remove it from the test character |

`script_docs` output: keep the relevant excerpts in `ENGINE_CAPABILITIES.md`; do not commit
the raw dump.

## Workflow for a change

1. Find the primitive in `<install>/game/` and record file + line in
   `docs/ENGINE_CAPABILITIES.md`.
2. Write the smallest script that uses it, in the `srd_` namespace.
3. `python3 tools/validate.py` (level A).
4. `./tools/install.sh` then enable the mod in the launcher.
5. Run the matching item in `docs/RUNTIME_TESTS.md` and write down what actually happened.
6. Update `STATUS.md` and `PHASE_LOG.md` in the same commit.
7. Commit small; no force push; PRs into `main`.

## Style

- Tabs for indentation, like vanilla.
- Every file starts with a comment naming the game version it targets.
- Every non-obvious effect carries the evidence that it exists.
- No literal magic numbers without a named script value.

## Localization

- UTF-8 **with BOM**, first line `l_english:`, file name `*_l_english.yml`.
- Only the nine languages listed in `game/localization/languages.yml` can ever load.
- Portuguese text goes to `docs/` (see `README.md`).
