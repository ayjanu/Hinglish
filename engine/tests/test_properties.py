"""Property tests (Development plan §5): normalization is idempotent, keys are stable."""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from hv.langs.hi import PACK

devanagari = st.text(
    alphabet=st.characters(min_codepoint=0x0900, max_codepoint=0x097F), max_size=20
)
latin = st.text(alphabet=st.sampled_from("abcdefghijklmnopqrstuvwxyz '’āīūṭḍ"), max_size=20)
latin_word = st.text(
    alphabet=st.sampled_from("abcdefghijklmnopqrstuvwxyz"), min_size=1, max_size=12
)


@given(devanagari)
def test_normalize_native_idempotent(s: str) -> None:
    once = PACK.normalize_native(s)
    assert PACK.normalize_native(once) == once


@given(devanagari)
def test_match_key_native_idempotent(s: str) -> None:
    once = PACK.match_key_native(s)
    assert PACK.match_key_native(once) == once


@given(latin)
def test_normalize_latin_idempotent(s: str) -> None:
    once = PACK.normalize_latin(s)
    assert PACK.normalize_latin(once) == once


@given(latin_word)
def test_key_stable_under_case_and_repeats(w: str) -> None:
    noisy = w.upper()[:1] + w[1:] + w[-1] * 3
    assert PACK.phonetic_key(PACK.normalize_latin(noisy)) == PACK.phonetic_key(
        PACK.normalize_latin(w + w[-1])
    )


@given(devanagari)
def test_converter_never_crashes(s: str) -> None:
    PACK.to_canonical(s)
    PACK.to_precise(s)
