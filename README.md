# Volume Forge

Source is on main. Generated trees are not.

## Census

- organ emit: 3329408 lines, 2368 files
- masterplan shards: 15302600 lines, 200 files
- x10 shards: 153003200 lines, 200 files, 6057526890 bytes
- stored_prose: 0
- mass clip: 1.1
- seed: 8847291

Counts are wc after emit. Writer estimates are not law.

## Compile

```bash
python -m volume_forge.emit_cli --out emit --ledger reports/ledger.json
python -m volume_forge.masterplan emit10
python -m volume_forge.masterplan_x10 emit100
wc -l emit100/shard_*.py
python tests_kernel.py
python tests_doctor.py
```

Do not commit emit, emit10, or emit100. Regenerate them.
