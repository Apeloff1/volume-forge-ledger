# Implement

1. Clone this repo.
2. Run `python -m volume_forge.emit_cli --out emit --ledger reports/ledger.json`.
3. Discard the estimate. Read `reports/ledger.json`.
4. Run `python tests_kernel.py`.
5. Import any `emit/<house>/<organ>.py` and call `run(1.0)`.
6. Refuse the module if stored_prose != 0 or mass exceeds prior * 1.1 per verb.

Catalog: 64 houses, 36 organs, 48 verbs. Seed family 8847291.
