from unittest.mock import patch
import pytest

from infrastructure.syllable_counters import (
  countSyllablesEnWordSimple,
  countSyllablesEnWord,
  countSyllablesEn,
  countSyllablesRuWord,
  countSyllablesRu,
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
