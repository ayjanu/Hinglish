"""Extract the frozen Hindi gold sets from the Dakshina archive into eval/gold/hi (P0-08).

    python data-build/build_gold_hi.py            # fetches (or reuses) the archive, extracts
    python data-build/build_gold_hi.py --verify   # only check extracted files against the manifest

Extracted files are not committed (they live under eval/gold/, which is gitignored).
eval/gold/MANIFEST.hi.json is committed: it pins each file's SHA-256, so the splits are
frozen. If Dakshina ever changes, the build fails instead of silently moving the goalposts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tarfile
from pathlib import Path

from fetch import fetch

ROOT = Path(__file__).resolve().parent.parent
GOLD = ROOT / "eval" / "gold" / "hi"
MANIFEST = ROOT / "eval" / "gold" / "MANIFEST.hi.json"

MEMBERS = {
    # train is used for development and tuning; dev for model selection; test is frozen
    "lexicon.train.tsv": "dakshina_dataset_v1.0/hi/lexicons/hi.translit.sampled.train.tsv",
    "lexicon.dev.tsv": "dakshina_dataset_v1.0/hi/lexicons/hi.translit.sampled.dev.tsv",
    "lexicon.test.tsv": "dakshina_dataset_v1.0/hi/lexicons/hi.translit.sampled.test.tsv",
    "sentences.dev.native.txt": "dakshina_dataset_v1.0/hi/romanized/hi.romanized.rejoined.dev.native.txt",
    "sentences.dev.roman.txt": "dakshina_dataset_v1.0/hi/romanized/hi.romanized.rejoined.dev.roman.txt",
    "sentences.test.native.txt": "dakshina_dataset_v1.0/hi/romanized/hi.romanized.rejoined.test.native.txt",
    "sentences.test.roman.txt": "dakshina_dataset_v1.0/hi/romanized/hi.romanized.rejoined.test.roman.txt",
}  # fmt: skip


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract() -> None:
    archive = fetch("dakshina-v1")
    GOLD.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive) as tar:
        for local, member in MEMBERS.items():
            f = tar.extractfile(member)
            if f is None:
                raise RuntimeError(f"{member} missing from archive")
            (GOLD / local).write_bytes(f.read())
    (GOLD / "ATTRIBUTION.txt").write_text(
        "Derived from the Dakshina dataset v1.0 (Google Research), CC BY-SA 4.0.\n"
        "Roark et al., LREC 2020. https://github.com/google-research-datasets/dakshina\n",
        "utf-8",
    )


def verify() -> bool:
    manifest = json.loads(MANIFEST.read_text("utf-8"))
    ok = True
    for name, expected in manifest["files"].items():
        path = GOLD / name
        actual = sha256(path) if path.exists() else "missing"
        if actual != expected:
            print(f"MISMATCH {name}: {actual}", file=sys.stderr)
            ok = False
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--verify", action="store_true")
    ap.add_argument(
        "--write-manifest", action="store_true", help="only when first freezing the sets"
    )
    args = ap.parse_args()
    if not args.verify:
        extract()
    if args.write_manifest:
        files = {name: sha256(GOLD / name) for name in MEMBERS}
        MANIFEST.write_text(
            json.dumps({"source": "dakshina-v1", "files": files}, indent=2) + "\n", "utf-8"
        )
        print(f"wrote {MANIFEST}")
        return 0
    if verify():
        print(f"gold sets OK in {GOLD}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
