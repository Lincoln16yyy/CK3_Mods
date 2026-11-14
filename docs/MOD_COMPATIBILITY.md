# MOD_COMPATIBILITY.md

Allowed states: **TESTADO E COMPATÍVEL**, **TESTADO COM LIMITAÇÕES**, **CONFLITO
CONFIRMADO**, **NÃO TESTADO**, **NÃO APLICÁVEL**.

"Compatible" is never claimed because the game opened. It requires both mods' features to
still work in the same session, which nobody has checked yet for SRD 0.1.0.

| Target | Shared surface | State | Basis |
| --- | --- | --- | --- |
| CK3 vanilla 1.20.1 | `yearly_playable_pulse` (merged via `on_actions`), own `srd_*` files | NÃO TESTADO | static only: vanilla defines the pulse, SRD appends to it |
| Auto Builder Mod | none (SRD changes no construction) | NÃO TESTADO | file inventory: no shared path |
| Automagic Architect | none | NÃO TESTADO | file inventory |
| Automatic Education | none | NÃO TESTADO | file inventory |
| Better Quality of Life | none (SRD adds no court-position logic) | NÃO TESTADO | file inventory |
| Better Marriages | `decision_group_types` untouched by SRD | NÃO TESTADO | SRD ships no decision group |
| Council Assignment Automation | none (SRD ships no `gui/`) | NÃO TESTADO | SRD file list |
| Council Autopilot | none | NÃO TESTADO | SRD file list |
| Court Automation | none (chained mod also renames its loc, SRD uses `srd_`) | NÃO TESTADO | loc key prefixes |
| Strategist Assistant | none | NÃO TESTADO | SRD file list |
| Tax Collection Automation | none (SRD spends gold, does not collect) | NÃO TESTADO | SRD file list |
| Nomad Autorefill | none | NÃO TESTADO | SRD file list |
| `caa_ca_compatch` (council patch) | `gui/window_council.gui` — SRD does not override it | NÃO TESTADO | SRD file list |
| `strategist_nomad_compatch` (military patch) | `gui/window_military.gui` — SRD does not override it | NÃO TESTADO | SRD file list |
| `loc_compatch_ca_court` | localization names — disjoint (`srd_` vs `ca_court_automation_`) | NÃO TESTADO | loc key prefixes |

## Recommended load order

1. The 13 automation mods (any order that already works for them).
2. The three compatibility patches last: `caa_ca_compatch`, `strategist_nomad_compatch`,
   `loc_compatch_ca_court`.
3. **Smart Realm Director** — it overrides nothing, so its position only matters if a
   future version adds an override.

## Conflict risks to watch in the first session

- A second `yearly_playable_pulse` declaration that replaces instead of appending would
  silently disable vanilla's yearly effects. Detection: vanilla yearly behaviour missing
  and `error.log` mentioning `yearly_playable_pulse`.
- Toast spam if several modules fire in the same year (only one module exists today).
- Two mods both writing `mod/ca_l_*.yml` would re-create the Court Automation problem;
  SRD does not ship any `ca_*` file.
