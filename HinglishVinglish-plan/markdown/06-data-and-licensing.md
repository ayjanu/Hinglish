# Data and licensing

Functionality comes first, but every source is tagged now so a commercial build can be produced later without an audit.

## 1. Provenance and licenses

Most of the stack is usable commercially; the two real constraints are Dakshina's share-alike clause and the IIT Bombay corpus, which must stay out of any commercial build. "Verify" means the license was not confirmed from a primary page during this research.

| Source | Used for | License (as found) | Commercial | Obligations / notes |
| --- | --- | --- | --- | --- |
| [Dakshina](https://github.com/google-research-datasets/dakshina) | Variant lexicon, gold sets, Hindi Wikipedia text for the LM | CC BY-SA 4.0 ([via FlipRate summary](https://pypi.org/project/fliprate/0.2.1/)) | Yes | Attribution; a distributed lexicon that includes Dakshina-derived rows must also be CC BY-SA. Keep those rows tagged so they can be split out |
| [Aksharantar](https://huggingface.co/datasets/ai4bharat/Aksharantar/blob/main/README.md) | Variant lexicon | Manually collected data CC-BY; mined data and existing sources CC0 | Yes | Attribution for the manual portion. One older dataset-card revision was tagged cc-by-nc-4.0; verify the current card before a commercial build |
| [IndicTrans2](https://huggingface.co/ai4bharat/indictrans2-en-indic-dist-200M) models | Translation | MIT | Yes | Hugging Face repo is gated: accept the conditions with the project account |
| [IndicXlit](https://github.com/AI4Bharat/IndicXlit) models | Transliteration fallback | Verify: an older PyPI release stated the models are CC BY-SA 4.0 ([PyPI 0.5.0.3](https://pypi.org/project/ai4bharat-transliteration/0.5.0.3/)) | Likely, with share-alike | Model outputs are probably not derivatives, but get legal review |
| [IndicLID](https://ai4bharat.iitm.ac.in/?p=1123) | Sentence language ID | MIT | Yes |  |
| [Indic Parler-TTS](https://huggingface.co/ai4bharat/indic-parler-tts) | Audio | Apache 2.0 ([summary](https://tts.ai/voices/indic-parler/)) | Yes | Gated repo; check gating terms |
| [Nisaba](https://www.github.com/google-research/nisaba) | Script normalization (upgrade) | Apache 2.0 | Yes |  |
| [py-fsrs](https://pypi.org/project/fsrs/0.1.3) | Scheduling | MIT | Yes | ts-fsrs license: verify |
| [wordfreq](https://pypi.org/project/wordfreq) | Frequency ranking | Verify code and data licenses | Likely |  |
| [indic\_transliteration](https://github.com/indic-transliteration/indic_transliteration_py) | Precise (diacritic) view, tests | Verify | Likely |  |
| [uroman](https://pypi.org/project/uroman) | Future non-Indic baselines | Verify | Unknown | Not used for Hindi |
| [IIT Bombay corpus](https://arxiv.org/abs/1710.02855v2) | Research and evaluation only | Non-commercial research | **No** | Never in a release build |
| IN22 benchmarks | Evaluation only | Released with IndicTrans2; verify | Eval use | Never shipped |
| [Kaggle English-Hindi](https://www.kaggle.com/datasets/preetviradiya/english-hindi-dataset) | Nothing (dropped) | Not stated on the page | **No** | Removed in P0-09 |
| In-house phrases, curriculum, recordings | Phrase memory, lessons, audio | Owned | Yes | Contributor agreements and speaker consent forms |

## 2. License gate and pre-commercial checks

The build script, not a person's memory, decides what goes into a release: each source in `sources.yaml` carries a license tag, and the build profile declares which tags it accepts.

```yaml
# data-build/sources.yaml (excerpt)
- id: dakshina-hi
  url: https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar
  sha256: <pinned>
  license: CC-BY-SA-4.0
  tags: [commercial-ok, share-alike, attribution]
- id: iitb-en-hi
  license: research-noncommercial
  tags: [noncommercial]

# data-build/profiles.yaml
dev:        { accept: [commercial-ok, noncommercial] }
commercial: { accept: [commercial-ok], require_attribution_file: true }
```

- Every lexicon row stores its `source`, so a build profile can exclude a source and the build reports exactly which rows and words were lost.
- The commercial profile writes an ATTRIBUTION file listing every CC-BY and CC-BY-SA source, bundled with the app.
- CI builds both profiles on every data change, so a commercial build is always one command away.

### Before the first commercial release

- [ ] Confirm the current Aksharantar dataset-card license on Hugging Face
- [ ] Confirm the IndicXlit model weight license and get legal advice on share-alike for model outputs
- [ ] Legal advice on whether serving lookups from a CC BY-SA-derived lexicon counts as distribution
- [ ] Read and record the gating terms of IndicTrans2 and Indic Parler-TTS repos
- [ ] Confirm wordfreq, ts-fsrs and indic\_transliteration licenses
- [ ] Contributor agreements for curriculum writers; consent forms for voice recordings
