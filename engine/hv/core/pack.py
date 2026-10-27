"""The LanguagePack protocol: everything language-specific lives behind this interface.

The resolver, translator and learning code must never mention a specific language.
Adding a language means writing a new pack (Technical architecture §3, §6).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable


@runtime_checkable
class LanguagePack(Protocol):
    code: str  # ISO 639-1, e.g. "hi"
    mt_code: str  # translation-model language tag, e.g. "hin_Deva"
    scheme_version: str  # e.g. "hv-roman 1.0.0"

    def normalize_native(self, s: str) -> str:
        """Storage form: keeps every distinction a reader would make."""
        ...

    def match_key_native(self, s: str) -> str:
        """Match key: drops distinctions writers routinely ignore (e.g. nukta)."""
        ...

    def normalize_latin(self, s: str) -> str:
        """Latin-normalized form of romanized input."""
        ...

    def phonetic_key(self, latin_word: str) -> str:
        """Over-merging key used to generate candidates for unseen spellings."""
        ...

    def to_canonical(self, native_text: str) -> str:
        """Native script -> canonical romanization (taught and displayed)."""
        ...

    def to_precise(self, native_text: str) -> str:
        """Native script -> diacritic romanization (shown on tap)."""
        ...

    def edit_costs(self) -> dict[tuple[str, str], float]:
        """Substitution costs for weighted edit distance between romanizations."""
        ...

    def tts_voices(self) -> Sequence[str]: ...
