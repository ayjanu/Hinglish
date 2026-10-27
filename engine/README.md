# hv: the HinglishVinglish language engine

Python package for the romanization side of HinglishVinglish. Everything language-specific
sits behind the `LanguagePack` protocol (`hv/core/pack.py`); Hindi is `hv/langs/hi`.

The normative spec is `HinglishVinglish-plan/markdown/02-linguistics-hv-roman-spec.md`.
If code and spec disagree, the spec wins until it is changed by review.

## What exists (Phase 0)

| Module | Spec | What it does |
| --- | --- | --- |
| `hv/langs/hi/normalize.py` | Linguistics §4 | Devanagari storage form and match key; Latin normalization; tokenizer with offsets |
| `hv/langs/hi/scheme.py` | Linguistics §2, §3 | Devanagari → canonical HV-Roman (schwa deletion, nasals, gemination, overrides) and the precise diacritic view |
| `hv/langs/hi/key.py` | Linguistics §5 | Phonetic key and weighted edit distance |
| `hv/cli.py` | | `hv romanize`, `hv precise`, `hv key`, `hv normalize`, interactive mode |

## Develop

```bash
cd engine
uv venv --python 3.12 && uv pip install -e ".[dev]"
uv run pytest -q        # unit, golden, property and contract tests
uv run ruff check hv tests && uv run mypy
```

Golden cases live in `tests/fixtures/golden_hi.json` and are meant to be shared with the
TypeScript offline port. Changing a canonical value there is a major HV-Roman version bump.

## Measure against real spellings

```bash
pip install pyyaml
python data-build/build_gold_hi.py      # downloads Dakshina once (~2 GB), checks SHA-256
python eval/report_hi.py --split dev
```
