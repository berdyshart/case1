from textblob import TextBlob
import deep_translator
import requests.exceptions

from domain.types import Language, Polarity
from infrastructure.language_detector import detectLanguage
import deep_translator.exceptions

# TextBlob умеет анализировать тональность только английского текста,
# поэтому для остальных языков текст сначала переводится на английский.
LANG_CODE_MAP = {
  Language.RU: "ru",
  Language.DE: "de",
  Language.FR: "fr",
}

_POLARITY_THRESHOLD = 0.05


def polarityFromScore(score: float) -> Polarity:
  """
  Function to map a numeric TextBlob polarity score to a Polarity label.
  :param score: polarity score in range [-1.0, 1.0].
  :return: Polarity label (POSITIVE / NEUTRAL / NEGATIVE).
  """
  if score > _POLARITY_THRESHOLD:
    return Polarity.POSITIVE
  if score < -_POLARITY_THRESHOLD:
    return Polarity.NEGATIVE
  return Polarity.NEUTRAL


def translateToEnglish(text: str, sourceCode: str) -> str:
  """
  Function to translate text into English so TextBlob can analyze it.
  :param text: original text.
  :param sourceCode: ISO 639-1 code of the source language (e.g. "ru").
  :return: text translated into English.
  """
  return deep_translator.GoogleTranslator(source=sourceCode, target="en").translate(text)


def analyzeSentiment(text: str) -> tuple[Polarity, float]:
  """
  Function to analyze the sentiment (polarity, subjectivity) of a text.

  Определяет язык текста через detectLanguage. Английский текст
  анализируется напрямую; текст на RU/DE/FR сначала переводится на
  английский, так как модель тональности TextBlob обучена только на
  английском. Если перевод не удался (например, нет сети или сервис
  перевода недоступен), в рамках учебного проекта анализ выполняется
  на исходном (непереведённом) тексте — это fallback, а не ошибка.

  :param text: text to analyze.
  :return: tuple of (Polarity, subjectivity), subjectivity in [0.0, 1.0].
  """
  lang, _ = detectLanguage(text)
  textToAnalyze = text

  sourceCode = LANG_CODE_MAP.get(lang)
  if sourceCode is not None:
    try:
      textToAnalyze = translateToEnglish(text, sourceCode)
    except (deep_translator.exceptions.RequestError, requests.exceptions.RequestException):
      textToAnalyze = text

  blob = TextBlob(textToAnalyze)
  polarity = polarityFromScore(blob.sentiment.polarity)
  subjectivity = blob.sentiment.subjectivity

  return polarity, subjectivity
