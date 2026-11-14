# MOD_AUDIT.md

Inventory taken from the live mod folder:
`~/.config/hydralauncher/wine-prefixes/1158310/drive_c/users/steamuser/Documents/Paradox Interactive/Crusader Kings III/mod`.
Load order was read from the same directory's `dlc_load.json` (13 active mods).

Legend for "audit depth": **files read** = descriptors plus the file list and the GUI
paths listed; **deep** = script contents inspected while designing SRD. Nothing below was
executed in game, so no behaviour claim is a runtime claim.

| # | Mod | Version | supported_version | Audit depth | What it automates (as declared by its files) | Overlaps SRD? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Auto Builder Mod | 3.2.2 | 1.20.1.2 | files read | Construction decisions via its own window (`gui/js_ab_window.gui`) | Builds; SRD will not touch construction |
| 2 | Automagic Architect (The Lazy Lord's Construction Tool) | 1.20.0.4 | 1.20.1.2 | files read | Construction tool (events `clrbnit_magic.8000-8013`) | same territory as #1 |
| 3 | Automatic Education — Guardian & University Manager | 1.6.0 | 1.19.* | files read | Guardian/university assignment (`autoedu_settings_window.gui`) | Education; SRD keeps out |
| 4 | Better Quality of Life (Maxim) | 2.2.9 | 1.20.* | files read | Court positions, mass prison actions, settings window | SRD must avoid court-position logic |
| 5 | Better Marriages: Marry Off All Children | 2.0.4 | 1.20.* | files read | Mass child betrothal/marriage (`mmoc_window.gui`) | Marriage; SRD keeps out |
| 6 | Council Assignment Automation | 0.1.1 | 1.20.* | deep | Council task assignment UI; overrides `gui/window_council.gui` to add one button | Council; SRD does not touch that window |
| 7 | Council Automation | 1.2 | 1.20.* | deep | Game rule `ca_councillors`, per-councillor "work alone" toggle; redefines `widget_councillor_item` in `gui/ca_councillor_item.gui` | Council; SRD does not touch |
| 8 | Council Autopilot | 1.1.5 | 1.20.* | deep | Council task automation buttons; overrides `gui/window_council.gui` | Council; SRD does not touch |
| 9 | Court Automation | 0.3.0 | 1.20.* | deep | Court positions, knights, court maintenance; own game rule file; loc files named `ca_l_<lang>.yml` | Court; SRD does not touch |
| 10 | Strategist Assistant | (no version field) | 1.20.1.* | deep | MAA/war planning panels; overrides `gui/window_military.gui` | Military; SRD does not touch |
| 11 | Nomad Autorefill | 0.1.2 | 1.20.* | deep | Nomad MAA refill controls; overrides `gui/window_military.gui` | Military; SRD does not touch |
| 12 | One-Click Vassal Transfer | 1.5.1 | 1.20.* | files read | Title/vassal transfer from `gui/window_title.gui` | Vassal titles; SRD gifts opinion instead |
| 13 | Tax Collection Automation | 0.3.0 | 1.20.1.* | files read | Tax collection flow, several scripted-widget adapters | Treasury income; SRD only spends |

## Known conflicts and their current handling

**Council Assignment Automation × Council Autopilot** both replace
`gui/window_council.gui`. A separate compatch (`caa_ca_compatch`, installed outside this
repository) merges the three council contributions into one file loaded last. SRD
deliberately contributes **no** `gui/window_council.gui`.

**Strategist Assistant × Nomad Autorefill** both replace `gui/window_military.gui`; the
compatch `strategist_nomad_compatch` merges them. SRD contributes **no**
`gui/window_military.gui`.

**Better Marriages × Better Quality of Life** both ship
`common/decision_group_types/zz_maxims_mods_group.txt`. Measured with sha256 on the
installed copies: both are `27225efd406bc2d0cf91dfb4e743d611c9feb1e0ca16fafe03355acefff967db`,
i.e. byte-identical. No action needed and none was taken.

**Localization clash** Court Automation and Council Automation both ship
`localization/<lang>/ca_l_<lang>.yml`, so only one of the two loads. The installed
`loc_compatch_ca_court` restores Court Automation's 65 keys per language under unique file
names. SRD names every file `srd_*`, so it cannot collide.

## What could not be inspected

- Runtime behaviour of all 13 mods (no game session was driven by the agent).
- Paradox Mods / Steam Workshop pages for #10 and #12 (no version metadata online was
  cross-checked; only the local files were read).
- Whether the two council compatibility patches behave as intended in game.
