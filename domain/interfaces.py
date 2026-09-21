from typing import Protocol

from domain.types import Language, Polarity


class SyllableCounter(Protocol):
  # Подсчитывает слоги в каждом слове текста.
  def __call__(self, text: str) -> list[int]: ...


class LanguageDetector(Protocol):
  # Определяет язык текста и уверенность модели.
  def __call__(self, text: str) -> tuple[Language, float]: ...


class SentimentAnalyzer(Protocol):
  # Анализирует настроение текста, возвращая полярность и оценку субъективности.
  def __call__(self, text: str) -> tuple[Polarity, float]: ...
