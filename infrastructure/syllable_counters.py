import string
import nltk
from nltk.corpus import cmudict
try:
    nltk.data.find('corpora/cmudict')
except LookupError:
    nltk.download('cmudict')

def countSyllablesEnWordSimple(word: str) -> int:
  """
  Function to count the number of syllables in a word heuristically.
  :param word: word to count syllables in.
  :return: number of syllables.
  """
  word = word.strip(".:;?!,()\"'-")
  if not word:
    return 0

  vowels = "aeiouy"
  count = 0
  isPrevVowel = False

  for char in word:
    if char in vowels:
      if not isPrevVowel:
        count += 1
        isPrevVowel = True
    else:
      isPrevVowel = False

  if word.endswith("e"):
    count -= 1

  if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
    count += 1

  if count <= 0:
    count = 1

  return count

def countSyllablesEnWord(word: str) -> int:
  """
  Function to count the number of syllables in an english word using nltk.
  :param word: word to count syllables in.
  :return: number of syllables.
  """
  d = cmudict.dict()

  if word in d:
    return len([ph for ph in d[word][0] if ph[-1].isdigit()])
  else:
    return countSyllablesEnWordSimple(word)

def countSyllablesEn(text: str) -> list:
  """
  Function to count the number of syllables in an english text.
  :param text: english text.
  :return: number of syllables.
  """
  text = text.lower()
  toRemove = (string.punctuation + "«»—…“”").replace("'", "").replace("-", "")

  for char in toRemove:
    text = text.replace(char, " ")

  return [countSyllablesEnWord(word) for word in text.split()]

def countSyllablesRuWord(word: str) -> int:
  """
  Function to count the number of syllables in a russian word.
  :param word: word to count syllables in.
  :return: number of syllables.
  """
  vowels = "аеёиоуыэюя"

  return sum(1 for char in word if char in vowels)

def countSyllablesRu(text: str) -> list:
  """
  Function to count the number of syllables in a russian text.
  :param text: text to count syllables in.
  :return:
  """
  text = text.lower()
  toRemove = (string.punctuation + "«»—…“”").replace("-", "")
  for char in toRemove:
    text = text.replace(char, " ")

  return [countSyllablesRuWord(word) for word in text.split()]
