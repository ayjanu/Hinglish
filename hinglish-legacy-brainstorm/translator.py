"""
Translator for HinglishVinglish
Handles bidirectional translation between English and Romanized Hindi
"""

from indic_transliteration import sanscript
from dataset_manager import DatasetManager


class Translator:
    def __init__(self):
        self.dataset_manager = DatasetManager()
        self.dataset_manager.load_dataset()

    def transliterate_to_roman(self, devanagari_text):
        """Convert Devanagari script to Romanized (ITRANS)"""
        try:
            return sanscript.transliterate(
                devanagari_text,
                sanscript.DEVANAGARI,
                sanscript.ITRANS
            )
        except Exception as e:
            print(f"Transliteration error: {e}")
            return None

    def transliterate_to_devanagari(self, roman_text):
        """Convert Romanized (ITRANS) to Devanagari script"""
        try:
            return sanscript.transliterate(
                roman_text,
                sanscript.ITRANS,
                sanscript.DEVANAGARI
            )
        except Exception as e:
            print(f"Transliteration error: {e}")
            return None

    def translate_english_to_hindi(self, english_text):
        """
        Translate English to Hindi
        Returns: (romanized_hindi, devanagari_hindi) tuple or (None, None)
        """
        # Lookup in dataset
        devanagari = self.dataset_manager.get_hindi_translation(english_text)

        if not devanagari:
            return None, None

        # Transliterate to Roman
        romanized = self.transliterate_to_roman(devanagari)

        return romanized, devanagari

    def translate_hindi_to_english(self, roman_hindi_text):
        """
        Translate Romanized Hindi to English
        Returns: (english_translation, devanagari_hindi) tuple or (None, None)
        """
        # Convert Roman to Devanagari
        devanagari = self.transliterate_to_devanagari(roman_hindi_text)

        if not devanagari:
            return None, None

        # Lookup in dataset
        english = self.dataset_manager.get_english_translation(devanagari)

        return english, devanagari


if __name__ == "__main__":
    # Test the translator
    translator = Translator()

    print("\n=== Testing English to Hindi ===")
    english = "hello"
    roman, devan = translator.translate_english_to_hindi(english)
    print(f"English: {english}")
    print(f"Romanized: {roman}")
    print(f"Devanagari: {devan}")

    print("\n=== Testing Transliteration ===")
    test_devan = "नमस्ते"
    roman = translator.transliterate_to_roman(test_devan)
    print(f"Devanagari: {test_devan}")
    print(f"Romanized: {roman}")
