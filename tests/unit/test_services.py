import pytest

from application.services import (
  getLanguageDetector,
  getSentimentAnalyzer,
  getSyllableCounter,
)
from domain.types import Language
from infrastructure.language_detector import detectLanguage
from infrastructure.sentiment import analyzeSentiment
from infrastructure.syllable_counters import (
  countSyllablesDe,
  countSyllablesEn,
  countSyllablesFr,
  countSyllablesRu,
)


def test_GetSyllableCounterEnReturnsCorrectFunction():
  # Проверяет получение счётчика слогов для английского языка.
  assert getSyllableCounter(Language.EN) is countSyllablesEn


def test_GetSyllableCounterRuReturnsCorrectFunction():
  # Проверяет получение счётчика слогов для русского языка.
  assert getSyllableCounter(Language.RU) is countSyllablesRu


@pytest.mark.parametrize(
  'lang, expectedCounter',
  [
    (Language.DE, countSyllablesDe),
    (Language.FR, countSyllablesFr),
  ]
)
def test_GetSyllableCounterReturnsCorrectFunction(lang, expectedCounter):
  # Проверяет получение счётчиков слогов для немецкого и французского языков.
  assert getSyllableCounter(lang) is expectedCounter


def test_GetLanguageDetectorReturnsDetectLanguage():
  # Проверяет получение функции определения языка.
  assert getLanguageDetector() is detectLanguage


def test_GetSentimentAnalyzerReturnsAnalyzeSentiment():
  # Проверяет получение функции анализа тональности.
  assert getSentimentAnalyzer() is analyzeSentiment
