from typing import Protocol
from domain.types import Language, Polarity


class SyllableCounter(Protocol):
    """
    Counts the syllables in each word of the text.
    """

    def __call__(self, text: str) -> list[int]: ...


class LanguageDetector(Protocol):
    """
    Determines the language of the text and the model's confidence.
    """

    def __call__(self, text: str) -> tuple[Language, float]: ...


class SentimentAnalyzer(Protocol):
    """
    Determines the language of the text and the model's confidence.
    """

    def __call__(self, text: str) -> tuple[Polarity, float]: ...
