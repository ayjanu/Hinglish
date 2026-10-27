"""Command-line interface for the HinglishVinglish engine.

Phase 0 covers the deterministic core; translation commands arrive in Phase 2.

    hv romanize "मैं कल दिल्ली जा रहा हूँ"     # canonical HV-Roman
    hv precise "नमस्ते"                       # diacritic view
    hv key bohot bahut bhot                   # phonetic keys
    hv normalize "Bahuuuut achha!"            # Latin normalization
    hv                                        # interactive mode
"""

from __future__ import annotations

import argparse
import sys

from hv import __version__
from hv.langs.hi import PACK


def _romanize(text: str) -> str:
    return PACK.to_canonical(text)


def _keys(words: list[str]) -> list[str]:
    out = []
    for w in words:
        norm = PACK.normalize_latin(w)
        out.append(f"{w}\t{norm}\t{PACK.phonetic_key(norm)}")
    return out


def _interactive() -> int:
    print(f"HinglishVinglish engine {__version__} ({PACK.scheme_version})")
    print("Type Devanagari to see HV-Roman, or romanized Hindi to see its phonetic key.")
    print("Empty line or Ctrl-D quits.\n")
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            print()
            return 0
        if not line:
            return 0
        if any("ऀ" <= ch <= "ॿ" for ch in line):
            print(f"  canonical: {PACK.to_canonical(line)}")
            print(f"  precise:   {PACK.to_precise(line)}")
        else:
            for row in _keys(line.split()):
                word, norm, key = row.split("\t")
                print(f"  {word}: normalized {norm!r}, key {key!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hv", description=__doc__.split("\n")[0])
    parser.add_argument("--version", action="version", version=f"hv {__version__}")
    sub = parser.add_subparsers(dest="cmd")
    for name, help_ in [
        ("romanize", "Devanagari -> canonical HV-Roman"),
        ("precise", "Devanagari -> diacritic romanization"),
        ("normalize", "normalize romanized input"),
    ]:
        p = sub.add_parser(name, help=help_)
        p.add_argument("text", nargs="+")
    pk = sub.add_parser("key", help="phonetic key for romanized words")
    pk.add_argument("words", nargs="+")

    args = parser.parse_args(argv)
    if args.cmd is None:
        return _interactive()
    if args.cmd == "romanize":
        print(_romanize(" ".join(args.text)))
    elif args.cmd == "precise":
        print(PACK.to_precise(" ".join(args.text)))
    elif args.cmd == "normalize":
        print(PACK.normalize_latin(" ".join(args.text)))
    elif args.cmd == "key":
        print("\n".join(_keys(args.words)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
