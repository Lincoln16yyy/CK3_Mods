# ARCHITECTURE.md

## Principles applied

- One namespace: every identifier starts with `srd_`.
- No `gui/` overrides. `gui/window_council.gui` and `gui/window_military.gui` are already
  owned by other mods plus two compatibility patches.
- Configuration lives in **game rules**, so every option is a real behaviour switch that
  survives save/load and succession (game rules are per-campaign).
- Execution is gated by cooldowns stored as timed character flags, which also survive
  save/load.
- Deterministic: the same treasury, vassals and flags always produce the same decision.

## Files

```
Smart_Realm_Director/
├── descriptor.mod
├── common/
│   ├── game_rules/srd_game_rules.txt            # srd_vassal_courtesies (4 modes)
│   ├── on_action/srd_on_actions.txt             # appends to yearly_playable_pulse
│   ├── scripted_effects/srd_vassals_effects.txt # gate → select → dispatch
│   ├── scripted_triggers/srd_vassals_triggers.txt
│   ├── script_values/srd_values.txt             # cost 30, reserve 150
│   ├── opinion_modifiers/srd_opinions.txt       # +25, 5 years, non-decaying
│   └── decisions/srd_decisions.txt              # read-only report entry point
├── events/srd_events.txt                        # 0001 supervised prompt, 0100 report
└── localization/english/srd_l_english.yml
```

## Yearly flow (Smart Vassals)

```
yearly_playable_pulse            (vanilla, per playable character)
└─ srd_yearly_playable_pulse     (our on_action, appended)
   └─ is_ai = no, is_ruler = yes
      └─ srd_vassals_yearly_effect
         ├─ gate: rule ≠ off, no srd_courtesy_cooldown flag,
         │        at least one vassal matching srd_courtesy_candidate_trigger
         ├─ srd_pick_courtesy_target_effect
         │        every_vassal → temporary list → random_in_list → scope:srd_candidate
         └─ dispatch
            ├─ Automatic : gold ≥ reserve  → srd_send_courtesy_effect  (spends 30 gold)
            ├─ Advisor   :                 → srd_advise_courtesy_effect (toast only)
            └─ Supervised:                 → set var + trigger srd_events.0001 (player decides)
```

## Candidate rule (`srd_courtesy_candidate_trigger`)

Alive, adult, not imprisoned, opinion of the liege ≤ −20, no `srd_gift_received` flag,
and no active `srd_courtesy_opinion` from the liege. That last clause stops the Director
from topping up an opinion that is already there.

## Cooldowns and limits

| Layer | Mechanism | Duration | Why |
| --- | --- | --- | --- |
| Ruler pulse | `srd_courtesy_cooldown` flag | 365 days (auto) / 180 days (advisor) / 90 days (supervised) | at most one gift per year |
| Per vassal | `srd_gift_received` flag on the vassal | 3 years | no gold farming, no opinion stacking |
| Report decision | decision `cooldown` | 30 days | no event spam |

## Modes (all four change behaviour)

| Mode | Spends gold | Changes opinion | Player asked | Suggestion shown |
| --- | --- | --- | --- | --- |
| Off | no | no | no | no |
| Advisor | no | no | no | yes (toast) |
| Supervised (default) | only if accepted | only if accepted | yes (event) | yes |
| Automatic | yes, above reserve floor | yes | no | yes (toast) |

## Treasury policy (Phase 1)

`srd_courtesy_reserve_value = 150` and `srd_courtesy_cost_value = 30`. Automatic mode only
runs when `gold >= 150`, so the gift leaves at least 120. Fixed numbers on purpose: they
are honest until income-aware values can be measured in a real campaign.

## Interfaces

Decisions/events instead of window overrides: the report decision opens
`srd_events.0100`, the supervised flow uses `srd_events.0001` with two options (accept is
disabled when gold is short). Phase 7 may add a scripted widget; the window files stay
untouched.

## What is deliberately absent

- No world-wide scans: only `every_vassal` of the player, once per year.
- No permanent character modifiers, no free resources, no title manipulation.
- No save-file writes, no vanilla overrides, no `gui/` files.
