from unittest.mock import patch, call
import pytest

from infrastructure.syllable_counters import (
  countSyllablesEnWordSimple,
  countSyllablesEnWord,
  countSyllablesEn,
  countSyllablesRuWord,
  countSyllablesRu,
  countSyllablesDeWord,
  countSyllablesDe,
)

@pytest.mark.parametrize(
  "word, expected",
  [
    ("cat", 1),
    ("hello", 2),
    ("beautiful", 3),
    ("isn't", 1),
    ("robot", 2),
    ("a", 1),
    ("y", 1),
    ("rhythm", 1),
  ],
)
def test_CountSyllablesEnWordSimpleBasicCases(word, expected):
  # Считает слоги в базовых английских словах.
  assert countSyllablesEnWordSimple(word) == expected

@pytest.mark.parametrize(
  "word, expected",
  [
    ("make", 1),
    ("like", 1),
    ("home", 1),
  ],
)
def test_CountSyllablesEnWordSimpleSilentE(word, expected):
  # Не считает немую "e" на конце слова слогом.
  assert countSyllablesEnWordSimple(word) == expected

@pytest.mark.parametrize(
  "word, expected",
  [
    ("table", 2),
    ("little", 2),
    ("simple", 2),
  ],
)
def test_CountSyllablesEnWordSimpleLeEnding(word, expected):
  # Считает окончание "-le" после согласной отдельным слогом.
  assert countSyllablesEnWordSimple(word) == expected

@pytest.mark.parametrize(
  "word, expected",
  [
    ("Hello,", "hello"),
    ("\"world!\"", "world"),
    ("(context-free).", "context-free"),
    ("isn't?", "isn't"),
    ("day,", "day"),
  ],
)
def test_CountSyllablesEnStripsSurroundingPunctuation(word, expected):
  # Убирает окружающие знаки препинания перед подсчётом слогов.
  with patch(
      "infrastructure.syllable_counters.countSyllablesEnWord",
      side_effect=lambda w: w,
  ):
    result = countSyllablesEn(word)

  assert result[0] == expected
  assert countSyllablesEnWordSimple("...") == 0
  assert countSyllablesEnWordSimple("") == 0

def test_CountSyllablesEnWordFallsBackToSimpleWhenNotFound():
  # Использует упрощённый подсчёт для слов, отсутствующих в словаре nltk.
  fakeDict = {}
  with patch("infrastructure.syllable_counters.cmudict.dict",
             return_value=fakeDict):
    with patch(
        "infrastructure.syllable_counters.countSyllablesEnWordSimple",
        return_value=0,
    ) as mockSimple:
      result = countSyllablesEnWord("algoriphobia")

  mockSimple.assert_called_once_with("algoriphobia")
  assert result == 0

def test_CountSyllablesEnReturnsOneValuePerWord():
  # Возвращает по одному значению на каждое слово текста.
  with patch(
      "infrastructure.syllable_counters.countSyllablesEnWord",
      side_effect=lambda w: 1,
  ) as mockWord:
    result = countSyllablesEn("Hello, world! It's a beautiful day.")

  assert len(result) == 6
  assert all(value == 1 for value in result)
  assert mockWord.call_count == 6

def test_CountSyllablesEnStripsPunctuationBeforeSplitting():
  # Убирает знаки препинания перед разбиением текста на слова.
  with patch(
      "infrastructure.syllable_counters.countSyllablesEnWord",
      side_effect=lambda w: w,
  ):
    result = countSyllablesEn("(And context-free).")

  assert result == ["and", "context-free"]

def test_CountSyllablesEnEmptyTextReturnsEmptyList():
  # Возвращает пустой список для пустого текста.

  assert countSyllablesEn("") == []

@pytest.mark.parametrize(
  "word, expected",
  [
    ("привет", 2),
    ("мир", 1),
    ("прекрасный", 3),
    ("не", 1),
    ("так", 1),
    ("ли", 1),
    ("робот-пылесос", 5),
    ("круто", 2),
  ],
)
def test_CountSyllablesRuWordBasicCases(word, expected):
  # Считает слоги в базовых русских словах.
  assert countSyllablesRuWord(word) == expected

def test_CountSyllablesRuWordNoVowelsReturnsZero():
  # Возвращает ноль для слов без гласных.
  assert countSyllablesRuWord("ъ") == 0
  assert countSyllablesRuWord("") == 0
  assert countSyllablesRuWord("ПРИВЕТ") == countSyllablesRuWord("привет")

def test_CountSyllablesRuStripsPunctuationButKeepsHyphen():
  # Убирает знаки препинания, сохраняя дефис между словами.

  with patch(
      "infrastructure.syllable_counters.countSyllablesRuWord",
      side_effect=lambda w: w,
  ):
    result = countSyllablesRu("Робот-пылесос — круто!")

  assert result == ["робот-пылесос", "круто"]

def test_CountSyllablesRuEmptyTextReturnsEmptyList():
  # Возвращает пустой список для пустого текста.

  assert countSyllablesRu("") == []

@pytest.mark.parametrize(
  "word, expected",
  [
    ("Haus", 1),
    ("Hund", 1),
    ("schön", 1),
    ("Katze", 2),
    ("Schule", 2),
    ("Straße", 2),
    ("Mädchen", 2),
    ("Zeitung", 2),
    ("Kindergarten", 4),
  ],
)
def test_CountSyllablesDeWordBasicCases(word, expected):
  # Считает слоги в базовых немецких словах.
  assert countSyllablesDeWord(word) == expected

@pytest.mark.parametrize(
  "word, expected",
  [
    ("Freund", 1),
    ("Auto", 2),
    ("Bäume", 2),
    ("Beispiel", 2),
    ("Fliegen", 2),
  ],
)
def test_CountSyllablesDeWordDiphthongsAndDigraphsAreOneSyllable(word, expected):
  # Считает дифтонги и диграфы (ei, eu, au, äu, ie) одним слогом.
  assert countSyllablesDeWord(word) == expected

@pytest.mark.parametrize(
  "word, expected",
  [
    ("Universität", 5),
    ("Ökonomie", 4),
    ("Übung", 2),
  ],
)
def test_CountSyllablesDeWordSingleLetterAtWordBoundary(word, expected):
  # Учитывает одиночную гласную в начале слова, которую pyphen не отделяет.
  assert countSyllablesDeWord(word) == expected

@pytest.mark.parametrize(
  "word, expected",
  [
    ("Fußballspiel", 3),
    ("Handschuh", 2),
    ("Donaudampfschifffahrtsgesellschaft", 8),
  ],
)
def test_CountSyllablesDeWordCompoundWords(word, expected):
  # Считает слоги в составных словах целиком.
  assert countSyllablesDeWord(word) == expected

@pytest.mark.parametrize(
  "word, expected",
  [
    ("E-Mail", 2),
    ("Baden-Württemberg", 5),
    ("Ost-West", 2),
  ],
)
def test_CountSyllablesDeWordHyphenatedWordsSumParts(word, expected):
  # Складывает слоги частей слова, разделённых дефисом.
  assert countSyllablesDeWord(word) == expected

@pytest.mark.parametrize(
  "word, expected",
  [
    ("geht's", 1),
    ("gibt's", 1),
    ("Wie's", 1),
  ],
)
def test_CountSyllablesDeWordIgnoresApostrophes(word, expected):
  # Не считает апостроф частью слова и не делит по нему слово.
  assert countSyllablesDeWord(word) == expected

@pytest.mark.parametrize(
  "word",
  [
    "Pst",
    "Hm",
    "Brr",
    "Psst",
  ],
)
def test_CountSyllablesDeWordWordWithoutVowelsHasOneSyllable(word):
  # Считает слово из одних согласных одним слогом, если в нём есть буквы.
  assert countSyllablesDeWord(word) == 1

@pytest.mark.parametrize(
  "word",
  [
    "123",
    "2024",
    "3,14",
  ],
)
def test_CountSyllablesDeWordNumbersHaveZeroSyllables(word):
  # Возвращает ноль для чисел, то есть слов без букв.
  assert countSyllablesDeWord(word) == 0

def test_CountSyllablesDeWordIgnoresDigitsInsideWord():
  # Игнорирует цифры внутри слова и считает только буквы.
  assert countSyllablesDeWord("Fußball2024") == countSyllablesDeWord("Fußball")
  assert countSyllablesDeWord("2024Fußball") == countSyllablesDeWord("Fußball")
  assert countSyllablesDeWord("Fuß2024ball") == countSyllablesDeWord("Fußball")

@pytest.mark.parametrize(
  "word",
  [
    "",
    "-",
    "---",
    "'",
    "'-'",
  ],
)
def test_CountSyllablesDeWordEmptyOrSeparatorsOnlyReturnsZero(word):
  # Возвращает ноль для пустой строки и строк из одних разделителей.
  assert countSyllablesDeWord(word) == 0

def test_CountSyllablesDeWordIgnoresLeadingAndTrailingHyphens():
  # Не создаёт лишних слогов из пустых частей по краям дефисного слова.
  assert countSyllablesDeWord("-Haus-") == 1
  assert countSyllablesDeWord("Haus--Tür") == countSyllablesDeWord("Haus-Tür")

def test_CountSyllablesDeWordCallsPyphenForEveryHyphenPart():
  # Вызывает pyphen отдельно для каждой части слова с дефисом.
  with patch("infrastructure.syllable_counters.deDict") as mockDict:
    mockDict.inserted.side_effect = lambda part, hyphen="-": part
    result = countSyllablesDeWord("Baden-Württemberg")

  assert mockDict.inserted.call_args_list == [
    call("Baden", hyphen="-"),
    call("Württemberg", hyphen="-"),
  ]
  assert result == 5

@pytest.mark.parametrize(
  "text, expected",
  [
    ("Hallo,", ["hallo"]),
    ("Welt!", ["welt"]),
    ("(Und Haus).", ["und", "haus"]),
    ("\"Tag\"", ["tag"]),
    ("Wirklich?!", ["wirklich"]),
    ("«Hallo» \u201cWelt\u201d", ["hallo", "welt"]),
  ],
)
def test_CountSyllablesDeStripsPunctuation(text, expected):
  # Убирает знаки препинания, включая немецкие кавычки, перед подсчётом слогов.
  with patch(
      "infrastructure.syllable_counters.countSyllablesDeWord",
      side_effect=lambda w: w,
  ):
    result = countSyllablesDe(text)

  assert result == expected
