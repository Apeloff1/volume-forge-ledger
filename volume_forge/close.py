"""Close the forge. File counts are live. Line counts are prior wc seals."""

from __future__ import annotations

import json
from pathlib import Path

SEALS = {
    "organ": {"dir": "emit", "files": 2368, "lines": 3329408, "census": "census.py"},
    "masterplan": {"dir": "emit10", "files": 200, "lines": 15302600, "census": "wc -l"},
    "x10": {"dir": "emit100", "files": 200, "lines": 153003200, "census": "wc -l"},
}


def close(root: Path) -> dict[str, object]:
    strata = []
    for name, spec in SEALS.items():
        path = root / spec["dir"]
        found = len(list(path.glob("**/*.py"))) if path.is_dir() else 0
        strata.append({
            "name": name,
            "dir": spec["dir"],
            "files_found": found,
            "files_sealed": spec["files"],
            "lines_sealed": spec["lines"],
            "census": spec["census"],
            "files_ok": found == spec["files"],
        })
    body = {
        "stored_prose": 0,
        "clip": 1.1,
        "seed": 8847291,
        "lines_sealed": sum(s["lines_sealed"] for s in strata),
        "files_ok": all(s["files_ok"] for s in strata),
        "strata": strata,
        "debts": [
            "shared control flow, unique coefficients",
            "x10 full shard import OOMs at 85000 functions",
            "generated trees are not in git",
        ],
    }
    dest = root / "reports" / "CLOSE.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(body, indent=2), encoding="utf-8")
    return body


if __name__ == "__main__":
    print(json.dumps(close(Path(".")), indent=2))
