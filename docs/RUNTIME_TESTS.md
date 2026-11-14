# RUNTIME_TESTS.md

Runtime evidence ledger for Smart Realm Director 0.1.0.

Uma sessão real aconteceu em 14/11 (20:38–20:40), em espanhol, com os dois mods ativos. Foi
ela que revelou os três defeitos de R0 — nenhum deles detectável apenas por validação
estática. As demais linhas continuam `PENDENTE` porque ninguém abriu a interface do mod
dentro do jogo ainda.

Session baseline: CK3 1.20.1, 13 automation mods + 3 compatibility patches + SRD.
Record the date, the character, the rule setting and the observed numbers for each row.

| ID | Check | State | Observed | Notes |
| --- | --- | --- | --- | --- |
| R0 | Game starts with SRD enabled, no new error lines | **FALHOU → CORRIGIDO, RE-TESTE PENDENTE** | sessão de 14/11 20:39, jogo em espanhol: `Mounted Data: …/mod/Smart_Realm_Director` e `Enabled`; 3 defeitos: (a) 8 `.txt` sem BOM, (b) 13 `Unrecognized loc key srd_*` porque a loc só existia em inglês, (c) `Unknown trigger: limit` em `any_vassal` | (a) BOM em todos os `.txt`; (b) loc criada nos 9 idiomas; (c) `limit` removido do `any_vassal` |
| R1 | `yearly_playable_pulse` merge did not remove vanilla yearly effects | PENDENTE | — | look for vanilla yearly behaviour + any `yearly_playable_pulse` error |
| R2 | Off mode: no toast, no event, no gold change | PENDENTE | — | one in-game year with a vassal at opinion ≤ −20 |
| R3 | Advisor: single toast, gold unchanged | PENDENTE | — | count toasts over two years |
| R4 | Supervised accept: −30 gold, vassal +25 opinion | PENDENTE | — | check the opinion tooltip shows "Court courtesy" |
| R5 | Supervised decline: nothing changes, variable cleared | PENDENTE | — | re-open the report event; no stuck state |
| R6 | Automatic above reserve: gift happens once per year | PENDENTE | — | start from gold 500 |
| R7 | Automatic below reserve: nothing happens | PENDENTE | — | start from gold 100 |
| R8 | Per-vassal 3-year cooldown holds | PENDENTE | — | observe two consecutive years |
| R9 | Save/reload keeps flags and does not duplicate a gift | PENDENTE | — | save right after a gift |
| R10 | Succession keeps the Director alive | PENDENTE | — | ruler dies with an active flag |
| R11 | Report decision opens and closes cleanly | PENDENTE | — | decision appears for a ruler only |
| R12 | `error.log` / `database_conflicts.log` clean for SRD | PARCIAL | `database_conflicts.log` sem uma única linha nesta sessão | os erros do `error.log` estão em R0; confirmar que sumiram após a correção |
| R13 | Performance: no frame hitch on the yearly pulse | PENDENTE | — | with a 60+ vassal realm |

## Static evidence (for contrast)

| Item | Result | Command |
| --- | --- | --- |
| Structure, braces, loc, references | passing | `python3 tools/validate.py` |
| Primitive existence in 1.20.1 | verified by file+line | `docs/ENGINE_CAPABILITIES.md` |
| GUI overrides | none | `find Smart_Realm_Director -path '*gui*'` |

Static checks never substitute for the rows above.
