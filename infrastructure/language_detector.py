import os
import fasttext
import domain.types

LANG_CODE_MAP = {
  'en': domain.types.Language.EN,
  'ru': domain.types.Language.RU,
  'de': domain.types.Language.DE,
  'fr': domain.types.Language.FR,
}

def detectLanguage(text: str) -> tuple:
  # Function to detect the language of text.
  baseDir = os.path.dirname(os.path.abspath(__file__))
  modelPath = os.path.join(baseDir, '..', 'lid.176.ftz')

  model = fasttext.load_model(os.path.normpath(modelPath))
  cleanText = text.replace('\n', ' ').strip()

  predictions = model.predict(cleanText, k=1)
  label = predictions[0][0]
  confidence = predictions[1][0]
  langCode = label.replace('__label__', '')

  lang = LANG_CODE_MAP[langCode]

  return lang, confidence
