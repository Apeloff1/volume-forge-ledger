"""Volumetric emitter.

Expands the house catalog into importable organ modules.
Each binding carries a unique coefficient, a clip, and a pointer hash.
The emit is generated. The census measures it. Neither may invent a count.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from volume_forge.catalog import HOUSES, ORGANS, VERBS
from volume_forge.kernel import SEED_FAMILY, STORED_PROSE


def _coeff(house: str, organ: str, verb: str, ordinal: int) -> int:
    raw = f"{house}|{organ}|{verb}|{ordinal}|{SEED_FAMILY}".encode()
    return int(hashlib.sha256(raw).hexdigest()[:8], 16)


def render_module(house: str, organ: str, house_i: int, organ_i: int) -> str:
    lines = [
        '"""Organ module. Pointer atom. stored_prose=0."""',
        "from __future__ import annotations",
        "",
        "import hashlib",
        "import struct",
        "",
        f"HOUSE = {house!r}",
        f"ORGAN = {organ!r}",
        f"HOUSE_I = {house_i}",
        f"ORGAN_I = {organ_i}",
        f"SEED = {SEED_FAMILY}",
        f"STORED_PROSE = {STORED_PROSE}",
        "MASS_CLIP = 1.1",
        "N_CAP = 8",
        "",
        "def _clip(proposed: float, prior: float) -> float:",
        "    if prior <= 0:",
        "        raise ValueError('prior mass must be positive')",
        "    ceiling = prior * MASS_CLIP",
        "    if proposed < 0:",
        "        raise ValueError('mass cannot be negative')",
        "    return ceiling if proposed > ceiling else proposed",
        "",
        "def _pointer(verb: str, ordinal: int) -> str:",
        "    payload = f'{HOUSE}/{ORGAN}/{verb}#{ordinal}|{SEED}|prose={STORED_PROSE}'.encode()",
        "    return hashlib.sha256(payload).hexdigest()",
        "",
        "def _leaf(verb: str, ordinal: int, mass: float) -> bytes:",
        "    packed = struct.pack('>dI', float(mass), ordinal & 0xFFFFFFFF)",
        "    return hashlib.sha256(f'{HOUSE}/{ORGAN}/{verb}'.encode() + packed).digest()",
        "",
    ]
    bindings = []
    for verb_i, verb in enumerate(VERBS):
        coeff = _coeff(house, organ, verb, verb_i)
        fn = f"v_{verb}_{verb_i:02d}"
        bindings.append(fn)
        lines.extend([
            f"def {fn}(prior: float, seed: int = SEED) -> dict[str, object]:",
            f"    coeff = {coeff}",
            "    proposed = prior * (1.0 + (coeff % 997) / 10000.0)",
            "    mass = _clip(proposed, prior)",
            f"    pointer = _pointer({verb!r}, {verb_i})",
            "    leaf = _leaf(%r, %d, mass)" % (verb, verb_i),
            "    era = f'HOUSE_ERA.{HOUSE}.{ORGAN}'",
            "    citation = 'era_bind:' + pointer[:16]",
            "    url = f'pointer://{HOUSE}/{ORGAN}/%s'" % verb,
            "    if STORED_PROSE != 0:",
            "        raise ValueError('stored_prose')",
            "    return {",
            "        'house': HOUSE,
            "        'organ': ORGAN,
            f"        'verb': {verb!r},",
            "        'ordinal': %d," % verb_i,
            "        'coeff': coeff,
            "        'mass': mass,
            "        'pointer': pointer,
            "        'leaf': leaf.hex(),",
            "        'era': era,
            "        'citation': citation,
            "        'url': url,
            "        'seed': seed,
            "        'stored_prose': STORED_PROSE,
            "        'G_delta': mass - prior,
            "    }",
            "",
        ])
    lines.append("BINDINGS = (")
    for fn in bindings:
        lines.append(f"    {fn},")
    lines.append(")")
    lines.extend([
        "",
        "def run(prior: float = 1.0, seed: int = SEED) -> dict[str, object]:",
        "    mass = prior",
        "    last = {}",
        "    leaves = []",
        "    for fn in BINDINGS:",
        "        last = fn(mass, seed)",
        "        mass = float(last['mass'])",
        "        leaves.append(str(last['leaf']))",
        "    root = hashlib.sha256(''.join(leaves).encode()).hexdigest()",
        "    return {'house': HOUSE, 'organ': ORGAN, 'mass': mass, 'steps': len(BINDINGS), 'root': root, 'stored_prose': STORED_PROSE, 'last': last}",
        "",
    ])
    return "\n".join(lines) + "\n"


def emit_tree(root: Path) -> dict[str, int]:
    root.mkdir(parents=True, exist_ok=True)
    files = 0
    lines = 0
    for house_i, house in enumerate(HOUSES):
        house_dir = root / house
        house_dir.mkdir(parents=True, exist_ok=True)
        (house_dir / "__init__.py").write_text(f'"""House pointer {house}. stored_prose=0."""\nHOUSE = {house!r}\n', encoding="utf-8")
        files += 1
        lines += 2
        for organ_i, organ in enumerate(ORGANS):
            text = render_module(house, organ, house_i, organ_i)
            (house_dir / f"{organ}.py").write_text(text, encoding="utf-8")
            files += 1
            lines += text.count("\n")
    return {"files": files, "lines_estimated": lines}
