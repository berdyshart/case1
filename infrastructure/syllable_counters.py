import string
from functools import lru_cache

import nltk
import pyphen
from pylexique import Lexique383

from infrastructure import additional_metrics

TO_REMOVE = (string.punctuation + '«»‹›—–…""„‚€§°' + '0123456789') \
  .replace('\'', '').replace('-', '')


def cleanText(text: str) -> list[str]:
  # Cleans text and returns list of words.
  return additional_metrics.cleanText(text)


@lru_cache(maxsize=1)
def getFrenchLexicon():
  # Returns cached French lexicon.
  return Lexique383()


try:
  import cmudict
  CMU_DICT = cmudict.dict()
except (ImportError, OSError):
  CMU_DICT = {}

cmudict = nltk.corpus.cmudict
deDict = pyphen.Pyphen(lang='de_DE', left=1, right=1)
lex = getFrenchLexicon()


def countSyllablesEnWordSimple(word: str) -> int:
  # Function to count the number of syllables in a word heuristically.
  word = word.strip('.:;?!,()\"-\'')
  if not word:
    return 0

  vowels = 'aeiouy'
  count = 0
  isPrevVowel = False

  for char in word:
    if char in vowels:
      if not isPrevVowel:
        count += 1
        isPrevVowel = True
    else:
      isPrevVowel = False

  if word.endswith('e'):
    count -= 1

  if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
    count += 1

  if count <= 0:
    count = 1

  return count


def countSyllablesEnWord(word: str) -> int:
  # Function to count the number of syllables in an English word using cmudict.
  word = word.lower()

  if word in CMU_DICT:
    phoneme_count = len([phoneme for phoneme in CMU_DICT[word][0] if phoneme[-1].isdigit()])
    return phoneme_count

  return countSyllablesEnWordSimple(word)


def countSyllablesEn(text: str) -> list:
  # Function to count the number of syllables in an english text.
  text = text.lower()

  for char in TO_REMOVE:
    text = text.replace(char, ' ')

  return [countSyllablesEnWord(word) for word in text.split()]


def countSyllablesRuWord(word: str) -> int:
  # Function to count the number of syllables in a russian word.
  word = word.lower()
  vowels = 'аеёиоуыэюя'

  return sum(1 for char in word if char in vowels)


def countSyllablesRu(text: str) -> list:
  # Function to count the number of syllables in a russian text.
  text = text.lower()

  for char in TO_REMOVE:
    text = text.replace(char, ' ')

  return [countSyllablesRuWord(word) for word in text.split()]


def countVowelGroupsDe(chunk: str) -> int:
  # Function to count vowel groups in a string.
  count = 0
  isPrevVowel = False
  deVowels = 'aeiouyäöü'

  for char in chunk.lower():
    if char in deVowels:
      if not isPrevVowel:
        count += 1
      isPrevVowel = True
    else:
      isPrevVowel = False

  return count


def countSyllablesDeWord(word: str) -> int:
  # Function to count the number of syllables in a german word.
  total = 0

  for part in word.replace('\'', '').split('-'):
    part = ''.join(char for char in part if char.isalpha())
    if not part:
      continue

    chunks = deDict.inserted(part, hyphen='-').split('-')
    syllable_count = max(1, sum(countVowelGroupsDe(chunk) for chunk in chunks))
    total += syllable_count

  return total


def countSyllablesDe(text: str) -> list:
  # Function to count the number of syllables in a german text.
  text = text.lower()

  for char in TO_REMOVE:
    text = text.replace(char, ' ')

  words = [word.strip('\'-') for word in text.split()]
  return [countSyllablesDeWord(word) for word in words if word]


def countSyllablesFrWordSimple(word: str) -> int:
  # Function to count the number of syllables in a french word heuristically.
  frVowels = 'aeiouyàâäéèêëîïôöùûüÿœæ'
  frHiatusVowels = 'äëïöüÿ'

  groups = []
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
    stem = word[:-1] if word.endswith('s') else word
    if stem.endswith('e') and groups[-1] == 'e':
      count -= 1
    elif stem.endswith(('que', 'gue')) and groups[-1] == 'ue':
      count -= 1

  return max(1, count)


def countSyllablesFrWord(word):
  # Function to count syllables in a french word.
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
  # Function to count the number of syllables in a french text.
  text = text.lower()

  for char in TO_REMOVE:
    text = text.replace(char, ' ')

  return [countSyllablesFrWord(word) for word in text.split()]
