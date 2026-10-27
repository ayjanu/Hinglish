"""Fetch pinned data sources with checksum verification and a license gate (P0-07).

    python data-build/fetch.py dakshina-v1                 # dev profile (default)
    python data-build/fetch.py dakshina-v1 --profile commercial
    python data-build/fetch.py --list

Files are cached in $HV_DATA_CACHE (default: ~/.cache/hinglishvinglish). A cached file
whose checksum matches is reused; a mismatch is an error, never silently replaced.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
CACHE = Path(os.environ.get("HV_DATA_CACHE", Path.home() / ".cache" / "hinglishvinglish"))


class GateError(RuntimeError):
    """A source was refused by the checksum or license gate."""


def load_yaml(name: str) -> Any:
    return yaml.safe_load((HERE / name).read_text("utf-8"))


def sources() -> dict[str, dict[str, Any]]:
    return {s["id"]: s for s in load_yaml("sources.yaml")["sources"]}


def check_license(src: dict[str, Any], profile: str) -> None:
    tags = src.get("tags") or []
    if not src.get("license") or not tags:
        raise GateError(f"{src['id']}: no license or tags recorded; refusing to use it")
    accept = set(load_yaml("profiles.yaml")[profile]["accept"])
    refused = [t for t in tags if t not in accept]
    if refused:
        raise GateError(f"{src['id']}: tags {refused} are not allowed in the '{profile}' profile")


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def fetch(source_id: str, profile: str = "dev") -> Path:
    src = sources().get(source_id)
    if src is None:
        raise GateError(f"unknown source '{source_id}'")
    check_license(src, profile)
    if not src.get("url") or not src.get("sha256"):
        raise GateError(f"{source_id}: url and sha256 must be pinned before it can be fetched")

    CACHE.mkdir(parents=True, exist_ok=True)
    dest = CACHE / Path(src["url"]).name
    if not dest.exists():
        print(f"downloading {src['url']} -> {dest}", file=sys.stderr)
        tmp = dest.with_suffix(dest.suffix + ".part")
        urllib.request.urlretrieve(src["url"], tmp)
        tmp.rename(dest)
    actual = sha256_of(dest)
    if actual != src["sha256"]:
        raise GateError(f"{source_id}: checksum mismatch ({actual}); delete {dest} and retry")
    return dest


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source", nargs="?")
    ap.add_argument("--profile", default="dev", choices=list(load_yaml("profiles.yaml")))
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(argv)
    if args.list or not args.source:
        for sid, s in sources().items():
            print(f"{sid:16s} {s['license']:28s} {' '.join(s.get('tags') or [])}")
        return 0
    try:
        print(fetch(args.source, args.profile))
    except GateError as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
