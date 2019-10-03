ENGLISH_TO_MORSE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "/": "-..-.",
    "@": ".--.-.",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
}


class TranslationError(Exception):
    """Raised during a failure in translation"""
    pass


class TranslatorNotFoundError(Exception):
    """Raised when a translator from specified source to target is not found"""
    pass


class English:
    """English language config"""
    char_break = ""
    word_break = " "


class Morse:
    """Morse language config"""
    char_break = "."
    word_break = "/"
    dot_symbol = "*"
    dash_symbol = "-"


class Translator:
    """Translator base class.
    Used to translate strings from a language to another"""

    def translate(self, string):
        """Translates a string from the source language of this translator
        to its target language.

        Args:
            string: Input string

        Returns:
            The translated string

        Raises:
            TranslationError: The string couldn't be translated
        """
        words = [word for word in string.split(self._source_lang.word_break)
                 if word != ""]
        translated_words = [self._translate_word(word) for word in words]
        return self._target_lang.word_break.join(translated_words)

    def _translate_word(self, word):
        if self._source_lang.char_break != "":
            word_chars = [
                char for char in word.split(self._source_lang.char_break)
                if char != ""
            ]
        else:
            word_chars = word
        try:
            translated_chars = [self._char_mappings[char]
                                for char in word_chars]
        except KeyError as e:
            raise TranslationError('Could not translate from '
                                   f'{self._source_lang.__name__} to '
                                   f'{self._target_lang.__name__}: no mapping '
                                   f'for symbol {str(e)}') from None
        return self._target_lang.char_break.join(translated_chars)


class EnglishToMorse(Translator):
    """Translator from english to morse"""

    def __init__(self):
        self._source_lang = English
        self._target_lang = Morse
        self._char_mappings = {
            key: value.replace(".", Morse.dot_symbol)
                      .replace("-", Morse.dash_symbol)
            for key, value in ENGLISH_TO_MORSE.items()
        }

    def translate(self, string):
        """Translates the input string from english to morse.
        The translation is case-insensitive, newlines and multiple consecutive
        spces are treated as single space characters. See base class.
        """
        return super().translate(string.replace('\n', ' ').upper())


class MorseToEnglish(Translator):
    """Translator from morse to english"""

    def __init__(self):
        self._source_lang = Morse
        self._target_lang = English
        self._char_mappings = {
            value.replace(".", Morse.dot_symbol)
                 .replace("-", Morse.dash_symbol): key
            for key, value in ENGLISH_TO_MORSE.items()
        }

    def translate(self, string):
        """Translates the input string from morse to uppercase english.
        An error is raised if the morse string contains unknown characters
        or illegal sequences (double character or word breaks). See base
        class."""
        if string.find(Morse.char_break * 2) != -1:
            raise TranslationError("Double character breaks are not allowed "
                                   "in morse") from None
        if string.find(Morse.char_break * 2) != -1:
            raise TranslationError("Double word breaks are not allowed "
                                   "in morse") from None
        return super().translate(string)


def get_translator(source_lang, target_lang):
    """Initializes a translator from source to target language if
    such translator is available

    Args:
        source_lang: Source language as a string
        target_lang: Target lanugage as a string

    Returns:
        Translator object from source to target language

    Raises:
        TranslatorNotFoundError: Translator from source to target
            language is not available
    """
    translators = {
        "english": {
            "morse": EnglishToMorse,
        },
        "morse": {
            "english": MorseToEnglish,
        },
    }
    try:
        return translators[source_lang][target_lang]()
    except KeyError:
        raise TranslatorNotFoundError(f'No translation from {source_lang} to '
                                      f'{target_lang} available') from None
