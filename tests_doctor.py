"""Doctor tests. Fail closed on missing organs."""

from pathlib import Path

from volume_forge.catalog import HOUSES, ORGANS
from volume_forge.doctor import expected_modules, missing
from volume_forge.seal import root_of


def test_catalog_width() -> None:
    assert len(expected_modules()) == len(HOUSES) * len(ORGANS)


def test_missing_sees_gap() -> None:
    tmp = Path("/tmp/vf_gap")
    house = tmp / "nexus"
    house.mkdir(parents=True, exist_ok=True)
    (house / "mass.py").write_text("HOUSE='nexus'\n", encoding="utf-8")
    gone = missing(tmp)
    assert "nexus/pointer" in gone
    assert "nexus/mass" not in gone


def test_seal_root_stable() -> None:
    rows = [
        {"house": "nexus", "organ": "mass", "root": "abc", "mass": 1.1},
        {"house": "nexus", "organ": "pointer", "root": "def", "mass": 1.21},
    ]
    assert root_of(rows) == root_of(rows)


if __name__ == "__main__":
    test_catalog_width()
    test_missing_sees_gap()
    test_seal_root_stable()
    print("doctor-ok")
