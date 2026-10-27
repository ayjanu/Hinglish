"""Normalization for Devanagari and romanized (Latin) Hindi input (Linguistics §4).

Storage form keeps every distinction a Hindi reader would make; the match key
drops the ones writers routinely ignore. Both functions are idempotent.
"""

from __future__ import annotations

import re
import unicodedata

from hv.core.types import Token, TokenLang

NUKTA = chr(0x093C)
ANUSVARA = chr(0x0902)
CHANDRABINDU = chr(0x0901)
ZWJ = chr(0x200D)
ZWNJ = chr(0x200C)

_DEVA_DIGITS = {chr(0x0966 + i): str(i) for i in range(10)}
_DEVA_DIGIT_TABLE = str.maketrans(_DEVA_DIGITS)


def normalize_native(s: str) -> str:
    """Devanagari storage form.

    NFC is applied first. Note that the precomposed nukta letters U+0958..U+095F
    (क़ ख़ ग़ ज़ ड़ ढ़ फ़ य़) are Unicode composition exclusions, so NFC always yields
    base consonant + U+093C NUKTA. Raw strings must never be compared without this.
    """
    s = unicodedata.normalize("NFC", s)
    s = s.replace(ZWJ, "").replace(ZWNJ, "")
    return s.translate(_DEVA_DIGIT_TABLE)


def match_key_native(s: str) -> str:
    """Devanagari match key: storage form minus nukta, chandrabindu merged into anusvara,
    and punctuation (danda included) removed."""
    s = normalize_native(s)
    s = s.replace(NUKTA, "").replace(CHANDRABINDU, ANUSVARA)
    # Drop punctuation and symbols (danda included) by Unicode category. A regex like
    # [^\w\s] must not be used here: it would also strip vowel signs, which are marks.
    s = "".join(" " if unicodedata.category(ch)[0] in "PS" else ch for ch in s)
    return re.sub(r"\s+", " ", s).strip()


_REPEAT3 = re.compile(r"([a-z])\1{2,}")
_INNER_APOSTROPHE = re.compile(r"(?<=[a-z])['’](?=[a-z])")


def normalize_latin(s: str) -> str:
    """Latin-normalized form of one or more romanized words.

    1. NFKD, then drop combining marks, so diacritic input (ā, ṭ) folds to ASCII.
    2. Lowercase.
    3. Collapse any letter repeated three or more times to two (bahuuuut -> bahuut).
    4. Delete apostrophes inside words (kya's -> kyas).
    Whitespace is collapsed; other punctuation is left for the tokenizer.
    """
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = _REPEAT3.sub(r"\1\1", s)
    s = _INNER_APOSTROPHE.sub("", s)
    return re.sub(r"\s+", " ", s).strip()


_TOKEN = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*|\d+(?:[.,]\d+)*|[^\w\s]", re.UNICODE)


def tokenize_latin(text: str) -> list[Token]:
    """Split romanized input into tokens, keeping offsets into the original string."""
    tokens: list[Token] = []
    for m in _TOKEN.finditer(text):
        raw = m.group(0)
        lang: TokenLang
        if raw[0].isdigit():
            lang = "num"
        elif not raw[0].isalnum():
            lang = "punct"
        else:
            lang = "unk"
        tokens.append(
            Token(text=raw, norm=normalize_latin(raw), start=m.start(), end=m.end(), lang=lang)
        )
    return tokens
