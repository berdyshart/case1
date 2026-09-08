from domain.interfaces import LanguageDetector, SentimentAnalyzer, SyllableCounter
from domain.types import Language
from infrastructure.language_detector import detectLanguage
from infrastructure.syllable_counters import countSyllablesEn, countSyllablesRu

_SYLLABLE_COUNTERS: dict[Language, SyllableCounter] = {
    Language.EN: countSyllablesEn,
    Language.RU: countSyllablesRu,
    # Language.DE, Language.FR — ждут реализации от Роли 2
}


def get_syllable_counter(lang: Language) -> SyllableCounter:
    """
    Returns the syllable-counting function for the language.
    """
    try:
        return _SYLLABLE_COUNTERS[lang]
    except KeyError as exc:
        raise NotImplementedError(f"Подсчёт слогов для {lang.name} ещё не реализован") from exc


def get_language_detector() -> LanguageDetector:
    return detectLanguage


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """
    Function for the not-yet-implemented sentiment analysis
    """
    raise NotImplementedError("Анализ тональности ещё не реализован")
