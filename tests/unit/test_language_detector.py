from unittest.mock import patch, MagicMock
import pytest
from infrastructure.language_detector import detectLanguage
from domain.types import Language

def test_DetectLanguageEnglish():
  # Распознаёт английский текст.
  fakeModel = MagicMock()
  fakeModel.predict.return_value = (("__label__en",), (0.95,))

  with patch("infrastructure.language_detector.fasttext.load_model",
             return_value=fakeModel):
    language, confidence = detectLanguage(
      "Hello, world! It's a beautiful day, isn't it?  (And context-free).")

  assert language == Language.EN
  assert confidence == 0.95

def test_DetectLanguageRussian():
  # Распознаёт русский текст.
  fakeModel = MagicMock()
  fakeModel.predict.return_value = (("__label__ru",), (0.99,))

  with patch("infrastructure.language_detector.fasttext.load_model",
             return_value=fakeModel):
    language, confidence = detectLanguage(
      "Привет, мир! Это прекрасный день, не так ли? Робот-пылесос — круто.")

  assert language == Language.RU
  assert confidence == 0.99

def test_DetectLanguageReturnsValidTypes():
  # Проверяет типы возвращаемых значений.
  fakeModel = MagicMock()
  fakeModel.predict.return_value = (("__label__en",), (0.9,))

  with patch("infrastructure.language_detector.fasttext.load_model",
             return_value=fakeModel):
    language, confidence = detectLanguage("Some text")

  assert isinstance(language, Language)
  assert isinstance(confidence, float)

def test_DetectLanguageReturnsTupleOfTwoElements():
  # Проверяет длину кортежа результата.
  fakeModel = MagicMock()
  fakeModel.predict.return_value = (("__label__en",), (0.8,))

  with patch("infrastructure.language_detector.fasttext.load_model",
             return_value=fakeModel):
    result = detectLanguage("text")

  assert isinstance(result, tuple)
  assert len(result) == 2

def test_DetectLanguageUnsupportedLanguage():
  # Проверяет ошибку при неизвестном языке.
  fakeModel = MagicMock()
  fakeModel.predict.return_value = (("__label__es",), (0.9,))

  with patch("infrastructure.language_detector.fasttext.load_model",
             return_value=fakeModel):
    with pytest.raises(KeyError):
      detectLanguage("Hola, mundo!")
