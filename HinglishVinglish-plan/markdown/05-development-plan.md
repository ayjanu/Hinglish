# Development plan

Tickets are written so a new developer can pick one up cold: each names its inputs, its output, and the test that proves it is done.

## 1. Repository and conventions

One monorepo, three deployables (engine+API, app, data build), and the spec tabs exported into `docs/spec` so code review can link to them.

```text
hinglishvinglish/
├── engine/                 # Python package `hv`
│   ├── hv/core/            # Token, Candidate, Resolution, LanguagePack protocol
│   ├── hv/langs/hi/        # Hindi pack: normalize, scheme, schwa, key, paradigms
│   ├── hv/resolve/         # langid, candidates, rerank
│   ├── hv/translate/       # phrase memory, NMT adapter, gloss
│   ├── hv/learn/           # grader, scheduler wrapper, curriculum
│   └── tests/              # unit, golden, property, contract
├── api/                    # FastAPI app; imports hv
├── app/                    # Expo + TypeScript
│   └── src/offline/        # TS port of normalize, key, lookup; ts-fsrs
├── data-build/             # ingest + build scripts -> lexicon-<ver>.sqlite
│   ├── sources.yaml        # every source, URL, checksum, license tag
│   └── curated/            # hand-maintained overrides, phrases, paradigms (CSV)
├── eval/                   # gold sets, benchmark runners, reports
└── docs/spec/              # exported spec tabs; golden tests generated from tables
```

| Area | Convention |
| --- | --- |
| Python | uv for environments, ruff for lint and format, mypy strict, pytest + hypothesis |
| TypeScript | pnpm, ESLint, Vitest, strict mode |
| CI | GitHub Actions: lint, type-check, unit and golden tests on every PR; gold-set evaluation nightly and on any change under langs/ or data-build/ |
| Versioning | Engine and API: semver. HV-Roman scheme: major on any canonical change. Lexicon: calendar version (2026.11.0) plus the scheme version it was built with |
| Data | Large sources are never committed; `sources.yaml` pins URL and SHA-256, and the build refuses a checksum mismatch |
| Definition of done | Code, tests, updated spec tab if behavior changed, and the eval report shows no regression on any ambiguity class |
| Curated data edits | Pull requests to CSVs in `curated/`, reviewed by a Hindi-speaking reviewer |

## 2. Phase 0 and Phase 1 backlog

Phase 0 builds the deterministic core and the test harness; Phase 1 makes romanized input resolve reliably. No model downloads are needed until P1-07.

### Phase 0: Foundations

| ID | Task | Acceptance criteria | Depends on |
| --- | --- | --- | --- |
| P0-01 | Monorepo scaffold, CI, tooling (Development plan §1) | CI runs lint, types, tests on a PR; a failing test blocks merge | — |
| P0-02 | Core types and LanguagePack protocol (Architecture §3) | mypy strict passes; a stub pack satisfies the contract tests | P0-01 |
| P0-03 | Devanagari normalizer + match key (Linguistics §4) | Every row of the §4 table is a passing test; hypothesis test: idempotent on random Devanagari | P0-02 |
| P0-04 | Latin normalizer (Linguistics §4) | Same, for Latin; diacritic input folds to ASCII | P0-02 |
| P0-05 | Character mapping + context rules (Linguistics §2, §3 context rules) | Golden tests generated from the §2 and §3 tables all pass | P0-03 |
| P0-06 | Rule schwa deletion (Linguistics §3) | All §3 examples pass; accuracy measured and reported on Arora et al.'s Hindi data | P0-05 |
| P0-07 | sources.yaml + license tags + checksum fetcher | Build fails on checksum mismatch or a source with no license tag | P0-01 |
| P0-08 | Gold sets: Dakshina Hindi dev/test lexicon and 10k romanized sentences, split and frozen | Files in eval/ with a README stating provenance; test split never used for tuning | P0-07 |
| P0-09 | Remove Kaggle runtime download from the old app; CLI calls the new engine | `python cli.py` runs offline with no credentials | P0-05 |

### Phase 1: Romanization engine

| ID | Task | Acceptance criteria | Depends on |
| --- | --- | --- | --- |
| P1-01 | Lexicon schema + build script producing lexicon-\<ver>.sqlite | Schema matches Plan overview; build is reproducible (same inputs → identical file hash) | P0-07 |
| P1-02 | Ingest Dakshina romanization lexicon with attestation counts | Variant rows carry source=dakshina and counts; spot check of 100 rows by a Hindi speaker | P1-01 |
| P1-03 | Ingest Aksharantar Hindi pairs | source=aksharantar; duplicates merged with Dakshina, counts summed | P1-01 |
| P1-04 | Rule-generated variants (accepted-input column of Linguistics §2) | Every lemma has its canonical + rule variants; no variant maps to more than 50 lemmas without review | P1-01 |
| P1-05 | Paradigm generator for regular nouns, adjectives, verbs (Linguistics §6) | Generated forms for 200 test lemmas match a native speaker's list at ≥ 98% | P1-01 |
| P1-06 | Phonetic key + weighted edit distance (Linguistics §5) | §5 tables pass; keys indexed in SQLite | P1-01 |
| P1-07 | IndicXlit fallback adapter | Returns top-5 Devanagari for unseen words; cached | P0-02 |
| P1-08 | Token language ID (homograph-aware) | ≥ 95% token accuracy on a 500-sentence hand-labeled code-mixed set (to be built in this ticket) | P1-02 |
| P1-09 | Candidate scoring + weight tuning on Dakshina dev | Tuned weights committed; top-1 on Dakshina test beats IndicXlit alone | P1-02–P1-07 |
| P1-10 | Arora et al. schwa classifier behind a flag | Beats the rule on held-out words; enabled only if it does | P0-06 |
| P1-11 | Round-trip CI invariant | For every lexicon entry, resolving its canonical spelling returns that entry; 100% required | P1-09 |

Estimate (one engine developer): Phase 0 about 3 weeks, Phase 1 about 4–5 weeks.

## 3. Phase 2 and Phase 3 backlog

Phase 2 adds translation and the API; Phase 3 is the first learner-facing release, so the app work starts here in parallel.

### Phase 2: Translation and API

| ID | Task | Acceptance criteria | Depends on |
| --- | --- | --- | --- |
| P2-01 | KenLM 5-gram on normalized Hindi Wikipedia (Dakshina native text) | Model built reproducibly; reranking improves sentence-level word accuracy on the Dakshina romanized sentences | P1-09 |
| P2-02 | Phrase memory: 600 curated A1–A2 phrases written in-house, native-speaker reviewed | CSV in curated/ with English, Devanagari, canonical, register, unit; owned content, no third-party license | P1-01 |
| P2-03 | IndicTrans2 adapter, both directions (dist-200M) | Batching, sentence splitting, IndicProcessor pre/post-processing; deterministic decoding (beam 4) | P0-02 |
| P2-04 | Translator: phrase memory first, NMT otherwise; gloss alignment | Exact phrase hits never call NMT; every Hindi token gets a lemma gloss | P2-02, P2-03 |
| P2-05 | Speaker-gender and politeness handling for English → Hindi | Test set of 100 first-person sentences: 100% use the requested gender; politeness tags respected | P2-04 |
| P2-06 | FastAPI service with the §4 Architecture endpoints (resolve, translate, romanize, lexicon) | OpenAPI generated; contract tests; problem+json errors; version fields in every response | P2-04 |
| P2-07 | MT evaluation harness | chrF++ on IN22-Conv with Devanagari input vs our romanized-then-resolved input, reported per release | P2-04 |
| P2-08 | Latency and memory measurement; ONNX or CTranslate2 conversion if budgets fail | Architecture §5 table updated with measured numbers | P2-06 |

### Phase 3: Learning MVP

| ID | Task | Acceptance criteria | Depends on |
| --- | --- | --- | --- |
| P3-01 | Postgres schema (users, cards, review\_log, decks) + Supabase auth | Migrations versioned; row-level security on per-user tables | P2-06 |
| P3-02 | Grader with the outcome → rating map (Learning science §2) | Table-driven tests for every row of the rating map, including wrong-inflection → Hard | P1-11 |
| P3-03 | Scheduler service on py-fsrs; session builder (due first, cap 100, 10 new, interleaved) | Simulated 60-day learner produces sensible due counts; sibling burying enforced | P3-01 |
| P3-04 | A1 curriculum content: 12 units, word lists, sentences, cloze items | Native-speaker reviewed; every item resolves through the engine without warnings | P2-02 |
| P3-05 | TTS batch: Indic Parler-TTS audio for all A1 items in two voices | Opus files on storage; 5% random sample checked by a native speaker for schwa and nasal errors | P3-04 |
| P3-06 | Expo app: onboarding (gender, politeness, goal), study session, five card types, feedback screens | Works on iOS, Android and web builds; screen-reader labels on all controls | P3-03 |
| P3-07 | Translator screen with gloss and save-to-deck | Saved sentence becomes cards in the learner's deck | P2-06, P3-06 |
| P3-08 | Offline study: TS port of normalize/key/lookup + ts-fsrs + sync | Port passes the same golden tests as Python (shared JSON fixtures); offline reviews sync idempotently | P3-02, P3-06 |
| P3-09 | Pilot: 20–50 learners for two weeks | Calibration and retention metrics (Learning science §4) reported; top 20 grading complaints triaged | P3-01–P3-08 |

Estimate (one engine developer, one app developer): Phase 2 about 4 weeks, Phase 3 about 6 weeks including the pilot.

## 4. Phase 4 backlog and launch checklist

Phase 4 turns the pilot into a public app: the A2 level, script bridge, pronunciation training, and the operational work a public launch needs.

| ID | Task | Acceptance criteria | Depends on |
| --- | --- | --- | --- |
| P4-01 | A2 curriculum (to about 1,500 lemmas): perfective + ne, compound verbs, modals | Native-speaker reviewed; same engine checks as P3-04 | P3-09 |
| P4-02 | Script bridge, four stages with per-letter-group gates (Learning science §3) | Gate thresholds configurable; stage changes logged | P3-06 |
| P4-03 | Minimal-pair perception trainer (त/ट, द/ड, aspirated pairs, nasal vowels) | At least four voices per pair; feedback each trial; unseen-voice test set held out | P3-05 |
| P4-04 | Native recordings for the core 500 words, replacing TTS | Recording guide, consent forms, loudness-normalized files | P3-05 |
| P4-05 | Per-learner FSRS optimization job (weekly) | Runs only above a minimum review count; log loss not worse than global parameters, else keep global | P3-03 |
| P4-06 | Progress dashboard: known words, retention, script stage, delayed-test results | Numbers match server-side metric definitions exactly | P3-09 |
| P4-07 | Graded reading passages served at ≥ 95% known-token coverage | Coverage computed from the learner's known-word set at request time | P4-01 |
| P4-08 | Experiment framework (learner-level randomization, pre-registered metric) | First experiment from Learning science §4 running | P4-06 |
| P4-09 | Account export and deletion, privacy notice, age gate | End-to-end tested; deletion removes rows and audio uploads | P3-01 |

### Launch checklist

- [ ] Data & licensing tab: every source in the release build is tagged commercial-OK, or the build is explicitly non-commercial
- [ ] Round-trip invariant at 100% for the shipped lexicon
- [ ] No regression on any ambiguity-class test set versus the pilot build
- [ ] Measured latency meets the Architecture §5 budgets, or the budgets were revised with sign-off
- [ ] Native-speaker review of all A1–A2 content and a 5% audio sample
- [ ] Crash-free sessions above 99.5% in the final beta week
- [ ] Privacy notice, export, deletion and age gate live
- [ ] Store listings, accessibility review (screen reader, dynamic type) done

Estimate: Phase 4 about 8 weeks with the two-developer team plus a part-time Hindi content reviewer, so roughly 25–27 weeks from Phase 0 to public launch.

## 5. Testing strategy

Seven layers, from milliseconds to weeks; the first four run on every pull request and the gold-set layer gates merges that touch language code or data.

| Layer | What it checks | Data | Runs |
| --- | --- | --- | --- |
| Unit | Each function's documented behavior | Inline cases | Every PR |
| Golden | Spec tables in the Linguistics tab | JSON fixtures generated from docs/spec, shared by Python and the TypeScript port | Every PR |
| Property | Normalization idempotent; canonical round-trip; key stable under case and repeat-letter noise | hypothesis-generated strings and lexicon entries | Every PR |
| Contract | Every LanguagePack satisfies the protocol; API matches OpenAPI | Stub and real packs | Every PR |
| Gold set | Top-1 word accuracy, sentence word accuracy, per ambiguity class | Dakshina Hindi test split, hand-labeled code-mixed set, ambiguity-class sets | Nightly + PRs touching langs/ or data-build/ |
| MT quality | chrF++ (sacrebleu) on IN22-Conv: Devanagari input vs romanized input | IN22-Conv | Per release |
| Human | Adequacy and fluency of translations and respellings | 200 sampled sentences per release | Per release |

### Human evaluation protocol

1. Sample 200 sentences: 100 from real (consented) learner inputs, 100 from IN22-Conv romanized by a native speaker.
2. Two bilingual raters score each output 1–5 for adequacy and fluency, blind to system version.
3. Report mean scores and inter-rater agreement; disagreements of two or more points go to a third rater.
4. Any release whose adequacy drops by 0.2 or more versus the previous release is blocked pending review.

### Gold-set hygiene

The Dakshina test split and the code-mixed set are frozen at P0-08 and never used for tuning or curated-list decisions. When a mistake from the test set is fixed by a curated override, the item moves to a separate "seen" file and is no longer counted as test.
