import fasttext
import os
import domain.types


LANG_CODE_MAP = {
    "en": domain.types.Language.EN,
    "ru": domain.types.Language.RU,
    "de": domain.types.Language.DE,
    "fr": domain.types.Language.FR,
}


def detectLanguage(text: str) -> tuple:
    """
    Function to detect the language of text.
    :param text: text to detect.
    :return: detected language.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "..", "lid.176.ftz")

    model = fasttext.load_model(os.path.normpath(MODEL_PATH))
    clean_text = text.replace("\n", " ").strip()

    predictions = model.predict(clean_text, k=1)
    label = predictions[0][0]
    confidence = predictions[1][0]
    lang_code = label.replace("__label__", "")

    lang = LANG_CODE_MAP[lang_code]

    return lang, confidence
