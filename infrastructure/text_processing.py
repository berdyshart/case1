from string import punctuation
from domain.types import TextStats
from domain.interfaces import SyllableCounter


def isEmptyText(text: str) -> bool:
  """Function to check if the incoming text is entirely empty."""
  return not text or not text.strip()


def isEmptyWord(word: str) -> bool:
  """Function to check if a specific word is empty."""
  return not word or not word.strip(punctuation + '«»—…“”')


def splitSentences(text: str) -> list[str]:
  """Function to split text into sentences."""
  if isEmptyText(text):
    return []
  cleanedText = text.replace('!', '.').replace('?', '.')
  sentences = [s.strip() for s in cleanedText.split('.') if s.strip()]
  if sentences:
    return sentences
  return [text.strip()]


def countSentences(text: str) -> int:
  """Function to return the total number of sentences in the text."""
  return len(splitSentences(text))


def splitWords(text: str) -> list[str]:
  """Function to split text into cleaned words without punctuation."""
  if isEmptyText(text):
    return []
  textClean = text.lower()
  toRemove = (punctuation + "«»‹›—–…“”„‚€§°" + "0123456789") \
    .replace("'", "").replace("-", "").replace('\'', '')
  for char in toRemove:
    textClean = textClean.replace(char, ' ')
  return [w for w in textClean.split() if w and not isEmptyWord(w)]


def countWords(text: str) -> int:
  """Function to return the total number of words in the text."""
  return len(splitWords(text))


def avgSentenceLength(text: str) -> float:
  """Function to calculate the average sentence length in words."""
  sentencesCount = countSentences(text)
  wordsCount = countWords(text)
  if sentencesCount == 0:
    return 0.0
  return wordsCount / sentencesCount


def avgWordLengthInChars(text: str) -> float:
  """Function to calculate the average word length in characters."""
  words = splitWords(text)
  if not words:
    return 0.0
  totalChars = sum(len(w) for w in words)
  return totalChars / len(words)


def computeStats(text: str, syllableCounter: SyllableCounter) -> TextStats:
  """Function to compute text stats."""
  words = splitWords(text)
  sentences = splitSentences(text)
  wCount = len(words)
  sCount = len(sentences)
  totalSyllables = sum(syllableCounter(text)) if wCount > 0 else 0
  avgSentLen = (wCount / sCount) if sCount > 0 else 0.0
  avgWordSyl = (totalSyllables / wCount) if wCount > 0 else 0.0
  return Text_Stats(
    sentenceCount=sCount,
    wordCount=wCount,
    syllableCount=totalSyllables,
    avgSentenceLength=avgSentLen,
    avgWordSyllables=avgWordSyl
  )