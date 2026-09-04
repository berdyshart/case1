from domain.types import TextStats, Language


def flesсh_index(stats: TextStats, lang: Language) -> float:
    """
    Function to calculate the Flesch index
    :param stats: text statistics (sentences, words, syllables, averages)
    :param lang: text language (EN, RU, DE, FR)
    :return: number (Flesch index)
    """

    if stats.word_count == 0 and stats.sentence_count == 0:
        return 0.0

    if lang == Language.EN:
        return 206.835 - 1.015 * stats.avg_sentence_length - 84.6 * stats.avg_word_syllable

    elif lang == Language.RU:
        return 206.835 - 1.3 * stats.avg_sentence_length - 60.1 * stats.avg_word_syllables

    elif lang == Language.DE:
        return 180.0 - 1.0 * stats.avg_sentence_length - 58.5 * stats.avg_word_syllables

    elif lang == Language.FR:
        return 207.0 - 1.015 * stats.avg_sentence_length - 73.6 * stats.avg_word_syllables

