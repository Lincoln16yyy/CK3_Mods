# PERFORMANCE.md

## Cost model of Phase 1

| Routine | Trigger | Cost | Bound |
| --- | --- | --- | --- |
| `srd_yearly_playable_pulse` | once per year per playable character | one `is_ai`/`is_ruler` check | O(playable characters) |
| `srd_vassals_yearly_effect` gate | same | one game-rule read, one flag check, one `any_vassal` scan | O(direct vassals of the player) |
| `srd_pick_courtesy_target_effect` | only if the gate passed | second vassal scan + temporary list | O(direct vassals) |
| `srd_send_courtesy_effect` | at most once per year | constant work + one toast | O(1) |

Worst case per year for the player: two passes over the direct vassal list, plus the same
`is_ai` check for every AI ruler (which stops immediately because `is_ai = no` is first in
the limit).

## Design rules that keep it cheap

- No `every_county`, `every_character`, `every_ruler` or world scan anywhere.
- Expensive branches sit behind cheap gates (mode → cooldown → candidate count).
- Candidate selection happens at most once per year, and only when needed.
- No GUI property re-evaluated per frame: the interface is a decision and an event.
- No permanent modifiers are added or removed in bulk.

## What is still unknown

- Actual impact on the yearly tick in a large realm (1000+ characters). The AI branch is
  one comparison per ruler, so the expected impact is negligible, but this is an estimate,
  not a measurement.
- Whether the toast during the yearly tick causes a visible hitch (R13 in
  `RUNTIME_TESTS.md`).

## Measurement plan

1. Baseline: vanilla session, 30 in-game years, note the average daily tick time from
   `debug.log` if available.
2. With the 13 mods + patches.
3. With SRD on `Automatic` and a 60+ vassal realm.
4. Compare the three; record the result here with the session date.

Until step 4 exists, this document records a cost *model*, not a measurement.
