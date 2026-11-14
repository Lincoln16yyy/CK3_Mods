# AGENTS.md — mandatory rules for this repository

1. **Source of truth is the installed engine.** CK3 1.20.1 lives in
   `~/Downloads/Crusader Kings III/Crusader Kings III/` on the development machine
   (`clausewitz_branch.txt` = `titus/release/1.20.1`). Wiki pages and old GitHub examples
   are hints, never proof.
2. **Research before implementing.** Every effect, trigger, scope, on_action and file
   format must be located in the installed `game/` files (file + line) before it is used.
   Record the evidence in `docs/ENGINE_CAPABILITIES.md`.
3. **Prove real execution.** A feature is only "automation" when it changes persistent
   game state through a documented effect. Opening a window, selecting a character or
   showing a suggestion is *recommendation*, and must be labelled as such.
4. **Never invent capabilities.** If an effect does not exist, say so and pick another
   approach. Never fake an action in documentation, logs or UI text.
5. **Never cheat to bypass costs.** No free gold, troops, prestige, development or control.
   Every automated action must cost what the player would pay.
6. **Do not duplicate existing automation.** The 13 installed mods are audited in
   `docs/MOD_AUDIT.md`. Extend gaps, not their territory.
7. **Do not shadow contested files.** `gui/window_council.gui` and
   `gui/window_military.gui` belong to other mods (and to compatibility patches). Prefer
   decisions, events, game rules and scripted widgets.
8. **No vanilla overrides without justification.** Any override needs a documented reason,
   an isolated compatibility note and a real test.
9. **Test in runtime before claiming success.** Static validation is level A only.
   Levels B and C are defined in `docs/TEST_PLAN.md`; keep `docs/RUNTIME_TESTS.md` truthful.
10. **Keep the documentation current** in the same commit as the code: `STATUS.md`,
    `PHASE_LOG.md`, `RUNTIME_TESTS.md`, `ENGINE_CAPABILITIES.md`.
11. **Small, descriptive commits.** One logical change per commit. No force push.
12. **Never commit** saves, logs, tokens, personal data or third-party mod files.
13. **Never declare success without evidence.** Report what was executed, what was only
    read, and what remains untested.
