# Learning science

Every learning feature traces to a finding below; features without one are cut or run as experiments.

## 1. Evidence base

Six findings with strong replication drive the design; each row says what the finding is and the rule it imposes on the product.

| Principle | Evidence | Design rule |
| --- | --- | --- |
| **Retrieval practice** | Students who practiced recall kept 61% of a passage after a week versus 40% for those who reread ([summary of Roediger & Karpicke, 2006](https://yukaichou.com/gamification-analysis/retrieval-practice-testing-effect-roediger-karpicke-learning/)); the effect has a century of replications ([Roediger & Karpicke, 2018](https://moodle2.units.it/pluginfile.php/572734/mod_resource/content/1/testing.pdf)) | Every exercise asks the learner to produce or recognize an answer; there is no "read the list" mode. New words are tested within the same session they are introduced |
| **Corrective feedback** | Retrieval benefits hold even after failed attempts, provided the correct answer is then shown ([Testing effect notes](https://notes.andymatuschak.org/Testing_effect)) | Every miss immediately shows the correct Devanagari, canonical spelling and audio |
| **Spacing** | A meta-analysis of 839 assessments in 317 experiments found the best gap between sessions grows with how long you need to remember ([Cepeda et al., 2006](https://pubmed.ncbi.nlm.nih.gov/16719566/)) | Reviews are scheduled by a memory model, never in fixed daily blocks |
| **Model-based scheduling** | FSRS predicts recall better than SM-2 in the large majority of collections in the open benchmark ([Anki forum](https://forums.ankiweb.net/t/fsrs-vs-sm2-in-2-seperate-profiles/52171)); Duolingo's trainable half-life regression roughly halved error versus a Leitner system ([Duolingo](https://blog.duolingo.com/how-we-learn-how-you-learn)) | Use FSRS (py-fsrs server, ts-fsrs offline); log every review in a form its optimizer can train on |
| **Interleaving** | Mixing categories beat blocking for learning to tell them apart, even though learners believed blocking helped more ([Kornell & Bjork, 2008, via Birnbaum et al.](https://www.springermedizin.de/article/10.3758/s13421-012-0272-7)); benefits are larger when categories are similar ([meta-analysis](https://www.psychologie.uni-wuerzburg.de/fileadmin/06020400/2019/Brunmair_Richter_in_press__2019_META-ANALYSIS_OF_INTERLEAVED_LEARNING.pdf)) | Confusable pairs are mixed within a session: त/ट, क/ख, ki/ke/ka, achha/achhi/achhe |
| **Vocabulary coverage** | Most learners need to know about 98% of the words in a text to read it unassisted, and 95% for minimal comprehension ([Hu & Nation, 2000, via Nation 2006](https://www.wgtn.ac.nz/__data/assets/pdf_file/0018/1626120/2006-How-large-a-vocab.pdf)) | Teach words in frequency order; reading passages are served only when the learner knows at least 95% of their tokens |

### Pronunciation needs its own method

Adult English speakers struggle to hear the Hindi dental–retroflex contrast; computer training produced about 10% improvement with little transfer to new speakers ([Pruitt, 1993](https://auditory.org/asamtgs/asa93ott/4pSP/4pSP13.html)). Difficulty also varies by talker and listener ([OSF study](https://osf.io/ut6zn)), and overnight sleep helps consolidate the learning ([Earle et al., 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11740156/)).

Rules: use several voices for every minimal pair; give feedback on each trial; spread perception practice across days; set expectations that this contrast takes weeks, and never block progress on it.

### Setting expectations

The US Foreign Service Institute estimates about 1,100 classroom hours for an English speaker to reach professional proficiency in Hindi ([FSI rankings](https://atlasandboots.com/foreign-service-institute-language-difficulty)). The app's honest goal is everyday conversation (CEFR A1–A2) plus script literacy, and it says so.

## 2. Learner model

Knowing a word is several separate skills, so each lemma spawns up to five cards, each scheduled independently by FSRS and unlocked in order.

| Card type | Prompt → answer | Unlocked when |
| --- | --- | --- |
| Meaning recognition | HV-Roman + audio → English (type or pick) | Word introduced |
| Meaning production | English → type Hindi | Recognition reaches Review state |
| Listening | Audio only → type Hindi | Production reaches Review state |
| Script reading | Devanagari → type HV-Roman | Learner's script stage covers all the word's letters |
| Usage (cloze) | Sentence with a gap → inflected form | Word's grammar unit is completed |

**Sibling burying:** two cards of the same lemma are never shown on the same day, so one does not give away the other.

### Automatic grading → FSRS rating

FSRS expects four ratings. The grader derives them from what the resolver did and how long the learner took, so learners never rate themselves.

| Outcome | Rating |
| --- | --- |
| Wrong word, no answer, or "show answer" pressed | Again |
| Right word reached only through the phonetic key or an edit-distance match, or a hint was used | Hard |
| Right word via canonical or an accepted variant | Good |
| Canonical spelling and response time under the learner's own 25th-percentile time for that card type | Easy |

For production cards, a correct lemma in the wrong inflection (achha for achhi) is rated Hard with a targeted grammar note, not Again. This mapping is a hypothesis: check it in Phase 3 by confirming FSRS's predicted recall is well calibrated against observed recall on these ratings.

### Scheduler settings

- Desired retention: default 0.90, adjustable 0.80–0.95 in settings.
- Parameters: global defaults until a learner has enough reviews, then per-learner optimization with the py-fsrs Optimizer ([py-fsrs](https://github.com/open-spaced-repetition/py-fsrs)), rerun weekly.
- Learning steps for new cards: 1 minute and 10 minutes within the session (py-fsrs defaults), so new words are retrieved twice before the session ends.

### Daily session

1. Due reviews first, capped at 100 a day so a missed week does not become a wall.
2. New items: default 10 a day, mixed into the reviews rather than shown as a block.
3. A short interleaved perception set (minimal pairs) every second session.
4. Typical length 10–15 minutes; the session ends when due cards are cleared, not on a timer.

## 3. Curriculum

Two levels ship first: A1 (about 500 lemmas plus survival phrases) and A2 (to about 1,500 lemmas). Words enter in frequency order within themed units, and grammar is taught through the words already known.

**Word list construction.** Rank lemmas by frequency (wordfreq's Hindi list, which draws on several corpora, cross-checked against Dakshina's Hindi Wikipedia text) ([wordfreq](https://pypi.org/project/wordfreq)). Remove proper nouns and Sanskrit-register words rare in speech, add high-frequency spoken words that written corpora under-count (haan, achha, yaar, theek), and have a native speaker review the final list.

### A1 units

| # | Unit | Grammar target | Example sentence |
| --- | --- | --- | --- |
| 1 | Greetings and politeness | namaste, dhanyavaad, aap as default | aap kaise hain? |
| 2 | Me and you | Pronouns + hona: hoon, hai, ho, hain | main student hoon |
| 3 | Things around me | Noun gender; ye / vo | ye kitaab hai |
| 4 | Describing | Adjective agreement -aa / -i / -e | achhi chaay |
| 5 | Numbers, money, time | Numerals 1–100, kitna / kitne | ye kitne ka hai? |
| 6 | Where things are | Postpositions + oblique: mein, par, ke paas | kitaab mez par hai |
| 7 | Whose is it | ka / ki / ke | Ram ki gaadi |
| 8 | Daily routine | Habitual present -ta hai | main roz chaay peeta hoon |
| 9 | Right now | Progressive raha hai | vo kha rahi hai |
| 10 | Asking for things | Imperatives at three politeness levels | paani dijiye |
| 11 | Plans | Future -ga / -gi / -ge | main kal aaunga |
| 12 | Food and travel phrases | Review, set phrases | mujhe ye chahiye |

A2 adds the perfective and ne, compound verbs, wanting and needing (chahiye, chaahna), can and must (sakna, padna), comparatives, and subjunctive requests.

### Script bridge

Devanagari is taught alongside, never instead of, the Roman track. Letters are introduced in groups ordered by frequency in the learner's known words, so every new letter immediately unlocks real words to read.

| Stage | What the learner sees | Advance when |
| --- | --- | --- |
| 1. Roman | HV-Roman only | Learner opts in to script (prompted after unit 3) |
| 2. Roman over script | HV-Roman with Devanagari beneath | 90% accuracy on the last 50 script-reading cards in the letter group |
| 3. Script over Roman | Devanagari, Roman revealed on tap | Same 90% / 50-card gate, per letter group |
| 4. Script only | Devanagari; Roman only in feedback | Learner's choice once all groups pass stage 3 |

The 90% and 50-card thresholds are starting values to tune with Phase 3 data.

## 4. Measuring whether learners learn

Engagement is not learning, so the primary metrics are memory and skill measures computed from review logs and periodic checks, with engagement tracked only as a guardrail.

| Metric | Definition | Use |
| --- | --- | --- |
| Observed retention | Share of reviews rated Good or Easy, per card type, per week | Should sit near the desired retention (0.90); a large gap means the grading map is miscalibrated |
| Scheduler calibration | Log loss and binned RMSE of FSRS predicted recall vs outcome, the metrics used by the open benchmark ([srsbench](https://archive.linux.duke.edu/cran/web/packages/srsbench/readme/README.html)) | Validates the automatic grading map |
| Known words | Lemmas with predicted recall above 0.9 on both recognition and production | Headline progress number shown to learners |
| Delayed test | Items not reviewed for 30 days, tested once without feedback | The honest measure of durable learning |
| Script reading speed | Correct words per minute on a fixed graded passage, monthly | Tracks the script bridge |
| Perception accuracy | Minimal-pair identification on unseen voices | Tracks pronunciation training transfer |
| Day-7 and day-30 return | Share of new learners active on those days | Guardrail only |

### Experiments

- Randomize at the learner level, never per session, so one person is not in two arms.
- Write down the primary metric and minimum sample before starting; stop at the planned size.
- First experiments: desired retention 0.85 vs 0.90; interleaved vs blocked minimal pairs; new items 10 vs 15 a day.

### Ethics

No streak-loss guilt notifications, no paywalled "streak repair", and no hiding due-review counts to inflate session starts. Learners can export their full review history and delete their account and data.
