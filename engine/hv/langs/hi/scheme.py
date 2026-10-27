"""HV-Roman: Devanagari -> canonical romanization (Linguistics §2, §3).

Pipeline for one word:
  1. override lookup (curated spellings win outright)
  2. segment into consonants, vowels (marking inherent schwas), nasals, visarga
  3. schwa deletion: word-final, then medial by Ohala's rule ə -> ∅ / VC_CV, right to left
  4. map characters and apply context rules (final long vowels, nasals, gemination)

The precise view (ISO 15919-style diacritics) is a straight transliteration with no
schwa deletion, used for the learner's "show exact spelling" view.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from hv.langs.hi.normalize import ANUSVARA, CHANDRABINDU, NUKTA, normalize_native

VIRAMA = chr(0x094D)
VISARGA = chr(0x0903)
AVAGRAHA = chr(0x093D)
DANDA = chr(0x0964)
DOUBLE_DANDA = chr(0x0965)

# consonant (base letter, optionally followed by nukta) -> (canonical, precise)
CONSONANTS: dict[str, tuple[str, str]] = {
    "क": ("k", "k"),
    "ख": ("kh", "kh"),
    "ग": ("g", "g"),
    "घ": ("gh", "gh"),
    "ङ": ("n", "ṅ"),
    "च": ("ch", "c"),
    "छ": ("chh", "ch"),
    "ज": ("j", "j"),
    "झ": ("jh", "jh"),
    "ञ": ("n", "ñ"),
    "ट": ("t", "ṭ"),
    "ठ": ("th", "ṭh"),
    "ड": ("d", "ḍ"),
    "ढ": ("dh", "ḍh"),
    "ण": ("n", "ṇ"),
    "त": ("t", "t"),
    "थ": ("th", "th"),
    "द": ("d", "d"),
    "ध": ("dh", "dh"),
    "न": ("n", "n"),
    "प": ("p", "p"),
    "फ": ("ph", "ph"),
    "ब": ("b", "b"),
    "भ": ("bh", "bh"),
    "म": ("m", "m"),
    "य": ("y", "y"),
    "र": ("r", "r"),
    "ल": ("l", "l"),
    "ळ": ("l", "ḷ"),
    "व": ("v", "v"),
    "श": ("sh", "ś"),
    "ष": ("sh", "ṣ"),
    "स": ("s", "s"),
    "ह": ("h", "h"),
    # nukta letters (stored decomposed: base + U+093C)
    "क" + NUKTA: ("q", "q"),
    "ख" + NUKTA: ("kh", "ḵh"),
    "ग" + NUKTA: ("gh", "ġ"),
    "ज" + NUKTA: ("z", "z"),
    "फ" + NUKTA: ("f", "f"),
    "य" + NUKTA: ("y", "ẏ"),
    # flaps: written d / dh in HV-Roman, following common usage (ladka, padhna)
    "ड" + NUKTA: ("d", "ṛ"),
    "ढ" + NUKTA: ("dh", "ṛh"),
}

# vowel key -> (independent letter, sign)
VowelKey = Literal["a", "aa", "i", "ii", "u", "uu", "ri", "e", "ai", "o", "au", "aw", "ae"]
INDEPENDENT_VOWELS: dict[str, VowelKey] = {
    "अ": "a",
    "आ": "aa",
    "इ": "i",
    "ई": "ii",
    "उ": "u",
    "ऊ": "uu",
    "ऋ": "ri",
    "ए": "e",
    "ऐ": "ai",
    "ओ": "o",
    "औ": "au",
    "ऑ": "aw",
    "ऍ": "ae",
}
VOWEL_SIGNS: dict[str, VowelKey] = {
    "ा": "aa",
    "ि": "i",
    "ी": "ii",
    "ु": "u",
    "ू": "uu",
    "ृ": "ri",
    "े": "e",
    "ै": "ai",
    "ो": "o",
    "ौ": "au",
    "ॉ": "aw",
    "ॅ": "ae",
}
# vowel key -> (canonical medial, canonical word-final, precise)
VOWELS: dict[VowelKey, tuple[str, str, str]] = {
    "a": ("a", "a", "a"),
    "aa": ("aa", "a", "ā"),
    "i": ("i", "i", "i"),
    "ii": ("ee", "i", "ī"),
    "u": ("u", "u", "u"),
    "uu": ("oo", "u", "ū"),
    "ri": ("ri", "ri", "r̥"),
    "e": ("e", "e", "ē"),
    "ai": ("ai", "ai", "ai"),
    "o": ("o", "o", "ō"),
    "au": ("au", "au", "au"),
    "aw": ("o", "o", "ô"),
    "ae": ("e", "e", "ê"),
}

# Words whose word-final inherent vowel is pronounced (tatsama words ending in a cluster).
# Curated, never guessed (Linguistics §3). Keys are storage-form Devanagari.
RETAINED_FINAL: frozenset[str] = frozenset(
    normalize_native(w)
    for w in ["मित्र", "चित्र", "पत्र", "मंत्र", "यंत्र", "तंत्र", "सूत्र", "शास्त्र", "राष्ट्र", "पुत्र"]
)

# Curated canonical spellings that override the rules (high-frequency irregulars, English loans).
OVERRIDES: dict[str, str] = {
    normalize_native(k): v
    for k, v in {
        "माँ": "maa",
        "मां": "maa",
        "डॉक्टर": "doctor",
        "फ़ोन": "phone",
        "फोन": "phone",
        "ट्रेन": "train",
        "बस": "bus",
        "स्कूल": "school",
    }.items()
}

SegKind = Literal["C", "V", "N", "H", "X"]


@dataclass
class Seg:
    kind: SegKind
    text: str  # source characters
    vowel: VowelKey | None = None  # for V
    inherent: bool = False  # for V: True = unwritten schwa
    deleted: bool = False  # for V: schwa deleted
    virama: bool = False  # for C: followed by an explicit virama


def segment(word: str) -> list[Seg]:
    """Split one normalized Devanagari word into segments."""
    segs: list[Seg] = []
    i, n = 0, len(word)
    while i < n:
        ch = word[i]
        if ch in CONSONANTS:
            cons = ch
            if i + 1 < n and word[i + 1] == NUKTA:
                cons += NUKTA
                i += 1
            if cons not in CONSONANTS:  # nukta on a letter we don't map: drop the nukta
                cons = ch
            segs.append(Seg("C", cons))
            nxt = word[i + 1] if i + 1 < n else ""
            if nxt == VIRAMA:
                segs[-1].virama = True
                i += 2
                continue
            if nxt in VOWEL_SIGNS:
                segs.append(Seg("V", nxt, vowel=VOWEL_SIGNS[nxt]))
                i += 2
                continue
            segs.append(Seg("V", "", vowel="a", inherent=True))
            i += 1
        elif ch in INDEPENDENT_VOWELS:
            segs.append(Seg("V", ch, vowel=INDEPENDENT_VOWELS[ch]))
            i += 1
        elif ch in (ANUSVARA, CHANDRABINDU):
            segs.append(Seg("N", ch))
            i += 1
        elif ch == VISARGA:
            segs.append(Seg("H", ch))
            i += 1
        elif ch == AVAGRAHA:
            i += 1
        else:
            segs.append(Seg("X", ch))
            i += 1
    return segs


def _is_live_vowel(segs: list[Seg], j: int) -> bool:
    return 0 <= j < len(segs) and segs[j].kind == "V" and not segs[j].deleted


def delete_schwas(segs: list[Seg], *, retain_final: bool = False) -> None:
    """Apply Hindi schwa deletion in place (Linguistics §3)."""
    vowel_idx = [k for k, s in enumerate(segs) if s.kind == "V"]
    if len(vowel_idx) <= 1:
        return  # monosyllables keep their vowel (न na)
    first_vowel = vowel_idx[0]

    # Word-final: delete the inherent schwa of the last consonant.
    last = segs[-1]
    if last.kind == "V" and last.inherent and not retain_final:
        last.deleted = True

    # Word-medial: ə -> ∅ / V C _ C V, scanning right to left. The strict pattern also
    # enforces "never next to a cluster": both neighbouring consonants must be single.
    for k in reversed(vowel_idx):
        s = segs[k]
        if not s.inherent or s.deleted or k == first_vowel:
            continue
        prev_c = k - 1 >= 0 and segs[k - 1].kind == "C"
        next_c = k + 1 < len(segs) and segs[k + 1].kind == "C"
        # A nasalized vowel (vowel + anusvara/chandrabindu) counts as the V on the left:
        # अंतराल -> antraal. Measured on Dakshina train (Oct 26, 2026): +0.1 pt agreement;
        # right-to-left order, cluster contexts and final-cluster retention all scored worse.
        left_v = _is_live_vowel(segs, k - 2) or (
            k - 2 >= 0 and segs[k - 2].kind == "N" and _is_live_vowel(segs, k - 3)
        )
        if prev_c and next_c and left_v and _is_live_vowel(segs, k + 2):
            s.deleted = True


_LABIALS = ("p", "b", "m")


def _render_canonical(segs: list[Seg]) -> str:
    out: list[str] = []
    n = len(segs)
    k = 0
    while k < n:
        s = segs[k]
        if s.kind == "C":
            canon = CONSONANTS[s.text][0]
            nxt = segs[k + 1] if k + 1 < n else None
            # च्छ collapses to chh (achha), decided Oct 26, 2026
            if s.virama and canon == "ch" and nxt is not None and nxt.text == "छ":
                k += 1
                continue
            # ज्ञ is pronounced gy in Hindi (gyaan)
            if s.virama and s.text == "ज" and nxt is not None and nxt.text == "ञ":
                out.append("gy")
                k += 2
                continue
            out.append(canon)
        elif s.kind == "V":
            if s.deleted:
                k += 1
                continue
            assert s.vowel is not None
            medial, final, _ = VOWELS[s.vowel]
            nasal_final = k + 2 == n and segs[k + 1].kind == "N"
            if k == n - 1:
                out.append(final)
            elif nasal_final:
                # word-final nasal vowel: ें -> ein (mein), ीं -> in (nahin), else medial + n
                if s.vowel == "e":
                    out.append("ein")
                elif s.vowel == "ii":
                    out.append("in")
                else:
                    out.append(medial + "n")
                k += 2
                continue
            else:
                out.append(medial)
        elif s.kind == "N":
            nxt = segs[k + 1] if k + 1 < n else None
            if nxt is not None and nxt.kind == "C":
                out.append("m" if CONSONANTS[nxt.text][0].startswith(_LABIALS) else "n")
            else:
                out.append("n")
        elif s.kind == "H":
            out.append("h")
        else:
            out.append(s.text)
        k += 1
    return "".join(out)


def word_to_canonical(word: str) -> str:
    """Canonical HV-Roman for one Devanagari word (no spaces or punctuation)."""
    w = normalize_native(word)
    if w in OVERRIDES:
        return OVERRIDES[w]
    segs = segment(w)
    delete_schwas(segs, retain_final=w in RETAINED_FINAL)
    return _render_canonical(segs)


def word_to_precise(word: str) -> str:
    """ISO 15919-style transliteration of one Devanagari word (inherent vowels kept)."""
    out: list[str] = []
    for s in segment(normalize_native(word)):
        if s.kind == "C":
            out.append(CONSONANTS[s.text][1])
        elif s.kind == "V":
            assert s.vowel is not None
            out.append(VOWELS[s.vowel][2])
        elif s.kind == "N":
            out.append("ṁ" if s.text == ANUSVARA else "m̐")
        elif s.kind == "H":
            out.append("ḥ")
        else:
            out.append(s.text)
    return "".join(out)


_DEVA_WORD = re.compile(r"[\u0900-\u0963\u0971-\u097f]+")


def _convert_text(text: str, word_fn: Callable[[str], str]) -> str:
    text = normalize_native(text).replace(DOUBLE_DANDA, ".").replace(DANDA, ".")
    return _DEVA_WORD.sub(lambda m: word_fn(m.group(0)), text)


def to_canonical(text: str) -> str:
    """Canonical HV-Roman for running Devanagari text; non-Devanagari passes through."""
    return _convert_text(text, word_to_canonical)


def to_precise(text: str) -> str:
    return _convert_text(text, word_to_precise)
