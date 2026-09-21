import pyphen, pylexique
import infrastructure.text_processing

def cleanText(text: str) -> list[str]:
  """Function to split text into a list of words."""
  return infrastructure.text_processing.splitWords(text)

try:
  import cmudict
  CMU_DICT = cmudict.dict()
except (ImportError, OSError):
  CMU_DICT = {}

deDict = pyphen.Pyphen(lang='de_DE', left=1, right=1)
lexDict = pylexique.Lexique383()

def countSyllablesEnWordSimple(word: str) -> int:
  """
  Function to count the number of syllables in a word heuristically.
  :param word: word to count syllables in.
  :return: number of syllables.
  """
  word = word.strip('.:;?!,()"\'-')
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
  text = cleanText(text)
  return [countSyllablesEnWord(word) for word in text]

def countSyllablesRuWord(word: str) -> int:
  """
  Function to count the number of syllables in a russian word.
  :param word: word to count syllables in.
  :return: number of syllables.
  """
  word = word.lower()
  vowels = 'аеёиоуыэюя'

  return sum(1 for char in word if char in vowels)

def countSyllablesRu(text: str) -> list:
  """
  Function to count the number of syllables in a russian text.
  :param text: text to count syllables in.
  :return: number of syllables of every word.
  """
  text = cleanText(text)

  return [countSyllablesRuWord(word) for word in text]

def countVowelGroupsDe(chunk: str) -> int:
  """
  Function to count vowel groups in a string (ei, eu, au, ie, ee, ... count as one).
  :param chunk: part of a word.
  :return: number of vowel groups.
  """
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
  """
  Function to count the number of syllables in a german word.
  :param word: word to count syllables in (may contain '-' or apostrophes).
  :return: number of syllables.
  """
  total = 0

  for part in word.replace('\'', '').split('-'):
    part = ''.join(char for char in part if char.isalpha())
    if not part:
      continue

    chunks = deDict.inserted(part, hyphen='-').split('-')
    total += max(1, sum(countVowelGroupsDe(chunk) for chunk in chunks))

  return total

def countSyllablesDe(text: str) -> list:
  """
  Function to count the number of syllables in a german text.
  :param text: german text.
  :return: number of syllables of every word (numbers give 0).
  """
  text = cleanText(text)

  return [countSyllablesDeWord(word) for word in text]

def countSyllablesFrWordSimple(word: str) -> int:
  """
  Function to count the number of syllables in a french word heuristically.
  :param word: lowercase word without punctuation.
  :return: number of syllables.
  """
  frVowels = 'aeiouyàâäéèêëîïôöùûüÿœæ'
  frHiatusVowels = 'äëïöüÿ'

  groups = []  # Every vowel group as a string.
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
      count -= 1  # Arnaque, analytique, longue: u and e are both silent.

  return max(1, count)

def countSyllablesFrWord(word):
  """
  Function to count the number of syllables in a french word using the Lexique383 lexicon.
  :param word: word to count syllables in.
  :return: number of syllables.
  """
  word = word.lower()
  wordData = lexDict.lexique.get(word)

  if wordData:
    if isinstance(wordData, list):
      wordData = wordData[0]
    syllablesStr = wordData.syll

    if syllablesStr:
      return len(syllablesStr.split('-'))

  return countSyllablesFrWordSimple(word)

def countSyllablesFr(text: str) -> list:
  """
  Function to count the number of syllables in a french text.
  :param text: french text.
  :return: number of syllables of every word (numbers give 0).
  """
  text = cleanText(text)

  return [countSyllablesFrWord(word) for word in text]
