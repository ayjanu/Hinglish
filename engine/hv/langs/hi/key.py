"""Phonetic key and weighted edit distance for romanized Hindi (Linguistics §5).

The key is a candidate generator, not a decision: it deliberately over-merges
spellings so the right word is always in the candidate list; scoring picks among them.
"""

from __future__ import annotations

import re

DIGRAPHS: list[tuple[str, str]] = [  # applied in this order, longest first
    ("chh", "c"), ("ch", "c"), ("sh", "s"), ("ph", "f"),
    ("kh", "k"), ("gh", "g"), ("jh", "j"), ("th", "t"),
    ("dh", "d"), ("bh", "b"), ("rh", "r"),
    ("ee", "i"), ("ii", "i"), ("oo", "u"), ("uu", "u"),
    ("au", "o"), ("ou", "o"), ("aw", "o"), ("ai", "e"), ("ae", "e"),
    ("aa", "a"), ("w", "v"), ("z", "j"), ("q", "k"), ("x", "ks"),
]  # fmt: skip


def phonetic_key(word: str) -> str:
    """Key for one Latin-normalized word (see normalize_latin)."""
    if not word:
        return word
    s = word
    for a, b in DIGRAPHS:
        s = s.replace(a, b)
    s = s[0] + s[1:].replace("h", "")  # drop non-initial h (aspiration; bahut)
    s = re.sub(r"a[ou]|o[au]", "o", s)  # vowel pairs exposed by dropping h
    s = re.sub(r"a[ie]", "e", s)
    s = re.sub(r"(.)\1+", r"\1", s)  # collapse doubled letters
    s = re.sub(r"([aeiou])n$", r"\1", s)  # drop word-final nasal n
    return s


# Substitution / indel costs (Linguistics §5). Pairs are unordered; "" means insert/delete.
EDIT_COSTS: dict[tuple[str, str], float] = {
    ("a", "aa"): 0.2, ("i", "ee"): 0.2, ("i", "ii"): 0.2, ("u", "oo"): 0.2, ("u", "uu"): 0.2,
    ("h", ""): 0.3,
    ("v", "w"): 0.1,
    ("z", "j"): 0.3,
    ("f", "ph"): 0.2,
}  # fmt: skip
# Note: ai/au are deliberately not units. Reading "au" as one unit would make
# "baut" vs "bahut" a substitution instead of a cheap dropped h.
DOUBLING_COST = 0.2
DEFAULT_COST = 1.0

# Multi-letter units are matched first so "ee" vs "i" costs 0.2, not 1.0 + 1.0.
_UNITS = sorted(
    {u for pair in EDIT_COSTS for u in pair if u} | set("abcdefghijklmnopqrstuvwxyz"),
    key=len,
    reverse=True,
)
_UNIT_RE = re.compile("|".join(re.escape(u) for u in _UNITS))


def _units(s: str) -> list[str]:
    return _UNIT_RE.findall(s)


def _sub_cost(a: str, b: str) -> float:
    if a == b:
        return 0.0
    return EDIT_COSTS.get((a, b), EDIT_COSTS.get((b, a), DEFAULT_COST))


def _indel_cost(u: str, neighbour: str | None) -> float:
    if neighbour == u:
        return DOUBLING_COST  # pakka vs paka
    return EDIT_COSTS.get((u, ""), DEFAULT_COST)


def weighted_edit_distance(a: str, b: str) -> float:
    """Edit distance over romanization units with the costs above."""
    x, y = _units(a), _units(b)
    m, n = len(x), len(y)
    d = [[0.0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        d[i][0] = d[i - 1][0] + _indel_cost(x[i - 1], x[i - 2] if i > 1 else None)
    for j in range(1, n + 1):
        d[0][j] = d[0][j - 1] + _indel_cost(y[j - 1], y[j - 2] if j > 1 else None)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            d[i][j] = min(
                d[i - 1][j] + _indel_cost(x[i - 1], x[i - 2] if i > 1 else None),
                d[i][j - 1] + _indel_cost(y[j - 1], y[j - 2] if j > 1 else None),
                d[i - 1][j - 1] + _sub_cost(x[i - 1], y[j - 1]),
            )
    return d[m][n]
