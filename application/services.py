"""
Композиция: получение конкретных реализаций по domain.interfaces.Protocol,
в зависимости от языка текста. Единая точка, где application/use_cases.py
узнаёт, какую функцию Роли 2 вызвать — вместо разбросанных if/elif по коду.
"""

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
    Возвращает функцию подсчёта слогов для языка.
    :raises NotImplementedError: для языка, для которого Роль 2 ещё не
    реализовала подсчёт слогов (сейчас — DE, FR).
    """
    try:
        return _SYLLABLE_COUNTERS[lang]
    except KeyError as exc:
        raise NotImplementedError(f"Подсчёт слогов для {lang.name} ещё не реализован") from exc


def get_language_detector() -> LanguageDetector:
    """Единственная реализация детектора языка — fasttext."""
    return detectLanguage


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Пока не реализовано — infrastructure/sentiment.py пуст (Роль 2)."""
    raise NotImplementedError("Анализ тональности ещё не реализован (Роль 2)")
