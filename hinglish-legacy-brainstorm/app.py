"""
HinglishVinglish - Language Learning App
Interactive CLI for translating between English and Romanized Hindi
"""

from translator import Translator


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("  HinglishVinglish - English ↔ Romanized Hindi Translator")
    print("="*60)


def print_menu():
    """Print main menu"""
    print("\nMain Menu:")
    print("1. Translate English to Romanized Hindi")
    print("2. Translate Romanized Hindi to English")
    print("3. Quit")
    print("-" * 60)


def translate_english_to_hindi(translator):
    """Handle English to Hindi translation"""
    print("\n--- English to Romanized Hindi ---")
    english_text = input("Enter English text: ").strip()

    if not english_text:
        print("Error: Empty input")
        return

    romanized, devanagari = translator.translate_english_to_hindi(english_text)

    if romanized and devanagari:
        print(f"\n✓ Translation found:")
        print(f"  English:    {english_text}")
        print(f"  Romanized:  {romanized}")
        print(f"  Devanagari: {devanagari}")
    else:
        print(f"\n✗ No translation found for: '{english_text}'")
        print("  Tip: Try single words or common phrases")


def translate_hindi_to_english(translator):
    """Handle Romanized Hindi to English translation"""
    print("\n--- Romanized Hindi to English ---")
    print("(Use ITRANS: a, A/aa, i, I/ii, u, U/uu, etc.)")
    roman_text = input("Enter Romanized Hindi: ").strip()

    if not roman_text:
        print("Error: Empty input")
        return

    english, devanagari = translator.translate_hindi_to_english(roman_text)

    if english and devanagari:
        print(f"\n✓ Translation found:")
        print(f"  Romanized:  {roman_text}")
        print(f"  Devanagari: {devanagari}")
        print(f"  English:    {english}")
    else:
        print(f"\n✗ No translation found for: '{roman_text}'")
        print("  Tip: Make sure you're using ITRANS romanization")


def main():
    """Main application loop"""
    print_banner()

    print("\nInitializing translator...")
    try:
        translator = Translator()
        print("✓ Translator ready!")
    except Exception as e:
        print(f"\n✗ Error initializing translator: {e}")
        print("\nPlease ensure:")
        print("1. You have installed dependencies: pip install -r requirements.txt")
        print("2. You have Kaggle API credentials in ~/.kaggle/kaggle.json")
        return

    while True:
        print_menu()
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            translate_english_to_hindi(translator)
        elif choice == "2":
            translate_hindi_to_english(translator)
        elif choice == "3":
            print("\nThank you for using HinglishVinglish!")
            print("Happy learning! 🙏\n")
            break
        else:
            print("\n✗ Invalid choice. Please enter 1, 2, or 3.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
