# Evaluation

## Gold sets (P0-08)

Built from Dakshina v1.0 (CC BY-SA 4.0) by `data-build/build_gold_hi.py` into
`eval/gold/hi/` (not committed). `eval/gold/MANIFEST.hi.json` pins every file's SHA-256, so
the splits are frozen.

| File | Use |
| --- | --- |
| `lexicon.train.tsv` | 25,000 words with attested romanizations: development and rule tuning |
| `lexicon.dev.tsv` | 2,500 words: model and weight selection |
| `lexicon.test.tsv` | 2,500 words: **frozen**, report only, never tune on it |
| `sentences.{dev,test}.{native,roman}.txt` | 5,000 hand-romanized sentence pairs each |

## Baseline: HV-Roman 1.0.0 (Oct 26, 2026)

`python eval/report_hi.py --split {train,dev}`

| Metric | Train (25,000) | Dev (2,500) |
| --- | --- | --- |
| Canonical spelling is one annotators produced | 49.0% | 51.2% |
| Canonical equals the most common attested spelling | 34.1% | 36.4% |
| Phonetic key matches an attested spelling's key | 77.4% | 77.5% |

The key-match rate is the one the resolver depends on: it is how often a real spelling
lands in the same candidate bucket as the word's canonical form.

### Findings that shaped Phase 0

- **Schwa rule variants** (measured on train, key-match): treating a nasalized vowel as
  the left-hand vowel in Ohala's rule helped (+0.1 pt) and was adopted. Left-to-right
  scanning (−0.5), allowing a cluster before the schwa (−1.0), retaining final schwa after
  clusters (−1.8) and a `-ीय → -iya` rule (−0.1) all hurt and were rejected.
- **Vowel length is the main gap with real usage.** For words whose canonical spelling
  writes medial long vowels as aa / ee / oo, only about 20% of attested spellings do.
  A short-vowel canonical (raja, thik, dudh) would raise "most common" from 34% to 53%.
  This is an open product decision, recorded in the plan; v1.0 keeps the spec as written.
- Remaining misses are dominated by compounds (अंकगणित) and English loanwords
  (अंडर → under), which need the Phase 1 lexicon, overrides and schwa classifier.
