"""Kernel tests. Fail closed."""

from volume_forge.kernel import MASS_CLIP, PointerClause, clip_mass, era_bind, fold_masses, merkle_leaf, merkle_root, split_pointer


def test_clip_ceiling() -> None:
    assert clip_mass(5.0, 1.0) == MASS_CLIP


def test_clip_rejects_negative() -> None:
    try:
        clip_mass(-1.0, 1.0)
    except ValueError:
        return
    raise AssertionError("negative mass accepted")


def test_era_has_citation() -> None:
    era = era_bind(PointerClause("nexus", "mass", "bind", 0))
    assert era.citation.startswith("era_bind:")
    assert era.url.startswith("pointer://")


def test_fold_never_exceeds_clip() -> None:
    state = fold_masses([100.0] * 8, prior=1.0)
    assert state.current <= 1.1 ** 8 + 1e-9


def test_merkle_stable() -> None:
    clause = PointerClause("helix", "merkle", "leaf", 3)
    a = merkle_leaf(clause, 1.1)
    assert merkle_root([a, a]) == merkle_root([a, a])


def test_split_caps() -> None:
    stimulus = " ".join(f"pointer://h/{i}" for i in range(20))
    assert len(split_pointer(stimulus)) == 8


if __name__ == "__main__":
    test_clip_ceiling()
    test_clip_rejects_negative()
    test_era_has_citation()
    test_fold_never_exceeds_clip()
    test_merkle_stable()
    test_split_caps()
    print("kernel-ok")
