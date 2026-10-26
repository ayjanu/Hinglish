# HinglishVinglish

A language learning app that translates between English and Romanized Hindi (Latin alphabet) using the Kaggle English-Hindi dataset.

## Features

- **Bidirectional Translation**: Translate English ↔ Romanized Hindi
- **Devanagari Display**: See both Romanized and Devanagari script for learning
- **ITRANS Romanization**: Uses ASCII-only ITRANS scheme (easy for English speakers)
- **130K+ Translations**: Powered by comprehensive English-Hindi dataset

## Setup

### Prerequisites

1. **Python 3.7+**
2. **Kaggle Account**: Create a free account at [kaggle.com](https://www.kaggle.com)
3. **Kaggle API Credentials**:
   - Go to [kaggle.com/settings/account](https://www.kaggle.com/settings/account)
   - Scroll to "API" section
   - Click "Create New API Token"
   - This downloads `kaggle.json`
   - Move it to `~/.kaggle/kaggle.json`
   - Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

### Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   python app.py
   ```

   The app will automatically download the dataset on first run.

## Usage

### Main Menu Options

1. **Translate English to Romanized Hindi**
   - Input: English text (e.g., "hello")
   - Output: Romanized Hindi (ITRANS) + Devanagari script

2. **Translate Romanized Hindi to English**
   - Input: Romanized Hindi in ITRANS format (e.g., "namaste")
   - Output: English translation + Devanagari script

3. **Quit**

### ITRANS Romanization Guide

The app uses ITRANS scheme for romanization:

| Devanagari | ITRANS | Sound |
|------------|--------|-------|
| अ | a | as in "about" |
| आ | A, aa | as in "father" |
| इ | i | as in "sit" |
| ई | I, ii | as in "see" |
| उ | u | as in "put" |
| ऊ | U, uu | as in "boot" |
| क | ka | as in "cat" |
| ख | kha | aspirated "k" |
| न | na | as in "not" |
| म | ma | as in "mom" |

**Examples**:
- नमस्ते → namaste
- धन्यवाद → dhanyavaad
- शुभ → shubha

## Project Structure

```
HinglishVinglish/
├── app.py                 # Main CLI interface
├── translator.py          # Translation engine
├── dataset_manager.py     # Kaggle dataset handler
├── requirements.txt       # Dependencies
├── README.md             # This file
└── data/                 # Dataset (auto-downloaded)
```

## Limitations (MVP)

- Exact sentence matching only (no fuzzy matching)
- No partial word matching
- No grammar or context awareness
- Dataset-dependent translations

## Troubleshooting

### "No dataset files found"
- Ensure Kaggle API credentials are properly set up
- Check internet connection
- Verify you have access to the dataset: [kaggle.com/datasets/preetviradiya/english-hindi-dataset](https://www.kaggle.com/datasets/preetviradiya/english-hindi-dataset)

### "No translation found"
- Try single words or common phrases
- The translation depends on the dataset coverage
- Check spelling and try variations

### Import errors
- Run: `pip install -r requirements.txt`
- Ensure you're using Python 3.7+

## Dependencies

- `indic-transliteration>=2.3.0` - Devanagari ↔ Roman transliteration
- `kaggle>=1.6.0` - Kaggle dataset API
- `pandas>=2.0.0` - Data manipulation

## Future Enhancements

- Fuzzy matching for typos
- Word-level translation fallback
- Pronunciation guide with audio
- Vocabulary learning mode
- Progress tracking
- Spaced repetition for memorization

## License

MIT

## Contributing

Contributions welcome! Feel free to submit issues and pull requests.
