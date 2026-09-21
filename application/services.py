from domain.interfaces import LanguageDetector, SentimentAnalyzer, SyllableCounter
from domain.types import Language
from infrastructure.language_detector import detectLanguage
from infrastructure.sentiment import analyzeSentiment
from infrastructure.syllable_counters import countSyllablesEn, countSyllablesRu, countSyllablesDe, countSyllablesFr

_SYLLABLE_COUNTERS: dict[Language, SyllableCounter] = {
  Language.EN: countSyllablesEn,
  Language.RU: countSyllablesRu,
  Language.DE: countSyllablesDe,
  Language.FR: countSyllablesFr,
}


def getSyllableCounter(lang: Language) -> SyllableCounter:
  # Возвращает функцию подсчёта слогов для языка.
  try:
    return _SYLLABLE_COUNTERS[lang]
  except KeyError as exc:
    raise NotImplementedError(f'Syllable counting for {lang.name} is not implemented') from exc


def getLanguageDetector() -> LanguageDetector:
  # Возвращает функцию определения языка.
  return detectLanguage


def getSentimentAnalyzer() -> SentimentAnalyzer:
  # Возвращает функцию анализа настроения.
  return analyzeSentiment
