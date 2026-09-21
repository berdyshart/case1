import unittest.mock
import pytest
import infrastructure.syllable_counters

MODULE = 'infrastructure.syllable_counters'
HUGE_TEXT_SIZE = 50_000

# English.
@pytest.mark.parametrize(
  'word, expected',
  [
    ('cat', 1),
    ('hello', 2),
    ('robot', 2),
    ('beautiful', 3),
    ('isn\'t', 1),
  ],
)
def test_CountSyllablesEnWordSimpleBasicCases(word, expected):
  # Считает слоги в типичных английских словах эвристикой.
  assert infrastructure.syllable_counters.countSyllablesEnWordSimple(word) == expected

@pytest.mark.parametrize(
  'word, expected',
  [
    ('make', 1),    # Немая "e" не считается слогом.
    ('home', 1),
    ('the', 1),     # После вычета немой "e" остаётся минимум один слог.
    ('table', 2),   # Окончание "-le" после согласной - отдельный слог.
    ('little', 2),
    ('apple', 2),
  ],
)
def test_CountSyllablesEnWordSimpleSilentEAndLeEnding(word, expected):
  # Учитывает немую "e" и окончание "-le" после согласной.
  assert infrastructure.syllable_counters.countSyllablesEnWordSimple(word) == expected

@pytest.mark.parametrize(
  'word, expected',
  [
    ('', 0),
    ('...', 0),
    ('\'', 0),
    ('(hello)', 2),  # Окружающая пунктуация срезается.
    ('a', 1),
    ('y', 1),
    ('rhythm', 1),   # Буква "y" считается гласной.
  ],
)
def test_CountSyllablesEnWordSimpleDegenerateInput(word, expected):
  # Пустые и состоящие из пунктуации строки дают 0, слова без явных гласных - минимум 1.
  assert infrastructure.syllable_counters.countSyllablesEnWordSimple(word) == expected

def test_CountSyllablesEnWordUsesDictionaryFirstAndFallsBackToSimple():
  # Сначала смотрит в cmudict (без учёта регистра), при отсутствии слова - эвристика.
  fakeDict = {'cat': [['K', 'AE1', 'T', 'AH0', 'P']]}  # Всего 2 гласных (ударных и безударных).
  with unittest.mock.patch.dict(f'{MODULE}.CMU_DICT', fakeDict, clear=True):
    assert infrastructure.syllable_counters.countSyllablesEnWord('CAT') == 2

    with unittest.mock.patch(f'{MODULE}.countSyllablesEnWordSimple', return_value=42) as mockSimple:
      assert infrastructure.syllable_counters.countSyllablesEnWord('Qzxvw') == 42

  mockSimple.assert_called_once_with('qzxvw')

# Russian.
@pytest.mark.parametrize(
  'word, expected',
  [
    ('привет', 2),
    ('мир', 1),
    ('не', 1),
    ('круто', 2),
    ('прекрасный', 3),
  ],
)
def test_CountSyllablesRuWordBasicCases(word, expected):
  # Считает слоги в типичных русских словах (слог = гласная).
  assert infrastructure.syllable_counters.countSyllablesRuWord(word) == expected

@pytest.mark.parametrize(
  'word, expected',
  [
    ('ёлка', 2),           # Буква "ё" - гласная.
    ('съёмка', 2),         # Буква "ъ" слог не образует.
    ('робот-пылесос', 5),  # Дефис не мешает, слоги частей складываются.
    ('кое-что', 3),
  ],
)
def test_CountSyllablesRuWordYoSignsAndHyphen(word, expected):
  # Учитывает "ё", не считает "ъ"/"ь" и суммирует слоги через дефис.
  assert infrastructure.syllable_counters.countSyllablesRuWord(word) == expected

@pytest.mark.parametrize(
  'word',
  ['', 'ъ', 'ь', 'в', '123', 'hello', '-', '...'],
)
def test_CountSyllablesRuWordWithoutRussianVowelsReturnsZero(word):
  # Возвращает 0 для пустой строки, слов без гласных, цифр и не-кириллицы.
  assert infrastructure.syllable_counters.countSyllablesRuWord(word) == 0

@pytest.mark.parametrize(
  'word, expected',
  [
    ('ПРИВЕТ', 2),
    ('Привет', 2),
    ('ЁЛКА', 2),
  ],
)
def test_CountSyllablesRuWordIsCaseInsensitive(word, expected):
  # Регистр букв не влияет на результат.
  assert infrastructure.syllable_counters.countSyllablesRuWord(word) == expected

# German.
@pytest.mark.parametrize(
  'word, expected',
  [
    ('Haus', 1),
    ('Katze', 2),
    ('Straße', 2),
    ('Mädchen', 2),
    ('Kindergarten', 4),
  ],
)
def test_CountSyllablesDeWordBasicCases(word, expected):
  # Считает слоги в типичных немецких словах.
  assert infrastructure.syllable_counters.countSyllablesDeWord(word) == expected

@pytest.mark.parametrize(
  'word, expected',
  [
    ('Freund', 1),                              # Дифтонг - один слог.
    ('Auto', 2),
    ('Universität', 5),                         # Одиночная гласная в начале слова.
    ('Ökonomie', 4),
    ('Fußballspiel', 3),                        # Составное слово.
    ('Donaudampfschifffahrtsgesellschaft', 8),
    ('Baden-Württemberg', 5),                   # Части через дефис суммируются.
    ('geht\'s', 1),                              # Апостроф не делит слово.
  ],
)
def test_CountSyllablesDeWordLanguageSpecificRules(word, expected):
  # Дифтонги, одиночные гласные на границе слова, композиты, дефис и апостроф.
  assert infrastructure.syllable_counters.countSyllablesDeWord(word) == expected

@pytest.mark.parametrize(
  'word, expected',
  [
    ('', 0),
    ('-', 0),
    ('\'-\'', 0),
    ('123', 0),
    ('3,14', 0),
    ('Fußball2024', 2),  # Цифры внутри слова игнорируются.
    ('-Haus-', 1),       # Пустые части по краям слогов не дают.
    ('Pst', 1),          # Слово из букв без гласных - минимум 1.
    ('Brr', 1),
  ],
)
def test_CountSyllablesDeWordDegenerateInput(word, expected):
  # Пусто, разделители и числа - 0 слогов; слово без гласных - 1.
  assert infrastructure.syllable_counters.countSyllablesDeWord(word) == expected

def test_CountSyllablesDeWordCallsPyphenPerPartAndCountsVowelGroups():
  # Вызывает pyphen для каждой части с дефисом и считает группы гласных в кусках.
  with unittest.mock.patch(f'{MODULE}.deDict') as mockDict:
    mockDict.inserted.side_effect = ['Ba-den', 'Würt-tem-berg']
    result = infrastructure.syllable_counters.countSyllablesDeWord('Baden-Württemberg')

  assert mockDict.inserted.call_args_list == [
    unittest.mock.call('Baden', hyphen='-'),
    unittest.mock.call('Württemberg', hyphen='-'),
  ]
  assert result == 5

# French.
@pytest.mark.parametrize(
  'word, expected',
  [
    ('chat', 1),
    ('bonjour', 2),
    ('maison', 2),
    ('ordinateur', 4),
    ('université', 5),
  ],
)
def test_CountSyllablesFrWordBasicCasesFromLexicon(word, expected):
  # Считает слоги в типичных французских словах по реальному словарю Lexique.
  assert infrastructure.syllable_counters.countSyllablesFrWord(word) == expected

@pytest.mark.parametrize(
  'word, expected',
  [
    ('eau', 1),      # Тройная гласная - один слог.
    ('maisons', 2),
    ('belle', 1),    # Конечное немое "e"/"es" не считается.
    ('arnaque', 2),  # Окончание "-que": "u" и "e" немые.
    ('longue', 1),
    ('haïr', 2),     # Трема разрывает группу гласных (hiatus).
    ('je', 1),       # Односложное слово не теряет единственный слог.
  ],
)
def test_CountSyllablesFrWordSimpleSpokenFrenchRules(word, expected):
  # Эвристика: немое "e", "-que/-gue", hiatus и минимум один слог.
  assert infrastructure.syllable_counters.countSyllablesFrWordSimple(word) == expected

@pytest.mark.parametrize(
  'lexiconEntry',
  [None, unittest.mock.MagicMock(syll=''), [unittest.mock.MagicMock(syll='')]],
  ids=['not-in-lexicon', 'empty-syll', 'empty-syll-in-list'],
)
def test_CountSyllablesFrWordFallsBackToSimpleWhenLexiconHasNoSyllables(lexiconEntry):
  # Использует эвристику, если слова нет в Lexique или у него пустая слоговая запись.
  with unittest.mock.patch(f'{MODULE}.lexDict') as mockLex:
    mockLex.lexique.get.return_value = lexiconEntry
    with unittest.mock.patch(f'{MODULE}.countSyllablesFrWordSimple', return_value=7) as mockSimple:
      result = infrastructure.syllable_counters.countSyllablesFrWord('QwxZyt')

  mockSimple.assert_called_once_with('qwxzyt')
  assert result == 7

@pytest.mark.parametrize(
  'lexiconEntry, expected',
  [
    (unittest.mock.MagicMock(syll='bO~-Zur'), 2),
    ([unittest.mock.MagicMock(syll='a-b-c'), unittest.mock.MagicMock(syll='a')], 3),  # Омографы: берётся первая запись.
  ],
  ids=['single-entry', 'homograph-list'],
)
def test_CountSyllablesFrWordLowercasesWordAndReadsSyllFromLexicon(lexiconEntry, expected):
  # Приводит слово к нижнему регистру перед поиском и считает части поля syll.
  with unittest.mock.patch(f'{MODULE}.lexDict') as mockLex:
    mockLex.lexique.get.return_value = lexiconEntry
    result = infrastructure.syllable_counters.countSyllablesFrWord('BonJour')

  mockLex.lexique.get.assert_called_once_with('bonjour')
  assert result == expected

# Wrappers: empty and huge text (shared for all languages).
@pytest.mark.parametrize(
  'countFunc, word, expectedPerWord',
  [
    (infrastructure.syllable_counters.countSyllablesEn, 'hello', 2),
    (infrastructure.syllable_counters.countSyllablesRu, 'привет', 2),
    (infrastructure.syllable_counters.countSyllablesDe, 'Haus', 1),
    (infrastructure.syllable_counters.countSyllablesFr, 'bonjour', 2),
  ],
  ids=['en', 'ru', 'de', 'fr'],
)
def test_CountSyllablesWrapperHandlesEmptyAndHugeText(countFunc, word, expectedPerWord):
  # Возвращает [] для текста без слов и по одному значению на слово для очень большого текста.
  with unittest.mock.patch(f'{MODULE}.cleanText', return_value=[]):
    assert countFunc('') == []

  with unittest.mock.patch(f'{MODULE}.cleanText', return_value=[word] * HUGE_TEXT_SIZE):
    result = countFunc('ignored')

  assert result == [expectedPerWord] * HUGE_TEXT_SIZE
