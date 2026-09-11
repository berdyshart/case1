import pytest
from domain.types import Text_Stats, Language
from infrastructure.flesch_calculators import fleschIndex, interpretFlesch, fleschKincaidIndex

# Тесты для проверки работы функции FleschIndex (12 тестов)
def test_FleschIndexEnEasy():
  """
  Проверяем английскую формулу на простом тексте.
  Текст: "The cat sat on the mat." (6 слов, 6 слогов)
  """
  stats = Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = fleschIndex(stats, Language.EN)
  expected = 206.835 - 1.015 * 6 - 84.6 * 1
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschIndexEnComplex():
  """
  Проверяем английскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = fleschIndex(stats, Language.EN)
  expected = 206.835 - 1.015 * 16.67 - 84.6 * 1.6
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschIndexEnDif():
  """
  Проверяем английскую формулу на сложном тексте (научная статья).
  Длинные предложения, много слогов на слово.
  """
  stats = Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = fleschIndex(stats, Language.EN)
  expected = 206.835 - 1.015 * 24.0 - 84.6 * 2.0
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschIndexRuEasy():
  """
  Проверяем русскую формулу на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = fleschIndex(stats, Language.RU)
  expected = 206.835 - 1.3 * 6 - 60.1 * 1
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschIndexRuComplex():
  """
  Проверяем русскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = fleschIndex(stats, Language.RU)
  expected = 206.835 - 1.3 * 16.67 - 60.1 * 1.6
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschIndexRuDif():
  """
  Проверяем русскую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = fleschIndex(stats, Language.RU)
  expected = 206.835 - 1.3 * 24.0 - 60.1 * 2.0
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschIndexFrEasy():
  """
  Проверяем французскую формулу на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = fleschIndex(stats, Language.FR)
  expected = 207.0 - 1.015 * 6 - 73.6 * 1
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschIndexFrComplex():
  """
  Проверяем французскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = fleschIndex(stats, Language.FR)
  expected = 207.0 - 1.015 * 16.67 - 73.6 * 1.6
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschIndexFrDif():
  """
  Проверяем французскую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = fleschIndex(stats, Language.FR)
  expected = 207.0 - 1.015 * 24.0 - 73.6 * 2.0
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschIndexDeEasy():
  """
  Проверяем немецкую формулу на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = fleschIndex(stats, Language.DE)
  expected = 180.0 - 1.0 * 6 - 58.5 * 1
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschIndexDeComplex():
  """
  Проверяем немецкую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = fleschIndex(stats, Language.DE)
  expected = 180.0 - 1.0 * 16.67 - 58.5 * 1.6
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschIndexDeDif():
  """
  Проверяем немецкую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = fleschIndex(stats, Language.DE)
  expected = 180.0 - 1.0 * 24.0 - 58.5 * 2.0
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

# Тесты для проверки работы функции interpretFlesch
def test_interpretVeryEasy():
  assert interpretFlesch(99) == "Very easy"
  assert interpretFlesch(95) == "Very easy"
  assert interpretFlesch(90) == "Very easy"

def test_interpretEasy():
  assert interpretFlesch(88) == "Easy"
  assert interpretFlesch(85) == "Easy"
  assert interpretFlesch(81) == "Easy"

def test_interpretFairlyEasy():
  assert interpretFlesch(76) == "Fairly easy"
  assert interpretFlesch(74) == "Fairly easy"
  assert interpretFlesch(72) == "Fairly easy"

def test_interpretStandard():
  assert interpretFlesch(68) == "Standard"
  assert interpretFlesch(65) == "Standard"
  assert interpretFlesch(60) == "Standard"

def test_interpretFairlyDifficult():
  assert interpretFlesch(58) == "Fairly difficult"
  assert interpretFlesch(55) == "Fairly difficult"
  assert interpretFlesch(50) == "Fairly difficult"
def test_interpretDifficult():
  assert interpretFlesch(48) == "Difficult"
  assert interpretFlesch(40) == "Difficult"
  assert interpretFlesch(30) == "Difficult"

def test_interpretVeryDifficult():
  assert interpretFlesch(29) == "Very difficult"
  assert interpretFlesch(15) == "Very difficult"
  assert interpretFlesch(0) == "Very difficult"

# Тесты для проверки работы функции fleschKincaidIndex (13 тестов)

def test_FleschKincaidEmptyText():
  """
  Проверяем граничный случай: пустой текст (0 слов, 0 предложений).
  Функция должна вернуть 0.0 независимо от языка.
  """
  stats = Text_Stats(
    sentenceCount=0,
    wordCount=0,
    syllableCount=0,
    avgSentenceLength=0.0,
    avgWordSyllables=0.0
  )
  score = fleschKincaidIndex(stats, Language.EN)
  assert score == 0.0

def test_FleschKincaidEnEasy():
  """
  Проверяем английскую формулу Флеша-Кинкейда на простом тексте.
  Текст: "The cat sat on the mat." (6 слов, 6 слогов)
  """
  stats = Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = fleschKincaidIndex(stats, Language.EN)
  expected = 0.39 * 6.0 + 11.8 * 1.0 - 15.59
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschKincaidEnComplex():
  """
  Проверяем английскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = fleschKincaidIndex(stats, Language.EN)
  expected = 0.39 * 16.67 + 11.8 * 1.6 - 15.59
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschKincaidEnDif():
  """
  Проверяем английскую формулу на сложном тексте (научная статья).
  Длинные предложения, много слогов на слово.
  """
  stats = Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = fleschKincaidIndex(stats, Language.EN)
  expected = 0.39 * 24.0 + 11.8 * 2.0 - 15.59
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschKincaidRuEasy():
  """
  Проверяем русскую формулу (адаптация И. В. Оборонного) на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = fleschKincaidIndex(stats, Language.RU)
  expected = 0.5 * 6.0 + 8.4 * 1.0 - 15.59
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschKincaidRuComplex():
  """
  Проверяем русскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = fleschKincaidIndex(stats, Language.RU)
  expected = 0.5 * 16.67 + 8.4 * 1.6 - 15.59
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschKincaidRuDif():
  """
  Проверяем русскую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = fleschKincaidIndex(stats, Language.RU)
  expected = 0.5 * 24.0 + 8.4 * 2.0 - 15.59
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschKincaidDeEasy():
  """
  Проверяем немецкую формулу (адаптация Amstad) на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = fleschKincaidIndex(stats, Language.DE)
  expected = 0.4 * 6.0 + 9.2 * 1.0 - 12.0
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschKincaidDeComplex():
  """
  Проверяем немецкую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = fleschKincaidIndex(stats, Language.DE)
  expected = 0.4 * 16.67 + 9.2 * 1.6 - 12.0
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschKincaidDeDif():
  """
  Проверяем немецкую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = fleschKincaidIndex(stats, Language.DE)
  expected = 0.4 * 24.0 + 9.2 * 2.0 - 12.0
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschKincaidFrEasy():
  """
  Проверяем французскую формулу (адаптация Кинкейда) на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = fleschKincaidIndex(stats, Language.FR)
  expected = 0.39 * 6.0 + 10.5 * 1.0 - 14.5
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschKincaidFrComplex():
  """
  Проверяем французскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = fleschKincaidIndex(stats, Language.FR)
  expected = 0.39 * 16.67 + 10.5 * 1.6 - 14.5
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"

def test_FleschKincaidFrDif():
  """
  Проверяем французскую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = fleschKincaidIndex(stats, Language.FR)
  expected = 0.39 * 24.0 + 10.5 * 2.0 - 14.5
  assert abs(score - expected) < 0.01, f"Expected {expected:.2f}, got {score:.2f}"
