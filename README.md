# Volume Forge

Built on main. No feature branch required.

```bash
python tests_kernel.py
python tests_doctor.py
python -m volume_forge
```

Exit 0 means file counts match the seals. Exit 2 means a tree is missing.

Sealed lines: organ 3329408, masterplan 15302600, x10 153003200. Sum 171635208.
stored_prose 0. clip 1.1. seed 8847291.

Regenerate trees. Do not commit them.

```bash
python -m volume_forge.emit_cli --out emit --ledger reports/ledger.json
python -m volume_forge.masterplan emit10
python -m volume_forge.masterplan_x10 emit100
```
