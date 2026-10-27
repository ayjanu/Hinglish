"""Measure HV-Roman against how people actually romanize Hindi (Dakshina gold sets).

    python eval/report_hi.py                  # train split (safe for development)
    python eval/report_hi.py --split dev
    python eval/report_hi.py --split test     # frozen: report only, never tune on it

Metrics, per native word:
  attested     canonical HV-Roman is one of the spellings annotators produced
  most_common  canonical equals the annotators' most frequent spelling
  key_match    canonical's phonetic key equals the key of some attested spelling
               (i.e. the resolver would find the word from that real spelling)
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))

from hv.langs.hi import PACK  # noqa: E402

GOLD = ROOT / "eval" / "gold" / "hi"


def load_lexicon(split: str) -> dict[str, dict[str, int]]:
    lex: dict[str, dict[str, int]] = defaultdict(dict)
    for line in (GOLD / f"lexicon.{split}.tsv").read_text("utf-8").splitlines():
        native, roman, count = line.split("\t")
        lex[native][roman.lower()] = int(count)
    return lex


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--split", default="train", choices=["train", "dev", "test"])
    args = ap.parse_args()
    lex = load_lexicon(args.split)
    n = len(lex)
    attested = most_common = key_match = 0
    for native, spellings in lex.items():
        canon = PACK.to_canonical(native)
        attested += canon in spellings
        most_common += canon == max(spellings, key=spellings.__getitem__)
        keys = {PACK.phonetic_key(PACK.normalize_latin(s)) for s in spellings}
        key_match += PACK.phonetic_key(canon) in keys
    print(f"scheme: {PACK.scheme_version}   split: {args.split}   words: {n}")
    print(f"attested     {attested / n:6.1%}")
    print(f"most_common  {most_common / n:6.1%}")
    print(f"key_match    {key_match / n:6.1%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
