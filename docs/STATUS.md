# STATUS.md

State vocabulary: **IMPLEMENTADO** (code exists) · **VALIDADO ESTÁTICO** (level A passed) ·
**VERIFICADO EM JOGO** (level B passed) · **PENDENTE** · **NÃO INICIADO**.

| Module | Code | Static | Runtime | Notes |
| --- | --- | --- | --- | --- |
| Smart Realm Controller (core hooks, modes, cooldowns) | IMPLEMENTADO | VALIDADO ESTÁTICO | PENDENTE | one on_action hook, four game-rule modes |
| Smart Vassals — courtesies to disloyal vassals | IMPLEMENTADO | VALIDADO ESTÁTICO | PENDENTE | spends real gold for real opinion |
| Smart Treasury — reserve policy | PARCIAL | VALIDADO ESTÁTICO | PENDENTE | only the courtesy reserve floor exists |
| Smart Dynasty — succession audit | NÃO INICIADO | — | — | Phase 5 |
| Smart Military | NÃO INICIADO | — | — | Strategist Assistant owns MAA purchase; Phase 4 will only cover gaps |
| Smart Development | NÃO INICIADO | — | — | Phase 6, recommendation-first |
| Smart Diplomacy | NÃO INICIADO | — | — | Phase 7, recommendation-first |
| Interface (report decision + event) | IMPLEMENTADO | VALIDADO ESTÁTICO | PENDENTE | no GUI override |
| Texto em português (pt-BR) | IMPLEMENTADO | VALIDADO ESTÁTICO | PENDENTE | gravado em `localization/english/` porque a engine não tem slot de português; ver `docs/LOCALIZATION.md` |

## What "VALIDADO ESTÁTICO" means here

`python3 tools/validate.py` passes: descriptor fields, balanced braces/brackets, BOM and
header of every loc file, no duplicate loc keys, every referenced `srd_*` key defined,
every `srd_*` effect/trigger defined, every event id defined, every game rule used
defined, and no `gui/` file shipped.

It does **not** mean the mod works. Nothing has run inside CK3.

## Immediate next steps

1. Session with `-debug_mode -develop`, run R0–R13 in `docs/RUNTIME_TESTS.md`.
2. Capture `script_docs` and complete the capability table.
3. Only then start Phase 2 (succession audit + shared treasury policy).
