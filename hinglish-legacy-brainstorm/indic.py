from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

roman = "kitaab"
hindi = transliterate(roman, sanscript.ITRANS, sanscript.DEVANAGARI)
print(hindi)