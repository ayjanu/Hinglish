"""Core data types shared by every stage of the pipeline (Technical architecture §3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

TokenLang = Literal["hi", "en", "num", "punct", "unk"]
CandidateSource = Literal["canonical", "variant", "key", "edit", "xlit"]


@dataclass(frozen=True)
class Token:
    """One unit of learner input, with offsets back into the original string."""

    text: str  # exactly as typed
    norm: str  # Latin-normalized form (Linguistics §4)
    start: int  # offset of the first character in the original input
    end: int  # offset one past the last character
    lang: TokenLang = "unk"
    lang_conf: float = 0.0


@dataclass(frozen=True)
class Candidate:
    """A possible native-script reading of a token."""

    native: str  # storage-form native script (e.g. NFC Devanagari)
    canonical: str  # canonical romanization of this surface form
    source: CandidateSource
    score: float
    lemma_id: int | None = None


@dataclass
class Resolution:
    """Result of resolving romanized text to native script."""

    tokens: list[Token]
    best: list[Candidate | None]  # one per token; None = pass-through (English, punctuation)
    alternatives: list[list[Candidate]] = field(default_factory=list)
    confidence: list[float] = field(default_factory=list)
