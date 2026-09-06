import pytest

from application.services import (
    get_language_detector,
    get_sentiment_analyzer,
    get_syllable_counter,
)
from domain.types import Language
from infrastructure.language_detector import detectLanguage
from infrastructure.syllable_counters import countSyllablesEn, countSyllablesRu


def test_get_syllable_counter_en_returns_correct_function():
    assert get_syllable_counter(Language.EN) is countSyllablesEn


def test_get_syllable_counter_ru_returns_correct_function():
    assert get_syllable_counter(Language.RU) is countSyllablesRu


@pytest.mark.parametrize("lang", [Language.DE, Language.FR])
def test_get_syllable_counter_raises_for_unimplemented_language(lang):
    with pytest.raises(NotImplementedError):
        get_syllable_counter(lang)


def test_get_language_detector_returns_detect_language():
    assert get_language_detector() is detectLanguage


def test_get_sentiment_analyzer_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        get_sentiment_analyzer()
