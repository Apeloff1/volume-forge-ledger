# Push x10

Branch forge/x10.

Census: wc -l emit100/shard_*.py = 153003200
Bytes: 6057526890
Files: 200
Bindings: 85000 per shard
stored_prose: 0
clip: 1.1

Compile:

```bash
python -m volume_forge.masterplan_x10 emit100
wc -l emit100/shard_*.py
```

Do not commit emit100.
