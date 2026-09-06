import pytest
from unittest.mock import patch, MagicMock

from infrastructure.language_detector import detectLanguage
from domain.types import Language


def test_DetectLanguageEnglish():
  # Arrange: подделываем модель, чтобы она всегда отвечала "en"
  fake_model = MagicMock()
  fake_model.predict.return_value = (("__label__en",), (0.95,))

  with patch("infrastructure.language_detector.fasttext.load_model",
             return_value=fake_model):
    # Act
    language, confidence = detectLanguage(
      "Hello, world! It's a beautiful day, isn't it?  (And context-free).")

  # Assert
  assert language == Language.EN
  assert confidence == 0.95


def test_DetectLanguageRussian():
  fake_model = MagicMock()
  fake_model.predict.return_value = (("__label__ru",), (0.99,))

  with patch("infrastructure.language_detector.fasttext.load_model",
             return_value=fake_model):
    language, confidence = detectLanguage(
      "Привет, мир! Это прекрасный день, не так ли? Робот-пылесос — круто.")

  assert language == Language.RU
  assert confidence == 0.99


def test_DetectLanguageReturnsValidTypes():
  """Проверяем именно ТИП возвращаемого значения — задача, из-за которой всё это затевалось."""
  fake_model = MagicMock()
  fake_model.predict.return_value = (("__label__en",), (0.9,))

  with patch("infrastructure.language_detector.fasttext.load_model",
             return_value=fake_model):
    language, confidence = detectLanguage("Some text")

  assert isinstance(language, Language)  # это объект enum, а не строка "en"
  assert isinstance(confidence, float)


def test_DetectLanguageReturnsTupleOfTwoElements():
  fake_model = MagicMock()
  fake_model.predict.return_value = (("__label__en",), (0.8,))

  with patch("infrastructure.language_detector.fasttext.load_model",
             return_value=fake_model):
    result = detectLanguage("text")

  assert isinstance(result, tuple)
  assert len(result) == 2


def test_DetectLanguageUnsupportedLanguage():
  """Язык, которого нет в LANG_CODE_MAP (например испанский), должен явно падать."""
  fake_model = MagicMock()
  fake_model.predict.return_value = (("__label__es",), (0.9,))

  with patch("infrastructure.language_detector.fasttext.load_model",
             return_value=fake_model):
    with pytest.raises(KeyError):
      detectLanguage("Hola, mundo!")
