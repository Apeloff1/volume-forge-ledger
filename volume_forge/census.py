"""Census. Counts are measured from disk. Estimates are not law."""

from __future__ import annotations

import json
from pathlib import Path


def count_tree(root: Path) -> dict[str, object]:
    by_house: dict[str, int] = {}
    files = 0
    lines = 0
    bytes_ = 0
    for path in sorted(root.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        n = text.count("\n")
        house = path.parent.name if path.parent != root else "_root"
        by_house[house] = by_house.get(house, 0) + n
        files += 1
        lines += n
        bytes_ += path.stat().st_size
    return {
        "files": files,
        "lines": lines,
        "bytes": bytes_,
        "by_house": by_house,
    }


def write_ledger(root: Path, dest: Path) -> dict[str, object]:
    census = count_tree(root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(census, indent=2), encoding="utf-8")
    return census
