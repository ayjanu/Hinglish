# Linguistics and HV-Roman specification

This tab is the normative spec: if code and this tab disagree, the tab wins until it is changed by review.

## 1. The Hindi sound system, for implementers

Hindi distinguishes four things English does not, and HV-Roman's lowercase ASCII deliberately flattens two of them. The Devanagari pivot keeps them; the learning app must teach them explicitly.

### Consonants

Stops and affricates form a 5 × 5 grid: five places of articulation, each with four manners plus a nasal. Rows are place, columns are manner.

| Place | Voiceless | Voiceless aspirated | Voiced | Voiced aspirated (breathy) | Nasal |
| --- | --- | --- | --- | --- | --- |
| Velar | क k | ख kh | ग g | घ gh | ङ n |
| Palatal | च ch | छ chh | ज j | झ jh | ञ n |
| Retroflex | ट t | ठ th | ड d | ढ dh | ण n |
| Dental | त t | थ th | द d | ध dh | न n |
| Labial | प p | फ ph | ब b | भ bh | म m |

Other consonants: य y, र r, ल l, व v, श sh, ष sh, स s, ह h. Flaps ड़ (r) and ढ़ (rh). Perso-Arabic and English loan sounds are written with a nukta dot: क़ q, ख़ kh, ग़ gh, ज़ z, फ़ f.

### Vowels

| Independent | Sign (matra) | Sound | HV-Roman |
| --- | --- | --- | --- |
| अ | (none, inherent) | short ə, the "u" in "but" | a |
| आ | ा | long a, "father" | aa (a word-finally) |
| इ | ि | short i, "sit" | i |
| ई | ी | long i, "see" | ee (i word-finally) |
| उ | ु | short u, "put" | u |
| ऊ | ू | long u, "boot" | oo (u word-finally) |
| ऋ | ृ | ri (Sanskrit loans) | ri |
| ए | े | long e, "they" without glide | e |
| ऐ | ै | open e, "bat" in standard Hindi | ai |
| ओ | ो | long o, "go" without glide | o |
| औ | ौ | open o, "caught" | au |
| ऑ | ॉ | English loan "o" in "doctor" | o |

Any vowel can be nasalized, written with ँ (chandrabindu) or ं (anusvara).

### The four contrasts English speakers miss

1. **Dental vs retroflex** (त/ट, द/ड). The hardest: English speakers have great difficulty perceiving it even after training, with gains of roughly 10% and little transfer to new speakers ([Pruitt, 1993](https://auditory.org/asamtgs/asa93ott/4pSP/4pSP13.html); [Polka, 1991](https://labs.sonicfield.org/library/cross-language-speech-perception-in-adults-phonemic-phonetic-and-acoustic-contri)). HV-Roman writes both as t / d.
2. **Aspiration**, a four-way contrast (क ख ग घ). HV-Roman marks it with h, which is the letter romanizers most often drop.
3. **Vowel length** (इ/ई, उ/ऊ). HV-Roman marks it medially (ee, oo) but not word-finally.
4. **Nasalization** (है hai vs हैं hain). Marked with n, which casual typists often omit.

Rule for the product: every contrast HV-Roman flattens is still stored in Devanagari, shown in the precise view, and drilled with minimal pairs.

## 2. HV-Roman v1.0 mapping table

Three spellings exist for every word: **canonical** (HV-Roman, taught and displayed), **precise** (ISO 15919 diacritics, shown on tap) and **accepted variants** (understood on input, never displayed as correct). The table is the single source for the converter, its tests and the in-app guide.

### Vowels and vowel signs

| Devanagari | Canonical | Precise | Accepted on input |
| --- | --- | --- | --- |
| अ (inherent) | a, or nothing where schwa is deleted | a | u (as in "mujh"), omitted |
| आ ा | aa medially; a at word end | ā | a, aa, aah (final) |
| इ ि | i | i | e, ee |
| ई ी | ee medially; i at word end | ī | i, ii, ee, ie |
| उ ु | u | u | oo, o |
| ऊ ू | oo medially; u at word end | ū | u, uu, oo, ou |
| ऋ ृ | ri | r̥ | ru, r |
| ए े | e | ē | ae, ay, a (word-final "he" style) |
| ऐ ै | ai | ai | e, ae, ay |
| ओ ो | o | ō | oh, oo |
| औ ौ | au | au | o, ou, aw |
| ऑ ॉ | o | ô | aw, a (English spelling preferred via lexicon) |

### Consonants

| Devanagari | Canonical | Precise | Accepted on input |
| --- | --- | --- | --- |
| क ख ग घ | k kh g gh | k kh g gh | c, q (क); k (ख, unaspirated); g (घ) |
| ङ | n | ṅ | ng |
| च छ ज झ | ch chh j jh | c ch j jh | c (च); ch, c (छ); z (ज); j (झ) |
| ञ | n | ñ | ny |
| ट ठ ड ढ | t th d dh | ṭ ṭh ḍ ḍh | t, d (unaspirated forms); dd, tt |
| ण | n | ṇ | nn, rn |
| त थ द ध | t th d dh | t th d dh | t (थ), d (ध) |
| न | n | n | nn |
| प फ ब भ | p ph b bh | p ph b bh | f (फ); b (भ), v (ब) |
| म | m | m | mm |
| य | y | y | i, e (between vowels), j |
| र | r | r | rr |
| ल | l | l | ll |
| व | v | v | w, u (after consonant: "swaad") |
| श ष | sh | ś ṣ | s, sch |
| स | s | s | sh, ss, c |
| ह | h | h | omitted (very common), hh |
| क़ | q | q | k |
| ख़ | kh | ḵh | k, kh |
| ग़ | gh | ġ | g |
| ज़ | z | z | j |
| फ़ | f | f | ph, p |
| ड़ | r | ṛ | d, rr, dd |
| ढ़ | rh | ṛh | dh, r |

### Signs, conjuncts and symbols

| Devanagari | Canonical | Notes |
| --- | --- | --- |
| ं anusvara | n; m before p ph b bh m | Homorganic nasal before a consonant; vowel nasal elsewhere (हैं hain) |
| ँ chandrabindu | n | Same canonical as anusvara; precise view shows m̐ |
| ः visarga | h | Rare in Hindi (दुःख duhkh) |
| ् virama | (nothing) | Suppresses the inherent vowel |
| क्ष | ksh | Accept: x, ks, kch |
| त्र | tr | Accept: tra, thr |
| ज्ञ | gy | Hindi pronunciation; accept: gn, jn, gya |
| श्र | shr | Accept: sr |
| ऽ avagraha | (dropped) | Sanskrit only |
| । ॥ danda | . | Sentence end |
| ०–९ | 0–9 | Always ASCII digits |
| ZWJ, ZWNJ | (dropped) | Removed during normalization |

Versioning rule: any change to a canonical output is a **major** HV-Roman version bump, because it changes what learners were taught. Adding accepted variants is a **minor** bump.

## 3. Spelling rules: Devanagari → canonical HV-Roman

The converter runs as an ordered pipeline over one normalized word; the first matching stage wins. A word in the hand-curated override list skips the pipeline entirely.

1. **Override lookup.** Curated spellings for high-frequency irregulars and English loans (डॉक्टर → doctor, फ़ोन → phone, माँ → maa).
2. **Segment into aksharas** (consonant cluster + vowel sign or inherent vowel), marking each inherent schwa as a candidate.
3. **Mark morpheme boundaries** from the lexicon (stem + suffix, compound parts). Boundaries block schwa deletion across them ([Narasimhan, Sproat & Kiraz, 2004](https://forms.mpi.nl/node/48164)).
4. **Schwa deletion** (below).
5. **Map characters** with the table in section 2.
6. **Apply context rules:** anusvara place assimilation, word-final vowel shortening, gemination.
7. **Lowercase and strip** anything outside a–z.

### Schwa deletion

The hard part of Hindi grapheme-to-phoneme conversion is deciding whether a written inherent vowel is pronounced ([Arora et al., 2020](https://aclanthology.org/2020.acl-main.696)).

- **Word-final:** delete the inherent schwa of the last consonant. Keep it only for words on the retained-final list (tatsama words ending in a cluster such as मित्र mitra); this list is curated, not guessed.
- **Word-medial:** apply Ohala's rule ə → ∅ / VC\_CV, scanning right to left, which is reported correct about 89% of the time ([Wikipedia: Schwa deletion](https://en.wikipedia.org/wiki/Schwa_deletion_in_Indo-Aryan_languages)). Never delete in the first syllable; never across a marked morpheme boundary; never next to a virama cluster.
- **Classifier override:** in Phase 1, replace the medial rule with the gradient-boosted classifier from Arora et al. ([code and data](https://github.com/aryamanarora/schwa-deletion)), keeping the rule as fallback.

| Word | Akshara analysis | Result | Why |
| --- | --- | --- | --- |
| नमक | na·ma·ka | namak | final schwa deleted; medial ma keeps its vowel (not VC\_CV) |
| नमकीन | na·ma·kī·na | namkeen | medial "ma" sits in VC\_CV, deleted; final deleted |
| समझना | sa·ma·jha·nā | samajhna | morpheme boundary samajh + na keeps stem vowels as in समझ |
| धड़कन | dha·ṛa·ka·na | dhadkan | medial ṛa deleted, final deleted |
| नमस्ते | na·mas·te | namaste | schwa before a cluster is kept |
| धन्यवाद | dha·nya·vā·da | dhanyavaad | final deleted; medial long ā → aa |

### Context rules

- **Final long vowels** आ ई ऊ become a, i, u at word end (क्या kya, लड़की ladki, आलू aalu). Because final schwa is deleted, a word-final "a" always signals आ except on the retained-final list.
- **Final nasal vowels** keep their n and the vowel's medial form if the vowel is long and nasal (हूँ hoon, कहाँ kahaan, नहीं nahin).
- **Anusvara before a consonant** becomes m before p, ph, b, bh, m (संबंध sambandh) and n elsewhere (हिंदी hindi).
- **Gemination** is written doubled (पक्का pakka, बच्चा bachcha, दिल्ली dilli), with one exception decided on Oct 26: च्छ collapses to chh (अच्छा achha).
- **Aspirated + same-place aspirated** conjuncts keep both letters (बुद्ध buddh).

Every example in this section becomes a golden test case; the test file is generated from this tab's tables.

## 4. Normalization

Two strings that a Hindi reader would call the same word must produce the same storage form and the same match key. Storage form keeps every distinction; match key drops the ones writers routinely ignore.

### Devanagari

| Step | Storage form | Match key | Why |
| --- | --- | --- | --- |
| Unicode NFC | yes | yes | Precomposed nukta letters U+0958–U+095F (क़ ख़ ग़ ज़ ड़ ढ़ फ़ य़) are composition exclusions, so NFC always yields base + U+093C nukta; never compare raw strings ([Unicode list discussion](https://corp.unicode.org/pipermail/unicode/2025-April/011441.html); [codepoints.net U+0958](https://codepoints.net/U+0958)) |
| Visual normalization | yes | yes | Fixes sequences that render alike but differ in code points (Nisaba's visual normalizer) ([Nisaba](https://www.github.com/google-research/nisaba)) |
| Remove ZWJ / ZWNJ | yes | yes | Rendering hints only |
| Nukta | kept | removed | Many writers omit it (जरूर for ज़रूर) |
| Chandrabindu ँ vs anusvara ं | kept | merged to ं | Used interchangeably in practice |
| Danda, punctuation | kept as tokens | removed |  |
| Devanagari digits | converted to ASCII | converted |  |

### Latin input

1. Unicode NFKD, then drop combining marks, so diacritic input (ā, ṭ) folds to ASCII.
2. Lowercase.
3. Collapse any letter repeated three or more times to two (bahuuuut → bahuut), since emphasis lengthening is common.
4. Split on whitespace and punctuation; delete apostrophes inside words ("kya's" → "kyas").
5. Map digits to number tokens, translated as numbers, never transliterated.
6. Keep the original token and character offsets so the UI can highlight exactly what the learner typed.

Normalization is idempotent: normalizing twice must equal normalizing once. This is a property test.

## 5. Phonetic key and candidate scoring

The phonetic key is a candidate generator, not a decision: it deliberately over-merges spellings so the right word is always in the candidate list, and scoring picks among them.

### Key algorithm (applied to normalized Latin input)

```python
import re

DIGRAPHS = [  # applied in this order, longest first
    ("chh", "c"), ("ch", "c"), ("sh", "s"), ("ph", "f"),
    ("kh", "k"), ("gh", "g"), ("jh", "j"), ("th", "t"),
    ("dh", "d"), ("bh", "b"), ("rh", "r"),
    ("ee", "i"), ("ii", "i"), ("oo", "u"), ("uu", "u"),
    ("au", "o"), ("ou", "o"), ("aw", "o"), ("ai", "e"), ("ae", "e"),
    ("aa", "a"), ("w", "v"), ("z", "j"), ("q", "k"), ("x", "ks"),
]

def phonetic_key(word: str) -> str:
    """word must already be Latin-normalized (section 4)."""
    s = word
    for a, b in DIGRAPHS:
        s = s.replace(a, b)
    s = s[0] + s[1:].replace("h", "")       # drop non-initial h (aspiration; bahut)
    s = re.sub(r"a[ou]|o[au]", "o", s)     # vowel pairs exposed by dropping h
    s = re.sub(r"a[ie]", "e", s)
    s = re.sub(r"(.)\1+", r"\1", s)         # collapse doubled letters
    s = re.sub(r"([aeiou])n$", r"\1", s)    # drop word-final nasal n
    return s
```

| Input spellings | Key | Lexicon word |
| --- | --- | --- |
| bahut, bohot, bhot, boht, bahot | bot | बहुत |
| achha, accha, acha, achcha | aca | अच्छा |
| nahin, nahi, nai, nhi | ne (nhi gives ni, reached by the edit-distance fallback) | नहीं (also matches ने: resolved by scoring) |
| kharaab, kharab, khrab | karab, krab | ख़राब (edit distance links krab) |
| zaroor, jaroor, zarur, jarur | jarur | ज़रूर |
| theek, thik, tik | tik | ठीक |
| hai, he | he | है |

All rows above were checked by running the function on Oct 26, 2026; they become its unit tests.

When the key misses (krab vs karab), fall back to keys within edit distance 1, then to IndicXlit.

### Scoring each candidate lemma

```latex
\text{score}(w) = 2.0\,\log P(\text{spelling}\mid w) + 1.0\,\log f(w) - 1.5\,d(\text{input}, v^*_w) + 1.0\,\log P_{LM}(w \mid \text{context})
```

- P(spelling | w): share of attested spellings of w that equal the input (Dakshina and Aksharantar counts, add-one smoothed); 0.5 floor for rule-generated variants.
- f(w): word frequency (wordfreq Hindi list, normalized).
- d: weighted edit distance from the input to w's closest accepted variant v\*, with costs: vowel length (a/aa, i/ee) 0.2, h insertion or deletion 0.3, doubling 0.2, v/w 0.1, z/j 0.3, any other edit 1.0.
- P\_LM: the sentence-level language-model term, added only in the sentence reranker.

The weights 2.0 / 1.0 / 1.5 / 1.0 are starting values. Tune them by grid search on the Dakshina Hindi dev split, maximizing top-1 accuracy, and freeze them per lexicon version.

### Confidence

Report confidence as the softmax margin between the top two candidates. Below 0.6, the UI shows the alternatives ("did you mean कि ki or की ki?") instead of silently picking.

## 6. Grammar the engine and curriculum must model

Hindi inflects nouns, adjectives and verbs for gender, number and case, so the lexicon stores lemmas with paradigms, not just word forms. Every inflected form gets its own canonical spelling, generated from the stem so schwa deletion stays consistent.

| Feature | Example | Engine requirement | Curriculum requirement |
| --- | --- | --- | --- |
| SOV word order, postpositions | main khaana khaata hoon (I food eat) | Gloss aligns Hindi order to English; never reorder the learner's Hindi | Early unit on word order |
| Two genders, agreement on adjectives and verbs | achha ladka / achhi ladki / achhe ladke | Lexicon stores gender; grader accepts only the agreeing form | Interleaved agreement drills |
| Direct vs oblique case | ladka → ladke ko, ghar → ghar mein | Paradigm table per noun class (-aa masculine, consonant-final, -i feminine) | Postpositions taught with oblique forms together |
| Possessive ka / ki / ke | Ram ka ghar, Ram ki gaadi | Agrees with the possessed noun, not the owner; a classic learner error | Explicit feedback message for wrong agreement |
| Ergative ne in perfective transitive | maine khaana khaaya | Verb agrees with the object, not the subject | Introduced at A2, after habitual and progressive tenses |
| Honorific pronouns tu / tum / aap | tu ja, tum jao, aap jaiye | Verb form depends on pronoun level; translator tags register | Learner chooses a default politeness level; aap taught first |
| Speaker gender in first person | main jaata hoon (m) / main jaati hoon (f) | English → Hindi output must use the learner's chosen gender | Profile setting asked at onboarding |
| Compound and light verbs | kar dena, ho jaana, kaam karna | Multi-word lexicon entries | Taught as chunks |

**Known MT bias.** A developer fine-tuning IndicTrans2 for conversation reports that its English → Hindi output predominantly takes a male perspective ([indictrans2-conv](https://github.com/saurabhv749/indictrans2-conv)). For first-person sentences the app must regenerate or re-inflect output to the learner's gender, and test this explicitly.

**Paradigm generation.** Phase 1 ships hand-written paradigm rules for the three regular noun classes, regular adjectives (-aa / -i / -e), and regular verb tense forms (-ta, -ta hai, raha hai, -ega, -aa / -ya perfective). Irregular forms (gaya, kiya, diya, liya, hua) are listed explicitly in the lexicon.

## 7. Ambiguity classes and worked examples

Most resolution errors fall into a small number of known classes; each has a named strategy and its own test set, so regressions are visible per class.

| Class | Example | Resolution |
| --- | --- | --- |
| Hindi / English homographs | main (मैं / main), to (तो / to), hi (ही / hi), is (इस / is), me (में / me), log (लोग / log) | Token language ID uses neighbours: a homograph between two confident Hindi tokens is Hindi. Sentence-level LID (IndicLID's hin\_Latn vs eng\_Latn) breaks ties |
| Same key, different word | ki → कि / की; nahi → नहीं / ने | Language-model reranking; show alternatives below 0.6 confidence |
| Lossy canonical letters | tota → तोता; t could be त or ट | Lexicon lookup decides; rule converter is never used in the Roman → Devanagari direction |
| Word-final a | mitra (retained schwa) vs ladka (आ) | Retained-final list in the lexicon |
| Nukta omitted | jaroor for ज़रूर | Match key drops nukta; storage keeps it |
| Same word, two meanings | kal = yesterday or tomorrow | Not a resolver problem: MT uses tense (kal ja raha hoon → tomorrow); gloss shows both senses |
| English loans | phone, doctor, train | Lexicon loan entries map English spelling ↔ Devanagari (फ़ोन); display keeps the English spelling |
| Unknown words, names | priyanka, gurgaon | IndicXlit top-k, LM-reranked; marked low confidence |

### End-to-end examples

| Learner types | Resolved Devanagari | Canonical shown back | English |
| --- | --- | --- | --- |
| mujhe bohot bhook lagi hai | मुझे बहुत भूख लगी है | mujhe **bahut bhookh** lagi hai | I am very hungry |
| mera phone kharab h | मेरा फ़ोन ख़राब है | mera phone **kharaab hai** | My phone is broken |
| main kal dilli ja rha hu | मैं कल दिल्ली जा रहा हूँ | main kal dilli ja **raha hoon** | I am going to Delhi tomorrow |
| main to ghar pe hi hu | मैं तो घर पे ही हूँ | main to ghar pe hi **hoon** | I'm just at home |

Bold marks the words whose spelling differs from the learner's input; the app shows these as gentle respelling notes, never as errors.
