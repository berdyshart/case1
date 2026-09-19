import string

import nltk
import pyphen

try:
  import cmudict
  CMU_DICT = cmudict.dict()
except (ImportError, OSError):
  CMU_DICT = {}

cmudict = nltk.corpus.cmudict
deDict = pyphen.Pyphen(lang="de_DE", left=1, right=1)

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
  Function to count the number of syllables in an English word using cmudict.
  :param word: word to count syllables in.
  :return: number of syllables.
  """
  word = word.lower()

  if word in CMU_DICT:
    return len([phoneme for phoneme in CMU_DICT[word][0] if phoneme[-1].isdigit()])

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
  word = word.lower()
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

def countVowelGroupsDe(chunk: str) -> int:
  """
  Function to count vowel groups in a string (ei, eu, au, ie, ee, ... count as one).
  :param chunk: part of a word.
  :return: number of vowel groups.
  """
  count = 0
  isPrevVowel = False
  deVowels = "aeiouyäöü"

  for char in chunk.lower():
    if char in deVowels:
      if not isPrevVowel:
        count += 1
      isPrevVowel = True
    else:
      isPrevVowel = False

  return count

def countSyllablesDeWord(word: str) -> int:
  """
  Function to count the number of syllables in a german word.
  Pyphen finds the boundaries (also between the parts of compound words),
  then vowel groups are counted inside every piece, because pyphen does not
  split off a single letter at the start/end (Uni-versität, Ö-ko-no-mie).
  Digits are ignored: a word without letters (a number) has 0 syllables.
  :param word: word to count syllables in (may contain '-' or apostrophes).
  :return: number of syllables.
  """
  total = 0

  for part in word.replace("'", "").split("-"):
    part = "".join(char for char in part if char.isalpha())
    if not part:
      continue

    chunks = deDict.inserted(part, hyphen="-").split("-")
    total += max(1, sum(countVowelGroupsDe(chunk) for chunk in chunks))

  return total

def countSyllablesDe(text: str) -> list:
  """
  Function to count the number of syllables in a german text.
  :param text: german text.
  :return: number of syllables of every word (numbers give 0).
  """
  text = text.lower().replace("’", "'")
  toRemove = (string.punctuation + "«»—…“”–").replace("-", "")

  for char in toRemove:
    if char == "'":
      text = text.replace(char, "")
    else:
      text = text.replace(char, " ")

  words = [word.strip("'-") for word in text.split()]
  return [countSyllablesDeWord(word) for word in words if word]

if __name__ == "__main__":
  print(*countSyllablesDe("Im Jahr 2026 kostet das Auto 12.500 € (3,5 % mehr) – E-Mail: Baden-Württemberg, geht’s!"), sep='\n')
