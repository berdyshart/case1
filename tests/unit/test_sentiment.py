import unittest.mock as mock
import pytest
import requests.exceptions
import infrastructure.sentiment as sentimentModule
import domain.types as domainTypes

patch = mock.patch
MagicMock = mock.MagicMock
analyzeSentiment = sentimentModule.analyzeSentiment
Language = domainTypes.Language
Polarity = domainTypes.Polarity

def fakeBlob(polarity: float, subjectivity: float) -> MagicMock:
  # Помощник: создаёт мок TextBlob(...) с заданными polarity/subjectivity.
  blob = MagicMock()
  blob.sentiment.polarity = polarity
  blob.sentiment.subjectivity = subjectivity
  return blob

def test_AnalyzeSentimentEnglishPositive():
  # Английский текст анализируется напрямую, без перевода.
  with patch('infrastructure.sentiment.detectLanguage', return_value = (Language.EN, 0.99)), \
       patch('infrastructure.sentiment.TextBlob', return_value = fakeBlob(0.8, 0.6))\
               as fakeTextBlob, \
       patch('infrastructure.sentiment.deep_translator.GoogleTranslator') as fakeTranslator:
    polarity, subjectivity = analyzeSentiment('This is a wonderful day!')

  assert polarity == Polarity.POSITIVE
  assert subjectivity == 0.6
  fakeTextBlob.assert_called_once_with('This is a wonderful day!')
  fakeTranslator.assert_not_called()

def test_AnalyzeSentimentEnglishNegative():
  # Отрицательный полярный балл должен маппиться в Polarity.NEGATIVE.
  with patch('infrastructure.sentiment.detectLanguage', return_value = (Language.EN, 0.9)), \
       patch('infrastructure.sentiment.TextBlob', return_value = fakeBlob(-0.7, 0.4)):
    polarity, subjectivity = analyzeSentiment('This is a terrible day!')

  assert polarity == Polarity.NEGATIVE
  assert subjectivity == 0.4

def test_AnalyzeSentimentNeutral():
  # Балл внутри порога [-0.05, 0.05] должен считаться нейтральным.
  with patch('infrastructure.sentiment.detectLanguage', return_value = (Language.EN, 0.9)), \
       patch('infrastructure.sentiment.TextBlob', return_value = fakeBlob(0.0, 0.1)):
    polarity, subjectivity = analyzeSentiment('The report was published today.')

  assert polarity == Polarity.NEUTRAL
  assert subjectivity == 0.1

def test_AnalyzeSentimentRussianTranslatesBeforeAnalysis():
  # Для русского текста должен вызываться перевод перед анализом TextBlob.
  fakeTranslatorInstance = MagicMock()
  fakeTranslatorInstance.translate.return_value = 'This is a wonderful day!'

  with patch('infrastructure.sentiment.detectLanguage', return_value = (Language.RU, 0.95)), \
       patch(
         'infrastructure.sentiment.deep_translator.GoogleTranslator',
         return_value = fakeTranslatorInstance,
       ) as fakeTranslatorCls, \
       patch('infrastructure.sentiment.TextBlob', return_value = fakeBlob(0.8, 0.6))\
               as fakeTextBlob:
    polarity, subjectivity = analyzeSentiment('Это прекрасный день!')

  fakeTranslatorCls.assert_called_once_with(source = 'ru', target = 'en')
  fakeTranslatorInstance.translate.assert_called_once_with('Это прекрасный день!')
  fakeTextBlob.assert_called_once_with('This is a wonderful day!')
  assert polarity == Polarity.POSITIVE
  assert subjectivity == 0.6

@pytest.mark.parametrize('lang,code', [
  (Language.RU, 'ru'),
  (Language.DE, 'de'),
  (Language.FR, 'fr'),
])
def test_AnalyzeSentimentUsesCorrectLanguageCode(lang, code):
  # Для каждого не-английского языка используется верный код перевода.
  fakeTranslatorInstance = MagicMock()
  fakeTranslatorInstance.translate.return_value = 'Translated text'

  with patch('infrastructure.sentiment.detectLanguage', return_value = (lang, 0.9)), \
       patch(
         'infrastructure.sentiment.deep_translator.GoogleTranslator',
         return_value = fakeTranslatorInstance,
       ) as fakeTranslatorCls, \
       patch('infrastructure.sentiment.TextBlob', return_value = fakeBlob(0.0, 0.0)):
    analyzeSentiment('Some text')

  fakeTranslatorCls.assert_called_once_with(source = code, target = 'en')

def test_AnalyzeSentimentFallsBackToOriginalTextOnTranslationFailure():
  # Если перевод падает (например, нет сети), анализируется исходный текст.
  with patch('infrastructure.sentiment.detectLanguage', return_value = (Language.RU, 0.9)), \
       patch(
         'infrastructure.sentiment.deep_translator.GoogleTranslator',
         side_effect = requests.exceptions.ConnectionError('network error'),
       ), \
       patch('infrastructure.sentiment.TextBlob', return_value = fakeBlob(0.2, 0.3))\
               as fakeTextBlob:
    polarity, subjectivity = analyzeSentiment('Отличный день!')

  fakeTextBlob.assert_called_once_with('Отличный день!')
  assert polarity == Polarity.POSITIVE
  assert subjectivity == 0.3

def test_AnalyzeSentimentReturnsTupleOfPolarityAndFloat():
  # Проверяем типы возвращаемого результата (соответствие протоколу SentimentAnalyzer).
  with patch('infrastructure.sentiment.detectLanguage', return_value = (Language.EN, 0.9)), \
       patch('infrastructure.sentiment.TextBlob', return_value = fakeBlob(0.3, 0.5)):
    result = analyzeSentiment('Some text')

  assert isinstance(result, tuple)
  assert len(result) == 2
  polarity, subjectivity = result
  assert isinstance(polarity, Polarity)
  assert isinstance(subjectivity, float)
