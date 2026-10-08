# Doctor

Stride doctor for a regenerated emit tree.

```bash
python -m volume_forge.emit_cli --out emit --ledger reports/ledger.json
python - << 'PY'
from pathlib import Path
from volume_forge.doctor import seal
from volume_forge.seal import root_of
body = seal(Path("emit"), Path("reports/seal.json"), step=128)
print(root_of(body["rows"]))
PY
python tests_doctor.py
```

Missing organs fail closed. Mass above prior times 1.1 per verb fails closed. stored_prose must be 0.

Live seal on the local emit: expected 2304, missing 0, sampled 9 at stride 256, root f572f08c935e5db97c0c3a92728a62060828c8fabc76286432dfd25afba29cb9.
