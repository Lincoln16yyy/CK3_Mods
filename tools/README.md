# tools/

| File | Purpose |
| --- | --- |
| `validate.py` | Static validation (level A in `docs/TEST_PLAN.md`). Run it before every commit and in CI. |
| `install.sh` | Copies `Smart_Realm_Director/` into the CK3 mod folder and writes the `.mod` descriptor. Never touches saves or `dlc_load.json`. |

```bash
python3 tools/validate.py
./tools/install.sh
```

`validate.py` exit codes: `0` all static checks passed, `1` at least one failure (printed
with the file and the reason).

The validator reports structure only. It cannot prove the mod behaves correctly inside
CK3 — that is `docs/RUNTIME_TESTS.md`.
