"""Sample runner. Executes a stride of emitted organs and checks invariants."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


def sample(emit_root: Path, stride: int = 64) -> dict[str, object]:
    sys.path.insert(0, str(emit_root.parent))
    package = emit_root.name
    rows = []
    modules = sorted(emit_root.rglob("*.py"))
    picked = [p for p in modules if p.name != "__init__.py"][::stride]
    for path in picked:
        mod = importlib.import_module(f"{package}.{path.parent.name}.{path.stem}")
        out = mod.run(1.0)
        if int(out["stored_prose"]) != 0:
            raise RuntimeError("stored_prose")
        if float(out["mass"]) > 1.1 ** int(out["steps"]) + 1e-6:
            raise RuntimeError("mass escaped clip")
        rows.append({"house": path.parent.name, "organ": path.stem, "mass": out["mass"], "root": out["root"], "steps": out["steps"]})
    return {"sampled": len(rows), "rows": rows}
