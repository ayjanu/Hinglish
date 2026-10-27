# Hinglish (HinglishVinglish)

Learn Hindi through a standardized romanization, HV-Roman, with Devanagari as the hidden
source of truth. The engine understands the many ways people type romanized Hindi
(bahut, bohot, bhot) and teaches one consistent spelling.

## Repository

| Path | What it is |
| --- | --- |
| `HinglishVinglish-plan/` | The analysis and implementation plan (spec, learning science, architecture, dev plan, licensing) |
| `engine/` | `hv`, the Python language engine |
| `data-build/` | Pinned data sources, license gate, gold-set builder |
| `eval/` | Evaluation scripts and baseline reports |
| `cli.py` | Command line, runs offline with no credentials |
| `hinglish-legacy-brainstorm/` | The original prototype, kept for reference only |

## Quick start

```bash
cd engine && pip install -e ".[dev]" && cd ..
python cli.py romanize "मैं कल दिल्ली जा रहा हूँ"   # main kal dilli ja raha hoon
python cli.py key bohot bahut bhot                 # all share the key "bot"
cd engine && pytest -q
```

## Status

**Phase 0 (foundations): in progress on branch `phase-0`.**

- [x] P0-01 monorepo scaffold, CI
- [x] P0-02 core types and LanguagePack protocol
- [x] P0-03 Devanagari normalizer and match key
- [x] P0-04 Latin normalizer and tokenizer
- [x] P0-05 HV-Roman character mapping and context rules
- [x] P0-06 rule-based schwa deletion, measured against Dakshina (see `eval/README.md`)
- [x] P0-07 `sources.yaml` with checksums and license gate
- [x] P0-08 frozen Dakshina gold sets (manifest committed)
- [x] P0-09 offline CLI replacing the Kaggle-based prototype

Phase 0's gate (100% canonical round-trip) needs the Phase 1 lexicon to exist, so it is
checked as part of P1-11.
