import fasttext


TEST1 = "Hello, world! It's a beautiful day, isn't it? (And context-free)."
TEST2 = "Algoriphobia"
TEST3 = "Привет, мир! Это прекрасный день, не так ли? Робот-пылесос — круто."


def detectLanguage(text: str) -> tuple:
    """
    Function to detect the language of text.
    :param text: text to detect.
    :return: detected language.
    """

    model_path = "lid.176.ftz"
    model = fasttext.load_model(model_path)
    clean_text = text.replace("\n", " ").strip()

    predictions = model.predict(clean_text, k=1)
    label = predictions[0][0]
    confidence = predictions[1][0]
    lang_code = label.replace("__label__", "")

    return lang_code, confidence
