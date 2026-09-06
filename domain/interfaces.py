"""
Протоколы (typing.Protocol) для функций Роли 2 — фиксируют контракт,
на который опираются фабрики (application/services.py) и сценарии
(application/use_cases.py), не привязываясь к конкретной реализации.
"""

from typing import Protocol

from domain.types import Language, Polarity


class SyllableCounter(Protocol):
    """Считает слоги по каждому слову текста.

    Соответствует infrastructure.syllable_counters.countSyllablesEn /
    countSyllablesRu — принимает целый текст, а не одно слово.
    """

    def __call__(self, text: str) -> list[int]: ...


class LanguageDetector(Protocol):
    """Определяет язык текста и уверенность модели.

    Соответствует infrastructure.language_detector.detectLanguage.
    """

    def __call__(self, text: str) -> tuple[Language, float]: ...


class SentimentAnalyzer(Protocol):
    """Возвращает тональность и субъективность текста.

    Пока не реализовано (infrastructure/sentiment.py пуст) — протокол
    заложен заранее, чтобы Роль 3 могла писать use_cases уже сейчас.
    """

    def __call__(self, text: str) -> tuple[Polarity, float]: ...
