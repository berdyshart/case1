import pytest
from unittest.mock import patch

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
def test_count_syllables_en_word_simple_basic_cases(word, expected):
  assert countSyllablesEnWordSimple(word) == expected


@pytest.mark.parametrize(
  "word, expected",
  [
    ("make", 1),
    ("like", 1),
    ("home", 1),
  ],
)
def test_count_syllables_en_word_simple_silent_e(word, expected):
  """немая "e" на конце не считается слогом"""
  assert countSyllablesEnWordSimple(word) == expected


@pytest.mark.parametrize(
  "word, expected",
  [
    ("table", 2),
    ("little", 2),
    ("simple", 2),
  ],
)
def test_count_syllables_en_word_simple_le_ending(word, expected):
  """окончание "-le" после согласной добавляет слог"""
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
def test_count_syllables_en_strips_surrounding_punctuation(word, expected):
  """"""
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
def test_count_syllables_ru_word_basic_cases(word, expected):
  assert countSyllablesRuWord(word) == expected


def test_count_syllables_ru_word_no_vowels_returns_zero():
  assert countSyllablesRuWord("ъ") == 0
  assert countSyllablesRuWord("") == 0
  assert countSyllablesRuWord("ПРИВЕТ") == countSyllablesRuWord("привет")


def test_count_syllables_en_word_falls_back_to_simple_when_not_found():
  """Проверка слов, которых нет в ntlk"""
  fake_dict = {}  # словарь пуст, слова там точно нет
  with patch("infrastructure.syllable_counters.cmudict.dict",
             return_value=fake_dict):
    with patch(
        "infrastructure.syllable_counters.countSyllablesEnWordSimple",
        return_value=0,
        # контрольное значение, чтобы убедиться, что вызвался именно fallback
    ) as mock_simple:
      result = countSyllablesEnWord("algoriphobia")

  mock_simple.assert_called_once_with("algoriphobia")
  assert result == 0


def test_count_syllables_en_returns_one_value_per_word():
  with patch(
      "infrastructure.syllable_counters.countSyllablesEnWord",
      side_effect=lambda w: 1,
  ) as mock_word:
    result = countSyllablesEn("Hello, world! It's a beautiful day.")

  assert len(result) == 6
  assert all(value == 1 for value in result)
  assert mock_word.call_count == 6


def test_count_syllables_en_strips_punctuation_before_splitting():
  with patch(
      "infrastructure.syllable_counters.countSyllablesEnWord",
      side_effect=lambda w: w,
  ):
    result = countSyllablesEn("(And context-free).")

  assert result == ["and", "context-free"]


def test_count_syllables_en_empty_text_returns_empty_list():
  assert countSyllablesEn("") == []


def test_count_syllables_ru_strips_punctuation_but_keeps_hyphen():
  with patch(
      "infrastructure.syllable_counters.countSyllablesRuWord",
      side_effect=lambda w: w,
  ):
    result = countSyllablesRu("Робот-пылесос — круто!")

  assert result == ["робот-пылесос", "круто"]


def test_count_syllables_ru_empty_text_returns_empty_list():
  assert countSyllablesRu("") == []
