# CK3_Mods

Modding projects for Crusader Kings III. Each project lives in its own directory so the
repository can hold several unrelated mods.

| Directory | What it is | State |
| --- | --- | --- |
| `Smart_Realm_Director/` | Autonomous realm administrator (this project) | Phase 1 implemented, runtime tests pending |
| `docs/` | Technical documentation | Living documents |
| `tools/` | Static validator, install helper and the PT-BR pack builder | Working |

## Jogo em português (PT-BR)

O CK3 1.20.1 não tem idioma português, então o jogo inteiro em PT-BR é feito substituindo
o pacote de um idioma existente. `tools/build_ptbr_pack.py` converte a tradução
comunitária "Tradução PT-BR" (de Emerson Antunes, feita para o slot espanhol) em um pacote
que cobre **inglês e espanhol**, com fallback no idioma nativo para chaves não traduzidas.

Cobertura medida: **96,1%** das 307.119 chaves do vanilla, **zero chave crua** nos arquivos
substituídos, 78 arquivos ainda em inglês. Método, instalação e limites em
`docs/PTBR_TRANSLATION.md`. O pacote gerado (29 MB) fica fora do git.

## Smart Realm Director

A CK3 mod that administers the realm for the player: it executes the administrative work
that the engine can genuinely perform, never fakes an action, never spawns gold or troops,
and leaves strategic decisions to the player.

**Phase 1 module — Smart Vassals (courtesies).** Every year the Director looks for one
vassal with a poor opinion of the ruler and either gifts them gold for a real opinion gain
(paid from the treasury), asks you first, only advises, or does nothing — depending on the
game rule you pick. It is the first module because no installed automation mod covers it.

### Install

```bash
./tools/install.sh                      # auto-detect, or pass the CK3 user dir
```

Then enable **Smart Realm Director** in the launcher. Load order guidance and the
compatibility matrix are in `docs/MOD_COMPATIBILITY.md`.

### Configure

Game rule *Smart Realm Director: Courtesies to Vassals* (category **Game Modes**):
`Off` / `Advisor` / `Supervised` (default) / `Automatic`. Every option changes real
behaviour; nothing is decorative.

The in-game interface is the decision **Ask the Director for a Report** plus the supervised
event. No `gui/window_*.gui` file is overridden: those windows are already contested by
other installed mods.

### Status, honestly

- **Verified statically:** every script primitive used here exists in the installed
  CK3 1.20.1 files (see `docs/ENGINE_CAPABILITIES.md` for file and line evidence), the
  files are balanced, localization is complete and CI passes.
- **Not verified:** nothing has been executed inside the game yet. `docs/RUNTIME_TESTS.md`
  lists the exact checks that still need a running CK3.
- **Language:** CK3 1.20.1 ships nine languages and Portuguese is not one of them
  (`game/localization/languages.yml`), so a pt-BR file can never be loaded. The game runs
  in English here, therefore the mod's in-game text is **Brazilian Portuguese stored in
  `localization/english/srd_l_english.yml`** — it displays as Portuguese because the
  English file is the one the engine reads. Details and the English originals:
  `docs/LOCALIZATION.md`.

### Documentation

- `docs/AI_CONTEXT.md` — context for a new agent or contributor
- `docs/ENGINE_CAPABILITIES.md` — what the installed engine provably supports
- `docs/MOD_AUDIT.md`, `docs/MOD_COMPATIBILITY.md` — the 13 installed mods
- `docs/GAP_ANALYSIS.md` — coverage matrix and the five candidate automations
- `docs/ARCHITECTURE.md` — module design, flow and cost
- `docs/TEST_PLAN.md`, `docs/RUNTIME_TESTS.md` — levels A/B/C and pending checks
- `docs/LOCALIZATION.md` — why the text is Portuguese inside the English file
- `docs/PERFORMANCE.md`, `docs/PHASE_LOG.md`, `docs/STATUS.md`
- `docs/DEVELOPMENT_GUIDE.md` — environment, debug mode, workflow
