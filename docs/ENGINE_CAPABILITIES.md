# ENGINE_CAPABILITIES.md

Evidence base: the **installed** game at
`~/Downloads/Crusader Kings III/Crusader Kings III/` (`clausewitz_branch.txt` =
`titus/release/1.20.1`, `titus_branch.txt` = `titus/release/1.20.1`). Line numbers are from
that build and will drift after a patch.

`script_docs` / `dump_data_types` have **not** been run yet (they need an in-game console
session). Until they are, this file is the authoritative list of what the Director is
allowed to use, and nothing outside it may be assumed.

## Verified primitives

| Capability | Primitive | Evidence (installed build) | Used by SRD |
| --- | --- | --- | --- |
| Yearly character pulse | `yearly_playable_pulse` (root = character) | `game/common/on_action/yearly_on_actions.txt:981`; documented in `common/on_action/_on_actions.info:7` | yes |
| Extend an existing on_action without replacing it | `on_action = { on_actions = { my_action } }` | `common/on_action/_on_actions.info` + ck3.paradoxwikis.com/Modding (lists are appended) | yes |
| Read a game rule | `has_game_rule = <setting_key>` | `game/common/activities/activity_types/coronation.txt:13`, `hunt.txt:1422` | yes |
| Define a game rule | `rule = { default = … categories = { game_modes } … }` | `game/common/game_rules/00_game_rules.txt`, `_game_rules.info`; same format in installed `CouncilAutomation/common/game_rules/ca_game_rules.txt` | yes |
| Spend gold | `remove_short_term_gold = <value>` | installed mods on this build: `auto_builder_mod/common/scripted_effects/js_ab_domicile_effects.txt:35`, `council_autopilot/events/council_autopilot_fabricate_events.txt:254` | yes |
| Opinion of one character toward another | `reverse_add_opinion = { target = X modifier = M years = N }` | `game/common/activities/activity_types/hike.txt:139` | yes |
| Query an opinion | `opinion = { target = X value <= N }` | `game/common/activities/pulse_actions/hunt_pulse_actions.txt:1371` | yes |
| Detect an existing opinion modifier | `has_opinion_modifier = { modifier = M target = T }` | `game/common/activities/activity_types/pilgrimage.txt:2793` | yes |
| Define an opinion modifier | `name = { opinion = N decaying = no years = N }` | `game/common/opinion_modifiers/00_council_opinions.txt` | yes |
| Timed character flag (cooldown) | `add_character_flag = { flag = F years/days = N }` | `game/common/character_interactions/00_character_interactions.txt:1413`, `00_vassal_interactions.txt:1692` | yes |
| Iterate vassals | `every_vassal = { limit = {…} … }`, `any_vassal = { count >= 1 }` | `game/common/on_action/death.txt:801`, `game/common/achievements/standard_achievements.txt:409` | yes |
| Build a candidate list | `add_to_temporary_list = L`, `random_in_list = { list = L }`, `save_temporary_scope_as = S` | `game/events/education_and_childhood/chinese_disciple_events.txt` | yes |
| Store a character in a variable | `set_variable = { name = V value = scope:X }`, `exists = var:V` | `game/common/scripted_effects/00_scripted_effects.txt:23`, `common/achievements/ep1_achievements.txt:25` | yes |
| Player-facing prompt | `trigger_event = { id = … }` + event `option = { trigger/effect }` | `game/common/activities/activity_types/hunt.txt:912` | yes |
| Notification toast | `send_interface_toast = { type title custom_tooltip left_icon }` | `game/common/decisions/clerical_chastity_decisions.txt` | yes |
| Decision as UI entry point | decision with `ai_check_interval = 0`, `is_shown`, `effect` | `game/common/decisions/clerical_chastity_decisions.txt` | yes |
| Powerful vassal test | `is_powerful_vassal = yes` | `game/common/activities/activity_types/tour.txt:467` | reserved (Phase 6) |
| Debug trace | `debug_log = "…"` | `game/common/scripted_effects/00_accolades_scripted_effects.txt:10873` | yes |

## Supported languages

`game/localization/languages.yml` lists exactly nine languages: English, French, German,
Polish, Spanish, Simplified Chinese, Russian, Korean, Japanese. **Portuguese is not
supported by CK3 1.20.1**; a `localization/braz_por/` folder is never loaded.

Workaround in use: the game is played in English, so the mod's Brazilian Portuguese text
is stored in `localization/english/srd_l_english.yml` (valid `l_english:` header). The
engine reads the English file and displays Portuguese. This only works for English
installs; other languages would need their own translated files. See
`docs/LOCALIZATION.md`.

## Known limits (proven negatives)

| Thing | Why it cannot be done | Evidence |
| --- | --- | --- |
| Call a character interaction from script | No effect triggers interactions; vanilla interactions are UI/engine entry points | no such effect found while searching `game/common/scripted_effects` for the 13 audited mechanics |
| Give troops / MAA without paying | Would require inventing cost; violates rule 5 in `AGENTS.md` | — |
| Load Portuguese text | language list is fixed by the engine | `game/localization/languages.yml` |
| Sort vassals by opinion inside an effect | No `order_by` iterator confirmed in this build | not attempted; `random_in_list` used instead |

## Pending capability checks

1. `script_docs` and `dump_data_types` in a `-debug_mode -develop` session, to confirm the
   effect list for 1.20.1 and to look for cheaper/cleaner equivalents.
2. Whether `yearly_playable_pulse` merges cleanly with three GUI mods installed (Phase 1
   runtime check, `docs/RUNTIME_TESTS.md` item R1).
3. Whether `remove_short_term_gold` can push the treasury below zero (reserve logic relies
   on it not doing so when the gate passes; item R4).
