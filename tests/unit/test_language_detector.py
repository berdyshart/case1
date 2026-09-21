import unittest.mock
import pytest
import infrastructure.language_detector, domain.types

def test_DetectLanguageEnglish():
  # Распознаёт английский текст.
  fakeModel = unittest.mock.MagicMock()
  fakeModel.predict.return_value = (('__label__en',), (0.95,))

  with unittest.mock.patch('infrastructure.language_detector.fasttext.load_model',
                           return_value=fakeModel):
    language, confidence = infrastructure.language_detector.detectLanguage(
      'Hello, world! It\'s a beautiful day, isn\'t it?  (And context-free).')

  assert language == domain.types.Language.EN
  assert confidence == 0.95

def test_DetectLanguageRussian():
  # Распознаёт русский текст.
  fakeModel = unittest.mock.MagicMock()
  fakeModel.predict.return_value = (('__label__ru',), (0.99,))

  with unittest.mock.patch('infrastructure.language_detector.fasttext.load_model',
                           return_value=fakeModel):
    language, confidence = infrastructure.language_detector.detectLanguage(
      'Привет, мир! Это прекрасный день, не так ли? Робот-пылесос — круто.')

  assert language == domain.types.Language.RU
  assert confidence == 0.99

def test_DetectLanguageFrench():
  # Распознаёт французский текст.
  fakeModel = unittest.mock.MagicMock()
  fakeModel.predict.return_value = (('__label__fr',), (0.94,))
  with unittest.mock.patch('infrastructure.language_detector.fasttext.load_model', return_value=fakeModel):
    language, confidence = infrastructure.language_detector.detectLanguage(
      'Bonjour le monde! C\'est une belle journée, n\'est-ce pas?'
    )
  assert language == domain.types.Language.FR
  assert confidence == 0.94

def test_DetectLanguageGerman():
  # Распознаёт немецкий текст.
  fakeModel = unittest.mock.MagicMock()
  fakeModel.predict.return_value = (('__label__de',), (0.97,))
  with unittest.mock.patch('infrastructure.language_detector.fasttext.load_model', return_value=fakeModel):
    language, confidence = infrastructure.language_detector.detectLanguage(
      'Hallo Welt! Es ist ein wunderschöner Tag, nicht wahr?'
    )
  assert language == domain.types.Language.DE
  assert confidence == 0.97

def test_DetectLanguageReturnsValidTypes():
  # Проверяет типы возвращаемых значений.
  fakeModel = unittest.mock.MagicMock()
  fakeModel.predict.return_value = (('__label__en',), (0.9,))

  with unittest.mock.patch('infrastructure.language_detector.fasttext.load_model',
                           return_value=fakeModel):
    language, confidence = infrastructure.language_detector.detectLanguage('Some text')

  assert isinstance(language, domain.types.Language)
  assert isinstance(confidence, float)

def test_DetectLanguageReturnsTupleOfTwoElements():
  # Проверяет длину кортежа результата.
  fakeModel = unittest.mock.MagicMock()
  fakeModel.predict.return_value = (('__label__en',), (0.8,))

  with unittest.mock.patch('infrastructure.language_detector.fasttext.load_model',
                           return_value=fakeModel):
    result = infrastructure.language_detector.detectLanguage('text')

  assert isinstance(result, tuple)
  assert len(result) == 2

def test_DetectLanguageUnsupportedLanguage():
  # Проверяет ошибку при неизвестном языке.
  fakeModel = unittest.mock.MagicMock()
  fakeModel.predict.return_value = (('__label__es',), (0.9,))

  with unittest.mock.patch('infrastructure.language_detector.fasttext.load_model',
                           return_value=fakeModel):
    with pytest.raises(KeyError):
      infrastructure.language_detector.detectLanguage('Hola, mundo!')
