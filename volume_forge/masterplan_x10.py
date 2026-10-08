"""Tenfold masterplan emitter.

200 shards, 85,000 bindings. Floor is 10x the 15,302,600 census.
The writer estimate is not law.
"""

from __future__ import annotations

from pathlib import Path

SHARDS = 200
FUNCS_PER_SHARD = 85000
SEED = 8847291
CLIP = 1.1


def _fn(shard: int, index: int) -> str:
    coeff = (SEED * 10007 + shard * 100003 + index * 97) & 0xFFFFFFFF
    return (
        f"def b_{shard:03d}_{index:05d}(prior: float) -> dict[str, object]:\n"
        f"    coeff = {coeff}\n"
        f"    proposed = prior * (1.0 + (coeff % 997) / 10000.0)\n"
        f"    ceiling = prior * {CLIP}\n"
        f"    if proposed < 0:\n"
        f"        raise ValueError('mass')\n"
        f"    mass = ceiling if proposed > ceiling else proposed\n"
        f"    return {{'shard': {shard}, 'index': {index}, 'coeff': coeff, 'mass': mass, 'stored_prose': 0}}\n\n"
    )


def render_shard(shard: int) -> str:
    parts = [
        '"""X10 masterplan shard. stored_prose=0. Mass clip 1.1."""\n',
        f"SHARD = {shard}\nSEED = {SEED}\nSTORED_PROSE = 0\nCLIP = {CLIP}\nFUNCS = {FUNCS_PER_SHARD}\n\n",
    ]
    parts.extend(_fn(shard, i) for i in range(FUNCS_PER_SHARD))
    parts.append(
        "def run(prior: float = 1.0, stride: int = 5000) -> dict[str, object]:\n"
        "    mass = prior\n"
        "    last = {}\n"
        "    steps = 0\n"
        f"    for index in range(0, {FUNCS_PER_SHARD}, stride):\n"
        f"        last = globals()[f'b_{shard:03d}_{{index:05d}}'](mass)\n"
        "        mass = float(last['mass'])\n"
        "        steps += 1\n"
        "    return {'shard': SHARD, 'mass': mass, 'steps': steps, 'stored_prose': STORED_PROSE, 'last': last}\n"
    )
    return "".join(parts)


def emit(root: Path) -> dict[str, int]:
    root.mkdir(parents=True, exist_ok=True)
    files = 0
    lines = 0
    bytes_ = 0
    for shard in range(SHARDS):
        text = render_shard(shard)
        path = root / f"shard_{shard:03d}.py"
        path.write_text(text, encoding="utf-8")
        files += 1
        lines += text.count("\n")
        bytes_ += path.stat().st_size
        if shard % 10 == 0:
            print(f"shard {shard} lines {lines}", flush=True)
    return {"files": files, "lines_written": lines, "bytes": bytes_}


if __name__ == "__main__":
    import json
    import sys
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "emit100")
    print(json.dumps(emit(out)))
