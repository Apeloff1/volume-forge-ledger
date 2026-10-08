"""Doctor. Stride-executes organs and refuses a lying tree."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from volume_forge.catalog import HOUSES, ORGANS, VERBS
from volume_forge.kernel import MASS_CLIP, STORED_PROSE


class DoctorFault(RuntimeError):
    pass


def expected_modules() -> list[tuple[str, str]]:
    return [(house, organ) for house in HOUSES for organ in ORGANS]


def missing(emit_root: Path) -> list[str]:
    gone = []
    for house, organ in expected_modules():
        if not (emit_root / house / f"{organ}.py").is_file():
            gone.append(f"{house}/{organ}")
    return gone


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem + "_" + path.parent.name, path)
    if spec is None or spec.loader is None:
        raise DoctorFault(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stride(emit_root: Path, step: int = 128) -> list[dict[str, object]]:
    rows = []
    modules = [emit_root / house / f"{organ}.py" for house, organ in expected_modules()]
    for path in modules[::step]:
        module = _load(path)
        out = module.run(1.0)
        steps = int(out["steps"])
        mass = float(out["mass"])
        if int(out["stored_prose"]) != STORED_PROSE:
            raise DoctorFault("stored_prose")
        if mass > MASS_CLIP ** steps + 1e-6:
            raise DoctorFault(f"mass escaped {path}")
        if steps != len(VERBS):
            raise DoctorFault(f"verb width {path}")
        rows.append({"house": out["house"], "organ": out["organ"], "mass": mass, "steps": steps, "root": out["root"], "stored_prose": 0})
    return rows


def seal(emit_root: Path, dest: Path, step: int = 128) -> dict[str, object]:
    gone = missing(emit_root)
    rows = stride(emit_root, step=step) if not gone else []
    body = {"expected": len(expected_modules()), "missing": gone, "sampled": len(rows), "stride": step, "stored_prose": STORED_PROSE, "clip": MASS_CLIP, "rows": rows, "ok": not gone and bool(rows)}
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(body, indent=2), encoding="utf-8")
    if gone:
        raise DoctorFault("missing organs")
    return body
