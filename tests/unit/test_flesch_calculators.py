import domain.types, infrastructure.flesch_calculators

# Тесты для проверки работы функции fleschIndex (12 тестов).
def test_FleschIndexEnEasy():
  """
  Проверяем английскую формулу на простом тексте.
  Текст: "The cat sat on the mat." (6 слов, 6 слогов)
  """
  stats = domain.types.Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.EN)
  expected = 206.835 - 1.015 * 6 - 84.6 * 1
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschIndexEnComplex():
  """
  Проверяем английскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.EN)
  expected = 206.835 - 1.015 * 16.67 - 84.6 * 1.6
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschIndexEnDif():
  """
  Проверяем английскую формулу на сложном тексте (научная статья).
  Длинные предложения, много слогов на слово.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.EN)
  expected = 206.835 - 1.015 * 24.0 - 84.6 * 2.0
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschIndexRuEasy():
  """
  Проверяем русскую формулу на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.RU)
  expected = 206.835 - 1.3 * 6 - 60.1 * 1
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschIndexRuComplex():
  """
  Проверяем русскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.RU)
  expected = 206.835 - 1.3 * 16.67 - 60.1 * 1.6
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschIndexRuDif():
  """
  Проверяем русскую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.RU)
  expected = 206.835 - 1.3 * 24.0 - 60.1 * 2.0
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschIndexFrEasy():
  """
  Проверяем французскую формулу на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.FR)
  expected = 207.0 - 1.015 * 6 - 73.6 * 1
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschIndexFrComplex():
  """
  Проверяем французскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.FR)
  expected = 207.0 - 1.015 * 16.67 - 73.6 * 1.6
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschIndexFrDif():
  """
  Проверяем французскую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.FR)
  expected = 207.0 - 1.015 * 24.0 - 73.6 * 2.0
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschIndexDeEasy():
  """
  Проверяем немецкую формулу на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.DE)
  expected = 180.0 - 1.0 * 6 - 58.5 * 1
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschIndexDeComplex():
  """
  Проверяем немецкую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.DE)
  expected = 180.0 - 1.0 * 16.67 - 58.5 * 1.6
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschIndexDeDif():
  """
  Проверяем немецкую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = infrastructure.flesch_calculators.fleschIndex(stats, domain.types.Language.DE)
  expected = 180.0 - 1.0 * 24.0 - 58.5 * 2.0
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

# Тесты для проверки работы функции interpretFlesch.
def test_InterpretVeryEasy():
  """Проверяем уровень 'Very easy' для значений индекса от 90 и выше."""
  assert infrastructure.flesch_calculators.interpretFlesch(99) == 'Very easy'
  assert infrastructure.flesch_calculators.interpretFlesch(95) == 'Very easy'
  assert infrastructure.flesch_calculators.interpretFlesch(90) == 'Very easy'

def test_InterpretEasy():
  """Проверяем уровень 'Easy' для значений индекса от 80 до 90."""
  assert infrastructure.flesch_calculators.interpretFlesch(88) == 'Easy'
  assert infrastructure.flesch_calculators.interpretFlesch(85) == 'Easy'
  assert infrastructure.flesch_calculators.interpretFlesch(81) == 'Easy'

def test_InterpretFairlyEasy():
  """Проверяем уровень 'Fairly easy' для значений индекса от 70 до 80."""
  assert infrastructure.flesch_calculators.interpretFlesch(76) == 'Fairly easy'
  assert infrastructure.flesch_calculators.interpretFlesch(74) == 'Fairly easy'
  assert infrastructure.flesch_calculators.interpretFlesch(72) == 'Fairly easy'

def test_InterpretStandard():
  """Проверяем уровень 'Standard' для значений индекса от 60 до 70."""
  assert infrastructure.flesch_calculators.interpretFlesch(68) == 'Standard'
  assert infrastructure.flesch_calculators.interpretFlesch(65) == 'Standard'
  assert infrastructure.flesch_calculators.interpretFlesch(60) == 'Standard'

def test_InterpretFairlyDifficult():
  """Проверяем уровень 'Fairly difficult' для значений индекса от 50 до 60."""
  assert infrastructure.flesch_calculators.interpretFlesch(58) == 'Fairly difficult'
  assert infrastructure.flesch_calculators.interpretFlesch(55) == 'Fairly difficult'
  assert infrastructure.flesch_calculators.interpretFlesch(50) == 'Fairly difficult'

def test_InterpretDifficult():
  """Проверяем уровень 'Difficult' для значений индекса от 30 до 50."""
  assert infrastructure.flesch_calculators.interpretFlesch(48) == 'Difficult'
  assert infrastructure.flesch_calculators.interpretFlesch(40) == 'Difficult'
  assert infrastructure.flesch_calculators.interpretFlesch(30) == 'Difficult'

def test_InterpretVeryDifficult():
  """Проверяем уровень 'Very difficult' для значений индекса ниже 30."""
  assert infrastructure.flesch_calculators.interpretFlesch(29) == 'Very difficult'
  assert infrastructure.flesch_calculators.interpretFlesch(15) == 'Very difficult'
  assert infrastructure.flesch_calculators.interpretFlesch(0) == 'Very difficult'

# Тесты для проверки работы функции fleschKincaidIndex (13 тестов).
def test_FleschKincaidEmptyText():
  """
  Проверяем граничный случай: пустой текст (0 слов, 0 предложений).
  Функция должна вернуть 0.0 независимо от языка.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=0,
    wordCount=0,
    syllableCount=0,
    avgSentenceLength=0.0,
    avgWordSyllables=0.0
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.EN)
  assert score == 0.0

def test_FleschKincaidEnEasy():
  """
  Проверяем английскую формулу Флеша-Кинкейда на простом тексте.
  Текст: "The cat sat on the mat." (6 слов, 6 слогов)
  """
  stats = domain.types.Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.EN)
  expected = 0.39 * 6.0 + 11.8 * 1.0 - 15.59
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschKincaidEnComplex():
  """
  Проверяем английскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.EN)
  expected = 0.39 * 16.67 + 11.8 * 1.6 - 15.59
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschKincaidEnDif():
  """
  Проверяем английскую формулу на сложном тексте (научная статья).
  Длинные предложения, много слогов на слово.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.EN)
  expected = 0.39 * 24.0 + 11.8 * 2.0 - 15.59
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschKincaidRuEasy():
  """
  Проверяем русскую формулу (адаптация И. В. Оборонного) на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.RU)
  expected = 0.5 * 6.0 + 8.4 * 1.0 - 15.59
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschKincaidRuComplex():
  """
  Проверяем русскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.RU)
  expected = 0.5 * 16.67 + 8.4 * 1.6 - 15.59
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschKincaidRuDif():
  """
  Проверяем русскую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.RU)
  expected = 0.5 * 24.0 + 8.4 * 2.0 - 15.59
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschKincaidDeEasy():
  """
  Проверяем немецкую формулу (адаптация Amstad) на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.DE)
  expected = 0.4 * 6.0 + 9.2 * 1.0 - 12.0
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschKincaidDeComplex():
  """
  Проверяем немецкую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.DE)
  expected = 0.4 * 16.67 + 9.2 * 1.6 - 12.0
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschKincaidDeDif():
  """
  Проверяем немецкую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.DE)
  expected = 0.4 * 24.0 + 9.2 * 2.0 - 12.0
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschKincaidFrEasy():
  """
  Проверяем французскую формулу (адаптация Кинкейда) на простом тексте.
  Текст с 1 предложением, 6 словами, 6 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=1,
    wordCount=6,
    syllableCount=6,
    avgSentenceLength=6.0,
    avgWordSyllables=1.0
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.FR)
  expected = 0.39 * 6.0 + 10.5 * 1.0 - 14.5
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschKincaidFrComplex():
  """
  Проверяем французскую формулу на более сложном тексте.
  Текст с 3 предложениями, 50 словами, 80 слогами.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=3,
    wordCount=50,
    syllableCount=80,
    avgSentenceLength=16.67,
    avgWordSyllables=1.6
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.FR)
  expected = 0.39 * 16.67 + 10.5 * 1.6 - 14.5
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'

def test_FleschKincaidFrDif():
  """
  Проверяем французскую формулу на сложном тексте.
  Длинные предложения, много слогов на слово.
  """
  stats = domain.types.Text_Stats(
    sentenceCount=5,
    wordCount=120,
    syllableCount=240,
    avgSentenceLength=24.0,
    avgWordSyllables=2.0
  )
  score = infrastructure.flesch_calculators.fleschKincaidIndex(stats, domain.types.Language.FR)
  expected = 0.39 * 24.0 + 10.5 * 2.0 - 14.5
  assert abs(score - expected) < 0.01, f'Expected {expected:.2f}, got {score:.2f}'
