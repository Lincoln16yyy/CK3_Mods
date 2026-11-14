# RUNTIME_TESTS.md

Runtime evidence ledger for Smart Realm Director 0.1.0.

**Nothing in this file has been executed yet.** The mod was written and statically
validated without driving a CK3 session; no agent has clicked through the game for this
version. Every row is therefore `PENDENTE` and must be filled in by whoever runs the game.

Session baseline: CK3 1.20.1, 13 automation mods + 3 compatibility patches + SRD.
Record the date, the character, the rule setting and the observed numbers for each row.

| ID | Check | State | Observed | Notes |
| --- | --- | --- | --- | --- |
| R0 | Game starts with SRD enabled, no new error lines | PENDENTE | — | compare against a session without SRD |
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
| R12 | `error.log` / `database_conflicts.log` clean for SRD | PENDENTE | — | attach the SRD-related lines |
| R13 | Performance: no frame hitch on the yearly pulse | PENDENTE | — | with a 60+ vassal realm |

## Static evidence (for contrast)

| Item | Result | Command |
| --- | --- | --- |
| Structure, braces, loc, references | passing | `python3 tools/validate.py` |
| Primitive existence in 1.20.1 | verified by file+line | `docs/ENGINE_CAPABILITIES.md` |
| GUI overrides | none | `find Smart_Realm_Director -path '*gui*'` |

Static checks never substitute for the rows above.
