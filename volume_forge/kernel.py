"""Volume Forge kernel.

Clipped mass, pointer clauses, era bind, and merkle leaves.
No stored prose. No stamped mass. No coin.
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass, field
from typing import Iterable, Mapping, Sequence


MASS_CLIP = 1.1
STORED_PROSE = 0
N_CAP = 8
SEED_FAMILY = 8847291


class VolumeFault(ValueError):
    """Fail-closed fault. A volume that lies about mass or prose is refused."""


@dataclass(frozen=True)
class PointerClause:
    house: str
    organ: str
    verb: str
    ordinal: int

    def key(self) -> str:
        return f"{self.house}/{self.organ}/{self.verb}#{self.ordinal}"


@dataclass(frozen=True)
class EraBind:
    title: str
    era: str
    citation: str
    url: str

    def as_dict(self) -> dict[str, str]:
        return {
            "title": self.title,
            "era": self.era,
            "citation": self.citation,
            "url": self.url,
        }


@dataclass
class MassState:
    prior: float
    current: float
    iteration: int
    trajectory: list[float] = field(default_factory=list)

    def clip(self, proposed: float) -> float:
        if self.prior <= 0:
            raise VolumeFault("prior mass must be positive")
        ceiling = self.prior * MASS_CLIP
        if proposed > ceiling:
            proposed = ceiling
        if proposed < 0:
            raise VolumeFault("mass cannot be negative")
        self.current = proposed
        self.iteration += 1
        self.trajectory.append(proposed)
        self.prior = proposed
        return proposed


def pointer_hash(clause: PointerClause, seed: int = SEED_FAMILY) -> str:
    payload = f"{clause.key()}|{seed}|prose={STORED_PROSE}".encode()
    return hashlib.sha256(payload).hexdigest()


def era_bind(clause: PointerClause, seed: int = SEED_FAMILY) -> EraBind:
    digest = pointer_hash(clause, seed)
    era = f"HOUSE_ERA.{clause.house}.{clause.organ}"
    return EraBind(
        title=f"{clause.organ}:{clause.verb}",
        era=era,
        citation=f"era_bind:{digest[:16]}",
        url=f"pointer://{clause.house}/{clause.organ}/{clause.verb}",
    )


def merkle_leaf(clause: PointerClause, mass: float, seed: int = SEED_FAMILY) -> bytes:
    packed = struct.pack(">dQ", float(mass), seed & 0xFFFFFFFFFFFFFFFF)
    return hashlib.sha256(clause.key().encode() + packed).digest()


def merkle_root(leaves: Sequence[bytes]) -> str:
    if not leaves:
        raise VolumeFault("empty leaf set")
    layer = list(leaves)
    while len(layer) > 1:
        if len(layer) % 2 == 1:
            layer.append(layer[-1])
        nxt: list[bytes] = []
        for i in range(0, len(layer), 2):
            nxt.append(hashlib.sha256(layer[i] + layer[i + 1]).digest())
        layer = nxt
    return layer[0].hex()


def split_pointer(stimulus: str, cap: int = N_CAP) -> list[str]:
    raw = [tok for tok in stimulus.replace(",", " ").split() if tok]
    clauses = [tok for tok in raw if "://" in tok or "/" in tok or tok.startswith("GB-")]
    if len(clauses) > cap:
        clauses = clauses[:cap]
    return clauses


def clip_mass(proposed: float, prior: float) -> float:
    state = MassState(prior=prior, current=prior, iteration=0)
    return state.clip(proposed)


def observe(mass: float, prior: float) -> dict[str, float | int]:
    delta = mass - prior
    return {"G_delta": delta, "mass_hint": mass, "stored_prose": STORED_PROSE, "clip": MASS_CLIP}


def fold_masses(values: Iterable[float], prior: float = 1.0) -> MassState:
    state = MassState(prior=prior, current=prior, iteration=0, trajectory=[prior])
    for value in values:
        state.clip(value)
    return state


def assert_no_prose(blob: Mapping[str, object]) -> None:
    if int(blob.get("stored_prose", 0)) != 0:
        raise VolumeFault("stored_prose must be zero")
