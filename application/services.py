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


def get_syllable_counter(lang: Language) -> SyllableCounter:
    """
    Returns the syllable-counting function for the language.
    """
    try:
        return _SYLLABLE_COUNTERS[lang]
    except KeyError as exc:
        raise NotImplementedError(f"Syllable counting for {lang.name} is not implemented") from exc


def get_language_detector() -> LanguageDetector:
    return detectLanguage


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """
    Returns the sentiment analysis function.
    """
    return analyzeSentiment
