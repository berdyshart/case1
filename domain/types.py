from dataclasses import dataclass
from enum import Enum, auto


class Language(Enum):
  EN = auto()
  RU = auto()
  DE = auto()
  FR = auto()


class Polarity(Enum):
  POSITIVE = 'positive'
  NEUTRAL = 'neutral'
  NEGATIVE = 'negative'


@dataclass(frozen=True)
class TextStats:
  sentenceCount: int
  wordCount: int
  syllableCount: int
  avgSentenceLength: float
  avgWordSyllables: float


@dataclass(frozen=True)
class AnalysisResult:
  language: Language
  fleschIndex: float
  fleschKincaid: float
  interpretation: str
  polarity: Polarity
  subjectivity: float
  lexicalDiversity: float
  rareWordDensity: float
  stats: TextStats
