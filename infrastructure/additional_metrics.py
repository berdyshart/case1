import string, collections

TO_REMOVE = (string.punctuation + '«»‹›—–…“”„‚€§°' + '0123456789') \
  .replace('\'', '').replace('-', '')

REMOVE_SET = set(TO_REMOVE)
APOSTROPHE_VARIANTS = ('’', '‘', 'ʼ', '`', '´')

FRENCH_ELISIONS = {
  'l', 'd', 'j', 'n', 'm', 't', 's', 'c',
  'qu', 'jusqu', 'lorsqu', 'puisqu', 'quoiqu',
}

def cleanText(text: str) -> list[str]:
  """Очищает текст и возвращает список слов в нижнем регистре."""
  text = text.lower()

  # Все виды апострофов заменяются на обычный.
  for variant in APOSTROPHE_VARIANTS:
    text = text.replace(variant, '\'')

  # Мусорные символы заменяются пробелом.
  text = ''.join(' ' if ch in REMOVE_SET else ch for ch in text)

  words = []
  for token in text.split():
    token = token.strip('\'-')

    # Французская элизия: l'homme -> homme, qu'aujourd'hui -> aujourd'hui.
    while '\'' in token:
      head, _, tail = token.partition('\'')
      if head in FRENCH_ELISIONS and tail:
        token = tail
      else:
        break

    token = token.strip('\'-')
    if token:
      words.append(token)
  return words

def lexicalDiversity(words: list[str]) -> float:
  """Лексическое разнообразие: число уникальных слов / общее число слов."""
  if not words:
    return 0.0
  return len(set(words)) / len(words)

def rareWordDensity(words: list[str]) -> float:
  """Плотность редких слов: доля слов, встречающихся в тексте ровно один раз."""
  if not words:
    return 0.0
  counts = collections.Counter(words)
  rare = sum(1 for c in counts.values() if c == 1)
  return rare / len(words)
