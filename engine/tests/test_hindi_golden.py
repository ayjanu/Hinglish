"""Golden tests generated from the spec tables (fixtures/golden_hi.json)."""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import pytest

from hv.langs.hi import PACK, SCHEME_VERSION
from hv.langs.hi.key import weighted_edit_distance

GOLDEN = json.loads((Path(__file__).parent / "fixtures" / "golden_hi.json").read_text("utf-8"))


def test_fixture_matches_scheme_version() -> None:
    assert GOLDEN["scheme_version"] == SCHEME_VERSION


@pytest.mark.parametrize(("native", "canonical"), sorted(GOLDEN["canonical"].items()))
def test_canonical_word(native: str, canonical: str) -> None:
    assert PACK.to_canonical(native) == canonical


@pytest.mark.parametrize(("native", "canonical"), sorted(GOLDEN["sentences"].items()))
def test_canonical_sentence(native: str, canonical: str) -> None:
    assert PACK.to_canonical(native) == canonical


@pytest.mark.parametrize(("spelling", "key"), sorted(GOLDEN["phonetic_key"].items()))
def test_phonetic_key(spelling: str, key: str) -> None:
    assert PACK.phonetic_key(spelling) == key


@pytest.mark.parametrize(("raw", "norm"), sorted(GOLDEN["normalize_latin"].items()))
def test_normalize_latin(raw: str, norm: str) -> None:
    assert PACK.normalize_latin(raw) == norm


@pytest.mark.parametrize(("raw", "key"), sorted(GOLDEN["match_key_native"].items()))
def test_match_key_native(raw: str, key: str) -> None:
    assert PACK.match_key_native(raw) == PACK.normalize_native(key)


def test_precomposed_nukta_equals_decomposed() -> None:
    precomposed = chr(0x095B)  # ज़ as one code point (a composition exclusion)
    decomposed = chr(0x091C) + chr(0x093C)
    assert PACK.normalize_native(precomposed) == PACK.normalize_native(decomposed) == decomposed
    assert PACK.to_canonical(precomposed + "रूर") == "zaroor"


def test_devanagari_digits_become_ascii() -> None:
    assert PACK.normalize_native("१२३") == "123"


def test_canonical_output_is_lowercase_ascii_for_words() -> None:
    for native in GOLDEN["canonical"]:
        out = PACK.to_canonical(native)
        assert out.isascii() and out == out.lower(), native


def test_precise_view_keeps_distinctions() -> None:
    # Dental and retroflex t are both "t" in canonical but distinct in precise.
    assert PACK.to_canonical("तोता") == PACK.to_canonical("टोटा") == "tota"
    assert PACK.to_precise("तोता") != PACK.to_precise("टोटा")
    assert unicodedata.normalize("NFC", PACK.to_precise("राम")) == "rāma"


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("raja", "raaja", 0.2),  # vowel length
        ("bahut", "baut", 0.3),  # dropped h
        ("wala", "vala", 0.1),
        ("pakka", "paka", 0.2),  # doubling
        ("jaroor", "zaroor", 0.3),
        ("kitab", "kitab", 0.0),
    ],
)
def test_weighted_edit_distance(a: str, b: str, expected: float) -> None:
    assert weighted_edit_distance(a, b) == pytest.approx(expected)
