from domain.types import Text_Stats, Language


def flesch_index(stats: Text_Stats, lang: Language) -> float:
  # Рассчитывает индекс удобочитаемости Флеша для текста на указанном языке.
  if stats.wordCount == 0 and stats.sentenceCount == 0:
    return 0.0

  if lang == Language.EN:
    return 206.835 - 1.015 * stats.avgSentenceLength - 84.6 * stats.avgWordSyllables

  elif lang == Language.RU:
    return 206.835 - 1.3 * stats.avgSentenceLength - 60.1 * stats.avgWordSyllables

  elif lang == Language.DE:
    return 180.0 - 1.0 * stats.avgSentenceLength - 58.5 * stats.avgWordSyllables

  elif lang == Language.FR:
    return 207.0 - 1.015 * stats.avgSentenceLength - 73.6 * stats.avgWordSyllables


def interpret_flesch(score: float, lang: Language) -> str:
  # Преобразует значение индекса Флеша в текстовую интерпретацию уровня читаемости.
  if score >= 90:
    return 'Very easy'

  elif score >= 80:
    return 'Easy'

  elif score >= 70:
    return 'Fairly easy'

  elif score >= 60:
    return 'Standard'

  elif score >= 50:
    return 'Fairly difficult'

  elif score >= 30:
    return 'Difficult'

  else:
    return 'Very difficult'
