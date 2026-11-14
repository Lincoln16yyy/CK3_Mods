# PHASE_LOG.md

Newest first. Each entry: date, what changed, what was tested, what is pending.

## 2026-11-14 — Diagnóstico do primeiro teste em jogo

- Relato do usuário: entrou em inglês e continuou inglês; trocou para espanhol e continuou
  espanhol. Causa encontrada: **os dois mods novos não estavam ativos** — `dlc_load.json`
  tinha só as 16 entradas antigas, sem `Smart_Realm_Director.mod` nem
  `traducao_ptbr_120.mod`. O jogo rodou às 20:29 com `pdx_settings.txt` em `l_spanish`.
- Correção: os dois mods foram adicionados ao `dlc_load.json` (18 entradas, backup feito).
- Correção de empacotamento: a pasta `localization/replace/english/` foi substituída pelo
  espelhamento direto `localization/english/`, que é o mecanismo usado pela própria
  tradução comunitária; `replace/` foi descartada para não duplicar definições.
- O pacote passou a incluir também `localization/spanish/` (original do autor), então a
  tradução aparece tanto com o jogo em inglês quanto em espanhol.

## 2026-11-14 — Game-wide PT-BR pack built

- Found the community translation "Tradução PT-BR" (Emerson Antunes), built for the Spanish
  slot and last updated 2026-07-10 (declared 1.19).
- `tools/build_ptbr_pack.py` converts it into an English-override pack and appends the
  English original for every key it does not translate.
- Measured on the installed build: 1172 files, 286.967 translated keys, 8.063 English
  fallbacks, 96,1% of the 307.119 vanilla keys covered, zero raw keys, 78 files still
  English.
- Installed as `traducao_ptbr_120` in the mod folder. Not verified in game (no session).

## 2026-11-14 — Localization switched to Brazilian Portuguese

- The game is played in English, and CK3 has no Portuguese language slot, so every SRD
  string was rewritten in pt-BR **inside `localization/english/srd_l_english.yml`**. The
  English originals are kept in `docs/LOCALIZATION.md`.
- Static checks re-run and passing; the live copy in the mod folder was reinstalled.
- Runtime still unverified (R0–R13 unchanged).

## 2026-11-14 — Phase 0 + Phase 1 (first delivery)

**Research**
- Confirmed the installed build: CK3 1.20.1 (`clausewitz_branch.txt` =
  `titus/release/1.20.1`), install under `~/Downloads/Crusader Kings III/`.
- Read the mod folder and `dlc_load.json`: 13 automation mods active, plus three
  compatibility patches installed outside this repository.
- Audited the engine primitives needed for Phase 1 and recorded file + line evidence in
  `docs/ENGINE_CAPABILITIES.md` (`yearly_playable_pulse`, `has_game_rule`, game rules,
  `remove_short_term_gold`, `reverse_add_opinion`, `add_character_flag` with `years`,
  `every_vassal`/`any_vassal`, `add_to_temporary_list`/`random_in_list`,
  `set_variable` with a scope, `send_interface_toast`).
- Established a hard negative: CK3 1.20.1 has no Portuguese language slot
  (`game/localization/languages.yml`), so pt-BR cannot be loaded by the engine.
- Verified the `zz_maxims_mods_group.txt` pair is byte-identical (sha256
  `27225efd…f967db`), so no compatibility work is needed there.

**Implementation (Phase 1, module Smart Vassals)**
- `Smart_Realm_Director/` with game rule `srd_vassal_courtesies`
  (Off / Advisor / Supervised / Supervised default / Automatic).
- Yearly hook appended to `yearly_playable_pulse`; candidate selection; real gift
  execution costing `remove_short_term_gold` and granting `srd_courtesy_opinion` (+25,
  5 years).
- Cooldowns: ruler flag (365/180/90 days) and per-vassal flag (3 years).
- Interface: supervised event `srd_events.0001`, report event `srd_events.0100`, decision
  `srd_realm_report_decision`.
- No `gui/` file, no vanilla override, no third-party file touched.

**Tooling**
- `tools/validate.py` (level A static checks) and `.github/workflows/validate.yml`.
- `tools/install.sh` for local installation.

**Tested**
- Static: `python3 tools/validate.py` — passing (structure, braces, localization,
  references, game rules, no GUI overrides).
- Runtime: **nothing**. No CK3 session was driven; `docs/RUNTIME_TESTS.md` is entirely
  `PENDENTE`.

**Pending**
- All of `docs/RUNTIME_TESTS.md` (R0–R13).
- `script_docs` / `dump_data_types` capture in a debug session.
- Phase 2 (succession audit + shared treasury reserve) once R1–R7 pass.
