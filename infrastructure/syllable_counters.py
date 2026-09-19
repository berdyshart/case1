import string
from functools import lru_cache
import nltk
import pyphen
import additional_metrics
from pylexique import Lexique383

def cleanText(text: str) -> list[str]:
  return additional_metrics.cleanText(text)

@lru_cache(maxsize=1)
def get_french_lexicon():
    return Lexique383()

try:
  import cmudict
  CMU_DICT = cmudict.dict()
except (ImportError, OSError):
  CMU_DICT = {}

cmudict = nltk.corpus.cmudict
deDict = pyphen.Pyphen(lang="de_DE", left=1, right=1)
lex = get_french_lexicon()

TO_REMOVE = (string.punctuation + "«»‹›—–…“”„‚€§°" + "0123456789")\
  .replace("'", "").replace("-", "")

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

  for char in TO_REMOVE:
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

  for char in TO_REMOVE:
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
  text = text.lower()

  for char in TO_REMOVE:
    text = text.replace(char, " ")

  words = [word.strip("'-") for word in text.split()]
  return [countSyllablesDeWord(word) for word in words if word]

def countSyllablesFrWordSimple(word: str) -> int:
  """
  Function to count the number of syllables in a french word heuristically (spoken french:
  a final silent e/es is not counted). Used when the word is not in the lexicon.
  :param word: lowercase word without punctuation.
  :return: number of syllables.
  """
  frVowels = "aeiouyàâäéèêëîïôöùûüÿœæ"
  frHiatusVowels = "äëïöüÿ"

  groups = []  # every vowel group as a string
  isPrevVowel = False

  for char in word:
    if char in frVowels:
      if isPrevVowel and char not in frHiatusVowels:
        groups[-1] += char
      else:
        groups.append(char)
      isPrevVowel = True
    else:
      isPrevVowel = False

  count = len(groups)

  if count > 1:
    stem = word[:-1] if word.endswith("s") else word
    if stem.endswith("e") and groups[-1] == "e":
      count -= 1
    elif stem.endswith(("que", "gue")) and groups[-1] == "ue":
      count -= 1  # arnaque, analytique, longue: u and e are both silent

  return max(1, count)

def countSyllablesFrWord(word):
  word = word.lower()
  word_data = lex.lexique.get(word)

  if word_data:
    if isinstance(word_data, list):
      word_data = word_data[0]
    syllables_str = word_data.syll

    if syllables_str:
      return len(syllables_str.split('-'))

  return countSyllablesFrWordSimple(word)

def countSyllablesFr(text: str) -> list:
  """
  Function to count the number of syllables in a french text.
  :param text: french text.
  :return: number of syllables of every word (numbers give 0).
  """
  text = text.lower()

  for char in TO_REMOVE:
    text = text.replace(char, " ")

  return [countSyllablesFrWord(word) for word in text.split()]
