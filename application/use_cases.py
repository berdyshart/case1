from collections import Counter

import infrastructure.additional_metrics

from application.services import getSyllableCounter
from domain.types import Analysis_Result
from infrastructure.flesch_calculators import fleschIndex, fleschKincaidIndex, interpretFlesch
from infrastructure.language_detector import detectLanguage
from infrastructure.sentiment import analyzeSentiment
from infrastructure.text_processing import computeStats, splitWords
from infrastructure.additional_metrics import lexicalDiversity, rareWordDensity


def analyzeText(text: str) -> Analysis_Result:
  # Выполняет полный анализ одного текста.
  if not text or not text.strip():
    raise ValueError('Текст не должен быть пустым')

  language = detectLanguage(text)[0]
  syllableCounter = getSyllableCounter(language)
  stats = computeStats(text, syllableCounter)

  fleschIndexValue = fleschIndex(stats, language)
  fleschKincaidValue = fleschKincaidIndex(stats, language)

  if fleschIndexValue is None or fleschKincaidValue is None:
    raise ValueError(
      f'Анализ для языка {language.name} не поддерживается'
    )

  interpretation = interpretFlesch(fleschIndexValue)
  polarity, subjectivity = analyzeSentiment(text)
  words = splitWords(text)

  if words:
    lexicalDiversity = infrastructure.additional_metrics.lexicalDiversity(words)
    rareWordDensity = infrastructure.additional_metrics.rareWordDensity(words)
  else:
    lexicalDiversity = 0.0
    rareWordDensity = 0.0

  return Analysis_Result(
    language=language,
    fleschIndex=fleschIndexValue,
    fleschKincaid=fleschKincaidValue,
    interpretation=interpretation,
    polarity=polarity,
    subjectivity=subjectivity,
    lexicalDiversity=lexicalDiversity,
    rareWordDensity=rareWordDensity,
    stats=stats
  )


def analyzeBatch(texts: list[str]) -> list[Analysis_Result]:
  # Выполняет анализ списка текстов.
  if not texts:
    raise ValueError('Список текстов не должен быть пустым')

  return [analyzeText(text) for text in texts]
