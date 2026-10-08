"""Shard seal for the tenfold tree. Missing shards fail closed."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from volume_forge.kernel import MASS_CLIP, merkle_root

SHARDS = 200


def missing(root: Path) -> list[str]:
    return [f"shard_{i:03d}" for i in range(SHARDS) if not (root / f"shard_{i:03d}.py").is_file()]


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample(root: Path, step: int = 40) -> list[dict[str, object]]:
    rows = []
    for i in range(0, SHARDS, step):
        path = root / f"shard_{i:03d}.py"
        module = _load(path)
        out = module.run(1.0, stride=10000)
        steps = int(out["steps"])
        mass = float(out["mass"])
        if int(out["stored_prose"]) != 0:
            raise RuntimeError("stored_prose")
        if mass > MASS_CLIP ** steps + 1e-6:
            raise RuntimeError(f"mass escaped {path.name}")
        rows.append({"shard": i, "mass": mass, "steps": steps, "stored_prose": 0})
    return rows


def root_of(rows: list[dict[str, object]]) -> str:
    leaves = [hashlib.sha256(f"{r['shard']}|{r['mass']}".encode()).digest() for r in rows]
    return merkle_root(leaves)


def seal(root: Path, dest: Path, step: int = 40) -> dict[str, object]:
    gone = missing(root)
    rows = sample(root, step=step) if not gone else []
    body = {
        "expected": SHARDS,
        "missing": gone,
        "sampled": len(rows),
        "rows": rows,
        "root": root_of(rows) if rows else "",
        "ok": not gone and bool(rows),
        "stored_prose": 0,
        "clip": MASS_CLIP,
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(body, indent=2), encoding="utf-8")
    if gone:
        raise RuntimeError("missing shards")
    return body
