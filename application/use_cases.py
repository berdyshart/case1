from collections import Counter
from application.services import get_syllable_counter
from domain.types import Analysis_Result
from infrastructure.flesch_calculators import (fleschIndexб, fleschKincaidIndex, interpretFlesch)
from infrastructure.language_detector import detectLanguage
from infrastructure.sentiment import analyzeSentiment
from infrastructure.text_processing import computeStats, splitWords

def analyzeText(text: str) -> Analysis_Result:
  # Выполняет полный анализ одного текста.
  if not text or not text.strip():
    raise ValueError('Текст не должен быть пустым')

  language = detectLanguage(text)[0]

  syllableCounter = get_syllable_counter(language)
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
    lexicalDiversity = len(set(words)) / len(words)
    wordCounts = Counter(words)
    rareWordsCount = sum(1 for count in wordCounts.values() if count == 1)
    rareWordDensity = rareWordsCount / len(words)

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
