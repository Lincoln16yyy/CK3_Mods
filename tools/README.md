# tools/

| File | Purpose |
| --- | --- |
| `validate.py` | Static validation (level A in `docs/TEST_PLAN.md`). Run it before every commit and in CI. |
| `install.sh` | Copies `Smart_Realm_Director/` into the CK3 mod folder and writes the `.mod` descriptor. Never touches saves or `dlc_load.json`. |
| `build_ptbr_pack.py` | Converts the community PT-BR translation (Spanish slot) into an English-override pack, appending English for every key it does not translate. See `docs/PTBR_TRANSLATION.md`. |

```bash
python3 tools/validate.py
./tools/install.sh
```

`validate.py` exit codes: `0` all static checks passed, `1` at least one failure (printed
with the file and the reason).

The PT-BR pack is third-party work; only the builder script lives in this repository:

```bash
python3 tools/build_ptbr_pack.py --source <repo>/traducao_pt_br \
  --game "$HOME/Downloads/Crusader Kings III/Crusader Kings III/game" \
  --out  "<CK3 user dir>/mod/traducao_ptbr_120"
```

The validator reports structure only. It cannot prove the mod behaves correctly inside
CK3 — that is `docs/RUNTIME_TESTS.md`.
