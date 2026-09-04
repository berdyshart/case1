# import nltk
# nltk.download('cmudict')
from nltk.corpus import cmudict
import string
import fasttext


TEST1 = "Hello, world! It's a beautiful day, isn't it? (And context-free)."
TEST2 = "Algoriphobia"
TEST3 = "Привет, мир! Это прекрасный день, не так ли? Робот-пылесос — круто."


def count_syllables_en_word_simple(word: str) -> int:
    """
    Эвристический метод подсчета слогов в одном английском слове.
    """
    word = word.lower().strip(".:;?!,()\"'-")
    if not word:
        return 0

    vowels = "aeiouy"
    count = 0
    is_prev_vowel = False

    for char in word:
        if char in vowels:
            if not is_prev_vowel:
                count += 1
                is_prev_vowel = True
        else:
            is_prev_vowel = False

    if word.endswith("e"):
        count -= 1

    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        count += 1

    if count <= 0:
        count = 1

    return count


def count_syllables_en_word(word):
    d = cmudict.dict()
    word = word.lower()
    if word in d:
        return len([ph for ph in d[word][0] if ph[-1].isdigit()])
    else:
        return count_syllables_en_word_simple(word)


def count_syllables_en(text):
    text = text.lower()
    to_remove = (string.punctuation + "«»—…“”").replace("'", "")

    for char in to_remove:
        text = text.replace(char, " ")

    return [count_syllables_en_word(word) for word in text.split()]


def count_syllables_ru_word(word) -> int:
    vowels = "аеёиоуыэюя"
    word = word.lower()
    return sum(1 for char in word if char in vowels)


def count_syllables_ru(text: str):
    """Считает общее количество слогов в русском тексте."""
    text = text.lower()
    to_remove = (string.punctuation + "«»—…“”").replace("-", "")
    for char in to_remove:
        text = text.replace(char, " ")

    return [count_syllables_ru_word(word) for word in text.split()]


def detect_language(text: str):
    model_path = "lid.176.ftz"
    model = fasttext.load_model(model_path)
    clean_text = text.replace("\n", " ").strip()

    # predict возвращает кортеж: (('__label__ru',), array([0.98]))
    predictions = model.predict(clean_text, k=1)
    print(predictions)
    # Извлекаем метку языка и точность
    label = predictions[0][0]
    confidence = predictions[1][0]

    # Удаляем префикс '__label__' чтобы получить чистый ISO-код (например, 'ru', 'en')
    lang_code = label.replace("__label__", "")

    return lang_code, confidence


if __name__ == '__main__':
    # print(count_syllables_en(TEST1))
    # print(count_syllables_en(TEST2))
    # print(count_syllables_ru(TEST3))

    lang, conf = detect_language(TEST1)
    print(lang, conf)
