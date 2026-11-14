# GAP_ANALYSIS.md

Classification vocabulary (mandatory):
**EXECUÇÃO REAL COMPROVADA** · **EXECUÇÃO POSSÍVEL, PRECISA TESTAR** ·
**INTEGRAÇÃO EXTERNA COMPROVADA** · **SOMENTE RECOMENDAÇÃO** · **NÃO SUPORTADA**.

"Comprovada" here means *the primitive exists in the installed 1.20.1 files* (see
`ENGINE_CAPABILITIES.md`). It does not mean SRD has executed it in game; that column is
`RUNTIME_TESTS.md`.

| System | Existing mod | Current function | Gap | Engine capability | Evidence | Priority | Test plan |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Council tasks | Council Autopilot / Council Automation / CAA | Assigns tasks, per-councillor toggles | none worth taking | — | `gui/window_council.gui` overrides | NÃO APLICÁVEL | — |
| Court positions & knights | Court Automation, BQoL | Fills positions, manages knights | none worth taking | — | `court_automation/gui/*` | NÃO APLICÁVEL | — |
| Construction | Auto Builder, Automagic Architect | Chooses and starts buildings | none worth taking | — | mods' own windows | NÃO APLICÁVEL | — |
| Education | Automatic Education | Guardians, university | none worth taking | — | `autoedu_*` | NÃO APLICÁVEL | — |
| Marriages of children | Better Marriages | Mass betrothal | none worth taking | — | `mmoc_*` | NÃO APLICÁVEL | — |
| MAA / war economy | Strategist Assistant, Nomad Autorefill | Purchase planning, refill | real purchase execution is theirs | — | `mwp_*`, `na_*` | NÃO APLICÁVEL | — |
| Taxes | Tax Collection Automation | Collection flow | none worth taking | — | `tcr*` adapters | NÃO APLICÁVEL | — |
| **Vassal opinion / stability** | none | — | **no mod gifts, sways or reconciles vassals automatically** | `reverse_add_opinion` + `remove_short_term_gold` + timed flags | `hike.txt:139`, `js_ab_domicile_effects.txt:35` | **P1 (implemented)** | R1–R5 |
| Succession readiness | none | — | no pre-succession audit (heir, regency risk, treasury buffer) | triggers + decisions + saved scopes | `on_action/death.txt` | P2 | R6 |
| Treasury planning | none (Auto Builder spends, Tax collects) | — | no reserve policy shared by modules | script values + game rules | `game_rules/00_game_rules.txt` | P2 | R7 |
| Faction risk | none | — | no early warning / reconciliation loop | `has_faction`-style triggers, opinion effects | `00_faction_interactions.txt` | P3 | R8 |
| Plague / disaster response | BQoL (manual tools) | manual | no automatic quarantine/isolation policy | needs capability proof | not found yet | P4 | — |
| War declaration | — | player only | stays player-only (deliberate) | — | `AGENTS.md` rule 5 | NÃO SUPORTADA (por decisão) | — |
| Autonomous warfare | — | — | not attempted | no proof | — | NÃO SUPORTADA | — |

## Five most promising own automations (ranked)

1. **Smart Vassals — courtesies to disloyal vassals.** Real gold, real opinion, no
   overlap, cheap to run. *Implemented in Phase 1.* Status: EXECUÇÃO POSSÍVEL, PRECISA TESTAR.
2. **Smart Dynasty — succession readiness audit.** Detect old ruler + weak heir + thin
   treasury, then recommend/prepare (legitimacy, guardians, reserves). SOMENTE RECOMENDAÇÃO
   in the safe version; any execution needs a proven effect per action.
3. **Smart Treasury — reserve policy.** One shared reserve floor that every module respects,
   plus a yearly "can we afford this?" gate. Currently implemented only as the courtesy
   reserve check.
4. **Smart Vassals — faction watch.** Early list of factions near their ultimatum threshold
   with a recommendation per faction. SOMENTE RECOMENDAÇÃO until each counter-action is
   proven.
5. **Smart Development — domain audit.** Which domain counties are under-developed or
   low-control, and which council task would fix it (delegating the action to the council
   mods instead of duplicating them). SOMENTE RECOMENDAÇÃO.

## Explicit non-goals

- Replacing Auto Builder, Court Automation, Council Autopilot or Strategist.
- Declaring war, revoking titles or imprisoning vassals without the player.
- Any action whose only implementation would be generating resources.
