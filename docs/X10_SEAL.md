# X10 seal

Fails closed if any of the 200 shards is missing, if stored_prose is not 0, or if mass escapes prior times 1.1 per sampled step.

```bash
python - << 'PY'
from pathlib import Path
from volume_forge.shard_seal import seal
print(seal(Path("emit100"), Path("reports/x10_seal.json"), step=40)["root"])
PY
```
