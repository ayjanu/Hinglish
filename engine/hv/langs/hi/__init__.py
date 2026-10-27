"""Hindi LanguagePack."""

from __future__ import annotations

from collections.abc import Sequence

from hv.langs.hi import key, normalize, scheme

SCHEME_VERSION = "hv-roman 1.0.0"


class HindiPack:
    code = "hi"
    mt_code = "hin_Deva"
    scheme_version = SCHEME_VERSION

    def normalize_native(self, s: str) -> str:
        return normalize.normalize_native(s)

    def match_key_native(self, s: str) -> str:
        return normalize.match_key_native(s)

    def normalize_latin(self, s: str) -> str:
        return normalize.normalize_latin(s)

    def phonetic_key(self, latin_word: str) -> str:
        return key.phonetic_key(latin_word)

    def to_canonical(self, native_text: str) -> str:
        return scheme.to_canonical(native_text)

    def to_precise(self, native_text: str) -> str:
        return scheme.to_precise(native_text)

    def edit_costs(self) -> dict[tuple[str, str], float]:
        return dict(key.EDIT_COSTS)

    def tts_voices(self) -> Sequence[str]:
        # Named Hindi speakers of Indic Parler-TTS (Technical architecture §1).
        return ("Rohit", "Divya")


PACK = HindiPack()

__all__ = ["PACK", "SCHEME_VERSION", "HindiPack"]
