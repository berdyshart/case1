import deep_translator, deep_translator.exceptions
import requests.exceptions
import textblob
import domain.types
import infrastructure.language_detector

TextBlob = textblob.TextBlob
Language = domain.types.Language
Polarity = domain.types.Polarity
detectLanguage = infrastructure.language_detector.detectLanguage

LANG_CODE_MAP = {
  Language.RU: 'ru',
  Language.DE: 'de',
  Language.FR: 'fr',
}

POLARITY_THRESHOLD = 0.05

def polarityFromScore(score: float) -> Polarity:
  """
  Function to map a numeric TextBlob polarity score to a Polarity label.
  :param score: polarity score in range [-1.0, 1.0].
  :return: Polarity label (POSITIVE / NEUTRAL / NEGATIVE).
  """
  if score > POLARITY_THRESHOLD:
    return Polarity.POSITIVE
  if score < -POLARITY_THRESHOLD:
    return Polarity.NEGATIVE
  return Polarity.NEUTRAL

def translateToEnglish(text: str, sourceCode: str) -> str:
  """
  Function to translate text into English so TextBlob can analyze it.
  :param text: original text.
  :param sourceCode: ISO 639-1 code of the source language (e.g. "ru").
  :return: text translated into English.
  """
  return deep_translator.GoogleTranslator(source = sourceCode, target = 'en').translate(text)

def analyzeSentiment(text: str) -> tuple[Polarity, float]:
  """
  Function to analyze the sentiment (polarity, subjectivity) of a text.
  :param text: text to analyze.
  :return: tuple of (Polarity, subjectivity), subjectivity in [0.0, 1.0].
  """
  lang, _ = detectLanguage(text)
  textToAnalyze = text

  sourceCode = LANG_CODE_MAP.get(lang)
  if sourceCode is not None:
    try:
      textToAnalyze = translateToEnglish(text, sourceCode)
    except (deep_translator.exceptions.RequestError, deep_translator.exceptions.TooManyRequests, requests.exceptions.RequestException):
      textToAnalyze = text

  blob = TextBlob(textToAnalyze)
  polarity = polarityFromScore(blob.sentiment.polarity)
  subjectivity = blob.sentiment.subjectivity

  return polarity, subjectivity
