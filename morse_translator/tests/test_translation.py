import pytest
from .. import get_translator
from ..translators import TranslationError


def test_translation_smoke():
    """Translating to morse and back to english should yield the same string
    in upper case"""
    english_to_morse = get_translator("english", "morse")
    morse_to_english = get_translator("morse", "english")
    morse = english_to_morse.translate("hello world")
    english = morse_to_english.translate(morse)
    assert english == "HELLO WORLD"


def test_translation_unknown_char():
    """Translating unknown character should raise an error"""
    english_to_morse = get_translator("english", "morse")
    with pytest.raises(TranslationError):
        english_to_morse.translate("ä")
