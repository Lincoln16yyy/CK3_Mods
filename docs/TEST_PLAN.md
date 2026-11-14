# TEST_PLAN.md

Three levels. A level is only "passed" when its own evidence exists.

## Level A — static (implemented, CI)

`python3 tools/validate.py` checks:

| # | Check | Failure means |
| --- | --- | --- |
| A1 | `descriptor.mod` has version / name / supported_version | launcher may reject the mod |
| A2 | balanced `{}` and `[]` outside strings and comments | parse error in game |
| A3 | loc file has BOM, correct header, no duplicate key | unlocalized text or silent override |
| A4 | every referenced `srd_*` loc key is defined | raw key shown in game |
| A5 | every `srd_*` effect/trigger called with `= yes` is defined | "unknown effect" in error.log |
| A6 | every triggered `srd_*` event id is defined | nothing happens on trigger |
| A7 | every `has_game_rule` setting used is defined | gate silently false |
| A8 | no `gui/` file ships in Phase 1 | accidental window override |

Status: **passing** (see CI badge/run). Static success says nothing about behaviour.

## Level B — functional in CK3 (pending)

| ID | Case | Setup | Expected |
| --- | --- | --- | --- |
| R1 | Mod loads | enable only SRD + vanilla | no SRD error lines in `error.log`; game rule visible |
| R2 | Off mode is silent | rule = Off, veiled vassal | no toast, no event, gold unchanged for one year |
| R3 | Advisor mode | rule = Advisor, vassal with opinion ≤ −20 | toast once, gold unchanged |
| R4 | Supervised accept | rule = Supervised | event appears; accept → −30 gold, vassal opinion +25 |
| R5 | Supervised decline | same, choose "Not now" | no gold change, no opinion change, variable cleared |
| R6 | Automatic + reserve | rule = Automatic, gold 500 | one gift in the year, gold ≈ 470, vassal +25 |
| R7 | Automatic below reserve | gold 100 (< 150) | no gift, no toast, no negative gold |
| R8 | Per-vassal cooldown | gift twice in 3 years | second year: no gift to the same vassal |
| R9 | Persistence | save, reload, wait a year | flags still honoured; no double gift in the same year |
| R10 | Succession | die with a gift flag active | new ruler: no crash, automation keeps working |

## Level C — long campaigns (pending)

Ten-year, thirty-year and hundred-year runs, as count → duke → king → emperor, plus clan
and nomadic governments where applicable. Measure treasury, development, military
strength, factions, successions, wall-clock performance and accumulated log errors. Use
dedicated test saves, never the player's campaign.

## Reporting rule

`docs/RUNTIME_TESTS.md` is the only place where runtime results live. A case is
`PASS` only with the observed values written next to it; otherwise it stays `PENDENTE`.
