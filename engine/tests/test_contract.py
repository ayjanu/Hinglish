"""Contract tests every LanguagePack must pass (Technical architecture §3)."""

from __future__ import annotations

import pytest

from hv.core import LanguagePack
from hv.langs import hi

PACKS = [hi.PACK]


@pytest.mark.parametrize("pack", PACKS, ids=lambda p: p.code)
def test_satisfies_protocol(pack: LanguagePack) -> None:
    assert isinstance(pack, LanguagePack)
    assert pack.code and pack.mt_code and pack.scheme_version


@pytest.mark.parametrize("pack", PACKS, ids=lambda p: p.code)
def test_normalizers_idempotent_on_samples(pack: LanguagePack) -> None:
    for s in ["नमस्ते", "ज़रूर", "  Bahuuut  "]:
        assert pack.normalize_native(pack.normalize_native(s)) == pack.normalize_native(s)
        assert pack.normalize_latin(pack.normalize_latin(s)) == pack.normalize_latin(s)
