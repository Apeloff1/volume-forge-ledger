"""House seal. Merkle over sampled organ roots. No coin."""

from __future__ import annotations

import hashlib
from typing import Sequence

from volume_forge.kernel import merkle_root


def root_of(rows: Sequence[dict[str, object]]) -> str:
    if not rows:
        raise ValueError("empty seal")
    leaves = []
    for row in rows:
        payload = f"{row['house']}/{row['organ']}|{row['root']}|{row['mass']}".encode()
        leaves.append(hashlib.sha256(payload).digest())
    return merkle_root(leaves)
