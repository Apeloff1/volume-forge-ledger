# Volume Forge

Measured volumetric emit for the Skeleton house.

The delivery is a forge plus a census. Line count is read off disk after emit. It is not stamped.

## Law

- Mass grows at most prior x 1.1 per step.
- stored_prose is 0.
- Era bind carries title, era, citation, url.
- Pointer clauses only. No sentence store.
- Census overwrites any estimate.

## Compile

```bash
python -m volume_forge.emit_cli --out emit --ledger reports/ledger.json
python tests_kernel.py
```

Another agent compiles by running the emitter, then reading reports/ledger.json. Do not hand-edit emit/. Regenerate it.

Measured close: 3329408 lines, 2368 files, after restoring skeleton/secret.py (one dropped write on the first pass).

The generated tree is not in this repo. It is a regenerate. The zip delivery holds the emit.
