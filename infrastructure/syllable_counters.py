# import nltk
# nltk.download('cmudict'), запустить обе эти строки, если код запущен впервые
from nltk.corpus import cmudict
import string


TEST1 = "Hello, world! It's a beautiful day, isn't it? (And context-free)."
TEST2 = "Algoriphobia"
TEST3 = "Привет, мир! Это прекрасный день, не так ли? Робот-пылесос — круто."


def countSyllablesEnWordSimple(word: str) -> int:
    """
    Function to count the number of syllables in a word heuristically.
    :param word: word to count syllables in.
    :return: number of syllables.
    """
    word = word.lower().strip(".:;?!,()\"'-")
    if not word:
        return 0

    vowels = "aeiouy"
    count = 0
    is_prev_vowel = False

    for char in word:
        if char in vowels:
            if not is_prev_vowel:
                count += 1
                is_prev_vowel = True
        else:
            is_prev_vowel = False

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
    word = word.lower()

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
    to_remove = (string.punctuation + "«»—…“”").replace("'", "")

    for char in to_remove:
        text = text.replace(char, " ")

    return [countSyllablesEnWord(word) for word in text.split()]


def countSyllablesRuWord(word: str) -> int:
    """
    Function to count the number of syllables in a russian word.
    :param word: word to count syllables in.
    :return: number of syllables.
    """
    vowels = "аеёиоуыэюя"
    word = word.lower()

    return sum(1 for char in word if char in vowels)


def countSyllablesRu(text: str) -> list:
    """
    Function to count the number of syllables in a russian text.
    :param text: text to count syllables in.
    :return:
    """
    text = text.lower()
    to_remove = (string.punctuation + "«»—…“”").replace("-", "")
    for char in to_remove:
        text = text.replace(char, " ")

    return [countSyllablesRuWord(word) for word in text.split()]
