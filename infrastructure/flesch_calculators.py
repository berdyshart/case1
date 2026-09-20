from domain.types import Text_Stats, Language

def fleschIndex(stats: Text_Stats, lang: Language) -> float | None:
  """Calculates the Flesch readability index for text in the specified language."""
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

def interpretFlesch(score: float) -> str:
  """Converts a Flesch index value to a text interpretation of readability level."""
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

def fleschKincaidIndex(stats: Text_Stats, lang: Language) -> float | None:
  """Calculates the Flesch-Kincaid text complexity index for the specified language."""
  if stats.wordCount == 0 and stats.sentenceCount == 0:
    return 0.0

  if lang == Language.EN:
    # Classical Flesch-Kincaid formula (U.S. Grade Level)
    return 0.39 * stats.avgSentenceLength + 11.8 * stats.avgWordSyllables - 15.59

  elif lang == Language.RU:
    # Adaptation for Russian education system (I. V. Oboronnyy)
    return 0.5 * stats.avgSentenceLength + 8.4 * stats.avgWordSyllables - 15.59

  elif lang == Language.DE:
    # German modification of Grade Level (Amstad index / Bern adaptation)
    return 0.4 * stats.avgSentenceLength + 9.2 * stats.avgWordSyllables - 12.0

  elif lang == Language.FR:
    # French modification of Grade Level (Kincaid formula adaptation)
    return 0.39 * stats.avgSentenceLength + 10.5 * stats.avgWordSyllables - 14.5

  return None
