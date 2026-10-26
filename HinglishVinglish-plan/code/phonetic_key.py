"""HV-Roman phonetic key (Linguistics & HV-Roman spec, section 5).

The key is a candidate generator, not a decision: it deliberately over-merges
romanized spellings so the right lexicon word is always among the candidates.
Input must already be Latin-normalized (spec section 4: NFKD + strip marks,
lowercase, collapse 3+ repeated letters, punctuation removed).

Run `python phonetic_key.py` to execute the examples from the spec as tests.
"""
import re

DIGRAPHS = [  # applied in this order, longest first
    ("chh", "c"), ("ch", "c"), ("sh", "s"), ("ph", "f"),
    ("kh", "k"), ("gh", "g"), ("jh", "j"), ("th", "t"),
    ("dh", "d"), ("bh", "b"), ("rh", "r"),
    ("ee", "i"), ("ii", "i"), ("oo", "u"), ("uu", "u"),
    ("au", "o"), ("ou", "o"), ("aw", "o"), ("ai", "e"), ("ae", "e"),
    ("aa", "a"), ("w", "v"), ("z", "j"), ("q", "k"), ("x", "ks"),
]


def phonetic_key(word: str) -> str:
    """word must already be Latin-normalized (spec section 4)."""
    s = word
    for a, b in DIGRAPHS:
        s = s.replace(a, b)
    s = s[0] + s[1:].replace("h", "")       # drop non-initial h (aspiration; bahut)
    s = re.sub(r"a[ou]|o[au]", "o", s)     # vowel pairs exposed by dropping h
    s = re.sub(r"a[ie]", "e", s)
    s = re.sub(r"(.)\1+", r"\1", s)         # collapse doubled letters
    s = re.sub(r"([aeiou])n$", r"\1", s)    # drop word-final nasal n
    return s


# Expected keys from the spec's table (spec section 5).
SPEC_EXAMPLES = {
    "bahut": "bot", "bohot": "bot", "bhot": "bot", "boht": "bot", "bahot": "bot",
    "achha": "aca", "accha": "aca", "acha": "aca", "achcha": "aca",
    "nahin": "ne", "nahi": "ne", "nai": "ne", "nhi": "ni",
    "kharaab": "karab", "kharab": "karab", "khrab": "krab",
    "zaroor": "jarur", "jaroor": "jarur", "zarur": "jarur", "jarur": "jarur",
    "theek": "tik", "thik": "tik", "tik": "tik",
    "hai": "he", "he": "he",
}


if __name__ == "__main__":
    failures = {w: (phonetic_key(w), k) for w, k in SPEC_EXAMPLES.items() if phonetic_key(w) != k}
    if failures:
        for w, (got, want) in failures.items():
            print(f"FAIL {w}: got {got!r}, want {want!r}")
        raise SystemExit(1)
    print(f"All {len(SPEC_EXAMPLES)} spec examples pass.")
